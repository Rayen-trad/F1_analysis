# main_page.py
import streamlit as st
from PIL import Image
import os

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="F1 2024 Analysis Hub",
    layout="wide"
)

# -------------------------------
# Dark theme & F1 red accent
# -------------------------------
st.markdown("""
    <style>
    /* Main background */
    .main {
        background-color: #0e0e0e;
        color: white;
    }
    h1, h2, h3 {
        color: #FF0000;  /* F1 red accent */
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #111111;
    }
    [data-testid="stSidebar"] .css-1d391kg a {
        color: white;
        text-decoration: none;
    }
    /* Highlight selected item in sidebar */
    [data-testid="stSidebar"] .css-1d391kg .st-c7 {
        color: #FF0000 !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# F1 Logo
# -------------------------------
logo_path = "assets/F1.svg.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, width=600)

# -------------------------------
# Welcome text
# -------------------------------
st.markdown("""
# Welcome to the F1 2024 Analysis Hub
Explore detailed Formula 1 race analytics including driver lap times, tire strategies, team pace, and tire degradation.
This dashboard allows you to dive deep into performance trends, tire management, and comparative analysis for the 2024 season.
""")

st.markdown("---")

# -------------------------------
# Analyses Grid (Images + Titles + Description)
# -------------------------------
analyses = [
    {
        "title": "Tire Strategies per Race",
        "description": "Visualize each driver’s tire stints during a race and how they managed their tire usage.",
        "image": "assets/Strategie.jpg"
    },
    {
        "title": "Lap Times Overlay",
        "description": "Compare multiple drivers’ lap times across a single race with pit stop markers and tire compounds.",
        "image": "assets/laptimes.jpg"
    },
    {
        "title": "Tire Degradation",
        "description": "Analyze lap time progression to understand tire wear patterns for drivers.",
        "image": "assets/Tire_deg.jpg"
    },
    {
        "title": "Team Pace Comparison",
        "description": "Compare median lap times of all F1 teams across the season.",
        "image": "assets/team_pace.jpg"
    },
    {
        "title": "Driver Lap Times Comparison",
        "description": "Compare selected drivers’ lap times in detail.",
        "image": "assets/driverlap.jpg"
    }
]

# -------------------------------
# Display analyses in a 2-column grid
# -------------------------------
num_cols = 2
for i in range(0, len(analyses), num_cols):
    cols = st.columns(num_cols)
    for j, analysis in enumerate(analyses[i:i+num_cols]):
        with cols[j]:
            # Display image
            if os.path.exists(analysis["image"]):
                img = Image.open(analysis["image"])
                st.image(img, width=500)  # <-- Modify width here
            # Title & description
            st.markdown(f"### {analysis['title']}")
            st.markdown(analysis["description"])

st.markdown("---")
st.markdown("Enjoy exploring the 2024 F1 season analytics with interactive plots and insightful visualizations!")
