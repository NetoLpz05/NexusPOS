from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str    
    user_id: str = None

@app.post("/api/chat")
async def chat_with_ia(data: ChatMessage):
    return {"response": f"¡Hola! Recibí tu mensaje: '{data.message}'. Pronto te daré detalles de nuestros videojuegos."}