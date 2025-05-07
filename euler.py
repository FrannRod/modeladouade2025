import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def euler(f, y0, t0, tf, h):
    t = np.arange(t0, tf + h, h)
    y = np.zeros_like(t)
    y[0] = y0
    for i in range(len(t) - 1):
        y[i + 1] = y[i] + h * f(t[i], y[i])
    return t, y

def euler_mejorado(f, y0, t0, tf, h):
    t = np.arange(t0, tf + h, h)
    y = np.zeros_like(t)
    y[0] = y0
    for i in range(len(t) - 1):
        y_pred = y[i] + h * f(t[i], y[i])
        y[i + 1] = y[i] + h * (f(t[i], y[i]) + f(t[i + 1], y_pred)) / 2
    return t, y

def runge_kutta_4(f, y0, t0, tf, h):
    t = np.arange(t0, tf + h, h)
    y = np.zeros_like(t)
    y[0] = y0
    for i in range(len(t) - 1):
        k1 = f(t[i], y[i])
        k2 = f(t[i] + h/2, y[i] + h*k1/2)
        k3 = f(t[i] + h/2, y[i] + h*k2/2)
        k4 = f(t[i] + h, y[i] + h*k3)
        y[i+1] = y[i] + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
    return t, y

# Ecuación diferencial: dy/dt = 0.4 * t * y
def f(t, y):
    return 0.4 * t * y

# Solución exacta
def sol_exacta(y0, t):
    return (1 / np.exp(0.2)) * np.exp(0.2 * t**2)

# Parámetros
y0, t0, tf, h = 1, 1, 2, 0.1

# Cálculo de soluciones
t, y_euler = euler(f, y0, t0, tf, h)
_, y_eul_mej = euler_mejorado(f, y0, t0, tf, h)
_, y_rk4 = runge_kutta_4(f, y0, t0, tf, h)
y_real = sol_exacta(y0, t)

# Crear tabla resumen
tabla = pd.DataFrame({
    'Tiempo': t,
    'Exacta': y_real,
    'Euler': y_euler,
    'Euler Mejorado': y_eul_mej,
    'Runge-Kutta 4': y_rk4
})

print(tabla)

# Graficar resultados
plt.figure(figsize=(10, 6))
plt.plot(t, y_real, label="Solución Exacta", color="blue", linestyle="-", linewidth=2)
plt.plot(t, y_euler, label="Euler", color="red", linestyle="dotted", linewidth=2, marker="o")
plt.plot(t, y_eul_mej, label="Euler Mejorado", color="green", linestyle="dashdot", linewidth=2, marker="d")
plt.plot(t, y_rk4, label="Runge-Kutta 4", color="purple", linestyle="--", linewidth=2, marker="s")

plt.xlabel("Tiempo")
plt.ylabel("Solución y")
plt.title("Comparación de Métodos Numéricos para EDO")
plt.legend()
plt.grid()
plt.show()
