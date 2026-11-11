import simpy
import random
import numpy as np

# Configuración de parámetros del sistema
NUM_DIAG_TECH = 1
NUM_SIMPLE_TECH = 1
NUM_COMPLEX_TECH = 1
ARRIVALS_MEAN = 15.0       # Lambda (Exponencial)
DIAG_MIN = 10.0            # Uniforme min
DIAG_MAX = 20.0            # Uniforme max
SIMPLE_MEAN = 12.0         # Exponencial reparación simple
COMPLEX_MEAN = 30.0        # Media Normal compleja
COMPLEX_STD = 5.0          # Desviación estándar Normal compleja
SIM_TIME = 2400            # 40 horas * 60 minutos

# Datos Históricos Reales
VALOR_REAL_HISTORICO = 45.0

# Lista para guardar el tiempo promedio en el sistema de cada una de las 10 réplicas
tiempos_promedio_replicas = []

def laptop_process(env, name, resources, total_system_times):
    # 1. Arribo al sistema (Guardamos la hora de entrada)
    arrival_time = env.now
    
    # 2. Fase de Diagnóstico
    with resources['diagnostico'].request() as req:
        yield req
        diag_duration = random.uniform(DIAG_MIN, DIAG_MAX)
        yield env.timeout(diag_duration)

    # 3. Clasificación
    prob = random.random()
    if prob <= 0.70:
        # 4a. Línea Simple
        with resources['simple'].request() as req:
            yield req
            simple_duration = random.expovariate(1.0 / SIMPLE_MEAN)
            yield env.timeout(simple_duration)
    else:
        # 4b. Línea Compleja
        with resources['complex'].request() as req:
            yield req
            complex_duration = random.normalvariate(COMPLEX_MEAN, COMPLEX_STD)
            yield env.timeout(complex_duration)
            
    # 5. Salida del sistema (Calculamos el tiempo total del ciclo completo)
    exit_time = env.now
    time_in_system = exit_time - arrival_time
    total_system_times.append(time_in_system)

def laptop_generator(env, resources, total_system_times):
    laptop_id = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / ARRIVALS_MEAN))
        laptop_id += 1
        env.process(laptop_process(env, f'Laptop_{laptop_id}', resources, total_system_times))

# =============================================================================
# BUCLE DE SIMULACIÓN: EJECUCIÓN DE LAS 10 RÉPLICAS INDEPENDIENTES
# =============================================================================
# Usamos una lista de 10 semillas diferentes para asegurar la independencia
semillas = [42, 105, 210, 315, 420, 525, 630, 735, 840, 945]

print("=== EJECUTANDO RÉPLICAS DE SIMULACIÓN ===")
for i, semilla in enumerate(semillas, start=1):
    # Reiniciamos generadores y listas por cada réplica
    random.seed(semilla)
    env = simpy.Environment()
    
    resources = {
        'diagnostico': simpy.Resource(env, capacity=NUM_DIAG_TECH),
        'simple': simpy.Resource(env, capacity=NUM_SIMPLE_TECH),
        'complex': simpy.Resource(env, capacity=NUM_COMPLEX_TECH)
    }
    
    # Lista local para capturar los tiempos de ciclo de esta réplica específica
    total_system_times = []
    
    # Arrancamos el proceso
    env.process(laptop_generator(env, resources, total_system_times))
    env.run(until=SIM_TIME)
    
    # Calculamos el promedio de esta réplica y lo guardamos
    promedio_replica = np.mean(total_system_times) if total_system_times else 0
    tiempos_promedio_replicas.append(promedio_replica)
    print(f"Réplica {i} (Semilla {semilla:3d}): Tiempo promedio en el sistema = {promedio_replica:.2f} min")

print("\n" + "="*60)
print("=== PARTE 3: REPORTE AUTOMÁTICO DE VALIDACIÓN ESTADÍSTICA ===")
print("="*60)

# 1. Cálculo Estadístico de las 10 réplicas
n = len(tiempos_promedio_replicas)
media_muestral = np.mean(tiempos_promedio_replicas)
# Usamos ddof=1 para obtener la desviación estándar muestral (n-1)
desviacion_estandar = np.std(tiempos_promedio_replicas, ddof=1)

print(f"Media muestral de las réplicas (X̄) : {media_muestral:.2f} minutos")
print(f"Desviación estándar muestral (s)   : {desviacion_estandar:.2f} minutos")

# 2. Construcción del Intervalo de Confianza (95% usando t-Student)
# Grados de libertad = n - 1 = 9. Valor crítico t(0.025, 9) = 2.262
t_critico = 2.262
error_estandar = desviacion_estandar / np.sqrt(n)
margen_error = t_critico * error_estandar

limite_inferior = media_muestral - margen_error
limite_superior = media_muestral + margen_error

print(f"Valor crítico t (95% conf, 9 gl)   : {t_critico}")
print(f"Intervalo de Confianza del 95%     : [{limite_inferior:.2f}, {limite_superior:.2f}] minutos")
print(f"Valor Histórico Real del Taller     : {VALOR_REAL_HISTORICO} minutos")
print("-" * 60)

# 3. Conclusión de Validación Automatizada
se_encuentra_dentro = limite_inferior <= VALOR_REAL_HISTORICO <= limite_superior

print("CONCLUSIÓN:")
if se_encuentra_dentro:
    print("✔ EL VALOR REAL SE ENCUENTRA DENTRO DEL INTERVALO DE CONFIANZA.")
    print(f"Podemos afirmar con un 95% de confianza que el simulador está VALIDADO,")
    print("ya que no existen diferencias estadísticamente significativas entre el taller real y el modelo.")
else:
    print("❌ EL VALOR REAL NO SE ENCUENTRA DENTRO DEL INTERVALO DE CONFIANZA.")
    print("El simulador NO está validado. Es necesario revisar los parámetros del modelo o calibrar las distribuciones.")
print("="*60)