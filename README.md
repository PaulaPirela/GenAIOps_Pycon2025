## Asistente de IA (GenAIOps 2025)
Este proyecto desarrolla e implementa un Asistente Virtual basado en la arquitectura RAG (Retrieval-Augmented Generation), con un enfoque en la evaluación rigurosa mediante MLflow. Fue concebido para el curso Minería de Grandes Volúmenes de Datos – EAFIT.

El asistente está diseñado para responder consultas sobre temas de salud preventiva y estilo de vida (como alimentación saludable, pausas activas y bienestar físico y mental), utilizando exclusivamente el contenido de documentos PDF internos procesados localmente. El rol configurado (Portavoz Institucional y Analista de Políticas) le exige comunicar de forma formal y técnica las directrices oficiales.


## Arquitectura y Estructura del Proyecto
El proyecto sigue una estructura modular que facilita la implementación de la pipeline RAG y su posterior evaluación:

GenAIOps_Pycon2025/
├── app/
│ ├── rag_pipeline.py    # Lógica de RAG: vectorstore y retrieval chain
│ ├── ui_streamlit.py    # Interfaz de usuario del chatbot (Streamlit)
│ ├── run_eval.py        # Script para la evaluación automatizada con MLflow
│ ├── dashboard.py       # Panel de visualización de métricas
│ ├── prompts/           # Directorio para las distintas versiones del prompt
├── data/
│ ├── pdfs/              # Documentos base del dominio
│ └── processed_txt/     # Textos pre-procesados y fragmentados
├── vectorstore/         # Almacenamiento FAISS del conocimiento indexado
├── tests/
│ ├── eval_dataset.json  # Dataset de evaluación (preguntas y respuestas de referencia)
├── .env                 # Variables de entorno (API keys y configuración)
├── requirements.txt
└── README.md

## Flujo Operacional del Sistema
1. Carga y Fragmentación: Los archivos PDF se procesan en rag_pipeline.py, convirtiéndose en texto y fragmentándose en bloques (chunks).

2. Construcción del Vectorstore (FAISS): Los fragmentos son vectorizados y almacenados localmente para permitir búsquedas semánticas eficientes.

3. Ejecución del Chatbot (Streamlit): El modelo recupera contexto relevante del vectorstore y genera respuestas contextuales a las preguntas del usuario.

4. Evaluación con MLflow: Se realiza una evaluación automática (run_eval.py) comparando las respuestas generadas contra un conjunto de referencia, registrando métricas de desempeño.

5. Dashboard Interactivo: dashboard.py permite la visualización de métricas como precisión, coherencia, y el GenAIOps Score promedio, con la capacidad de comparar diferentes configuraciones de prompt y tamaño de chunk.


## Ejecución del Proyecto
1. Configuración y Dependencias
Clonar el repositorio e instalar dependencias:

git clone https://github.com/PaulaPirela/GenAIOps_Pycon2025.git
cd GenAIOps_Pycon2025
pip install -r requirements.txt

Crear el archivo .env para la configuración:
OPENAI_API_KEY=tu_api_key
PROMPT_VERSION=v1_asistente_bienestar
CHUNK_SIZE=512
CHUNK_OVERLAP=50

2. Construcción de la Base de Conocimiento
Procesar los documentos PDF para crear el almacén vectorial FAISS:
python -c "from app.rag_pipeline import save_vectorstore; save_vectorstore('data/processed_txt')"

3. Interacción con el Chatbot
Iniciar la interfaz de la aplicación Streamlit:
streamlit run app/ui_streamlit.py

4. Evaluación Automática
Ejecutar la comparación con el dataset de referencia e iniciar el registro de métricas en MLflow:
python app/run_eval.py

