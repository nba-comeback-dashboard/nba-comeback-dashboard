import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
import json
import os


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

    header = game_data.get("header", {})
    competitions = header.get("competitions", [{}])[0]

    home_team = (
        competitions.get("competitors", [{}])[0]
        .get("team", {})
        .get("displayName", "Home")
    )
    away_team = (
        competitions.get("competitors", [{}])[1]
        .get("team", {})
        .get("displayName", "Away")
    )

    # Extract game date
    game_date = ""
    if "header" in game_data:
        header = game_data["header"]
        if "competitions" in header and len(header["competitions"]) > 0:
            competition = header["competitions"][0]
            if "date" in competition:
                game_date = competition["date"]
                try:
                    # Convert from ISO format to readable date
                    game_date = datetime.datetime.fromisoformat(
                        game_date.replace("Z", "+00:00")
                    ).strftime("%B %d, %Y")
                except ValueError as e:
                    print(f"Error parsing date: {e}")
                    print(f"Raw date string: {game_date}")
                    game_date = "Unknown Date"

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

    return df, home_team, away_team, game_date


def get_team_abbreviation(team_name):
    """Convert team name to abbreviation."""
    team_abbr_map = {
        "Atlanta Hawks": "ATL",
        "Boston Celtics": "BOS",
        "Brooklyn Nets": "BKN",
        "Charlotte Hornets": "CHA",
        "Chicago Bulls": "CHI",
        "Cleveland Cavaliers": "CLE",
        "Dallas Mavericks": "DAL",
        "Denver Nuggets": "DEN",
        "Detroit Pistons": "DET",
        "Golden State Warriors": "GSW",
        "Houston Rockets": "HOU",
        "Indiana Pacers": "IND",
        "Los Angeles Clippers": "LAC",
        "Los Angeles Lakers": "LAL",
        "Memphis Grizzlies": "MEM",
        "Miami Heat": "MIA",
        "Milwaukee Bucks": "MIL",
        "Minnesota Timberwolves": "MIN",
        "New Orleans Pelicans": "NOP",
        "New York Knicks": "NYK",
        "Oklahoma City Thunder": "OKC",
        "Orlando Magic": "ORL",
        "Philadelphia 76ers": "PHI",
        "Phoenix Suns": "PHX",
        "Portland Trail Blazers": "POR",
        "Sacramento Kings": "SAC",
        "San Antonio Spurs": "SAS",
        "Toronto Raptors": "TOR",
        "Utah Jazz": "UTA",
        "Washington Wizards": "WAS",
    }
    return team_abbr_map.get(team_name, team_name[:3].upper())


def format_date_for_filename(date_str):
    """Convert date string to YYYY_MM_DD format."""
    try:
        # Try parsing the date in the format "Month DD, YYYY"
        date_obj = datetime.datetime.strptime(date_str, "%B %d, %Y")
        return date_obj.strftime("%Y_%m_%d")
    except ValueError:
        # If parsing fails, return a sanitized version of the input
        return date_str.replace("/", "_").replace("-", "_")


def save_live_probability_plot(fig, away_team, home_team, game_date):
    """Save the live probability plot with standardized naming convention."""
    # Get team abbreviations
    away_abbr = get_team_abbreviation(away_team)
    home_abbr = get_team_abbreviation(home_team)

    # Format the date
    date_str = format_date_for_filename(game_date)

    # Create the filename
    filename = f"goto_{away_abbr}_{home_abbr}_{date_str}_live_prob.png"

    # Create the full path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(
        script_dir, "../../docs/frontend/source/analysis/", filename
    )
    abs_save_path = os.path.abspath(save_path)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(abs_save_path), exist_ok=True)

    # Save the figure
    fig.savefig(abs_save_path, dpi=300, bbox_inches="tight")
    print(f"Saved plot to absolute path: {abs_save_path}")


