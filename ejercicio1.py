import sympy
import sympy as sp

# Definir la variable
x = sp.symbols('x')

# Definir la función que deseas integrar
funcion = sp.sin(x)  # Por ejemplo, la función seno

# Calcular la integral indefinida
integral_indefinida = sp.integrate(funcion, x)
print(f'Integral indefinida de sin(x): {integral_indefinida}')

# Calcular la integral definida de 0 a pi
integral_definida = sp.integrate(funcion, (x, 0, sp.pi))
print(f'Integral definida de sin(x) de 0 a pi: {integral_definida}')