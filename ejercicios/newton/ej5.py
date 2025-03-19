import sys
import os
from math import e
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from ejercicios.metodos_numericos import newtonRaphson


def funcion(x):
    return e**x + x**2 - 4

def derivada(x):
    return e**x + 2*x

x0 = 0.5
tolerancia = 1e-6
print(f"\nMétodo de Newton-Raphson:")
resultado, iteraciones = newtonRaphson(funcion, derivada, x0, tolerancia)
print(f"\nResultado: {resultado}")
print(f"Iteraciones: {iteraciones}")

