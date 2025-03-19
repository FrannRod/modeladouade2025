import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from ejercicios.metodos_numericos import newtonRaphson

# √6(2)
# √6(2) = x
# x**6-2 = 0 = f(x)

def funcion(x):
    return x**6 - 2

def derivada(x):
    return 6*x**5

x0 = 1
tolerancia = 1e-8
print(f"\nMétodo de Newton-Raphson:")
resultado, iteraciones = newtonRaphson(funcion, derivada, x0, tolerancia)
print(f"\nResultado: {resultado}")
print(f"Iteraciones: {iteraciones}")

