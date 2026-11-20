# MedicRural-PE

### Sistema de gestión de inventario de medicamentos e insumos médicos

## 1. Introducción

MedicRural-PE es un proyecto académico desarrollado en Python que busca facilitar la gestión y el control de medicamentos e insumos médicos en establecimientos de salud rurales del Perú.

El sistema permite registrar medicamentos, consultar las cantidades disponibles, actualizar el inventario y controlar las entradas y salidas de productos. También permite identificar medicamentos con stock bajo y próximos a vencer.

El proyecto aplica diferentes conceptos de programación, como la programación orientada a objetos, programación estructurada y programación funcional. Además, utiliza archivos JSON para almacenar la información del inventario.

## 2. Objetivo general

Desarrollar un sistema que permita gestionar el inventario de medicamentos e insumos médicos, facilitando el control de existencias y la identificación de posibles situaciones de desabastecimiento en establecimientos de salud rurales.

## 3. Objetivos específicos

- Registrar medicamentos e insumos médicos.
- Consultar los productos disponibles.
- Actualizar las cantidades del inventario.
- Registrar entradas y salidas de productos.
- Identificar medicamentos con stock bajo.
- Detectar medicamentos próximos a vencer.
- Generar reportes del inventario.

## 4. Funcionalidades principales

- Registro de medicamentos.
- Consulta del inventario.
- Actualización de existencias.
- Registro de entradas y salidas.
- Identificación de productos agotados o con stock bajo.
- Detección de medicamentos próximos a vencer.
- Generación de reportes generales.

## 5. Tecnologías utilizadas

- Python 3.x
- JSON para el almacenamiento de información.
- Visual Studio Code como entorno de desarrollo.
- Git y GitHub para el control de versiones.
- pytest para las pruebas automatizadas.

## 6. Estructura del proyecto

```text
MedicRural-PE/
│
├── main.py
├── medicamentos.json
├── requirements.txt
├── README.md
├── .gitignore
│
├── docs/
│   ├── diagrama_uml.png
│
└── evidencias/
    ├── ejecucion.png
    └── pruebas.png
```

## 7. Instalación y ejecución

### Requisitos previos

- Tener instalado Python 3.x.
- Contar con Visual Studio Code.
- Tener instalado pytest.

### Instalar pytest

```bash
python -m pip install pytest
```

### Ejecutar el programa

```bash
python main.py
```

### Ejecutar las pruebas automatizadas

```bash
python -m pytest -v
```

## 8. Conceptos de programación aplicados

### Programación orientada a objetos

Se utilizan clases y objetos para representar los medicamentos, establecimientos, movimientos y la gestión del inventario.

### Programación estructurada

Se emplean funciones, condicionales y estructuras repetitivas para organizar el funcionamiento del sistema.

### Programación funcional

Se utilizan funciones como `filter()` y `map()` para procesar y consultar información del inventario.

### Manejo de excepciones

Se realizan validaciones para evitar operaciones incorrectas, como registrar cantidades negativas o retirar más productos de los disponibles.

## 9. Pruebas automatizadas

El proyecto utiliza pytest para comprobar el funcionamiento de diferentes operaciones del inventario, como la creación de medicamentos, actualización del stock, registro de entradas y salidas y detección de stock bajo.

Las pruebas se encuentran en la carpeta `tests`.

## 10. Alcance del proyecto

MedicRural-PE es un prototipo académico que funciona mediante una interfaz de consola. Su finalidad es demostrar la aplicación de conceptos de programación en la gestión de inventarios de establecimientos de salud rurales.

El sistema utiliza datos de ejemplo y no está conectado a una plataforma médica real.

## 11. Integrantes del equipo

- Mateo Oroche
- Leonel Morales
- Ruddy Raraz
- Valentino Pomalaya

## 12. Proyecto académico

Desarrollado como parte de las actividades académicas de Ingeniería de Sistemas.
