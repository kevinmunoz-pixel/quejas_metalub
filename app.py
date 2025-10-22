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
st.set_page_config(page_title="Registro de Quejas y Sugerencias", page_icon="📝")
st.title("📝 Registro de Quejas y Sugerencias")
st.write("Por favor complete el siguiente formulario para registrar su queja o sugerencia.")

# Fecha automática
fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.write(f"📅 Fecha y hora: **{fecha}**")

# Tipo de cliente
tipo = st.radio("Seleccione el tipo de registro:", ["Externo", "Interno"])

# Campo dinámico según tipo
if tipo == "Externo":
    nombre = st.text_input("Nombre del cliente o empresa")
else:
    nombre = st.selectbox("Área interna", ["Producción", "Calidad", "Mantenimiento", "Laboratorio", "Administración"])

# Detalle de la queja o sugerencia
detalle = st.text_area("Describa brevemente la queja o sugerencia:")

# Confirmación
confirmar = st.checkbox("Confirmo que la información ingresada es correcta")

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


