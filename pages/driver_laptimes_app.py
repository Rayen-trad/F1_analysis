# C:\F1_analysis\streamlit_analysis\driver_lap_times_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import os
from PIL import Image

# -----------------------
# Load Data
# -----------------------
DATA_PATH = r"C:\F1_analysis\data\processed\laps_2024_cleaned.csv"
df = pd.read_csv(DATA_PATH)

# -----------------------
# Paths to images
# -----------------------
DRIVER_IMAGES_PATH = r"C:\F1_analysis\assets\drivers"
CAR_IMAGES_PATH = r"C:\F1_analysis\assets\teams"

# -----------------------
# Page setup
# -----------------------
st.set_page_config(page_title="F1 2024 Driver Lap Times", layout="wide")
st.title("🏎️ F1 2024 Driver Lap Times Analysis")

# -----------------------
# Sidebar filters
# -----------------------
st.sidebar.header("Filters")

selected_race = st.sidebar.selectbox("Select Race", df["Race_Name"].unique())
race_df = df[df["Race_Name"] == selected_race]

selected_driver = st.sidebar.selectbox("Select Driver", sorted(race_df["Driver"].unique()))

# -----------------------
# Display driver + car images using columns
# -----------------------
driver_img_file = os.path.join(DRIVER_IMAGES_PATH, f"{selected_driver}.png")
team_name = race_df[race_df["Driver"] == selected_driver]["Team"].iloc[0]
car_img_file = os.path.join(CAR_IMAGES_PATH, f"{team_name}.png")

col1, col2 = st.columns([1, 4])

with col1:
    if os.path.exists(driver_img_file):
        driver_img = Image.open(driver_img_file)
        st.image(driver_img, width=150)

with col2:
    if os.path.exists(car_img_file):
        car_img = Image.open(car_img_file)
        st.image(car_img, width=600)

# -----------------------
# Filter driver laps
# -----------------------
driver_laps = race_df[race_df["Driver"] == selected_driver].sort_values("LapNumber").reset_index()

# -----------------------
# Tyre color mapping
# -----------------------
COMPOUND_COLORS = {
    "SOFT": "#FF3333",
    "MEDIUM": "#FFD700",
    "HARD": "#E6E6E6",
    "INTERMEDIATE": "#39B54A",
    "WET": "#1E90FF"
}

# -----------------------
# Plotly scatter plot
# -----------------------
fig = px.scatter(
    driver_laps,
    x="LapNumber",
    y="LapTimeSeconds",
    color="Compound",
    color_discrete_map=COMPOUND_COLORS,
    hover_data={
        "LapNumber": True,
        "LapTimeSeconds": True,
        "Compound": True,
        "PitInTime": True
    },
    title=f"{selected_driver} – {selected_race}",
    height=600
)

fig.update_yaxes(autorange="reversed", title="Lap Time (s)")
fig.update_xaxes(title="Lap Number")
fig.update_layout(
    plot_bgcolor="#111111",
    paper_bgcolor="#111111",
    font_color="#FFFFFF",
    legend_title_text="Tyre Compound"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------
# Optional: Show raw data
# -----------------------
if st.checkbox("Show raw lap data"):
    st.dataframe(driver_laps)
