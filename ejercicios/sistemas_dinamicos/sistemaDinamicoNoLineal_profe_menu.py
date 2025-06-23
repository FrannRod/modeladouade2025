import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import tkinter as tk
from tkinter import ttk, messagebox
from numpy.linalg import eig, inv


# Función para graficar el sistema
def graficar_sistema(nombre, sistema, A=None, mostrar_autovec=False, x_eq=None):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_title(nombre)
    zoom = 3
    x = np.linspace(-zoom, zoom, 20)
    y = np.linspace(-zoom, zoom, 20)
    X, Y = np.meshgrid(x, y)
    U, V = np.zeros_like(X), np.zeros_like(Y)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            dxdt, dydt = sistema(0, [X[i, j], Y[i, j]])
            U[i, j], V[i, j] = dxdt, dydt

    N = np.sqrt(U**2 + V**2)
    U_norm = U / (N + 1e-8)
    V_norm = V / (N + 1e-8)
    ax.quiver(X, Y, U_norm, V_norm, color='gray')

    init_conds = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0.5, 0), (0, 0.5)]
    for ic in init_conds:
        sol = solve_ivp(sistema, [0, 10], ic, t_eval=np.linspace(0, 10, 500))
        ax.plot(sol.y[0], sol.y[1], lw=1)

    if A is not None and mostrar_autovec:
        vals, vecs = eig(A)
        for i in range(vecs.shape[1]):
            v = vecs[:, i].real
            v = v / np.linalg.norm(v)
            ax.plot([0, 3 * v[0]], [0, 3 * v[1]], 'g--', lw=2)
            ax.plot([0, -3 * v[0]], [0, -3 * v[1]], 'g--', lw=2)
        ax.text(-2.8, 2.6, f"Autovalores: {np.round(vals, 2)}", fontsize=10)

    if x_eq is not None:
        ax.plot(x_eq[0], x_eq[1], 'ro', markersize=8)
        ax.text(x_eq[0] + 0.2, x_eq[1], 'Equilibrio desplazado', color='red')

    def on_click(event):
        if event.inaxes == ax:
            ic = [event.xdata, event.ydata]
            sol_f = solve_ivp(sistema, [0, 10], ic, t_eval=np.linspace(0, 10, 500))
            sol_b = solve_ivp(sistema, [0, -10], ic, t_eval=np.linspace(0, -10, 500))
            ax.plot(sol_f.y[0], sol_f.y[1], 'r', lw=2)
            ax.plot(sol_b.y[0], sol_b.y[1], 'b--', lw=1)
            fig.canvas.draw()

    fig.canvas.mpl_connect('button_press_event', on_click)
    ax.set_xlim(-zoom, zoom)
    ax.set_ylim(-zoom, zoom)
    ax.grid()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


# GUI
def main_gui():
    root = tk.Tk()
    root.title('Simulador de Sistemas Dinámicos')
    root.geometry('520x450')

    sistemas_famosos = {
        "Van der Pol": {
            "dx": "y",
            "dy": "mu*(1 - x**2)*y - x",
            "A": "",
            "f": "",
            "params": {"mu": 1.0}
        },
        "Nodo espiral (inestable)": {
            "dx": "x - y",
            "dy": "x + y",
            "A": "1 -1; 1 1",
            "f": "",
        },
        "Nodo fuente": {
            "dx": "2*x",
            "dy": "3*y",
            "A": "2 0; 0 3",
            "f": "",
        },
        "Silla": {
            "dx": "x",
            "dy": "-y",
            "A": "1 0; 0 -1",
            "f": "",
        },
        "Centro": {
            "dx": "-y",
            "dy": "x",
            "A": "0 -1; 1 0",
            "f": "",
        },
        "Sistema no homogéneo": {
            "dx": "0",
            "dy": "0",
            "A": "0 1; -1 0",
            "f": "[0, np.sin(t)]",
        }
    }

    selected_system = tk.StringVar()
    tk.Label(root, text="Selecciona un sistema famoso:").pack()
    dropdown = ttk.Combobox(root, textvariable=selected_system, values=list(sistemas_famosos.keys()))
    dropdown.pack()

    def cargar_sistema(event=None):
        nombre = selected_system.get()
        if nombre in sistemas_famosos:
            config = sistemas_famosos[nombre]
            dx_entry.delete(0, tk.END)
            dx_entry.insert(0, config["dx"])
            dy_entry.delete(0, tk.END)
            dy_entry.insert(0, config["dy"])
            A_entry.delete(0, tk.END)
            A_entry.insert(0, config.get("A", ""))
            ft_entry.delete(0, tk.END)
            ft_entry.insert(0, config.get("f", ""))

    dropdown.bind("<<ComboboxSelected>>", cargar_sistema)

    tk.Label(root, text='dx/dt =').pack()
    dx_entry = tk.Entry(root, width=40)
    dx_entry.pack()

    tk.Label(root, text='dy/dt =').pack()
    dy_entry = tk.Entry(root, width=40)
    dy_entry.pack()

    tk.Label(root, text='Matriz A (opcional):').pack()
    A_entry = tk.Entry(root, width=40)
    A_entry.pack()

    tk.Label(root, text='Campo f(t) (opcional):').pack()
    ft_entry = tk.Entry(root, width=40)
    ft_entry.pack()

    autovec_check = tk.BooleanVar()
    autovec_check.set(True)
    tk.Checkbutton(root, text='Mostrar autovectores y neutros', variable=autovec_check).pack()

    def plot_field():
        dx_formula = dx_entry.get()
        dy_formula = dy_entry.get()
        A_text = A_entry.get()
        ft_text = ft_entry.get()
        mostrar_autovec = autovec_check.get()

        A = None
        if A_text.strip():
            try:
                filas = A_text.strip().split(';')
                A = np.array([[float(num) for num in fila.strip().split()] for fila in filas])
                if A.shape != (2, 2):
                    raise ValueError("A debe ser 2x2")
            except Exception as e:
                messagebox.showerror("Error", f"Error en matriz A: {e}")
                return

        def sistema(t, z):
            x, y = z
            local_vars = {'x': x, 'y': y, 'np': np, 't': t, 'mu': 1.0}
            dx = eval(dx_formula, local_vars)
            dy = eval(dy_formula, local_vars)

            ft = None
            if ft_text.strip():
                try:
                    ft = eval(ft_text, {'t': t, 'np': np})
                except Exception as e:
                    messagebox.showerror("Error", f"Error en f(t): {e}")
                    raise

            if A is not None:
                dx += A[0, 0]*x + A[0, 1]*y
                dy += A[1, 0]*x + A[1, 1]*y
            if ft is not None:
                dx += ft[0]
                dy += ft[1]

            return [dx, dy]

        x_eq = None
        if A is not None and ft_text.strip():
            try:
                ft0 = eval(ft_text, {'t': 0, 'np': np})
                x_eq = -inv(A) @ ft0
            except Exception as e:
                messagebox.showwarning("Advertencia", f"No se pudo calcular el equilibrio desplazado: {e}")

        nombre = f"Sistema: dx={dx_formula}, dy={dy_formula}"
        graficar_sistema(nombre, sistema, A=A, mostrar_autovec=mostrar_autovec, x_eq=x_eq)

    tk.Button(root, text='Graficar campo', command=plot_field).pack(pady=10)

    root.mainloop()


main_gui()
