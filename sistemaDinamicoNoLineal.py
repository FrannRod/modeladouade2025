# sistemaDinamicoNoLineal.py

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# 1. Definición simbólica del sistema
x, y = sp.symbols('x y', real=True)
f1 = x*(2-x-y)
f2 = y*(3-2*x-y)

# 2. Cálculo de puntos de equilibrio: f1 = 0, f2 = 0
soluciones = sp.solve([f1, f2], [x, y], dict=True)

# 3. Matriz Jacobiana simbólica
J = sp.Matrix([[sp.diff(f1, x), sp.diff(f1, y)],
               [sp.diff(f2, x), sp.diff(f2, y)]])

# Función para clasificar el tipo de equilibrio según sus autovalores
def clasificar_autovalores(autovalores):
    λ1, λ2 = autovalores
    re1, re2 = sp.re(λ1), sp.re(λ2)
    im1, im2 = sp.im(λ1), sp.im(λ2)

    # Punto de silla: señales opuestas en parte real
    if re1 * re2 < 0:
        return "Punto de silla"
    # Centro: partes reales cero, partes imaginarias no cero
    if re1 == 0 and re2 == 0 and (im1 != 0 or im2 != 0):
        return "Centro"
    # Espiral (foco)
    if im1 != 0 or im2 != 0:
        if re1 < 0 and re2 < 0:
            return "Espiral estable"
        elif re1 > 0 and re2 > 0:
            return "Espiral inestable"
        else:
            return "Espiral (mixto)"
    # Nodo (sin parte imaginaria)
    if im1 == 0 and im2 == 0:
        if re1 < 0 and re2 < 0:
            return "Nodo estable"
        elif re1 > 0 and re2 > 0:
            return "Nodo inestable"
        elif re1 == 0 or re2 == 0:
            return "Nodo degenerado / bifurcación"
    return "Indeterminado"

# 4. Evaluar Jacobiana y autovalores en cada equilibrio
puntos_equilibrio = []
for sol in soluciones:
    px = sol[x]
    py = sol[y]
    # Convertimos Jacobiana a valores numéricos
    J_eval = J.subs({x: px, y: py}).evalf()
    # Obtenemos autovalores numéricos
    eig_dict = J_eval.eigenvals()
    lista_eig = []
    for valor, mult in eig_dict.items():
        for _ in range(int(mult)):
            lista_eig.append(valor)
    naturaleza = clasificar_autovalores(lista_eig)
    puntos_equilibrio.append({
        'punto': (sp.N(px), sp.N(py)),
        'autovalores': lista_eig,
        'naturaleza': naturaleza
    })

# Mostrar resultados por consola
print("Puntos de equilibrio y su clasificación:")
for info in puntos_equilibrio:
    px, py = info['punto']
    eigs = info['autovalores']
    nat = info['naturaleza']
    # Para cada autovalor, convertimos a float (python complex) y formateamos
    eig_strs = []
    for eig in eigs:
        ev = complex(eig)  # convierte 1 + I -> (1+1j)
        real = ev.real
        imag = ev.imag
        eig_strs.append(f"{real:.4f}{imag:+.4f}j")
    print(f"  - Punto ({px:.4f}, {py:.4f}):")
    print(f"      Autovalores = [{eig_strs[0]}, {eig_strs[1]}]")
    print(f"      Naturaleza = {nat}")

# 5. Gráfica de campo vectorial y trayectorias (phase portrait)
def campo_vectorial(x_val, y_val):
    u = x_val*(1 - x_val**2 - y_val**2) - y_val
    v = y_val*(1 - x_val**2 - y_val**2) + x_val
    return u, v

# Dominio de la gráfica
lim = 1.5
n = 400
x_vals = np.linspace(-lim, lim, n)
y_vals = np.linspace(-lim, lim, n)
X, Y = np.meshgrid(x_vals, y_vals)
U, V = campo_vectorial(X, Y)

plt.figure(figsize=(6,6))
plt.streamplot(X, Y, U, V, density=1.0, linewidth=0.7, arrowsize=1)

# Graficar los puntos de equilibrio y su etiqueta
for info in puntos_equilibrio:
    px, py = info['punto']
    plt.plot(float(px), float(py), 'ro')
    plt.text(float(px)+0.05, float(py)+0.05, info['naturaleza'], color='r', fontsize=8)

plt.title("Diagrama de fases del sistema dinámico")
plt.xlabel("x")
plt.ylabel("y")
plt.axhline(0, color='k', linewidth=0.5)
plt.axvline(0, color='k', linewidth=0.5)
plt.xlim(-lim, lim)
plt.ylim(-lim, lim)
plt.gca().set_aspect('equal', 'box')
plt.tight_layout()
plt.show()
