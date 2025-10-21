import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

# -------------------------------
# Configuración nombres
# -------------------------------
nombre_formulario_app = "ML-RG-0037 Formulario de Quejas y Sugerencias"
google_sheet_id = "TU_HOJA_ID_AQUI"  # Pega aquí el ID de tu Google Sheet

# -------------------------------
# Configuración Streamlit
# -------------------------------
st.set_page_config(
    page_title=nombre_formulario_app,
    page_icon="🛢️",
    layout="centered"
)

# Logo METALUB
try:
    st.image("logo.png", width=150)
except:
    pass

st.markdown(f"<h1 style='text-align: center; color: #006400;'>{nombre_formulario_app}</h1>", unsafe_allow_html=True)
st.markdown("---")

# -------------------------------
# Formulario dinámico
# -------------------------------
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

# Botón enviar
if st.button("Enviar"):
    try:
        # Conectar con Google Sheets
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(google_sheet_id).sheet1

        # Leer datos actuales
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        # Número de solicitud
        numero_solicitud = df["No. Solicitud"].max() + 1 if not df.empty else 1

        # Nueva fila
        nueva_fila = pd.DataFrame({
            "No. Solicitud": [numero_solicitud],
            "Fecha": [fecha.strftime("%Y-%m-%d")],
            "Hora": [hora.strftime("%H:%M")],
            "Tipo de Cliente": [tipo_cliente],
            "Nombre del Cliente o Área": [nombre_area],
            "Tipo de Reporte": [tipo_reporte],
            "Descripción": [descripcion]
        })

        # Agregar a Google Sheets
        df = pd.concat([df, nueva_fila], ignore_index=True)
        set_with_dataframe(sheet, df)

        st.success(f"✅ Respuesta registrada correctamente. Número de solicitud: {numero_solicitud}")

    except Exception as e:
        st.error(f"❌ Ha ocurrido un error: {e}")
