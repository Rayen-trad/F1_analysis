# Tire_Usage_Interactive_Improved_Theme.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(
    page_title="F1 Tire Strategies",
    layout="wide"
)
st.title("🏁 F1 Tire Strategies & Pit Analysis")

# -------------------------------
# Load dataset
# -------------------------------
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # C:\F1_analysis
DATA_PATH = BASE_DIR / "data" / "processed" / "f1_cleaned.csv"

df = pd.read_csv(DATA_PATH)

# -------------------------------
# Sidebar: Race selection
# -------------------------------
races = df["Race_Name"].unique()
selected_race = st.sidebar.selectbox("Select Race", sorted(races))
race_df = df[df["Race_Name"] == selected_race]

# -------------------------------
# Drivers in this race (use Abbreviation for images)
# -------------------------------
drivers = race_df["Abbreviation"].unique()

# -------------------------------
# Show driver images neatly
# -------------------------------
st.subheader("Drivers")
cols = st.columns(len(drivers))
for i, driver in enumerate(drivers):
    img_path = f"C:/F1_analysis/assets/drivers/{driver}.png"
    if os.path.exists(img_path):
        cols[i].image(img_path, width=120, caption=driver)
    else:
        cols[i].write(driver)

# -------------------------------
# Tire Strategy Plot (stacked horizontal bars)
# -------------------------------
compound_colors = {
    "SOFT": "#FF073A",        # Neon red
    "MEDIUM": "#FFD700",      # Neon yellow
    "HARD": "#FFFFFF",        # White
    "INTERMEDIATE": "#00FF00",# Neon green
    "WET": "#00BFFF"          # Neon blue
}

# Create stints summary
stints = race_df[["Abbreviation", "Stint", "Tire_Compound", "Stint_Length"]]
stints_summary = stints.groupby(["Abbreviation", "Stint", "Tire_Compound"]).sum().reset_index()

fig_tire = px.bar(
    stints_summary,
    x="Stint_Length",
    y="Abbreviation",
    color="Tire_Compound",
    orientation='h',
    text="Stint_Length",
    color_discrete_map=compound_colors,
    hover_data=["Tire_Compound", "Stint_Length"],
    template="plotly_dark"
)

fig_tire.update_layout(
    title=f"Tire Strategies – {selected_race}",
    xaxis_title="Lap Number",
    yaxis_title="Driver",
    yaxis={'categoryorder':'total ascending'},
    barmode='stack',
    plot_bgcolor="#111111",
    paper_bgcolor="#111111",
    font=dict(color="#FFFFFF"),
    height=600
)

st.plotly_chart(fig_tire, use_container_width=True)

# -------------------------------
# Average Total Pit Stops per Circuit (Plotly version)
# -------------------------------
st.subheader("Average Pit Stops per Circuit – 2024 Season")
pit_stops_per_circuit = df.groupby("Circuit")["TotalPitStops"].mean().sort_values().reset_index()

fig_pit = px.bar(
    pit_stops_per_circuit,
    x="Circuit",
    y="TotalPitStops",
    text="TotalPitStops",
    color="TotalPitStops",
    color_continuous_scale=px.colors.sequential.Reds,
    template="plotly_dark"
)

fig_pit.update_layout(
    xaxis_tickangle=-45,
    xaxis_title="Circuit",
    yaxis_title="Average Pit Stops",
    plot_bgcolor="#111111",
    paper_bgcolor="#111111",
    font=dict(color="#FFFFFF"),
    height=500
)

st.plotly_chart(fig_pit, use_container_width=True)

# -------------------------------
# Correlation Matrix – Air Temp, Track Temp & Total Pit Stops (Plotly version)
# -------------------------------
st.subheader("Correlation Matrix – Air Temp, Track Temp & Total Pit Stops")
corr_df = df[["Air_Temp_C", "Track_Temp_C", "TotalPitStops"]]
corr_matrix = corr_df.corr().round(2)

fig_corr = px.imshow(
    corr_matrix,
    text_auto=True,
    color_continuous_scale=px.colors.sequential.Reds,
    template="plotly_dark"
)

fig_corr.update_layout(
    plot_bgcolor="#111111",
    paper_bgcolor="#111111",
    font=dict(color="#FFFFFF"),
    height=450
)

st.plotly_chart(fig_corr, use_container_width=True)
