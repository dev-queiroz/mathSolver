import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sympy as sp
import numpy as np
import io
import base64

def plot_2d(expr, label):
    try:
        x = sp.Symbol('x')
        if not expr.free_symbols:
            return None

        x_vals = np.linspace(-10, 10, 100)
        y_vals = [float(expr.subs(x, val)) for val in x_vals]

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label=label)
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.legend()
        ax.grid(True)
        ax.set_title(f"Gráfico 2D: {label}")

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
        return img_str
    except Exception:
        return None

def plot_3d(equation_str):
    try:
        x, y = sp.Symbol('x'), sp.Symbol('y')
        expr = sp.sympify(equation_str.split('=')[1])
        x_vals = np.linspace(-5, 5, 50)
        y_vals = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = np.array([[float(expr.subs({'x': x_val, 'y': y_val})) 
                       for x_val in x_vals] for y_val in y_vals])

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f"Gráfico 3D: {equation_str}")

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
        return img_str
    except Exception:
        return None