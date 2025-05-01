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
    plot_biggest_deficit,
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


eras = [
    # ERA ONE
    (1996, 2024),
]

plot_biggest_deficit(
    json_name=f"{chart_base_path}/occurs/all_time_scores.json.gz",
    year_groups=eras,
    start_time=48,
    down_mode="score",
    # cumulate=True,
    min_point_margin=-1000,
    max_point_margin=1000,
    calculate_occurrences=True,
)

plot_biggest_deficit(
    json_name=f"{chart_base_path}/occurs/all_time_scores_or_more.json.gz",
    year_groups=eras,
    start_time=48,
    down_mode="score",
    cumulate=True,
    min_point_margin=-1000,
    max_point_margin=1000,
    calculate_occurrences=True,
)

plot_biggest_deficit(
    json_name=f"{chart_base_path}/occurs/all_time_max_48_point_margin.json.gz",
    year_groups=eras,
    start_time=48,
    down_mode="max",
    # cumulate=True,
    # max_point_margin=1000,
    calculate_occurrences=False,
)

plot_biggest_deficit(
    json_name=f"{chart_base_path}/occurs/all_time_max_or_more_48_point_margin.json.gz",
    year_groups=eras,
    start_time=48,
    down_mode="max",
    cumulate=True,
    max_point_margin=1000,
    calculate_occurrences=True,
)

plot_biggest_deficit(
    json_name=f"{chart_base_path}/occurs/all_time_at_6_point_margin.json.gz",
    year_groups=eras,
    start_time=6,
    down_mode="at_down",
    # cumulate=True,
    max_point_margin=1000,
    calculate_occurrences=True,
)

plot_biggest_deficit(
    json_name=f"{chart_base_path}/occurs/all_time_at_or_more_6_point_margin.json.gz",
    year_groups=eras,
    start_time=6,
    down_mode="at_down",
    cumulate=True,
    max_point_margin=1000,
    calculate_occurrences=True,
)

plot_biggest_deficit(
    json_name=f"{chart_base_path}/occurs/all_time_at_or_more_24_point_margin.json.gz",
    year_groups=eras,
    start_time=24,
    down_mode="at_down",
    cumulate=True,
    max_point_margin=1000,
    calculate_occurrences=True,
)

plot_biggest_deficit(
    json_name=f"{chart_base_path}/occurs/all_time_at_or_more_12_point_margin.json.gz",
    year_groups=eras,
    start_time=12,
    down_mode="at_down",
    cumulate=True,
    max_point_margin=1000,
    calculate_occurrences=True,
)


eras = [
    # ERA ONE
    ("P1996", 2024),
]

plot_biggest_deficit(
    json_name=f"{chart_base_path}/occurs/all_time_playoffs_at_or_more_6_point_margin.json.gz",
    year_groups=eras,
    start_time=6,
    down_mode="at_down",
    cumulate=True,
    max_point_margin=1000,
    calculate_occurrences=True,
)


eras = [
    # ERA ONE
    (1996, 2016),
    (2017, 2024),
]


plot_biggest_deficit(
    json_name=f"{chart_base_path}/occurs/old_school_v_modern_scores.json.gz",
    year_groups=eras,
    start_time=48,
    down_mode="score",
    # cumulate=True,
    min_point_margin=-1000,
    max_point_margin=1000,
    calculate_occurrences=True,
)

plot_biggest_deficit(
    json_name=f"{chart_base_path}/occurs/old_school_v_modern_scores_or_more.json.gz",
    year_groups=eras,
    start_time=48,
    down_mode="score",
    cumulate=True,
    min_point_margin=-1000,
    max_point_margin=1000,
    calculate_occurrences=True,
)


plot_biggest_deficit(
    json_name=f"{chart_base_path}/occurs/old_school_v_modern_max_or_more_48_point_margin.json.gz",
    year_groups=eras,
    start_time=48,
    down_mode="max",
    cumulate=True,
    max_point_margin=1000,
    calculate_occurrences=True,
)


plot_biggest_deficit(
    json_name=f"{chart_base_path}/occurs/old_school_v_modern_at_or_more_6_point_margin.json.gz",
    year_groups=eras,
    start_time=6,
    down_mode="at_down",
    cumulate=True,
    max_point_margin=1000,
    calculate_occurrences=True,
)

plot_biggest_deficit(
    json_name=f"{chart_base_path}/occurs/old_school_v_modern_at_or_more_24_point_margin.json.gz",
    year_groups=eras,
    start_time=24,
    down_mode="at_down",
    cumulate=True,
    max_point_margin=1000,
    calculate_occurrences=True,
)


eras = [
    # ERA ONE
    ("R1996", 2024),
    ("P1996", 2024),
]

plot_biggest_deficit(
    json_name=f"{chart_base_path}/occurs/all_time_reg_v_playoffs_at_or_more_6_point_margin.json.gz",
    year_groups=eras,
    start_time=6,
    down_mode="at_down",
    cumulate=True,
    max_point_margin=1000,
    calculate_occurrences=True,
)

plot_biggest_deficit(
    json_name=f"{chart_base_path}/occurs/all_time_reg_v_playoffs_at_or_more_0_point_margin.json.gz",
    year_groups=eras,
    start_time=0,
    down_mode="at_down",
    cumulate=True,
    max_point_margin=1000,
    calculate_occurrences=True,
)

eras = [
    # ERA ONE
    ("P1996", 2024),
    ("P2021", 2024),
]

plot_biggest_deficit(
    json_name=f"{chart_base_path}/occurs/very_modern_vs_all_time_at_or_more_6_point_margin.json.gz",
    year_groups=eras,
    start_time=6,
    down_mode="at_down",
    cumulate=True,
    max_point_margin=1000,
    calculate_occurrences=True,
)

plot_biggest_deficit(
    json_name=f"{chart_base_path}/occurs/very_modern_vs_all_time_at_or_more_0_point_margin.json.gz",
    year_groups=eras,
    start_time=0,
    down_mode="at_down",
    cumulate=True,
    max_point_margin=1000,
    calculate_occurrences=True,
)
