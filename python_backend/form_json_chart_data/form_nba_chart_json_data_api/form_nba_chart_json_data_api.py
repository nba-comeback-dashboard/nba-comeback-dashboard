# form_nba_chart_json_data_api.py
"""
Main API module for forming NBA chart JSON data.

This module provides the primary interface for creating JSON data files for NBA game analysis charts.
It contains the core functions for generating different types of analysis plots based on NBA game data.
"""

# Third-party imports
from scipy.stats import norm

# Local imports
from form_nba_chart_json_data_season_game_loader import Games
from form_nba_chart_json_data_plot_primitives import (
    PointsDownLine,
    PercentLine,
    FinalPlot,
)
from form_nba_chart_json_data_num import Num

__LINEAR_Y_AXIS__ = False


def parse_season_type(year):
    """
    Parse year string to determine season type and numeric year.

    Parameters:
    -----------
    year : str or int
        Year string (possibly with prefix) or year as int

    Returns:
    --------
    tuple
        (numeric_year, season_type) where season_type is 'Regular Season', 'Playoffs', or 'all'
    """
    year_str = str(year)
    if year_str.startswith("R"):
        season_type = "Regular Season"
        numeric_year = int(year_str[1:])
    elif year_str.startswith("P"):
        season_type = "Playoffs"
        numeric_year = int(year_str[1:])
    else:
        season_type = "all"
        numeric_year = int(year)

    return numeric_year, season_type


