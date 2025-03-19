import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from ejercicios.metodos_numericos import newtonRaphson


def funcion(x):
    return x**3 -2*x - 5

def derivada(x):
    return 3*x**2 - 2

x0 = 1.5
tolerancia = 1e-6
print(f"\nMétodo de Newton-Raphson:")
resultado, iteraciones = newtonRaphson(funcion, derivada, x0, tolerancia)
print(f"\nResultado: {resultado}")
print(f"Iteraciones: {iteraciones}")

