# form_nba_chart_json_data_plot_primitives.py
"""
Plot primitive classes for NBA chart data generation.

This module defines the core classes used to create the JSON data structure
for NBA visualization charts. It includes classes for representing lines,
points, and complete plots that can be serialized to JSON.
"""

# Standard library imports
import json
import os

# Local imports
from form_nba_chart_json_data_season_game_loader import GAME_MINUTES, TIME_TO_INDEX_MAP
from form_nba_chart_json_data_num import Num


# Define ScoreStatisticPercent class here to avoid circular imports
class ScoreStatisticPercent:
    def __repr__(self):
        odds, win_count, loss_count, game_count = self.odds
        return f"{int(100.0 * (odds or 0.0))}% {win_count}/{loss_count}"

    def __init__(self):
        self.wins = set()
        self.losses = set()

    @property
    def odds(self):
        try:
            odds = float(len(self.wins) / self.win_plus_loss_count)
        except ZeroDivisionError:
            odds = None
        return [odds, len(self.wins), len(self.losses), self.game_count]

    @property
    def game_count(self):
        return float(len(self.wins | self.losses))

    @property
    def win_plus_loss_count(self):
        return float(len(self.wins) + len(self.losses))

    def to_json(self, games, all_game_ids, calculate_occurrences):
        if not calculate_occurrences:
            json_data = {
                "win_count": len(self.wins),
                "loss_count": len(self.losses),
                "win_plus_loss_count": self.win_plus_loss_count,
                "game_count": self.game_count,
            }
        else:
            json_data = {
                "win_plus_loss_count": self.win_plus_loss_count,
                "game_count": self.game_count,
            }

        if not calculate_occurrences:
            # Sample up to 10 random wins
            win_games = self.wins
            loss_games = self.losses
            mode_keys = ["win", "loss"]
        else:
            occurred_games = self.wins | self.losses
            not_occurred_games = all_game_ids - occurred_games
            mode_keys = ["occurred", "not_occurred"]

        for mode in mode_keys:
            if mode == "not_occurred":
                continue
            game_ids = locals()[f"{mode}_games"]
            if calculate_occurrences:
                game_ids = [game_id.split("_AWAY")[0] for game_id in game_ids]
            game_sample = Num.random.sample(list(game_ids), min(10, len(game_ids)))

            # Create Game objects for the samples
            sorted_games = [games[game_id] for game_id in game_sample]
            sorted_games.sort(key=lambda game: game.game_date)
            json_data[f"{mode}_games"] = [
                {
                    "game_id": game.game_id,
                    "game_date": game.game_date,
                    "game_summary": game.get_game_summary_json_string(),
                }
                for game in sorted_games
            ]

        return json_data


class PlotLine:
    def get_xy(self):
        raise NotImplementedError("Subclasses must implement the get_xy method")


