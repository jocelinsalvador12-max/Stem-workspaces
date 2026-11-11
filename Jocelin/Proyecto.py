import simpy
import random
import psycopg2

# =========================
# CONFIGURACIÓN
# =========================

APACHE_CAPACITY = 150
POSTGRES_CAPACITY = 100

ESTUDIANTES = 1000
PROFESORES = 200

SIMULATION_TIME = 7200
TIMEOUT = 15

# =========================
# MÉTRICAS
# =========================

exitosas = 0
caidas = 0
esperas = []

max_apache = 0
max_postgres = 0


def usuario(env, tipo, apache, postgres):
    global exitosas, caidas
    global max_apache, max_postgres

    llegada = env.now

    try:
        # Solicita Apache
        with apache.request() as req_apache:

            resultado = yield req_apache | env.timeout(TIMEOUT)

            if req_apache not in resultado:
                caidas += 1
                return

            max_apache = max(max_apache, apache.count)

            # Solicita PostgreSQL
            with postgres.request() as req_postgres:

                resultado_db = yield req_postgres | env.timeout(TIMEOUT)

                if req_postgres not in resultado_db:
                    caidas += 1
                    return

                max_postgres = max(max_postgres, postgres.count)

                espera = env.now - llegada
                esperas.append(espera)

                # Tiempo de procesamiento
                if tipo == "estudiante":
                    tiempo = random.expovariate(1 / 0.5)
                else:
                    tiempo = max(0.1, random.normalvariate(1.5, 0.4))

                yield env.timeout(tiempo)

                exitosas += 1

    except Exception as e:
        print("Error:", e)
        caidas += 1


def generar_estudiantes(env, apache, postgres):

    for _ in range(ESTUDIANTES):

        llegada = random.uniform(0, SIMULATION_TIME)

        yield env.timeout(llegada / ESTUDIANTES)

        env.process(
            usuario(env, "estudiante", apache, postgres)
        )


def generar_profesores(env, apache, postgres):

    for _ in range(PROFESORES):

        llegada = random.uniform(0, SIMULATION_TIME)

        yield env.timeout(llegada / PROFESORES)

        env.process(
            usuario(env, "profesor", apache, postgres)
        )


# =========================
# INICIAR SIMULACIÓN
# =========================

env = simpy.Environment()

apache = simpy.Resource(
    env,
    capacity=APACHE_CAPACITY
)

postgres = simpy.Resource(
    env,
    capacity=POSTGRES_CAPACITY
)

env.process(
    generar_estudiantes(
        env,
        apache,
        postgres
    )
)

env.process(
    generar_profesores(
        env,
        apache,
        postgres
    )
)

env.run(until=SIMULATION_TIME)

# =========================
# RESULTADOS
# =========================

promedio_espera = 0

if len(esperas) > 0:
    promedio_espera = sum(esperas) / len(esperas)

total = exitosas + caidas

if total > 0:
    porcentaje_caidas = (caidas / total) * 100
else:
    porcentaje_caidas = 0

if porcentaje_caidas > 5:
    resultado = "NO FACTIBLE"
elif porcentaje_caidas > 2:
    resultado = "RIESGO ALTO"
else:
    resultado = "FACTIBLE"

print("\n===== RESULTADOS =====")
print("Exitosas:", exitosas)
print("Caídas:", caidas)
print("Espera Promedio:", round(promedio_espera, 2))
print("Máximo Apache:", max_apache)
print("Máximo PostgreSQL:", max_postgres)
print("Resultado:", resultado)

# =========================
# GUARDAR EN POSTGRESQL
# =========================

try:

    conexion = psycopg2.connect(
        host="localhost",
        database="moodle_sim",
        user="postgres",
        password="TU_PASSWORD"
    )

    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO reporte_factibilidad_moodle(
        total_peticiones_exitosas,
        total_peticiones_caidas,
        tiempo_espera_promedio_seg,
        max_uso_apache,
        max_uso_postgres,
        resultado_factibilidad
    )
    VALUES (%s,%s,%s,%s,%s,%s)
    """,
    (
        exitosas,
        caidas,
        round(promedio_espera, 2),
        max_apache,
        max_postgres,
        resultado
    ))

    conexion.commit()

    cursor.close()
    conexion.close()

    print("Resultados guardados en PostgreSQL")

except Exception as e:

    print("Error PostgreSQL:")
    print(e)