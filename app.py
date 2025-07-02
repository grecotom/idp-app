import streamlit as st
import pandas as pd
import gspread
import json
import os
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="IDP Platform", layout="wide")

# Load credentials from Streamlit Secrets
credentials_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
scope = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(credentials_dict, scopes=scope)
client = gspread.authorize(credentials)

SHEET_ID = "1R-xYz56xJAePDb1x5slsfWJaHOusvl-9AiU-ed36smw"
sheet = client.open_by_key(SHEET_ID)

# Utility functions
def load_sheet(name):
    ws = sheet.worksheet(name)
    return pd.DataFrame(ws.get_all_records())

def update_sheet(name, df):
    ws = sheet.worksheet(name)
    ws.clear()
    ws.update([df.columns.tolist()] + df.values.tolist())

def merge_with_players(section_df):
    players_df = load_sheet("Players")
    return section_df.merge(players_df, on="Player Name", how="left")

# Sidebar menu as vertical buttons
st.sidebar.title("Navigation")
menu_options = [
    "Players",
    "Personality",
    "IDP_1",
    "IDP_2",
    "Skills",
    "Player Profile"
]
menu = None
for option in menu_options:
    if st.sidebar.button(option):
        menu = option
if menu is None:
    menu = menu_options[0]

# Section 1 - Players
if menu == "Players":
    st.title("🧍 Players Overview")
    df = load_sheet("Players")
    teams = df["Team"].dropna().unique()
    positions = df["Position 1"].dropna().unique()

    team_filter = st.multiselect("Filter by Team", options=teams)
    pos_filter = st.multiselect("Filter by Position 1", options=positions)

    filtered_df = df.copy()
    if team_filter:
        filtered_df = filtered_df[filtered_df["Team"].isin(team_filter)]
    if pos_filter:
        filtered_df = filtered_df[filtered_df["Position 1"].isin(pos_filter)]

    edited_df = st.data_editor(filtered_df, num_rows="dynamic")
    if st.button("Save Player Data"):
        update_sheet("Players", edited_df)
        st.success("Players sheet updated successfully!")

# Section 2 - Personality
elif menu == "Personality":
    st.title("🧠 Personality Overview")
    df = load_sheet("Personality")
    df = merge_with_players(df)

    team_filter = st.multiselect("Filter by Team", options=df["Team"].dropna().unique())
    pos_filter = st.multiselect("Filter by Position 1", options=df["Position 1"].dropna().unique())

    if team_filter:
        df = df[df["Team"].isin(team_filter)]
    if pos_filter:
        df = df[df["Position 1"].isin(pos_filter)]

    shown = df[["Player Name", "DOB", "Age", "Position 1", "Position 2", "Personality Trait", "Personality Definition"]]
    edited_df = st.data_editor(shown, num_rows="dynamic")
    if st.button("Save Personality Data"):
        update_sheet("Personality", edited_df)
        st.success("Personality sheet updated successfully!")

# Section 3 - IDP_1
elif menu == "IDP_1":
    st.title("🎯 IDP_1 Overview")
    df = load_sheet("IDP_1")
    df = merge_with_players(df)

    team_filter = st.multiselect("Filter by Team", options=df["Team"].dropna().unique())
    pos_filter = st.multiselect("Filter by Position 1", options=df["Position 1"].dropna().unique())

    if team_filter:
        df = df[df["Team"].isin(team_filter)]
    if pos_filter:
        df = df[df["Position 1"].isin(pos_filter)]

    shown = df[["Player Name", "DOB", "Age", "Position 1", "Position 2", "Date", "Season Timing", "Goals", "Reality", "Opportunity"]]
    edited_df = st.data_editor(shown, num_rows="dynamic")
    if st.button("Save IDP_1 Data"):
        update_sheet("IDP_1", edited_df)
        st.success("IDP_1 sheet updated successfully!")

# Section 4 - IDP_2
elif menu == "IDP_2":
    st.title("📈 IDP_2 Overview")
    df = load_sheet("IDP_2")
    df = merge_with_players(df)

    team_filter = st.multiselect("Filter by Team", options=df["Team"].dropna().unique())
    pos_filter = st.multiselect("Filter by Position 1", options=df["Position 1"].dropna().unique())

    if team_filter:
        df = df[df["Team"].isin(team_filter)]
    if pos_filter:
        df = df[df["Position 1"].isin(pos_filter)]

    shown = df[["Player Name", "DOB", "Age", "Position 1", "Position 2", "Date", "Development Area", "Component", "Intervention", "Responsibility", "Time Frame", "Success Measures"]]
    edited_df = st.data_editor(shown, num_rows="dynamic")
    if st.button("Save IDP_2 Data"):
        update_sheet("IDP_2", edited_df)
        st.success("IDP_2 sheet updated successfully!")

# Section 5 - Skills
elif menu == "Skills":
    st.title("💡 Skills Overview")
    df = load_sheet("Skills")
    df = merge_with_players(df)

    team_filter = st.multiselect("Filter by Team", options=df["Team"].dropna().unique())
    pos_filter = st.multiselect("Filter by Position 1", options=df["Position 1"].dropna().unique())

    if team_filter:
        df = df[df["Team"].isin(team_filter)]
    if pos_filter:
        df = df[df["Position 1"].isin(pos_filter)]

    shown = df[["Player Name", "DOB", "Age", "Position 1", "Position 2", "Date", "Focus_Skill_1", "Focus_Skill_2", "Focus_Skill_3", "Dev_Skill_1", "Dev_Skill_2", "Dev_Skill_3"]]
    edited_df = st.data_editor(shown, num_rows="dynamic")
    if st.button("Save Skills Data"):
        update_sheet("Skills", edited_df)
        st.success("Skills sheet updated successfully!")

# Section 6 - Player Profile
elif menu == "Player Profile":
    st.title("🧾 Full Player Profile")
    players_df = load_sheet("Players")
    player_names = players_df["Player Name"].dropna().unique()
    selected = st.selectbox("Select a player", player_names)

    if selected:
        st.subheader(f"Player: {selected}")
        info = players_df[players_df["Player Name"] == selected].iloc[0]
        col1, col2 = st.columns([1, 3])
        with col1:
            profile_pic_url = info.get("Profile Picture", "")
            if profile_pic_url.startswith("http"):
                st.image(profile_pic_url, width=150)
            else:
                st.warning("No valid profile picture URL provided.")
            st.markdown(f"**Team:** {info.get('Team', '')}")
            st.markdown(f"**DOB:** {info.get('DOB', '')}")
            st.markdown(f"**Age:** {info.get('Age', '')}")
            st.markdown(f"**Position 1:** {info.get('Position 1', '')}")
            st.markdown(f"**Position 2:** {info.get('Position 2', '')}")

        with st.expander("🎯 IDP_1"):
            idp1 = load_sheet("IDP_1")
            st.data_editor(idp1[idp1["Player Name"] == selected], num_rows="dynamic")

        with st.expander("📈 IDP_2"):
            idp2 = load_sheet("IDP_2")
            st.data_editor(idp2[idp2["Player Name"] == selected], num_rows="dynamic")

        with st.expander("💡 Skills"):
            skills = load_sheet("Skills")
            st.data_editor(skills[skills["Player Name"] == selected], num_rows="dynamic")

        with st.expander("🧠 Personality"):
            pers = load_sheet("Personality")
            st.data_editor(pers[pers["Player Name"] == selected], num_rows="dynamic")
