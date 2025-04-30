import math
import sys
import os

# Añadir el directorio padre al path para poder importar el módulo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metodos_numericos import puntoFijoAitken

def funcion(x):
    return (math.sin(x)+5)**(1/3)

# Usar el método de punto fijo con aceleración de Aitken
x0 = 2
tolerancia = 1e-6

resultado, iteraciones = puntoFijoAitken(funcion, x0, tolerancia)

print(f"\nResultado final: {resultado}")
print(f"Convergencia en {iteraciones} iteraciones")
