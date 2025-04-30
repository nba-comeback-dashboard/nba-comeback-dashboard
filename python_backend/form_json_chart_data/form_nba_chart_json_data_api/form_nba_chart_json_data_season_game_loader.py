# form_nba_chart_json_data_season_game_loader.py
"""
Data loading module for NBA season and game data.

This module handles loading and processing NBA game data from JSON files.
It provides classes for representing seasons, games, and game collections,
along with utility functions for filtering and analyzing game data.

The module defines granular time intervals for game analysis, supporting
minute-by-minute analysis as well as sub-minute intervals (down to 5-second
increments) in the final minute of the game.
"""

# Standard library imports
import json
import os
import gzip


# Defines time intervals for analysis, from start of game (48 minutes)
# to end of game (0), with sub-minute intervals in the final minute
GAME_MINUTES = [
    48,  # Game start
    36,  # Start of 2nd half (3rd quarter)
    35,
    34,
    33,
    32,
    31,
    30,
    29,
    28,
    27,
    26,
    25,
    24,  # Halftime
    23,
    22,
    21,
    20,
    19,
    18,
    17,
    16,
    15,
    14,
    13,  # 3rd quarter and early 4th
    12,  # Start of 4th quarter
    11,
    10,
    9,
    8,
    7,
    6,
    5,
    4,
    3,
    2,
    1,  # Final minute (60 seconds)
    "45s",  # 45 seconds remaining
    "30s",  # 30 seconds remaining
    "15s",  # 15 seconds remaining
    "10s",  # 10 seconds remaining
    "5s",  # 5 seconds remaining
    0,  # Game end (buzzer)
]


# Mapping from time point to array index for efficient lookup
TIME_TO_INDEX_MAP = {key: index for index, key in enumerate(GAME_MINUTES)}


class Season:
    """Manages loading of season data from JSON files."""

    _seasons = {}  # Class-level cache of loaded seasons

    @classmethod
    def get_season(cls, year):
        """Get a season by year, loading it if necessary."""
        if year not in cls._seasons:
            cls._seasons[year] = Season(year)
        return cls._seasons[year]

    def __init__(self, year):
        """Initialize a season by loading its JSON data."""
        self.year = year
        self.filename = f"{json_base_path}/nba_season_{year}.json.gz"

        # Verify the file exists
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"Season data file not found: {self.filename}")

        # Load the season data
        if self.filename.endswith(".gz"):
            with gzip.open(self.filename, "rt") as f:  # 'rt' for text mode
                self.data = json.load(f)
        else:
            with open(self.filename, "r") as f:
                self.data = json.load(f)

        # Extract season metadata
        self.season_year = self.data["season_year"]
        self.team_count = self.data["team_count"]
        self.teams = self.data["teams"]
        self.team_stats = self.data["team_stats"]

        # The games are loaded on demand via the games property
        self._games = None

    @property
    def games(self):
        """Lazy load and cache the game objects."""
        if self._games is None:
            self._games = {}
            for game_id, game_data in self.data["games"].items():
                self._games[game_id] = Game(game_data, game_id, self)
        return self._games


class Games:
    """Collection of NBA games for specified seasons loaded from JSON files."""

    def __init__(self, start_year, stop_year, season_type="all"):
        """
        Initialize games collection for the given year range with optional filtering.

        Parameters:
        -----------
        start_year : int
            First season year to include
        stop_year : int
            Last season year to include
        game_filter : GameFilter or None
            Filter to apply to games. If None, all games in the date range are included.
        """
        self.games = {}
        self.start_year = start_year
        self.stop_year = stop_year

        self.season_type = season_type

        # Load all games from the date range
        for year in range(start_year, stop_year + 1):
            season = Season.get_season(year)

            for game_id, game in season.games.items():
                if season_type != "all" and game.season_type != season_type:
                    continue
                self.games[game_id] = game

    def __getitem__(self, game_id):
        return self.games[game_id]

    def __len__(self):
        return len(self.games)

    def __iter__(self):
        return self.games.values().__iter__()

    def keys(self):
        return self.games.keys()

    def get_years_string(self):
        """Format the years string for display."""

        def short(year):
            return str(year)[-2:]

        if self.season_type != "all":
            season_type = f" {self.season_type}"
        else:
            season_type = ""

        if self.start_year == self.stop_year:
            return f"{self.start_year}-{short(self.start_year+1)}{season_type}"
        else:
            return (
                f"{self.start_year}-{short(self.start_year+1)} to "
                f"{self.stop_year}-{short(self.stop_year+1)}{season_type}"
            )

    def add_playoff_series_lookup_map(self):
        self.playoff_map = PlayoffMap()
        for game in self.games.values():
            self.playoff_map.add_game(game)
        self.playoff_map.finalize_adding_games()


