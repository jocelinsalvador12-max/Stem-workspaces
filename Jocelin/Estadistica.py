import simpy
import random
import numpy as np

# Configuración de parámetros
RANDOM_SEED = 42
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

# Listas para recolectar métricas
waiting_times_diag = []
repaired_count = 0
total_diag_time = 0.0
total_simple_time = 0.0
total_complex_time = 0.0

def laptop_process(env, name, resources):
    global repaired_count, total_diag_time, total_simple_time, total_complex_time
    
    # 1. Arribo al sistema
    arrival_time = env.now
    
    # 2. Fase de Diagnóstico
    with resources['diagnostico'].request() as req:
        yield req
        start_diag = env.now
        wait_diag = start_diag - arrival_time
        waiting_times_diag.append(wait_diag)
        
        # Tiempo de servicio diagnóstico
        diag_duration = random.uniform(DIAG_MIN, DIAG_MAX)
        yield env.timeout(diag_duration)
        total_diag_time += diag_duration

    # 3. Clasificación
    prob = random.random()
    if prob <= 0.70:
        # 4a. Línea Simple
        with resources['simple'].request() as req:
            yield req
            simple_duration = random.expovariate(1.0 / SIMPLE_MEAN)
            yield env.timeout(simple_duration)
            total_simple_time += simple_duration
    else:
        # 4b. Línea Compleja
        with resources['complex'].request() as req:
            yield req
            complex_duration = random.normalvariate(COMPLEX_MEAN, COMPLEX_STD)
            yield env.timeout(complex_duration)
            total_complex_time += complex_duration
            
    # 5. Salida
    repaired_count += 1

def laptop_generator(env, resources):
    laptop_id = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / ARRIVALS_MEAN))
        laptop_id += 1
        env.process(laptop_process(env, f'Laptop_{laptop_id}', resources))

# Inicialización del entorno
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Recursos
resources = {
    'diagnostico': simpy.Resource(env, capacity=NUM_DIAG_TECH),
    'simple': simpy.Resource(env, capacity=NUM_SIMPLE_TECH),
    'complex': simpy.Resource(env, capacity=NUM_COMPLEX_TECH)
}

# Ejecución
env.process(laptop_generator(env, resources))
env.run(until=SIM_TIME)

# C) Reporte de Métricas del Sistema
avg_wait_diag = np.mean(waiting_times_diag) if waiting_times_diag else 0
util_diag = (total_diag_time / SIM_TIME) * 100
util_simple = (total_simple_time / SIM_TIME) * 100
util_complex = (total_complex_time / SIM_TIME) * 100

print("=== REPORTE DE MÉTRICAS DEL SISTEMA (40 HORAS) ===")
print(f"Tiempo promedio de espera en cola de diagnóstico: {avg_wait_diag:.2f} minutos")
print(f"Utilización del Técnico de Diagnóstico: {util_diag:.2f}%")
print(f"Utilización del Técnico de Línea Simple: {util_simple:.2f}%")
print(f"Utilización del Especialista Complejo: {util_complex:.2f}%")
print(f"Número total de laptops reparadas con éxito: {repaired_count}")