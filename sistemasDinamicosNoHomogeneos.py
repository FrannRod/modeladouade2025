import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import inspect

A = np.array([[1, 2],
              [0, -1]], dtype=float)

def b(t):
    return np.array([t, -t], dtype=float)

def get_b_str(bfunc):
    src = inspect.getsource(bfunc).strip()
    for line in src.split('\n'):
        if 'return' in line:
            return line.strip().replace('return np.array(', '').replace(', dtype=float)', '')
    return "b(t)"

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

# Seteo de condiciones iniciales: cercanas al origen y sobre los autovectores
init_points = []
radii = np.linspace(-1.2, 1.2, 7)
for r in radii:
    init_points.append([r, 0])
    init_points.append([0, r])
    # agrego sobre autovectores (normalizados)
    v1 = autovectores[:,0] / np.linalg.norm(autovectores[:,0])
    v2 = autovectores[:,1] / np.linalg.norm(autovectores[:,1])
    init_points.append(r * v1)
    init_points.append(r * v2)

zoom = 3
x1 = np.linspace(-zoom, zoom, 22)
x2 = np.linspace(-zoom, zoom, 22)
X1, X2 = np.meshgrid(x1, x2)

fig, axs = plt.subplots(1, 2, figsize=(13,8))

# ---- Gráfico homogéneo ----
ax = axs[0]
ax.set_title(f"Sistema homogéneo\nx' = {A[0,0]}x + {A[0,1]}y\ny' = {A[1,0]}x + {A[1,1]}y", pad=12)
U = A[0,0]*X1 + A[0,1]*X2
V = A[1,0]*X1 + A[1,1]*X2
ax.quiver(X1, X2, U, V, color='gray', alpha=0.5)
ax.set_xlabel("x")
ax.set_ylabel("y")

# Trajectorias: solo en rango [0, 2] para evitar desbordes
t_span = [0, 2]
for x0 in init_points:
    sol = solve_ivp(sistema_homogeneo, t_span, x0, t_eval=np.linspace(*t_span, 250))
    ax.plot(sol.y[0], sol.y[1], linewidth=1.0, alpha=0.9)
ax.plot(0, 0, 'ro', markersize=8, label="Punto de equilibrio")

# Autovectores normalizados, largos = 1
for i, color in enumerate(['blue', 'green']):
    vec = autovectores[:, i]
    vec_norm = vec / np.linalg.norm(vec)
    ax.arrow(0, 0, vec_norm[0], vec_norm[1],
             color=color, head_width=0.15, head_length=0.23, linewidth=2.2, length_includes_head=True)
    ax.text(vec_norm[0]*1.1, vec_norm[1]*1.1, f'v{i+1}', fontsize=12, color=color, fontweight='bold')

ax.set_xlim(-zoom, zoom)
ax.set_ylim(-zoom, zoom)
ax.grid(alpha=0.3)
ax.legend(loc='upper right', fontsize=9)

# ---- Gráfico no homogéneo ----
ax = axs[1]
b_str = get_b_str(b)
ax.set_title(f"Sistema no homogéneo\nx' = {A[0,0]}x + {A[0,1]}y + {b_str}\ny' = {A[1,0]}x + {A[1,1]}y", pad=12)
U = A[0,0]*X1 + A[0,1]*X2 + b(0)[0]
V = A[1,0]*X1 + A[1,1]*X2 + b(0)[1]
ax.quiver(X1, X2, U, V, color='gray', alpha=0.5)
ax.set_xlabel("x")
ax.set_ylabel("y")

# Trayectorias del no homogéneo, también en rango corto
for x0 in init_points:
    sol = solve_ivp(sistema_no_homogeneo, t_span, x0, t_eval=np.linspace(*t_span, 250))
    ax.plot(sol.y[0], sol.y[1], linewidth=1.0, alpha=0.9)

# Neclinas (t=0)
x_vals = np.linspace(-zoom, zoom, 400)
if A[0,1] != 0:
    y_neclina_x = (-A[0,0]*x_vals - b(0)[0])/A[0,1]
    ax.plot(x_vals, y_neclina_x, 'g--', label="Neclina x'", linewidth=1.3)
if A[1,1] != 0:
    y_neclina_y = (-A[1,0]*x_vals - b(0)[1])/A[1,1]
    ax.plot(x_vals, y_neclina_y, 'b--', label="Neclina y'", linewidth=1.3)

ax.set_xlim(-zoom, zoom)
ax.set_ylim(-zoom, zoom)
ax.grid(alpha=0.3)
ax.legend(loc='upper right', fontsize=10)
ax.annotate("Sin punto de equilibrio fijo\n(b depende de t)",
            xy=(ax.get_xlim()[0]+0.1, ax.get_ylim()[1]-0.5),
            color='red', fontsize=9,
            ha='left', va='top',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='red'))

# ---- Texto informativo ----
info_text = (
    f"Matriz A = {A.tolist()}\n"
    f"Determinante: {determinante:.3f} | Traza (Tau): {traza:.3f} | Discriminante: {discriminante:.3f}\n"
    f"Autovalores: {np.round(autovalores,3)}\n"
    f"Tipo de sistema: {tipo}\n"
    f"b(t) = {b_str}\n"
    "Punto de equilibrio sistema no homogéneo: NO EXISTE, b(t) depende de t"
)
fig.text(0.5, 0.02, info_text, ha='center', va='bottom', fontsize=10, family='monospace', bbox=dict(facecolor='white', alpha=0.95, edgecolor='gray'))

plt.subplots_adjust(bottom=0.19, wspace=0.23, right=0.97, top=0.93)
plt.show()
