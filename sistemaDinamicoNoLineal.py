# sistemaDinamicoNoLineal.py

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# -----------------------------
# 1. DEFINÍ TU SISTEMA EN UN ÚNICO LUGAR
# -----------------------------
#   - Acá definís las ecuaciones simbólicas: f1(x,y) = \dot x, f2(x,y) = \dot y.
#   - Para cambiar a otro sistema, solo reemplazás estas dos líneas.
x, y = sp.symbols('x y', real=True)
f1 = x*(2 - x - y)
f2 = y*(3 - 2*x - y)

# -----------------------------
# 2. CALCULAR PUNTOS DE EQUILIBRIO
# -----------------------------
soluciones = sp.solve([f1, f2], [x, y], dict=True)

# -----------------------------
# 3. JACOBIANA SIMBÓLICA Y CLASIFICACIÓN
# -----------------------------
J = sp.Matrix([
    [sp.diff(f1, x), sp.diff(f1, y)],
    [sp.diff(f2, x), sp.diff(f2, y)]
])

def clasificar_autovalores(avalores):
    λ1, λ2 = avalores
    re1, re2 = sp.re(λ1), sp.re(λ2)
    im1, im2 = sp.im(λ1), sp.im(λ2)

    if re1 * re2 < 0:
        return "Punto de silla"
    if re1 == 0 and re2 == 0 and (im1 != 0 or im2 != 0):
        return "Centro"
    if im1 != 0 or im2 != 0:
        if re1 < 0 and re2 < 0:
            return "Espiral estable"
        elif re1 > 0 and re2 > 0:
            return "Espiral inestable"
        else:
            return "Espiral (mixto)"
    if im1 == 0 and im2 == 0:
        if re1 < 0 and re2 < 0:
            return "Nodo estable"
        elif re1 > 0 and re2 > 0:
            return "Nodo inestable"
        elif re1 == 0 or re2 == 0:
            return "Nodo degenerado / bifurcación"
    return "Indeterminado"

puntos_equilibrio = []
for sol in soluciones:
    px = sol[x]
    py = sol[y]
    J_eval = J.subs({x: px, y: py}).evalf()
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

# Armamos un texto con toda la info para mostrar al costado del gráfico
texto_info = "Puntos de equilibrio y clasificación:\n"
for info in puntos_equilibrio:
    px, py = info['punto']
    eigs = info['autovalores']
    nat = info['naturaleza']
    eig_strs = []
    for eig in eigs:
        ev = complex(eig)
        real = ev.real
        imag = ev.imag
        eig_strs.append(f"{real:.4f}{imag:+.4f}j")
    texto_info += f"- ({px:.4f}, {py:.4f}): [{eig_strs[0]}, {eig_strs[1]}] → {nat}\n"

# -----------------------------
# 4. GENERAR VERSIÓN NUMÉRICA DEL CAMPO CON LAMBDIFY
# -----------------------------
f1_num = sp.lambdify((x, y), f1, 'numpy')
f2_num = sp.lambdify((x, y), f2, 'numpy')

def campo_vectorial(x_val, y_val):
    u = f1_num(x_val, y_val)
    v = f2_num(x_val, y_val)
    return u, v

# -----------------------------
# 5. GRAFICAR DIAGRAMA DE FASES CON CAJA DE TEXTO AL COSTADO
# -----------------------------
lim = 4     # Ajustá según dónde estén los equilibrios
n = 400
x_vals = np.linspace(-lim, lim, n)
y_vals = np.linspace(-lim, lim, n)
X, Y = np.meshgrid(x_vals, y_vals)
U, V = campo_vectorial(X, Y)

fig = plt.figure(figsize=(10, 6))

# Subplot izquierdo: diagrama de fases
ax_phase = fig.add_subplot(1, 2, 1)
ax_phase.streamplot(X, Y, U, V, density=1.0, linewidth=0.7, arrowsize=1)
for info in puntos_equilibrio:
    px, py = info['punto']
    ax_phase.plot(float(px), float(py), 'ro')
    ax_phase.text(float(px) + 0.05, float(py) + 0.05, info['naturaleza'],
                  color='r', fontsize=8)
ax_phase.set_title("Diagrama de fases")
ax_phase.set_xlabel("x")
ax_phase.set_ylabel("y")
ax_phase.axhline(0, color='k', linewidth=0.5)
ax_phase.axvline(0, color='k', linewidth=0.5)
ax_phase.set_xlim(-lim, lim)
ax_phase.set_ylim(-lim, lim)
ax_phase.set_aspect('equal', 'box')

# Subplot derecho: cuadro de texto con la información
ax_text = fig.add_subplot(1, 2, 2)
ax_text.axis('off')  # Ocultamos ejes
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax_text.text(0, 1, texto_info, fontsize=10, va='top', ha='left', bbox=props)

plt.tight_layout()
plt.show()
