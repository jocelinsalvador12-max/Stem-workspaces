import random
import math
import psycopg2
import numpy as np
from scipy.stats import chisquare

# =========================
# CONEXIÓN A POSTGRESQL
# =========================

conexion = psycopg2.connect(
    host="localhost",
    database="simulacion",
    user="postgres",
    password="flores"
)

cursor = conexion.cursor()

# =========================
# LISTAS PARA DATOS
# =========================

tiempos_llegada = []
tiempos_respuesta = []

# =========================
# GENERAR 100 SIMULACIONES
# =========================

for i in range(100):

    # --------------------------------
    # 1. TRANSFORMADA INVERSA
    # --------------------------------

    r = random.random()

    tiempo_llegada = -200 * math.log(1 - r)

    tiempos_llegada.append(tiempo_llegada)

    # --------------------------------
    # 2. MÉTODO DE COMPOSICIÓN
    # --------------------------------

    r1 = random.random()

    if r1 < 0.8:
        tipo = "GET"
        media = 50
    else:
        tipo = "POST"
        media = 120

    # --------------------------------
    # 3. MÉTODO DE CONVOLUCIÓN
    # --------------------------------

    total = 0

    for j in range(4):

        r2 = random.random()

        subproceso = -media * math.log(1 - r2)

        total += subproceso

    tiempo_respuesta = total

    tiempos_respuesta.append(tiempo_respuesta)

    # --------------------------------
    # GUARDAR EN POSTGRESQL
    # --------------------------------

    cursor.execute("""
        INSERT INTO metricas_simulacion
        (tipo_peticion, tiempo_llegada, tiempo_respuesta)
        VALUES (%s, %s, %s)
    """, (tipo, tiempo_llegada, tiempo_respuesta))

# =========================
# GUARDAR CAMBIOS
# =========================

conexion.commit()

# =========================
# PRUEBA CHI-CUADRADA
# =========================

# Histograma observado
observado, bins = np.histogram(tiempos_llegada, bins=10)

# Frecuencia esperada uniforme
esperado = [len(tiempos_llegada)/10] * 10

chi, p = chisquare(observado, esperado)

print("\n========= RESULTADOS =========")
print("Chi-cuadrada:", chi)
print("Valor p:", p)

if p > 0.05:
    print("La distribución parece válida.")
else:
    print("La distribución NO parece válida.")

# =========================
# CERRAR CONEXIÓN
# =========================

cursor.close()
conexion.close()

print("\nDatos guardados correctamente.")