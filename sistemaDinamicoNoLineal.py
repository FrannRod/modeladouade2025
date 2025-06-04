# sistema_dinamico.py

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# 1. Definí tu sistema en un solo lugar.
#    Si querés estudiar otro sistema, solo cambiá estas dos líneas:
x_sym, y_sym = sp.symbols('x y', real=True)
ecu1 = x_sym*(1- x_sym) - x_sym * y_sym
ecu2 = x_sym * y_sym - y_sym

# Convertimos las ecuaciones a cadenas para que aparezcan en el gráfico.
sistema_str = f"x' = {str(ecu1)}\n" + f"y' = {str(ecu2)}"

# 2. Calculá puntos de equilibrio (ecu1 = 0, ecu2 = 0)
sols = sp.solve([ecu1, ecu2], [x_sym, y_sym], dict=True)

# 3. Armá la matriz Jacobiana y sacá autovalores/autovectores
jacob = sp.Matrix([
    [sp.diff(ecu1, x_sym), sp.diff(ecu1, y_sym)],
    [sp.diff(ecu2, x_sym), sp.diff(ecu2, y_sym)]
])

def tipo_por_autovals(vals):
    l1, l2 = vals
    r1, r2 = sp.re(l1), sp.re(l2)
    i1, i2 = sp.im(l1), sp.im(l2)
    # Nodo fuente o sumidero
    if i1 == 0 and i2 == 0:
        if r1 > 0 and r2 > 0:
            return "Nodo fuente"
        if r1 < 0 and r2 < 0:
            return "Nodo sumidero"
        if r1 == 0 or r2 == 0:
            return "Nodo degenerado"
    # Punto de silla
    if r1 * r2 < 0:
        return "Punto de silla"
    # Centro
    if r1 == 0 and r2 == 0 and (i1 != 0 or i2 != 0):
        return "Centro"
    # Espiral (foco)
    if i1 != 0 or i2 != 0:
        if r1 < 0 and r2 < 0:
            return "Espiral estable"
        if r1 > 0 and r2 > 0:
            return "Espiral inestable"
        return "Espiral (mixto)"
    return "Indeterminado"

puntos_eq = []
for s in sols:
    px = s[x_sym]
    py = s[y_sym]
    # Evaluamos Jacobiana en (px, py) y convertimos a valores numéricos
    J_eval = jacob.subs({x_sym: px, y_sym: py}).evalf()
    # Sacamos autovalores (con multiplicidad)
    eigs_dict = J_eval.eigenvals()
    eigs = []
    for val, mult in eigs_dict.items():
        for _ in range(int(mult)):
            eigs.append(val)
    # Sacamos autovectores
    evects = J_eval.eigenvects()
    autovs = []
    for triple in evects:
        vec_sim = triple[2][0]    # primer autovector de ese autovalor
        comp0 = complex(vec_sim[0])
        comp1 = complex(vec_sim[1])
        norma = np.sqrt(
            (comp0.real)**2 + (comp0.imag)**2 +
            (comp1.real)**2 + (comp1.imag)**2
        )
        if norma == 0:
            autovs.append((0.0 + 0.0j, 0.0 + 0.0j))
        else:
            autovs.append((comp0 / norma, comp1 / norma))
    tipo = tipo_por_autovals(eigs)
    puntos_eq.append({
        'coords': (sp.N(px), sp.N(py)),
        'jacobiano': J_eval,
        'autovalores': eigs,
        'autovectores': autovs,
        'clasif': tipo
    })