def plot_win_probability_and_point_margin(
    df,
    espn_game_id,
    home_team,
    away_team,
    game_date,
    show_team="away",
    save_files=False,
    colors=None,
    start_time=18,
):
    """Plot win probability and point margin vs time.

    Args:
        df: DataFrame containing the game data
        espn_game_id: ESPN game ID
        home_team: Name of home team
        away_team: Name of away team
        game_date: Date of the game
        show_team: Which team's win probability to show ('both', 'home', or 'away')
        save_files: Whether to save plot and data files (default: False)
        colors: List of colors for the lines in order [home, point_margin, away]
               Default is ['tab:blue', 'tab:green', 'tab:red']
        start_time: Time in minutes to start the plot from (default: 18)
    """
    if df.empty:
        print("No data to plot.")
        return

    # Filter data to only include times >= start_time and <= 48
    df = df[(df["minutesElapsed"] >= start_time) & (df["minutesElapsed"] <= 48)].copy()

    # Set default colors if not provided
    if colors is None:
        colors = ["tab:blue", "tab:green", "tab:red"]

    print(f"Using colors: {colors}")  # Debug print

    # Set a modern font
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]
    plt.rcParams["font.weight"] = "bold"

    fig, ax1 = plt.subplots(figsize=(14, 8))

    # Plot win probability on the primary y-axis
    ax1.set_xlabel("Minutes Elapsed", color="black")
    ax1.set_ylabel("Win Probability (%)", color="black")

    # Create lines list to store plot objects
    lines = []

    # Plot home team first (should be blue)
    if show_team in ["both", "home"]:
        print(f"Plotting home team with color: {colors[0]}")  # Debug print
        (line1,) = ax1.plot(
            df["minutesElapsed"],
            df["homeWinProbability"],
            color=colors[0],  # Should be blue
            label=f"{home_team} Win Probability",
            linewidth=4.0,
            alpha=0.5,
        )
        lines.append(line1)

    # Plot away team second (should be red)
    if show_team in ["both", "away"]:
        print(f"Plotting away team with color: {colors[2]}")  # Debug print
        (line2,) = ax1.plot(
            df["minutesElapsed"],
            100 - df["homeWinProbability"],
            color=colors[2],  # Should be red
            label=f"{away_team} ESPN Win Probability",
            linewidth=4.0,
            alpha=0.5,
        )
        lines.append(line2)

    # Calculate and plot dashboard probabilities
    time_minutes, dashboard_prop = get_dashboard_prob(
        df["minutesElapsed"], df["pointMargin"], modern=False, use_game_filter=False
    )

    # Filter dashboard points to only show up to 48 minutes
    mask = time_minutes <= 48
    time_minutes = time_minutes[mask]
    dashboard_prop = dashboard_prop[mask]

    (line3,) = ax1.plot(
        time_minutes,
        dashboard_prop,
        "ro",
        label=f"{away_team} Dashboard Win Probability All Games",
        linewidth=8.0,
        alpha=0.5,
    )
    lines.append(line3)

    # Calculate and plot dashboard probabilities
    time_minutes, dashboard_prop = get_dashboard_prob(
        df["minutesElapsed"], df["pointMargin"], modern=True, use_game_filter=True
    )

    # Filter dashboard points to only show up to 48 minutes
    mask = time_minutes <= 48
    time_minutes = time_minutes[mask]
    dashboard_prop = dashboard_prop[mask]

    (line3,) = ax1.plot(
        time_minutes,
        dashboard_prop,
        "co",
        label=f"{away_team} Dashboard Win Probability Modern @Home/Away",
        linewidth=8.0,
        alpha=0.5,
    )
    lines.append(line3)

    ax1.tick_params(axis="y", colors="black")
    ax1.set_ylim(-5, 125)  # Add 5% padding at bottom and 25% at top
    ax1.set_xlim(start_time, 48)  # Set x-axis to end at 48 minutes

    # Set y-axis ticks every 10%
    ax1.set_yticks(range(0, 126, 10))

    # Add sub-grids every 5%
    ax1.set_yticks(range(0, 126, 5), minor=True)
    ax1.grid(True, alpha=0.5)  # Increased from 0.3 to 0.5 for major grid
    ax1.grid(True, which="minor", alpha=0.4)  # Increased from 0.2 to 0.4 for minor grid

    ax1.axhline(y=50, color="black", linestyle="--", alpha=0.3)

    # Create a twin axis for point margin (should be green)
    ax2 = ax1.twinx()
    ax2.set_ylabel("Point Margin (Home - Away)", color="black")
    print(f"Plotting point margin with color: {colors[1]}")  # Debug print
    (line4,) = ax2.plot(
        df["minutesElapsed"],
        df["pointMargin"],
        color=colors[1],  # Should be green
        label="Point Margin",
        linewidth=4.0,
        alpha=0.5,
    )
    lines.append(line4)
    ax2.tick_params(axis="y", colors="black")
    ax2.axhline(y=0, color="black", linestyle="--", alpha=0.3)

    # Add vertical lines for period changes (only for periods after start_time)
    for period in range(2, 5):  # Periods 2, 3, 4
        period_start = (period - 1) * 12
        if period_start >= start_time:  # Only plot if after start_time
            plt.axvline(x=period_start, color="gray", linestyle="-", alpha=0.5)

    # Add potential overtime periods
    if df["period"].max() > 4:
        for ot in range(1, df["period"].max() - 3):
            ot_start = 48 + (ot - 1) * 5  # Each OT is 5 minutes
            if ot_start >= start_time:  # Only plot if after start_time
                plt.axvline(x=ot_start, color="gray", linestyle="-", alpha=0.5)

    # Create legend with all lines
    ax1.legend(lines, [line.get_label() for line in lines], loc="upper left")

    plt.title(
        f"Win Probability and Point Margin - {away_team} @ {home_team} ({game_date})"
    )
    plt.tight_layout()

    # Save the plot and data only if save_files is True
    if save_files:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.savefig(f"nba_game_{espn_game_id}_win_prob_{timestamp}.png")
        df.to_csv(f"nba_game_{espn_game_id}_win_prob_{timestamp}.csv", index=False)
        print(f"Saved plot and data files with timestamp: {timestamp}")

        # Save the standardized version
        save_live_probability_plot(fig, away_team, home_team, game_date)

    return fig


