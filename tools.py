from datetime import datetime

def sumar(a, b):
    return int(a) + int(b)

def restar(a, b):
    return int(a) - int(b)


def multiplicar(a, b):
    return int(a) * int(b)

def obtener_fecha():
    return datetime.now().strftime("%d/%m/%Y")