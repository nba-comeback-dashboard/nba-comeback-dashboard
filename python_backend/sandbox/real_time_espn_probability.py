import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def get_nba_win_probability_history(game_id):
    """
    Fetches historical win probability data for a completed NBA game from ESPN.

    Args:
        game_id (str): ESPN's NBA game ID (e.g., '401705718')

    Returns:
        pandas.DataFrame: DataFrame containing timestamp, home win probability, and point margin
    """
    # ESPN API endpoint for game data
    url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={game_id}"

    try:
        # Make request to ESPN API
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        data = response.json()

        # Check if game data is available
        if "winprobability" not in data:
            print(f"Win probability data not available for game ID: {game_id}")
            return None

        # Extract win probability data
        win_prob_data = data["winprobability"]

        if not win_prob_data:
            print(f"Win probability data is empty for game ID: {game_id}")
            return None

        # Get team names
        teams = data["header"]["competitions"][0]["competitors"]
        home_team = None
        away_team = None

        for team in teams:
            if team.get("homeAway") == "home":
                home_team = team["team"]["displayName"]
            else:
                away_team = team["team"]["displayName"]

        # Get final score
        home_score = None
        away_score = None
        for team in teams:
            if team.get("homeAway") == "home":
                home_score = int(team.get("score", 0))
            else:
                away_score = int(team.get("score", 0))

        game_date = data["header"]["competitions"][0]["date"]
        game_status = data["header"]["competitions"][0]["status"]["type"]["detail"]

        print(f"\nGame Information:")
        print(f"Date: {game_date}")
        print(f"Status: {game_status}")
        print(f"Teams: {away_team} ({away_score}) @ {home_team} ({home_score})")
        print(f"Final Score: {home_team} {home_score} - {away_team} {away_score}")
        print(
            f"Result: {'Home team won' if home_score > away_score else 'Away team won'}"
        )

        # Create empty lists to store our data
        timestamps = []
        home_win_probs = []
        point_margins = []
        game_times = []

        # Process win probability data
        for entry in win_prob_data:
            # Get timestamp (seconds left in game)
            timestamps.append(entry.get("secondsLeft", 0))

            # Get home team win probability (as percentage)
            home_prob = entry.get("homeWinPercentage", 0) * 100
            home_win_probs.append(home_prob)

            # Calculate point margin (positive for home team lead, negative for away team lead)
            home_score = entry.get("homeScore", 0)
            away_score = entry.get("awayScore", 0)
            margin = home_score - away_score
            point_margins.append(margin)

            # Get period and clock time
            period = entry.get("period", 0)
            clock = entry.get("clock", 0)
            game_time = f"Q{period} {clock}"
            game_times.append(game_time)

        # Create DataFrame
        df = pd.DataFrame(
            {
                "seconds_left": timestamps,
                "game_time": game_times,
                "home_win_prob": home_win_probs,
                "point_margin": point_margins,
                "home_team": home_team,
                "away_team": away_team,
            }
        )

        # Sort by timestamp (descending seconds left = ascending game time)
        df = df.sort_values("seconds_left", ascending=False).reset_index(drop=True)

        # Add elapsed time column (seconds from start of game)
        # Assuming standard NBA game length is 48 minutes (2880 seconds)
        total_game_seconds = 2880  # 48 minutes * 60 seconds
        df["elapsed_time"] = total_game_seconds - df["seconds_left"]

        # Add game information
        df["game_id"] = game_id
        df["game_date"] = game_date

        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing data: {e}")
        return None


