import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# 1) Cálculo de puntos de equilibrio y su estabilidad
y = sp.symbols('y')
f_sym = 3*y*(y-2)
eq_points_sym = sp.solve(f_sym, y)
fprime_sym = sp.diff(f_sym, y)

eq_points = sorted([float(pt) for pt in eq_points_sym])
stability = {}
for pt in eq_points:
    fp = float(fprime_sym.subs(y, pt))
    stability[pt] = 'Estable' if fp < 0 else 'Inestable'

print("Puntos de equilibrio y estabilidad:")
for pt, estado in stability.items():
    print(f"  y = {pt:.1f} → {estado} (f' = {float(fprime_sym.subs(y, pt)):.1f})")

# Función numérica
f = sp.lambdify(y, f_sym, 'numpy')


# 2) y' vs y
y_vals = np.linspace(eq_points[0]-1, eq_points[-1]+1, 400)
plt.figure()
plt.plot(y_vals, f(y_vals), linewidth=2)
plt.axhline(0, color='k', lw=0.8)
for pt in eq_points:
    plt.plot(pt, 0, 'ro', ms=6)
plt.xlabel("y")
plt.ylabel("y' = 3y(y-2)")
plt.title("y' en función de y")
plt.grid()


# 3) Diagrama de fase unidimensional
plt.figure(figsize=(2,6))
plt.axvline(0, color='k', lw=1)
y_min, y_max = eq_points[0]-1, eq_points[-1]+1

# marca puntos estables/inestables
for pt in eq_points:
    fp = float(fprime_sym.subs(y, pt))
    if fp < 0:
        plt.plot(0, pt, 'ko', ms=8)      # estable: relleno negro
    else:
        plt.plot(0, pt, 'wo', mec='k', ms=8)  # inestable: círculo vacío

# flechas de convergencia/divergencia
intervals = [(y_min, eq_points[0])] + \
            [(eq_points[i], eq_points[i+1]) for i in range(len(eq_points)-1)] + \
            [(eq_points[-1], y_max)]
for a, b in intervals:
    y_mid = 0.5*(a + b)
    direction = np.sign(f(y_mid))
    plt.arrow(0, y_mid, 0, 0.4*direction,
              head_width=0.05, head_length=0.1,
              length_includes_head=True)

plt.ylim(y_min, y_max)
plt.xticks([])
plt.yticks(eq_points)
plt.ylabel("y")
plt.title("Diagrama de fase")
plt.tight_layout()


# 4) Diagrama de soluciones y(t)
t_span = (0, 10)
t_eval = np.linspace(*t_span, 400)

# condiciones iniciales: 2 en cada región
initials = {
    'y<0': [-1, -2],
    '0<y<2': [0.5, 1.5],
    'y>2': [3, 4]
}

plt.figure()
for region, y0_list in initials.items():
    for y0 in y0_list:
        sol = solve_ivp(lambda t, y: 3*y*(y-2),
                        t_span, [y0], t_eval=t_eval)
        plt.plot(sol.t, sol.y[0], label=f"y(0)={y0:.1f}")

# marcas fuertes de las rectas de equilibrio
for pt in eq_points:
    plt.axhline(pt, color='k', linestyle='--', linewidth=2)

plt.xlabel("t")
plt.ylabel("y(t)")
plt.title("Trayectorias y(t) para distintas condiciones iniciales")
plt.legend(title="Condiciones iniciales", loc='best')
plt.grid()


plt.show()
