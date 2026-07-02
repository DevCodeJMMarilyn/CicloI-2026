PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS fact_ventas;
DROP TABLE IF EXISTS dim_productos;
DROP TABLE IF EXISTS dim_clientes;

CREATE TABLE dim_productos (
    id_producto INTEGER PRIMARY KEY,
    sku TEXT NOT NULL UNIQUE,
    producto TEXT NOT NULL,
    categoria TEXT NOT NULL,
    marca TEXT NOT NULL,
    costo_unitario_usd REAL NOT NULL CHECK (costo_unitario_usd >= 0),
    precio_lista_usd REAL NOT NULL CHECK (precio_lista_usd >= 0),
    activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1))
);

CREATE TABLE dim_clientes (
    id_cliente INTEGER PRIMARY KEY,
    nombre_cliente TEXT NOT NULL,
    segmento TEXT NOT NULL CHECK (segmento IN ('Retail', 'Mayorista', 'Corporativo')),
    departamento TEXT NOT NULL,
    municipio TEXT NOT NULL,
    direccion TEXT NOT NULL,
    telefono TEXT,
    email TEXT UNIQUE,
    fecha_alta TEXT NOT NULL
);

CREATE TABLE fact_ventas (
    id_venta INTEGER PRIMARY KEY,
    fecha_venta TEXT NOT NULL,
    id_producto INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    canal_venta TEXT NOT NULL CHECK (canal_venta IN ('Tienda', 'Online', 'Telefono')),
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario_usd REAL NOT NULL CHECK (precio_unitario_usd >= 0),
    descuento_usd REAL NOT NULL DEFAULT 0 CHECK (descuento_usd >= 0),
    impuesto_usd REAL NOT NULL DEFAULT 0 CHECK (impuesto_usd >= 0),
    total_venta_usd REAL NOT NULL CHECK (total_venta_usd >= 0),
    moneda TEXT NOT NULL DEFAULT 'USD' CHECK (moneda = 'USD'),
    FOREIGN KEY (id_producto) REFERENCES dim_productos (id_producto),
    FOREIGN KEY (id_cliente) REFERENCES dim_clientes (id_cliente)
);

CREATE INDEX idx_fact_ventas_fecha ON fact_ventas (fecha_venta);
CREATE INDEX idx_fact_ventas_producto ON fact_ventas (id_producto);
CREATE INDEX idx_fact_ventas_cliente ON fact_ventas (id_cliente);

INSERT INTO dim_productos (
    id_producto, sku, producto, categoria, marca, costo_unitario_usd, precio_lista_usd, activo
) VALUES
(1, 'NR-TEC-001', 'Laptop NovaBook 14', 'Tecnologia', 'NovaTech', 520.00, 799.00, 1),
(2, 'NR-TEC-002', 'Mouse inalambrico', 'Tecnologia', 'ClickPro', 8.50, 18.99, 1),
(3, 'NR-TEC-003', 'Teclado mecanico', 'Tecnologia', 'KeyMax', 29.00, 59.99, 1),
(4, 'NR-TEC-004', 'Monitor LED 24 pulgadas', 'Tecnologia', 'ViewNova', 92.00, 159.00, 1),
(5, 'NR-HOG-001', 'Cafetera electrica', 'Hogar', 'CasaPlus', 22.00, 44.99, 1),
(6, 'NR-HOG-002', 'Licuadora 5 velocidades', 'Hogar', 'CasaPlus', 18.00, 39.99, 1),
(7, 'NR-ROP-001', 'Camisa casual hombre', 'Ropa', 'Urbano', 9.00, 24.99, 1),
(8, 'NR-ROP-002', 'Jeans dama', 'Ropa', 'Urbano', 14.50, 34.99, 1),
(9, 'NR-CAL-001', 'Zapatos deportivos', 'Calzado', 'RunFit', 24.00, 54.99, 1),
(10, 'NR-CAL-002', 'Sandalias casuales', 'Calzado', 'SolMar', 7.00, 19.99, 1),
(11, 'NR-ALI-001', 'Canasta basica familiar', 'Alimentos', 'Selecto', 18.50, 29.99, 1),
(12, 'NR-ALI-002', 'Cafe molido premium', 'Alimentos', 'Volcan', 3.20, 7.99, 1);

