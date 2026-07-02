import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).with_name("novaretail.db")


def crear_base_datos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.executescript(
        """
        DROP TABLE IF EXISTS FactVentas;
        DROP TABLE IF EXISTS DimCliente;
        DROP TABLE IF EXISTS DimProducto;
        DROP TABLE IF EXISTS DimRegion;

        CREATE TABLE DimRegion (
            RegionID INTEGER PRIMARY KEY,
            Pais TEXT NOT NULL,
            Departamento TEXT NOT NULL,
            Municipio TEXT NOT NULL,
            Moneda TEXT NOT NULL DEFAULT 'USD'
        );

        CREATE TABLE DimProducto (
            ProductoID INTEGER PRIMARY KEY,
            NombreProducto TEXT NOT NULL,
            Categoria TEXT NOT NULL,
            Marca TEXT NOT NULL,
            PrecioUnitario REAL NOT NULL
        );

        CREATE TABLE DimCliente (
            ClienteID INTEGER PRIMARY KEY,
            NombreCliente TEXT NOT NULL,
            Genero TEXT NOT NULL,
            Edad INTEGER NOT NULL,
            Segmento TEXT NOT NULL,
            RegionID INTEGER NOT NULL,
            FOREIGN KEY (RegionID) REFERENCES DimRegion(RegionID)
        );

        CREATE TABLE FactVentas (
            VentaID INTEGER PRIMARY KEY,
            FechaVenta TEXT NOT NULL,
            ClienteID INTEGER NOT NULL,
            ProductoID INTEGER NOT NULL,
            Cantidad INTEGER NOT NULL,
            PrecioUnitario REAL NOT NULL,
            Descuento REAL NOT NULL DEFAULT 0,
            TotalVenta REAL NOT NULL,
            MetodoPago TEXT NOT NULL,
            CanalVenta TEXT NOT NULL,
            FOREIGN KEY (ClienteID) REFERENCES DimCliente(ClienteID),
            FOREIGN KEY (ProductoID) REFERENCES DimProducto(ProductoID)
        );
        """
    )

    regiones = [
        (1, "El Salvador", "San Salvador", "San Salvador", "USD"),
        (2, "El Salvador", "La Libertad", "Santa Tecla", "USD"),
        (3, "El Salvador", "Santa Ana", "Santa Ana", "USD"),
        (4, "El Salvador", "San Miguel", "San Miguel", "USD"),
        (5, "El Salvador", "Sonsonate", "Sonsonate", "USD"),
        (6, "El Salvador", "Usulutan", "Usulutan", "USD"),
        (7, "El Salvador", "La Paz", "Zacatecoluca", "USD"),
        (8, "El Salvador", "Ahuachapan", "Ahuachapan", "USD"),
    ]

    productos = [
        (1, "Laptop NovaBook 14", "Tecnologia", "NovaTech", 699.99),
        (2, "Smartphone Nova X1", "Tecnologia", "NovaTech", 349.99),
        (3, "Audifonos Bluetooth", "Accesorios", "SoundPro", 39.99),
        (4, "Monitor LED 24 pulgadas", "Tecnologia", "ViewMax", 159.99),
        (5, "Teclado Mecanico", "Accesorios", "KeyMaster", 59.99),
        (6, "Mouse Inalambrico", "Accesorios", "ClickPro", 24.99),
        (7, "Silla Ergonomica", "Oficina", "ComfortPlus", 189.99),
        (8, "Escritorio Ejecutivo", "Oficina", "Woodline", 249.99),
        (9, "Impresora Multifuncional", "Oficina", "PrintFast", 129.99),
        (10, "Tablet NovaTab 10", "Tecnologia", "NovaTech", 219.99),
        (11, "Cafetera Electrica", "Hogar", "HomeStar", 44.99),
        (12, "Licuadora 5 Velocidades", "Hogar", "HomeStar", 54.99),
        (13, "Microondas 0.9 pies", "Hogar", "HeatWave", 119.99),
        (14, "Refrigeradora 12 pies", "Hogar", "CoolMax", 499.99),
        (15, "Smart TV 43 pulgadas", "Tecnologia", "ViewMax", 379.99),
    ]

    clientes = [
        (1, "Andrea Lopez", "Femenino", 28, "Retail", 1),
        (2, "Carlos Martinez", "Masculino", 35, "Retail", 2),
        (3, "Sofia Hernandez", "Femenino", 42, "Corporativo", 1),
        (4, "Miguel Ramirez", "Masculino", 31, "Retail", 3),
        (5, "Gabriela Torres", "Femenino", 26, "Retail", 4),
        (6, "Jorge Morales", "Masculino", 39, "Mayorista", 5),
        (7, "Lucia Perez", "Femenino", 33, "Corporativo", 2),
        (8, "Fernando Castillo", "Masculino", 45, "Mayorista", 6),
        (9, "Mariana Gutierrez", "Femenino", 24, "Retail", 7),
        (10, "Roberto Aguilar", "Masculino", 52, "Corporativo", 8),
        (11, "Daniela Escobar", "Femenino", 30, "Retail", 1),
        (12, "Oscar Rivera", "Masculino", 41, "Mayorista", 3),
        (13, "Paola Vasquez", "Femenino", 37, "Corporativo", 4),
        (14, "Luis Mejia", "Masculino", 29, "Retail", 5),
        (15, "Karla Flores", "Femenino", 34, "Retail", 6),
        (16, "Ricardo Salazar", "Masculino", 48, "Corporativo", 7),
        (17, "Beatriz Nunez", "Femenino", 27, "Retail", 8),
        (18, "Manuel Caceres", "Masculino", 36, "Mayorista", 2),
        (19, "Elena Chavez", "Femenino", 44, "Corporativo", 1),
        (20, "Hector Molina", "Masculino", 32, "Retail", 4),
    ]

    ventas_base = [
        (1, "2026-01-03", 1, 2, 1, 349.99, 10.00, "Tarjeta", "Tienda"),
        (2, "2026-01-04", 2, 3, 2, 39.99, 0.00, "Efectivo", "Tienda"),
        (3, "2026-01-05", 3, 1, 3, 699.99, 100.00, "Transferencia", "Corporativo"),
        (4, "2026-01-06", 4, 6, 1, 24.99, 0.00, "Efectivo", "Tienda"),
        (5, "2026-01-07", 5, 10, 1, 219.99, 15.00, "Tarjeta", "Online"),
        (6, "2026-01-08", 6, 14, 2, 499.99, 50.00, "Transferencia", "Mayorista"),
        (7, "2026-01-09", 7, 4, 4, 159.99, 40.00, "Transferencia", "Corporativo"),
        (8, "2026-01-10", 8, 8, 5, 249.99, 125.00, "Transferencia", "Mayorista"),
        (9, "2026-01-11", 9, 11, 1, 44.99, 0.00, "Efectivo", "Tienda"),
        (10, "2026-01-12", 10, 15, 2, 379.99, 30.00, "Tarjeta", "Online"),
        (11, "2026-01-13", 11, 5, 1, 59.99, 0.00, "Tarjeta", "Tienda"),
        (12, "2026-01-14", 12, 9, 3, 129.99, 20.00, "Transferencia", "Mayorista"),
        (13, "2026-01-15", 13, 7, 2, 189.99, 25.00, "Tarjeta", "Corporativo"),
        (14, "2026-01-16", 14, 12, 1, 54.99, 5.00, "Efectivo", "Tienda"),
        (15, "2026-01-17", 15, 13, 1, 119.99, 0.00, "Tarjeta", "Online"),
        (16, "2026-01-18", 16, 1, 2, 699.99, 80.00, "Transferencia", "Corporativo"),
        (17, "2026-01-19", 17, 3, 1, 39.99, 0.00, "Efectivo", "Tienda"),
        (18, "2026-01-20", 18, 4, 6, 159.99, 90.00, "Transferencia", "Mayorista"),
        (19, "2026-01-21", 19, 10, 2, 219.99, 20.00, "Tarjeta", "Corporativo"),
        (20, "2026-01-22", 20, 2, 1, 349.99, 0.00, "Tarjeta", "Online"),
        (21, "2026-02-01", 1, 15, 1, 379.99, 15.00, "Tarjeta", "Online"),
        (22, "2026-02-02", 2, 11, 2, 44.99, 0.00, "Efectivo", "Tienda"),
        (23, "2026-02-03", 3, 9, 5, 129.99, 60.00, "Transferencia", "Corporativo"),
        (24, "2026-02-04", 4, 5, 1, 59.99, 0.00, "Tarjeta", "Tienda"),
        (25, "2026-02-05", 5, 6, 2, 24.99, 0.00, "Efectivo", "Tienda"),
        (26, "2026-02-06", 6, 8, 4, 249.99, 100.00, "Transferencia", "Mayorista"),
        (27, "2026-02-07", 7, 1, 1, 699.99, 50.00, "Transferencia", "Corporativo"),
        (28, "2026-02-08", 8, 14, 3, 499.99, 120.00, "Transferencia", "Mayorista"),
        (29, "2026-02-09", 9, 3, 2, 39.99, 5.00, "Tarjeta", "Online"),
        (30, "2026-02-10", 10, 13, 1, 119.99, 10.00, "Efectivo", "Tienda"),
        (31, "2026-02-11", 11, 2, 2, 349.99, 30.00, "Tarjeta", "Online"),
        (32, "2026-02-12", 12, 7, 6, 189.99, 150.00, "Transferencia", "Mayorista"),
        (33, "2026-02-13", 13, 4, 3, 159.99, 35.00, "Transferencia", "Corporativo"),
        (34, "2026-02-14", 14, 12, 1, 54.99, 0.00, "Efectivo", "Tienda"),
        (35, "2026-02-15", 15, 11, 1, 44.99, 0.00, "Tarjeta", "Tienda"),
        (36, "2026-02-16", 16, 10, 4, 219.99, 75.00, "Transferencia", "Corporativo"),
        (37, "2026-02-17", 17, 6, 1, 24.99, 0.00, "Efectivo", "Tienda"),
        (38, "2026-02-18", 18, 15, 2, 379.99, 40.00, "Transferencia", "Mayorista"),
        (39, "2026-02-19", 19, 1, 1, 699.99, 25.00, "Tarjeta", "Corporativo"),
        (40, "2026-02-20", 20, 5, 2, 59.99, 10.00, "Tarjeta", "Online"),
        (41, "2026-03-01", 1, 9, 1, 129.99, 0.00, "Tarjeta", "Tienda"),
        (42, "2026-03-02", 2, 10, 1, 219.99, 10.00, "Tarjeta", "Online"),
        (43, "2026-03-03", 3, 8, 2, 249.99, 30.00, "Transferencia", "Corporativo"),
        (44, "2026-03-04", 4, 14, 1, 499.99, 20.00, "Tarjeta", "Tienda"),
        (45, "2026-03-05", 5, 3, 3, 39.99, 0.00, "Efectivo", "Tienda"),
        (46, "2026-03-06", 6, 7, 3, 189.99, 45.00, "Transferencia", "Mayorista"),
        (47, "2026-03-07", 7, 13, 2, 119.99, 15.00, "Tarjeta", "Corporativo"),
        (48, "2026-03-08", 8, 1, 2, 699.99, 100.00, "Transferencia", "Mayorista"),
        (49, "2026-03-09", 9, 2, 1, 349.99, 20.00, "Tarjeta", "Online"),
        (50, "2026-03-10", 10, 12, 2, 54.99, 5.00, "Efectivo", "Tienda"),
    ]

    ventas = [
        (
            venta_id,
            fecha,
            cliente_id,
            producto_id,
            cantidad,
            precio_unitario,
            descuento,
            round((cantidad * precio_unitario) - descuento, 2),
            metodo_pago,
            canal_venta,
        )
        for (
            venta_id,
            fecha,
            cliente_id,
            producto_id,
            cantidad,
            precio_unitario,
            descuento,
            metodo_pago,
            canal_venta,
        ) in ventas_base
    ]

    cursor.executemany("INSERT INTO DimRegion VALUES (?, ?, ?, ?, ?);", regiones)
    cursor.executemany("INSERT INTO DimProducto VALUES (?, ?, ?, ?, ?);", productos)
    cursor.executemany("INSERT INTO DimCliente VALUES (?, ?, ?, ?, ?, ?);", clientes)
    cursor.executemany(
        """
        INSERT INTO FactVentas (
            VentaID,
            FechaVenta,
            ClienteID,
            ProductoID,
            Cantidad,
            PrecioUnitario,
            Descuento,
            TotalVenta,
            MetodoPago,
            CanalVenta
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        ventas,
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    crear_base_datos()
    print(f"Base de datos creada correctamente: {DB_PATH}")
