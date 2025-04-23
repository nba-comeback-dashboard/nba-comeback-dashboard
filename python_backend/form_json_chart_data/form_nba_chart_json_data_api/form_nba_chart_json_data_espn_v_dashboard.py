# form_nba_chart_json_data_espn_v_dashboard.py
"""
Module for handling ESPN win probability data and dashboard comparison.

This module provides functionality to fetch ESPN win probability data and
compare it with NBA Dashboard probability calculations. It includes classes and
functions for creating visualization JSON data that shows the comparison between
ESPN's predicted win probabilities and those calculated using the NBA Dashboard.
"""

# Standard library imports
import json
import os
import gzip
import datetime
from typing import Tuple, List, Dict, Any, Optional

# Third-party imports
import requests
import numpy as np
from scipy.interpolate import interp1d
from scipy.stats import norm

# Local imports
from form_nba_chart_json_data_season_game_loader import (
    TIME_TO_INDEX_MAP,
    GAME_MINUTES,
    Games,
)
from form_nba_chart_json_data_plot_primitives import PlotLine, FinalPlot
from form_nba_chart_json_data_num import Num

# Import from global variable
import form_nba_chart_json_data_season_game_loader as loader


class EspnLine(PlotLine):
    """
    Represents a line plotting ESPN win probability versus time.

    This class handles ESPN win probability data and formats it for visualization.
    """

    def __init__(
        self,
        legend: str,
        x_values: List[float],
        y_values: List[float],
        point_margins: List[float],
        team_name: str,
    ):
        """
        Initialize a line for ESPN win probability.

        Parameters:
        -----------
        legend : str
            Legend text for the line
        x_values : list
            List of time points (minutes elapsed)
        y_values : list
            List of win probability percentages
        team_name : str
            Name of the team this probability is for
        """
        self.legend = legend
        self.x_values = x_values
        self.y_values = y_values
        self.point_margins = point_margins
        self.team_name = team_name
        self.number_of_games = 1  # Always 1 for ESPN data

    def get_xy(self):
        """
        Get x and y values for plotting.

        Returns:
        --------
        tuple
            (x_values, y_values) where x_values are time points and
            y_values are win probabilities
        """
        return self.x_values, self.y_values

    def to_json(self, calculate_occurrences=False):
        """
        Convert line data to JSON format.

        Creates a structured JSON representation of the line data
        suitable for rendering in the frontend.

        Parameters:
        -----------
        calculate_occurrences : bool
            Parameter for compatibility with PointsDownLine.to_json()
            (not used in this class)

        Returns:
        --------
        dict
            JSON-serializable dictionary of line data
        """
        from scipy.stats import norm

        json_data = {
            "legend": self.legend,
            "team_name": self.team_name,
            "line_type": "live-data",
        }

        # Convert to native Python types for JSON serialization
        json_data["x_values"] = [float(x) for x in self.x_values]
        json_data["y_values"] = y_values = []

        sign = -1  # Hard coded right now for looking at away team.
        for index, y_value in enumerate(self.y_values):
            # y_value is already in sigma space after the transformation in plot_espn_versus_dashboard
            # Convert sigma back to probability for percent field
            percent = norm.cdf(float(y_value))

            point_json = {
                "x_value": float(self.x_values[index]),
                "y_value": float(y_value),
                "point_margin": int(sign * self.point_margins[index]),
                "percent": percent,  # Already in 0-1 decimal format
            }
            y_values.append(point_json)

        return json_data