INSERT INTO dim_clientes (
    id_cliente, nombre_cliente, segmento, departamento, municipio, direccion, telefono, email, fecha_alta
) VALUES
(1, 'Ana Martinez', 'Retail', 'San Salvador', 'San Salvador', 'Colonia Escalon, 79 Avenida Norte #215', '503-2221-1001', 'ana.martinez@correo.com', '2025-01-10'),
(2, 'Carlos Hernandez', 'Retail', 'La Libertad', 'Santa Tecla', 'Residencial Las Delicias, Pasaje 3 #18', '503-2288-1002', 'carlos.hernandez@correo.com', '2025-01-18'),
(3, 'Distribuidora Cuscatlan', 'Mayorista', 'Cuscatlan', 'Cojutepeque', 'Barrio El Centro, Avenida Rafael Cabrera #42', '503-2372-1003', 'compras@distcuscatlan.com', '2025-02-02'),
(4, 'Marta Lopez', 'Retail', 'Santa Ana', 'Santa Ana', 'Urbanizacion El Palmar, Calle Principal #9', '503-2440-1004', 'marta.lopez@correo.com', '2025-02-14'),
(5, 'Grupo Pacifico SA de CV', 'Corporativo', 'San Miguel', 'San Miguel', 'Avenida Roosevelt Sur, Plaza Comercial Local 12', '503-2667-1005', 'finanzas@grupopacifico.com', '2025-03-01'),
(6, 'Jose Rivera', 'Retail', 'Sonsonate', 'Sonsonate', 'Colonia Santa Marta, Poligono B #23', '503-2451-1006', 'jose.rivera@correo.com', '2025-03-09'),
(7, 'Comercial La Union', 'Mayorista', 'La Union', 'La Union', 'Barrio Concepcion, 2a Calle Oriente #31', '503-2604-1007', 'ventas@comerciallaunion.com', '2025-03-22'),
(8, 'Karla Pineda', 'Retail', 'Ahuachapan', 'Ahuachapan', 'Colonia El Progreso, Calle Los Ausoles #7', '503-2413-1008', 'karla.pineda@correo.com', '2025-04-05'),
(9, 'Servicios Metapan', 'Corporativo', 'Santa Ana', 'Metapan', 'Carretera a San Salvador, Km 112, Bodega 4', '503-2402-1009', 'admin@serviciosmetapan.com', '2025-04-17'),
(10, 'Luis Morales', 'Retail', 'La Paz', 'Zacatecoluca', 'Barrio El Calvario, 4a Avenida Sur #16', '503-2334-1010', 'luis.morales@correo.com', '2025-05-03');

