-- =========================================
-- BASE DE DATOS: FashionStore
-- =========================================
CREATE DATABASE FashionStore;
USE FashionStore;

-- =========================================
-- TABLA PRODUCTOS
-- =========================================
CREATE TABLE Productos (
    id_producto INT PRIMARY KEY,
    producto VARCHAR(100),
    categoria VARCHAR(50),
    subcategoria VARCHAR(50),
    marca VARCHAR(50),
    genero VARCHAR(20), -- Hombre, Mujer, Niño, Niña, Unisex
    temporada VARCHAR(20) -- Primavera, Verano, Otoño, Invierno
);

INSERT INTO Productos VALUES
(1, 'Jeans Clásicos', 'Ropa', 'Pantalones', 'Levis', 'Hombre', 'Todo año'),
(2, 'Camisa Manga Larga', 'Ropa', 'Camisas', 'Zara', 'Hombre', 'Otoño'),
(3, 'Vestido Floral', 'Ropa', 'Vestidos', 'H&M', 'Mujer', 'Primavera'),
(4, 'Chaqueta de Cuero', 'Ropa', 'Chaquetas', 'Zara', 'Mujer', 'Invierno'),
(5, 'Zapatillas Deportivas', 'Calzado', 'Tenis', 'Nike', 'Unisex', 'Todo año'),
(6, 'Jeans Skinny', 'Ropa', 'Pantalones', 'H&M', 'Mujer', 'Todo año'),
(7, 'Camiseta Básica', 'Ropa', 'Camisetas', 'GAP', 'Hombre', 'Verano'),
(8, 'Sudadera con Capucha', 'Ropa', 'Sudaderas', 'Adidas', 'Unisex', 'Invierno'),
(9, 'Falda Plisada', 'Ropa', 'Faldas', 'Bershka', 'Mujer', 'Primavera'),
(10, 'Shorts Deportivos', 'Ropa', 'Shorts', 'Nike', 'Hombre', 'Verano'),
(11, 'Vestido de Noche', 'Ropa', 'Vestidos', 'Zara', 'Mujer', 'Invierno'),
(12, 'Camisa Polo', 'Ropa', 'Camisas', 'Lacoste', 'Hombre', 'Verano'),
(13, 'Jeans Acampanados', 'Ropa', 'Pantalones', 'Levis', 'Mujer', 'Otoño'),
(14, 'Chaqueta de Plumas', 'Ropa', 'Chaquetas', 'The North Face', 'Unisex', 'Invierno'),
(15, 'Zapatos Formales', 'Calzado', 'Zapatos', 'Aldo', 'Hombre', 'Todo año');

-- =========================================
-- TABLA CLIENTES
-- =========================================
CREATE TABLE Clientes (
    id_cliente INT PRIMARY KEY,
    nombre VARCHAR(100),
    ciudad VARCHAR(50),
    pais VARCHAR(50),
    edad INT,
    genero VARCHAR(20)
);

INSERT INTO Clientes VALUES
(1, 'Ana López', 'Madrid', 'España', 28, 'Femenino'),
(2, 'Carlos Ruiz', 'Barcelona', 'España', 35, 'Masculino'),
(3, 'María García', 'Valencia', 'España', 42, 'Femenino'),
(4, 'Juan Pérez', 'Sevilla', 'España', 31, 'Masculino'),
(5, 'Laura Martínez', 'Bilbao', 'España', 25, 'Femenino'),
(6, 'Pedro Sánchez', 'Madrid', 'España', 45, 'Masculino'),
(7, 'Elena Gómez', 'Barcelona', 'España', 33, 'Femenino'),
(8, 'David Fernández', 'Valencia', 'España', 29, 'Masculino'),
(9, 'Sara Díaz', 'Sevilla', 'España', 38, 'Femenino'),
(10, 'Javier Rodríguez', 'Bilbao', 'España', 41, 'Masculino');

