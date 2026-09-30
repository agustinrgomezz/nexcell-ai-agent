import os
from openai import OpenAI
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

class AgenteNexcell:
    def __init__(self):
        # Configuramos el cliente para usar la API de Groq (que es compatible con la librería openai)
        self.cliente = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        self.modelo = "qwen/qwen3.8-27b"
        self.historial = []
        self._inicializar_contexto()

    def _inicializar_contexto(self):
        # El System Prompt define la personalidad y los límites del bot
        prompt_sistema = (
            "Eres el asistente virtual técnico de Nexcell, un e-commerce de celulares. "
            "Tu tarea es ayudar a los clientes con consultas sobre dispositivos, "
            "recomendaciones tecnológicas y soporte de compras. Responde de forma "
            "clara, profesional y concisa (máximo 3 párrafos cortos)."
        )
        self.historial.append({"role": "system", "content": prompt_sistema})

    def procesar_mensaje(self, mensaje_usuario):
        # 1. Agregamos lo que dice el usuario al historial
        self.historial.append({"role": "user", "content": mensaje_usuario})

        try:
            # 2. Hacemos la llamada a la API enviando TODO el historial para mantener el contexto
            respuesta = self.cliente.chat.completions.create(
                model=self.modelo,
                messages=self.historial,
                temperature=0.6,
                max_tokens=300
            )
            
            mensaje_ia = respuesta.choices[0].message.content
            
            # 3. Guardamos la respuesta del agente para que la recuerde en el próximo turno
            self.historial.append({"role": "assistant", "content": mensaje_ia})
            
            return mensaje_ia

        except Exception as e:
            return f"Error en el servidor de Nexcell: {e}"