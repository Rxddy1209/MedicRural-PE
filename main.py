import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Collectors;

// MedicRural-PE: sistema de gestión de inventario médico.
public class MedicRuralPE {

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        menu();
    }

    // Representa un medicamento o insumo médico del inventario.
    static class Medicamento {
        private String codigo;
        private String nombre;
        private int stock;
        private int stockMinimo;
        private String vencimiento;
        private String tipo;

        public Medicamento(String codigo, String nombre, int stock,
                           int stockMinimo, String vencimiento, String tipo) {
            if (codigo == null || codigo.trim().isEmpty()
                    || nombre == null || nombre.trim().isEmpty()) {
                throw new IllegalArgumentException("El código y el nombre son obligatorios.");
            }
            if (stock < 0 || stockMinimo < 0) {
                throw new IllegalArgumentException("Las cantidades no pueden ser negativas.");
            }

            try {
                LocalDate.parse(vencimiento);
            } catch (DateTimeParseException e) {
                throw new IllegalArgumentException("La fecha debe tener el formato AAAA-MM-DD.");
            }

            this.codigo = codigo.trim().toUpperCase();
            this.nombre = nombre.trim();
            this.stock = stock;
            this.stockMinimo = stockMinimo;
            this.vencimiento = vencimiento;
            this.tipo = (tipo == null || tipo.trim().isEmpty()) ? "Medicamento" : tipo;
        }

        // Establece una nueva cantidad total de stock.
        public void actualizarStock(int cantidad) {
            if (cantidad < 0) {
                throw new IllegalArgumentException("El stock no puede ser negativo.");
            }
            this.stock = cantidad;
        }

        public void registrarEntrada(int cantidad) {
            if (cantidad <= 0) {
                throw new IllegalArgumentException("La cantidad de entrada debe ser mayor que cero.");
            }
            this.stock += cantidad;
        }

        public void registrarSalida(int cantidad) {
            if (cantidad <= 0) {
                throw new IllegalArgumentException("La cantidad de salida debe ser mayor que cero.");
            }
            if (cantidad > stock) {
                throw new IllegalArgumentException("No hay stock suficiente para realizar la salida.");
            }
            this.stock -= cantidad;
        }

        public String verificarStock() {
            if (stock == 0) {
                return "AGOTADO";
            }
            if (stock <= stockMinimo) {
                return "STOCK BAJO";
            }
            return "NORMAL";
        }

        public boolean proximoAVencer() {
            LocalDate fechaVencimiento = LocalDate.parse(vencimiento);
            // ChronoUnit.DAYS calcula correctamente la diferencia entre fechas.
            long diferencia = java.time.temporal.ChronoUnit.DAYS.between(LocalDate.now(), fechaVencimiento);
            return diferencia >= 0 && diferencia <= 30;
        }

        public JsonObject aJson() {
            JsonObject objeto = new JsonObject();
            objeto.addProperty("codigo", codigo);
            objeto.addProperty("nombre", nombre);
            objeto.addProperty("stock", stock);
            objeto.addProperty("stock_minimo", stockMinimo);
            objeto.addProperty("vencimiento", vencimiento);
            objeto.addProperty("tipo", tipo);
            return objeto;
        }
    }

    // Representa un establecimiento rural y estima su riesgo operativo.
    static class Establecimiento {
        private String nombre;
        private String accesibilidad;
        private int diasReserva;

        public Establecimiento(String nombre, String accesibilidad, int diasReserva) {
            this.nombre = nombre;
            this.accesibilidad = accesibilidad.toLowerCase();
            this.diasReserva = diasReserva;
        }

        public String calcularRiesgo() {
            // Criterios demostrativos; deben validarse con personal responsable.
            if (accesibilidad.equals("baja") || diasReserva <= 3) {
                return "ALTO";
            }
            if (diasReserva <= 7) {
                return "MEDIO";
            }
            return "BAJO";
        }
    }

    // Registra una entrada o salida de inventario.
    static class Movimiento {
        private String codigo;
        private String tipo;
        private int cantidad;
        private String fecha;

        public Movimiento(String codigo, String tipo, int cantidad) {
            this.codigo = codigo;
            this.tipo = tipo;
            this.cantidad = cantidad;
            this.fecha = LocalDateTime.now().format(
                    DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
        }

        public JsonObject aJson() {
            JsonObject objeto = new JsonObject();
            objeto.addProperty("codigo", codigo);
            objeto.addProperty("tipo", tipo);
            objeto.addProperty("cantidad", cantidad);
            objeto.addProperty("fecha", fecha);
            return objeto;
        }
    }

    // Patrón Factory para crear recursos médicos.
    static class MedicamentoFactory {
        public static Medicamento crearMedicamento(String codigo, String nombre,
                                                    int stock, int minimo,
                                                    String vencimiento, String tipo) {
            return new Medicamento(codigo, nombre, stock, minimo, vencimiento, tipo);
        }
    }

    // Patrón Singleton: mantiene una única instancia del gestor.
    static class GestorInventario {
        private static GestorInventario instancia;
        private final List<Medicamento> recursos;
        private final List<Movimiento> movimientos;
        private final Establecimiento establecimiento;
        private final Path archivoDatos = Path.of("medicamentos.json");
        private final Gson gson = new GsonBuilder().setPrettyPrinting().create();

        private GestorInventario() {
            recursos = new ArrayList<>();
            movimientos = new ArrayList<>();
            establecimiento = new Establecimiento(
                    "Centro de Salud Rural Santa Rosa, Chugur, Cajamarca",
                    "media", 7);
            cargarDatos();
        }

        public static synchronized GestorInventario obtenerInstancia() {
            if (instancia == null) {
                instancia = new GestorInventario();
            }
            return instancia;
        }

        public Medicamento buscar(String codigo) {
            String codigoNormalizado = codigo.trim().toUpperCase();
            for (Medicamento recurso : recursos) {
                if (recurso.codigo.equals(codigoNormalizado)) {
                    return recurso;
                }
            }
            return null;
        }

        public void agregar(Medicamento recurso) {
            if (buscar(recurso.codigo) != null) {
                throw new IllegalArgumentException("Ya existe un producto con ese código.");
            }
            recursos.add(recurso);
            guardarDatos();
        }

        public Medicamento actualizar(String codigo, int nuevaCantidad) {
            Medicamento recurso = buscar(codigo);
            if (recurso == null) {
                throw new IllegalArgumentException("No se encontró el producto.");
            }
            recurso.actualizarStock(nuevaCantidad);
            guardarDatos();
            return recurso;
        }

        public Medicamento entrada(String codigo, int cantidad) {
            Medicamento recurso = buscar(codigo);
            if (recurso == null) {
                throw new IllegalArgumentException("No se encontró el producto.");
            }
            recurso.registrarEntrada(cantidad);
            movimientos.add(new Movimiento(codigo, "ENTRADA", cantidad));
            guardarDatos();
            return recurso;
        }

        public Medicamento salida(String codigo, int cantidad) {
            Medicamento recurso = buscar(codigo);
            if (recurso == null) {
                throw new IllegalArgumentException("No se encontró el producto.");
            }
            recurso.registrarSalida(cantidad);
            movimientos.add(new Movimiento(codigo, "SALIDA", cantidad));
            guardarDatos();
            return recurso;
        }

        public List<Medicamento> listar() {
            return recursos;
        }

        public List<Movimiento> getMovimientos() {
            return movimientos;
        }

        public Establecimiento getEstablecimiento() {
            return establecimiento;
        }

        public void guardarDatos() {
            JsonObject datos = new JsonObject();
            JsonArray medicamentosJson = new JsonArray();
            for (Medicamento recurso : recursos) {
                medicamentosJson.add(recurso.aJson());
            }

            JsonArray movimientosJson = new JsonArray();
            for (Movimiento movimiento : movimientos) {
                movimientosJson.add(movimiento.aJson());
            }

            datos.add("medicamentos", medicamentosJson);
            datos.add("movimientos", movimientosJson);

            try {
                Files.writeString(archivoDatos, gson.toJson(datos));
            } catch (IOException e) {
                throw new RuntimeException("No se pudieron guardar los datos: " + e.getMessage());
            }
        }

        public void cargarDatos() {
            if (!Files.exists(archivoDatos)) {
                recursos.add(MedicamentoFactory.crearMedicamento(
                        "M001", "Paracetamol", 100, 20, "2027-12-31", "Medicamento"));
                recursos.add(MedicamentoFactory.crearMedicamento(
                        "M002", "Amoxicilina", 10, 20, "2027-06-30", "Medicamento"));
                recursos.add(MedicamentoFactory.crearMedicamento(
                        "I001", "Guantes descartables", 0, 30, "2028-01-31", "Insumo médico"));
                guardarDatos();
                return;
            }

            try {
                String contenido = Files.readString(archivoDatos);
                JsonObject datos = JsonParser.parseString(contenido).getAsJsonObject();

                JsonArray medicamentosJson = datos.getAsJsonArray("medicamentos");
                if (medicamentosJson != null) {
                    for (int i = 0; i < medicamentosJson.size(); i++) {
                        JsonObject item = medicamentosJson.get(i).getAsJsonObject();
                        String tipo = item.has("tipo")
                                ? item.get("tipo").getAsString() : "Medicamento";

                        recursos.add(MedicamentoFactory.crearMedicamento(
                                item.get("codigo").getAsString(),
                                item.get("nombre").getAsString(),
                                item.get("stock").getAsInt(),
                                item.get("stock_minimo").getAsInt(),
                                item.get("vencimiento").getAsString(),
                                tipo));
                    }
                }

                JsonArray movimientosJson = datos.getAsJsonArray("movimientos");
                if (movimientosJson != null) {
                    for (int i = 0; i < movimientosJson.size(); i++) {
                        JsonObject item = movimientosJson.get(i).getAsJsonObject();
                        Movimiento movimiento = new Movimiento(
                                item.get("codigo").getAsString(),
                                item.get("tipo").getAsString(),
                                item.get("cantidad").getAsInt());
                        movimiento.fecha = item.get("fecha").getAsString();
                        movimientos.add(movimiento);
                    }
                }
            } catch (Exception e) {
                throw new RuntimeException("No se pudo cargar el inventario: " + e.getMessage());
            }
        }
    }

    // Genera consultas y resúmenes del inventario.
    static class Reporte {
        public static List<Medicamento> stockBajo(List<Medicamento> recursos) {
            return recursos.stream()
                    .filter(r -> r.verificarStock().equals("STOCK BAJO"))
                    .collect(Collectors.toList());
        }

        public static List<Medicamento> agotados(List<Medicamento> recursos) {
            return recursos.stream()
                    .filter(r -> r.verificarStock().equals("AGOTADO"))
                    .collect(Collectors.toList());
        }

        public static List<Medicamento> proximosAVencer(List<Medicamento> recursos) {
            return recursos.stream()
                    .filter(Medicamento::proximoAVencer)
                    .collect(Collectors.toList());
        }

        public static List<String> nombres(List<Medicamento> recursos) {
            return recursos.stream()
                    .map(r -> r.nombre)
                    .collect(Collectors.toList());
        }

        public static void mostrar(List<Medicamento> recursos) {
            if (recursos.isEmpty()) {
                System.out.println("No hay productos para mostrar.");
                return;
            }

            System.out.printf("%n%-8s %-25s %8s %12s %-12s%n",
                    "CÓDIGO", "PRODUCTO", "STOCK", "MÍNIMO", "ESTADO");
            System.out.println("-".repeat(70));

            for (Medicamento r : recursos) {
                String nombreCorto = r.nombre.length() > 25
                        ? r.nombre.substring(0, 25) : r.nombre;
                System.out.printf("%-8s %-25s %8d %12d %-12s%n",
                        r.codigo, nombreCorto, r.stock, r.stockMinimo,
                        r.verificarStock());
            }
        }

        public static void resumen(GestorInventario gestor) {
            System.out.println("\n========== REPORTE GENERAL ==========");
            System.out.println("Total de productos: " + gestor.recursos.size());
            System.out.println("Stock bajo: " + stockBajo(gestor.recursos).size());
            System.out.println("Agotados: " + agotados(gestor.recursos).size());
            System.out.println("Próximos a vencer (30 días): "
                    + proximosAVencer(gestor.recursos).size());
            System.out.println("Riesgo del establecimiento: "
                    + gestor.establecimiento.calcularRiesgo());
            mostrar(gestor.recursos);
        }
    }

    // Lee un número entero y comprueba que cumpla el mínimo indicado.
    private static Integer leerEntero(String mensaje, int minimo) {
        System.out.print(mensaje);
        try {
            int valor = Integer.parseInt(scanner.nextLine().trim());
            if (valor < minimo) {
                throw new NumberFormatException();
            }
            return valor;
        } catch (NumberFormatException e) {
            System.out.println("Error: ingrese un número entero igual o mayor que " + minimo + ".");
            return null;
        }
    }

    private static void menu() {
        GestorInventario gestor = GestorInventario.obtenerInstancia();

        while (true) {
            System.out.println("""

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
                    """);
            System.out.print("Seleccione una opción: ");
            String opcion = scanner.nextLine().trim();

            try {
                switch (opcion) {
                    case "1" -> {
                        System.out.print("Código: ");
                        String codigo = scanner.nextLine().trim();

                        System.out.print("Nombre: ");
                        String nombre = scanner.nextLine().trim();

                        Integer stock = leerEntero("Stock inicial: ", 0);
                        if (stock == null) continue;

                        Integer minimo = leerEntero("Stock mínimo: ", 0);
                        if (minimo == null) continue;

                        System.out.print("Vencimiento (AAAA-MM-DD): ");
                        String vencimiento = scanner.nextLine().trim();

                        System.out.print("Tipo (Medicamento/Insumo médico): ");
                        String tipo = scanner.nextLine().trim();
                        if (tipo.isEmpty()) tipo = "Medicamento";

                        Medicamento recurso = MedicamentoFactory.crearMedicamento(
                                codigo, nombre, stock, minimo, vencimiento, tipo);
                        gestor.agregar(recurso);
                        System.out.println("Producto registrado correctamente.");
                    }
                    case "2" -> Reporte.mostrar(gestor.listar());

                    case "3" -> {
                        System.out.print("Código del producto: ");
                        String codigo = scanner.nextLine();
                        Integer cantidad = leerEntero("Nueva cantidad total: ", 0);
                        if (cantidad != null) {
                            Medicamento recurso = gestor.actualizar(codigo, cantidad);
                            System.out.println("Stock actualizado. Nuevo estado: "
                                    + recurso.verificarStock());
                        }
                    }
                    case "4" -> {
                        System.out.print("Código del producto: ");
                        String codigo = scanner.nextLine();
                        Integer cantidad = leerEntero("Cantidad que ingresa: ", 1);
                        if (cantidad != null) {
                            Medicamento recurso = gestor.entrada(codigo, cantidad);
                            System.out.println("Entrada registrada. Stock actual: " + recurso.stock);
                        }
                    }
                    case "5" -> {
                        System.out.print("Código del producto: ");
                        String codigo = scanner.nextLine();
                        Integer cantidad = leerEntero("Cantidad que sale: ", 1);
                        if (cantidad != null) {
                            Medicamento recurso = gestor.salida(codigo, cantidad);
                            System.out.println("Salida registrada. Stock actual: " + recurso.stock);
                        }
                    }
                    case "6" -> {
                        System.out.println("\n--- PRODUCTOS CON STOCK BAJO ---");
                        Reporte.mostrar(Reporte.stockBajo(gestor.recursos));
                        System.out.println("\n--- PRODUCTOS AGOTADOS ---");
                        Reporte.mostrar(Reporte.agotados(gestor.recursos));
                    }
                    case "7" -> {
                        System.out.println("\n--- PRÓXIMOS A VENCER ---");
                        Reporte.mostrar(Reporte.proximosAVencer(gestor.recursos));
                    }
                    case "8" -> Reporte.resumen(gestor);

                    case "9" -> {
                        System.out.println("Gracias por utilizar MedicRural-PE.");
                        return;
                    }
                    default -> System.out.println("Opción no válida. Intente nuevamente.");
                }
            } catch (RuntimeException e) {
                System.out.println("Error: " + e.getMessage());
            }
        }
    }
}
