# 💚 Asistente de Bienestar Medellín – GenAIOps 2025

Este proyecto implementa un **Asistente Virtual de Bienestar** basado en **RAG (Retrieval-Augmented Generation)** y evaluado con **MLflow**, dentro del contexto del curso **Minería de Grandes Volúmenes de Datos – EAFIT**.  
El asistente responde preguntas sobre **alimentación saludable, pausas activas y bienestar físico y mental** utilizando información contenida en documentos PDF procesados localmente.

---

## 🧱 Arquitectura del Proyecto

GenAIOps_Pycon2025/
│
├── app/
│ ├── rag_pipeline.py # Construcción del pipeline RAG (vectorstore + retrieval chain)
│ ├── ui_streamlit.py # Interfaz del chatbot (Streamlit)
│ ├── run_eval.py # Evaluación automática con MLflow
│ ├── dashboard.py # Visualización de métricas y resultados
│ ├── prompts/ # Versiones del prompt (v1_asistente_bienestar, etc.)
│ └── init.py
│
├── data/
│ ├── pdfs/ # Documentos base del dominio
│ └── processed_txt/ # Textos procesados y fragmentados
│
├── vectorstore/ # Almacenamiento FAISS del conocimiento indexado
├── tests/
│ ├── eval_dataset.json # Dataset de evaluación (preguntas + respuestas esperadas)
│ └── test_run_eval.py # Pruebas automatizadas de evaluación
│
├── .env # Variables de entorno (API keys y configuración)
├── requirements.txt
└── README.md

yaml
Copiar código

---

## 🧩 Flujo General del Sistema

1. **Carga de documentos**  
   Los archivos PDF se convierten en texto y se fragmentan en bloques (*chunks*) con `rag_pipeline.py`.

2. **Construcción del vectorstore (FAISS)**  
   Cada fragmento se transforma en un vector y se guarda localmente para búsquedas semánticas eficientes.

3. **Ejecución del chatbot (Streamlit)**  
   El modelo consulta el vectorstore, recupera información relevante y genera una respuesta contextual.

4. **Evaluación automática con MLflow**  
   Las respuestas se comparan con un conjunto de referencia y se registran métricas de desempeño.

5. **Dashboard interactivo**  
   Permite visualizar precisión, coherencia y métricas multicriterio por configuración de prompt y chunk.

---

## 🚀 Ejecución del Proyecto

### 1️⃣ Configuración inicial

Clona el repositorio e instala las dependencias:

```bash
git clone https://github.com/tiagog20/GenAIOps_Pycon2025.git
cd GenAIOps_Pycon2025
pip install -r requirements.txt
Crea el archivo .env con tu configuración:

bash
Copiar código
OPENAI_API_KEY=tu_api_key
PROMPT_VERSION=v1_asistente_bienestar
CHUNK_SIZE=512
CHUNK_OVERLAP=50
2️⃣ Construcción de la base de conocimiento
Ejecuta el pipeline para procesar los PDF y generar el vectorstore:

bash
Copiar código
python -c "from app.rag_pipeline import save_vectorstore; save_vectorstore('data/processed_txt')"
Esto crea la base vectorial FAISS que el asistente usará para recuperar contexto.

3️⃣ Ejecución del Chatbot
Inicia la aplicación Streamlit:

bash
Copiar código
streamlit run app/ui_streamlit.py
Desde la interfaz podrás interactuar con el Asistente de Bienestar Medellín, que responde preguntas sobre hábitos saludables, nutrición o pausas activas.

4️⃣ Evaluación Automática
Ejecuta la evaluación con MLflow:

bash
Copiar código
python app/run_eval.py
Esto compara las respuestas generadas por el modelo con las respuestas esperadas (tests/eval_dataset.json)
y registra métricas como correctness, relevance, coherence, toxicity, harmfulness, y un GenAIOps Score promedio.

Visualiza los resultados:

bash
Copiar código
mlflow ui
Abre http://localhost:5000 en tu navegador.

5️⃣ Visualización en Dashboard
Ejecuta el panel de métricas:

bash
Copiar código
streamlit run app/dashboard.py
El dashboard permite:

Ver resultados individuales por pregunta

Comparar configuraciones de prompt_version y chunk_size

Analizar métricas promedio (sin mapa de calor 🌈, interfaz limpia y moderna)

📊 Ejemplo de Resultados
Pregunta	Correctness	Relevance	Coherence	Toxicity	Harmfulness	GenAIOps Score
¿Qué recomienda la guía nacional para la hidratación diaria?	1.0	0.9	0.85	0.0	0.0	0.91
¿Qué prácticas promueven una buena salud mental?	0.8	0.88	0.83	0.0	0.0	0.84
¿Qué alimentos deben evitarse en exceso?	1.0	0.9	0.86	0.0	0.0	0.92

Promedio global: 0.86 ✅
El asistente muestra buena coherencia y relevancia en el dominio de bienestar.

🎓 Desafío para Estudiantes
Este proyecto es también un reto de GenAIOps diseñado para que los estudiantes extiendan, evalúen y mejoren el sistema.

🧩 Parte 1: Personalización
Elige un nuevo dominio: salud, educación, legal, energía, bancario, etc.

Reemplaza los documentos PDF: agrégalos en data/pdfs/.

Modifica o crea prompts: en app/prompts/.

Crea tu dataset de evaluación: en tests/eval_dataset.json.

✅ Parte 2: Evaluación Automática
Ejecuta:

bash
Copiar código
python app/run_eval.py
Evalúa el rendimiento con métricas binarias (correcto / incorrecto) y registra resultados en MLflow.

🔧 Parte 3: Nivel Investigador – Evaluación Multicriterio
Implementa evaluación con LabeledCriteriaEvalChain (LangChain) para analizar:

correctness – ¿Es correcta la respuesta?

relevance – ¿Es relevante respecto a la pregunta?

coherence – ¿Está bien estructurada la respuesta?

toxicity – ¿Contiene lenguaje ofensivo?

harmfulness – ¿Podría causar daño la información?

Cada criterio debe:

Registrar una métrica (score) en MLflow

(Opcional) Guardar un razonamiento (reasoning)

📚 Referencia: LabeledCriteriaEvalChain – LangChain Docs

📊 Parte 4: Mejora del Dashboard
Extiende app/dashboard.py para visualizar:

Métricas por criterio (correctness, coherence, toxicity, etc.)

Comparaciones entre configuraciones

(Opcional) Razonamientos textuales del modelo

🧪 Parte 5: Presenta y Reflexiona
Compara configuraciones distintas (chunk_size, prompt_version) y justifica tu selección.

Pregúntate:

¿Qué configuración genera mejores respuestas?

¿En qué fallan los modelos?

¿Fueron incoherentes o riesgosos?

Usa las métricas de MLflow y capturas del dashboard como evidencia.

🚀 Bonus
Crea nuevos criterios personalizados con LabeledCriteriaEvalChain, como:

clarity – claridad y redacción

creativity – innovación o expresividad

💡 Conclusiones
El Asistente de Bienestar Medellín demuestra una aplicación práctica de principios GenAIOps:

Modularidad y reproducibilidad

Evaluación cuantitativa con MLflow

Trazabilidad de prompts y configuraciones

Interfaz accesible y contextual

💬 “La tecnología al servicio del bienestar humano.”

👨‍🏫 Créditos
Autores: Santiago González Granada & María del Rosario Castro Mantilla
Universidad: EAFIT – Maestría en Ciencia de los Datos y Analítica
Curso: Minería de Grandes Volúmenes de Datos
Taller: GenAIOps 2025 – Chatbots Evaluables con LangChain y MLflow