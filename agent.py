from model import preguntar
from tools import sumar

#creamos una función que reciba un mensaje y devuelva la respuesta del modelo
def ejecutar(mensaje): 
    respuesta = preguntar(mensaje) # llamamos a la función preguntar del archivo model.py para obtener la respuesta del modelo

     # Comprobar si el modelo solicita una herramienta
    if respuesta.message.tool_calls:

        for llamada in respuesta.message.tool_calls:
            nombre = llamada.function.name
            argumentos = llamada.function.arguments

            # Ejecutar la herramienta correspondiente
            if nombre == "sumar":
                a = int(argumentos["a"])
                b = int(argumentos["b"])

                resultado = sumar(a, b)

                return f"El resultado de sumar {a} + {b} es {resultado}"

    # Si no solicita herramientas, devolver su respuesta normal
    return respuesta.message.content