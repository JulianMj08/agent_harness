from ollama import chat
from tools import sumar

def preguntar(mensaje, herramientas=None): # la función preguntar recibe un mensaje y una lista de herramientas (opcional) y devuelve la respuesta del modelo
    response = chat(
        model="qwen3:4b",
        messages=mensaje,
        tools=herramientas or [] # si no se pasan herramientas, se pasa una lista vacía
    )
    return response.message