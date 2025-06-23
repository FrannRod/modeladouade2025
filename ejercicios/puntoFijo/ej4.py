import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from ejercicios.metodos_numericos import puntoFijo

x0 = 1 # Lo dice el enunciado
# f(x) = x**3 - x - 1
# 0 = x**3 - x - 1
# x = x**3 - 1 = g(x)
# g'(x) = 3x**2 - 1
# g'(x0) = 3*1**2 - 1 = 2
# |g'(x0)| = 2 > 1
# No converge
# reescribo g(x)
# x = x**3 - 1
# x = (x + 1)**(1/3) = g(x)
# g'(x) = 1/3 * (x + 1)**(-2/3)
# g'(x0) = 1/3 * (1 + 1)**(-2/3) = 1/3 * 2**(-2/3) = 1/3 * 1/2**(2/3) = 1/3 * 1/1.5874 = 0.2
# |g'(x0)| = 0.2 < 1
# Converge


def funcion(x):
    return (x+1)**(1/3)

def main():
    tolerancia = 1e-6
    print(f"\nMétodo Punto Fijo:")
    resultado, iteraciones = puntoFijo(funcion, x0, tolerancia)
    print(f"Resultado: {resultado}")
    print(f"Iteraciones: {iteraciones}")

if __name__ == "__main__":
    main() 
