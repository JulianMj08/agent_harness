from ollama import chat
from tools import sumar

def preguntar(mensaje):
    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": mensaje
            }
        ],
        tools=[sumar]
    )
    return response