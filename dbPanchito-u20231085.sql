-- u20231085
CREATE DATABASE PanchitoTech;
USE PanchitoTech;
CREATE TABLE Clientes (
    id_cliente INT PRIMARY KEY,
    nombre VARCHAR(100),
    ciudad VARCHAR(50),
    fecha_registro DATE
);
INSERT INTO Clientes VALUES
(1, 'Carlos Martínez', 'San Salvador', '2025-01-10'),
(2, 'Ana López', 'Santa Ana', '2025-02-15'),
(3, 'Luis Hernández', 'San Miguel', '2025-03-20'),
(4, 'María González', 'San Salvador', '2025-04-05'),
(5, 'Pedro Ramírez', 'La Libertad', '2025-05-18');
CREATE TABLE Productos (
    id_producto INT PRIMARY KEY,
    nombre VARCHAR(100),
    categoria VARCHAR(50),
    precio DECIMAL(10,2)
);
INSERT INTO Productos VALUES
(1, 'Laptop HP', 'Computadoras', 850.00),
(2, 'Laptop Dell', 'Computadoras', 900.00),
(3, 'Mouse Inalámbrico', 'Accesorios', 25.00),
(4, 'Teclado Mecánico', 'Accesorios', 70.00),
(5, 'Monitor 24"', 'Monitores', 180.00),
(6, 'Celular Samsung', 'Celulares', 650.00);
CREATE TABLE Vendedores (
    id_vendedor INT PRIMARY KEY,
    nombre VARCHAR(100)
);
INSERT INTO Vendedores VALUES
(1, 'Juan Pérez'),
(2, 'Laura Gómez'),
(3, 'Ricardo Flores');
CREATE TABLE Ventas (
    id_venta INT PRIMARY KEY,
    fecha DATE,
    id_cliente INT,
    id_vendedor INT,
    total DECIMAL(10,2),
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
    FOREIGN KEY (id_vendedor) REFERENCES Vendedores(id_vendedor)
);
INSERT INTO Ventas VALUES
(1, '2023-06-01', 1, 1, 875.00),
(2, '2023-06-05', 2, 2, 950.00),
(3, '2023-07-10', 3, 1, 720.00),
(4, '2023-07-15', 4, 3, 180.00),
(5, '2023-08-02', 5, 2, 925.00),
(6, '2023-08-20', 1, 1, 650.00),
(7, '2023-09-01', 2, 3, 110.00),
(8, '2023-09-18', 3, 2, 180.00);
CREATE TABLE Detalle_Venta (
    id_detalle INT PRIMARY KEY,
    id_venta INT,
    id_producto INT,
    cantidad INT,
    subtotal DECIMAL(10,2),
    FOREIGN KEY (id_venta) REFERENCES Ventas(id_venta),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
);
INSERT INTO Detalle_Venta VALUES
(1, 1, 1, 1, 850.00),
(2, 1, 3, 1, 25.00),

(3, 2, 2, 1, 900.00),
(4, 2, 3, 2, 50.00),

(5, 3, 6, 1, 650.00),
(6, 3, 3, 2, 50.00),
(7, 3, 4, 1, 20.00),

(8, 4, 5, 1, 180.00),

(9, 5, 2, 1, 900.00),
(10, 5, 4, 1, 25.00),

(11, 6, 6, 1, 650.00),

(12, 7, 4, 1, 70.00),
(13, 7, 3, 2, 40.00),

(14, 8, 5, 1, 180.00);


SELECT * FROM Clientes;
SELECT * FROM Productos;
SELECT * FROM Ventas;
SELECT * FROM Detalle_Venta;

-- actividad:
-- Ventas totales:
select SUM(total) AS venta_Totales FROM Ventas;

-- Ventas por mes
SELECT MONTH(fecha), SUM(total) from Ventas GROUP BY MONTH(fecha);
SELECT MONTH(fecha) AS mes, SUM(total) AS ventas_totales FROM Ventas GROUP BY MONTH(fecha) ORDER BY mes;

SELECT DATENAME(MONTH, fecha) AS mes, SUM(total) AS Venta_Total FROM Ventas GROUP BY MONTH(fecha), MONTH(fecha) ORDER BY MONTH(fecha);

-- arreglado
SELECT DATENAME(MONTH, fecha) AS mes, SUM(total) AS Venta_Total FROM Ventas 
GROUP BY MONTH(fecha), DATENAME(MONTH, fecha) ORDER BY MONTH(fecha);




--      // Inicio de la tarea //

-- Top 10 de productos más vendidos
SELECT TOP 10
       P.nombre AS Producto,
       SUM(DV.cantidad) AS Cantidad_Vendida
FROM Detalle_Venta DV JOIN Productos P ON DV.id_producto = P.id_producto 
GROUP BY P.nombre ORDER BY Cantidad_Vendida DESC;

-- ¿Quién es el vendedor estrella?
SELECT V.nombre AS Vendedor, SUM(VE.total) AS Total_Vendido
	FROM Ventas VE JOIN Vendedores V ON VE.id_vendedor = V.id_vendedor
	GROUP BY V.nombre ORDER BY Total_Vendido DESC;

-- Cliente estrella
SELECT C.nombre AS Cliente,
       SUM(V.total) AS Total_Comprado
FROM Ventas V JOIN Clientes C ON V.id_cliente = C.id_cliente
GROUP BY C.nombre ORDER BY Total_Comprado DESC;

-- ¿Qué categoría es más rentable?
SELECT P.categoria, SUM(DV.subtotal) AS Total_Ganado FROM Detalle_Venta DV 
JOIN Productos P ON DV.id_producto = P.id_producto 
GROUP BY P.categoria ORDER BY Total_Ganado DESC;

-- DESAFIO Consulta Maestro–Detalle es decir Venta completa
SELECT C.nombre AS Cliente, VEND.nombre AS Vendedor, P.nombre AS Producto,
       DV.subtotal AS Monto_Total FROM Ventas V
JOIN Clientes C ON V.id_cliente = C.id_cliente
JOIN Vendedores VEND ON V.id_vendedor = VEND.id_vendedor
JOIN Detalle_Venta DV ON V.id_venta = DV.id_venta
JOIN Productos P ON DV.id_producto = P.id_producto;






--Adicional (tarea en grupo)
--¿Qué meses tienen picos de demanda?
SELECT DATENAME(MONTH, fecha) AS Mes, SUM(total) AS Venta_Total FROM Ventas 
	GROUP BY DATENAME(MONTH, fecha), MONTH(fecha) ORDER BY MONTH(fecha);

--¿Qué productos están “estancados”?
SELECT P.nombre AS Producto, SUM(DV.cantidad) AS Total_Vendido FROM Detalle_Venta DV
	JOIN Productos P ON DV.id_producto = P.id_producto GROUP BY P.nombre ORDER BY Total_Vendido ASC;

