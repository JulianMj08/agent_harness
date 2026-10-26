from agent import ejecutar


while True: # bucle infinito para que el usuario pueda seguir haciendo preguntas
    mensaje = input("Tú: ")

    if mensaje.lower() in ["salir", "exit", "quit"]:
        break

    respuesta = ejecutar(mensaje)

    print(f"IA te estoy respondiendo desde main: {respuesta}")