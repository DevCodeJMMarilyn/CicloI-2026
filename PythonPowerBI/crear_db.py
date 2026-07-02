import sqlite3

# Conectar a la base de datos (se crea automáticamente)
conn = sqlite3.connect("tienda.db")
cursor = conn.cursor()

# =========================================
# CREAR TABLAS
# =========================================

# Tabla de Productos
cursor.execute("""
CREATE TABLE IF NOT EXISTS Productos(
    id_producto INTEGER PRIMARY KEY,
    producto TEXT,
    categoria TEXT
)
""")

# Tabla de Ventas
cursor.execute("""
CREATE TABLE IF NOT EXISTS Ventas(
    id_venta INTEGER PRIMARY KEY,
    id_producto INTEGER,
    cantidad INTEGER,
    precio_unitario REAL,
    id_tiempo INTEGER
)
""")

# Tabla de Tiempo (dimensión temporal)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Tiempo(
    id_tiempo INTEGER PRIMARY KEY,
    mes INTEGER,
    mes_nombre TEXT
)
""")

# =========================================
# INSERTAR DATOS DE EJEMPLO
# =========================================

# Insertar productos
cursor.executemany("INSERT INTO Productos VALUES (?,?,?)", [
    (1, 'Laptop', 'Tecnologia'),
    (2, 'Mouse', 'Tecnologia'),
    (3, 'Camisa', 'Ropa'),
    (4, 'Zapatos', 'Calzado')
])

# Insertar dimensiones de tiempo
cursor.executemany("INSERT INTO Tiempo VALUES (?,?,?)", [
    (1, 1, 'Enero'),
    (2, 2, 'Febrero'),
    (3, 3, 'Marzo')
])

# Insertar ventas
cursor.executemany("INSERT INTO Ventas VALUES (?,?,?,?,?)", [
    (1, 1, 2, 800, 1),   # 2 laptops en Enero
    (2, 2, 5, 20, 1),    # 5 mouses en Enero
    (3, 3, 3, 25, 2),    # 3 camisas en Febrero
    (4, 4, 2, 50, 3),    # 2 zapatos en Marzo
    (5, 1, 1, 800, 2)    # 1 laptop en Febrero
])

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print(" Base de datos creada exitosamente!")