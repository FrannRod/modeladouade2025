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
semilla = 0
np.random.seed(semilla)
 
# Definir la función a evaluar
def f(x):
    return 1/(x*x+1)
 
# Número de puntos aleatorios
a, b = 0, 1
n = 5000
confianza = 0.95
 
# Generar números aleatorios en el intervalo [0, π]
datos = np.random.uniform(a, b, n)
volumen = b - a
 
# Evaluar los puntos en la función
evaluados = f(datos)
 
# Calcular estadísticas sobre los valores evaluados
media = np.mean(evaluados)
integral = media * volumen
desv_estandar = np.std(evaluados, ddof=1)
error_estandar = desv_estandar / np.sqrt(n)
varianza = np.var(evaluados, ddof=1)
z = obtener_valor_z(confianza)
 
# Calcular la integral exacta para comparar
integral_exacta, _ = quad(f, a, b)

# Crear una figura con dos subplots: uno para el histograma y otro para la tabla
fig = plt.figure(figsize=(14, 8))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1])

# Subplot para el histograma
ax1 = fig.add_subplot(gs[0])
ax1.hist(datos, bins=50, alpha=0.6, color='b', density=True)
ax1.set_title("Distribución de los valores generados")
ax1.set_xlabel("x")
ax1.set_ylabel("Frecuencia")

# Subplot para la tabla de resultados
ax2 = fig.add_subplot(gs[1])
ax2.axis('off')  # Ocultar ejes

# Datos para la tabla
tabla_datos = [
    ["Integral de f(x)", ""],
    ["Semilla", f"{semilla}"],
    ["Límite inferior a", f"{a}"],
    ["Límite superior b", f"{b}"],
    ["Muestras", f"{n}"],
    ["Confianza", f"{confianza}"],
    ["Valor z", f"{z:.4f}"],
    ["", ""],
    ["Media muestral", f"{media:.6f}"],
    ["Estimación por Monte Carlo", f"{integral:.6f}"],
    ["Valor exacto de la integral", f"{integral_exacta:.6f}"],
    ["Error absoluto", f"{abs(integral - integral_exacta):.6f}"],
    ["Desviación estándar", f"{desv_estandar:.6f}"],
    ["Varianza", f"{varianza:.6f}"],
    ["Error estándar", f"{error_estandar:.6f}"],
    ["Intervalo de confianza del " + f"{confianza*100}%", f"[{integral - z * error_estandar:.6f}, {integral + z * error_estandar:.6f}]"],
    ["Valor mínimo generado", f"{np.min(datos):.6f}"],
    ["Valor máximo generado", f"{np.max(datos):.6f}"]
]

# Crear la tabla
tabla = ax2.table(
    cellText=tabla_datos,
    loc='center',
    cellLoc='left',
    colWidths=[0.5, 0.5]
)

# Dar formato a la tabla
tabla.auto_set_font_size(False)
tabla.set_fontsize(10)
tabla.scale(1, 1.5)  # Ajustar el tamaño de la tabla

# Añadir una línea de separación después del encabezado
for i in range(len(tabla_datos)):
    if i == 6:  # Después de la fila de separación
        for j in range(2):
            celda = tabla[i, j]
            celda.set_text_props(weight='bold')
    elif i == 0:  # Título
        for j in range(2):
            celda = tabla[i, j]
            celda.set_text_props(weight='bold')

plt.tight_layout()
plt.show()