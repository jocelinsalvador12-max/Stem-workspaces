import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ===============================
# GENERADOR LCG
# ===============================
def generador_lcg(n, semilla, a, c, m):
    numeros = []
    x = semilla
    for _ in range(n):
        x = (a * x + c) % m
        numeros.append(x / m)
    return np.array(numeros)


# ===============================
# PRUEBAS
# ===============================
def test_uniformidad(datos):
    f_obs, _ = np.histogram(datos, bins=10, range=(0,1))
    f_exp = len(datos) / 10
    chi_stat, p_val = stats.chisquare(f_obs, f_exp)
    return chi_stat, p_val


def test_rachas(datos):
    media = np.mean(datos)
    secuencia = [1 if x >= media else 0 for x in datos]

    rachas = 1
    for i in range(1, len(secuencia)):
        if secuencia[i] != secuencia[i-1]:
            rachas += 1

    n1 = secuencia.count(1)
    n0 = secuencia.count(0)

    media_r = ((2 * n1 * n0) / (n1 + n0)) + 1
    var_r = (2 * n1 * n0 * (2 * n1 * n0 - n1 - n0)) / (((n1 + n0)**2) * (n1 + n0 - 1))
    z = (rachas - media_r) / np.sqrt(var_r)

    return z


# ===============================
# ENTRADAS EDITABLES
# ===============================
print("=== CONFIGURACIÓN ===")

n = int(input("Cantidad de números (ej. 1000): "))
semilla = int(input("Semilla: "))
a = int(input("Multiplicador (a): "))
c = int(input("Incremento (c): "))
m = int(input("Módulo (m): "))

# ===============================
# GENERAR DATOS
# ===============================
datos = generador_lcg(n, semilla, a, c, m)

# ===============================
# PRUEBAS
# ===============================
chi, p = test_uniformidad(datos)
z = test_rachas(datos)

# ===============================
# RESULTADOS EN CONSOLA
# ===============================
print("\n=== RESULTADOS ===")
print(f"Chi²: {chi:.4f}")
print(f"P-valor: {p:.4f} -> {'PASA' if p > 0.05 else 'FALLA'}")
print(f"Z (Rachas): {z:.4f} -> {'PASA' if abs(z) < 1.96 else 'FALLA'}")

# ===============================
# GRÁFICAS TODAS JUNTAS
# ===============================
fig, axs = plt.subplots(1, 3, figsize=(15,5))

# 1. Histograma
axs[0].hist(datos, bins=10)
axs[0].set_title("Uniformidad")

# 2. Dispersión
axs[1].scatter(datos[:-1], datos[1:], s=5)
axs[1].set_title("Independencia")

# 3. Serie
axs[2].plot(datos[:100])  # primeros 100 para ver comportamiento
axs[2].set_title("Serie (primeros 100)")

plt.suptitle(f"LCG (n={n}, a={a}, c={c}, m={m})")
plt.tight_layout()
plt.show()