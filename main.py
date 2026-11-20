from datetime import date, datetime
import json
from pathlib import Path


ARCHIVO_DATOS = Path(__file__).with_name("medicamentos.json")


class Medicamento:
    """Representa un medicamento o insumo médico del inventario."""

    def __init__(self, codigo, nombre, stock, stock_minimo, vencimiento, tipo="Medicamento"):
        if not codigo.strip() or not nombre.strip():
            raise ValueError("El código y el nombre son obligatorios.")
        if stock < 0 or stock_minimo < 0:
            raise ValueError("Las cantidades no pueden ser negativas.")
        try:
            date.fromisoformat(vencimiento)
        except ValueError:
            raise ValueError("La fecha debe tener el formato AAAA-MM-DD.")

        self.codigo = codigo.strip().upper()
        self.nombre = nombre.strip()
        self.stock = int(stock)
        self.stock_minimo = int(stock_minimo)
        self.vencimiento = vencimiento
        self.tipo = tipo

    def actualizar_stock(self, cantidad):
        """Establece una nueva cantidad total de stock."""
        if cantidad < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.stock = int(cantidad)

    def registrar_entrada(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad de entrada debe ser mayor que cero.")
        self.stock += int(cantidad)

    def registrar_salida(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad de salida debe ser mayor que cero.")
        if cantidad > self.stock:
            raise ValueError("No hay stock suficiente para realizar la salida.")
        self.stock -= int(cantidad)

    def verificar_stock(self):
        if self.stock == 0:
            return "AGOTADO"
        if self.stock <= self.stock_minimo:
            return "STOCK BAJO"
        return "NORMAL"

    def proximo_a_vencer(self, dias=30):
        fecha_vencimiento = date.fromisoformat(self.vencimiento)
        diferencia = (fecha_vencimiento - date.today()).days
        return 0 <= diferencia <= dias

    def a_diccionario(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "stock": self.stock,
            "stock_minimo": self.stock_minimo,
            "vencimiento": self.vencimiento,
            "tipo": self.tipo
        }


class Establecimiento:
    """Representa un establecimiento rural y estima su riesgo operativo."""

    def __init__(self, nombre, accesibilidad="media", dias_reserva=7):
        self.nombre = nombre
        self.accesibilidad = accesibilidad.lower()
        self.dias_reserva = int(dias_reserva)

    def calcular_riesgo(self):
        # Criterios demostrativos; deben validarse con personal responsable.
        if self.accesibilidad == "baja" or self.dias_reserva <= 3:
            return "ALTO"
        if self.dias_reserva <= 7:
            return "MEDIO"
        return "BAJO"


class Movimiento:
    """Registra una entrada o salida de inventario."""

    def __init__(self, codigo, tipo, cantidad):
        self.codigo = codigo
        self.tipo = tipo
        self.cantidad = cantidad
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def a_diccionario(self):
        return {
            "codigo": self.codigo,
            "tipo": self.tipo,
            "cantidad": self.cantidad,
            "fecha": self.fecha
        }


class MedicamentoFactory:
    """Patrón Factory para crear recursos médicos."""

    @staticmethod
    def crear_medicamento(codigo, nombre, stock, minimo, vencimiento, tipo):
        return Medicamento(codigo, nombre, stock, minimo, vencimiento, tipo)


class GestorInventario:
    """Patrón Singleton: mantiene una instancia del gestor."""

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(self):
        if self._inicializado:
            return
        self.recursos = []
        self.movimientos = []
        self.establecimiento = Establecimiento(
            "Centro de Salud Rural Santa Rosa, Chugur, Cajamarca",
            "media",
            7
        )
        self.cargar_datos()
        self._inicializado = True

    def buscar(self, codigo):
        codigo = codigo.strip().upper()
        for recurso in self.recursos:
            if recurso.codigo == codigo:
                return recurso
        return None

    def agregar(self, recurso):
        if self.buscar(recurso.codigo):
            raise ValueError("Ya existe un producto con ese código.")
        self.recursos.append(recurso)
        self.guardar_datos()

    def actualizar(self, codigo, nueva_cantidad):
        recurso = self.buscar(codigo)
        if recurso is None:
            raise LookupError("No se encontró el producto.")
        recurso.actualizar_stock(nueva_cantidad)
        self.guardar_datos()
        return recurso

    def entrada(self, codigo, cantidad):
        recurso = self.buscar(codigo)
        if recurso is None:
            raise LookupError("No se encontró el producto.")
        recurso.registrar_entrada(cantidad)
        self.movimientos.append(Movimiento(codigo, "ENTRADA", cantidad))
        self.guardar_datos()
        return recurso

    def salida(self, codigo, cantidad):
        recurso = self.buscar(codigo)
        if recurso is None:
            raise LookupError("No se encontró el producto.")
        recurso.registrar_salida(cantidad)
        self.movimientos.append(Movimiento(codigo, "SALIDA", cantidad))
        self.guardar_datos()
        return recurso

    def listar(self):
        return self.recursos

    def guardar_datos(self):
        datos = {
            "medicamentos": [r.a_diccionario() for r in self.recursos],
            "movimientos": [m.a_diccionario() for m in self.movimientos]
        }
        ARCHIVO_DATOS.write_text(
            json.dumps(datos, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

    def cargar_datos(self):
        if not ARCHIVO_DATOS.exists():
            self.recursos = [
                MedicamentoFactory.crear_medicamento(
                    "M001", "Paracetamol", 100, 20, "2027-12-31", "Medicamento"
                ),
                MedicamentoFactory.crear_medicamento(
                    "M002", "Amoxicilina", 10, 20, "2027-06-30", "Medicamento"
                ),
                MedicamentoFactory.crear_medicamento(
                    "I001", "Guantes descartables", 0, 30, "2028-01-31", "Insumo médico"
                )
            ]
            self.movimientos = []
            self.guardar_datos()
            return

        try:
            datos = json.loads(ARCHIVO_DATOS.read_text(encoding="utf-8"))
            self.recursos = [
                MedicamentoFactory.crear_medicamento(
                    item["codigo"], item["nombre"], item["stock"],
                    item["stock_minimo"], item["vencimiento"], item.get("tipo", "Medicamento")
                )
                for item in datos.get("medicamentos", [])
            ]
            self.movimientos = []
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            raise RuntimeError(f"No se pudo cargar el inventario: {error}")


class Reporte:
    """Genera consultas y resúmenes del inventario."""

    @staticmethod
    def stock_bajo(recursos):
        return list(filter(lambda r: r.verificar_stock() == "STOCK BAJO", recursos))

    @staticmethod
    def agotados(recursos):
        return list(filter(lambda r: r.verificar_stock() == "AGOTADO", recursos))

    @staticmethod
    def proximos_a_vencer(recursos):
        return list(filter(lambda r: r.proximo_a_vencer(), recursos))

    @staticmethod
    def nombres(recursos):
        return list(map(lambda r: r.nombre, recursos))

    @staticmethod
    def mostrar(recursos):
        if not recursos:
            print("No hay productos para mostrar.")
            return
        print("\\n{:<8} {:<25} {:>8} {:>12} {:<12}".format(
            "CÓDIGO", "PRODUCTO", "STOCK", "MÍNIMO", "ESTADO"
        ))
        print("-" * 70)
        for r in recursos:
            print("{:<8} {:<25} {:>8} {:>12} {:<12}".format(
                r.codigo, r.nombre[:25], r.stock, r.stock_minimo, r.verificar_stock()
            ))

    @staticmethod
    def resumen(gestor):
        print("\\n========== REPORTE GENERAL ==========")
        print(f"Total de productos: {len(gestor.recursos)}")
        print(f"Stock bajo: {len(Reporte.stock_bajo(gestor.recursos))}")
        print(f"Agotados: {len(Reporte.agotados(gestor.recursos))}")
        print(f"Próximos a vencer (30 días): {len(Reporte.proximos_a_vencer(gestor.recursos))}")
        print(f"Riesgo del establecimiento: {gestor.establecimiento.calcular_riesgo()}")
        Reporte.mostrar(gestor.recursos)


def leer_entero(mensaje, minimo=0):
    try:
        valor = int(input(mensaje))
        if valor < minimo:
            raise ValueError
        return valor
    except ValueError:
        print(f"Error: ingrese un número entero igual o mayor que {minimo}.")
        return None


def menu():
    gestor = GestorInventario()

    while True:
        print("""
========== MEDICRURAL-PE ==========
1. Registrar medicamento o insumo
2. Ver inventario completo
3. Modificar stock total
4. Registrar entrada
5. Registrar salida
6. Ver alertas de stock
7. Ver productos próximos a vencer
8. Generar reporte general
9. Salir
""")
        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                codigo = input("Código: ").strip()
                nombre = input("Nombre: ").strip()
                stock = leer_entero("Stock inicial: ")
                if stock is None:
                    continue
                minimo = leer_entero("Stock mínimo: ")
                if minimo is None:
                    continue
                vencimiento = input("Vencimiento (AAAA-MM-DD): ").strip()
                tipo = input("Tipo (Medicamento/Insumo médico): ").strip() or "Medicamento"
                recurso = MedicamentoFactory.crear_medicamento(
                    codigo, nombre, stock, minimo, vencimiento, tipo
                )
                gestor.agregar(recurso)
                print("Producto registrado correctamente.")

            elif opcion == "2":
                Reporte.mostrar(gestor.listar())

            elif opcion == "3":
                codigo = input("Código del producto: ")
                cantidad = leer_entero("Nueva cantidad total: ")
                if cantidad is not None:
                    recurso = gestor.actualizar(codigo, cantidad)
                    print(f"Stock actualizado. Nuevo estado: {recurso.verificar_stock()}")

            elif opcion == "4":
                codigo = input("Código del producto: ")
                cantidad = leer_entero("Cantidad que ingresa: ", 1)
                if cantidad is not None:
                    recurso = gestor.entrada(codigo, cantidad)
                    print(f"Entrada registrada. Stock actual: {recurso.stock}")

            elif opcion == "5":
                codigo = input("Código del producto: ")
                cantidad = leer_entero("Cantidad que sale: ", 1)
                if cantidad is not None:
                    recurso = gestor.salida(codigo, cantidad)
                    print(f"Salida registrada. Stock actual: {recurso.stock}")

            elif opcion == "6":
                print("\\n--- PRODUCTOS CON STOCK BAJO ---")
                Reporte.mostrar(Reporte.stock_bajo(gestor.recursos))
                print("\\n--- PRODUCTOS AGOTADOS ---")
                Reporte.mostrar(Reporte.agotados(gestor.recursos))

            elif opcion == "7":
                print("\\n--- PRÓXIMOS A VENCER ---")
                Reporte.mostrar(Reporte.proximos_a_vencer(gestor.recursos))

            elif opcion == "8":
                Reporte.resumen(gestor)

            elif opcion == "9":
                print("Gracias por utilizar MedicRural-PE.")
                break

            else:
                print("Opción no válida. Intente nuevamente.")

        except (ValueError, LookupError, RuntimeError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    menu()