def main():
    # Test with the specified ESPN Game ID
    # espn_game_id = "401705718"  # min v bucks
    espn_game_id = "401767823"  # gsw v houston
    # espn_game_id = "401705392"  # okc v minn
    # espn_game_id = "401705755"  # ind v clev
    # espn_game_id = "401766459"  # mem gsw
    # espn_game_id = "401705066"
    # espn_game_id = "401704734"
    # espn_game_id = "401585795"  # cle at nyk
    # espn_game_id = "401704988"  # minn @ houston

    # Configure which team's win probability to show
    show_team = "away"  # Options: 'both', 'home', 'away'

    # Configure whether to save output files
    files = True  # Set to True to save plot and data files

    # Configure line colors (optional)
    colors = ["tab:red", "tab:green", "tab:blue"]  # Default colors

    # Configure start time for the plot
    start_time = 18  # Start the plot from this many minutes

    print(f"Fetching data for ESPN Game ID: {espn_game_id}")
    game_data = get_espn_game_data(espn_game_id)

    # Debug print the header structure
    if "header" in game_data:
        print("\nHeader structure:")
        print(json.dumps(game_data["header"], indent=2))

    print("Extracting win probability data...")
    win_prob_map = extract_win_probability_data(game_data)
    print(f"Found {len(win_prob_map)} win probability data points")

    print("Creating play-by-play data with win probability...")
    df, home_team, away_team, game_date = create_play_data_with_win_probability(
        game_data, win_prob_map
    )
    print(f"Created dataset with {len(df)} plays")
    print(f"Game date: {game_date}")

    if not df.empty:
        print(f"Game: {home_team} vs {away_team} on {game_date}")

        # Save full dataset only if files is True
        if files:
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
            df,
            espn_game_id,
            home_team,
            away_team,
            game_date,
            show_team,
            save_files,
            colors,
            start_time,
        )
        plt.show()
    else:
        print("No data found for the specified game.")


import sys
import os

# Add the API directory to the path using relative path from script location
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
form_nba_chart_json_data_api_dir = os.path.join(
    parent_dir, "form_json_chart_data/form_nba_chart_json_data_api"
)
sys.path.append(form_nba_chart_json_data_api_dir)

# Import API functions
from form_nba_chart_json_data_api import (
    plot_biggest_deficit,
    # plot_percent_versus_time,
    GameFilter,
    Games,
    PointsDownLine,
)

# Calculate script directory from __file__
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Script directory: {script_dir}")

# Change working directory to the script's location
os.chdir(script_dir)
print(f"Working directory changed to: {os.getcwd()}")
# Base paths for input and output files
json_base_path = "../../docs/frontend/source/_static/json/seasons"

import form_nba_chart_json_data_season_game_loader as loader

# Convert relative json_base_path to an absolute path
json_base_path = os.path.abspath(os.path.join(script_dir, json_base_path))
loader.json_base_path = json_base_path


def get_dashboard_prob(time_minutes, point_margin, modern=False, use_game_filter=False):
    from scipy.interpolate import interp1d
    import numpy as np

    time_minutes = np.array(time_minutes)
    point_margin = np.array([float(x) for x in list(point_margin)])

    if modern:
        eras_one = [
            # ERA ONE
            (2017, 2024),
            # (1996, 2024),
        ]
    else:
        eras_one = [
            # ERA ONE
            (1996, 2024),
        ]

    # Round the time values to avoid floating point issues
    time_minutes = np.round(time_minutes, decimals=6)
    point_margin = np.round(point_margin, decimals=6)

    point_fn = interp1d(
        time_minutes,
        point_margin,
        bounds_error=False,
        kind="previous",
        fill_value=(point_margin[0], point_margin[-1]),
    )

    from scipy.stats import norm

    probabilities = []
    times = []

    for t in range(18, 48, 1):
        current_time = 48.0 - t
        current_margin = point_fn(t)

        if use_game_filter:
            if current_margin <= 0:
                for_at_home = True
            else:
                for_at_home = False

            game_filter = GameFilter(for_at_home=for_at_home)
        else:
            game_filter = None

        games = Games(
            start_year=eras_one[0][0],
            stop_year=eras_one[0][1],
        )
        points_down_line = PointsDownLine(
            games=games,
            game_filter=game_filter,
            start_time=current_time,
            down_mode="at",
            max_point_margin=-1,
            fit_max_points=-1,
        )
        sigma = points_down_line.m * -1.0 * abs(current_margin) + points_down_line.b
        percent = norm.cdf(sigma)

        if current_margin <= 0:
            percent = 1.0 - percent

        probabilities.append(percent * 100.0)
        times.append(t)

    return np.array(times), np.array(probabilities)


if __name__ == "__main__":
    main()
