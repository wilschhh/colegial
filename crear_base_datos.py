import sqlite3

conn = sqlite3.connect("estudiantes.db")
cursor = conn.cursor()

# Tabla de estudiantes
cursor.execute("""
CREATE TABLE IF NOT EXISTS estudiantes (
    cedula TEXT PRIMARY KEY,
    nombre TEXT,
    fecha_nacimiento TEXT,
    edad INTEGER,
    direccion TEXT,
    escuela TEXT,
    grado TEXT,
    tipo_sangre TEXT,
    alergias TEXT
)
""")

# Tabla de acudientes
cursor.execute("""
CREATE TABLE IF NOT EXISTS acudientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cedula_estudiante TEXT,
    nombre TEXT,
    contacto TEXT,
    correo TEXT,
    parentesco TEXT,
    FOREIGN KEY (cedula_estudiante) REFERENCES estudiantes(cedula)
)
""")

# Tabla de pagos
cursor.execute("""
CREATE TABLE IF NOT EXISTS pagos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cedula_estudiante TEXT,
    seguro_anual REAL,
    total_contrato REAL,
    pago_mensual REAL,
    FOREIGN KEY (cedula_estudiante) REFERENCES estudiantes(cedula)
)
""")

conn.commit()
conn.close()

print("Base de datos creada con éxito.")
