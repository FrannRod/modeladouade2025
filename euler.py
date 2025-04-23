import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def euler(f, y0, t0, tf, h):
    t_values = np.arange(t0, tf + h, h)
    y_values = np.zeros(len(t_values))
    y_values[0] = y0
    for i in range(1, len(t_values)):
        y_values[i] = y_values[i - 1] + h * f(t_values[i - 1], y_values[i - 1])
    return t_values, y_values

def f(t, y):
    return t + y

def solucion_particular(t):
    return -t - 1 + 2 * np.exp(t)

# Condiciones iniciales y parámetros
y0, t0, tf, h = 1, 0, 1, 0.1

# Soluciones
t_euler, y_euler = euler(f, y0, t0, tf, h)
y_real = solucion_particular(t_euler)

# Crear DataFrame
resultados = pd.DataFrame({
    'Tiempo': t_euler,
    'Euler': y_euler,
    'Solución Real': y_real
})

print(resultados)

# Graficar resultados
plt.plot(t_euler, y_euler, label='Euler')
plt.plot(t_euler, y_real, label='Solución Real')
plt.xlabel('Tiempo')
plt.ylabel('Valor de y')
plt.legend()
plt.title('Métodos de Euler, Euler Mejorado y Solución Real')
plt.show()