class DashboardLine(PlotLine):
    """
    Represents a line plotting Dashboard win probability versus time.

    This class calculates win probability based on NBA Dashboard data and
    formats it for visualization.
    """

    def __init__(
        self,
        legend,
        x_values,
        y_values,
        point_margins,
        team_name,
        start_year,
        stop_year,
        use_home_away_game_filter,
    ):
        """
        Initialize a line for Dashboard win probability.

        Parameters:
        -----------
        legend : str
            Legend text for the line
        x_values : list
            List of time points (minutes elapsed)
        y_values : list
            List of win probability percentages
        team_name : str
            Name of the team this probability is for
        url : str
            URL to link to for this line's data source
        game_filter : GameFilter or None
            Filter that was applied to games for this line
        """
        self.legend = legend
        self.x_values = x_values
        self.y_values = y_values
        self.point_margins = point_margins
        self.team_name = team_name
        self.start_year = start_year
        self.stop_year = stop_year
        self.use_home_away_game_filter = use_home_away_game_filter
        self.number_of_games = 0  # Will be set based on data

    def get_xy(self):
        """
        Get x and y values for plotting.

        Returns:
        --------
        tuple
            (x_values, y_values) where x_values are time points and
            y_values are win probabilities
        """
        return self.x_values, self.y_values

    def to_json(self, calculate_occurrences=False):
        """
        Convert line data to JSON format.

        Creates a structured JSON representation of the line data
        suitable for rendering in the frontend.

        Parameters:
        -----------
        calculate_occurrences : bool
            Parameter for compatibility with PointsDownLine.to_json()
            (not used in this class)

        Returns:
        --------
        dict
            JSON-serializable dictionary of line data
        """
        from scipy.stats import norm

        json_data = {
            "legend": self.legend,
            "team_name": self.team_name,
            "line_type": "dashboard",
        }

        # if self.game_filter:
        #    json_data["filter_string"] = self.game_filter.get_filter_string()

        # Convert to native Python types for JSON serialization
        json_data["x_values"] = [float(x) for x in self.x_values]
        json_data["y_values"] = y_values = []

        # Base URL parameters
        plot_type = "2"  # Default: Points Down At Time plot
        if str(self.start_year).startswith("R"):
            seasons = f"{self.start_year[1:]}-{self.stop_year}-R"
        elif str(self.start_year).startswith("P"):
            seasons = f"{self.start_year[1:]}-{self.stop_year}-P"
        else:
            seasons = f"{self.start_year}-{self.stop_year}-B"

        mode = "auto"  # Auto mode

        # Hard coded right now for looking at away team.
        sign = -1

        for index, y_value in enumerate(self.y_values):
            # y_value is already in sigma space after the transformation in plot_espn_versus_dashboard
            # Convert sigma back to probability for percent field
            percent = norm.cdf(float(y_value))

            # Get the time value for this point and format it for URL
            x_value = float(self.x_values[index])
            time_param = self._format_time_for_url(x_value)

            point_margin = self.point_margins[index] * sign

            if self.use_home_away_game_filter is False:
                url = f"p={plot_type}&t={time_param}&s={seasons}"
            else:
                if point_margin <= 0:
                    game_filter = "ANY-a-ANY"
                else:
                    game_filter = "ANY-h-ANY"
                url = (
                    f"p={plot_type}&t={time_param}&s={seasons}&g={game_filter}&m={mode}"
                )

            point_json = {
                "x_value": x_value,
                "y_value": float(y_value),
                "point_margin": int(point_margin),
                "percent": percent,  # Already in 0-1 decimal format
                "url": url,
            }
            y_values.append(point_json)

        return json_data

    def _format_time_for_url(self, time_remaining):
        """
        Format time remaining for URL parameter.

        Converts the remaining time into the appropriate URL parameter format.
        For sub-minute times in the final minute, uses special second formats.

        Parameters:
        -----------
        time_remaining : float
            Time remaining in minutes

        Returns:
        --------
        str
            Formatted time string for URL
        """
        # Check if time is within the final minute
        if 0 < time_remaining <= 1:
            # Calculate seconds remaining
            seconds_remaining = int(time_remaining * 60)

            # Special handling for specific second intervals
            if 44 <= seconds_remaining <= 46:
                return "45s"
            elif 29 <= seconds_remaining <= 31:
                return "30s"
            elif 14 <= seconds_remaining <= 16:
                return "15s"
            elif 9 <= seconds_remaining <= 11:
                return "10s"
            elif 4 <= seconds_remaining <= 6:
                return "5s"
            elif seconds_remaining < 3:
                return "0"  # End of regulation
            else:
                # For other seconds in the final minute, return the minute remaining
                return "1"
        elif time_remaining <= 0:
            # Overtime handling
            ot_period = 1 + int(abs(time_remaining) / 5)
            minutes_in_ot = abs(time_remaining) % 5

            if minutes_in_ot > 4.9:  # Very end of OT
                return f"{ot_period}OT-0"
            else:
                minutes_remaining = 5 - minutes_in_ot
                return f"{ot_period}OT-{int(minutes_remaining)}"
        else:
            # Regular game time (return minutes remaining)
            return str(int(time_remaining))


def get_espn_game_data(espn_game_id: str) -> dict:
    """
    Fetch game data from ESPN API.

    Parameters:
    -----------
    espn_game_id : str
        ESPN game ID to fetch data for

    Returns:
    --------
    dict
        JSON response from ESPN API containing game data

    Raises:
    -------
    Exception
        If the API request fails
    """
    url = f"http://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={espn_game_id}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    return response.json()


def extract_win_probability_data(game_data: dict) -> dict:
    """
    Extract win probability data and create a mapping of playId to win probability.

    Parameters:
    -----------
    game_data : dict
        Game data from ESPN API

    Returns:
    --------
    dict
        Mapping of play IDs to home win percentages
    """
    win_prob_map = {}

    if "winprobability" not in game_data:
        return win_prob_map

    for entry in game_data["winprobability"]:
        play_id = entry.get("playId")
        home_win_pct = entry.get("homeWinPercentage")
        if play_id is not None and home_win_pct is not None:
            win_prob_map[play_id] = home_win_pct

    return win_prob_map


