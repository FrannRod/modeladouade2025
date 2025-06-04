# sistema_dinamico.py

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# 1. Definí tu sistema en un solo lugar
#    Reemplazá estas dos líneas si querés otro sistema.
x_sym, y_sym = sp.symbols('x y', real=True)
ecu1 = x_sym*(2 - x_sym - y_sym)
ecu2 = y_sym*(3 - 2*x_sym - y_sym)

# 2. Calculá puntos de equilibrio resolviendo ecu1=0, ecu2=0
sols = sp.solve([ecu1, ecu2], [x_sym, y_sym], dict=True)

# 3. Armá la matriz jacobiana y clasificá cada punto
jacob = sp.Matrix([
    [sp.diff(ecu1, x_sym), sp.diff(ecu1, y_sym)],
    [sp.diff(ecu2, x_sym), sp.diff(ecu2, y_sym)]
])

def tipo_por_autovals(vals):
    l1, l2 = vals
    r1, r2 = sp.re(l1), sp.re(l2)
    i1, i2 = sp.im(l1), sp.im(l2)
    if r1*r2 < 0:
        return "Silla"
    if r1 == 0 and r2 == 0 and (i1 != 0 or i2 != 0):
        return "Centro"
    if i1 != 0 or i2 != 0:
        if r1 < 0 and r2 < 0:
            return "Espiral estable"
        if r1 > 0 and r2 > 0:
            return "Espiral inestable"
        return "Espiral (mixto)"
    if i1 == 0 and i2 == 0:
        if r1 < 0 and r2 < 0:
            return "Nodo estable"
        if r1 > 0 and r2 > 0:
            return "Nodo inestable"
        return "Nodo degenerado"
    return "Indeterminado"

puntos_eq = []
for s in sols:
    px = s[x_sym]
    py = s[y_sym]
    J_eval = jacob.subs({x_sym: px, y_sym: py}).evalf()
    eigs = []
    for val, mult in J_eval.eigenvals().items():
        for _ in range(int(mult)):
            eigs.append(val)
    tipo = tipo_por_autovals(eigs)
    puntos_eq.append({
        'coords': (sp.N(px), sp.N(py)),
        'autovals': eigs,
        'clasif': tipo
    })

# Armamos el texto con la info de cada punto
texto = "Puntos de equilibrio y clasificación:\n"
for info in puntos_eq:
    px, py = info['coords']
    av = info['autovals']
    cadena_autovals = []
    for a in av:
        c = complex(a)
        cadena_autovals.append(f"{c.real:.4f}{c.imag:+.4f}j")
    texto += f"- ({px:.4f}, {py:.4f}): [{cadena_autovals[0]}, {cadena_autovals[1]}] → {info['clasif']}\n"

# 4. Generar versión numérica del campo con lambdify
f1_np = sp.lambdify((x_sym, y_sym), ecu1, 'numpy')
f2_np = sp.lambdify((x_sym, y_sym), ecu2, 'numpy')

def campo(xv, yv):
    return f1_np(xv, yv), f2_np(xv, yv)

# 5. Dibujar diagrama de fases y mostrar la info al costado
limite = 4.0
puntos = 400
xs = np.linspace(-limite, limite, puntos)
ys = np.linspace(-limite, limite, puntos)
Xg, Yg = np.meshgrid(xs, ys)
Ug, Vg = campo(Xg, Yg)

fig = plt.figure(figsize=(10, 6))

# Gráfico de fase
ax1 = fig.add_subplot(1, 2, 1)
ax1.streamplot(Xg, Yg, Ug, Vg, density=1.0, linewidth=0.7, arrowsize=1)
for info in puntos_eq:
    px, py = info['coords']
    ax1.plot(float(px), float(py), 'ro')
    ax1.text(float(px) + 0.05, float(py) + 0.05, info['clasif'],
             color='r', fontsize=8)
ax1.set_title("Diagrama de fases")
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.axhline(0, color='k', linewidth=0.5)
ax1.axvline(0, color='k', linewidth=0.5)
ax1.set_xlim(-limite, limite)
ax1.set_ylim(-limite, limite)
ax1.set_aspect('equal')

# Cuadro de texto con la información
ax2 = fig.add_subplot(1, 2, 2)
ax2.axis('off')
caja = dict(boxstyle='round', facecolor='white', alpha=0.6)
ax2.text(0, 1, texto, fontsize=10, va='top', ha='left', bbox=caja)

plt.tight_layout()
plt.show()
