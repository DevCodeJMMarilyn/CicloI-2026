USE PanchitoBilingue;
GO

/* =========================================
ELIMINAR TABLAS SI YA EXISTEN
========================================= */

IF OBJECT_ID('Fact_Pagos','U') IS NOT NULL DROP TABLE Fact_Pagos;
IF OBJECT_ID('Dim_Tiempo','U') IS NOT NULL DROP TABLE Dim_Tiempo;
IF OBJECT_ID('Dim_Grados','U') IS NOT NULL DROP TABLE Dim_Grados;
IF OBJECT_ID('Dim_Ciudades','U') IS NOT NULL DROP TABLE Dim_Ciudades;
IF OBJECT_ID('Dim_Estudiantes','U') IS NOT NULL DROP TABLE Dim_Estudiantes;
GO

/* =========================================
TABLAS DIMENSION
========================================= */

CREATE TABLE Dim_Estudiantes(
id_estudiante INT PRIMARY KEY,
nombre VARCHAR(50),
edad INT
);

CREATE TABLE Dim_Ciudades(
id_ciudad INT PRIMARY KEY,
ciudad VARCHAR(50)
);

CREATE TABLE Dim_Grados(
id_grado INT PRIMARY KEY,
grado VARCHAR(30)
);

CREATE TABLE Dim_Tiempo(
id_tiempo INT IDENTITY(1,1) PRIMARY KEY,
mes VARCHAR(20),
anio INT
);

/* =========================================
TABLA DE HECHOS
========================================= */

CREATE TABLE Fact_Pagos(
id_pago INT PRIMARY KEY,
id_estudiante INT,
id_grado INT,
id_ciudad INT,
id_tiempo INT,
monto DECIMAL(10,2),

FOREIGN KEY (id_estudiante) REFERENCES Dim_Estudiantes(id_estudiante),
FOREIGN KEY (id_grado) REFERENCES Dim_Grados(id_grado),
FOREIGN KEY (id_ciudad) REFERENCES Dim_Ciudades(id_ciudad),
FOREIGN KEY (id_tiempo) REFERENCES Dim_Tiempo(id_tiempo)
);

/* =========================================
CARGA DE DIMENSIONES
========================================= */

INSERT INTO Dim_Estudiantes
SELECT id_estudiante, nombre, edad
FROM Estudiantes;

INSERT INTO Dim_Ciudades
SELECT id_ciudad, ciudad
FROM Ciudades;

INSERT INTO Dim_Grados
SELECT id_grado, grado
FROM Grados;

INSERT INTO Dim_Tiempo(mes,anio)
SELECT DISTINCT mes,anio
FROM Pagos;

/* =========================================
CARGA DE TABLA DE HECHOS
========================================= */

INSERT INTO Fact_Pagos
SELECT
p.id_pago,
p.id_estudiante,
i.id_grado,
e.id_ciudad,
t.id_tiempo,
p.monto
FROM Pagos p
JOIN Estudiantes e
ON p.id_estudiante = e.id_estudiante
JOIN Inscripciones i
ON p.id_estudiante = i.id_estudiante
JOIN Dim_Tiempo t
ON p.mes = t.mes AND p.anio = t.anio;

/* =========================================
CONSULTAS BI (DESDE TABLA DE HECHOS)
========================================= */

-- TOTAL DE ESTUDIANTES
SELECT COUNT(DISTINCT id_estudiante) AS total_estudiantes
FROM Fact_Pagos;

-- ESTUDIANTES POR CIUDAD
SELECT c.ciudad,
COUNT(DISTINCT f.id_estudiante) AS estudiantes
FROM Fact_Pagos f
JOIN Dim_Ciudades c
ON f.id_ciudad = c.id_ciudad
GROUP BY c.ciudad;

-- ESTUDIANTES DE USULUTAN
SELECT COUNT(DISTINCT f.id_estudiante) AS estudiantes_usulutan
FROM Fact_Pagos f
JOIN Dim_Ciudades c
ON f.id_ciudad = c.id_ciudad
WHERE c.ciudad = 'Usulutan';

-- INGRESOS POR MES
SELECT t.mes,
SUM(f.monto) AS ingresos
FROM Fact_Pagos f
JOIN Dim_Tiempo t
ON f.id_tiempo = t.id_tiempo
GROUP BY t.mes
ORDER BY t.mes;

-- DISTRIBUCION POR GRADO
SELECT g.grado,
COUNT(DISTINCT f.id_estudiante) AS estudiantes
FROM Fact_Pagos f
JOIN Dim_Grados g
ON f.id_grado = g.id_grado
GROUP BY g.grado;

-- ANALISIS COMPLETO BI
SELECT
c.ciudad,
g.grado,
t.mes,
COUNT(DISTINCT f.id_estudiante) AS estudiantes,
SUM(f.monto) AS ingresos
FROM Fact_Pagos f
JOIN Dim_Ciudades c ON f.id_ciudad = c.id_ciudad
JOIN Dim_Grados g ON f.id_grado = g.id_grado
JOIN Dim_Tiempo t ON f.id_tiempo = t.id_tiempo
GROUP BY c.ciudad,g.grado,t.mes
ORDER BY c.ciudad;

