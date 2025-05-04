import streamlit as st
import sqlite3
from datetime import datetime

st.title("Registro de Estudiantes - Administrador")

def calcular_edad(fecha_nacimiento):
    hoy = datetime.today()
    nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    return hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))

def guardar_datos(cedula, nombre, fecha_nac, direccion, escuela, grado, sangre, alergias,
                  acudiente_nombre, contacto, correo, parentesco,
                  seguro_anual, total_contrato, pago_mensual):
    
    edad = calcular_edad(fecha_nac)
    conn = sqlite3.connect("estudiantes.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO estudiantes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (cedula, nombre, fecha_nac, edad, direccion, escuela, grado, sangre, alergias))

    cursor.execute("INSERT INTO acudientes (cedula_estudiante, nombre, contacto, correo, parentesco) VALUES (?, ?, ?, ?, ?)",
                   (cedula, acudiente_nombre, contacto, correo, parentesco))

    cursor.execute("INSERT INTO pagos (cedula_estudiante, seguro_anual, total_contrato, pago_mensual) VALUES (?, ?, ?, ?)",
                   (cedula, seguro_anual, total_contrato, pago_mensual))

    conn.commit()
    conn.close()
    st.success("Estudiante registrado correctamente")

with st.form("formulario"):
    st.header("Datos del Estudiante")
    cedula = st.text_input("Cédula")
    nombre = st.text_input("Nombre completo")
    fecha_nac = st.date_input("Fecha de nacimiento").strftime("%Y-%m-%d")
    direccion = st.text_input("Dirección")
    escuela = st.text_input("Escuela")
    grado = st.text_input("Grado")
    sangre = st.text_input("Tipo de sangre")
    alergias = st.text_input("Alergias o enfermedades")

    st.header("Datos del Acudiente")
    acudiente_nombre = st.text_input("Nombre completo del acudiente")
    contacto = st.text_input("Número de contacto")
    correo = st.text_input("Correo electrónico")
    parentesco = st.text_input("Parentesco")

    st.header("Información de Pago")
    seguro_anual = st.number_input("Seguro anual", min_value=0.0)
    total_contrato = st.number_input("Total del contrato", min_value=0.0)
    pago_mensual = st.number_input("Pago mensual", min_value=0.0)

    submit = st.form_submit_button("Guardar")

    if submit:
        guardar_datos(cedula, nombre, fecha_nac, direccion, escuela, grado, sangre, alergias,
                      acudiente_nombre, contacto, correo, parentesco,
                      seguro_anual, total_contrato, pago_mensual)
