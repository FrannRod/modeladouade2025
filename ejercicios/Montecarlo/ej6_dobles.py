import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.stats import norm

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
 
# Definir la función a evaluar
def f(x):
    return np.sin(x)
 
# Número de puntos aleatorios
n = 10000
 
# Generar números aleatorios en el intervalo [0, π]
a, b = 0, np.pi
datos = np.random.uniform(a, b, n)
volumen = b - a
confianza = 0.95
 
# Evaluar los puntos en la función
evaluados = f(datos)
 
# Calcular estadísticas sobre los valores evaluados
media = np.mean(evaluados)
integral= media * volumen
desv_estandar = np.std(evaluados, ddof=1)
error_estandar = desv_estandar / np.sqrt(n)
varianza = np.var(evaluados, ddof=1)
z = obtener_valor_z(confianza)
 
# Calcular la integral exacta para comparar
integral_exacta, _ = quad(f, a, b)
 
# Visualización de resultados
plt.hist(datos, bins=50, alpha=0.6, color='b', density=True)
plt.title("Distribución de los valores generados")
plt.xlabel("x")
plt.ylabel("Frecuencia")
plt.show()
 
#integral estimada
print("=========================================================================")
print(f"Integral de f(x)")
print(f"Limite inferior a:{a}")
print(f"limite superior b:{b}")
print(f"muestras: {n}")
print(f"confianza: {confianza}")
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
print(f"Valor mínimo generado: {np.min(datos)}")
print(f"Valor máximo generado: {np.max(datos)}")
 
# 99,5% = 2,807
# 99% = 2,576
# 97% = 2,968
# 95% = 1,96
# 90% = 1,645
# 80% = 1,282