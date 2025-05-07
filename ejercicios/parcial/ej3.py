import numpy as np

# Definir la función, cuidando el caso x=0
def f(x):
    return np.where(x == 0, 1.0, np.log(x+1)/x)

# Derivada segunda para el error (calculada simbólicamente o numéricamente)
def f2(x):
    # Evitar división por cero en x=0
    # El límite de f2(x) cuando x->0 es -1/2
    return np.where(
        x == 0,
        -0.5,
        -1/(x+1)**2 + 2*np.log(x+1)/x**3 - 2/(x**2*(x+1))
    )

a, b = 0, 1
n = 4
h = (b - a) / n

# Puntos
x = np.linspace(a, b, n+1)
y = f(x)

# Regla del trapecio compuesta
trapecio = h/2 * (y[0] + 2*np.sum(y[1:-1]) + y[-1])

# Calcular el error estimado usando f''(e=0.5)
e = 0.5
error = -((b-a)*h**2/12) * f2(e)

print("Aproximación por trapecio compuesta (n=4):", trapecio)
print("Error estimado en e=0.5:", error)