Visualizar los resultados de MLflow en el navegador:
mlflow ui
(Abrir http://localhost:5000)

5. Visualización de Métricas
Iniciar el panel de métricas y resultados:
streamlit run app/dashboard.py

README del Asistente de IA (GenAIOps 2025)
Este proyecto desarrolla e implementa un Asistente Virtual basado en la arquitectura RAG (Retrieval-Augmented Generation), con un enfoque en la evaluación rigurosa mediante MLflow. Fue concebido para el curso Minería de Grandes Volúmenes de Datos – EAFIT.

El asistente está diseñado para responder consultas sobre temas de salud preventiva y estilo de vida (como alimentación saludable, pausas activas y bienestar físico y mental), utilizando exclusivamente el contenido de documentos PDF internos procesados localmente. El rol configurado (Portavoz Institucional y Analista de Políticas) le exige comunicar de forma formal y técnica las directrices oficiales.

Arquitectura y Estructura del Proyecto
El proyecto sigue una estructura modular que facilita la implementación de la pipeline RAG y su posterior evaluación:

GenAIOps_Pycon2025/
├── app/
│ ├── rag_pipeline.py    # Lógica de RAG: vectorstore y retrieval chain
│ ├── ui_streamlit.py    # Interfaz de usuario del chatbot (Streamlit)
│ ├── run_eval.py        # Script para la evaluación automatizada con MLflow
│ ├── dashboard.py       # Panel de visualización de métricas
│ ├── prompts/           # Directorio para las distintas versiones del prompt
├── data/
│ ├── pdfs/              # Documentos base del dominio
│ └── processed_txt/     # Textos pre-procesados y fragmentados
├── vectorstore/         # Almacenamiento FAISS del conocimiento indexado
├── tests/
│ ├── eval_dataset.json  # Dataset de evaluación (preguntas y respuestas de referencia)
├── .env                 # Variables de entorno (API keys y configuración)
├── requirements.txt
└── README.md
Flujo Operacional del Sistema
Carga y Fragmentación: Los archivos PDF se procesan en rag_pipeline.py, convirtiéndose en texto y fragmentándose en bloques (chunks).

Construcción del Vectorstore (FAISS): Los fragmentos son vectorizados y almacenados localmente para permitir búsquedas semánticas eficientes.

Ejecución del Chatbot (Streamlit): El modelo recupera contexto relevante del vectorstore y genera respuestas contextuales a las preguntas del usuario.

Evaluación con MLflow: Se realiza una evaluación automática (run_eval.py) comparando las respuestas generadas contra un conjunto de referencia, registrando métricas de desempeño.

Dashboard Interactivo: dashboard.py permite la visualización de métricas como precisión, coherencia, y el GenAIOps Score promedio, con la capacidad de comparar diferentes configuraciones de prompt y tamaño de chunk.

Ejecución del Proyecto
1. Configuración y Dependencias
Clonar el repositorio e instalar dependencias:

Bash

git clone https://github.com/PaulaPirela//GenAIOps_Pycon2025.git
cd GenAIOps_Pycon2025
pip install -r requirements.txt
Crear el archivo .env para la configuración:

Bash

OPENAI_API_KEY=tu_api_key
PROMPT_VERSION=v1_asistente_bienestar
CHUNK_SIZE=512
CHUNK_OVERLAP=50
2. Construcción de la Base de Conocimiento
Procesar los documentos PDF para crear el almacén vectorial FAISS:

Bash

python -c "from app.rag_pipeline import save_vectorstore; save_vectorstore('data/processed_txt')"
3. Interacción con el Chatbot
Iniciar la interfaz de la aplicación Streamlit:

Bash

streamlit run app/ui_streamlit.py
4. Evaluación Automática
Ejecutar la comparación con el dataset de referencia e iniciar el registro de métricas en MLflow:

Bash

python app/run_eval.py
Visualizar los resultados de MLflow en el navegador:

Bash

mlflow ui
(Abrir http://localhost:5000)

5. Visualización de Métricas
Iniciar el panel de métricas y resultados:

Bash

streamlit run app/dashboard.py

## Desafío y Extensión (GenAIOps para Estudiantes)
El proyecto sirve como un reto de GenAIOps para la mejora continua del sistema, enfocándose en la modularidad y la evaluación cuantitativa:

1. Personalización: Adaptar el asistente a un nuevo dominio (reemplazo de documentos PDF y creación de un nuevo dataset de evaluación).

2. Evaluación Automática: Ejecución y registro de métricas binarias de rendimiento en MLflow.

Nivel Investigador – Evaluación Multicriterio: Implementación de LabeledCriteriaEvalChain de LangChain para analizar métricas detalladas:
1. correctness, relevance, coherence.

2. oxicity, harmfulness.

3. Registro del score y el razonamiento para cada criterio.

3. Mejora del Dashboard: Extensión de app/dashboard.py para visualizar métricas por criterio y comparaciones de configuración.

4. Análisis y Reflexión: Comparación de diferentes configuraciones (chunk_size, prompt_version) usando la evidencia de las métricas de MLflow para justificar la mejor selección.

5. Bonus: Creación de criterios personalizados (clarity, creativity) para la evaluación.

## Conclusiones
El Asistente de IA demuestra una aplicación práctica de principios GenAIOps, destacando la modularidad, la reproducibilidad, la trazabilidad de configuraciones (prompts, chunks), y la evaluación cuantitativa con MLflow para garantizar la calidad y coherencia de las respuestas.
