import pandas as pd
import seaborn as sns

# Load cleaned dataset
DATA_PATH = r"C:\F1_analysis\data\processed\laps_2024_cleaned.csv"
df = pd.read_csv(DATA_PATH)

# Get all races
def get_races():
    return sorted(df["Race_Name"].unique())

# Get drivers for a given race
def get_drivers(race_name):
    return sorted(df[df["Race_Name"] == race_name]["Driver"].unique())

# Generate team color mapping
def get_team_colors(race_df):
    teams = race_df["Team"].unique()
    return dict(zip(teams, sns.color_palette("tab10", len(teams))))
