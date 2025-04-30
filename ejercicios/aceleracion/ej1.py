import math
import sys
import os

# Añadir el directorio padre al path para poder importar el módulo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metodos_numericos import puntoFijoAitken, newtonRaphson


def funcion(x):
    return x**3 - math.sin(x) - 5

def derivada(x):
    return -math.cos(x) + 3*x**2

# Usar el método de Newton-Raphson para encontrar el punto fijo de g(x)
x0 = 2
tolerancia = 1e-8
resultado_newton, iteraciones_newton = newtonRaphson(funcion, derivada, x0, tolerancia)

print(f"\n[Newton-Raphson] Resultado final: {resultado_newton}")
print(f"[Newton-Raphson] Convergencia en {iteraciones_newton} iteraciones")
