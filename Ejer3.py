class Material:
    def __init__(self, id, titulo, autor, año_publicacion):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.año_publicacion = año_publicacion
        self.prestado = False

    def prestar(self):
        if not self.prestado:
            self.prestado = True
            print(f"{self.titulo} ha sido prestado.")
        else:
            print(f"{self.titulo} ya está prestado.")

    def devolver(self):
        if self.prestado:
            self.prestado = False
            print(f"{self.titulo} ha sido devuelto.")
        else:
            print(f"{self.titulo} no está prestado.")

class Libro(Material):
    def __init__(self, id, titulo, autor, año_publicacion, isbn, genero):
        super().__init__(id, titulo, autor, año_publicacion)
        self.isbn = isbn
        self.genero = genero

class Revista(Material):
    def __init__(self, id, titulo, autor, año_publicacion, frecuencia):
        super().__init__(id, titulo, autor, año_publicacion)
        self.frecuencia = frecuencia

class DVD(Material):
    def __init__(self, id, titulo, autor, año_publicacion, duracion, director):
        super().__init__(id, titulo, autor, año_publicacion)
        self.duracion = duracion
        self.director = director

# Ejemplo de uso
if __name__ == "__main__":
    libro1 = Libro(1, "Cien años de soledad", "Gabriel García Márquez", 1967, "978-3-16-148410-0", "Ficción")
    revista1 = Revista(2, "National Geographic", "Varios", 2023, "Mensual")
    dvd1 = DVD(3, "Inception", "Christopher Nolan", 2010, 148, "Christopher Nolan")

    # Préstamos
    libro1.prestar()
    revista1.prestar()
    dvd1.prestar()

    # Devoluciones
    libro1.devolver()
    revista1.devolver()
    dvd1.devolver()

    # Intentar prestar de nuevo
    libro1.prestar()
    libro1.prestar()  # Intentar prestar de nuevo