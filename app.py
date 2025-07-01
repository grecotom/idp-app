import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Configuración
st.set_page_config(page_title="IDP App", layout="wide")

# Autenticación con Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(credentials)

# ID del Google Sheet (copiado del link)
SHEET_ID = "1R-xYz56xJAePDb1x5slsfWJaHOusvl-9AiU-ed36smw"
sheet = client.open_by_key(SHEET_ID)

# Función para cargar cada hoja
def load_sheet(name):
    ws = sheet.worksheet(name)
    data = ws.get_all_records()
    return pd.DataFrame(data)

# Función para agregar fila
def append_to_sheet(name, row):
    ws = sheet.worksheet(name)
    ws.append_row(row)

# Sidebar para navegación
menu = st.sidebar.selectbox("Ir a sección", [
    "📋 Listado de jugadores",
    "➕ Agregar jugador",
    "🎯 Agregar IDP_1",
    "📈 Agregar IDP_2",
    "💡 Agregar Skills",
    "🧠 Agregar Personality"
])

# 1. Listado de jugadores con vínculos
if menu == "📋 Listado de jugadores":
    st.title("Listado de jugadores con Skills y Personality")

    players_df = load_sheet("Players")
    skills_df = load_sheet("Skills")
    pers_df = load_sheet("Personality")

    df = players_df.merge(skills_df, how="left", on="Player Name").merge(pers_df, how="left", on="Player Name")
    st.dataframe(df)

# 2. Agregar jugador
elif menu == "➕ Agregar jugador":
    st.title("Agregar nuevo jugador")
    with st.form("add_player"):
        name = st.text_input("Nombre del jugador")
        birth = st.date_input("Fecha de nacimiento")
        position = st.text_input("Posición")
        submitted = st.form_submit_button("Guardar")
        if submitted:
            append_to_sheet("Players", [name, str(birth), position])
            st.success("✅ Jugador agregado")

# 3. Agregar IDP_1
elif menu == "🎯 Agregar IDP_1":
    st.title("Agregar entrada IDP_1")
    with st.form("add_idp1"):
        name = st.text_input("Jugador")
        date = st.date_input("Fecha")
        goal = st.text_input("Goal")
        reality = st.text_input("Reality")
        opportunity = st.text_input("Opportunity")
        action = st.text_input("Action Plan")
        submitted = st.form_submit_button("Guardar")
        if submitted:
            append_to_sheet("IDP_1", [name, str(date), goal, reality, opportunity, action])
            st.success("✅ IDP_1 guardado")

# 4. Agregar IDP_2
elif menu == "📈 Agregar IDP_2":
    st.title("Agregar entrada IDP_2")
    with st.form("add_idp2"):
        name = st.text_input("Jugador")
        date = st.date_input("Fecha")
        focus = st.text_input("Focus")
        notes = st.text_area("Notas")
        submitted = st.form_submit_button("Guardar")
        if submitted:
            append_to_sheet("IDP_2", [name, str(date), focus, notes])
            st.success("✅ IDP_2 guardado")

# 5. Agregar Skills
elif menu == "💡 Agregar Skills":
    st.title("Agregar skill")
    with st.form("add_skill"):
        name = st.text_input("Jugador")
        skill = st.text_input("Skill")
        level = st.text_input("Nivel")
        submitted = st.form_submit_button("Guardar")
        if submitted:
            append_to_sheet("Skills", [name, skill, level])
            st.success("✅ Skill guardado")

# 6. Agregar Personality
elif menu == "🧠 Agregar Personality":
    st.title("Agregar tipo de personalidad")
    with st.form("add_personality"):
        name = st.text_input("Jugador")
        trait = st.text_input("Tipo")
        definition = st.text_area("Definición")
        submitted = st.form_submit_button("Guardar")
        if submitted:
            append_to_sheet("Personality", [name, trait, definition])
            st.success("✅ Personalidad guardada")