# 4. Armá el texto para mostrar al costado, con todo en "formato matriz"
texto = "Sistema dinámico:\n"
texto += f"  {sistema_str}\n\n"
texto += "Puntos de equilibrio y detalle:\n\n"
for info in puntos_eq:
    px, py = info['coords']
    Jm = info['jacobiano']
    a11 = float(Jm[0, 0]); a12 = float(Jm[0, 1])
    a21 = float(Jm[1, 0]); a22 = float(Jm[1, 1])
    texto += f"• Punto ({px:.4f}, {py:.4f}):\n"
    # Jacobiano en formato matriz alineada
    texto += "    Jacobiano =\n"
    texto += f"      [ {a11:>7.4f}  {a12:>7.4f} ]\n"
    texto += f"      [ {a21:>7.4f}  {a22:>7.4f} ]\n"
    # Autovalores y autovectores en bloques horizontales
    av = info['autovalores']
    # Tomamos parte real o imaginaria según corresponda
    e1, e2 = float(sp.re(av[0])), float(sp.re(av[1]))
    e1_str = f"{e1:>7.4f}"
    e2_str = f"{e2:>7.4f}"
    # Autovectores (dos vectores columna normalizados)
    avs = info['autovectores']
    vx1, vy1 = avs[0]
    vx2, vy2 = avs[1]
    v11 = float(np.real(vx1)); v21 = float(np.real(vy1))
    v12 = float(np.real(vx2)); v22 = float(np.real(vy2))
    v11_str = f"{v11:>7.4f}"
    v21_str = f"{v21:>7.4f}"
    v12_str = f"{v12:>7.4f}"
    v22_str = f"{v22:>7.4f}"
    texto += "    Autovalores =     Autovectores =\n"
    texto += f"      [ {e1_str} ]         [ {v11_str}  {v12_str} ]\n"
    texto += f"      [ {e2_str} ]         [ {v21_str}  {v22_str} ]\n"
    # Clasificación final
    texto += f"    → Clasificación = {info['clasif']}\n\n"

# 5. Generar versión numérica del campo con lambdify
f1_np = sp.lambdify((x_sym, y_sym), ecu1, 'numpy')
f2_np = sp.lambdify((x_sym, y_sym), ecu2, 'numpy')

def campo(xv, yv):
    return f1_np(xv, yv), f2_np(xv, yv)

# 6. Dibujar diagrama de fases, núclinas y cuadro de texto al costado
limite = 4.0
res = 400
xs = np.linspace(-limite, limite, res)
ys = np.linspace(-limite, limite, res)
Xg, Yg = np.meshgrid(xs, ys)
Ug, Vg = campo(Xg, Yg)

# Usamos GridSpec para aprovechar mejor el espacio horizontal:
fig = plt.figure(figsize=(12, 6))
gs = fig.add_gridspec(1, 2, width_ratios=[3, 2], wspace=0.3)

# Subplot 1: diagrama de fases (más ancho)
ax1 = fig.add_subplot(gs[0, 0])
# Campo vectorial
ax1.streamplot(Xg, Yg, Ug, Vg, density=1.1, linewidth=0.7, arrowsize=1)

# Núclinas: curvas f1 = 0 (x-núclina) y f2 = 0 (y-núclina)
# Dibujamos contornos donde Ug = 0 y Vg = 0
nc1 = ax1.contour(
    Xg, Yg, Ug,
    levels=[0], colors='tab:blue', linestyles='--', linewidths=1,
    alpha=0.8
)
nc2 = ax1.contour(
    Xg, Yg, Vg,
    levels=[0], colors='tab:green', linestyles='-.', linewidths=1,
    alpha=0.8
)
# Agregamos leyenda manual para núclinas
nc1_proxy = plt.Line2D([0], [0], color='tab:blue', linestyle='--')
nc2_proxy = plt.Line2D([0], [0], color='tab:green', linestyle='-.')
ax1.legend(
    [nc1_proxy, nc2_proxy],
    ["x-núclina (f1=0)", "y-núclina (f2=0)"],
    loc='upper right', fontsize=8, framealpha=0.7
)

# Marcamos y etiquetamos cada punto de equilibrio
for info in puntos_eq:
    px, py = info['coords']
    ax1.plot(float(px), float(py), 'ro')
    ax1.text(float(px) + 0.05, float(py) + 0.05, info['clasif'],
             color='r', fontsize=8)

ax1.set_title("Diagrama de fases con núclinas")
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.axhline(0, color='k', linewidth=0.5)
ax1.axvline(0, color='k', linewidth=0.5)
ax1.set_xlim(-limite, limite)
ax1.set_ylim(-limite, limite)
ax1.set_aspect('equal')

# Subplot 2: cuadro de texto con toda la info (monospace para alinear)
ax2 = fig.add_subplot(gs[0, 1])
ax2.axis('off')
caja = dict(boxstyle='round', facecolor='white', alpha=0.8)
ax2.text(
    0, 1, texto,
    fontsize=9, va='top', ha='left',
    fontfamily='monospace', bbox=caja
)

plt.show()
