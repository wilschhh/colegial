import streamlit as st
import sqlite3
from datetime import datetime

# Conectar a la base de datos (se crea si no existe)
conn = sqlite3.connect("estudiantes.db")
cursor = conn.cursor()

# Crear tabla de estudiantes
cursor.execute("""
CREATE TABLE IF NOT EXISTS estudiantes (
    cedula TEXT PRIMARY KEY,
    nombre TEXT,
    fecha_nac TEXT,
    edad INTEGER,
    direccion TEXT,
    escuela TEXT,
    grado TEXT,
    sangre TEXT,
    alergias TEXT
)
""")

# Crear tabla de acudientes
cursor.execute("""
CREATE TABLE IF NOT EXISTS acudientes (
    cedula_estudiante TEXT,
    nombre TEXT,
    contacto TEXT,
    correo TEXT,
    parentesco TEXT,
    FOREIGN KEY (cedula_estudiante) REFERENCES estudiantes(cedula)
)
""")

# Crear tabla de pagos
cursor.execute("""
CREATE TABLE IF NOT EXISTS pagos (
    cedula_estudiante TEXT,
    seguro_anual REAL,
    total_contrato REAL,
    mensualidad REAL,
    FOREIGN KEY (cedula_estudiante) REFERENCES estudiantes(cedula)
)
""")

conn.commit()

# Función para calcular edad
def calcular_edad(fecha_nac):
    nacimiento = datetime.strptime(fecha_nac, "%Y-%m-%d")
    hoy = datetime.today()
    return hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))

# Función para guardar datos
def guardar_datos(cedula, nombre, fecha_nac, direccion, escuela, grado, sangre, alergias,
                  acudiente_nombre, contacto, correo, parentesco,
                  seguro_anual, total_contrato, mensualidad):
    edad = calcular_edad(fecha_nac)
    
    cursor.execute("INSERT INTO estudiantes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (
        cedula, nombre, fecha_nac, edad, direccion, escuela, grado, sangre, alergias
    ))
    
    cursor.execute("INSERT INTO acudientes VALUES (?, ?, ?, ?, ?)", (
        cedula, acudiente_nombre, contacto, correo, parentesco
    ))
    
    cursor.execute("INSERT INTO pagos VALUES (?, ?, ?, ?)", (
        cedula, seguro_anual, total_contrato, mensualidad
    ))
    
    conn.commit()

# Título
st.title("Registro de Estudiantes - Admin")

# --- Datos del Estudiante ---
st.header("Datos del Estudiante")
cedula = st.text_input("Cédula del estudiante (sin guiones)").replace("-", "")
nombre = st.text_input("Nombre completo")
fecha_nac = st.date_input("Fecha de nacimiento", format="YYYY-MM-DD")
direccion = st.text_input("Dirección")
escuela = st.text_input("Escuela")
grado = st.text_input("Grado")
sangre = st.text_input("Tipo de sangre")
alergias = st.text_input("Alergias o enfermedades")

# --- Datos del Acudiente ---
st.header("Datos del Acudiente")
acudiente_nombre = st.text_input("Nombre completo del acudiente")
contacto = st.text_input("Número de contacto")
correo = st.text_input("Correo electrónico")
parentesco = st.text_input("Parentesco")

# --- Información de Pago ---
st.header("Información de Pago")
seguro_anual = st.number_input("Seguro anual ($)", min_value=0.0, step=10.0)
total_contrato = st.number_input("Total del contrato ($)", min_value=0.0, step=10.0)
mensualidad = st.number_input("Pago en mensualidad ($)", min_value=0.0, step=10.0)

# Botón de Guardar
if st.button("Guardar"):
    try:
        guardar_datos(cedula, nombre, fecha_nac.strftime("%Y-%m-%d"), direccion, escuela, grado, sangre, alergias,
                      acudiente_nombre, contacto, correo, parentesco,
                      seguro_anual, total_contrato, mensualidad)
        st.success("✅ Datos guardados correctamente.")
    except sqlite3.IntegrityError:
        st.error("❌ Ya existe un estudiante registrado con esa cédula.")
    except Exception as e:
        st.error(f"❌ Error al guardar: {e}")
