import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from ejercicios.metodos_numericos import puntoFijo

def funcion(x):
    return (x+1)**(1/3)

def main():
    x0 = 1
    tolerancia = 1e-6
    print(f"\nMétodo Punto Fijo:")
    resultado, iteraciones = puntoFijo(funcion, x0, tolerancia)
    print(f"Resultado: {resultado}")
    print(f"Iteraciones: {iteraciones}")

if __name__ == "__main__":
    main() 