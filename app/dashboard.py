# app/dashboard.py

import mlflow
import pandas as pd
import streamlit as st

# -----------------------------------------------------------
# CONFIGURACIÓN INICIAL
# -----------------------------------------------------------
st.set_page_config(page_title="📊 Dashboard General de Evaluación", layout="wide")
st.title("💚 Evaluación del Asistente de Bienestar Medellín")

client = mlflow.tracking.MlflowClient()

# -----------------------------------------------------------
# CARGAR EXPERIMENTOS
# -----------------------------------------------------------
experiments = [exp for exp in client.search_experiments() if exp.name.startswith("eval_")]

if not experiments:
    st.warning("⚠️ No se encontraron experimentos con nombre que empiece por 'eval_'.")
    st.stop()

exp_names = [exp.name for exp in experiments]
selected_exp_name = st.selectbox("📁 Selecciona un experimento:", exp_names)

experiment = client.get_experiment_by_name(selected_exp_name)
runs = client.search_runs(experiment_ids=[experiment.experiment_id], order_by=["start_time DESC"])

if not runs:
    st.warning("⚠️ No hay ejecuciones registradas en este experimento.")
    st.stop()

# -----------------------------------------------------------
# PROCESAR DATOS DE RUNS
# -----------------------------------------------------------
data = []
for run in runs:
    params = run.data.params
    metrics = run.data.metrics
    data.append({
        "Pregunta": params.get("question"),
        "Prompt Version": params.get("prompt_version"),
        "Chunk Size": int(params.get("chunk_size", 0)),
        "Overlap": int(params.get("chunk_overlap", 0)),
        "Correctness": metrics.get("correctness", 0),
        "Relevance": metrics.get("relevance", 0),
        "Coherence": metrics.get("coherence", 0),
        "Toxicity": metrics.get("toxicity", 0),
        "Harmfulness": metrics.get("harmfulness", 0),
        "GenAIOps Score": metrics.get("genaiops_score", 0)
    })

df = pd.DataFrame(data)

# -----------------------------------------------------------
# VISUALIZAR DATOS
# -----------------------------------------------------------
st.subheader("📋 Resultados individuales por pregunta")
st.dataframe(df, width="stretch")

# -----------------------------------------------------------
# ANÁLISIS PROMEDIO
# -----------------------------------------------------------
st.subheader("📈 Promedios por criterio")

mean_df = df[["Correctness", "Relevance", "Coherence", "Toxicity", "Harmfulness", "GenAIOps Score"]].mean().reset_index()
mean_df.columns = ["Criterio", "Promedio"]
mean_df["Promedio"] = mean_df["Promedio"].round(3)

col1, col2 = st.columns([1, 2])

with col1:
    st.dataframe(mean_df, width="stretch")

with col2:
    st.bar_chart(mean_df.set_index("Criterio"), width="stretch")

# -----------------------------------------------------------
# CONFIGURACIONES
# -----------------------------------------------------------
st.subheader("⚙️ Comparación de configuraciones")
grouped = df.groupby(["Prompt Version", "Chunk Size"]).agg(
    Promedio_GenAIOps=("GenAIOps Score", "mean"),
    Num_Preguntas=("Pregunta", "count")
).reset_index()

st.dataframe(grouped, width="stretch")

st.success("✅ Dashboard actualizado — sin mapa de calor, con métricas limpias y comparaciones configurables.")
