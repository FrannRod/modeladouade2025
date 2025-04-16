import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import dblquad
from scipy.stats import norm
from mpl_toolkits.mplot3d import Axes3D

def obtener_valor_z(confianza):
    """
    Calcula el valor z para un nivel de confianza dado.
    
    Args:
        confianza (float): Nivel de confianza deseado (entre 0 y 1)
    
    Returns:
        float: Valor z correspondiente al nivel de confianza
    """
    return norm.ppf((1 + confianza) / 2)

# Fijar la semilla para reproducibilidad
np.random.seed(0)
 
# Definir la función a evaluar (función de dos variables)
def f(x, y):
    return np.exp(x + y)
 
# Número de puntos aleatorios
n = 50000
 
# Definir los límites de integración
x_min, x_max = 0, 2  # Límites para x
y_min, y_max = 1, 3  # Límites para y
volumen = (x_max - x_min) * (y_max - y_min)
confianza = 0.90
# Generar puntos aleatorios en el dominio de integración
x = np.random.uniform(x_min, x_max, n)
y = np.random.uniform(y_min, y_max, n)
 
# Evaluar los puntos en la función
evaluados = f(x, y)
 
# Calcular estadísticas sobre los valores evaluados
media = np.mean(evaluados)
integral = media * volumen
desv_estandar = np.std(evaluados, ddof=1)
error_estandar = desv_estandar / np.sqrt(n)
varianza = np.var(evaluados, ddof=1)
z = obtener_valor_z(confianza)
 
# Calcular la integral exacta para comparar
integral_exacta, _ = dblquad(lambda y, x: f(x, y), x_min, x_max, lambda x: y_min, lambda x: y_max)
 
# Visualización de resultados en 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, evaluados, c=evaluados, cmap='viridis', alpha=0.6, s=10)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('f(X,Y)')
ax.set_title("Distribución de los valores generados")
plt.show()
 
# Integral estimada
print("=========================================================================")
print(f"Integral doble de f(x,y)")
print(f"Límites para x: [{x_min}, {x_max}]")
print(f"Límites para y: [{y_min}, {y_max}]")
print(f"Volumen: {volumen}")
print(f"Muestras: {n}")
print(f"Confianza: {confianza}")
print(f"z: {z}")
print("=========================================================================")
 
# Mostrar resultados mejorados
print(f"\nMedia muestral: {media}")
print(f"Estimación por Monte Carlo: {integral}")
print(f"Valor exacto de la integral: {integral_exacta}")
print(f"Error absoluto: {abs(integral - integral_exacta)}")
print(f"Desviación estándar: {desv_estandar}")
print(f"Varianza: {varianza}")
print(f"Error estándar: {error_estandar}")
print(f"Intervalo de confianza del {confianza*100}%: [{integral - z * error_estandar}, {integral + z * error_estandar}]")
print(f"Valor mínimo generado en x: {np.min(x)}")
print(f"Valor máximo generado en x: {np.max(x)}")
print(f"Valor mínimo generado en y: {np.min(y)}")
print(f"Valor máximo generado en y: {np.max(y)}")
 
# 99,5% = 2,807
# 99% = 2,576
# 97% = 2,968
# 95% = 1,96
# 90% = 1,645
# 80% = 1,282