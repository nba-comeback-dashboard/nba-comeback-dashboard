import pandas as pd
import matplotlib.pyplot as plt
from nba_api.stats.endpoints import winprobabilitypbp

# Get the win probability play-by-play data for the specified game
# game_id = "0022401152"
# game_id = "0042400151"
game_id = "0022400826"
win_prob_data = winprobabilitypbp.WinProbabilityPBP(game_id=game_id)
win_prob_df = win_prob_data.get_data_frames()[0]

# Extract relevant columns
df = win_prob_df[
    [
        "GAME_ID",
        "EVENT_NUM",
        "HOME_PCT",
        "VISITOR_PCT",
        "HOME_PTS",
        "VISITOR_PTS",  #
        "PERIOD",
        "SECONDS_REMAINING",
        "DESCRIPTION",
    ]
]


# Calculate point margin (home team perspective)
df["POINT_MARGIN"] = df["HOME_PTS"] - df["VISITOR_PTS"]

# Create a time vector (minutes elapsed in the game)
# NBA games have 4 periods of 12 minutes each (48 minutes total in regulation)
df["MINUTES_ELAPSED"] = ((df["PERIOD"] - 1) * 12) + (12 - df["SECONDS_REMAINING"] / 60)

# Sort by minutes elapsed to ensure chronological order
df = df.sort_values("MINUTES_ELAPSED")

# Extract home team name and visiting team name from the first play description
first_play = df["DESCRIPTION"].iloc[0]
teams = first_play.split(" ")
if "vs." in teams:
    vs_index = teams.index("vs.")
    home_team = " ".join(teams[vs_index + 1 : vs_index + 3])
    visiting_team = " ".join(teams[vs_index - 2 : vs_index])
else:
    home_team = "Home Team"
    visiting_team = "Visiting Team"

# Create plots
plt.figure(figsize=(14, 10))

# Win probability plot
plt.subplot(2, 1, 1)
plt.plot(
    df["MINUTES_ELAPSED"],
    df["HOME_PCT"] * 100,
    "b-",
    label=f"{home_team} Win Probability",
)
plt.plot(
    df["MINUTES_ELAPSED"],
    df["VISITOR_PCT"] * 100,
    "r-",
    label=f"{visiting_team} Win Probability",
)
plt.axhline(y=50, color="black", linestyle="--", alpha=0.3)
plt.title(f"Win Probability Over Time - Game ID: {game_id}")
plt.xlabel("Minutes Elapsed")
plt.ylabel("Win Probability (%)")
plt.grid(True, alpha=0.3)
plt.legend()

# Score margin plot
plt.subplot(2, 1, 2)
plt.plot(df["MINUTES_ELAPSED"], df["POINT_MARGIN"], "g-")
plt.axhline(y=0, color="black", linestyle="--", alpha=0.3)
plt.title(f"Point Margin Over Time (Home Team Perspective) - Game ID: {game_id}")
plt.xlabel("Minutes Elapsed")
plt.ylabel("Point Margin")
plt.grid(True, alpha=0.3)

plt.tight_layout()

# Save the vectors to CSV for further analysis
output_df = df[["MINUTES_ELAPSED", "HOME_PCT", "VISITOR_PCT", "POINT_MARGIN"]]
output_df.to_csv(f"game_{game_id}_win_prob_and_margin.csv", index=False)

print(f"Analysis complete for Game ID: {game_id}")
print(f"Home Team: {home_team}, Visiting Team: {visiting_team}")
print(f"Data saved to 'game_{game_id}_win_prob_and_margin.csv'")

# Display the plot
plt.show()

# If you want to get just the vectors for further processing
time_vector = df["MINUTES_ELAPSED"].values
home_win_prob_vector = df["HOME_PCT"].values
visitor_win_prob_vector = df["VISITOR_PCT"].values
point_margin_vector = df["POINT_MARGIN"].values

print(f"Retrieved {len(time_vector)} data points")
