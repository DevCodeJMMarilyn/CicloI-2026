import sqlite3
import random
from datetime import datetime, timedelta

# Crear base de datos
conn = sqlite3.connect('ventas.db')
cursor = conn.cursor()

# Crear tabla Productos
cursor.execute('''
CREATE TABLE IF NOT EXISTS Productos (
    id_producto INTEGER PRIMARY KEY,
    nombre TEXT,
    categoria TEXT
)
''')

# Crear tabla Ventas
cursor.execute('''
CREATE TABLE IF NOT EXISTS Ventas (
    id_venta INTEGER PRIMARY KEY,
    id_producto INTEGER,
    fecha DATE,
    total_venta REAL,
    cantidad INTEGER,
    FOREIGN KEY (id_producto) REFERENCES Productos (id_producto)
)
''')

# Datos de productos
productos = [
    (1, 'Laptop', 'Tecnología'),
    (2, 'Camisa', 'Ropa'),
    (3, 'Sofá', 'Hogar'),
    (4, 'Arroz', 'Alimentación'),
    (5, 'Smartphone', 'Tecnología'),
    (6, 'Pantalón', 'Ropa'),
    (7, 'Mesa', 'Hogar'),
    (8, 'Pasta', 'Alimentación'),
    (9, 'Tablet', 'Tecnología'),
    (10, 'Zapatos', 'Ropa')
]

cursor.executemany('INSERT OR IGNORE INTO Productos VALUES (?, ?, ?)', productos)

# Generar ventas aleatorias
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
ventas = []

for i in range(1, 1001):
    id_prod = random.randint(1, 10)
    fecha = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    cantidad = random.randint(1, 5)
    precio_unit = random.uniform(10, 500)
    total = cantidad * precio_unit
    ventas.append((i, id_prod, fecha.date(), round(total, 2), cantidad))

cursor.executemany('INSERT OR IGNORE INTO Ventas VALUES (?, ?, ?, ?, ?)', ventas)

conn.commit()
conn.close()

print("Base de datos creada con datos de ejemplo.")