class PointsDownLine(PlotLine):
    """
    Represents a line plotting win probability versus score statistic.

    This class handles the analysis of how win probability changes based on
    various score statistics at different times in a game. It supports analyzing
    different statistics like point margins at specific moments, minimum point
    margins during periods, or playoff series scores.
    """

    # Boundaries for valid percentage values to avoid numerical issues
    min_percent = 1 / 10000000000.0
    max_percent = 1.0 - min_percent

    def __init__(
        self,
        games,
        game_filter,
        start_time,
        score_statistic_mode,
        legend=None,
        cumulate=False,
        min_score_statistic=None,
        max_score_statistic=None,
        fit_min_win_game_count=None,
        fit_max_points=float("inf"),
        calculate_occurrences=False,
    ):
        """
        Initialize a line for analyzing score statistic vs. win probability.

        Parameters:
        -----------
        games : Games
            Collection of games to analyze
        game_filter : GameFilter or None
            Filter to apply to games
        start_time : int or str
            Time point to start analysis from (minute value or sub-minute string)
        score_statistic_mode : str
            Analysis mode:
            - 'point_margin_at_time': Point margin at specific time point
            - 'min_point_margin': Minimum point margin faced during the period
            - 'losing_point_margin_at_time': Negative point margin at specific time
            - 'final_team_score': Final score of team
            - 'playoff_series_score': Playoff series score analysis
        legend : str or None
            Legend text for the line
        cumulate : bool
            Whether to cumulate score statistics for "or more" analysis
        min_score_statistic : int or None
            Minimum score statistic to include
        max_score_statistic : int, "auto", or None
            Maximum score statistic to include
        fit_min_win_game_count : int or None
            Minimum number of wins required for regression
        fit_max_points : float, str, or None
            Maximum points to include in regression fit
        calculate_occurrences : bool
            Whether to calculate occurrence percentages instead of win percentages
        """
        self.plot_type = "percent_v_score_statistic"
        self.games = games
        self.legend = legend

        self.start_time = start_time
        self.score_statistic_mode = score_statistic_mode
        self.calculate_occurrences = calculate_occurrences

        self.score_statistic_map = score_statistic_map = self.setup_score_statistic_map(
            games, game_filter, start_time, score_statistic_mode
        )

        all_game_ids = self.get_all_game_ids()
        self.number_of_games = len(all_game_ids)
        if self.legend:
            self.legend = f"{legend} ({self.number_of_games:,} Games)"

        if cumulate:
            self.cumulate_score_statistics(score_statistic_map)

        # For playoff series analysis, only consider score statistics <= 0
        # This focuses on teams that are tied or behind in the series
        # Disable cumulative calculations (or_less/or_more) as they don't apply to series scores
        if score_statistic_mode == "playoff_series_score":
            or_less_score_statistic = None
            or_more_score_statistic = None
        elif calculate_occurrences:
            or_less_score_statistic = None
            or_more_score_statistic = None
        else:
            or_less_score_statistic, or_more_score_statistic = (
                self.clean_score_statistic_map_end_points(score_statistic_map)
            )

        self.score_statistic_map = score_statistic_map
        self.score_statistics = sorted(score_statistic_map)
        self.percents = [
            score_statistic_map[minute].odds[0] for minute in self.score_statistics
        ]
        if score_statistic_mode == "playoff_series_score":
            self.occurs = []
            for score_statistic in self.score_statistics:
                score_stat_data = score_statistic_map[score_statistic]
                all_games = score_stat_data.wins | score_stat_data.losses
                current_playoff_ids = set()
                for game_id in all_games:
                    game_playoff_id = games.playoff_map.get_series_id(games[game_id])
                    current_playoff_ids.add(game_playoff_id)
                self.occurs.append(len(current_playoff_ids) / len(self.playoff_ids))
        else:
            self.occurs = []
            for score_statistic in self.score_statistics:
                score_stat_data = score_statistic_map[score_statistic]
                game_count = len(score_stat_data.wins | score_stat_data.losses)
                self.occurs.append(game_count / (self.number_of_games))

        if calculate_occurrences:
            self.percents = self.occurs

        self.percents = [max(self.min_percent, percent) for percent in self.percents]
        self.percents = [min(self.max_percent, percent) for percent in self.percents]
        self.sigmas = [Num.PPF(percent) for percent in self.percents]

        fix_max_points = self.fit_regression_lines(
            fit_min_win_game_count,
            fit_max_points,
            calculate_occurrences=calculate_occurrences,
        )
        if score_statistic_mode == "playoff_series_score":
            self.score_statistics = [k for k in self.score_statistics if k <= 0]
            self.score_statistic_map = score_statistic_map = {
                k: v for (k, v) in score_statistic_map.items() if k <= 0
            }
            max_score_statistic = 100

        elif max_score_statistic == "auto":
            max_score_statistic = fix_max_points + 6

        if self.score_statistic_mode == "final_team_score" or self.calculate_occurrences:
            pass
        elif min_score_statistic is not None or max_score_statistic is not None:
            self.filter_max_score_statistic(min_score_statistic, max_score_statistic)

        self.max_score_statistic = max_score_statistic

        self.or_less_score_statistic = or_less_score_statistic
        self.or_more_score_statistic = or_more_score_statistic

    def get_all_game_ids(self):
        """Get all game IDs included in this plot line.

        For playoff series analysis, returns the set of playoff series IDs.
        For regular analysis, returns the set of all game IDs in the score statistic map.
        """
        if self.score_statistic_mode == "playoff_series_score":
            # For playoff series, use the playoff_ids set which tracks series IDs
            # rather than individual game IDs
            all_game_ids = self.playoff_ids
        else:
            # For regular analysis, collect all game IDs from wins and losses
            all_game_ids = set()
            for data in self.score_statistic_map.values():
                all_game_ids.update(data.wins)
                all_game_ids.update(data.losses)
        return all_game_ids

    def setup_score_statistic_map(self, games, game_filter, start_time, score_statistic_mode):
        """
        Create a mapping of score statistics to win/loss outcomes for analysis.

        This method processes the game data according to the specified analysis mode:
        - 'point_margin_at_time': Analyzes point margin at a specific time point
        - 'min_point_margin': Analyzes minimum point margin faced during the period
        - 'losing_point_margin_at_time': Analyzes negative point margin at specific time
        - 'final_team_score': Analyzes final score of team
        - 'playoff_series_score': Analyzes playoff series score

        Parameters:
        -----------
        games : Games
            Collection of games to analyze
        game_filter : GameFilter or None
            Filter to apply to games
        start_time : int or str
            Time point to start analysis from
        score_statistic_mode : str
            Analysis mode

        Returns:
        --------
        dict
            Dictionary mapping score statistics to ScoreStatisticPercent objects

        Raises:
        -------
        AssertionError
            If start_time is not in TIME_TO_INDEX_MAP
        NotImplementedError
            If score_statistic_mode is not one of the supported modes
        """
        score_statistic_map = {}
        if start_time not in TIME_TO_INDEX_MAP:
            raise AssertionError(
                f"Invalid start_time: {start_time}, not found in TIME_TO_INDEX_MAP"
            )

        # Initialize tracking of playoff series IDs when in playoff_series_score mode
        # This set will collect unique series identifiers instead of individual game IDs
        if score_statistic_mode == "playoff_series_score":
            self.playoff_ids = set()

        for game in games:
            if score_statistic_mode == "final_team_score":
                win_score_statistic = max(game.final_home_points, game.final_away_points)
                lose_score_statistic = min(game.final_home_points, game.final_away_points)
            elif score_statistic_mode == "point_margin_at_time":
                # Analyze point margin at the specific time point
                sign = 1 if game.score_diff > 0 else -1
                score_statistic = game.score_statistic_map[start_time]["point_margin"]
                win_score_statistic = sign * score_statistic
                lose_score_statistic = -1 * win_score_statistic
            elif score_statistic_mode == "losing_point_margin_at_time":
                # Analyze negative point margin at the specific time point
                sign = 1 if game.score_diff > 0 else -1
                score_statistic = game.score_statistic_map[start_time]["point_margin"]
                win_score_statistic = sign * score_statistic
                lose_score_statistic = -1 * win_score_statistic
                # Only track negative margins
                if win_score_statistic > 0:
                    win_score_statistic = 0
                if lose_score_statistic > 0:
                    lose_score_statistic = 0
            elif score_statistic_mode == "min_point_margin":
                # Analyze minimum point margin faced during the period
                score_statistic = game.score_statistic_map[start_time]["point_margin"]
                win_score_statistic = float("inf")
                lose_score_statistic = float("inf")

                # Determine the range of time to analyze
                start_index = TIME_TO_INDEX_MAP[start_time]
                stop_index = TIME_TO_INDEX_MAP[0]  # End of game

                # Find the minimum margin throughout the period
                for index in range(start_index, stop_index + 1):
                    time = GAME_MINUTES[index]
                    score_statistic_data = game.score_statistic_map[time]

                    # For first time point, use the current margin
                    if index == start_index:
                        min_score_statistic = score_statistic_data["point_margin"]
                        max_score_statistic = score_statistic_data["point_margin"]
                    else:
                        # For subsequent time points, use min/max values
                        min_score_statistic = score_statistic_data["min_point_margin"]
                        max_score_statistic = score_statistic_data["max_point_margin"]

                    if game.score_diff > 0:  # Home team won
                        win_score_statistic = min(min_score_statistic, win_score_statistic)
                        lose_score_statistic = min(
                            -1.0 * max_score_statistic, lose_score_statistic
                        )
                    elif game.score_diff < 0:  # Away team won
                        win_score_statistic = min(
                            -1.0 * max_score_statistic, win_score_statistic
                        )
                        lose_score_statistic = min(min_score_statistic, lose_score_statistic)
                    else:
                        raise AssertionError("NBA games can't end in a tie")
            # Special handling for playoff series analysis
            elif score_statistic_mode == "playoff_series_score":
                try:
                    # Get score statistics based on playoff series score (e.g., 3-1, 2-3)
                    # Returns a tuple of (win_margin, lose_margin, playoff_id)
                    win_score_statistic, lose_score_statistic, playoff_id = (
                        games.playoff_map.get_playoff_point_margins(game, game_filter)
                    )

                except ValueError:
                    # Skip series that don't meet our criteria (e.g., not completed)
                    continue
                else:
                    # Track this playoff series ID for analysis
                    self.playoff_ids.add(playoff_id)
            else:
                raise NotImplementedError(f"Unsupported score_statistic_mode: {score_statistic_mode}")

            # Record the outcomes based on the game filter

            if self.calculate_occurrences:
                if (
                    self.score_statistic_mode == "min_point_margin"
                    and min(lose_score_statistic, win_score_statistic) == 0
                ):
                    raise AssertionError

                if self.score_statistic_mode == "final_team_score":
                    occurs_score_stat_percent = score_statistic_map.setdefault(
                        win_score_statistic, ScoreStatisticPercent()
                    )
                    occurs_score_stat_percent.wins.add(game.game_id)
                    occurs_score_stat_percent = score_statistic_map.setdefault(
                        lose_score_statistic, ScoreStatisticPercent()
                    )
                    occurs_score_stat_percent.wins.add(f"{game.game_id}_AWAY")
                elif (
                    self.score_statistic_mode == "playoff_series_score" or 
                    self.score_statistic_mode == "point_margin_at_time"
                ):
                    occurs_score_stat_percent = score_statistic_map.setdefault(
                        win_score_statistic, ScoreStatisticPercent()
                    )
                    occurs_score_stat_percent.wins.add(game.game_id)
                    occurs_score_stat_percent = score_statistic_map.setdefault(
                        lose_score_statistic, ScoreStatisticPercent()
                    )
                    occurs_score_stat_percent.wins.add(game.game_id)
                    if self.score_statistic_mode == "playoff_series_score":
                        if win_score_statistic == 0 or lose_score_statistic == 0:
                            raise AssertionError
                        if -3 <= win_score_statistic <= 3:
                            # For playoff series occurs, we track 3-3, 2-2, 1-1 and tied
                            # all as sep. x values.
                            occurs_score_stat_percent = score_statistic_map.setdefault(
                                0, ScoreStatisticPercent()
                            )
                            occurs_score_stat_percent.wins.add(game.game_id)

                elif self.score_statistic_mode == "min_point_margin" or self.score_statistic_mode == "losing_point_margin_at_time":
                    occurs_score_stat_percent = score_statistic_map.setdefault(
                        min(lose_score_statistic, win_score_statistic), ScoreStatisticPercent()
                    )
                    occurs_score_stat_percent.wins.add(game.game_id)
                else:
                    raise Exception

            else:
                if self.score_statistic_mode == "playoff_series_score":
                    playoff_series = games.playoff_map.get_playoff_series(game)
                else:
                    playoff_series = None
                if game_filter is None or game_filter.is_match(
                    game, is_win=True, playoff_series=playoff_series
                ):
                    win_score_stat_percent = score_statistic_map.setdefault(
                        win_score_statistic, ScoreStatisticPercent()
                    )
                    win_score_stat_percent.wins.add(game.game_id)

                if game_filter is None or game_filter.is_match(
                    game, is_win=False, playoff_series=playoff_series
                ):
                    lose_score_stat_percent = score_statistic_map.setdefault(
                        lose_score_statistic, ScoreStatisticPercent()
                    )
                    lose_score_stat_percent.losses.add(game.game_id)

        return score_statistic_map

    def cumulate_score_statistics(self, score_statistic_map):
        score_stat_items = sorted(score_statistic_map.items())
        for index, value in enumerate(score_stat_items):
            p0 = value[1]
            try:
                p1 = score_stat_items[index + 1][1]
            except IndexError:
                break
            else:
                p1.wins.update(p0.wins)
                p1.losses.update(p0.losses)

    def clean_score_statistic_map_end_points(self, score_statistic_map):
        first_score_statistic = None
        for score_statistic, score_stat_percent in sorted(score_statistic_map.items()):
            if score_stat_percent.odds[0] > 0:
                if first_score_statistic is None:
                    first_score_statistic = score_statistic
                break
            else:
                first_score_statistic = score_statistic

        last_score_statistic = None
        for score_statistic, score_stat_percent in sorted(
            score_statistic_map.items(), reverse=True
        ):
            if score_stat_percent.odds[0] < 1.0:
                if last_score_statistic is None:
                    last_score_statistic = score_statistic
                break
            else:
                last_score_statistic = score_statistic

        for score_statistic, score_stat_percent in sorted(score_statistic_map.items()):
            if score_statistic < first_score_statistic:
                wins = score_stat_percent.wins
                if wins:
                    raise AssertionError
                score_statistic_map[first_score_statistic].losses.update(
                    score_stat_percent.losses
                )
                score_statistic_map.pop(score_statistic)
            elif score_statistic > last_score_statistic:
                losses = score_stat_percent.losses
                if losses:
                    raise AssertionError
                score_statistic_map[last_score_statistic].wins.update(
                    score_stat_percent.wins
                )
                score_statistic_map.pop(score_statistic)
        return first_score_statistic, last_score_statistic

    def fit_regression_lines(
        self, min_game_count, max_fit_point, calculate_occurrences
    ):
        if calculate_occurrences:
            self.m = None
            self.b = None
            return max_fit_point

        if str(max_fit_point).endswith("%"):
            amount = float(max_fit_point[:-1]) / 100.0
            for index, max_fit_point_amount in enumerate(self.score_statistics):
                if self.percents[index] > amount:
                    break
            else:
                raise AssertionError(max_fit_point)
            max_fit_point = max_fit_point_amount

            # At least 10 points of fit data
            try:
                safe_fit_point = self.score_statistics[10]
            except IndexError:
                safe_fit_point = self.score_statistics[-1]
            if safe_fit_point > -2:
                safe_fit_point = -2
            max_fit_point = max(max_fit_point, safe_fit_point)
            max_fit_point = max(max_fit_point, -18)

        if self.score_statistics.index(max_fit_point) < 2:
            max_fit_point = self.score_statistics[2]

        min_game_count = min_game_count if min_game_count is not None else 0
        max_fit_point = max_fit_point if max_fit_point is not None else float("inf")

        fit_xy = [
            (score_statistic, self.sigmas[index])
            for index, score_statistic in enumerate(self.score_statistics)
            if
            (
                # len(self.score_statistic_map[score_statistic].wins) >= min_game_count
                self.min_percent <= self.percents[index] <= self.max_percent
                and score_statistic <= max_fit_point
            )
        ]
        fit_x = [p[0] for p in fit_xy]
        fit_y = [p[1] for p in fit_xy]
        if len(fit_x) < 2:
            raise AssertionError
        try:
            result = Num.least_squares(fit_x, fit_y)
            m, b = result["m"], result["b"]
        except:
            raise

        self.m = m
        self.b = b

        X = []
        Y = []
        x = []
        y = []
        for score_statistic, data in sorted(self.score_statistic_map.items()):
            x.append(score_statistic)
            y.append(data.odds[0])
            for game_id in data.wins:
                Y.append(1)
                X.append(score_statistic)
            for game_id in data.losses:
                Y.append(0)
                X.append(score_statistic)
            if score_statistic >= max_fit_point:
                break

        X = Num.array(X)
        Y = Num.array(Y)
        x = Num.array(x)
        y = Num.array(y)

        model_probit = Num.fit_it_mle(X=X, Y=Y, model="probit", m_est=m, b_est=b)

        self.m = model_probit["m"]
        self.b = model_probit["b"]

        return max_fit_point

    @property
    def wins_count(self):
        return [
            len(self.score_statistic_map[score_statistic].wins)
            for score_statistic in self.score_statistics
        ]

    def margin_at_percent(self, percent):
        percent = percent * 0.01
        amount = Num.PPF(percent)
        margin = (amount - self.b) / self.m
        point_A = self.score_statistic_map.get(int(Num.ceil(margin)), ScoreStatisticPercent())
        point_B = self.score_statistic_map.get(
            int(Num.floor(margin)), ScoreStatisticPercent()
        )
        if Num.absolute(point_A.odds[0] or 0.0 - percent) < Num.absolute(
            point_B.odds[0] or 0.0 - percent
        ):
            return margin, int(Num.ceil(margin)), point_A
        else:
            return margin, int(Num.floor(margin)), point_B

    def margin_at_record(self):
        for score_statistic, data in sorted(self.score_statistic_map.items()):
            if data.wins:
                return score_statistic, score_statistic, data

    def filter_max_score_statistic(self, min_score_statistic, max_score_statistic):
        if min_score_statistic is not None:
            self.score_statistic_map = {
                k: v for k, v in self.score_statistic_map.items() if k >= min_score_statistic
            }
            self.score_statistics = sorted(self.score_statistic_map)
            self.percents = self.percents[-len(self.score_statistics) :]
            self.occurs = self.occurs[-len(self.score_statistics) :]
            self.sigmas = self.sigmas[-len(self.score_statistics) :]
        if max_score_statistic is not None:
            self.score_statistic_map = {
                k: v for k, v in self.score_statistic_map.items() if k <= max_score_statistic
            }
            self.score_statistics = sorted(self.score_statistic_map)
            self.percents = self.percents[: len(self.score_statistics)]
            self.occurs = self.occurs[: len(self.score_statistics)]
            self.sigmas = self.sigmas[: len(self.score_statistics)]

    def get_xy(self):
        return self.score_statistics, self.sigmas

    def to_json(self, calculate_occurrences=False):
        json_data = {
            "legend": self.legend,
            "m": self.m,
            "b": self.b,
            "number_of_games": self.number_of_games,
            "or_less_score_statistic": self.or_less_score_statistic,
            "or_more_score_statistic": self.or_more_score_statistic,
        }
        json_data["x_values"] = list(self.score_statistics)
        json_data["y_values"] = y_values = []
        for index, score_statistic in enumerate(self.score_statistics):
            score_stat_json = self.score_statistic_map[score_statistic].to_json(
                self.games,
                self.get_all_game_ids(),
                calculate_occurrences,
            )
            score_stat_json["percent"] = self.percents[index]
            score_stat_json["score_statistic_occurs_percent"] = self.occurs[index]
            score_stat_json["sigma"] = self.sigma_final[index]
            score_stat_json["y_value"] = self.sigma_final[index]
            score_stat_json["x_value"] = self.score_statistics[index]
            y_values.append(score_stat_json)
        return json_data

    def plot_point_raw_margins(self, games):
        # This method is not used in the production code and requires direct
        # plotting libraries. It is kept for reference purposes only.
        pass

    def set_sigma_final(self, min_y, max_y):
        y = self.percents
        y = [max(min_y, p) for p in y]
        y = [min(max_y, p) for p in y]
        y = [Num.PPF(p) for p in y]
        self.sigma_final = y


