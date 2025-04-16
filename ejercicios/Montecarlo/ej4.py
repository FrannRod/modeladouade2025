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
    return np.sqrt(x)
 
# Número de puntos aleatorios
n = 5000000
 
# Generar números aleatorios en el intervalo [0, π]
a, b = 1, 4
datos = np.random.uniform(a, b, n)
longitud = b - a
confianza = 0.99
 
# Evaluar los puntos en la función
evaluados = f(datos)
 
# Calcular estadísticas sobre los valores evaluados
media = np.mean(evaluados) * longitud
desv_estandar = np.std(evaluados, ddof=1)
error_estandar = desv_estandar / np.sqrt(n)
varianza = np.var(evaluados, ddof=1)
 
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
print("=========================================================================")
 
# Mostrar resultados mejorados
print(f"\nEstimación por Monte Carlo (media): {media}")

print(f"Valor exacto de la integral: {integral_exacta}")
print(f"Error absoluto: {abs(media - integral_exacta)}")
print(f"Desviación estándar: {desv_estandar}")
print(f"Error estándar: {error_estandar}")
print(f"Varianza: {varianza}")

z = obtener_valor_z(confianza)
print(f"Intervalo de confianza del {confianza*100}%: [{media - z * error_estandar}, {media + z * error_estandar}]")

print(f"Valor mínimo generado: {np.min(datos)}")
print(f"Valor máximo generado: {np.max(datos)}")
 
# 99,5% = 2,807
# 99% = 2,576
# 97% = 2,968
# 95% = 1,96
# 90% = 1,645
# 80% = 1,282