from pprint import pprint
from model import preguntar
from tools import sumar, restar, multiplicar

MODEL = "qwen3:4b"

# Herramientas que el modelo puede solicitar
HERRAMIENTAS = [sumar, restar, multiplicar]

# Registro que relaciona cada nombre con su función Python
REGISTRO_HERRAMIENTAS = {
    funcion.__name__: funcion
    for funcion in HERRAMIENTAS
}

# Límite de iteraciones para evitar bucles infinitos
MAX_ITERACIONES = 10

# Historial persistente durante la ejecución del programa, aca se guardara el historial de la conversación, incluyendo los mensajes del usuario, las respuestas del modelo y los resultados de las herramientas
MENSAJES = [
    {
        "role": "system",
        "content": (
            "Eres un asistente útil y conversacional. "
            "Puedes utilizar herramientas matemáticas. "
            "Ten en cuenta el contexto de la conversación anterior."
            "Responde siempre en español. "
            "No muestres razonamientos internos ni explicaciones "
            "de tu proceso de pensamiento. "
            "Responde directamente al usuario."
        )
    }
]

#creamos una función que reciba un mensaje y devuelva la respuesta del modelo
def ejecutar(mensaje): 

    
    # Añadimos el nuevo mensaje al historial
    MENSAJES.append({
        "role": "user",
        "content": mensaje
    })    
    

    # Repetimos el ciclo hasta obtener una respuesta final
    for iteracion in range(MAX_ITERACIONES):

        print(f"\n[AGENTE] Iteración {iteracion + 1}")
        print("[DEBUG] Consultando al modelo...")

        # Primera llamada: el modelo decide qué hacer
        respuesta = preguntar(MENSAJES, HERRAMIENTAS) # llamamos a la función preguntar del archivo model.py para obtener la respuesta del modelo

        print("[DEBUG] Modelo respondió.")
        print("[DEBUG] Contenido:", repr(respuesta.content))
        print("[DEBUG] Herramientas:", respuesta.tool_calls)

        # Guardamos la respuesta del modelo en el historial
        MENSAJES.append(respuesta)

        # Si no solicita herramientas, termina el turno
        if not respuesta.tool_calls:
            if respuesta.content:
                print("\n--- HISTORIAL ---")
                pprint(MENSAJES)
                return respuesta.content

            raise RuntimeError("El modelo devolvió una respuesta vacía.")

        # Ejecutamos todas las herramientas solicitadas
        for llamada in respuesta.tool_calls:
            nombre = llamada.function.name
            argumentos = llamada.function.arguments


            # Buscamos la función en el registro
            funcion = REGISTRO_HERRAMIENTAS.get(nombre)

            if funcion is None:
                raise ValueError(
                        f"Herramienta no permitida: {nombre}"
                )

            print(
                f"\n[HERRAMIENTA EJECUTADA] "
                f"{nombre}({argumentos})"
            )

            # Ejecutamos la función correspondiente
            resultado = funcion(**argumentos)

            # Devolvemos el resultado de la herramienta al modelo
            MENSAJES.append({
                "role": "tool",
                "tool_name": nombre,
                "content": str(resultado)
            })


        # El modelo no produjo una respuesta final dentro del límite
    raise RuntimeError(
        f"El agente alcanzó el límite de "
        f"{MAX_ITERACIONES} iteraciones."
    )