class PercentLine(PlotLine):
    """
    Represents a line plotting point deficit versus time for a specific win probability.

    This class tracks how the point deficit required for a specific win probability
    changes throughout the game. It can represent both actual data from game analysis
    and theoretical guide curves (such as the square root relationship).
    """

    def __init__(self, games, legend, x_values, line_data):
        """
        Initialize a line for tracking deficit changes over time.

        Parameters:
        -----------
        games : Games or None
            Collection of games analyzed (None for theoretical guide lines)
        legend : str
            Legend text for the line
        x_values : list
            List of time points (typically minutes remaining)
        line_data : list
            Either:
            - List of tuples (deficit, point_margin, PointMarginPercent) for actual data
            - List of float values for theoretical guides
        """
        self.games = games
        self.legend = legend
        self.x_values = x_values
        self.line_data = line_data
        # Store game count for matching PointsDownLine behavior
        self.number_of_games = len(games) if games else 0

    def get_xy(self):
        """
        Get x and y values for plotting.

        Returns:
        --------
        tuple
            (x_values, y_values) where x_values are time points and
            y_values are point deficits
        """
        x_values = self.x_values
        y_values = (
            [point[0] for point in self.line_data]
            if isinstance(self.line_data[0], tuple)
            else self.line_data
        )
        return x_values, y_values

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
        json_data = {
            "legend": self.legend,
            "number_of_games": self.number_of_games,
        }

        if self.legend == "Record":
            adjust_y = 0.2
        else:
            adjust_y = 0.0

        json_data["x_values"] = self.x_values
        json_data["y_values"] = y_values = []

        for index, point in enumerate(self.line_data):
            if isinstance(point, float):
                point_json = {}
                y_value = y_fit_value = point
            else:
                point_margin_percent = point[-1]
                y_value = point[1]
                y_fit_value = point[0] - adjust_y

                if point_margin_percent is None:
                    point_json = {}
                else:
                    point_json = point_margin_percent.to_json(
                        self.games, set(self.games.keys()), calculate_occurrences=False
                    )
                    if self.legend != "Record":
                        if "win_games" in point_json:
                            point_json.pop("win_games")
                        if "loss_games" in point_json:
                            point_json.pop("loss_games")
                        if (
                            hasattr(point_margin_percent, "odds")
                            and point_margin_percent.odds
                        ):
                            point_json["percent"] = point_margin_percent.odds[0]

            point_json["x_value"] = self.x_values[index]
            point_json["y_value"] = y_value
            point_json["y_fit_value"] = y_fit_value
            y_values.append(point_json)

        return json_data


