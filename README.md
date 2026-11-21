# MedicRural-PE

### Sistema de gestión de inventario de medicamentos e insumos médicos

## 1. Introducción

MedicRural-PE es un proyecto académico desarrollado en Java que busca facilitar la gestión y el control de medicamentos e insumos médicos en establecimientos de salud rurales del Perú.

El sistema permite registrar medicamentos, consultar las cantidades disponibles, actualizar el inventario y controlar las entradas y salidas de productos. También permite identificar medicamentos con stock bajo y próximos a vencer.

El proyecto aplica diferentes conceptos de programación, como la programación orientada a objetos, programación estructurada y programación funcional. Además, utiliza archivos JSON mediante la biblioteca Gson para almacenar la información del inventario.

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

- Registro de medicamentos e insumos médicos.
- Consulta del inventario.
- Actualización de existencias.
- Registro de entradas y salidas.
- Identificación de productos agotados o con stock bajo.
- Detección de medicamentos próximos a vencer.
- Generación de reportes generales.

## 5. Tecnologías utilizadas

- **Java 17:** lenguaje de programación utilizado para desarrollar el sistema.
- **Apache NetBeans:** entorno de desarrollo utilizado para escribir y ejecutar el código.
- **Apache Maven:** herramienta para gestionar el proyecto y sus dependencias.
- **Gson:** biblioteca utilizada para leer y guardar información en archivos JSON.
- **JSON:** formato utilizado para almacenar los datos del inventario.
- **Git:** herramienta para el control de versiones.
- **GitHub:** plataforma utilizada para almacenar y compartir el proyecto.

## 6. Estructura del proyecto

```text
MedicRural-PE/
│
├── src/
│   ├── main/
│   │   └── java/
│   │       └── MedicRuralPE.java
│   │
│   └── test/
│       └── java/
│           └── MedicRuralPETest.java
│
├── documentos/
│   └── diagrama_uml.png
│
├── evidencias/
│   ├── ejecucion.png
│   └── pruebas.png
│
├── medicamentos.json
├── pom.xml
├── README.md
└── .gitignore
```

**Nota:** La estructura muestra la organización prevista del proyecto. Los archivos de pruebas se incorporarán cuando se implemente la configuración de JUnit.

## 7. Instalación y ejecución

### Requisitos previos

- Tener instalado Java JDK 17 o superior.
- Contar con Apache NetBeans.
- Tener instalado Apache Maven.
- Disponer de conexión a Internet para descargar las dependencias iniciales del proyecto.

### Configuración de dependencias

El proyecto utiliza Maven para administrar sus dependencias. La biblioteca Gson se configura en el archivo `pom.xml`.

### Ejecutar el programa

1. Abrir Apache NetBeans.
2. Seleccionar File → Open Project.
3. Buscar la carpeta del proyecto MedicRural-PE.
4. Esperar a que Maven cargue las dependencias.
5. Ejecutar el archivo `MedicRuralPE.java`.

El programa mostrará un menú en la consola desde el cual se podrán utilizar las diferentes funcionalidades del inventario.

### Ejecutar desde la terminal

Para compilar el proyecto:

```bash
mvn clean compile
```

Para ejecutar las pruebas automatizadas, una vez configurado JUnit:

```bash
mvn test
```

## 8. Conceptos de programación aplicados

### Programación orientada a objetos

Se utilizan clases y objetos para representar los medicamentos, establecimientos, movimientos y la gestión del inventario. También se aplican patrones de diseño como Singleton y Factory.

### Programación estructurada

Se emplean métodos, condicionales y estructuras repetitivas para organizar el funcionamiento del sistema y controlar las operaciones del inventario.

### Programación funcional

Se utilizan herramientas de Java como Stream API, `filter()` y `map()` para procesar colecciones de medicamentos, identificar productos con stock bajo y obtener información específica.

### Manejo de excepciones

Se utilizan mecanismos como `try`, `catch` y validaciones para evitar operaciones incorrectas, como registrar cantidades negativas o retirar más productos de los disponibles.

## 9. Pruebas automatizadas

El proyecto contempla la implementación de pruebas automatizadas en Java para comprobar el funcionamiento de las diferentes operaciones del inventario.

Se utilizará JUnit para verificar aspectos como:

- Creación de medicamentos.
- Actualización del stock.
- Registro de entradas y salidas.
- Detección de productos con stock bajo.
- Validación de cantidades.
- Consulta de medicamentos próximos a vencer.

Las pruebas se organizarán en la carpeta `src/test/java`.

## 10. Alcance del proyecto

MedicRural-PE es un prototipo académico que funciona mediante una interfaz de consola. Su finalidad es demostrar la aplicación de conceptos de programación en la gestión de inventarios de establecimientos de salud rurales.

El sistema utiliza datos de ejemplo y no está conectado a una plataforma médica real.

## 11. Integrantes del equipo

- Mateo Oroche
- Leonel Morales
- Ruddy Raraz
- Valentino Pomalaya

## 12. Proyecto académico

Desarrollado como parte de las actividades académicas del curso de Lenguaje de Programación de Ingeniería de Sistemas.
