# tire_degradation_app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# -------------------------------
# Settings
# -------------------------------
DATA_PATH = r"C:\F1_analysis\data\processed\laps_2024_cleaned.csv"
DRIVER_IMG_FOLDER = r"C:\F1_analysis\assets\drivers"

st.set_page_config(page_title="F1 Tire Degradation", layout="wide")
st.title("F1 2024 Tire Degradation Analysis 🚦")

# -------------------------------
# Load dataset
# -------------------------------
df = pd.read_csv(DATA_PATH)

# -------------------------------
# Helper functions
# -------------------------------
def get_races():
    return sorted(df["Race_Name"].unique())

def get_drivers(selected_race):
    return sorted(df[df["Race_Name"] == selected_race]["Driver"].unique())

def get_team_colors(race_df):
    teams = race_df["Team"].unique()
    colors = {}
    for team in teams:
        colors[team] = {
            "Mercedes": "#00D2BE",
            "Red Bull Racing": "#1E41FF",
            "Ferrari": "#DC0000",
            "McLaren": "#FF8700",
            "Alpine": "#0090FF",
            "AlphaTauri": "#2B4562",
            "Aston Martin": "#006F62",
            "Williams": "#005AFF",
            "Haas": "#BD9E57",
            "Alfa Romeo": "#900000"
        }.get(team, "grey")
    return colors

# -------------------------------
# Sidebar selection
# -------------------------------
selected_race = st.sidebar.selectbox("Select Race", get_races())
selected_drivers = st.sidebar.multiselect(
    "Select Drivers",
    get_drivers(selected_race),
    default=get_drivers(selected_race)[:2]
)

if selected_drivers:
    race_df = df[df["Race_Name"] == selected_race].sort_values("LapNumber")
    team_colors = get_team_colors(race_df)

    # -------------------------------
    # Display driver images first
    # -------------------------------
    st.subheader("Selected Drivers")
    max_cols = min(4, len(selected_drivers))
    cols = st.columns(max_cols)
    for col, driver in zip(cols, selected_drivers):
        img_path = os.path.join(DRIVER_IMG_FOLDER, f"{driver}.png")
        if os.path.exists(img_path):
            col.image(img_path, caption=driver, use_container_width=True)
        else:
            col.write(f"No image for {driver}")

    # -------------------------------
    # Prepare figure
    # -------------------------------
    fig = go.Figure()

    for driver in selected_drivers:
        driver_laps = race_df[race_df["Driver"] == driver].reset_index()
        driver_laps['LapDelta'] = driver_laps['LapTimeSeconds'].diff().fillna(0)
        driver_laps['CumulativeDegradation'] = driver_laps['LapDelta'].cumsum()
        team = driver_laps["Team"].iloc[0]

        fig.add_trace(go.Scatter(
            x=driver_laps["LapNumber"],
            y=driver_laps["CumulativeDegradation"],
            mode='lines+markers',
            name=driver,
            line=dict(color=team_colors[team], width=3),
            marker=dict(size=8),
            hovertemplate=
            '<b>%{text}</b><br>Laps: %{x}<br>Degradation: %{y:.2f}s<extra></extra>',
            text=[driver]*len(driver_laps)
        ))

        # Pit stops
        pit_laps = driver_laps[driver_laps["PitInTime"].notna()]
        for lap in pit_laps["LapNumber"]:
            fig.add_vline(x=lap, line=dict(color=team_colors[team], dash='dash', width=1))

    fig.update_layout(
        title=f"Cumulative Tire Degradation – {selected_race}",
        xaxis_title="Lap Number",
        yaxis_title="Cumulative Lap Time Increase (s)",
        template="plotly_dark",
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="#FF0000"),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)
