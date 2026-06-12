import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables desde el archivo .env
load_dotenv()

app = FastAPI()

# Configuración de CORS para comunicarse con Astro (puerto 4321)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321", "http://127.0.0.1:4321"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# Instrucciones del sistema para recuperar la identidad del bot
NEXUS_BOT_INSTRUCTIONS = """
Eres Nexus AI, el asistente virtual oficial de la plataforma Nexus POS (una tienda multiplataforma de videojuegos).
Tu objetivo es ayudar amablemente a los usuarios con dudas sobre:
1. Juegos disponibles en la tienda.
2. Keys (claves) de activación de productos.
3. Historial de compras y soporte técnico básico de la plataforma.

Reglas de comportamiento:
- Responde siempre en español de forma entusiasta, clara y concisa.
- Usa emoticonos relacionados con videojuegos de forma moderada (🎮, 🕹️, 👋, 🚀).
- Usa texto en negrita (**texto**) para resaltar elementos importantes o nombres de juegos.
- Si el usuario te saluda, dale la bienvenida formal a Nexus POS.
- Si te preguntan algo totalmente ajeno a los videojuegos o a la tienda, redirige la conversación amablemente hacia el ecosistema de Nexus POS.
"""

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    
    # INSPECTOR DE CONFIGURACIÓN OPENROUTER
    print("\n" + "="*50)
    print("🤖 CONFIGURACIÓN DETECTADA PARA OPENROUTER:")
    print(f"¿La variable existe?: {api_key is not None}")
    if api_key:
        print(f"Longitud: {len(api_key)} caracteres")
        print(f"¿Es formato OpenRouter? (sk-or-v1): {api_key.startswith('sk-or-v1')}")
    print("="*50 + "\n")
    
    if not api_key:
        raise HTTPException(
            status_code=500, 
            detail="La API Key no está configurada en el archivo .env."
        )
        
    try:
        # Se inicializa el cliente apuntando a los servidores de OpenRouter
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        # Llamada estructurada al estilo OpenAI/OpenRouter buscando a Gemini
        response = client.chat.completions.create(
            model="google/gemini-2.5-flash",  # Id del modelo en OpenRouter
            messages=[
                {
                    "role": "system",
                    "content": NEXUS_BOT_INSTRUCTIONS
                },
                {
                    "role": "user",
                    "content": request.message
                }
            ],
            temperature=0.7
        )
        
        # Se extrae el texto de la respuesta
        bot_response = response.choices[0].message.content
        return {"response": bot_response}
        
    except Exception as e:
        print(f"❌ Error en OpenRouter/Gemini: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno al procesar con OpenRouter: {str(e)}"
        )