class Game:
    """
    Represents a single NBA game with all related statistics.

    Each Game object contains metadata about the game (teams, date, etc.)
    and a structured mapping of point margins at different times throughout
    the game, enabling detailed analysis of game progression and comebacks.
    """

    index = 0  # Class variable to track game index

    def __init__(self, game_data, game_id, season):
        """
        Initialize game with data from JSON.

        Parameters:
        -----------
        game_data : dict
            Raw game data from JSON
        game_id : str
            Unique identifier for the game
        season : Season
            Reference to the Season object this game belongs to
        """
        self.index = Game.index
        Game.index += 1

        # Store the game ID and reference to season
        self.game_id = game_id
        self.season = season

        # Copy basic properties
        self.game_date = game_data["game_date"]
        self.season_type = game_data["season_type"]
        self.season_year = game_data["season_year"]
        self.home_team_abbr = game_data["home_team_abbr"]
        self.away_team_abbr = game_data["away_team_abbr"]
        self.score = game_data["score"]

        # Parse final score
        self.final_away_points, self.final_home_points = [
            int(x) for x in self.score.split(" - ")
        ]

        # Calculate point differential (positive means home team won)
        self.score_diff = int(self.final_home_points) - int(self.final_away_points)

        # Determine win/loss
        if self.score_diff > 0:
            self.wl_home = "W"
            self.wl_away = "L"
        elif self.score_diff < 0:
            self.wl_home = "L"
            self.wl_away = "W"
        else:
            raise AssertionError("NBA games can't end in a tie")

        # Process and store point margins at each time point
        # This creates a dictionary mapping time points (from GAME_MINUTES) to point margin data
        self.point_margin_map = get_point_margin_map_from_json(
            game_data["point_margins"]
        )

        # Set team win percentages and rankings from season data
        self.home_team_win_pct = season.team_stats[self.home_team_abbr]["win_pct"]
        self.away_team_win_pct = season.team_stats[self.away_team_abbr]["win_pct"]
        self.home_team_rank = season.team_stats[self.home_team_abbr]["rank"]
        self.away_team_rank = season.team_stats[self.away_team_abbr]["rank"]

    def get_game_summary_json_string(self):
        """Returns a formatted string summary of the game suitable for JSON display."""

        # Format the rank as ordinal (1st, 2nd, 3rd, etc.)
        def ordinal(n):
            if 10 <= n % 100 <= 20:
                suffix = "th"
            else:
                suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
            return f"{n}{suffix}"

        # Get team ranks from season data
        home_rank = self.home_team_rank
        away_rank = self.away_team_rank

        # Format the ranks as ordinals
        home_rank_str = ordinal(home_rank) if home_rank > 0 else "N/A"
        away_rank_str = ordinal(away_rank) if away_rank > 0 else "N/A"

        # Return the formatted string without W/L indicators
        return (
            f"{self.away_team_abbr}"
            f"({away_rank_str}/{self.away_team_win_pct:.3f}) @ "
            f"{self.home_team_abbr}"
            f"({home_rank_str}/{self.home_team_win_pct:.3f})"
            f": {self.final_away_points}-{self.final_home_points}"
        )


def get_point_margin_map_from_json(point_margins_data):
    """
    Process point margins from JSON data into a structured map.

    Converts the compact string representation of point margins from the JSON data
    into a structured dictionary mapping time points to point margin data.

    The input format is a list of strings with format "index=value" or
    "index=point_margin,min_point_margin,max_point_margin" where:
    - index corresponds to positions in the GAME_MINUTES array
    - point_margin is the current point margin at that time
    - min/max_point_margin track the extremes reached during intervals

    Parameters:
    -----------
    point_margins_data : list
        List of strings containing point margin data in compressed format

    Returns:
    --------
    dict
        A dictionary mapping time points (from GAME_MINUTES) to point margin data dictionaries
        containing 'point_margin', 'min_point_margin', and 'max_point_margin' keys
    """
    # Extract point margins from the JSON data
    raw_point_margin_map = {}
    for point_margin in point_margins_data:
        index, points_string = point_margin.split("=", 1)
        if "," in points_string:
            point_margin, min_point_margin, max_point_margin = [
                int(x) for x in points_string.split(",")
            ]
        else:
            point_margin = min_point_margin = max_point_margin = int(points_string)
        raw_point_margin_map[int(index)] = {
            "point_margin": point_margin,
            "min_point_margin": min_point_margin,
            "max_point_margin": max_point_margin,
        }

    # Create a complete mapping for all time points in GAME_MINUTES
    point_margin_map = {}
    last_point_margin = None
    for index in range(len(GAME_MINUTES)):
        key = GAME_MINUTES[index]
        try:
            point_margin_data = raw_point_margin_map[index]
        except KeyError:
            # If data is missing for this time point, use the last known point margin
            if last_point_margin is None:
                raise AssertionError
            point_margin_data = {
                "point_margin": last_point_margin,
                "min_point_margin": last_point_margin,
                "max_point_margin": last_point_margin,
            }
        point_margin_map[key] = point_margin_data
        last_point_margin = point_margin_data["point_margin"]
    return point_margin_map


