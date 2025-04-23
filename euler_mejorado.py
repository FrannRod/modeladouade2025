import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def euler_mejorado(f, y0, t0, tf, h):
    """ Método de Euler mejorado (Heun). """
    t = np.arange(t0, tf + h, h)
    y = np.zeros_like(t)
    y[0] = y0

    for i in range(len(t) - 1):
        y_pred = y[i] + h * f(t[i], y[i])  # Predicción con Euler
        y[i + 1] = y[i] + h * (f(t[i], y[i]) + f(t[i + 1], y_pred)) / 2  # Corrección

    return t, y

# Ecuación diferencial: dy/dt = y*sin(t)
def f(t, y):
    return 0.4 * t * y

# Solución exacta
def sol_exacta(y0, t):
    return (1 / np.exp(0.2)) * np.exp(0.2 * t**2)

# Parámetros
y0, t0, tf, h = 1, 1, 2, 0.1  # Condiciones iniciales

# Cálculo de soluciones
t, y_eul_mej = euler_mejorado(f, y0, t0, tf, h)
y_real = sol_exacta(y0, t)

# Crear tabla resumen
tabla = pd.DataFrame({
    'Tiempo': t,
    'Exacta': y_real,
    'Euler Mejorado': y_eul_mej
})

print(tabla)

# Graficar resultados
plt.figure(figsize=(8, 5))
plt.plot(t, y_real, label="Solución Exacta", color="blue", linestyle="-", linewidth=2)
plt.plot(t, y_eul_mej, label="Euler Mejorado", color="green", linestyle="dashdot", linewidth=2, marker="d")

plt.xlabel("Tiempo")
plt.ylabel("Solución y")
plt.title("Comparación de Métodos Numéricos para EDO")
plt.legend()
plt.grid()
plt.show()
