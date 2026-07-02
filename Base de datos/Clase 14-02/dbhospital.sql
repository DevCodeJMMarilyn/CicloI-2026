-- Lab 1 U20231085
CREATE DATABASE HospitalBI;
USE HospitalBI;
CREATE TABLE Pacientes (
    id_paciente INT PRIMARY KEY,
    nombre VARCHAR(100),
    edad INT,
    genero VARCHAR(10),
    ciudad VARCHAR(100)
);
CREATE TABLE Doctores (
    id_doctor INT PRIMARY KEY,
    nombre VARCHAR(100),
    especialidad VARCHAR(100)
);
CREATE TABLE Consultas (
    id_consulta INT PRIMARY KEY,
    fecha DATE,
    id_paciente INT,
    id_doctor INT,
    costo DECIMAL(10,2),
    FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente),
    FOREIGN KEY (id_doctor) REFERENCES Doctores(id_doctor)
);
CREATE TABLE Diagnosticos (
    id_diagnostico INT PRIMARY KEY,
    id_consulta INT,
    enfermedad VARCHAR(100),
    FOREIGN KEY (id_consulta) REFERENCES Consultas(id_consulta)
);
INSERT INTO Pacientes VALUES
(1,'Juan Perez',30,'M','San Salvador'),
(2,'Maria Lopez',25,'F','Santa Ana'),
(3,'Carlos Ruiz',40,'M','San Miguel'),
(4,'Ana Torres',35,'F','La Libertad'),
(5,'Luis Gomez',50,'M','San Salvador');
INSERT INTO Doctores VALUES
(1,'Dr. Hernandez','Cardiologia'),
(2,'Dra. Martinez','Pediatria'),
(3,'Dr. Lopez','Medicina General'),
(4,'Dra. Ramos','Dermatologia');
INSERT INTO Consultas VALUES
(1,'2025-01-10',1,3,25),
(2,'2025-01-12',2,2,30),
(3,'2025-01-15',3,1,50),
(4,'2025-02-01',4,4,40),
(5,'2025-02-05',5,1,50),
(6,'2025-02-10',1,3,25),
(7,'2025-03-01',2,2,30),
(8,'2025-03-03',3,1,50);
INSERT INTO Diagnosticos VALUES
(1,1,'Gripe'),
(2,2,'Control niño sano'),
(3,3,'Hipertension'),
(4,4,'Dermatitis'),
(5,5,'Arritmia'),
(6,6,'Gripe'),
(7,7,'Vacunacion'),
(8,8,'Hipertension');

-- Inicio del lab
USE HospitalBI;
-- KPI 1: INGRESOS TOTALES
-- Calcular cuánto dinero ha generado el hospital en total
SELECT 
    SUM(costo) AS ingresos_totales
FROM Consultas;


-- KPI 2: RENTABILIDAD MENSUAL
-- Determinar cuánto se generó en cada mes 
SELECT 
    MONTH(fecha) AS mes,
    SUM(costo) AS ingresos_mensuales
FROM Consultas
GROUP BY MONTH(fecha)
ORDER BY mes;

-- KPI 3: CONSULTAS POR ESPECIALIDAD
-- Identificar qué área médica tiene mayor demanda 
SELECT 
    d.especialidad,
    COUNT(c.id_consulta) AS total_consultas
FROM Consultas c
INNER JOIN Doctores d 
    ON c.id_doctor = d.id_doctor
GROUP BY d.especialidad
ORDER BY total_consultas DESC;

-- KPI 4: RANKING DE DOCTORES
-- Identificar qué doctor genera más ingresos
SELECT 
    d.nombre,
    COUNT(c.id_consulta) AS total_consultas,
    SUM(c.costo) AS ingresos_generados
FROM Consultas c
INNER JOIN Doctores d 
    ON c.id_doctor = d.id_doctor
GROUP BY d.nombre
ORDER BY ingresos_generados DESC;

-- KPI 5: FRECUENCIA PATOLÓGICA
-- Detectar las enfermedades más diagnosticadas
SELECT 
    enfermedad,
    COUNT(*) AS frecuencia
FROM Diagnosticos
GROUP BY enfermedad
ORDER BY frecuencia DESC;

-- KPI 6: TICKET PROMEDIO
-- Calcular el ingreso promedio por consulta
SELECT 
    AVG(costo) AS ticket_promedio
FROM Consultas;

-- KPI 7: RECURRENCIA DE PACIENTES
-- Identificar qué pacientes visitan más el hospital
SELECT 
    p.nombre,
    COUNT(c.id_consulta) AS total_visitas
FROM Consultas c
INNER JOIN Pacientes p 
    ON c.id_paciente = p.id_paciente
GROUP BY p.nombre
ORDER BY total_visitas DESC;

-- KPI 8: INGRESOS POR CIUDAD
-- Analizar de qué ciudad provienen más ingresos
SELECT 
    p.ciudad,
    SUM(c.costo) AS ingresos_ciudad
FROM Consultas c
INNER JOIN Pacientes p 
    ON c.id_paciente = p.id_paciente
GROUP BY p.ciudad
ORDER BY ingresos_ciudad DESC;
