import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Configurar backend para evitar errores en PyCharm
matplotlib.use('TkAgg')

def f(x):
    return x**2 - 2

a, b = 0, 1  # Intervalo de integración
n = 4  # Número de subintervalos
dx = (b - a) / n  # Ancho de cada subintervalo

# Puntos donde se evaluará la función (extremo derecho de cada subintervalo)
x_right = np.linspace(a, b - dx, n) + dx
heights = f(x_right)  # Alturas de los rectángulos

# Cálculo de la suma de Riemann
riemann_sum = np.sum(heights * dx)
print(f"Suma de Riemann: {round(riemann_sum,2)}")

# Graficar la función
x = np.linspace(a, b, 100)
y = f(x)
plt.plot(x, y, 'r', label='$f(x) = x^2 - 2$')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)

# Graficar los rectángulos
for i in range(n):
    plt.bar(x_right[i] - dx, heights[i], width=dx, align='edge', color='blue', edgecolor='black', alpha=0.5)

plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Suma de Riemann - Extremo derecho')
plt.legend()

# Guardar en archivo en lugar de mostrar directamente
plt.savefig("riemann_plot.png")
print("Gráfico guardado como 'riemann_plot.png'")

plt.show()