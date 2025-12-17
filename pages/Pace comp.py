# pages/team_pace_race.py
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

# -----------------------
# Paths
# -----------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "laps_2024_cleaned.csv"

# -----------------------
# Load dataset
# -----------------------
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

# -----------------------
# Streamlit layout
# -----------------------
st.title("Team Pace Comparison per Race")

# Select race
races = df["Race_Name"].unique()
selected_race = st.selectbox("Select a race", sorted(races))

# Filter dataset
race_df = df[df["Race_Name"] == selected_race].copy()
race_df = race_df[race_df["IsPersonalBest"] == True]

# Order teams by median lap time
team_order = race_df.groupby("Team")["LapTimeSeconds"].median().sort_values().index

# Plot interactive boxplot
fig = px.box(
    race_df,
    x="Team",
    y="LapTimeSeconds",
    color="Team",
    category_orders={"Team": team_order},
    title=f"{selected_race} – Team Pace Comparison",
    points="all",  # show individual laps as points
)

fig.update_layout(
    xaxis_title=None,
    yaxis_title="Lap Time (s)",
    showlegend=False,
    template="plotly_white",
)

st.plotly_chart(fig, use_container_width=True)

# Optional: add a download button
st.download_button(
    label="Download plot as PNG",
    data=fig.to_image(format="png"),
    file_name=f"{selected_race}_team_pace.png",
)
