import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from ejercicios.metodos_numericos import diferencias_divididas

puntos = [
    (0, 0),
    (2, 0.7),
    (4, 1.8),
    (6,3.4),
    (8,5.1),
    (10,6.3),
    (12,7.3),
    (14,8),
    (16,8.4)
]

diferencias_divididas(puntos)
