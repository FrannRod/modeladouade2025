import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import dblquad
from scipy.stats import norm
from mpl_toolkits.mplot3d import Axes3D

def obtener_valor_z(confianza):
    return norm.ppf((1 + confianza) / 2)

# Parámetros dados
semilla = 0
np.random.seed(semilla)
n = 10000 * 4
confianza = 0.95

# Límites de integración
x_min, x_max = 0, 1
y_min, y_max = 1, 3
volumen = (x_max - x_min) * (y_max - y_min)

# Definir la función a integrar
def f(x, y):
    return x * np.exp(y)

# Generar puntos aleatorios
x = np.random.uniform(x_min, x_max, n)
y = np.random.uniform(y_min, y_max, n)

# Evaluar la función en los puntos generados
evaluados = f(x, y)

# Estadísticas
media = np.mean(evaluados)
integral = media * volumen
desv_estandar = np.std(evaluados, ddof=1)
error_estandar = desv_estandar / np.sqrt(n)
varianza = np.var(evaluados, ddof=1)
z = obtener_valor_z(confianza)

# Integral exacta para comparar
integral_exacta, _ = dblquad(lambda y, x: f(x, y), x_min, x_max, lambda x: y_min, lambda x: y_max)

# Gráfica y tabla de resultados
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
ax2.axis('off')

tabla_datos = [
    ["Integral doble de f(x,y) = x*e^y", ""],
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

tabla = ax2.table(
    cellText=tabla_datos,
    cellLoc='left',
    loc='center',
    colWidths=[0.5, 0.5]
)
tabla.auto_set_font_size(False)
tabla.set_fontsize(10)
tabla.scale(1.2, 1.5)
ax2.set_title("Resultados de la Integración por Monte Carlo", pad=20, fontsize=14)

plt.tight_layout()
plt.show()
