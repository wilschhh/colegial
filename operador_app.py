import streamlit as st
import sqlite3

st.title("Panel del Operador - Control de Pagos")

def obtener_datos_por_cedula(cedula):
    conn = sqlite3.connect("estudiantes.db")
    c = conn.cursor()

    c.execute("SELECT * FROM estudiantes WHERE cedula = ?", (cedula,))
    estudiante = c.fetchone()

    c.execute("SELECT * FROM pagos WHERE cedula_estudiante = ?", (cedula,))
    pagos = c.fetchone()

    conn.close()
    return estudiante, pagos

cedula = st.text_input("Buscar estudiante por cédula")

if st.button("Buscar"):
    estudiante, pagos = obtener_datos_por_cedula(cedula)

    if estudiante:
        st.subheader("Datos del Estudiante")
        etiquetas = ["Cédula", "Nombre", "Fecha Nac.", "Edad", "Dirección", "Escuela", "Grado", "Sangre", "Alergias"]
        for label, dato in zip(etiquetas, estudiante):
            st.write(f"**{label}:** {dato}")

        if pagos:
            st.subheader("Información de Pago")
            st.write(f"**Seguro anual:** ${pagos[2]:.2f}")
            st.write(f"**Total del contrato:** ${pagos[3]:.2f}")
            st.write(f"**Pago mensual:** ${pagos[4]:.2f}")
        else:
            st.warning("No hay información de pagos registrada para este estudiante.")
    else:
        st.error("Estudiante no encontrado.")