class FinalPlot:
    def __init__(
        self,
        plot_type,
        title,
        x_label,
        y_label,
        x_ticks,
        x_tick_labels,
        y_ticks,
        y_tick_labels,
        min_x,
        max_x,
        lines,
        json_name,
        use_normal_labels=False,
        cumulate=False,
        calculate_occurrences=False,
        espn_game_id=None,
    ):
        self.plot_type = plot_type
        self.title = title
        self.min_x = min_x
        self.max_x = max_x
        self.x_label = x_label

        # For ESPN vs Dashboard plots, always use Win Probability (%)
        if plot_type == "espn_versus_dashboard":
            self.y_label = "Win Probability (%)"
            # Store ESPN game ID for ESPN plots
            self.espn_game_id = espn_game_id
        else:
            self.y_label = ("Win " + "\u03c3") if use_normal_labels else y_label
        # self.x_ticks = x_ticks
        if use_normal_labels == "max_or_more":
            y_ticks = list(Num.arange(-4.0, 2.0, 0.5))
            y_tick_labels = [f"{p:0.2f}" for p in y_ticks]
        elif use_normal_labels == "at":
            y_ticks = list(Num.arange(-3.5, 4.0, 0.5))
            y_tick_labels = [f"{p:0.2f}" for p in y_ticks]
        elif use_normal_labels == "max":
            y_ticks = list(Num.arange(-4.0, 3.0, 0.5))
            y_tick_labels = [f"{p:0.2f}" for p in y_ticks]
        elif not use_normal_labels:
            pass
        else:
            raise NotImplementedError(use_normal_labels)

        self.calculate_occurrences = calculate_occurrences
        self.x_ticks = x_ticks
        self.x_tick_labels = x_tick_labels
        self.y_ticks = y_ticks
        self.y_tick_labels = y_tick_labels
        self.lines = lines
        self.json_name = json_name

    def to_json(self):
        json_data = dict(self.__dict__)
        json_data.pop("json_name")
        lines = json_data.pop("lines")

        json_data["lines"] = json_lines = []

        for line in lines:
            json_lines.append(line.to_json(self.calculate_occurrences))

        # Make sure the directory exists
        if self.json_name is None:
            return
        os.makedirs(os.path.dirname(self.json_name), exist_ok=True)
        if not self.json_name.endswith(".gz"):
            self.json_name = self.json_name + ".gz"
        if self.json_name.endswith(".gz"):
            import gzip

            with gzip.open(self.json_name, "wt") as fileobj:
                fileobj.write(json.dumps(json_data, indent=4))
        else:
            with open(self.json_name, "w") as fileobj:
                fileobj.write(json.dumps(json_data, indent=4))
