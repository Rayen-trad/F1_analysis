# C:\F1_analysis\streamlit_analysis\team_pace_season_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import os

# -------------------------------
# Load Data
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent 
DATA_PATH = BASE_DIR / "data" / "processed" / "laps_2024_cleaned.csv"
df = pd.read_csv(DATA_PATH)

# Keep only personal best laps for fair team pace comparison
season_df = df[df["IsPersonalBest"] == True].copy()
all_teams = season_df["Team"].unique()

# -------------------------------
# Official F1 Team Colors
# -------------------------------
TEAM_COLORS = {
    "Red Bull Racing": "#0600EF",
    "Mercedes": "#00D2BE",
    "Ferrari": "#DC0000",
    "McLaren": "#FF8700",
    "Alfa Romeo": "#900000",
    "Aston Martin": "#006F62",
    "AlphaTauri": "#2B4562",
    "Alpine": "#0090FF",
    "Williams": "#005AFF",
    "Haas F1 Team": "#FFFFFF"
}

# -------------------------------
# Path to team images
# -------------------------------
TEAM_IMAGES_FOLDER = BASE_DIR / "assets" / "teams"

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(page_title="Team Pace - Season Overview", layout="wide")
st.markdown("<h1 style='color:#FF0000'>F1 2024 Season – Team Pace Comparison</h1>", unsafe_allow_html=True)

st.markdown("""
Select the teams you want to display from the sidebar.  
Each plot corresponds to a team, showing their lap time distribution across all races.
""")

# -------------------------------
# Sidebar for team selection
# -------------------------------
selected_teams = st.sidebar.multiselect(
    "Select teams to display",
    options=all_teams,
    default=list(all_teams[:3])
)

if not selected_teams:
    st.warning("Please select at least one team to display.")
else:
    for team in selected_teams:
        team_df = season_df[season_df["Team"] == team]

        # Display team car image above the plot - full width
        img_path = os.path.join(TEAM_IMAGES_FOLDER, f"{team}.png")
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)  # full width

        # Order races chronologically
        race_order = (
            team_df.groupby("Race_Name")["Round"].median()
            .sort_values()
            .index
        )

        # -------------------------------
        # Plot Team Pace
        # -------------------------------
        fig, ax = plt.subplots(figsize=(20, 10))

        # Get official color
        team_color = TEAM_COLORS.get(team, "grey")

        # Neon-style boxplot
        sns.boxplot(
            data=team_df,
            x="Race_Name",
            y="LapTimeSeconds",
            order=race_order,
            color=team_color,
            ax=ax,
            whiskerprops=dict(color="white", linewidth=2),
            boxprops=dict(edgecolor="white", linewidth=2),
            medianprops=dict(color="#FF0000", linewidth=2),
            capprops=dict(color="white", linewidth=2),
        )

        ax.set_facecolor("#111111")
        ax.set_title(f"{team} – Season Pace", color="#FF0000", fontsize=18)
        ax.set_ylabel("Lap Time (s)", color="white", fontsize=14)
        ax.set_xlabel(None)
        ax.tick_params(colors="white", rotation=45)
        ax.grid(False)

        fig.patch.set_facecolor("#111111")
        plt.tight_layout()
        st.pyplot(fig)
