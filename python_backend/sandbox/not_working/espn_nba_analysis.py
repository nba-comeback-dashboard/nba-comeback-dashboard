import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Fetch data from ESPN API
url = "http://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event=401705718"
response = requests.get(url)
data = response.json()

# Examine the structure of the response
print("Keys in the main response:", data.keys())

# Extract winprobability data
win_probability = data.get("winprobability", [])
print("\nWin Probability Entries:", len(win_probability))
if win_probability:
    print("Sample Win Probability Entry:", win_probability[0])

# Extract plays data
plays = data.get("plays", [])
print("\nPlays Entries:", len(plays))
if plays:
    print("Sample Play Entry:", plays[0])

# Create a DataFrame to store and analyze the data
win_prob_data = []

for wp_entry in win_probability:
    play_id = wp_entry.get("playId")
    home_wp = wp_entry.get("homeWinPercentage")
    
    # Find corresponding play in plays list
    play_details = next((p for p in plays if p.get("id") == play_id), None)
    
    if play_details:
        game_time_info = play_details.get("clock", {})
        period = play_details.get("period", {}).get("number", 0)
        
        # Calculate point margin (positive when home team is ahead)
        home_score = play_details.get("homeScore", 0)
        away_score = play_details.get("awayScore", 0)
        point_margin = home_score - away_score
        
        # Get timestamp if available
        timestamp = play_details.get("timeStamp", "")
        
        win_prob_data.append({
            "play_id": play_id,
            "period": period,
            "clock": game_time_info,
            "timestamp": timestamp,
            "home_score": home_score,
            "away_score": away_score,
            "point_margin": point_margin,
            "home_win_probability": home_wp
        })

# Create DataFrame
df = pd.DataFrame(win_prob_data)
print("\nDataFrame Shape:", df.shape)
print("\nDataFrame Sample:")
print(df.head())

# Save data to CSV
df.to_csv("espn_nba_game_analysis.csv", index=False)

# Visualize the relationship between point margin and win probability
plt.figure(figsize=(12, 6))
plt.scatter(df["point_margin"], df["home_win_probability"], alpha=0.6)
plt.title("Home Win Probability vs Point Margin")
plt.xlabel("Point Margin (Home - Away)")
plt.ylabel("Home Win Probability")
plt.grid(True, alpha=0.3)
plt.savefig("win_prob_vs_margin.png")

# Summary of findings
print("\nData Structure Summary:")
print(f"- Total win probability entries: {len(win_probability)}")
print(f"- Total plays entries: {len(plays)}")
print(f"- Matched entries: {len(win_prob_data)}")
print("\nStructure Analysis:")
print("- Win probability data is linked to plays through 'playId'")
print("- Each play has timing information (period and clock)")
print("- Score information allows calculation of point margin")
print("- Home win probability represents chance of home team winning")