class PlayoffMap:
    """A collection of playoff series data organized by series key.

    This class maps playoff games to their respective series and provides
    methods to access playoff series data and point margins.
    """

    def __init__(self):
        self._data = {}  # Maps series keys to PlayoffSeries objects

    def add_game(self, game):
        """Add a game to the appropriate playoff series based on teams and year."""
        self._data.setdefault(self._get_series_key(game), set()).add(game)

    def _get_series_key(self, game):
        """Create a unique key for a playoff series based on teams and year.

        The key is a tuple of (team1, team2, year) where team1 and team2 are
        alphabetically sorted to ensure consistency regardless of home/away.
        """
        year = game.game_date.split("-", 1)[0]
        series_key = sorted([game.home_team_abbr, game.away_team_abbr])
        series_key.append(year)
        return tuple(series_key)

    def finalize_adding_games(self):
        """Convert collected game sets into PlayoffSeries objects for analysis."""
        self._data = {k: PlayoffSeries(k, v) for k, v in self._data.items()}
        self.add_round_number()

    def get_playoff_point_margins(self, game, game_filter):
        """Get the point margins for a game in the context of its playoff series.

        Returns a tuple of (point_margin, inverse_point_margin, series_id).
        """
        series_key = self._get_series_key(game)
        playoff_series = self._data[series_key]
        return playoff_series.get_playoff_point_margins(game, game_filter)

    def add_round_number(self):
        """
        Add round numbers to each playoff series in the map.

        Round 1 corresponds to the first round of playoffs,
        Round 2 to the second round, etc., up to Round 4 (Finals).

        The round is determined by counting each team's prior series wins in that year.
        """
        # Dictionary to track series wins by team and year
        series_wins_by_year = {}

        # First pass: identify series winners
        for series_key, playoff_series in self._data.items():
            year = series_key[2]
            team1, team2 = series_key[0], series_key[1]

            # Get the winner of this series
            if playoff_series.series_home_team_wins:
                winner = playoff_series.series_home_team
            else:
                winner = playoff_series.series_away_team

            # Initialize the year's tracking dict if needed
            if year not in series_wins_by_year:
                series_wins_by_year[year] = {}

            # Store the winner for this series
            playoff_series.winner = winner

            # Initialize win counts for both teams if not already present
            for team in [team1, team2]:
                if team not in series_wins_by_year[year]:
                    series_wins_by_year[year][team] = 0

        # Sort all series by date (so we count wins in chronological order)
        series_by_date = {}
        for series_key, playoff_series in self._data.items():
            year = series_key[2]
            # Get the first game date as the series start date
            first_game_id = next(iter(playoff_series.game_results_map))
            first_game_date = playoff_series.game_results_map[first_game_id][
                "game_date"
            ]

            if year not in series_by_date:
                series_by_date[year] = []

            series_by_date[year].append((first_game_date, series_key, playoff_series))

        # Process each year's series in chronological order
        for year, series_list in series_by_date.items():
            # Sort series by date
            series_list.sort()

            for _, series_key, playoff_series in series_list:
                team1, team2 = series_key[0], series_key[1]

                # The round is determined by the minimum number of series wins
                # between the two teams at the start of this series
                min_series_wins = min(
                    series_wins_by_year[year].get(team1, 0),
                    series_wins_by_year[year].get(team2, 0),
                )

                # Assign the round (1-based)
                playoff_series.round = min_series_wins + 1

                # After determining the round, increment the winner's series win count
                winner = playoff_series.winner
                series_wins_by_year[year][winner] += 1


