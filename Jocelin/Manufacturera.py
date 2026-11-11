import numpy as np
import matplotlib.pyplot as plt

# Seteo de semilla para asegurar que el docente vea los mismos resultados (Replicabilidad)
np.random.seed(42) 

# Configuración de la simulación
iteraciones = 10000  
precio_venta = 120
costos_fijos = 40000

# 1. Generación de variables aleatorias
# np.random.normal genera valores con distribución de campana de Gauss
demanda = np.random.normal(1000, 200, iteraciones)

# np.random.uniform genera valores donde cualquier punto entre 45 y 55 tiene igual probabilidad
costo_unitario = np.random.uniform(45, 55, iteraciones)

# 2. Modelo determinístico aplicado a cada ensayo de Monte Carlo
# Utilidad = (Demanda * Margen Unitario) - Gastos Operativos
utilidades = (demanda * (precio_venta - costo_unitario)) - costos_fijos

# 3. Análisis Estadístico
utilidad_promedio = np.mean(utilidades) # Calcula la esperanza matemática
probabilidad_perdida = (np.sum(utilidades < 0) / iteraciones) * 100 # Conteo de casos negativos

print(f"Utilidad Promedio Esperada: ${utilidad_promedio:.2f}")
print(f"Probabilidad de tener pérdidas: {probabilidad_perdida:.2f}%")