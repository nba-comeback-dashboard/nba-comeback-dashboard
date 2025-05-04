"""
Script for generating NBA game analysis charts for 2020-2018 seasons.

This script creates JSON chart data files for visualizing NBA game trends
and win probabilities, with a focus on the 2020-2018 seasons.
"""

import sys
import os

# Add the API directory to the path using relative path from script location
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
form_nba_chart_json_data_api_dir = os.path.join(
    parent_dir, "form_nba_chart_json_data_api"
)
sys.path.append(form_nba_chart_json_data_api_dir)

# Import API functions
from form_nba_chart_json_data_api import (
    create_score_statistic_v_probability_chart_json,
    GameFilter,
    Era,
)

# Calculate script directory from __file__
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Script directory: {script_dir}")

# Change working directory to the script's location
os.chdir(script_dir)
print(f"Working directory changed to: {os.getcwd()}")
# Base paths for input and output files
json_base_path = (
    "/Users/ajcarter/workspace/GIT_nbacd_GITHUB_IO/docs/_static/json/seasons"
)
chart_base_path = (
    "/Users/ajcarter/workspace/GIT_NBACD/docs/frontend/source/_static/json/charts"
)

import form_nba_chart_json_data_season_game_loader as loader

# Convert relative json_base_path to an absolute path
json_base_path = os.path.abspath(os.path.join(script_dir, json_base_path))
loader.json_base_path = json_base_path


eras = [
    # ERA ONE
    Era(1996, 2023, season_type="playoffs"),
]

# create_score_statistic_v_probability_chart_json(
#     json_name=f"{chart_base_path}/playoff_series/playoff_series_all_time.json.gz",
#     eras=eras,
#     start_time=48,
#     score_statistic_mode="playoff_series_score",
# )

# create_score_statistic_v_probability_chart_json(
#     json_name=f"{chart_base_path}/playoff_series/playoff_series_all_time_occurs.json.gz",
#     eras=eras,
#     start_time=48,
#     score_statistic_mode="playoff_series_score",
#     calculate_occurrences=True,
# )

eras = [
    # ERA ONE
    Era(1996, 2023, season_type="playoffs"),
]

game_filters = [
    GameFilter(playoff_for_home=True),
    GameFilter(playoff_for_home=False),
]

create_score_statistic_v_probability_chart_json(
    json_name=f"{chart_base_path}/playoff_series/playoff_series_all_time_home_v_away.json.gz",
    eras=eras,
    start_time=48,
    score_statistic_mode="playoff_series_score",
    game_filters=game_filters,
)

create_score_statistic_v_probability_chart_json(
    json_name=f"{chart_base_path}/playoff_series/playoff_series_all_time_home_v_away_occurs.json.gz",
    eras=eras,
    start_time=48,
    score_statistic_mode="playoff_series_score",
    game_filters=game_filters,
    calculate_occurrences=True,
)

exit()


eras = [
    # ERA ONE
    Era(1996, 2023, season_type="playoffs"),
]

game_filters = [
    GameFilter(playoff_round=1),
    GameFilter(playoff_round=2),
]

create_score_statistic_v_probability_chart_json(
    json_name=f"{chart_base_path}/playoff_series/playoff_series_all_time_by_round_1_2.json.gz",
    eras=eras,
    start_time=48,
    score_statistic_mode="playoff_series_score",
    game_filters=game_filters,
)

create_score_statistic_v_probability_chart_json(
    json_name=f"{chart_base_path}/playoff_series/playoff_series_all_time_by_round_1_2_occurs.json.gz",
    eras=eras,
    start_time=48,
    score_statistic_mode="playoff_series_score",
    calculate_occurrences=True,
    game_filters=game_filters,
)

game_filters = [
    GameFilter(playoff_round=3),
    GameFilter(playoff_round=4),
]

create_score_statistic_v_probability_chart_json(
    json_name=f"{chart_base_path}/playoff_series/playoff_series_all_time_by_round_3_4.json.gz",
    eras=eras,
    start_time=48,
    score_statistic_mode="playoff_series_score",
    game_filters=game_filters,
)

create_score_statistic_v_probability_chart_json(
    json_name=f"{chart_base_path}/playoff_series/playoff_series_all_time_by_round_3_4_occurs.json.gz",
    eras=eras,
    start_time=48,
    score_statistic_mode="playoff_series_score",
    calculate_occurrences=True,
    game_filters=game_filters,
)


eras = [
    # ERA ONE
    Era(1996, 2016, season_type="playoffs"),
    Era(2017, 2023, season_type="playoffs"),
]

create_score_statistic_v_probability_chart_json(
    json_name=f"{chart_base_path}/playoff_series/playoff_series_old_school_versus_modern.json.gz",
    eras=eras,
    start_time=48,
    score_statistic_mode="playoff_series_score",
)

create_score_statistic_v_probability_chart_json(
    json_name=f"{chart_base_path}/playoff_series/playoff_series_old_school_versus_modern_occurs.json.gz",
    eras=eras,
    start_time=48,
    score_statistic_mode="playoff_series_score",
    calculate_occurrences=True,
)
