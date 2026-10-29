from model import preguntar
from tools import sumar

MODEL = "qwen3:4b"

HERRAMIENTAS = [sumar]

#creamos una función que reciba un mensaje y devuelva la respuesta del modelo
def ejecutar(mensaje): 

    mensajes = [
        {
        "role": "system",
        "content": (
            "Eres un asistente útil y conversacional. "
            "Cuando utilices una herramienta, explica al usuario "
            "el resultado de forma natural y breve. "
            "No afirmes haber utilizado herramientas si no las has utilizado."
        )
    },
        {
            "role": "user",
            "content": mensaje
        }
    ]
    # Primera llamada: el modelo decide qué hacer
    respuesta = preguntar(mensajes, HERRAMIENTAS) # llamamos a la función preguntar del archivo model.py para obtener la respuesta del modelo

     # Guardamos la respuesta del modelo en el historial
    mensajes.append(respuesta)

     # Comprobar si el modelo solicita una herramienta
    if respuesta.tool_calls:

        for llamada in respuesta.tool_calls:
            nombre = llamada.function.name
            argumentos = llamada.function.arguments

            # Ejecutar la herramienta correspondiente
            if nombre == "sumar":
                a = int(argumentos["a"])
                b = int(argumentos["b"])

                print(f"\n[HERRAMIENTA EJECUTADA] sumar({a}, {b})")

                resultado = sumar(a, b)

            else:
                raise ValueError(f"Herramienta no permitida: {nombre}")

            # Devolvemos el resultado de la herramienta al modelo
            mensajes.append({
                "role": "tool",
                "tool_name": nombre,
                "content": str(resultado)
            })

            # Segunda llamada: el modelo redacta la respuesta final
        respuesta_final = preguntar(mensajes)

        return respuesta_final.content

    # Si no solicita herramientas, devolver su respuesta normal
    return respuesta.content