# Nexcell AI Agent 

Microservicio RESTful desarrollado en Python que actúa como motor cognitivo para el ecosistema Nexcell. Permite integrar capacidades de procesamiento de lenguaje natural (NLP) conectando sistemas cliente externos con modelos de lenguaje a través de la API de Groq.

##  Tecnologías
* **Python 3.x**
* **FastAPI** (Framework web)
* **Uvicorn** (Servidor ASGI)
* **Groq API** (Inferencia de LLMs ultrarrápida)

##  Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/agustinrgomezz/nexcell-ai-agent.git](https://github.com/agustinrgomezz/nexcell-ai-agent.git)
   cd nexcell-ai-agent
   ```

2. **Instalar las dependencias requeridas:**
   ```bash
   pip install fastapi uvicorn groq
   ```

3. **Configuración de la API Key:**
   Para que el agente se conecte al modelo de lenguaje, se necesita configurar tu propia API Key de Groq como variable de entorno o directamente en tu archivo de configuración .

4. **Ejecutar el servidor local:**
   Levanta el microservicio utilizando Uvicorn:
   ```bash
   uvicorn api:app --reload
   ```

5. **Prueba y Documentación:**
   El servidor quedará a la escucha en `http://127.0.0.1:8000`. 
   
   FastAPI genera documentación interactiva automáticamente. Puedes probar el endpoint `/chat` directamente desde tu navegador entrando a:
    **`http://127.0.0.1:8000/docs`**
