import os
import json
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from io import StringIO

# -----------------------------
# LEER CREDENCIALES DESDE VARIABLE DE ENTORNO
# -----------------------------
cred_json = os.getenv("GOOGLE_CREDENTIALS")
if not cred_json:
    st.error("No se encontró la variable de entorno GOOGLE_CREDENTIALS")
    st.stop()

# Convertir la cadena JSON en objeto usable
creds_dict = json.loads(cred_json)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
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
            fila = [fecha, hora, tipo_cliente, nombre_area, queja, sugerencia]
            sheet.append_row(fila)
            st.success("✅ Respuesta registrada correctamente.")
        except Exception as e:
            st.error(f"❌ Ha ocurrido un error al enviar los datos: {e}")