class GameFilter:
    """
    Filter for NBA games based on team attributes.

    Allows filtering games based on:
    - Which team won/lost (home/away)
    - Team ranking category (top_5, top_10, mid_10, bot_10, bot_5)
    - Specific team abbreviations

    Note: For both winning and losing teams, you can only specify either a rank filter
    OR a team abbreviation filter, not both.
    """

    def __init__(
        self,
        for_at_home=None,
        for_rank=None,
        for_team_abbr=None,
        vs_rank=None,
        vs_team_abbr=None,
    ):
        """
        Initialize a GameFilter with criteria for filtering NBA games.

        Parameters:
        -----------
        for_at_home : bool or None
            If True, only include games where the home team won
            If False, only include games where the away team won
            If None, don't filter based on home/away win
        for_rank : str or None
            Filter winning team by rank category ('top_5', 'top_10', 'mid_10', 'bot_10', 'bot_5')
            Cannot be used together with for_team_abbr
        for_team_abbr : str or None
            Filter winning team by abbreviation (can be a single abbr or comma-separated list)
            Cannot be used together with for_rank
        vs_rank : str or None
            Filter losing team by rank category ('top_5', 'top_10', 'mid_10', 'bot_10', 'bot_5')
            Cannot be used together with vs_team_abbr
        vs_team_abbr : str or None
            Filter losing team by abbreviation (can be a single abbr or comma-separated list)
            Cannot be used together with vs_rank

        Raises:
        -------
        ValueError
            If both for_rank and for_team_abbr are specified, or
            if both vs_rank and vs_team_abbr are specified
        """
        # Check for invalid combinations
        if for_rank is not None and for_team_abbr is not None:
            raise ValueError("Cannot specify both for_rank and for_team_abbr")
        if vs_rank is not None and vs_team_abbr is not None:
            raise ValueError("Cannot specify both vs_rank and vs_team_abbr")

        self.for_at_home = for_at_home
        self.for_rank = for_rank
        self.for_team_abbr = for_team_abbr
        self.vs_rank = vs_rank
        self.vs_team_abbr = vs_team_abbr

        # Parse team abbreviations into lists if provided as strings
        if isinstance(self.for_team_abbr, str):
            self.for_team_abbr = [
                abbr.strip() for abbr in self.for_team_abbr.split(",")
            ]
        if isinstance(self.vs_team_abbr, str):
            self.vs_team_abbr = [abbr.strip() for abbr in self.vs_team_abbr.split(",")]

        # vs_at_home is just the inverse of for_at_home
        self.vs_at_home = None if self.for_at_home is None else not self.for_at_home

    def is_match(self, game, is_win):
        """
        Check if a game matches the filter criteria.

        Parameters:
        -----------
        game : Game
            The game to check against the filter

        Returns:
        --------
        bool
            True if game matches all filter criteria, False otherwise
        """
        # Determine if the home team won
        if (game.score_diff > 0 and is_win) or (game.score_diff < 0 and not is_win):
            for_team_abbr = game.home_team_abbr
            for_team_rank = game.home_team_rank
            vs_team_abbr = game.away_team_abbr
            vs_team_rank = game.away_team_rank
            for_team_where = "home"
        elif (game.score_diff < 0 and is_win) or (game.score_diff > 0 and not is_win):
            for_team_abbr = game.away_team_abbr
            for_team_rank = game.away_team_rank
            vs_team_abbr = game.home_team_abbr
            vs_team_rank = game.home_team_rank
            for_team_where = "away"
        else:
            raise AssertionError

        # Check for_at_home filter if it's specified
        if self.for_at_home is True and for_team_where != "home":
            return False
        elif self.for_at_home is False and for_team_where != "away":
            return False
        # Check for_team_abbr filter
        if self.for_team_abbr and for_team_abbr not in self.for_team_abbr:
            return False

        # Check vs_team_abbr filter
        if self.vs_team_abbr and vs_team_abbr not in self.vs_team_abbr:
            return False

        # Check for_rank filter
        if self.for_rank:
            if not self._check_rank(
                for_team_rank, self.for_rank, game.season.team_count
            ):
                return False

        # Check vs_rank filter
        if self.vs_rank:
            if not self._check_rank(vs_team_rank, self.vs_rank, game.season.team_count):
                return False

        # If all filters passed, the game matches
        return True

    def _check_rank(self, rank, rank_filter, team_count):
        """
        Check if a team's rank matches the specified rank filter.

        Parameters:
        -----------
        rank : int
            The team's rank
        rank_filter : str
            The rank filter ('top_5', 'top_10', 'mid_10', 'bot_10', 'bot_5')
        team_count : int
            Total number of teams in the season

        Returns:
        --------
        bool
            True if the rank matches the filter, False otherwise
        """
        if rank_filter == "top_5":
            return 1 <= rank <= 5
        elif rank_filter == "top_10":
            return 1 <= rank <= 10
        elif rank_filter == "mid_10":
            mid_start = (team_count // 2) - 5
            mid_end = (team_count // 2) + 4
            return mid_start <= rank <= mid_end
        elif rank_filter == "bot_10":
            return team_count - 9 <= rank <= team_count
        elif rank_filter == "bot_5":
            return team_count - 4 <= rank <= team_count
        else:
            return False

    def _get_rank_display_name(self, rank_filter):
        """
        Get a display-friendly name for a rank filter.

        Parameters:
        -----------
        rank_filter : str
            The rank filter value

        Returns:
        --------
        str
            A formatted display name for the rank
        """
        if not rank_filter:
            return ""

        if rank_filter == "top_5":
            return "Top 5"
        elif rank_filter == "top_10":
            return "Top 10"
        elif rank_filter == "mid_10":
            return "Mid 10"
        elif rank_filter == "bot_10":
            return "Bot 10"
        elif rank_filter == "bot_5":
            return "Bot 5"
        else:
            return rank_filter

    def get_filter_string(self):
        """
        Generate a human-readable description of the filter criteria.

        Returns:
        --------
        str
            A formatted string describing the filter criteria
        """
        for_parts = []
        vs_parts = []

        # Build for criteria string
        if self.for_rank:
            for_parts.append(f"{self._get_rank_display_name(self.for_rank)}")
        elif self.for_team_abbr:
            if isinstance(self.for_team_abbr, list) and len(self.for_team_abbr) == 1:
                for_parts.append(f"{self.for_team_abbr[0]}")
            elif isinstance(self.for_team_abbr, list):
                teams = ", ".join(self.for_team_abbr)
                for_parts.append(f"{teams}")
            else:
                for_parts.append(f"{self.for_team_abbr}")

        if self.for_at_home is not None:
            for_parts.append("@ Home" if self.for_at_home else "@ Away")

        # Build vs criteria string
        if self.vs_rank:
            vs_parts.append(f"{self._get_rank_display_name(self.vs_rank)}")
        elif self.vs_team_abbr:
            if isinstance(self.vs_team_abbr, list) and len(self.vs_team_abbr) == 1:
                vs_parts.append(f"{self.vs_team_abbr[0]}")
            elif isinstance(self.vs_team_abbr, list):
                teams = ", ".join(self.vs_team_abbr)
                vs_parts.append(f"{teams}")
            else:
                vs_parts.append(f"{self.vs_team_abbr}")

        # if self.vs_at_home is not None:
        #    vs_parts.append("@ Home" if self.vs_at_home else "@ Away")

        # Combine for and vs parts into a complete string
        for_str = f"{' '.join(for_parts)}" if for_parts else ""
        vs_str = f"Plays {' '.join(vs_parts)}" if vs_parts else ""

        if for_str and vs_str:
            return f"For {for_str} {vs_str}"
        elif for_str:
            return f"For {for_str}"
        elif vs_str:
            return f"For {vs_str}"
        else:
            return "For All Games"


def plot_biggest_deficit(
    json_name,
    year_groups,
    start_time,
    down_mode,
    cumulate=False,
    min_point_margin=None,
    max_point_margin=None,
    fit_min_win_game_count=None,
    fit_max_points=None,
    game_filters=None,
    plot=False,
    calculate_occurrences=False,
    use_normal_labels=False,
    linear_y_axis=False,
    use_logit=False,
):
    """
    Generate plots and JSON data showing win probability based on point deficit.

    Creates chart data showing how point deficits at different game times
    correlate with comeback probabilities. Can analyze either deficits at a
    specific moment or maximum deficits faced during a period.

    Parameters:
    -----------
    json_name : str
        Path to save the JSON output
    year_groups : list of tuples
        List of (start_year, end_year) ranges to analyze
    start_time : int or str
        Time point to start analysis from, can be:
        - Integer minute value (e.g., 48 for game start, 24 for halftime)
        - String for sub-minute times in final minute (e.g., "45s", "30s", "15s")
    down_mode : str
        Analysis mode:
        - 'at': Point deficit at specific time point
        - 'max': Maximum point deficit faced during the period from start_time to end
    cumulate : bool
        Whether to cumulate point totals (for "or more" analysis)
    min_point_margin : int or None
        Minimum point margin to include in analysis
    max_point_margin : int, "auto", or None
        Maximum point margin to include in analysis
        - int: Specific max value
        - "auto": Automatically determine based on data
        - None: Use defaults based on down_mode
    fit_min_win_game_count : int or None
        Minimum number of wins required for fitting regression
    fit_max_points : float, str, or None
        Maximum points to include in regression fit
        - float: Specific max value
        - str ending with '%': Percentile cutoff (e.g., "10%")
        - None: Use defaults based on down_mode
    game_filters : list of GameFilter or None
        List of filters to apply to games. Each filter will be paired with each year group.
    plot : bool
        Whether to generate matplotlib plots in addition to JSON output
    calculate_occurrences : bool
        Whether to calculate occurrence percentages instead of win percentages
    use_normal_labels : bool or str
        Type of labels to use for y-axis
    linear_y_axis : bool
        Whether to use linear y-axis instead of probit scaling
    use_logit : bool
        Whether to use logit transformation instead of probit for probabilities
    """

    global __LINEAR_Y_AXIS__
    if linear_y_axis:
        __LINEAR_Y_AXIS__ = True
        Num.CDF = lambda x: x
        Num.PPF = lambda x: x
    else:
        __LINEAR_Y_AXIS__ = False

    if use_logit:
        from scipy.special import logit, expit

        Num.CDF = expit
        Num.PPF = logit

    if start_time == 48:
        time_desc = "Entire Game"
    elif start_time == 36:
        if down_mode == "at":
            time_desc = "2nd Quarter"
        else:
            time_desc = "Final 3 Quarters"
    elif start_time == 24:
        time_desc = "2nd Half"
    elif start_time == 12:
        time_desc = "4th Quarter"
    elif start_time == 1:
        time_desc = "Final Minute"
    elif isinstance(start_time, str):
        time_desc = f"Final {start_time}"
    elif 1 < start_time < 12:
        time_desc = f"Final {start_time} Minutes"
    elif start_time == 0:
        time_desc = "At End of Regulation"
    else:
        raise NotImplementedError(start_time)

    or_more = " Or More" if cumulate else ""

    # If game_filters is None, create a list with a single None element
    if game_filters is None:
        game_filters = [None]
    elif not isinstance(game_filters, list):
        game_filters = [game_filters]

    fit_min_win_game_count = (
        3 if fit_min_win_game_count is None else fit_min_win_game_count
    )
    if calculate_occurrences:
        start_text = ""
    else:
        start_text = "Win % v. "

    if down_mode == "at":
        title = f"{start_text}Points Down{or_more} At Start of {time_desc}"
        or_more = ""
        max_point_margin = -1 if max_point_margin is None else max_point_margin
        fit_max_points = -1 if fit_max_points is None else fit_max_points
    else:
        title = f"{start_text}Max Points Down{or_more} During {time_desc}"
        max_point_margin = "auto" if max_point_margin is None else max_point_margin
        if fit_max_points is None:
            fit_max_points = "10%"

    if calculate_occurrences:
        max_point_margin = 1000

    if down_mode == "playoff_series":
        max_point_margin = 0
        if game_filters[0]:
            raise AssertionError
        year_groups = list(year_groups)
        for index, year_group in enumerate(year_groups):
            try:
                int(year_group[0])
            except ValueError:
                if str(year_group[0]) == "P":
                    pass
                else:
                    raise AssertionError
            else:
                year_groups[index] = [f"P{year_group[0]}", year_group[1]]

    # Prepare data for combinations of year groups and filters
    points_down_lines = []

    number_of_year_groups = len(year_groups)
    number_of_game_filters = len(game_filters)
    if number_of_game_filters == 1 and game_filters[0] is None:
        number_of_game_filters = 0

    game_years_strings = []
    game_filter_strings = []

    # Create combinations of year groups and filters
    for start_year, stop_year in year_groups:
        for game_filter_index, game_filter in enumerate(game_filters):
            # Parse season type using the helper function
            start_year_numeric, season_type = parse_season_type(start_year)
            stop_year_numeric, _ = parse_season_type(stop_year)

            # Use the Games class that loads from JSON with optional game filter
            games = Games(
                start_year=start_year_numeric,
                stop_year=stop_year_numeric,
                season_type=season_type,
            )

            if down_mode == "playoff_series":
                games.add_playoff_series_lookup_map()

            if number_of_year_groups > 1 or number_of_game_filters < 2:
                legend = games.get_years_string()
            else:
                legend = ""

            if game_filter_index == 0:
                game_years_strings.append(games.get_years_string())
            if game_filter:
                game_filter_strings.append(game_filter.get_filter_string())

            if number_of_game_filters > 1:
                if legend:
                    legend = f"{legend} | "
                legend = f"{legend}{game_filter.get_filter_string()}"

            points_down_line = PointsDownLine(
                games=games,
                game_filter=game_filter,
                legend=legend,
                start_time=start_time,
                down_mode=down_mode,
                cumulate=cumulate,
                min_point_margin=min_point_margin,
                max_point_margin=max_point_margin,
                fit_min_win_game_count=fit_min_win_game_count,
                fit_max_points=fit_max_points,
                calculate_occurrences=calculate_occurrences,
            )

            # To create js objects
            points_down_lines.append(points_down_line)

    if number_of_year_groups == 1 and number_of_game_filters > 1:
        title = f"{title} | {points_down_lines[0].games.get_years_string()}"

    elif number_of_game_filters == 1:
        title = f"{title} | {game_filters[0].get_filter_string()}"

    if down_mode == "score":
        if cumulate:
            title = "Points Scored Or Less"
        else:
            title = "Points Scored"
        for line in points_down_lines:
            line.legend = line.legend.replace("Games)", "Scores)")
    elif down_mode == "playoff_series":
        if calculate_occurrences:
            title = "Series Score"
        else:
            title = "Win % Versus Series Score"
        for line in points_down_lines:
            line.legend = line.legend.replace("Games)", "Playoff Series)")

    if calculate_occurrences:
        title = f"Occurrence % of {title}"

    bound_x = float("inf")
    for line in points_down_lines:
        bound_x = min(bound_x, line.max_point_margin)
    min_x, max_x, y_tick_values, y_tick_labels = (
        get_points_down_normally_spaced_y_ticks(points_down_lines, bound_x=bound_x)
    )

    for points_down_line in points_down_lines:
        min_y = y_tick_values[0]
        max_y = y_tick_values[-1]
        points_down_line.set_sigma_final(min_y, max_y)

    x_label = "Point Margin"
    if calculate_occurrences:
        y_label = "Occurrence %"
    else:
        y_label = "Win %"

    if down_mode == "playoff_series":
        x_label = "Series Score"
        if calculate_occurrences:
            x_ticks = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0]
            x_label = "Series Score"
            x_tick_labels = [
                "0-4",
                "1-4",
                "2-4",
                "3-4",
                "0-3",
                "1-3",
                "0-2",
                "2-3",
                "1-2",
                "0-1",
                "Tied",
            ]
        else:
            x_ticks = [-7, -6, -5, -4, -3, -2, -1, 0]
            x_tick_labels = ["Lost", "0-3", "1-3", "0-2", "2-3", "1-2", "0-1", "Tied"]
    else:
        x_ticks = None
        x_tick_labels = None

    final_plot = FinalPlot(
        plot_type="point_margin_v_win_percent",
        title=title,
        x_label=x_label,
        y_label=y_label,
        x_ticks=x_ticks,
        x_tick_labels=x_tick_labels,
        y_ticks=[Num.PPF(p) for p in y_tick_values],
        y_tick_labels=y_tick_labels,
        min_x=min_x,
        max_x=max_x,
        lines=points_down_lines,
        json_name=json_name,
        use_normal_labels=use_normal_labels,
        cumulate=cumulate,
        calculate_occurrences=calculate_occurrences,
    )
    if json_name is not None:
        final_plot.to_json()

    return title, game_years_strings, game_filter_strings, final_plot


def get_points_down_normally_spaced_y_ticks(plot_lines, bound_x=float("inf")):
    min_y = next_min_y = float("inf")
    max_y = next_max_y = -1.0 * float("inf")
    min_x = float("inf")
    max_x = -1.0 * float("inf")
    for plot_line in plot_lines:
        x = plot_line.point_margins
        y = plot_line.percents
        min_x = min(min_x, min(x))
        max_x = max(max_x, min(max(x), bound_x))
        min_y = min(min_y, min(y))
        max_y = max(max_y, max(y))
        next_min_y = min(next_min_y, min([p if p > 1e-9 else float("inf") for p in y]))
        next_max_y = max(
            next_max_y,
            max([p if p < (1.0 - 1e-9) else -float("inf") for p in y]),
        )
        if plot_line.m is not None:
            y_fit = plot_line.m * Num.array(x) + plot_line.b
            min_y = min(min_y, Num.CDF(Num.min(y_fit)))
            max_y = max(max_y, Num.CDF(Num.max(y_fit)))
            next_min_y = min(next_min_y, Num.CDF(Num.min(y_fit)))
            next_max_y = max(next_max_y, Num.CDF(Num.max(y_fit)))

    if __LINEAR_Y_AXIS__:
        y_ticks = {
            0.001: "0%",
            0.10: "10%",
            0.20: "20%",
            0.30: "30%",
            0.40: "40%",
            0.50: "50%",
            0.60: "60%",
            0.70: "70%",
            0.80: "80%",
            0.90: "90%",
            0.999: "100%",
        }
    else:
        y_ticks = {
            1 / 100000.0: "1/100000",
            1 / 10000.0: "1/10000",
            1 / 1000.0: "1/1000",
            1 / 500.0: "1/500",
            1 / 200.0: "1/200",
            0.01: "1%",
            0.025: "2.5%",
            0.05: "5%",
            0.10: "10%",
            0.20: "20%",
            0.30: "30%",
            0.40: "40%",
            0.50: "50%",
            0.60: "60%",
            0.70: "70%",
            0.80: "80%",
            0.90: "90%",
            0.95: "95%",
            0.975: "97.5%",
            0.99: "99.0%",
            0.995: "99.5%",
            0.998: "99.8%",
            0.999: "99.9%",
            0.9999: "99.99%",
            0.99999: "99.999%",
            0.999999: "99.9999%",
            0.9999999: "99.99999%",
        }
    y_tick_indicies = [
        index for index, key in enumerate(y_ticks) if next_min_y <= key <= next_max_y
    ]
    y_min_index, y_max_index = y_tick_indicies[0] - 1, y_tick_indicies[-1] + 1
    y_ticks_final = {
        k: v
        for index, (k, v) in enumerate(y_ticks.items())
        if y_min_index <= index <= y_max_index
    }

    y_tick_values = list(y_ticks_final.keys())
    y_tick_labels = list(y_ticks_final.values())

    if min_y < next_min_y:
        y_tick_labels[0] = "Never"
    if max_y > next_max_y:
        y_tick_labels[-1] = "100%"

    # Find first index <= min_y and last index >= max_y
    first_index = 0
    last_index = len(y_tick_values) - 1

    for i, tick in enumerate(y_tick_values):
        if tick <= min_y:
            first_index = i
            break

    for i in range(len(y_tick_values) - 1, -1, -1):
        if y_tick_values[i] >= max_y:
            last_index = i
            break

    return min_x, max_x, y_tick_values, y_tick_labels


def plot_percent_versus_time(
    json_name,
    year_groups,
    start_time,
    percents,
    game_filters=None,
    plot_2x_guide=False,
    plot_4x_guide=False,
    plot_6x_guide=False,
    plot_2x_bad_guide=False,
    plot_3x_bad_guide=False,
    plot_calculated_guides=False,
    python_only_calculate_cdf_constant=False,
):
    """
    Generate plots and JSON data showing win probability versus time for NBA games.

    This function analyzes how point deficits corresponding to specific win percentages
    change throughout the game. It tracks the required deficit for a given comeback
    probability at each minute from start_time down to the end of the game.

    Parameters:
    -----------
    json_name : str
        Path to save the JSON output
    year_groups : list of tuples
        List of (start_year, end_year) ranges to analyze
    start_time : int
        Starting minute of analysis (e.g., 24 for halftime)
    percents : list
        List of percentages to track (e.g., ["20%", "10%", "5%", "1%"])
    game_filters : list of GameFilter or None
        List of filters to apply to games. Each filter will be paired with each year group.
    plot_2x_guide : bool
        Whether to plot the 2√t theoretical curve guide
    plot_4x_guide : bool
        Whether to plot the 4√t theoretical curve guide
    plot_6x_guide : bool
        Whether to plot the 6√t theoretical curve guide
    plot_2x_bad_guide : bool
        Whether to plot the 2t (linear) guide
    plot_3x_bad_guide : bool
        Whether to plot the 3t (linear) guide
    plot_calculated_guides : bool
        Whether to calculate and plot regression guides from actual data
    python_only_calculate_cdf_constant : bool
        Whether to calculate the CDF coefficient (for debugging, not used in output)
    """

    # If game_filters is None, create a list with a single None element
    if game_filters is None:
        game_filters = [None]
    elif not isinstance(game_filters, list):
        game_filters = [game_filters]

    # Prepare for tracking variables
    number_of_year_groups = len(year_groups)
    number_of_game_filters = len(game_filters)
    if number_of_game_filters == 1 and game_filters[0] is None:
        number_of_game_filters = 0

    # Setup time range
    times = list(range(start_time, 0, -1))
    min_point_margin = float("inf")
    max_point_margin = -1.0 * float("inf")

    percent_lines = []

    game_years_strings = []
    game_filter_strings = []

    # Create combinations of year groups, filters, and percents
    all_percent_data = []
    for start_year, stop_year in year_groups:
        for game_filter_index, game_filter in enumerate(game_filters):
            # Parse season type using the helper function
            start_year_numeric, season_type = parse_season_type(start_year)
            stop_year_numeric, _ = parse_season_type(stop_year)

            # Use the Games class that loads from JSON with optional game filter
            games = Games(
                start_year=start_year_numeric,
                stop_year=stop_year_numeric,
                season_type=season_type,
            )
            if game_filter_index == 0:
                game_years_strings.append(games.get_years_string())
            if game_filter:
                game_filter_strings.append(game_filter.get_filter_string())
            # Get points data for each time point
            percent_data = {}
            for current_time in times:
                points_down_line = PointsDownLine(
                    games=games,
                    game_filter=game_filter,
                    start_time=current_time,
                    down_mode="at",
                    max_point_margin=-1,
                    fit_max_points=-1,
                )
                game_count = points_down_line.number_of_games
                for percent in percents:
                    current_percents = percent_data.setdefault(percent, [])
                    if percent == "Record":
                        point_margin = points_down_line.margin_at_record()
                    else:
                        point_margin = points_down_line.margin_at_percent(
                            float(percent[:-1])
                        )

                    current_percents.append(point_margin)
                    min_point_margin = min(min_point_margin, point_margin[0])
                    max_point_margin = max(max_point_margin, point_margin[0])

            all_percent_data.append((games, game_count, game_filter, percent_data))

    percent_strings = all_percent_data[0][3].keys()
    for percent_string in percent_strings:
        for games, game_count, game_filter, percent_data in all_percent_data:
            percent_value = percent_data[percent_string]
            # Format percent string for display
            # display_percent = percent_string
            # if percent_string.endswith("S"):
            #     amount = percent_string[0:-1]
            #     display_percent = f"{amount}√t"
            # elif percent_string.endswith("T"):
            #     amount = percent_string[0:-1]
            #     display_percent = f"{amount}t"
            legend = f"{percent_string}"
            if number_of_year_groups > 1:
                legend = f"{legend} | {games.get_years_string()} ({game_count:,} Games)"
            if number_of_game_filters > 1:
                legend = f"{legend} | {game_filter.get_filter_string()}"
            percent_lines.append(PercentLine(games, legend, times, percent_value))

    if plot_calculated_guides:
        for percent_line in list(percent_lines):
            legend = percent_line.legend
            x = [Num.power(p, 0.5) for p in percent_line.x_values[-12:]]
            y = [p[0] for p in percent_line.line_data[-12:]]
            result = Num.least_squares(x, y, slope_only=True)
            amount = result["m"]
            percent_lines.append(
                PercentLine(
                    None,
                    f"{legend}: {-amount:.2f}√t",
                    times,
                    [amount * Num.power(x, 0.5) for x in times],
                )
            )

    if plot_2x_guide:
        percent_lines.append(
            PercentLine(None, "2√t", times, [-2 * Num.power(x, 0.5) for x in times])
        )
    if plot_4x_guide:
        percent_lines.append(
            PercentLine(None, "4√t", times, [-4 * Num.power(x, 0.5) for x in times])
        )
    if plot_6x_guide:
        percent_lines.append(
            PercentLine(None, "6√t", times, [-6 * Num.power(x, 0.5) for x in times])
        )
    if plot_2x_bad_guide:
        percent_lines.append(PercentLine(None, "2t", times, [-2.0 * x for x in times]))
    if plot_3x_bad_guide:
        percent_lines.append(PercentLine(None, "3t", times, [-3.0 * x for x in times]))

    title = "% Chance of Coming Back: Points Down v. Time"
    if number_of_year_groups == 1:
        title = f"{title} | {games.get_years_string()} ({game_count:,} Games)"
    if number_of_game_filters == 1:
        title = f"{title} | {game_filters[0].get_filter_string()}"

    # Calculate y_ticks for the plot
    x_label = "Minutes Remaining"
    y_label = "Points Down"
    x_ticks = list(range(start_time, 0, -1))
    y_ticks = list(
        range(
            int(Num.floor(min_point_margin)) - 1, int(Num.ceil(max_point_margin)) + 2, 2
        )
    )

    if python_only_calculate_cdf_constant:
        x = times[-12:]
        for games, game_count, game_filter, percent_data in all_percent_data:
            x_final = []
            y_final = []
            for percent_string, percent_value in percent_data.items():
                percent_amount = float(percent_string[:-1])
                y = [p[0] for p in percent_value[-12:]]
                result = Num.least_squares(x, y, slope_only=True)
                x_final.extend(Num.PPF(percent_amount / 100.0) * p**0.5 for p in x)
                y_final.extend(y)
            result = Num.least_squares(x_final, y_final, slope_only=True)
            print(f"CDF coefficent: {result["m"]}.")

    # Create the final plot
    final_plot = FinalPlot(
        plot_type="time_v_point_margin",
        title=title,
        x_label=x_label,
        y_label=y_label,
        x_ticks=None,
        x_tick_labels=None,
        y_ticks=y_ticks,
        y_tick_labels=y_ticks,
        min_x=min(x_ticks),
        max_x=max(x_ticks),
        json_name=json_name,
        lines=percent_lines,
    )
    final_plot.to_json()

    return title, game_years_strings, game_filter_strings


def plot_espn_versus_dashboard(
    json_name,
    espn_game_id,
    year_groups,
    use_home_away_game_filters=False,
    show_team="away",
    start_time=18,
):
    """
    Generate plots and JSON data comparing ESPN win probability with NBA Dashboard calculations.

    This function analyzes win probability data from ESPN for a specific game and compares
    it with probabilities calculated using the NBA Dashboard methodology. It produces a JSON
    file that can be used for visualization in the frontend.

    Parameters:
    -----------
    json_name : str
        Path to save the JSON output
    espn_game_id : str
        ESPN game ID to fetch data for
    year_groups : list of tuples
        List of (start_year, end_year) ranges to use for Dashboard calculations
    use_home_away_game_filters : bool
        Whether to apply home/away game filters based on point margin
    show_modern_only : bool
        Whether to only show modern era calculations (2017-2024)
    show_team : str
        Which team's perspective to show ('home', 'away', or 'both')
    start_time : int
        Time in minutes to start the plot from (default: 18)

    Returns:
    --------
    tuple
        (title, game_years_strings, game_filter_strings, final_plot)
    """
    # Import here to avoid circular import
    from form_nba_chart_json_data_espn_v_dashboard import (
        EspnLine,
        DashboardLine,
        get_team_nickname,
        get_espn_game_data,
        extract_win_probability_data,
        create_play_data_with_win_probability,
        get_dashboard_win_probability,
    )

    # Fetch ESPN data
    game_data = get_espn_game_data(espn_game_id)
    win_prob_map = extract_win_probability_data(game_data)
    plays, home_team, away_team, game_date = create_play_data_with_win_probability(
        game_data, win_prob_map
    )

    if not plays:
        raise ValueError(f"No play data found for ESPN game ID: {espn_game_id}")

    # Filter data to only include times >= start_time
    plays = [play for play in plays if play["minutesElapsed"] >= start_time]

    # Get team abbreviations
    # home_abbr = get_team_abbreviation(home_team)
    # away_abbr = get_team_abbreviation(away_team)

    # Prepare data for lines
    lines = []

    # Create metrics for title and eventual URL construction
    # number_of_year_groups = len(year_groups)

    game_years_strings = []
    game_filter_strings = []

    # Extract time and probability data for plotting
    minutes_elapsed = [play["minutesElapsed"] for play in plays]
    home_win_probability = [play["homeWinProbability"] for play in plays]
    away_win_probability = [100 - wp for wp in home_win_probability]

    # Add ESPN win probability lines
    point_margins = [play["pointMargin"] for play in plays]
    if show_team in ["both", "home"]:
        home_nickname = get_team_nickname(home_team)
        espn_home_line = EspnLine(
            legend=f"{home_nickname} ESPN Win Probability",
            x_values=minutes_elapsed,
            y_values=home_win_probability,
            point_margins=point_margins,
            team_name=home_team,
        )
        lines.append(espn_home_line)

    if show_team in ["both", "away"]:
        away_nickname = get_team_nickname(away_team)
        espn_away_line = EspnLine(
            legend=f"{away_nickname} ESPN Win Probability",
            x_values=minutes_elapsed,
            y_values=away_win_probability,
            point_margins=point_margins,
            team_name=away_team,
        )
        lines.append(espn_away_line)

    # Add Dashboard probability lines
    for start_year, stop_year in year_groups:
        # Parse season type using the helper function
        start_year_numeric, season_type = parse_season_type(start_year)
        stop_year_numeric, _ = parse_season_type(stop_year)

        # Build legend string
        years_string = f"{start_year_numeric}-{stop_year_numeric}"
        if len(game_years_strings) == 0:
            game_years_strings.append(years_string)

        # Calculate dashboard probabilities
        times, dashboard_probabilities, dashboard_point_margins = (
            get_dashboard_win_probability(
                plays=plays,
                start_year=start_year_numeric,
                stop_year=stop_year_numeric,
                season_type=season_type,
                use_home_away_game_filter=use_home_away_game_filters,
            )
        )

        # Create Dashboard line
        if show_team == "home":
            dashboard_probabilities = 100 - dashboard_probabilities
            team_for_dashboard = home_team
        else:
            team_for_dashboard = away_team

        # Get team nickname
        team_nickname = get_team_nickname(team_for_dashboard)

        # Construct URL for linking in the frontend
        url_base = "../../_static/json/charts"
        url_params = f"?years={years_string}"
        if use_home_away_game_filters:
            url_params += "&filter=ANY-h-ANY"
        dashboard_url = f"{url_base}{url_params}"

        dashboard_line = DashboardLine(
            legend=f"{team_nickname} Dashboard Win Probability {years_string}",
            x_values=list(times),
            y_values=list(dashboard_probabilities),
            point_margins=list(dashboard_point_margins),
            team_name=team_for_dashboard,
            start_year=start_year,
            stop_year=stop_year,
            use_home_away_game_filter=use_home_away_game_filters,
        )
        lines.append(dashboard_line)

    # Create title
    title = f"{away_team} @ {home_team} ({game_date})"
    title = f"{title} | Use Seasons: {game_years_strings[0]}"
    if season_type == "all":
        pass
    elif season_type == "Regular Season":
        title = f"{title} | Use Regular Season Data"
    elif season_type == "Playoffs":
        title = f"{title} | Use Playoff Data"
    else:
        raise ValueError(f"Invalid season type: {season_type}")

    if use_home_away_game_filters:
        title = f"{title} | Use {away_team.split()[-1]} @ Away"

    # if number_of_year_groups == 1 and number_of_game_filters > 1:
    #    title = f"{title} | {game_years_strings[0]}"
    # elif number_of_game_filters == 1:
    #    title = f"{title} | {game_filters[0].get_filter_string()}"

    # Convert probabilities to Gaussian sigma values using norm.ppf
    for line in lines:
        new_y_values = []
        for i, point in enumerate(line.y_values):
            # Convert percentage to probability (0-1 range)
            prob = point / 100.0
            # Handle edge cases to avoid infinity
            if prob <= 0.0001:
                prob = 0.0001
            elif prob >= 0.9999:
                prob = 0.9999
            # Convert to sigma using norm.ppf (same as Num.PPF)
            sigma = norm.ppf(prob)
            # Update value
            new_y_values.append(sigma)
        line.y_values = new_y_values

    # For ESPN charts, use fixed min_y=0.0001 and max_y=0.9999 to ensure consistent scale
    # These values can be adjusted later if needed

    min_prob = min(min(away_win_probability), min(dashboard_probabilities))
    max_prob = max(max(away_win_probability), max(dashboard_probabilities))
    # Match the y_ticks structure from get_points_down_normally_spaced_y_ticks function
    min_y = norm().ppf(max(0.01 * min_prob, 1e-6)) * 0.99
    max_y = norm().ppf(min(0.01 * max_prob, 1.0 - 1e-6)) * 1.01
    y_ticks = [
        -3.719016485156023,  # 0.0001 (norm.ppf(0.0001))
        -3.2905267314418994,  # 0.001 (1/1000)
        -2.8782386238373773,  # 0.002 (1/500)
        -2.5758293035489004,  # 0.005 (1/200)
        -2.3263478740408408,  # 0.01
        -1.9599639845400545,  # 0.025
        -1.6448536269514729,  # 0.05
        -1.2815515655446004,  # 0.10
        -0.8416212335729142,  # 0.20
        -0.5244005127080409,  # 0.30
        -0.2533471031357997,  # 0.40
        0.0,  # 0.50
        0.2533471031357997,  # 0.60
        0.5244005127080407,  # 0.70
        0.8416212335729143,  # 0.80
        1.2815515655446004,  # 0.90
        1.6448536269514729,  # 0.95
        1.9599639845400545,  # 0.975
        2.3263478740408408,  # 0.99
        2.5758293035489004,  # 0.995
        # 2.8782386238373773,  # 0.998
        3.0902323061678132,  # 0.999
        3.719016485156023,  # 0.9999
        4.264890793922602,  # 0.99999
    ]
    for index, y_tick in enumerate(y_ticks):
        first_index = index
        if y_tick > min_y:
            break

    for index, y_tick in enumerate(y_ticks):
        last_index = index
        if y_tick > max_y:
            break

    y_tick_labels = [
        "1/10000",  # 0.0001
        "1/1000",  # 0.001
        "1/500",  # 0.002
        "1/200",  # 0.005
        "1%",  # 0.01
        "2.5%",  # 0.025
        "5%",  # 0.05
        "10%",  # 0.10
        "20%",  # 0.20
        "30%",  # 0.30
        "40%",  # 0.40
        "50%",  # 0.50
        "60%",  # 0.60
        "70%",  # 0.70
        "80%",  # 0.80
        "90%",  # 0.90
        "95%",  # 0.95
        "97.5%",  # 0.975
        "99%",  # 0.99
        "99.5%",  # 0.995
        # "99.8%",  # 0.998
        "99.9%",  # 0.999
        "99.99%",  # 0.9999
        "100%",  # 0.99999
    ]

    # Create final plot
    final_plot = FinalPlot(
        plot_type="espn_versus_dashboard",
        title=title,
        x_label="Time Remaining",
        y_label="Win Probability (%)",
        x_ticks=None,
        x_tick_labels=None,
        y_ticks=y_ticks[first_index : last_index + 1],
        y_tick_labels=y_tick_labels[first_index : last_index + 1],
        min_x=0,  # Changed to 0 since we're showing time remaining
        max_x=48 - start_time,  # Changed to show time remaining
        lines=lines,
        json_name=json_name,
        espn_game_id=espn_game_id,  # Include ESPN game ID in the top level
    )

    # Convert x_values to time remaining for all lines
    for line in lines:
        line.x_values = [48 - x for x in line.x_values]

    final_plot.to_json()

    return title, game_years_strings, game_filter_strings, final_plot
