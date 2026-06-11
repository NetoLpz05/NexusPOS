import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Cargar las variables de entorno antes de inicializar cualquier cliente
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# El SDK de google-genai busca automáticamente la variable "GEMINI_API_KEY" en el entorno
try:
    client = genai.Client()
except Exception as e:
    print(f"Error crítico: No se pudo inicializar el cliente de Gemini. Verifica tu GEMINI_API_KEY. Detalle: {e}")

class ChatMessage(BaseModel):
    message: str    
    user_id: str = None

SYSTEM_INSTRUCTION = """
Eres NEXUS AI, el asistente virtual oficial de 'Nexus POS', una tienda premium de videojuegos digitales.
Tu objetivo es resolver dudas de los usuarios con un tono tecnológico, entusiasta, amigable y sumamente eficiente.

Sigue estrictamente estas directrices:
1. INFORMACIÓN SOBRE PRODUCTOS: Si te preguntan qué juegos hay disponibles, di que ofreces un catálogo variado de claves digitales (Steam, Epic Games, PlayStation, Xbox) con los mejores precios del mercado y que pueden explorarlos en la tienda principal.
2. HISTORIAL Y CÓDIGOS (KEYS): Si el usuario pregunta por sus códigos adquiridos, indícale de forma clara que debe ir a su 'Perfil' (haciendo clic en su avatar arriba a la derecha) y seleccionar la pestaña 'Historial de Compras'.
3. GUARDAR FAVORITOS: Explícales que pueden marcar cualquier juego con el ícono del corazón (❤️) para tenerlo guardado en la sección 'Mis Favoritos' de su perfil.
4. SOPORTE TÉCNICO Y ERRORES DE PAGO: Si mencionan fallas en el carrito, errores de pago (como el aviso de 'error crítico' o códigos 403), o problemas de autenticación, diles amablemente que se trata de un problema técnico temporal y que pueden contactar de inmediato a soporte@nexuspos.com para solucionarlo de forma personalizada.
5. CONCISIÓN: Mantén tus respuestas breves, estructuradas con viñetas si es necesario, y usa emojis relacionados con el gaming (🎮, 📦, 🔑, 🤖). Nunca salgas de tu rol de asistente de Nexus POS.
"""

@app.post("/api/chat")
async def chat_with_ia(data: ChatMessage):
    if not data.message.strip():
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío.")
        
    try:
        # Llamada oficial al modelo gemini-2.5-flash usando la nueva arquitectura de Google GenAI
        response = client.models.generate_content(
            model='gemini-3.0-flash',
            contents=data.message,
            config={
                'system_instruction': SYSTEM_INSTRUCTION,
                'temperature': 0.7
            }
        )
        
        # Devolvemos la respuesta formateada en JSON
        return {"response": response.text}
        
    except Exception as e:
        print(f"Error interno con Gemini API: {e}")
        raise HTTPException(status_code=500, detail="Error al procesar tu solicitud con el servicio de IA.")