import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# ========== 1. Definición del sistema ==========
A = np.array([[1, 0],
              [0, -2]], dtype=float)

def b(t):
    return np.array([np.cos(t), 0], dtype=float)  # Vector no constante

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

# --- Ajuste del zoom: usá [-3,3] o el rango que te quede más cómodo ---
x1 = np.linspace(-3, 3, 20)
x2 = np.linspace(-3, 3, 20)
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

for x0 in [(-2, -2), (-2, 2), (2, -2), (2, 2), (0, 2), (2, 0), (-2, 0), (0, -2)]:
    sol = solve_ivp(sistema_homogeneo, [0, 3], x0, t_eval=np.linspace(0,3,200))
    plt.plot(sol.y[0], sol.y[1], linewidth=1.5)

eq_hom, = plt.plot(0, 0, 'ro', markersize=8, label="Punto de equilibrio")
plt.grid(alpha=0.3)
plt.xlim(-3, 3)
plt.ylim(-3, 3)
plt.legend(loc='upper right', fontsize=9)

# ========== 4. Sistema no homogéneo ==========
plt.subplot(1,2,2)
plt.title(f"Sistema no homogéneo\nx' = {A[0,0]}x + {A[0,1]}y + e^t\ny' = {A[1,0]}x + {A[1,1]}y", pad=20)
U = A[0,0]*X1 + A[0,1]*X2 + b(0)[0]
V = A[1,0]*X1 + A[1,1]*X2 + b(0)[1]
plt.quiver(X1, X2, U, V, color='gray', alpha=0.5)
plt.xlabel("x")
plt.ylabel("y")

for x0 in [(-2, -2), (-2, 2), (2, -2), (2, 2), (0, 2), (2, 0), (-2, 0), (0, -2)]:
    sol = solve_ivp(sistema_no_homogeneo, [0, 3], x0, t_eval=np.linspace(0,3,200))
    plt.plot(sol.y[0], sol.y[1], linewidth=1.5)

# Aviso: no hay punto de equilibrio fijo para b(t) no constante
plt.text(-2.9, 2.4, "Sin punto de equilibrio fijo\n(b depende de t)", fontsize=9, color='red', bbox=dict(facecolor='white', alpha=0.7, edgecolor='red'))

# ========== 5. Neclinas (en t=0, sólo como referencia visual) ==========
x_vals = np.linspace(-3, 3, 400)
handles = []
labels = []

if A[0,1] != 0:
    y_neclina_x = (-A[0,0]*x_vals - b(0)[0])/A[0,1]
    neclina_x, = plt.plot(x_vals, y_neclina_x, 'g--', label="Neclina x'", linewidth=1.5)
    handles.append(neclina_x)
    labels.append("Neclina x'")
if A[1,1] != 0:
    y_neclina_y = (-A[1,0]*x_vals - b(0)[1])/A[1,1]
    neclina_y, = plt.plot(x_vals, y_neclina_y, 'b--', label="Neclina y'", linewidth=1.5)
    handles.append(neclina_y)
    labels.append("Neclina y'")

plt.xlim(-3, 3)
plt.ylim(-3, 3)
if handles:
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
    f"Punto de equilibrio sistema no homogéneo: NO EXISTE, b(t) depende de t"
)
plt.figtext(0.5, 0.01, info_text, ha='center', va='bottom', fontsize=9, family='monospace')

plt.subplots_adjust(bottom=0.23, wspace=0.35, right=0.88)
plt.show()
