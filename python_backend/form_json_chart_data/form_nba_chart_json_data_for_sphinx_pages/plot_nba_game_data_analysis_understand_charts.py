# plot_nba_game_data_analysis_20_18.py
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
    Era,
)

# Calculate script directory from __file__
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Script directory: {script_dir}")

# Change working directory to the script's location
os.chdir(script_dir)
print(f"Working directory changed to: {os.getcwd()}")
# Base paths for input and output files
json_base_path = "../../../docs/frontend/source/_static/json/seasons"
chart_base_path = "../../../docs/frontend/source/_static/json/charts"

import form_nba_chart_json_data_season_game_loader as loader

# Convert relative json_base_path to an absolute path
json_base_path = os.path.abspath(os.path.join(script_dir, json_base_path))
loader.json_base_path = json_base_path


eras_one = [
    # ERA ONE
    Era(1997, 1997, season_type="regular_season"),
    Era(2022, 2022, season_type="regular_season"),
    Era(2023, 2023, season_type="regular_season"),
]

create_score_statistic_v_probability_chart_json(
    json_name=f"{chart_base_path}/understand/nbacd_max_or_more_48_espn_0.json",
    eras=eras_one,
    start_time=48,
    down_mode="max",
    cumulate=True,
    max_point_margin=-2,
)


eras_one = [
    # ERA ONE
    Era(1996, 2016),
    Era(2017, 2024),
]

create_score_statistic_v_probability_chart_json(
    json_name=f"{chart_base_path}/understand/nbacd_max_48_eras_1.json",
    eras=eras_one,
    start_time=48,
    down_mode="max",
    cumulate=False,
    max_point_margin=2,
)


create_score_statistic_v_probability_chart_json(
    json_name=f"{chart_base_path}/understand/nbacd_down_at_24_eras_1.json",
    eras=eras_one,
    start_time=24,
    score_statistic_mode="point_margin_at_time",
    cumulate=False,
    max_score_statistic=2,
)
