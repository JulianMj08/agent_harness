from agent import ejecutar


while True: # bucle infinito para que el usuario pueda seguir haciendo preguntas
    mensaje = input("Tú: ")

    if mensaje.lower() in ["salir", "exit", "quit"]:
        break

    try:
        respuesta = ejecutar(mensaje)
        print(f"IA: {respuesta}")
    except Exception as error:
        print(f"Error: {error}")