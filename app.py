import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ================= CONFIGURACIÓN GOOGLE SHEETS =================
try:
    cred_json = st.secrets["google"]["credentials"]
    creds_dict = json.loads(cred_json)

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    sheet_name = "ML-RG-0040 Registro de Quejas y Sugerencias"
    sheet = client.open(sheet_name).sheet1
except Exception as e:
    st.error(f"❌ Error al conectar con Google Sheets: {e}")
    st.stop()

# ================= INTERFAZ STREAMLIT =================
st.set_page_config(page_title="ML-RG-0037 Formulario de Quejas y Sugerencias", page_icon=":memo:", layout="centered")

st.image("logo.png", width=150)
st.title("ML-RG-0037 Formulario de Quejas y Sugerencias")
st.markdown("---")

# Fecha y hora automática
fecha = st.date_input("Fecha", datetime.now().date())
hora = st.time_input("Hora", datetime.now().time())
tipo_cliente = st.selectbox("Tipo de cliente", ["Externo", "Interno"])

# Nombre/Área dinámico
if tipo_cliente == "Externo":
    nombre_area = st.text_input("Nombre del Cliente o Área")
else:
    nombre_area = st.selectbox("Nombre del Cliente o Área", ["Producción", "Calidad"])

tipo_reporte = st.selectbox("Tipo de reporte", ["Queja", "Sugerencia"])
descripcion = st.text_area("Descripción o detalle", height=150)

# ================= ENVÍO =================
if st.button("📤 Enviar registro"):
    if not nombre or not detalle:
        st.warning("⚠️ Por favor complete todos los campos obligatorios antes de enviar.")
    elif not confirmar:
        st.info("☑️ Debe confirmar que la información ingresada es correcta antes de enviar.")
    else:
        try:
            registros = sheet.get_all_records()
            numero = len(registros) + 1

            fila = [numero, fecha, tipo, nombre, detalle]

            sheet.append_row(fila)
            st.success(f"✅ Registro enviado con éxito. Número de solicitud: **{numero}**")
            st.balloons()
        except Exception as e:

            st.error(f"❌ Ocurrió un error al guardar en Google Sheets: {e}")
