import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

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

    # 🔧 Validar encabezados automáticamente
    encabezados_correctos = [
        "No. Solicitud",
        "Fecha",
        "Hora",
        "Tipo de Cliente",
        "Nombre del Cliente o Área",
        "Tipo de Reporte",
        "Descripción"
    ]

    headers_actuales = sheet.row_values(1)
    if headers_actuales != encabezados_correctos:
        sheet.delete_rows(1)  # elimina encabezado incorrecto
        sheet.insert_row(encabezados_correctos, 1)

except Exception as e:
    st.error(f"❌ Error al conectar con Google Sheets: {e}")
    st.stop()

# ================= INTERFAZ STREAMLIT =================
st.set_page_config(
    page_title="ML-RG-0037 Formulario de Quejas y Sugerencias",
    page_icon=":memo:",
    layout="centered"
)

st.image("logo.png", width=150)
st.title("ML-RG-0037 Formulario de Quejas y Sugerencias")
st.markdown("---")
st.write("Por favor complete el siguiente formulario para registrar su queja o sugerencia.")

# Fecha y hora automática ajustada a Costa Rica (UTC-6)
ahora = datetime.utcnow() - timedelta(hours=6)
fecha = ahora.strftime("%Y-%m-%d")
hora = ahora.strftime("%H:%M:%S")

st.write(f"**Fecha:** {fecha}")
st.write(f"**Hora:** {hora}")

# Tipo de cliente
tipo_cliente = st.selectbox("Tipo de Cliente", ["Externo", "Interno"])

# Nombre o Área según tipo
if tipo_cliente == "Externo":
    nombre_area = st.text_input("Nombre del Cliente o Área")
else:
    nombre_area = st.selectbox("Nombre del Cliente o Área", ["Producción", "Calidad"])

# Tipo de Reporte
tipo_reporte = st.selectbox("Tipo de Reporte", ["Queja", "Sugerencia"])

# Descripción
detalle = st.text_area("Descripción de la queja o sugerencia")

# Confirmación
confirmar = st.checkbox("Confirmo que la información ingresada es correcta")

# ================= ENVÍO =================
if st.button("📤 Enviar registro"):
    if not nombre_area or not detalle:
        st.warning("⚠️ Por favor complete todos los campos obligatorios antes de enviar.")
    elif not confirmar:
        st.info("☑️ Debe confirmar que la información ingresada es correcta antes de enviar.")
    else:
        try:
            registros = sheet.get_all_records()
            numero = len(registros) + 1

            # Orden de columnas en Google Sheets
            fila = [numero, fecha, hora, tipo_cliente, nombre_area, tipo_reporte, detalle]

            sheet.append_row(fila)
            st.success(f"✅ Registro enviado con éxito. Número de solicitud: **{numero}**")
            st.balloons()
        except Exception as e:
            st.error(f"❌ Ocurrió un error al guardar en Google Sheets: {e}")