-- =========================================
-- TABLA TIENDAS
-- =========================================
CREATE TABLE Tiendas (
    id_tienda INT PRIMARY KEY,
    tienda VARCHAR(100),
    ciudad VARCHAR(50),
    pais VARCHAR(50),
    region VARCHAR(50)
);

INSERT INTO Tiendas VALUES
(1, 'FashionStore Madrid Centro', 'Madrid', 'España', 'Centro'),
(2, 'FashionStore Barcelona Diagonal', 'Barcelona', 'España', 'Este'),
(3, 'FashionStore Valencia', 'Valencia', 'España', 'Este'),
(4, 'FashionStore Sevilla', 'Sevilla', 'España', 'Sur'),
(5, 'FashionStore Bilbao', 'Bilbao', 'España', 'Norte');

-- =========================================
-- TABLA TIEMPO (Calendario)
-- =========================================
CREATE TABLE Tiempo (
    id_tiempo INT PRIMARY KEY,
    fecha DATE,
    dia INT,
    mes INT,
    mes_nombre VARCHAR(20),
    trimestre INT,
    año INT
);

-- Insertar días del primer semestre 2024
DECLARE @fecha DATE = '2024-01-01';
DECLARE @contador INT = 1;

WHILE @fecha <= '2024-06-30'
BEGIN
    INSERT INTO Tiempo VALUES (
        @contador,
        @fecha,
        DAY(@fecha),
        MONTH(@fecha),
        CASE MONTH(@fecha)
            WHEN 1 THEN 'Enero'
            WHEN 2 THEN 'Febrero'
            WHEN 3 THEN 'Marzo'
            WHEN 4 THEN 'Abril'
            WHEN 5 THEN 'Mayo'
            WHEN 6 THEN 'Junio'
        END,
        CASE 
            WHEN MONTH(@fecha) IN (1,2,3) THEN 1
            WHEN MONTH(@fecha) IN (4,5,6) THEN 2
        END,
        YEAR(@fecha)
    );
    SET @fecha = DATEADD(day, 1, @fecha);
    SET @contador = @contador + 1;
END;


-- =========================================
-- TABLA VENTAS (HECHOS)
-- =========================================
CREATE TABLE Ventas (
    id_venta INT PRIMARY KEY,
    id_tiempo INT,
    id_cliente INT,
    id_producto INT,
    id_tienda INT,
    cantidad INT,
    precio_unitario DECIMAL(10,2),
    descuento DECIMAL(10,2),
    FOREIGN KEY (id_tiempo) REFERENCES Tiempo(id_tiempo),
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto),
    FOREIGN KEY (id_tienda) REFERENCES Tiendas(id_tienda)
);

