# driver_lap_overlay_app.py
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from PIL import Image
import os

# -------------------------------
# Load dataset
# -------------------------------
DATA_PATH = r"C:\F1_analysis\data\processed\laps_2024_cleaned.csv"
df = pd.read_csv(DATA_PATH)

# -------------------------------
# Utility functions
# -------------------------------

def get_races():
    return sorted(df["Race_Name"].unique())

def get_drivers(race):
    return sorted(df[df["Race_Name"] == race]["Driver"].unique())

# Example: team colors as RGB tuples (0-1), convert to hex for Plotly
TEAM_COLORS_RGB = {
    "Red Bull Racing": (0.0, 0.0, 0.94),
    "Mercedes": (0.0, 0.82, 0.75),
    "Ferrari": (0.86, 0.0, 0.0),
    "McLaren": (1.0, 0.53, 0.0),
    "Alfa Romeo": (0.56, 0.0, 0.0),
    "Aston Martin": (0.0, 0.44, 0.38),
    "AlphaTauri": (0.17, 0.27, 0.38),
    "Alpine": (0.0, 0.56, 1.0),
    "Williams": (0.0, 0.35, 1.0),
    "Haas F1 Team": (1.0, 1.0, 1.0)
}

def rgb_to_hex(rgb_tuple):
    """Convert RGB tuple (0-1 floats) to hex string."""
    return '#{:02x}{:02x}{:02x}'.format(
        int(rgb_tuple[0]*255),
        int(rgb_tuple[1]*255),
        int(rgb_tuple[2]*255)
    )

def get_team_colors(race_df):
    teams = race_df["Team"].unique()
    return {team: rgb_to_hex(TEAM_COLORS_RGB.get(team, (0.5,0.5,0.5))) for team in teams}

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="F1 2024 Lap Times Overlay", layout="wide")
st.title("🏎️ F1 2024 Lap Times Overlay Analysis")

# Sidebar filters
selected_race = st.sidebar.selectbox("Select Race", get_races())
drivers_selected = st.sidebar.multiselect(
    "Select Drivers",
    get_drivers(selected_race),
    default=get_drivers(selected_race)[:2]
)

if drivers_selected:
    race_df = df[df["Race_Name"] == selected_race].sort_values("LapNumber").reset_index()
    team_colors = get_team_colors(race_df)

    # -------------------------------
    # Display driver images
    # -------------------------------
    st.markdown("### Drivers")
    driver_cols = st.columns(len(drivers_selected))
    for col, driver in zip(driver_cols, drivers_selected):
        img_path = os.path.join(r"C:\F1_analysis\assets\drivers", f"{driver}.png")
        if os.path.exists(img_path):
            img = Image.open(img_path)
            col.image(img, width=300)  # Adjust width
        else:
            col.text(driver)

    # -------------------------------
    # Plot interactive lap times
    # -------------------------------
    fig = go.Figure()

    for driver in drivers_selected:
        driver_laps = race_df[race_df["Driver"] == driver]
        team = driver_laps["Team"].iloc[0]
        team_color = team_colors[team]

        fig.add_trace(go.Scatter(
            x=driver_laps["LapNumber"],
            y=driver_laps["LapTimeSeconds"],
            mode="lines+markers",
            name=driver,
            line=dict(color=team_color, width=2),
            marker=dict(size=8),
            hovertemplate="Lap %{x}<br>Lap Time: %{y:.3f}s<extra></extra>"
        ))

        # Pit stops as vertical lines
        pit_laps = driver_laps[driver_laps["PitInTime"].notna()]
        for lap in pit_laps["LapNumber"]:
            fig.add_vline(
                x=lap,
                line=dict(color=team_color, dash="dash", width=1),
                opacity=0.5
            )

    fig.update_layout(
        title=f"Lap Times Overlay – {selected_race}",
        xaxis_title="Lap Number",
        yaxis_title="Lap Time (s)",
        yaxis_autorange="reversed",
        template="plotly_dark",
        height=600,
        width=1200
    )

    st.plotly_chart(fig, use_container_width=True)
