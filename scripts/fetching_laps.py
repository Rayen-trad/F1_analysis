import fastf1
from fastf1.core import Laps
import pandas as pd
from tqdm import tqdm
import os

# -------------------------------
# Folder Setup
# -------------------------------
cache_folder = r"C:\F1_analysis\fastf1_cache"
processed_folder = r"C:\F1_analysis\data\processed"
season_folder = os.path.join(processed_folder, '2024')

os.makedirs(cache_folder, exist_ok=True)
os.makedirs(processed_folder, exist_ok=True)
os.makedirs(season_folder, exist_ok=True)

# Enable FastF1 cache
fastf1.Cache.enable_cache(cache_folder)

# Output file for 2024 laps
output_file = os.path.join(season_folder, 'laps_2024.csv')

# -------------------------------
# Season to fetch
# -------------------------------
season = 2024

# -------------------------------
# Fetch events
# -------------------------------
all_laps = []

print(f"Processing season {season}...")
try:
    events = fastf1.get_event_schedule(season)
except Exception as e:
    print(f"Failed to fetch event schedule for {season}: {e}")
    events = pd.DataFrame()  # fallback

# -------------------------------
# Loop through rounds
# -------------------------------
for round_no, event_row in tqdm(events.iterrows(), total=len(events), desc=f"Season {season}"):
    try:
        race = fastf1.get_session(season, round_no + 1, 'R')  # 'R' = Race
        race.load()  # load laps and telemetry

        # Load laps
        laps: Laps = race.laps
        laps = laps.reset_index()  # convert to DataFrame
        laps['Season'] = season
        laps['Round'] = round_no + 1
        laps['Race_Name'] = race.event['EventName']
        laps['Circuit'] = race.event['EventName']
        laps['Country'] = race.event['Country']
        laps['Date'] = race.event['EventDate']

        # Append to list
        all_laps.append(laps)

        # Optional: save JSON per round (like in your previous script)
        # round_file = os.path.join(season_folder, f"laps_round{round_no + 1}.csv")
        # laps.to_csv(round_file, index=False)

    except Exception as e:
        print(f"Failed to process Round {round_no + 1}: {e}")

# -------------------------------
# Save all laps CSV
# -------------------------------
if all_laps:
    final_df = pd.concat(all_laps, ignore_index=True)
    final_df.to_csv(output_file, index=False)
    print(f"\n✅ Saved all 2024 race laps to {output_file}")
else:
    print("No laps were loaded for 2024.")
