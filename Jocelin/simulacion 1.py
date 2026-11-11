import simpy
import random

# --- CONFIGURACIÓN BASE ---
SEMILLA = 42
TIEMPO_PROCESAMIENTO = 5   # Tiempo promedio (segundos) que toma un Check-in
TIEMPO_SIMULACION = 60     # Tiempo límite del experimento

def proceso_registro_hotel(env, nombre, servidor_cloud, tiempos_espera, contadores):
    tiempo_llegada = env.now
    
    with servidor_cloud.request() as peticion:
        # El cliente abandona si el servidor tarda más de 8 segundos en responder (Timeout)
        resultado = yield peticion | env.timeout(8)
        
        if peticion in resultado:
            tiempo_espera = env.now - tiempo_llegada
            tiempos_espera.append(tiempo_espera)
            
            # Simular tiempo de ejecución real (pago, base de datos)
            tiempo_ejecucion = random.normalvariate(TIEMPO_PROCESAMIENTO, 1)
            yield env.timeout(max(0.5, tiempo_ejecucion))
            
            contadores['atendidos'] += 1
        else:
            contadores['rechazados'] += 1

def generador_huespedes(env, intervalo_llegada, servidor_cloud, tiempos_espera, contadores):
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / intervalo_llegada))
        i += 1
        env.process(proceso_registro_hotel(env, f"Huésped-{i}", servidor_cloud, tiempos_espera, contadores))

def correr_simulacion(servidores, intervalo):
    """Función que encapsula la simulación para poder reutilizarla por escenario"""
    random.seed(SEMILLA)
    env = simpy.Environment()
    servidor_cloud = simpy.Resource(env, capacity=servidores)
    
    # Estructuras para guardar métricas por simulación
    tiempos_espera = []
    contadores = {'atendidos': 0, 'rechazados': 0}
    
    env.process(generador_huespedes(env, intervalo, servidor_cloud, tiempos_espera, contadores))
    env.run(until=TIEMPO_SIMULACION)
    
    promedio_espera = sum(tiempos_espera) / len(tiempos_espera) if tiempos_espera else 0
    return contadores['atendidos'], contadores['rechazados'], promedio_espera

# --- FASE DE EXPERIMENTACIÓN ---

# Escenario A: Infraestructura Austera
atendidos_A, rechazados_A, espera_A = correr_simulacion(servidores=1, intervalo=2)

# Escenario B: Temporada Alta (Pico)
atendidos_B, rechazados_B, espera_B = correr_simulacion(servidores=3, intervalo=0.5)

# Escenario C: Auto-escalado Óptimo 
# Buscaremos el número mínimo de servidores para que rechazados sea 0 bajo demanda de Temporada Alta (intervalo = 0.5)
servidores_C = 3
while True:
    atendidos_C, rechazados_C, espera_C = correr_simulacion(servidores=servidores_C, intervalo=0.5)
    if rechazados_C == 0:
        break
    servidores_C += 1

# --- REPORTE DE RESULTADOS ---
print("=" * 80)
print(f"{'ESCENARIO':<30} | {'SERVIDORES':<10} | {'ATENDIDOS':<10} | {'RECHAZADOS':<10} | {'ESPERA PROM.':<12}")
print("=" * 80)
print(f"{'A: Infraestructura Austera':<30} | {1:<10} | {atendidos_A:<10} | {rechazados_A:<10} | {espera_A:.2f}s")
print(f"{'B: Temporada Alta (Pico)':<30} | {3:<10} | {atendidos_B:<10} | {rechazados_B:<10} | {espera_B:.2f}s")
print(f"{'C: Auto-escalado Óptimo':<30} | {servidores_C:<10} | {atendidos_C:<10} | {rechazados_C:<10} | {espera_C:.2f}s")
print("=" * 80)