class PlayoffSeries:
    """Represents a single NBA playoff series between two teams.

    This class tracks the progression of a playoff series, maintains the series score
    after each game, and maps the series states to point margins for analysis.
    """

    def __init__(self, id, games):
        """Initialize a playoff series with a set of games.

        Args:
            id: Unique identifier for the series (tuple of teams and year)
            games: Collection of Game objects belonging to this series
        """
        self.id = id
        # Convert set to sorted list by game date
        from datetime import datetime

        sorted_games = sorted(
            games, key=lambda g: datetime.strptime(g.game_date, "%Y-%m-%d")
        )

        # Get first game to determine home/away teams for series
        first_game = sorted_games[0]
        self.series_home_team = first_game.home_team_abbr
        self.series_away_team = first_game.away_team_abbr

        # Initialize tracking of wins
        home_wins = 0
        away_wins = 0

        # Create game results map
        self.game_results_map = {}

        for game in sorted_games:
            # Get scores - always from perspective of series home team
            if game.home_team_abbr == self.series_home_team:
                home_score = game.final_home_points
                away_score = game.final_away_points
            else:
                home_score = game.final_away_points
                away_score = game.final_home_points

            # Update win counts
            if home_score > away_score:
                home_wins += 1
            else:
                away_wins += 1

            # Create game summary with series score
            self.game_results_map[game.game_id] = {
                "home_team": game.home_team_abbr,
                "away_team": game.away_team_abbr,
                "home_score": game.final_home_points,
                "away_score": game.final_away_points,
                "game_date": game.game_date,
                "series_score": f"{home_wins}-{away_wins}",
            }

        # Determine the series winner
        if home_wins > away_wins:
            self.series_home_team_wins = True
        else:
            self.series_home_team_wins = False

    # Map series scores to point margins for analysis
    # Positive values indicate winning position, negative for losing position
    # Magnitude reflects the strength of position (e.g., 4-0 is strongest win at +10)
    game_score_map = {
        "4-0": 10,  # Best win - sweep
        "4-1": 9,  # Second best win
        "4-2": 8,  # Win in 6 games
        "4-3": 7,  # Win in 7 games (closest win)
        "3-0": 6,  # Up 3-0
        "3-1": 5,  # Up 3-1
        "2-0": 4,  # Up 2-0
        "3-2": 3,  # Up 3-2
        "2-1": 2,  # Up 2-1
        "1-0": 1,  # Up 1-0
        "0-1": -1,  # Down 0-1
        "1-2": -2,  # Down 1-2
        "2-3": -3,  # Down 2-3
        "0-2": -4,  # Down 0-2
        "1-3": -5,  # Down 1-3
        "0-3": -6,  # Down 0-3
        "3-4": -7,  # Lost in 7 games (closest loss)
        "2-4": -8,  # Lost in 6 games
        "1-4": -9,  # Second worst loss
        "0-4": -10,  # Worst loss - swept
    }

    def get_playoff_point_margins(self, game, game_filter):
        """Convert a playoff series score to equivalent point margins for analysis.

        Maps the series score (e.g., "3-1") at the time of the given game to
        a point margin value that can be used in win probability analysis.

        Args:
            game: The game object to get point margins for

        Returns:
            Tuple of (point_margin, inverse_point_margin, series_id)

        Raises:
            ValueError: If series is not a valid 7-game series or if series is over
        """
        # Verify this is a complete 7-game series (one team reached 4 wins)
        last_series_score = list(self.game_results_map.values())[-1]["series_score"]
        if "4-" not in last_series_score and "-4" not in last_series_score:
            raise ValueError("Not a 7 game series")

        if game_filter and game_filter.playoff_round != self.round:
            raise ValueError(
                f"Not correct round {game_filter.playoff_round} != {self.round}"
            )

        # Get the series score at the time of this game
        game_series_data = self.game_results_map[game.game_id]
        game_series_score = game_series_data["series_score"]

        # Handle tied series (return 0 point margin)
        home_score, away_score = game_series_score.split("-")
        if home_score == away_score:
            return 0, 0, self.id

        # Normalize series score if away team won the series
        # This ensures scores are always from perspective of eventual winner
        if not self.series_home_team_wins:
            game_series_score = f"{away_score}-{home_score}"

        # Map series score to point margin
        try:
            point_margin = self.game_score_map[game_series_score]
        except KeyError:
            raise ValueError(f"Series is over {game_series_score}")
        else:
            return point_margin, -point_margin, self.id