def plot_win_probability(df):
    """
    Plots win probability and point margin over time.

    Args:
        df (pandas.DataFrame): DataFrame with win probability data
    """
    if df is None or df.empty:
        print("No data to plot")
        return

    # Create a figure with two subplots sharing the x-axis
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(14, 10), sharex=True, gridspec_kw={"height_ratios": [2, 1]}
    )

    # Get team names
    home_team = df["home_team"].iloc[0]
    away_team = df["away_team"].iloc[0]
    game_id = df["game_id"].iloc[0]
    game_date = df["game_date"].iloc[0]

    # Filter out any duplicate timestamps
    df = df.drop_duplicates(subset=["seconds_left"])

    # Plot win probability
    ax1.plot(df["elapsed_time"], df["home_win_prob"], "b-", linewidth=2)
    ax1.set_title(
        f"Win Probability: {away_team} @ {home_team} (Game ID: {game_id}, Date: {game_date})",
        fontsize=16,
    )
    ax1.set_ylabel(f"{home_team} Win Probability (%)", fontsize=12)
    ax1.set_ylim(0, 100)
    ax1.grid(True)
    ax1.axhline(y=50, color="gray", linestyle="--", alpha=0.7)

    # Add team labels
    ax1.text(
        df["elapsed_time"].max() / 2,
        95,
        home_team,
        fontsize=12,
        ha="center",
        color="blue",
    )
    ax1.text(
        df["elapsed_time"].max() / 2,
        5,
        away_team,
        fontsize=12,
        ha="center",
        color="red",
    )

    # Add quarter lines
    for quarter_end in [720, 1440, 2160]:  # End of Q1, Q2, Q3
        ax1.axvline(x=quarter_end, color="gray", linestyle="-", alpha=0.5)
        ax1.text(quarter_end, 50, f"Q{quarter_end//720}", fontsize=10, ha="center")

    # Plot point margin
    ax2.plot(df["elapsed_time"], df["point_margin"], "g-", linewidth=2)
    ax2.set_xlabel("Game Time (minutes)", fontsize=12)
    ax2.set_ylabel("Point Margin (+ home lead)", fontsize=12)
    ax2.grid(True)
    ax2.axhline(y=0, color="gray", linestyle="--", alpha=0.7)

    # Add quarter lines to second plot too
    for quarter_end in [720, 1440, 2160]:  # End of Q1, Q2, Q3
        ax2.axvline(x=quarter_end, color="gray", linestyle="-", alpha=0.5)

    # Format x-axis to display in minutes
    def format_time(seconds, pos=None):
        m = seconds / 60
        return f"{int(m)}"

    ax2.xaxis.set_major_formatter(plt.FuncFormatter(format_time))

    # Add annotations for key moments (largest swings in win probability)
    df["win_prob_diff"] = df["home_win_prob"].diff().abs()
    key_moments = df.nlargest(5, "win_prob_diff")

    for _, moment in key_moments.iterrows():
        elapsed = moment["elapsed_time"]
        prob = moment["home_win_prob"]
        margin = moment["point_margin"]
        game_time = moment["game_time"]

        # Annotate win probability plot
        ax1.plot(elapsed, prob, "ro", markersize=8)
        ax1.annotate(
            f"{game_time}\nMargin: {margin}",
            (elapsed, prob),
            xytext=(0, 20),
            textcoords="offset points",
            arrowprops=dict(arrowstyle="->", color="red"),
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7),
        )

    plt.tight_layout()

    # Save the plot
    filename = f"nba_game_{game_id}_win_prob.png"
    plt.savefig(filename)
    print(f"Plot saved to {filename}")

    # Show the plot
    plt.show()


def save_win_probability_data(df, game_id):
    """
    Saves win probability data to CSV file.

    Args:
        df (pandas.DataFrame): DataFrame with win probability data
        game_id (str): ESPN's NBA game ID
    """
    if df is None or df.empty:
        print("No data to save")
        return

    filename = f"nba_game_{game_id}_win_prob_data.csv"
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

    # Also save a focused version with just key columns
    focus_cols = [
        "elapsed_time",
        "seconds_left",
        "game_time",
        "home_win_prob",
        "point_margin",
    ]
    df[focus_cols].to_csv(f"nba_game_{game_id}_win_prob_data_focused.csv", index=False)
    print(f"Focused data saved to nba_game_{game_id}_win_prob_data_focused.csv")


def analyze_win_probability(df):
    """
    Analyzes win probability data to find key moments and trends.

    Args:
        df (pandas.DataFrame): DataFrame with win probability data
    """
    if df is None or df.empty:
        print("No data to analyze")
        return

    home_team = df["home_team"].iloc[0]
    away_team = df["away_team"].iloc[0]

    # Calculate win probability changes
    df["win_prob_diff"] = df["home_win_prob"].diff()

    # Find largest swings in win probability
    big_swings = pd.concat(
        [df.nlargest(10, "win_prob_diff"), df.nsmallest(10, "win_prob_diff")]
    )
    big_swings = big_swings.sort_values("elapsed_time")

    print("\nKey Moments (Largest Win Probability Swings):")
    for _, moment in big_swings.iterrows():
        direction = "↑" if moment["win_prob_diff"] > 0 else "↓"
        print(
            f"{moment['game_time']}: {home_team} Win Prob: {moment['home_win_prob']:.1f}% ({direction} {abs(moment['win_prob_diff']):.1f}%), "
            + f"Margin: {moment['point_margin']} pts"
        )

    # Find when win probability crossed 50% (lead changes in win probability)
    df["win_prob_over_50"] = df["home_win_prob"] > 50
    df["win_prob_lead_change"] = df["win_prob_over_50"] != df["win_prob_over_50"].shift(
        1
    )
    win_prob_lead_changes = df[df["win_prob_lead_change"] == True].copy()

    print(f"\nWin Probability Lead Changes: {len(win_prob_lead_changes)}")
    for _, change in win_prob_lead_changes.iterrows():
        leader = home_team if change["home_win_prob"] > 50 else away_team
        print(
            f"{change['game_time']}: {leader} takes the lead in win probability "
            + f"({change['home_win_prob']:.1f}% for {home_team}), Margin: {change['point_margin']} pts"
        )

    # Calculate average win probability by quarter
    df["quarter"] = (df["elapsed_time"] // 720) + 1
    quarter_avg = df.groupby("quarter")["home_win_prob"].mean()

    print("\nAverage Win Probability by Quarter:")
    for quarter, avg_prob in quarter_avg.items():
        print(f"Q{quarter}: {avg_prob:.1f}% for {home_team}")


if __name__ == "__main__":
    # Game ID from April 9, 2025
    GAME_ID = "401705718"

    # Get win probability data
    df = get_nba_win_probability_history(GAME_ID)

    if df is not None:
        # Save data
        save_win_probability_data(df, GAME_ID)

        # Analyze data
        analyze_win_probability(df)

        # Plot data
        plot_win_probability(df)
