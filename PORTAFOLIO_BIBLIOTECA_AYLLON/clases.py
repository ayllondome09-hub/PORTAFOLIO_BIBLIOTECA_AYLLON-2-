


from datetime import date


class Libro:

    def __init__(self, codigo, titulo, autor, estado):
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.estado = estado


class Prestamo:

    def __init__(self, numero, codigo_libro, estudiante, fecha, estado):
        self.numero = numero
        self.codigo_libro = codigo_libro
        self.estudiante = estudiante
        self.fecha = fecha
        self.estado = estado


class SistemaBiblioteca:

    ARCHIVO_LIBROS = "libros.txt"
    ARCHIVO_PRESTAMOS = "prestamos.txt"

    LIBROS_INICIALES = [
        Libro(1, "Python para todos", "Charles Severance", "Disponible"),
        Libro(2, "Aprende Java", "Ana Torres", "Disponible"),
        Libro(3, "Bases de datos", "Carlos Mora", "Disponible")
    ]

    def __init__(self):
        self.libros = self.cargar_libros()
        self.prestamos = self.cargar_prestamos()

    # ==============================
    # GUARDAR Y CARGAR LIBROS
    # ==============================

    def guardar_libros(self):
        with open(self.ARCHIVO_LIBROS, "w", encoding="utf-8") as archivo:
            for libro in self.libros:
                linea = f"{libro.codigo},{libro.titulo},"
                linea += f"{libro.autor},{libro.estado}\n"
                archivo.write(linea)

    def cargar_libros(self):
        libros = []

        try:
            with open(self.ARCHIVO_LIBROS, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    datos = linea.strip().split(",")

                    libros.append(
                        Libro(
                            int(datos[0]),
                            datos[1],
                            datos[2],
                            datos[3]
                        )
                    )

        except FileNotFoundError:
            print("No se encontró libros.txt: se usan los libros iniciales.")

            for libro in self.LIBROS_INICIALES:
                libros.append(
                    Libro(libro.codigo, libro.titulo, libro.autor, libro.estado)
                )

            self.libros = libros
            self.guardar_libros()

        return libros

    # ==============================
    # GUARDAR Y CARGAR PRESTAMOS
    # ==============================

    def guardar_prestamos(self):
        with open(self.ARCHIVO_PRESTAMOS, "w", encoding="utf-8") as archivo:
            for prestamo in self.prestamos:
                linea = f"{prestamo.numero},{prestamo.codigo_libro},"
                linea += f"{prestamo.estudiante},{prestamo.fecha},"
                linea += f"{prestamo.estado}\n"
                archivo.write(linea)

    def cargar_prestamos(self):
        prestamos = []

        try:
            with open(self.ARCHIVO_PRESTAMOS, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    datos = linea.strip().split(",")

                    prestamos.append(
                        Prestamo(
                            int(datos[0]),
                            int(datos[1]),
                            datos[2],
                            datos[3],
                            datos[4]
                        )
                    )

        except FileNotFoundError:
            print("No se encontró prestamos.txt: se inicia sin préstamos.")

            self.prestamos = prestamos
            self.guardar_prestamos()

        return prestamos

    # ==============================
    # VALIDAR DATOS
    # ==============================

    def leer_entero(self, mensaje):
        while True:
            try:
                return int(input(mensaje))
            except ValueError:
                print("Error: debe escribir un número entero.")

    def leer_texto(self, mensaje):
        while True:
            texto = input(mensaje).strip()

            if texto == "":
                print("Error: este campo no puede estar vacío.")

            elif "," in texto:
                print("Error: no use comas en este campo.")

            else:
                return texto

    # ==============================
    # BUSCAR LIBRO POR CODIGO
    # ==============================

    def buscar_por_codigo(self, codigo):
        for libro in self.libros:
            if libro.codigo == codigo:
                return libro

        return None

    # ==============================
    # REGISTRAR LIBRO
    # ==============================

    def registrar_libro(self):
        titulo = self.leer_texto("Título del libro: ")
        autor = self.leer_texto("Autor del libro: ")

        codigo_siguiente = 1

        for libro in self.libros:
            if libro.codigo >= codigo_siguiente:
                codigo_siguiente = libro.codigo + 1

        libro_nuevo = Libro(
            codigo_siguiente,
            titulo,
            autor,
            "Disponible"
        )

        self.libros.append(libro_nuevo)
        self.guardar_libros()

        print(f"Libro registrado con el código {codigo_siguiente}.")
        return libro_nuevo

    # ==============================
    # MOSTRAR LIBROS
    # ==============================

    def mostrar_libros(self):
        print(f"\n{'CÓDIGO':<8} {'TÍTULO':<30} {'AUTOR':<25} ESTADO")
        print("-" * 78)

        for libro in self.libros:
            print(f"{libro.codigo:<8} {libro.titulo:<30} "
                  f"{libro.autor:<25} {libro.estado}")

        print(f"Total de libros: {len(self.libros)}")
        return len(self.libros)

    # ==============================
    # BUSCAR LIBRO
    # ==============================

    def buscar_libro(self):
        palabra = self.leer_texto("Palabra a buscar en el título: ")
        encontrados = 0

        for libro in self.libros:
            if palabra.lower() in libro.titulo.lower():
                print(f"{libro.codigo}: {libro.titulo} - "
                      f"{libro.autor} ({libro.estado})")
                encontrados += 1

        if encontrados == 0:
            print("No se encontraron libros con esa palabra.")

        return encontrados

    # ==============================
    # PRESTAR LIBRO
    # ==============================

    def prestar_libro(self):
        codigo = self.leer_entero("Código del libro a prestar: ")
        libro = self.buscar_por_codigo(codigo)

        if libro is None:
            print("Error: no existe un libro con ese código.")
            return False

        if libro.estado == "Prestado":
            print("Error: el libro ya está prestado.")
            return False

        estudiante = self.leer_texto("Nombre del estudiante: ")

        numero_siguiente = 1

        for prestamo in self.prestamos:
            if prestamo.numero >= numero_siguiente:
                numero_siguiente = prestamo.numero + 1

        prestamo_nuevo = Prestamo(
            numero_siguiente,
            codigo,
            estudiante,
            str(date.today()),
            "Activo"
        )

        self.prestamos.append(prestamo_nuevo)
        libro.estado = "Prestado"

        self.guardar_libros()
        self.guardar_prestamos()

        print(f"Préstamo #{numero_siguiente} registrado correctamente.")
        return True

    # ==============================
    # DEVOLVER LIBRO
    # ==============================

    def devolver_libro(self):
        codigo = self.leer_entero("Código del libro a devolver: ")
        libro = self.buscar_por_codigo(codigo)

        if libro is None:
            print("Error: no existe un libro con ese código.")
            return False

        if libro.estado == "Disponible":
            print("Error: el libro no está prestado.")
            return False

        for prestamo in self.prestamos:
            if prestamo.codigo_libro == codigo and prestamo.estado == "Activo":

                libro.estado = "Disponible"
                prestamo.estado = "Devuelto"

                self.guardar_libros()
                self.guardar_prestamos()

                print("Libro devuelto correctamente.")
                return True

        return False

    # ==============================
    # MOSTRAR PRESTAMOS
    # ==============================

    def mostrar_prestamos(self):
        print(f"\n{'NÚMERO':<8} {'LIBRO':<30} {'ESTUDIANTE':<24} "
              f"{'FECHA':<12} ESTADO")
        print("-" * 92)

        for prestamo in self.prestamos:
            libro = self.buscar_por_codigo(prestamo.codigo_libro)

            if libro is not None:
                print(f"{prestamo.numero:<8} {libro.titulo:<30} "
                      f"{prestamo.estudiante:<24} {prestamo.fecha:<12} "
                      f"{prestamo.estado}")

        return len(self.prestamos)

    # ==============================
    # REPORTE GENERAL
    # ==============================

    def reporte_general(self):
        disponibles = 0
        prestados = 0
        activos = 0

        for libro in self.libros:
            if libro.estado == "Disponible":
                disponibles += 1
            else:
                prestados += 1

        for prestamo in self.prestamos:
            if prestamo.estado == "Activo":
                activos += 1

        try:
            porcentaje = prestados * 100 / len(self.libros)

        except ZeroDivisionError:
            porcentaje = 0

        print("\n========== REPORTE GENERAL ==========")
        print(f"Total de libros:          {len(self.libros)}")
        print(f"Libros disponibles:       {disponibles}")
        print(f"Libros prestados:         {prestados}")
        print(f"Préstamos registrados:    {len(self.prestamos)}")
        print(f"Préstamos activos:        {activos}")
        print(f"Porcentaje prestado:      {porcentaje:.1f}%")

        return porcentaje

    # ==============================
    # MENU PRINCIPAL
    # ==============================

    def menu(self):
        opcion = 0

        while opcion != 8:
            print("""
==================================
   BIBLIOTECA DIGITAL TEC AZUAY
==================================
1. Registrar libro      5. Devolver libro
2. Mostrar libros       6. Mostrar préstamos
3. Buscar libro         7. Reporte general
4. Prestar libro        8. Salir
""")

            opcion = self.leer_entero("Elija una opción: ")

            if opcion == 1:
                self.registrar_libro()

            elif opcion == 2:
                self.mostrar_libros()

            elif opcion == 3:
                self.buscar_libro()

            elif opcion == 4:
                self.prestar_libro()

            elif opcion == 5:
                self.devolver_libro()

            elif opcion == 6:
                self.mostrar_prestamos()

            elif opcion == 7:
                self.reporte_general()

            elif opcion == 8:
                self.guardar_libros()
                self.guardar_prestamos()
                print("Datos guardados. ¡Hasta pronto!")

            else:
                print("Opción no válida: elija un número del 1 al 8.")
