import random
import statistics

# --- CONFIGURACIÓN DE LA RED ---
ciudades = ["Querétaro", "Celaya", "Silao"]
tasa_pedidos_h = 12   # Media de pedidos/hora (Poisson)
tiempo_base_viaje = 45  # Media de 45 min (Normal)
desv_estandar = 10     # Desviación de 10 min

def simular_jornada(horas):
    total_pedidos = []
    tiempos_totales = []
    retrasos = 0
    
    print(f"--- Iniciando Simulación de {horas} hrs ---")
    
    for h in range(1, horas + 1):
        # 1. VARIABLE DISCRETA: Pedidos recibidos
        n_pedidos = 0
        t = 0
        while True:
            t += random.expovariate(tasa_pedidos_h)
            if t > 1: 
                break
            n_pedidos += 1
        
        total_pedidos.append(n_pedidos)
        
        # 2. VARIABLE CONTINUA: Tiempo de entrega para cada pedido
        for i in range(n_pedidos):
            tiempo_viaje = random.gauss(tiempo_base_viaje, desv_estandar)
            tiempos_totales.append(tiempo_viaje)
            
            # --- NUEVA CONDICIÓN ---
            if tiempo_viaje > 60:
                retrasos += 1
                print(f"⚠️ Retraso en Red por Tráfico (tiempo: {round(tiempo_viaje, 2)} min)")
            
        print(f"Hora {h}: {n_pedidos} pedidos recibidos.")

    return total_pedidos, tiempos_totales, retrasos

# Ejecución
pedidos, tiempos, retrasos = simular_jornada(12)

# --- RESULTADOS ---
print("\n--- REPORTE FINAL ---")
print(f"Total pedidos en el día: {sum(pedidos)}")
print(f"Promedio de pedidos/hora: {statistics.mean(pedidos):.2f}")
print(f"Tiempo promedio de entrega: {statistics.mean(tiempos):.2f} min")
print(f"Tiempo total acumulado de operación: {sum(tiempos):.2f} min (≈ {sum(tiempos)/60:.2f} horas)")
print(f"Pedidos con retraso (>60 min): {retrasos}")
