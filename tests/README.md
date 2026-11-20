[test_inventario.py](https://github.com/user-attachments/files/35127726/test_inventario.py)
import pytest
from main import Medicamento, GestorInventario, Reporte


def test_crear_medicamento():
    producto = Medicamento("M100", "Paracetamol", 50, 10, "2027-12-31")
    assert producto.nombre == "Paracetamol"
    assert producto.stock == 50


def test_actualizar_stock():
    producto = Medicamento("M101", "Ibuprofeno", 20, 10, "2027-12-31")
    producto.actualizar_stock(8)
    assert producto.stock == 8
    assert producto.verificar_stock() == "STOCK BAJO"


def test_no_permitir_stock_negativo():
    producto = Medicamento("M102", "Alcohol", 20, 5, "2027-12-31")
    with pytest.raises(ValueError):
        producto.actualizar_stock(-1)


def test_entrada_y_salida():
    producto = Medicamento("M103", "Gasas", 10, 3, "2027-12-31")
    producto.registrar_entrada(5)
    producto.registrar_salida(4)
    assert producto.stock == 11


def test_no_permitir_salida_mayor_al_stock():
    producto = Medicamento("M104", "Guantes", 2, 1, "2027-12-31")
    with pytest.raises(ValueError):
        producto.registrar_salida(3)


def test_detectar_stock_bajo():
    producto = Medicamento("M105", "Amoxicilina", 5, 10, "2027-12-31")
    assert producto.verificar_stock() == "STOCK BAJO"


def test_filter_stock_bajo():
    productos = [
        Medicamento("M106", "A", 50, 10, "2027-12-31"),
        Medicamento("M107", "B", 5, 10, "2027-12-31")
    ]
    assert [p.nombre for p in Reporte.stock_bajo(productos)] == ["B"]
