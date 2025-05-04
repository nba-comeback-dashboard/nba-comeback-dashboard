# plot_nba_game_data_analysis_thumb.py
"""
Script for generating thumbnail charts for NBA game analysis.

This script creates simplified JSON chart data files intended for thumbnail
or preview displays of NBA game analysis visualizations.
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
json_base_path = "../../../docs/frontend/source/_static/json/seasons"
chart_base_path = "../../../docs/frontend/source/_static/json/charts"

import form_nba_chart_json_data_season_game_loader as loader

# Convert relative json_base_path to an absolute path
json_base_path = os.path.abspath(os.path.join(script_dir, json_base_path))
loader.json_base_path = json_base_path

base_path = f"{chart_base_path}/thumb"
# Control which plots to generate
plot_all = True

eras_one = [
    # ERA ONE
    Era(1996, 2024),
    # Era(2017, 2024),
]

plot_percent_versus_time(
    json_name=f"{base_path}/nbacd_points_versus_time_all_eras.json",
    year_groups=eras_one,
    start_time=24,
    percents=["20%", "10%", "5%", "1%", "Record"],
)

plot_percent_versus_time(
    json_name=f"{base_path}/nbacd_points_versus_time_with_guides_all_eras.json",
    year_groups=eras_one,
    start_time=24,
    percents=["20%", "5%", "1%"],
    plot_2x_guide=True,
    plot_4x_guide=True,
    plot_6x_guide=True,
)

plot_percent_versus_time(
    json_name=f"{base_path}/nbacd_points_versus_time_with_bad_guides_all_eras.json",
    year_groups=eras_one,
    start_time=16,
    plot_2x_bad_guide=True,
    plot_3x_bad_guide=True,
    percents=["20%", "5%", "1%"],
)

plot_percent_versus_time(
    json_name=f"{base_path}/nbacd_points_versus_time_with_calculated_guides_all_eras.json",
    year_groups=eras_one,
    start_time=24,
    percents=["20%", "5%", "1%"],
    plot_calculated_guides=True,
)

eras_one = [
    # ERA ONE
    Era(1996, 2016),
]


plot_percent_versus_time(
    json_name=f"{base_path}/nbacd_points_versus_time_with_guides_old_school_era.json",
    year_groups=eras_one,
    start_time=24,
    percents=["20%", "5%", "1%"],
    plot_calculated_guides=True,
)

eras_one = [
    # ERA ONE
    Era(2017, 2024),
]

plot_percent_versus_time(
    json_name=f"{base_path}/nbacd_points_versus_time_with_guides_modern_era.json",
    year_groups=eras_one,
    start_time=24,
    percents=["20%", "5%", "1%"],
    plot_calculated_guides=True,
)
