-- Tarea Practica BI PanchitoDB U20231085
USE PanchitoTech;
-- PARTE A
-- Creamos una tabla para análisis de clientes
-- Esta tabla resume el comportamiento de compra

CREATE TABLE Analisis_Clientes (
    id_cliente INT,
    nombre_cliente VARCHAR(100),
    total_compras INT,
    total_gastado DECIMAL(10,2),
    ticket_promedio DECIMAL(10,2)
);

-- Insertamos datos calculados en la tabla analítica
INSERT INTO Analisis_Clientes
SELECT 
    C.id_cliente,
    C.nombre,
    
    -- Contamos cuántas compras hizo cada cliente
    COUNT(V.id_venta) AS total_compras,
    
    -- Sumamos todo lo que gastó
    SUM(V.total) AS total_gastado,
    
    -- Calculamos el promedio de gasto por compra
    SUM(V.total) / COUNT(V.id_venta) AS ticket_promedio

FROM Clientes C
JOIN Ventas V ON C.id_cliente = V.id_cliente
-- Agrupamos por cliente
GROUP BY C.id_cliente, C.nombre;

-- Mostramos la tabla final
SELECT * FROM Analisis_Clientes;


-- PARTE B 
-- Clientes ordenados por frecuencia de compra
SELECT *
FROM Analisis_Clientes
ORDER BY total_compras DESC;

-- Clientes que gastan más que el promedio
SELECT *
FROM Analisis_Clientes
WHERE total_gastado > (
    SELECT AVG(total_gastado)
    FROM Analisis_Clientes
);

-- Clientes ocasionales
SELECT *
FROM Analisis_Clientes
WHERE total_compras = 1
AND total_gastado < 200;


-- PARTE C 
-- Clasificación de clientes
SELECT 
    *,
    CASE
        WHEN total_gastado > 800 THEN 'Premium'
        WHEN total_compras > 2 THEN 'Frecuente'
        WHEN total_compras = 1 THEN 'Ocasional'
        ELSE 'Regular'
    END AS tipo_cliente
FROM Analisis_Clientes;

-- Creamos una nueva tabla llamada Segmentacion_Clientes
-- Esta tabla guardará la clasificación de cada cliente
CREATE TABLE Segmentacion_Clientes AS
-- Seleccionamos todos los datos de la tabla analítica
SELECT 
    *,
    -- Creamos una nueva columna llamada tipo_cliente
    CASE
        -- Si el cliente gastó más de $800
        WHEN total_gastado > 800 THEN 'Premium'
        -- Si hizo más de 2 compras
        WHEN total_compras > 2 THEN 'Frecuente'
        -- Si solo compró una vez
        WHEN total_compras = 1 THEN 'Ocasional'
        -- Si no cumple ninguna condición
        ELSE 'Regular'
    END AS tipo_cliente

FROM Analisis_Clientes;
SELECT * FROM Analisis_Clientes;