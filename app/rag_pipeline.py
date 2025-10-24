import os
from dotenv import load_dotenv
from pathlib import Path

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda

# -----------------------------------------------------------
# 1️⃣ CONFIGURACIÓN INICIAL
# -----------------------------------------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# -----------------------------------------------------------
# 2️⃣ DETECCIÓN AUTOMÁTICA DE FORMATO (PDF o TXT)
# -----------------------------------------------------------
def detectar_tipo_archivo(data_path: str):
    """Detecta si la carpeta contiene PDFs o TXTs"""
    path = Path(data_path)
    pdfs = list(path.glob("*.pdf"))
    txts = list(path.glob("*.txt"))
    if pdfs and not txts:
        return "pdf"
    elif txts and not pdfs:
        return "txt"
    elif pdfs and txts:
        return "mixto"
    else:
        raise FileNotFoundError(f"⚠️ No se encontraron archivos en {data_path}")


# -----------------------------------------------------------
# 3️⃣ INGESTA Y VECTORSTORE
# -----------------------------------------------------------
def save_vectorstore(data_path: str = "data/pdfs",
                     chunk_size: int = 512,
                     chunk_overlap: int = 50):
    """
    Carga los documentos (PDF o TXT) desde data_path,
    genera embeddings y guarda un índice FAISS localmente.
    """
    tipo = detectar_tipo_archivo(data_path)
    print(f"📂 Cargando documentos desde: {data_path} ({tipo.upper()})")

    if tipo == "pdf":
        loader = DirectoryLoader(data_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
    else:
        loader = DirectoryLoader(data_path, glob="**/*.txt", loader_cls=TextLoader)

    documents = loader.load()
    print(f"🧾 Se cargaron {len(documents)} documentos.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                              chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(documents)
    print(f"✂️  Documentos divididos en {len(chunks)} fragmentos.")

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectordb = FAISS.from_documents(chunks, embeddings)

    os.makedirs("vectorstore", exist_ok=True)
    vectordb.save_local("vectorstore")
    print("✅ Vectorstore guardado en ./vectorstore/")


def load_vectorstore_from_disk():
    """Carga el índice FAISS desde ./vectorstore"""
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectordb = FAISS.load_local("vectorstore", embeddings,
                                allow_dangerous_deserialization=True)
    print("✅ Vectorstore cargado desde disco.")
    return vectordb


# -----------------------------------------------------------
# 4️⃣ PIPELINE RAG MODERNO (LangChain ≥ 0.3.x)
# -----------------------------------------------------------
def build_chain(vectordb, prompt_version: str = "v6_asistente_bienestar_cercano"):
    """
    Construye un pipeline RAG moderno compatible con chain.invoke()
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    system_prompt = (
        "Eres el Asistente de Bienestar Medellín. "
        "Responde con empatía, naturalidad y precisión, "
        "usando solo información confiable de los documentos. "
        "Si no tienes información suficiente, dilo claramente."
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ])

    # ✅ versión moderna con retriever.invoke() y RunnableLambda
    def retrieve_context(inputs):
        question = inputs["question"]
        docs = retriever.invoke(question)
        context = "\n\n".join([doc.page_content for doc in docs])
        return {
            "context": context,
            "question": question,
            "chat_history": inputs.get("chat_history", []),
        }

    chain = (
        RunnableLambda(retrieve_context)
        | prompt
        | llm
    )

    print(f"🤖 Cadena RAG construida con prompt: {prompt_version}")
    return chain


# -----------------------------------------------------------
# 5️⃣ PRUEBA LOCAL
# -----------------------------------------------------------
if __name__ == "__main__":
    save_vectorstore("data/pdfs")  # o "data/processed_txt" si ya convertiste
    vectordb = load_vectorstore_from_disk()
    chain = build_chain(vectordb)
    result = chain.invoke({
        "question": "¿Qué recomienda el asistente para una dieta saludable?",
        "chat_history": []
    })
    print("💬", result)
