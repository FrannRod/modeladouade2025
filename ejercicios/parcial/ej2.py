import math
import sys
import os

# Añadir el directorio padre al path para poder importar el módulo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metodos_numericos import lagrange, diferencias_divididas

# Definir los puntos
x_puntos = [0, 0.5, 1, 1.5]
y_puntos = [0, 1, 0, -1]

# Llamar a la función de Lagrange
polinomio = lagrange(x_puntos, y_puntos)

puntos = [
    (0, 0),
    (0.5, 1),
    (1, 0),
    (1.5, -1)
]

diferencias_divididas(puntos)
