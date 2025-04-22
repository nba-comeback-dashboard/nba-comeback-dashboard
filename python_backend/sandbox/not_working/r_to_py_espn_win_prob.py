import requests
import pandas as pd
import json
import time
from typing import Dict, Any, Optional


def espn_nba_wp(game_id: int) -> pd.DataFrame:
    """
    Get NBA win probability chart data from ESPN

    Parameters
    ----------
    game_id : int
        Game ID filter for querying a single game

    Returns
    -------
    pd.DataFrame
        A data frame with 21 variables:
        - game_id: numeric
        - play_id: character
        - home_win_percentage: numeric
        - away_win_percentage: numeric
        - tie_percentage: numeric
        - sequence_number: character
        - text: character
        - away_score: integer
        - home_score: integer
        - scoring_play: logical
        - score_value: integer
        - participants: list
        - shooting_play: logical
        - type_id: character
        - type_text: character
        - period_number: integer
        - period_display_value: character
        - clock_display_value: character
        - team_id: character
        - coordinate_x: integer
        - coordinate_y: integer

    Examples
    --------
    >>> espn_nba_wp(game_id=401283399)
    """

    espn_game_id = game_id
    espn_wp = pd.DataFrame()

    try:
        # Make the API request
        response = requests.get(
            f"http://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={espn_game_id}"
        )
        response.raise_for_status()  # Raise error for bad responses

        # Parse the JSON response
        data = response.json()

        # Extract win probability data
        espn_wp_vals = pd.json_normalize(data.get("winprobability", []))
        if espn_wp_vals.empty:
            print(
                f"{time.ctime()}: game_id '{espn_game_id}' invalid or no ESPN win probability data available!"
            )
            return pd.DataFrame()

        # Convert column names to snake_case
        espn_wp_vals.columns = [
            col.lower().replace(".", "_") for col in espn_wp_vals.columns
        ]

        # Extract plays data and convert to DataFrame
        plays_data = data.get("plays", [])
        espn_plays = pd.json_normalize(plays_data)

        # Convert column names to snake_case
        espn_plays.columns = [
            col.lower().replace(".", "_") for col in espn_plays.columns
        ]

        # Rename id column to play_id
        if "id" in espn_plays.columns:
            espn_plays = espn_plays.rename(columns={"id": "play_id"})

        # Merge datasets
        espn_wp = pd.merge(espn_wp_vals, espn_plays, on="play_id", how="left")

        # Calculate away win percentage
        espn_wp["away_win_percentage"] = (
            1 - espn_wp["home_win_percentage"] - espn_wp.get("tie_percentage", 0)
        )

        # Add game_id column
        espn_wp["game_id"] = espn_game_id

        # Reorder columns to match R function
        first_cols = [
            "game_id",
            "play_id",
            "home_win_percentage",
            "away_win_percentage",
            "tie_percentage",
        ]
        other_cols = [col for col in espn_wp.columns if col not in first_cols]
        espn_wp = espn_wp[first_cols + other_cols]

        # Add metadata
        espn_wp.attrs["source"] = "ESPN NBA Win Probability Information from ESPN.com"
        espn_wp.attrs["timestamp"] = time.ctime()

    except Exception as e:
        print(
            f"{time.ctime()}: Error retrieving data for game_id '{espn_game_id}': {str(e)}"
        )
        return pd.DataFrame()

    return espn_wp


# Example usage
if __name__ == "__main__":
    # Example game ID
    data = espn_nba_wp(game_id="401705718")
    print(data.head())
