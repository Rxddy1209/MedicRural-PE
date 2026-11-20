# MedicRural-PE

Sistema académico de consola desarrollado en Python para administrar el inventario de medicamentos e insumos médicos de establecimientos de salud rurales.

## Objetivo

Registrar productos, actualizar cantidades, controlar entradas y salidas, identificar stock bajo o agotado y generar reportes de inventario.

> Los datos incluidos son ficticios y se utilizan únicamente con fines académicos. Los criterios de riesgo son demostrativos y no representan una evaluación sanitaria validada.

## Requisitos

- Python 3.10 o superior
- Git
- Visual Studio Code (recomendado)

## Instalación y ejecución

1. Descarga o clona este repositorio.
2. Abre la carpeta del proyecto en Visual Studio Code.
3. (Opcional) Crea un entorno virtual:

   ```bash
   python -m venv .venv
   ```

4. Activa el entorno virtual en Windows:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

5. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

6. Ejecuta el programa:

   ```bash
   python main.py
   ```

## Funciones del sistema

1. Registrar medicamentos e insumos.
2. Consultar el inventario.
3. Modificar el stock total de un producto.
4. Registrar entradas.
5. Registrar salidas, verificando que exista cantidad suficiente.
6. Consultar productos con stock bajo o agotado.
7. Identificar productos próximos a vencer (30 días).
8. Generar un reporte general.

## Estados del stock

- **NORMAL:** stock superior al mínimo.
- **STOCK BAJO:** stock mayor que cero e igual o inferior al mínimo.
- **AGOTADO:** stock igual a cero.

## Paradigmas y conceptos aplicados

- **Orientado a objetos:** clases `Medicamento`, `Establecimiento`, `Movimiento`, `GestorInventario` y `Reporte`.
- **Funcional:** `filter()` y `map()` para consultar y transformar colecciones.
- **Estructurado:** menú, condicionales, ciclos y validaciones.
- **Patrones:** Factory para crear productos y Singleton para el gestor.
- **Persistencia:** archivo `medicamentos.json`.
- **Excepciones:** control de datos inválidos, productos inexistentes y salidas superiores al stock.

## Pruebas

Instala pytest y ejecuta:

```bash
pytest -v
```

## Estructura

```text
MedicRural-PE/
├── main.py
├── medicamentos.json
├── requirements.txt
├── README.md
├── .gitignore
├── tests/
│   └── test_inventario.py
├── docs/
│   └── diagrama_uml.png
└── evidencias/
    ├── ejecucion.png
    └── pruebas.png
```

Las carpetas `docs/` y `evidencias/` pueden completarse con el diagrama UML y capturas reales del funcionamiento.

## Alcance y limitaciones

Es un prototipo local de consola. No incluye autenticación, sincronización entre establecimientos ni conexión con proveedores. No debe utilizarse para gestionar inventarios clínicos reales sin validación, controles de seguridad y revisión del personal responsable.