INSERT INTO fact_ventas (
    id_venta, fecha_venta, id_producto, id_cliente, canal_venta, cantidad,
    precio_unitario_usd, descuento_usd, impuesto_usd, total_venta_usd, moneda
) VALUES
(1, '2026-01-03', 1, 1, 'Tienda', 1, 799.00, 25.00, 100.62, 874.62, 'USD'),
(2, '2026-01-04', 2, 2, 'Online', 3, 18.99, 0.00, 7.41, 64.38, 'USD'),
(3, '2026-01-05', 11, 3, 'Telefono', 15, 29.99, 20.00, 55.88, 485.73, 'USD'),
(4, '2026-01-07', 5, 4, 'Tienda', 2, 44.99, 5.00, 11.05, 96.03, 'USD'),
(5, '2026-01-09', 4, 5, 'Online', 4, 159.00, 40.00, 77.48, 673.48, 'USD'),
(6, '2026-01-10', 12, 6, 'Tienda', 6, 7.99, 2.00, 5.97, 51.91, 'USD'),
(7, '2026-01-12', 7, 7, 'Telefono', 20, 24.99, 35.00, 60.29, 525.09, 'USD'),
(8, '2026-01-15', 9, 8, 'Tienda', 1, 54.99, 0.00, 7.15, 62.14, 'USD'),
(9, '2026-01-17', 3, 9, 'Online', 5, 59.99, 15.00, 37.05, 321.00, 'USD'),
(10, '2026-01-20', 6, 10, 'Tienda', 1, 39.99, 0.00, 5.20, 45.19, 'USD'),
(11, '2026-01-22', 8, 1, 'Online', 2, 34.99, 3.00, 8.71, 75.69, 'USD'),
(12, '2026-01-25', 10, 2, 'Tienda', 3, 19.99, 0.00, 7.80, 67.77, 'USD'),
(13, '2026-02-02', 1, 3, 'Telefono', 3, 779.00, 100.00, 290.81, 2527.81, 'USD'),
(14, '2026-02-03', 2, 4, 'Tienda', 2, 18.99, 0.00, 4.94, 42.92, 'USD'),
(15, '2026-02-05', 5, 5, 'Online', 6, 44.99, 18.00, 32.75, 284.69, 'USD'),
(16, '2026-02-08', 9, 6, 'Tienda', 2, 54.99, 5.00, 13.65, 118.63, 'USD'),
(17, '2026-02-10', 11, 7, 'Telefono', 25, 29.99, 40.00, 92.27, 802.02, 'USD'),
(18, '2026-02-11', 12, 8, 'Online', 4, 7.99, 0.00, 4.15, 36.11, 'USD'),
(19, '2026-02-13', 4, 9, 'Tienda', 2, 159.00, 20.00, 38.74, 336.74, 'USD'),
(20, '2026-02-15', 7, 10, 'Online', 3, 24.99, 5.00, 9.10, 79.07, 'USD'),
(21, '2026-02-18', 6, 1, 'Tienda', 2, 39.99, 0.00, 10.40, 90.38, 'USD'),
(22, '2026-02-20', 8, 2, 'Online', 1, 34.99, 0.00, 4.55, 39.54, 'USD'),
(23, '2026-02-22', 3, 3, 'Telefono', 8, 59.99, 30.00, 58.49, 508.41, 'USD'),
(24, '2026-02-25', 10, 4, 'Tienda', 4, 19.99, 4.00, 9.88, 85.84, 'USD'),
(25, '2026-03-01', 1, 5, 'Online', 2, 799.00, 80.00, 197.34, 1715.34, 'USD'),
(26, '2026-03-03', 2, 6, 'Tienda', 1, 18.99, 0.00, 2.47, 21.46, 'USD'),
(27, '2026-03-04', 11, 7, 'Telefono', 30, 29.99, 50.00, 110.46, 960.16, 'USD'),
(28, '2026-03-06', 5, 8, 'Online', 1, 44.99, 0.00, 5.85, 50.84, 'USD'),
(29, '2026-03-09', 9, 9, 'Tienda', 4, 54.99, 20.00, 25.99, 225.95, 'USD'),
(30, '2026-03-11', 12, 10, 'Online', 8, 7.99, 3.00, 7.92, 68.84, 'USD'),
(31, '2026-03-13', 4, 1, 'Tienda', 1, 159.00, 0.00, 20.67, 179.67, 'USD'),
(32, '2026-03-15', 7, 2, 'Online', 2, 24.99, 0.00, 6.50, 56.48, 'USD'),
(33, '2026-03-17', 3, 3, 'Telefono', 10, 59.99, 50.00, 71.49, 621.39, 'USD'),
(34, '2026-03-20', 6, 4, 'Tienda', 3, 39.99, 5.00, 14.95, 129.92, 'USD'),
(35, '2026-03-22', 8, 5, 'Online', 5, 34.99, 15.00, 20.79, 180.74, 'USD'),
(36, '2026-03-25', 10, 6, 'Tienda', 2, 19.99, 0.00, 5.20, 45.18, 'USD'),
(37, '2026-04-01', 1, 7, 'Telefono', 4, 779.00, 150.00, 385.58, 3351.58, 'USD'),
(38, '2026-04-02', 2, 8, 'Online', 5, 18.99, 5.00, 11.69, 101.64, 'USD'),
(39, '2026-04-04', 11, 9, 'Tienda', 12, 29.99, 10.00, 45.23, 395.11, 'USD'),
(40, '2026-04-06', 5, 10, 'Online', 2, 44.99, 0.00, 11.70, 101.68, 'USD'),
(41, '2026-04-08', 4, 1, 'Tienda', 2, 159.00, 20.00, 38.74, 336.74, 'USD'),
(42, '2026-04-10', 12, 2, 'Online', 10, 7.99, 4.00, 9.87, 85.77, 'USD'),
(43, '2026-04-12', 7, 3, 'Telefono', 18, 24.99, 30.00, 54.58, 474.40, 'USD'),
(44, '2026-04-14', 9, 4, 'Tienda', 1, 54.99, 0.00, 7.15, 62.14, 'USD'),
(45, '2026-04-16', 3, 5, 'Online', 6, 59.99, 20.00, 44.19, 384.13, 'USD'),
(46, '2026-04-18', 6, 6, 'Tienda', 4, 39.99, 8.00, 19.24, 171.20, 'USD'),
(47, '2026-04-20', 8, 7, 'Telefono', 12, 34.99, 25.00, 51.34, 446.22, 'USD'),
(48, '2026-04-22', 10, 8, 'Online', 2, 19.99, 0.00, 5.20, 45.18, 'USD'),
(49, '2026-05-01', 1, 9, 'Tienda', 1, 799.00, 40.00, 98.67, 857.67, 'USD'),
(50, '2026-05-03', 2, 10, 'Online', 4, 18.99, 2.00, 9.61, 83.57, 'USD'),
(51, '2026-05-05', 11, 1, 'Tienda', 5, 29.99, 0.00, 19.49, 169.44, 'USD'),
(52, '2026-05-07', 5, 2, 'Online', 3, 44.99, 6.00, 16.76, 145.73, 'USD'),
(53, '2026-05-09', 4, 3, 'Telefono', 5, 159.00, 60.00, 95.55, 830.55, 'USD'),
(54, '2026-05-11', 12, 4, 'Tienda', 7, 7.99, 2.00, 7.01, 60.94, 'USD'),
(55, '2026-05-13', 7, 5, 'Online', 10, 24.99, 15.00, 30.55, 265.45, 'USD'),
(56, '2026-05-15', 9, 6, 'Tienda', 2, 54.99, 0.00, 14.30, 124.28, 'USD'),
(57, '2026-05-17', 3, 7, 'Telefono', 7, 59.99, 25.00, 51.34, 446.27, 'USD'),
(58, '2026-05-19', 6, 8, 'Online', 2, 39.99, 0.00, 10.40, 90.38, 'USD'),
(59, '2026-05-21', 8, 9, 'Tienda', 3, 34.99, 5.00, 12.99, 112.96, 'USD'),
(60, '2026-05-23', 10, 10, 'Online', 5, 19.99, 5.00, 12.34, 107.29, 'USD');
