# app.py
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# -----------------------------
# CONFIGURACIÓN DEL GOOGLE SHEET
# -----------------------------
# Ruta absoluta a tu archivo de credenciales
cred_path = r"C:\Users\kevin\OneDrive\Documentos\QuejasApp\credenciales.json"

# Permisos necesarios
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Autenticación
creds = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope)
client = gspread.authorize(creds)

# Abrir Google Sheet
sheet_name = "ML-RG-0040 Registro de Quejas y Sugerencias"
sheet = client.open(sheet_name).sheet1

# -----------------------------
# STREAMLIT FORMULARIO
# -----------------------------
st.set_page_config(page_title="ML-RG-0037 Formulario de Quejas y Sugerencias", page_icon=":memo:", layout="centered")

st.image("logo.png", width=150)
st.title("ML-RG-0037 Formulario de Quejas y Sugerencias")
st.markdown("---")

# Fecha y hora automática
fecha = datetime.now().strftime("%Y-%m-%d")
hora = datetime.now().strftime("%H:%M:%S")

# Tipo de cliente
tipo_cliente = st.selectbox("Tipo de Cliente", ["Externo", "Interno"])

# Nombre o Área según tipo
if tipo_cliente == "Externo":
    nombre_area = st.text_input("Nombre del Cliente o Área")
else:
    nombre_area = st.selectbox("Nombre del Cliente o Área", ["Producción", "Calidad"])

# Queja y sugerencia
queja = st.text_area("Queja")
sugerencia = st.text_area("Sugerencia")

# Botón para enviar
if st.button("Enviar"):
    if nombre_area.strip() == "" or queja.strip() == "":
        st.error("Por favor completa todos los campos requeridos.")
    else:
        try:
            # Agregar fila al Google Sheet
            fila = [fecha, hora, tipo_cliente, nombre_area, queja, sugerencia]
            sheet.append_row(fila)
            st.success("✅ Respuesta registrada correctamente.")
        except Exception as e:
            st.error(f"❌ Ha ocurrido un error al enviar los datos: {e}")
