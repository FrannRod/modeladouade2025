import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import inspect

# ========== 1. Definición del sistema ==========
A = np.array([[-1, 0],
              [0, -2]], dtype=float)

def b(t): # Cambiá esta función a gusto
    array = [t, -t]
    return np.array(array, dtype=float)

def get_b_str(bfunc):
    src = inspect.getsource(bfunc).strip()
    for line in src.split('\n'):
        if 'array = ' in line:
            return line.replace('array = ', '').strip()
    return "b(t)"

# ========== 2. Sistema homogéneo ==========
determinante = np.linalg.det(A)
traza = np.trace(A)
discriminante = traza**2 - 4*determinante
autovalores, autovectores = np.linalg.eig(A)

if discriminante < 0:
    tipo = "Foco" if traza != 0 else "Centro"
elif discriminante > 0:
    if all(autovalores > 0):
        tipo = "Nodo inestable"
    elif all(autovalores < 0):
        tipo = "Nodo estable"
    elif autovalores[0]*autovalores[1] < 0:
        tipo = "Silla de montar"
    else:
        tipo = "Indeterminado"
else:
    tipo = "Nodo degenerado"

def sistema_homogeneo(t, X):
    return A @ X

def sistema_no_homogeneo(t, X):
    return A @ X + b(t)

# --- Ajuste del zoom y puntos iniciales ---
zoom = 3
x1 = np.linspace(-zoom, zoom, 20)
x2 = np.linspace(-zoom, zoom, 20)
X1, X2 = np.meshgrid(x1, x2)

fig, axs = plt.subplots(1,2, figsize=(14,7))

# ========== 3. Diagrama de fases (homogéneo) ==========
ax = axs[0]
ax.set_title(
    f"Sistema homogéneo\nx' = {A[0,0]}x + {A[0,1]}y\ny' = {A[1,0]}x + {A[1,1]}y",
    pad=15)
U = A[0,0]*X1 + A[0,1]*X2
V = A[1,0]*X1 + A[1,1]*X2
ax.quiver(X1, X2, U, V, color='gray', alpha=0.5)
ax.set_xlabel("x")
ax.set_ylabel("y")

# Trayectorias cerca del origen:
init_points = []
r = np.linspace(-2, 2, 7)
for v in r:
    init_points += [(v, 0), (0, v), (v, v)]
init_points += [(-1, 1), (1, -1), (-1, -1), (1, 1)]

for x0 in init_points:
    sol = solve_ivp(sistema_homogeneo, [0, 3], x0, t_eval=np.linspace(0,3,200))
    ax.plot(sol.y[0], sol.y[1], linewidth=1.1)
eq_hom, = ax.plot(0, 0, 'ro', markersize=8, label="Punto de equilibrio")
ax.grid(alpha=0.3)
ax.set_xlim(-zoom, zoom)
ax.set_ylim(-zoom, zoom)
ax.legend(loc='upper right', fontsize=9)

# ========== 4. Sistema no homogéneo ==========
ax = axs[1]
b_str = get_b_str(b)
ax.set_title(
    f"Sistema no homogéneo\nx' = {A[0,0]}x + {A[0,1]}y + {b_str}\ny' = {A[1,0]}x + {A[1,1]}y",
    pad=15)
U = A[0,0]*X1 + A[0,1]*X2 + b(0)[0]
V = A[1,0]*X1 + A[1,1]*X2 + b(0)[1]
ax.quiver(X1, X2, U, V, color='gray', alpha=0.5)
ax.set_xlabel("x")
ax.set_ylabel("y")

for x0 in init_points:
    sol = solve_ivp(sistema_no_homogeneo, [0, 3], x0, t_eval=np.linspace(0,3,200))
    ax.plot(sol.y[0], sol.y[1], linewidth=1.1)

# Aviso: no hay punto de equilibrio fijo para b(t) no constante
ax.annotate("Sin punto de equilibrio fijo\n(b depende de t)",
            xy=(ax.get_xlim()[0]+0.1, ax.get_ylim()[1]-0.5),
            color='red',
            fontsize=9,
            ha='left', va='top',
            bbox=dict(facecolor='white', alpha=0.85, edgecolor='red'))

# ========== 5. Neclinas (en t=0, sólo como referencia visual) ==========
x_vals = np.linspace(-zoom, zoom, 400)
handles = []
labels = []

if A[0,1] != 0:
    y_neclina_x = (-A[0,0]*x_vals - b(0)[0])/A[0,1]
    neclina_x, = ax.plot(x_vals, y_neclina_x, 'g--', label="Neclina x'", linewidth=1.2)
    handles.append(neclina_x)
    labels.append("Neclina x'")
if A[1,1] != 0:
    y_neclina_y = (-A[1,0]*x_vals - b(0)[1])/A[1,1]
    neclina_y, = ax.plot(x_vals, y_neclina_y, 'b--', label="Neclina y'", linewidth=1.5)
    handles.append(neclina_y)
    labels.append("Neclina y'")

ax.set_xlim(-zoom, zoom)
ax.set_ylim(-zoom, zoom)
if handles:
    ax.legend(handles, labels, loc='upper right', fontsize=9)
ax.grid(alpha=0.3)

# ========== 6. Texto informativo ==========
info_text = (
    f"Matriz A = {A.tolist()}\n"
    f"Determinante: {determinante:.3f} | "
    f"Traza (Tau): {traza:.3f} | "
    f"Discriminante: {discriminante:.3f}\n"
    f"Autovalores: {np.round(autovalores,3)}\n"
    f"Tipo de sistema: {tipo}\n"
    f"b(t) = {b_str}\n"
    f"Punto de equilibrio sistema no homogéneo: NO EXISTE, b(t) depende de t"
)
fig.text(0.5, 0.05, info_text, ha='center', va='center', fontsize=10, family='monospace', bbox=dict(facecolor='white', alpha=0.93, edgecolor='gray'))

plt.subplots_adjust(bottom=0.18, wspace=0.27, right=0.95)
plt.show()
