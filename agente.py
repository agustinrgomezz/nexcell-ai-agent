import os
import mysql.connector
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AgenteNexcell:
    def __init__(self):
        self.cliente = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        self.modelo = "qwen/qwen3.8-27b"
        self.historial = []
        self._inicializar_contexto()

    def _obtener_inventario_db(self):
        try:
            # Conexión a tu MySQL local
            conexion = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASS", ""),
                database=os.getenv("DB_NAME", "nexcell_db"),
                port=os.getenv("DB_PORT", "3307")
            )
            cursor = conexion.cursor(dictionary=True)
            
            # ADAPTÁ ESTA CONSULTA al nombre real de tus tablas en Nexcell
            cursor.execute("SELECT marca, nombre, precio, stock FROM productos WHERE stock > 0 AND estado = 1")
            productos = cursor.fetchall()
            
            conexion.close()
            
            #Ahora armamos un texto para pasarselo a la IA y que lo pueda entender
            if not productos:
                return "Actualmente no hay stock disponible."
                
            texto_inventario = "Inventario actual disponible:\n"
            for p in productos:
                texto_inventario += f"- {p['marca']} {p['nombre']}: ${p['precio']} (Stock: {p['stock']})\n"
                
            return texto_inventario
            
        except Exception as e:
            print(f"Advertencia: No se pudo conectar a la BD ({e}). Usando modo sin stock.")
            return "El sistema de inventario está fuera de línea."

    def _inicializar_contexto(self):
        # 1. Buscamos el stock real en MySQL
        inventario_actual = self._obtener_inventario_db()
        
        # 2. Se lo inyectamos al System Prompt
        prompt_sistema = (
            "Eres el asistente virtual técnico de Nexcell, un e-commerce de celulares. "
            "Tu tarea es ayudar a los clientes basándote ÚNICAMENTE en el siguiente inventario real:\n\n"
            f"{inventario_actual}\n\n"
            "Si un usuario pregunta por un modelo que no está en esta lista, decile amablemente que no hay stock. "
            "Responde de forma clara, profesional y concisa (máximo 3 párrafos cortos)."
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