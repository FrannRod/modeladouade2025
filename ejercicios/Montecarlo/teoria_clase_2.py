import numpy as np
 
# Parámetros
n = 14000  # Cantidad de números aleatorios
#intervalos
a=0
b=1
 
# Generar números aleatorios uniformemente distribuidos en el intervalo
x_aleatorios = np.random.uniform(a,b, n)
 
# Definir la función a evaluar f(x)
def funcion(x):
    return np.exp(-x**2)
 
# Evaluar la función
x_eval = funcion(x_aleatorios)
 
#desviacion estandar muestral
desviacion_estandar_muestral = np.std(x_eval, ddof=1)
 
# Calcular la media de los valores evaluados
media = np.mean(x_eval)
 
# Mostrar la media
print(f"Media de los valores evaluados: {media}")
# mostrar desviacion estandar
print(f"Desviación estándar muestral: {desviacion_estandar_muestral}")
