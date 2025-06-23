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
semilla = 0
np.random.seed(semilla)
 
# Definir la función a evaluar (función de dos variables)
def f(x, y):
    return x*x+y*y
 
# Número de puntos aleatorios
n = 100000
confianza = 0.95
 
# Definir los límites de integración
x_min, x_max = 0, 1  # Límites para x
y_min, y_max = 0, 1  # Límites para y
volumen = (x_max - x_min) * (y_max - y_min)
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
 
# Crear una figura con dos subplots: uno para el gráfico 3D y otro para la tabla
fig = plt.figure(figsize=(18, 10))

# Gráfico 3D
ax1 = fig.add_subplot(121, projection='3d')
scatter = ax1.scatter(x, y, evaluados, c=evaluados, cmap='viridis', alpha=0.6, s=10)
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('f(X,Y)')
ax1.set_title("Distribución de los valores generados")

# Tabla de resultados
ax2 = fig.add_subplot(122)
ax2.axis('off')  # Ocultar ejes

# Crear los datos para la tabla
tabla_datos = [
    ["Integral doble de f(x,y)", ""],
    ["Semilla", f"{semilla}"],
    [f"Límites para x", f"[{x_min}, {x_max}]"],
    [f"Límites para y", f"[{y_min}, {y_max}]"],
    [f"Volumen", f"{volumen:.6f}"],
    [f"Muestras", f"{n}"],
    [f"Confianza", f"{confianza:.2f}"],
    [f"z", f"{z:.6f}"],
    ["", ""],
    [f"Media muestral", f"{media:.6f}"],
    [f"Estimación por Monte Carlo", f"{integral:.6f}"],
    [f"Valor exacto de la integral", f"{integral_exacta:.6f}"],
    [f"Error absoluto", f"{abs(integral - integral_exacta):.6f}"],
    [f"Desviación estándar", f"{desv_estandar:.6f}"],
    [f"Varianza", f"{varianza:.6f}"],
    [f"Error estándar", f"{error_estandar:.6f}"],
    [f"Intervalo de confianza del {confianza*100}%", f"[{integral - z * error_estandar:.6f}, {integral + z * error_estandar:.6f}]"],
    [f"Valor mínimo generado en x", f"{np.min(x):.6f}"],
    [f"Valor máximo generado en x", f"{np.max(x):.6f}"],
    [f"Valor mínimo generado en y", f"{np.min(y):.6f}"],
    [f"Valor máximo generado en y", f"{np.max(y):.6f}"]
]

# Crear la tabla
tabla = ax2.table(
    cellText=tabla_datos,
    cellLoc='left',
    loc='center',
    colWidths=[0.5, 0.5]
)

# Ajustar el estilo de la tabla
tabla.auto_set_font_size(False)
tabla.set_fontsize(10)
tabla.scale(1.2, 1.5)

# Añadir un título a la tabla
ax2.set_title("Resultados de la Integración por Monte Carlo", pad=20, fontsize=14)

# Ajustar el layout y mostrar la figura
plt.tight_layout()
plt.show()
