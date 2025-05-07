import numpy as np
import pandas as pd
import math
import sys
import os

# Añadir el directorio raíz al path para poder importar el módulo
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import matplotlib.pyplot as plt
from euler import euler, runge_kutta_4

# Definir la función de la EDO
def f(x, y):
    return np.cos(x) + x

# Solución exacta (opcional, para comparar)
def sol_exacta(x):
    # y(x) = sin(x) + x^2/2 + C
    # y(0) = 1 => 0 + 0 + C = 1 => C = 1
    return np.sin(x) + x**2/2 + 1

# Parámetros
y0 = 1
x0 = 0
xf = np.pi/2
h = np.pi/8

# Calcular soluciones numéricas
x, y_euler = euler(f, y0, x0, xf, h)
_, y_rk4 = runge_kutta_4(f, y0, x0, xf, h)
y_real = sol_exacta(x)

# Crear tabla resumen
tabla = pd.DataFrame({
    'x': x,
    'Exacta': y_real,
    'Euler': y_euler,
    'Runge-Kutta 4': y_rk4
})

print(tabla)

# Graficar resultados
plt.figure(figsize=(10, 6))
plt.plot(x, y_real, label="Solución Exacta", color="blue", linestyle="-", linewidth=2)
plt.plot(x, y_euler, label="Euler", color="red", linestyle="dotted", linewidth=2, marker="o")
plt.plot(x, y_rk4, label="Runge-Kutta 4", color="purple", linestyle="--", linewidth=2, marker="s")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Comparación de Métodos Numéricos para EDO: $y' = \cos(x) + x$")
plt.legend()
plt.grid()
plt.show()

# a) Método de Euler con h = pi/8, precisión e-1, mostrando componentes
print("=== Inciso a) Euler con h = pi/8, precisión 1e-1 ===")
x_a, y_euler_a = euler(f, y0, x0, xf, h)
y_real_a = sol_exacta(x_a)

# Calcular las componentes de Euler paso a paso
f_evals = [f(x_a[i], y_euler_a[i]) for i in range(len(x_a)-1)]
y_next = [y_euler_a[i] + h * f_evals[i] for i in range(len(f_evals))]
error_abs = [abs(y_real_a[i+1] - y_next[i]) for i in range(len(y_next))]

tabla_a = pd.DataFrame({
    'x_i': x_a[:-1],
    'y_i': y_euler_a[:-1],
    'f(x_i, y_i)': f_evals,
    'y_{i+1}': y_next,
    'Exacta_{i+1}': y_real_a[1:],
    'Error abs': error_abs
})

print(tabla_a)
print(f"Error máximo: {np.max(error_abs)}")

# Explicación de las fórmulas:
print("""
Fórmulas del método de Euler:
    y_{i+1} = y_i + h * f(x_i, y_i)
    x_{i+1} = x_i + h

Donde:
    - x_i: valor actual de x
    - y_i: valor actual de y
    - f(x_i, y_i): valor de la derivada en el punto (x_i, y_i)
    - y_{i+1}: valor siguiente de y calculado por Euler
    - Error abs: |y_exacta_{i+1} - y_{i+1}|
""")

# b) Runge-Kutta 4 con precisión e-6, mostrando los k
print("\n=== Inciso b) RK4 con precisión 1e-6, mostrando k1, k2, k3, k4 ===")

def runge_kutta_4_verbose(f, y0, t0, tf, tol):
    # Elegimos un h suficientemente pequeño para cumplir la tolerancia
    N = int(np.ceil((tf - t0) / 0.01))  # Paso inicial pequeño
    h = (tf - t0) / N
    t = np.arange(t0, tf + h, h)
    y = np.zeros_like(t)
    y[0] = y0
    for i in range(len(t) - 1):
        k1 = f(t[i], y[i])
        k2 = f(t[i] + h/2, y[i] + h*k1/2)
        k3 = f(t[i] + h/2, y[i] + h*k2/2)
        k4 = f(t[i] + h, y[i] + h*k3)
        y[i+1] = y[i] + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
        print(f"Paso {i}: x={t[i]:.6f}, y={y[i]:.6f}")
        print(f"  k1={k1:.6f}, k2={k2:.6f}, k3={k3:.6f}, k4={k4:.6f}")
    return t, y

# Ejecutar con h pequeño hasta que el error sea menor a 1e-6
h_b = 0.001  # Paso pequeño para asegurar la tolerancia
x_b, y_rk4_b = runge_kutta_4_verbose(f, y0, x0, xf, h_b)
y_real_b = sol_exacta(x_b)
error_b = np.abs(y_real_b - y_rk4_b)
print(f"\nError máximo alcanzado: {np.max(error_b)}")

# Mostrar el último valor
print(f"\nValor final aproximado en x={x_b[-1]:.6f}: y={y_rk4_b[-1]:.8f}")
print(f"Valor exacto: {y_real_b[-1]:.8f}")
print(f"Error absoluto: {abs(y_real_b[-1] - y_rk4_b[-1]):.2e}")