-- Insertar 50 ventas de ejemplo
INSERT INTO Ventas VALUES
(1, 15, 1, 1, 1, 2, 89.90, 0),
(2, 15, 2, 3, 2, 1, 59.90, 0),
(3, 16, 3, 5, 3, 1, 120.00, 10),
(4, 16, 4, 2, 1, 3, 49.90, 0),
(5, 17, 5, 7, 4, 2, 29.90, 5),
(6, 17, 1, 8, 2, 1, 79.90, 0),
(7, 18, 2, 4, 3, 1, 149.90, 15),
(8, 18, 3, 6, 1, 2, 69.90, 0),
(9, 19, 4, 9, 5, 1, 39.90, 0),
(10, 19, 5, 10, 2, 3, 34.90, 0),
(11, 20, 6, 11, 3, 1, 89.90, 0),
(12, 20, 7, 12, 4, 2, 79.90, 10),
(13, 21, 8, 13, 1, 1, 69.90, 0),
(14, 21, 9, 14, 2, 1, 199.90, 20),
(15, 22, 10, 15, 5, 1, 129.90, 0),
(16, 22, 1, 2, 3, 2, 49.90, 0),
(17, 23, 2, 4, 4, 1, 149.90, 0),
(18, 23, 3, 6, 1, 1, 69.90, 5),
(19, 24, 4, 8, 2, 2, 79.90, 0),
(20, 24, 5, 10, 3, 1, 34.90, 0),
(21, 45, 6, 1, 4, 1, 89.90, 0),
(22, 45, 7, 3, 5, 1, 59.90, 0),
(23, 46, 8, 5, 1, 2, 120.00, 10),
(24, 46, 9, 7, 2, 1, 29.90, 0),
(25, 47, 10, 9, 3, 3, 39.90, 0),
(26, 47, 1, 11, 4, 1, 89.90, 0),
(27, 48, 2, 13, 5, 1, 69.90, 5),
(28, 48, 3, 15, 1, 1, 129.90, 0),
(29, 49, 4, 2, 2, 2, 49.90, 0),
(30, 49, 5, 4, 3, 1, 149.90, 15),
(31, 50, 6, 6, 4, 1, 69.90, 0),
(32, 50, 7, 8, 5, 2, 79.90, 0),
(33, 60, 8, 10, 1, 1, 34.90, 0),
(34, 60, 9, 12, 2, 1, 79.90, 10),
(35, 61, 10, 14, 3, 1, 199.90, 20),
(36, 61, 1, 1, 4, 2, 89.90, 0),
(37, 62, 2, 3, 5, 1, 59.90, 0),
(38, 62, 3, 5, 1, 1, 120.00, 0),
(39, 63, 4, 7, 2, 3, 29.90, 0),
(40, 63, 5, 9, 3, 1, 39.90, 0),
(41, 75, 6, 11, 4, 1, 89.90, 0),
(42, 75, 7, 13, 5, 2, 69.90, 0),
(43, 76, 8, 15, 1, 1, 129.90, 5),
(44, 76, 9, 2, 2, 1, 49.90, 0),
(45, 77, 10, 4, 3, 1, 149.90, 0),
(46, 77, 1, 6, 4, 2, 69.90, 0),
(47, 78, 2, 8, 5, 1, 79.90, 10),
(48, 78, 3, 10, 1, 2, 34.90, 0),
(49, 79, 4, 12, 2, 1, 79.90, 0),
(50, 79, 5, 14, 3, 1, 199.90, 15);

-- COMENZAMOS LAS CONSULTAS OLAP
-- Identificacion de dimensiones 
SELECT * FROM Productos;
SELECT * FROM Tiendas;
SELECT * FROM Clientes;
SELECT * FROM Tiempo;

-- KPIS
-- Ventas totaless
SELECT sum(cantidad * precio_unitario) as Ingresos_Totales from Ventas;

-- Ticket promedio
SELECT COUNT(*) as total_transacciones, 
SUM(cantidad * precio_unitario) as IngresoTotal, 
ROUND(SUM(cantidad *  precio_unitario)/count(*), 2) as ticket_Promedio from Ventas;


-- ventas por categoría
select p.categoria, SUM(v.cantidad * v.precio_unitario) as Ingresos from Ventas v 
join Productos p on v.id_producto = p.id_producto group by p.categoria;

-- con porcentaje
-- calculamos
select p.categoria, SUM(v.cantidad * v.precio_unitario) as Ingresos,
round(SUM(v.cantidad * v.precio_unitario)/ (select sum(cantidad * precio_unitario) from ventas)*100,2) as Porcentaje
from Ventas v join Productos p on v.id_producto = p.id_producto 
group by p.categoria
order by Ingresos desc;

-- ventas por marcas
SELECT 
    p.marca,
    SUM(v.cantidad * v.precio_unitario) AS Ingresos
FROM Ventas v
JOIN Productos p 
    ON v.id_producto = p.id_producto
GROUP BY p.marca
ORDER BY Ingresos DESC;

-- ventas por marcas con porcentaje
SELECT 
    p.marca,
    SUM(v.cantidad * v.precio_unitario) AS Ingresos,
    ROUND(
        SUM(v.cantidad * v.precio_unitario) * 100.0 /
        (SELECT SUM(cantidad * precio_unitario) FROM Ventas),
        2
    ) AS Porcentaje
FROM Ventas v
JOIN Productos p 
    ON v.id_producto = p.id_producto
GROUP BY p.marca
ORDER BY Ingresos DESC;