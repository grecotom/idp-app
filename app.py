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

# Sidebar as dashboard-like navigation
st.sidebar.markdown("""
<style>
.sidebar .sidebar-content {
    background-color: #f0f2f6;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Navigation")
menu = st.sidebar.radio("", [
    "Players",
    "Personality",
    "IDP_1",
    "IDP_2",
    "Skills",
    "Player Profile"
])

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

    edited_df = st.data_editor(filtered_df, num_rows="fixed")
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
    st.data_editor(shown, key="personality_editor", on_change=lambda: update_sheet("Personality", shown), num_rows="fixed")

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
    st.data_editor(shown, key="idp1_editor", on_change=lambda: update_sheet("IDP_1", shown), num_rows="fixed")

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
    st.data_editor(shown, key="idp2_editor", on_change=lambda: update_sheet("IDP_2", shown), num_rows="fixed")

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
    st.data_editor(shown, key="skills_editor", on_change=lambda: update_sheet("Skills", shown), num_rows="fixed")

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

        st.markdown("---")
        st.subheader("🎯 IDP_1")
        idp1 = load_sheet("IDP_1")
        st.data_editor(idp1[idp1["Player Name"] == selected], key="pp_idp1", num_rows="fixed")

        st.subheader("📈 IDP_2")
        idp2 = load_sheet("IDP_2")
        st.data_editor(idp2[idp2["Player Name"] == selected], key="pp_idp2", num_rows="fixed")

        st.subheader("💡 Skills")
        skills = load_sheet("Skills")
        st.data_editor(skills[skills["Player Name"] == selected], key="pp_skills", num_rows="fixed")

        st.subheader("🧠 Personality")
        pers = load_sheet("Personality")
        st.data_editor(pers[pers["Player Name"] == selected], key="pp_pers", num_rows="fixed")