def create_play_data_with_win_probability(
    game_data: dict, win_prob_map: dict
) -> Tuple[List[Dict[str, Any]], str, str, str]:
    """
    Create structured play data with win probability from ESPN game data.

    Parameters:
    -----------
    game_data : dict
        Game data from ESPN API
    win_prob_map : dict
        Mapping of play IDs to win percentages

    Returns:
    --------
    tuple
        (plays, home_team, away_team, game_date) where:
        - plays is a list of dictionaries containing play data
        - home_team is the home team name
        - away_team is the away team name
        - game_date is the formatted game date
    """
    plays = []

    if "plays" not in game_data:
        return plays, "", "", ""

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
    if "date" in competitions:
        game_date = competitions["date"]
        try:
            # Convert from ISO format to readable date
            game_date = datetime.datetime.fromisoformat(
                game_date.replace("Z", "+00:00")
            ).strftime("%B %d, %Y")
        except ValueError:
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

        # Calculate game time in minutes (each period is 12 minutes in NBA, OT is 5 min)
        if period <= 4:  # Regular periods
            minutes_elapsed = ((period - 1) * 12) + (12 - clock_in_mins)
        else:  # Overtime periods
            minutes_elapsed = 48 + ((period - 5) * 5) + (5 - clock_in_mins)

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

        # Filter plays to keep only the last entry for each unique minutesElapsed.
        # This ensures we get the final score and probability for a given time point,
        # which is important for situations like free throws where multiple plays
        # can occur at the same time but we want the final state after all plays.
        plays_by_time = {}
        for play in plays:
            plays_by_time[play["minutesElapsed"]] = play
        plays = list(plays_by_time.values())

        # Sort by time
        plays.sort(key=lambda x: x["minutesElapsed"])

    return plays, home_team, away_team, game_date


def get_team_nickname(team_name: str) -> str:
    """
    Extract team nickname from full team name.

    Parameters:
    -----------
    team_name : str
        Full team name

    Returns:
    --------
    str
        Team nickname (e.g., "Timberwolves" from "Minnesota Timberwolves")
    """
    # Special case for Trail Blazers
    if "Trail Blazers" in team_name:
        return "Trail Blazers"
    # Special case for 76ers
    if "76ers" in team_name:
        return "76ers"

    # For most teams, the nickname is the last word
    parts = team_name.split()
    if len(parts) > 1:
        return parts[-1]
    return team_name  # Return original if can't extract


def get_team_abbreviation(team_name: str) -> str:
    """
    Convert team name to abbreviation.

    Parameters:
    -----------
    team_name : str
        Full team name

    Returns:
    --------
    str
        Team abbreviation
    """
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


def create_dashboard_time_vector() -> List:
    """
    Create a time vector for dashboard data that matches API time points.

    Returns:
    --------
    list
        List of time points for dashboard analysis, from 36 minutes to end of regulation
        and optionally overtimes
    """
    # Start with regular time points from 36 minutes to 1 minute
    time_vector = list(range(36, 0, -1))

    # Add sub-minute time points for final minute
    time_vector.extend(["45s", "30s", "15s", "10s", "5s", 0])

    return time_vector


def extend_time_vector_for_overtime(time_vector: List, max_period: int) -> List:
    """
    Extend the time vector to include overtime periods if needed.

    Parameters:
    -----------
    time_vector : list
        Base time vector
    max_period : int
        Maximum period number in the game data

    Returns:
    --------
    list
        Extended time vector including overtime periods if needed
    """
    extended_vector = time_vector.copy()

    # Add overtime periods if needed (each OT is 5 minutes)
    if max_period > 4:
        num_ots = max_period - 4
        for ot in range(1, num_ots + 1):
            # For each overtime, add time points 5, 4, 3, 2, 1, "45s", "30s", "15s", "10s", "5s", 0
            ot_times = list(range(5, 0, -1))
            ot_times.extend(["45s", "30s", "15s", "10s", "5s", 0])
            # Map these to the correct elapsed time
            ot_base = 48 + (ot - 1) * 5
            extended_vector.extend([f"{ot}OT-{t}" for t in ot_times])

    return extended_vector


