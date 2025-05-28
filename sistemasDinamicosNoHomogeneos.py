import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# ========== 1. Definición del sistema ==========
A = np.array([[-1, 0],
              [0, -2]], dtype=float)

def b(t):
    return np.array([np.cos(3*t), 0], dtype=float)

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

x1 = np.linspace(-5, 5, 20)
x2 = np.linspace(-5, 5, 20)
X1, X2 = np.meshgrid(x1, x2)

plt.figure(figsize=(15, 8))

# ========== 3. Diagrama de fases (homogéneo) ==========
plt.subplot(1,2,1)
plt.title(f"Sistema homogéneo\nx' = {A[0,0]}x + {A[0,1]}y\ny' = {A[1,0]}x + {A[1,1]}y", pad=20)
U = A[0,0]*X1 + A[0,1]*X2
V = A[1,0]*X1 + A[1,1]*X2
plt.quiver(X1, X2, U, V, color='gray', alpha=0.5)
plt.xlabel("x")
plt.ylabel("y")

for x0 in [(-4, -4), (-4, 4), (4, -4), (4, 4), (0, 3), (3, 0), (-3, 0), (0, -3)]:
    sol = solve_ivp(sistema_homogeneo, [0, 5], x0, t_eval=np.linspace(0,5,200))
    plt.plot(sol.y[0], sol.y[1], linewidth=1.5)

eq_hom, = plt.plot(0, 0, 'ro', markersize=8, label="Punto de equilibrio")
plt.grid(alpha=0.3)
plt.legend(loc='upper right', fontsize=9)

# ========== 4. Sistema no homogéneo ==========
t = 0  # Valor inicial para t
xp = -np.linalg.inv(A) @ b(t)

plt.subplot(1,2,2)
plt.title(f"Sistema no homogéneo\nx' = {A[0,0]}x + {A[0,1]}y + e^t\ny' = {A[1,0]}x + {A[1,1]}y", pad=20)
U = A[0,0]*X1 + A[0,1]*X2 + b(0)[0]
V = A[1,0]*X1 + A[1,1]*X2 + b(0)[1]
plt.quiver(X1, X2, U, V, color='gray', alpha=0.5)
plt.xlabel("x")
plt.ylabel("y")

for x0 in [(-4, -4), (-4, 4), (4, -4), (4, 4), (0, 3), (3, 0), (-3, 0), (0, -3)]:
    sol = solve_ivp(sistema_no_homogeneo, [0, 5], x0, t_eval=np.linspace(0,5,200))
    plt.plot(sol.y[0], sol.y[1], linewidth=1.5)

eq_nh, = plt.plot(*xp, 'ro', markersize=10, label="Punto de equilibrio")

# ========== 5. Neclinas ==========
# x' = a11 x + a12 y + b1 = 0 --> y = (-a11 x - b1)/a12
# y' = a21 x + a22 y + b2 = 0 --> y = (-a21 x - b2)/a22
x_vals = np.linspace(-5, 5, 400)
if A[0,1] != 0:
    y_neclina_x = (-A[0,0]*x_vals - b(0)[0])/A[0,1]
    neclina_x, = plt.plot(x_vals, y_neclina_x, 'g--', label="Neclina x'", linewidth=1.5)
else:
    neclina_x = None
if A[1,1] != 0:
    y_neclina_y = (-A[1,0]*x_vals - b(0)[1])/A[1,1]
    neclina_y, = plt.plot(x_vals, y_neclina_y, 'b--', label="Neclina y'", linewidth=1.5)
else:
    neclina_y = None

plt.xlim(-5,5)
plt.ylim(-5,5)

# Solo una leyenda por label
handles = [eq_nh]
labels = ["Punto de equilibrio"]
if neclina_x:
    handles.append(neclina_x)
    labels.append("Neclina x'")
if neclina_y:
    handles.append(neclina_y)
    labels.append("Neclina y'")

plt.legend(handles, labels, loc='upper right', fontsize=9)
plt.grid(alpha=0.3)

# ========== 6. Texto informativo ==========
info_text = (
    f"Matriz A:\n{A}\n\n"
    f"Determinante: {determinante:.3f}\n"
    f"Traza (Tau): {traza:.3f}\n"
    f"Discriminante: {discriminante:.3f}\n"
    f"Autovalores: {autovalores}\n"
    f"Autovectores (columnas):\n{autovectores}\n"
    f"Tipo de sistema: {tipo}\n"
    f"Punto de equilibrio sistema no homogéneo: {xp}\n"
)
plt.figtext(0.5, 0.01, info_text, ha='center', va='bottom', fontsize=9, family='monospace')

plt.subplots_adjust(bottom=0.23, wspace=0.35, right=0.88)
plt.show()
