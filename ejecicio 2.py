import json

class Hotel:
    def _init_(self):
        self.habitaciones = {
            "simple": {"precio": 50, "disponibles": [101, 102, 103]},
            "doble": {"precio": 80, "disponibles": [201, 202]},
            "matrimonial": {"precio": 120, "disponibles": [301]}
        }
        self.clientes_habituales = {}
        self.reservas = {}
        self.descuento_habituales = 0.1
        self.archivo_reservas = "reservas.json"
        self.cargar_reservas()

    def guardar_reservas(self):
        with open(self.archivo_reservas, "w") as f:
            json.dump(self.reservas, f)

    def cargar_reservas(self):
        try:
            with open(self.archivo_reservas, "r") as f:
                self.reservas = json.load(f)
        except FileNotFoundError:
            self.reservas = {}

    def listar_habitaciones_disponibles(self, tipo):
        return self.habitaciones.get(tipo, {}).get("disponibles", [])

    def obtener_precio(self, tipo):
        return self.habitaciones.get(tipo, {}).get("precio", "Tipo de habitación no encontrado")

    def obtener_descuento(self):
        return self.descuento_habituales

    def calcular_precio_total(self, id_cliente, tipo, noches):
        precio = self.obtener_precio(tipo)
        if id_cliente in self.clientes_habituales:
            precio *= (1 - self.descuento_habituales)
        return precio * noches

    def reservar_habitacion(self, num_habitacion, nombre_cliente, id_cliente):
        for tipo, datos in self.habitaciones.items():
            if num_habitacion in datos["disponibles"]:
                datos["disponibles"].remove(num_habitacion)
                self.reservas[num_habitacion] = {"nombre": nombre_cliente, "id": id_cliente, "tipo": tipo}
                self.guardar_reservas()
                return f"Habitación {num_habitacion} reservada para {nombre_cliente}"
        return "Habitación no disponible"

    def eliminar_reserva(self, num_habitacion):
        if num_habitacion in self.reservas:
            tipo = self.reservas[num_habitacion]["tipo"]
            self.habitaciones[tipo]["disponibles"].append(num_habitacion)
            del self.reservas[num_habitacion]
            self.guardar_reservas()
            return f"Reserva de habitación {num_habitacion} eliminada"
        return "No existe reserva para esa habitación"

    def cambiar_precio(self, tipo, nuevo_precio):
        if tipo in self.habitaciones:
            self.habitaciones[tipo]["precio"] = nuevo_precio
            return f"Nuevo precio para {tipo}: {nuevo_precio}"
        return "Tipo de habitación no encontrado"

    def cambiar_descuento(self, nuevo_descuento):
        self.descuento_habituales = nuevo_descuento
        return f"Nuevo descuento para clientes habituales: {nuevo_descuento * 100}%"

    def calcular_ganancias(self, mes):
        ganancias = sum(self.obtener_precio(reserva["tipo"]) for reserva in self.reservas.values())
        return ganancias * 30

    def listar_habitaciones_reservadas(self):
        if not self.reservas:
            return "No hay habitaciones reservadas."
        return "\n".join([f"Habitación {num}: {datos['nombre']} (ID: {datos['id']}, Tipo: {datos['tipo']})"
                          for num, datos in self.reservas.items()])

# Programa interactivo
hotel = Hotel()
while True:
    print("\n--- Menú del Hotel ---")
    print("1. Listar habitaciones disponibles")
    print("2. Obtener precio de una habitación")
    print("3. Consultar descuento para clientes habituales")
    print("4. Calcular precio total para un cliente")
    print("5. Reservar una habitación")
    print("6. Eliminar una reserva")
    print("7. Cambiar precio de una habitación")
    print("8. Cambiar descuento para clientes habituales")
    print("9. Calcular ganancias del mes")
    print("10. Salir")
    print("11. Listar habitaciones reservadas")  # Nueva opción
    
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        tipo = input("Ingrese el tipo de habitación (simple, doble, matrimonial): ")
        print("Habitaciones disponibles:", hotel.listar_habitaciones_disponibles(tipo))
    elif opcion == "2":
        tipo = input("Ingrese el tipo de habitación: ")
        print("Precio:", hotel.obtener_precio(tipo))
    elif opcion == "3":
        print("Descuento para clientes habituales:", hotel.obtener_descuento() * 100, "%")
    elif opcion == "4":
        id_cliente = input("Ingrese el número de identificación del cliente: ")
        tipo = input("Ingrese el tipo de habitación: ")
        noches = int(input("Ingrese el número de noches: "))
        print("Precio total:", hotel.calcular_precio_total(id_cliente, tipo, noches))
    elif opcion == "5":
        num_habitacion = int(input("Ingrese el número de habitación: "))
        nombre_cliente = input("Ingrese el nombre del cliente: ")
        id_cliente = input("Ingrese el número de identificación del cliente: ")
        print(hotel.reservar_habitacion(num_habitacion, nombre_cliente, id_cliente))
    elif opcion == "6":
        num_habitacion = int(input("Ingrese el número de habitación: "))
        print(hotel.eliminar_reserva(num_habitacion))
    elif opcion == "7":
        tipo = input("Ingrese el tipo de habitación: ")
        nuevo_precio = int(input("Ingrese el nuevo precio: "))
        print(hotel.cambiar_precio(tipo, nuevo_precio))
    elif opcion == "8":
        nuevo_descuento = float(input("Ingrese el nuevo descuento (ejemplo: 0.15 para 15%): "))
        print(hotel.cambiar_descuento(nuevo_descuento))
    elif opcion == "9":
        mes = input("Ingrese el mes para calcular ganancias: ")
        print("Ganancias del mes:", hotel.calcular_ganancias(mes))
    elif opcion == "10":
        print("Saliendo del programa...")
        break
    elif opcion == "11":
        print("\n--- Habitaciones Reservadas ---")
        print(hotel.listar_habitaciones_reservadas())
    else:
        print("Opción no válida, intente de nuevo.")