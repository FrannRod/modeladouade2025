import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from ejercicios.metodos_numericos import newtonRaphson


def funcion(x):
    return x**5-x-1

def derivada(x):
    return 5*x**4 - 1

x0 = 1
tolerancia = 1e-6
print(f"\nMétodo de Newton-Raphson:")
resultado, iteraciones = newtonRaphson(funcion, derivada, x0, tolerancia)
print(f"\nResultado: {resultado}")
print(f"Iteraciones: {iteraciones}")

