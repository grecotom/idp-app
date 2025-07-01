import streamlit as st
import pandas as pd
import gspread
import json
import os
from google.oauth2.service_account import Credentials

# Streamlit page config
st.set_page_config(page_title="Player Development Portal", layout="wide")

# Load credentials from Streamlit Secrets
credentials_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
scope = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(credentials_dict, scopes=scope)
client = gspread.authorize(credentials)

# Google Sheet setup
SHEET_ID = "1R-xYz56xJAePDb1x5slsfWJaHOusvl-9AiU-ed36smw"
sheet = client.open_by_key(SHEET_ID)

# Utility functions
def load_sheet(name):
    ws = sheet.worksheet(name)
    data = ws.get_all_records()
    return pd.DataFrame(data)

def append_to_sheet(name, row):
    ws = sheet.worksheet(name)
    ws.append_row(row)

def update_sheet_row(name, df):
    ws = sheet.worksheet(name)
    ws.clear()
    ws.update([df.columns.values.tolist()] + df.values.tolist())

# App layout
menu = st.sidebar.radio("Navigation", ["Home", "Player Dashboard"])

# 1. Editable Player List
if menu == "Home":
    st.title("📄 Player List")
    st.markdown("Edit player data directly below. Changes will be saved to Google Sheets.")

    players_df = load_sheet("Players")
    edited_df = st.data_editor(players_df, num_rows="dynamic")

    if st.button("Save Changes"):
        update_sheet_row("Players", edited_df)
        st.success("Player list updated!")

# 2. Individual Player Dashboard
elif menu == "Player Dashboard":
    st.title("🔍 Player Dashboard")

    players_df = load_sheet("Players")
    player_names = players_df["Player Name"].dropna().unique()
    selected = st.selectbox("Select a player", player_names)

    if selected:
        st.subheader(f"Profile: {selected}")

        col1, col2 = st.columns([1, 3])
        with col1:
            info = players_df[players_df["Player Name"] == selected].iloc[0]
            st.image(info["Profile Picture"], width=150)
            st.markdown(f"**Team:** {info['Team']}")
            st.markdown(f"**DOB:** {info['DOB']}")
            st.markdown(f"**Age:** {info['Age']}")
            st.markdown(f"**Position 1:** {info['Position 1']}")
            st.markdown(f"**Position 2:** {info['Position 2']}")

        # Load and show each section as expandable
        with st.expander("🎯 IDP_1"):
            idp1 = load_sheet("IDP_1")
            st.dataframe(idp1[idp1["Player Name"] == selected])

        with st.expander("📊 IDP_2"):
            idp2 = load_sheet("IDP_2")
            st.dataframe(idp2[idp2["Player Name"] == selected])

        with st.expander("🧠 Personality"):
            pers = load_sheet("Personality")
            st.dataframe(pers[pers["Player Name"] == selected])

        with st.expander("🔧 Skills"):
            skills = load_sheet("Skills")
            st.dataframe(skills[skills["Player Name"] == selected])