def calculate_dashboard_probability(
    time_point,
    point_margin,
    start_year,
    stop_year,
    game_filter,
    season_type,
):
    """
    Calculate win probability using NBA Dashboard methodology.

    Uses PointsDownLine to get the linear regression coefficients for the
    specified time point and game filter, then calculates the win probability
    for the given point margin.

    Parameters:
    -----------
    game_filter : GameFilter
        Filter to apply to games
    time_point : int
        Time point to calculate probability for (minutes remaining)
    point_margin : float
        Current point margin (positive for home team leading)
    start_year : int
        Start year for data analysis
    stop_year : int
        End year for data analysis

    Returns:
    --------
    float
        Win probability as a percentage (0-100)
    """
    # Import here to avoid circular import
    from form_nba_chart_json_data_api import PointsDownLine

    # Load games with appropriate filter
    games = Games(
        start_year=start_year,
        stop_year=stop_year,
        season_type=season_type,
    )

    # Create PointsDownLine for this time point
    points_down_line = PointsDownLine(
        games=games,
        game_filter=game_filter,
        start_time=time_point,
        down_mode="at",
        max_point_margin=-1,
        fit_max_points=-1,
    )

    # Calculate win probability using regression coefficients
    sigma = points_down_line.m * -1.0 * abs(point_margin) + points_down_line.b
    percent = norm.cdf(sigma)

    # Adjust based on which team is leading
    if point_margin < 0:
        percent = 1.0 - percent

    return percent * 100.0  # Convert to percentage


def get_dashboard_win_probability(
    plays,
    start_year,
    stop_year,
    season_type,
    use_home_away_game_filter,
):
    """
    Calculate Dashboard win probability for the game plays.

    Parameters:
    -----------
    plays : list
        List of play dictionaries with time and point margin data
    use_home_away_game_filter : bool
        Whether to apply home/away game filter based on point margin
    modern_era : bool
        Whether to use only modern era games (2017-2024) for analysis

    Returns:
    --------
    tuple
        (times, probabilities) arrays of time points and corresponding win probabilities
    """
    # Import here to avoid circular import
    from form_nba_chart_json_data_api import GameFilter

    # Extract time and point margin data
    time_minutes = np.array([play["minutesElapsed"] for play in plays])
    point_margin = np.array([play["pointMargin"] for play in plays])

    # Create interpolation function for point margin
    point_fn = interp1d(
        time_minutes,
        point_margin,
        bounds_error=False,
        kind="previous",
        fill_value=(point_margin[0], point_margin[-1]),
    )

    probabilities = []
    times = []

    # Calculate probability at each minute
    point_margin_used = []
    for t in range(
        18, 48
    ):  # 18 to 47 minutes elapsed (excluding the final minute for now)
        current_time = 48.0 - t  # Convert to minutes remaining
        current_margin = point_fn(t)

        # home_rank = "top_5"
        # away_rank = "mid_10"
        # Create appropriate game filter
        if use_home_away_game_filter:
            if current_margin <= 0:  # Away team leading
                game_filter = GameFilter(
                    for_at_home=True,
                    # for_rank=home_rank,
                    # vs_rank=away_rank,
                )  # For home team trailing
            else:  # Home team leading
                game_filter = GameFilter(
                    for_at_home=False,
                    # for_rank=away_rank,
                    # vs_rank=home_rank,
                )  # For away team trailing
        else:
            game_filter = None

        # Calculate probability using Dashboard method
        probability = calculate_dashboard_probability(
            time_point=current_time,
            point_margin=current_margin,
            start_year=start_year,
            stop_year=stop_year,
            season_type=season_type,
            game_filter=game_filter,
        )

        probabilities.append(float(probability))  # Convert numpy types to Python float
        times.append(int(t))  # Convert numpy types to Python int
        point_margin_used.append(current_margin)

    # Special handling for the final minute with sub-minute intervals
    sub_minute_times = {
        "45s": 47.25,  # 45 seconds remaining in final minute (47 + 0.25)
        "30s": 47.5,  # 30 seconds remaining in final minute (47 + 0.5)
        "15s": 47.75,  # 15 seconds remaining in final minute (47 + 0.75)
        "10s": 47.833,  # 10 seconds remaining in final minute (47 + 0.833)
        "5s": 47.917,  # 5 seconds remaining in final minute (47 + 0.917)
        0: 48.0,  # End of game
    }

    # Create a simple linear interpolation between the point margins at minute 47 and the final margin
    for time_point, x_value in sub_minute_times.items():
        point_margin = point_fn(x_value)
        point_margin_used.append(point_margin)

        # Create appropriate game filter
        if use_home_away_game_filter:
            if point_margin <= 0:  # Away team leading
                game_filter = GameFilter(for_at_home=True)  # For home team trailing
            else:  # Home team leading
                game_filter = GameFilter(for_at_home=False)  # For away team trailing
        else:
            game_filter = None

        # Calculate probability
        probability = calculate_dashboard_probability(
            time_point=time_point,
            point_margin=point_margin,
            start_year=start_year,
            stop_year=stop_year,
            season_type=season_type,
            game_filter=game_filter,
        )

        probabilities.append(float(probability))
        times.append(float(x_value))  # Use the exact x_value for plotting

    # Sort by time
    paired_data = sorted(zip(times, probabilities), key=lambda x: x[0])
    times = [t for t, _ in paired_data]
    probabilities = [p for _, p in paired_data]

    return times, probabilities, point_margin_used
