import os
import json
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Leer el Secret desde Streamlit Cloud
cred_json = os.getenv("GOOGLE_CREDENTIALS")
if not cred_json:
    st.error("No se encontró la variable de entorno GOOGLE_CREDENTIALS")
    st.stop()

# Convertir la cadena JSON a diccionario
creds_dict = json.loads(cred_json)

# Permisos de Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Autenticación
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Abrir Google Sheet
sheet_name = "ML-RG-0040 Registro de Quejas y Sugerencias"
sheet = client.open(sheet_name).sheet1
