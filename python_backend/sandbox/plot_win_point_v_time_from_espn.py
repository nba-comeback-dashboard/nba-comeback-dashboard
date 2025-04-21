import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np


def get_espn_game_data(espn_game_id):
    """Fetch game data from ESPN API."""
    url = f"http://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={espn_game_id}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    return response.json()


def extract_win_probability_data(game_data):
    """Extract win probability data and create a mapping of playId to win probability."""
    win_prob_map = {}

    if "winprobability" not in game_data:
        return win_prob_map

    for entry in game_data["winprobability"]:
        play_id = entry.get("playId")
        home_win_pct = entry.get("homeWinPercentage")
        if play_id is not None and home_win_pct is not None:
            win_prob_map[play_id] = home_win_pct

    return win_prob_map


def create_play_data_with_win_probability(game_data, win_prob_map):
    """Create a DataFrame with play data and win probability."""
    plays = []

    if "plays" not in game_data:
        return pd.DataFrame()

    home_team = (
        game_data.get("header", {})
        .get("competitions", [{}])[0]
        .get("competitors", [{}])[0]
        .get("team", {})
        .get("displayName", "Home")
    )
    away_team = (
        game_data.get("header", {})
        .get("competitions", [{}])[0]
        .get("competitors", [{}])[1]
        .get("team", {})
        .get("displayName", "Away")
    )

    for play in game_data["plays"]:
        play_id = play.get("id")
        if play_id not in win_prob_map:
            continue

        period = play.get("period", {}).get("number", 0)
        clock_minutes = play.get("clock", {}).get("displayValue", "0:00")

        # Convert clock time (MM:SS) to minutes
        if ":" in clock_minutes:
            mins, secs = clock_minutes.split(":")
            clock_in_mins = int(mins) + (int(secs) / 60)
        else:
            clock_in_mins = 0

        # Calculate game time in minutes (each period is 12 minutes in NBA)
        minutes_elapsed = ((period - 1) * 12) + (12 - clock_in_mins)

        home_score = play.get("homeScore", 0)
        away_score = play.get("awayScore", 0)
        point_margin = home_score - away_score

        plays.append(
            {
                "playId": play_id,
                "period": period,
                "clockTime": clock_minutes,
                "minutesElapsed": minutes_elapsed,
                "homeScore": home_score,
                "awayScore": away_score,
                "pointMargin": point_margin,
                "homeWinProbability": win_prob_map[play_id]
                * 100,  # Convert to percentage
            }
        )

    df = pd.DataFrame(plays)
    if not df.empty:
        df = df.sort_values("minutesElapsed")

    return df, home_team, away_team


def plot_win_probability_and_point_margin(df, espn_game_id, home_team, away_team):
    """Plot win probability and point margin vs time."""
    if df.empty:
        print("No data to plot.")
        return

    fig, ax1 = plt.subplots(figsize=(14, 8))

    # Plot win probability on the primary y-axis
    color = "tab:blue"
    ax1.set_xlabel("Minutes Elapsed")
    ax1.set_ylabel("Win Probability (%)", color=color)
    ax1.plot(
        df["minutesElapsed"],
        df["homeWinProbability"],
        color=color,
        label=f"{home_team} Win Probability",
    )
    ax1.plot(
        df["minutesElapsed"],
        100 - df["homeWinProbability"],
        color="tab:red",
        label=f"{away_team} Win Probability",
    )
    ax1.tick_params(axis="y", labelcolor=color)
    ax1.set_ylim(0, 100)
    ax1.axhline(y=50, color="black", linestyle="--", alpha=0.3)
    ax1.grid(True, alpha=0.3)

    # Create a twin axis for point margin
    ax2 = ax1.twinx()
    color = "tab:green"
    ax2.set_ylabel("Point Margin (Home - Away)", color=color)
    ax2.plot(df["minutesElapsed"], df["pointMargin"], color=color, label="Point Margin")
    ax2.tick_params(axis="y", labelcolor=color)
    ax2.axhline(y=0, color="black", linestyle="--", alpha=0.3)

    # Add vertical lines for period changes
    for period in range(2, 5):  # Periods 2, 3, 4
        period_start = (period - 1) * 12
        plt.axvline(x=period_start, color="gray", linestyle="-", alpha=0.5)
        plt.text(
            period_start,
            ax1.get_ylim()[1],
            f" Period {period}",
            verticalalignment="top",
        )

    # Add potential overtime periods
    if df["period"].max() > 4:
        for ot in range(1, df["period"].max() - 3):
            ot_start = 48 + (ot - 1) * 5  # Each OT is 5 minutes
            plt.axvline(x=ot_start, color="gray", linestyle="-", alpha=0.5)
            plt.text(ot_start, ax1.get_ylim()[1], f" OT{ot}", verticalalignment="top")

    # Combine legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.title(
        f"Win Probability and Point Margin - {home_team} vs {away_team} (Game ID: {espn_game_id})"
    )
    plt.tight_layout()

    # Save the plot and data
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    plt.savefig(f"nba_game_{espn_game_id}_win_prob_{timestamp}.png")
    df.to_csv(f"nba_game_{espn_game_id}_win_prob_{timestamp}.csv", index=False)

    return fig


def main():
    # Test with the specified ESPN Game ID
    espn_game_id = "401705718"
    espn_game_id = "401767823"

    print(f"Fetching data for ESPN Game ID: {espn_game_id}")
    game_data = get_espn_game_data(espn_game_id)

    print("Extracting win probability data...")
    win_prob_map = extract_win_probability_data(game_data)
    print(f"Found {len(win_prob_map)} win probability data points")

    print("Creating play-by-play data with win probability...")
    df, home_team, away_team = create_play_data_with_win_probability(
        game_data, win_prob_map
    )
    print(f"Created dataset with {len(df)} plays")

    if not df.empty:
        print(f"Game: {home_team} vs {away_team}")

        # Save full dataset
        df.to_csv(f"nba_game_{espn_game_id}_win_prob_data.csv", index=False)

        # Create a more focused dataset with just the key columns
        focused_df = df[
            ["minutesElapsed", "homeWinProbability", "pointMargin", "period"]
        ]
        focused_df.to_csv(
            f"nba_game_{espn_game_id}_win_prob_data_focused.csv", index=False
        )

        print("Plotting win probability and point margin...")
        fig = plot_win_probability_and_point_margin(
            df, espn_game_id, home_team, away_team
        )
        plt.show()
    else:
        print("No data found for the specified game.")


if __name__ == "__main__":
    main()
