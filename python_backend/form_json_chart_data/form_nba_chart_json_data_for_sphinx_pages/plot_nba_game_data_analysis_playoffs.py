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
    plot_percent_versus_time,
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
    Era(1996, 2024, season_type="regular_season"),
    Era(1996, 2024, season_type="playoffs"),
]

create_score_statistic_v_probability_chart_json(
    json_name=f"{chart_base_path}/playoffs/max_down_or_more_48_reg_v_playoffs_all_time.json.gz",
    eras=eras,
    start_time=48,
    score_statistic_mode="min_point_margin",
    cumulate=True,
)

create_score_statistic_v_probability_chart_json(
    json_name=f"{chart_base_path}/playoffs/at_24_reg_v_playoffs_all_time.json.gz",
    eras=eras,
    start_time=24,
    score_statistic_mode="point_margin_at_time",
    cumulate=False,
)

create_score_statistic_v_probability_chart_json(
    json_name=f"{chart_base_path}/playoffs/at_12_reg_v_playoffs_all_time.json.gz",
    eras=eras,
    start_time=12,
    score_statistic_mode="point_margin_at_time",
    cumulate=False,
)

plot_percent_versus_time(
    json_name=f"{chart_base_path}/playoffs/percent_from_24_reg_v_playoffs_all_time.json.gz",
    eras=eras,
    start_time=24,
    percents=["5%"],
)
