# app/ui_streamlit.py
import sys, os, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from app.rag_pipeline import load_vectorstore_from_disk, build_chain

# -----------------------------------------------------------
# 1️⃣ CONFIGURACIÓN Y ESTILO PERSONALIZADO
# -----------------------------------------------------------
st.set_page_config(
    page_title="Asistente de Bienestar Medellín",
    page_icon="💚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    body {
        font-family: 'DejaVu Sans', sans-serif;
        background-color: #F5F9F6;
        color: #333333;
    }
    .main {
        background-color: #F5F9F6;
    }
    h1 {
        color: #2E7D32;
        text-align: center;
        font-weight: 800;
        margin-bottom: 0.2em;
    }
    .subheader {
        color: #4F4F4F;
        text-align: center;
        font-size: 1.05em;
        margin-bottom: 1.2em;
    }
    .banner {
        background: linear-gradient(90deg, #A5D6A7, #81C784, #66BB6A);
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 20px;
        color: white;
        font-weight: 600;
        font-size: 1em;
        text-align: center;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.2);
    }
    .user-bubble {
        background-color: #E8F5E9;
        color: #2E7D32;
        padding: 0.7em 1em;
        border-radius: 1em;
        margin: 0.4em 0;
        width: fit-content;
        max-width: 80%;
    }
    .bot-bubble {
        background-color: #C8E6C9;
        color: #1B5E20;
        padding: 0.7em 1em;
        border-radius: 1em;
        margin: 0.4em 0;
        width: fit-content;
        max-width: 80%;
        align-self: flex-end;
    }
    .chat-container {
        display: flex;
        flex-direction: column-reverse;
    }
    .clean-btn button {
        background-color: #81C784 !important;
        color: white !important;
        border-radius: 10px;
        font-weight: 600;
        border: none;
        transition: 0.3s;
    }
    .clean-btn button:hover {
        background-color: #66BB6A !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------
# 2️⃣ BANNER SUPERIOR (personalizable)
# -----------------------------------------------------------
st.markdown(
    """
    <div class='banner'>
        🌿 <b>Universidad EAFIT · Taller de GenAIOps</b> — Chatbot de Bienestar y Vida Saludable 🌿
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------
# 3️⃣ ENCABEZADO PRINCIPAL
# -----------------------------------------------------------
st.markdown("<h1>💚 Asistente de Bienestar Medellín</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subheader'>Tu guía en hábitos saludables, bienestar y estilo de vida en Medellín.<br>Pregúntame sobre alimentación, pausas activas o autocuidado 🧘‍♀️</p>",
    unsafe_allow_html=True
)

# -----------------------------------------------------------
# 4️⃣ INPUT Y BOTÓN REINICIO
# -----------------------------------------------------------
col1, col2 = st.columns([4, 1])
with col1:
    question = st.text_input(
        "💭 Escribe tu pregunta sobre salud o bienestar:",
        placeholder="Ejemplo: ¿Qué puedo comer para tener más energía?"
    )
with col2:
    st.markdown("<div class='clean-btn'>", unsafe_allow_html=True)
    if st.button("🧘 Reiniciar"):
        st.session_state.chat_history = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------
# 5️⃣ ESTADO DEL CHAT
# -----------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------------------------------------
# 6️⃣ CARGAR RAG
# -----------------------------------------------------------
vectordb = load_vectorstore_from_disk()
chain = build_chain(vectordb)

# -----------------------------------------------------------
# 7️⃣ PROCESAR PREGUNTA
# -----------------------------------------------------------
if question:
    with st.spinner("Pensando... 💭"):
        chat_history_lc = []
        for q, a in st.session_state.chat_history:
            chat_history_lc.append(HumanMessage(content=q))
            chat_history_lc.append(AIMessage(content=a))

        result = chain.invoke({"question": question, "chat_history": chat_history_lc})

        if hasattr(result, "content"):
            answer = result.content
        elif isinstance(result, dict) and "answer" in result:
            answer = result["answer"]
        else:
            answer = str(result)

        # 🔹 Simular escritura del bot (animación)
        placeholder = st.empty()
        animated = ""
        for char in answer:
            animated += char
            placeholder.markdown(
                f"<div class='bot-bubble'><b>🤖 Asistente:</b> {animated}▌</div>",
                unsafe_allow_html=True,
            )
            time.sleep(0.01)
        placeholder.markdown(
            f"<div class='bot-bubble'><b>🤖 Asistente:</b> {answer}</div>",
            unsafe_allow_html=True,
        )

        st.session_state.chat_history.append((question, answer))

# -----------------------------------------------------------
# 8️⃣ HISTORIAL
# -----------------------------------------------------------
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("## 🗨️ Conversación")
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    for q, a in reversed(st.session_state.chat_history[:-1]):
        st.markdown(f"<div class='user-bubble'><b>🧑 Tú:</b> {q}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='bot-bubble'><b>🤖 Asistente:</b> {a}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
