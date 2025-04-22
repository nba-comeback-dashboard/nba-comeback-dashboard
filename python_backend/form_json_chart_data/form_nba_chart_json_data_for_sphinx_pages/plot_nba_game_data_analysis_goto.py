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
    plot_percent_versus_time,
    plot_espn_versus_dashboard,
    GameFilter,
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
    (1996, 2024),
]

plot_espn_versus_dashboard(
    json_name=f"{chart_base_path}/goto/espn_v_dashboard_all_time_min_at_bucks_401705718.json.gz",
    espn_game_id="401705718",
    year_groups=eras,
    game_filters=None,
)

plot_espn_versus_dashboard(
    json_name=f"{chart_base_path}/goto/espn_v_dashboard_all_time_gsw_at_hou_401767823.json.gz",
    espn_game_id="401767823",
    year_groups=eras,
    game_filters=None,
)

eras = [
    # ERA ONE
    (2017, 2024),
]

plot_espn_versus_dashboard(
    json_name=f"{chart_base_path}/goto/espn_v_dashboard_modern_at_home_min_at_bucks_401705718.json.gz",
    espn_game_id="401705718",
    year_groups=eras,
    game_filters=[GameFilter(for_at_home=True)],
)

plot_espn_versus_dashboard(
    json_name=f"{chart_base_path}/goto/espn_v_dashboard_modern_at_home_gsw_at_hou_401767823.json.gz",
    espn_game_id="401767823",
    year_groups=eras,
    game_filters=[GameFilter(for_at_home=True)],
)


# plot_espn_versus_dashboard(
#     json_name=f"{chart_base_path}/goto/espn_v_dashboard_all_time_401705392.json.gz",
#     espn_game_id="401705392",
#     year_groups=eras,
#     game_filters=None,
# )


exit()


eras = [
    # ERA ONE
    (1996, 2024),
]

plot_percent_versus_time(
    json_name=f"{chart_base_path}/goto/nbacd_points_versus_36_time_all_eras.json",
    year_groups=eras,
    start_time=36,
    percents=["33%", "20%", "15%", "10%", "5%", "1%", "Record"],
)


game_filters = [
    GameFilter(for_at_home=True),
]

eras = [
    # ERA ONE
    (2017, 2024),
]

plot_percent_versus_time(
    json_name=f"{chart_base_path}/goto/nbacd_points_versus_36_for_home_modern_era.json",
    year_groups=eras,
    start_time=36,
    percents=["33%", "20%", "15%", "10%", "5%", "1%", "Record"],
    game_filters=game_filters,
)

game_filters = [
    GameFilter(for_at_home=False),
]

plot_percent_versus_time(
    json_name=f"{chart_base_path}/goto/nbacd_points_versus_36_for_away_modern_era.json",
    year_groups=eras,
    start_time=36,
    percents=["33%", "20%", "15%", "10%", "5%", "1%", "Record"],
    game_filters=game_filters,
)


# eras = [
#     # ERA ONE
#     (2017, 2024),
# ]

# plot_percent_versus_time(
#     json_name=f"{chart_base_path}/goto/nbacd_points_versus_36_time_modern_era.json",
#     year_groups=eras,
#     start_time=36,
#     percents=["33%", "20%", "15%", "10%", "5%", "1%", "Record"],
# )

# eras = [
#     # ERA ONE
#     ("P2017", 2024),
# ]

# plot_percent_versus_time(
#     json_name=f"{chart_base_path}/goto/nbacd_points_versus_36_time_modern_era_playoffs.json",
#     year_groups=eras,
#     start_time=36,
#     percents=["33%", "20%", "15%", "10%", "5%", "1%", "Record"],
# )


eras = [
    # ERA ONE
    (2017, 2024),
]

game_filters = [
    GameFilter(for_at_home=True),
]

plot_biggest_deficit(
    json_name=f"{chart_base_path}/goto/at_10_at_home_modern_era.json.gz",
    year_groups=eras,
    start_time=10,
    down_mode="at",
    game_filters=game_filters,
    cumulate=False,
    max_point_margin=-4,
    fit_max_points=-1,
)


eras = [
    # ERA ONE
    (2021, 2024),
]

game_filters = [
    GameFilter(vs_team_abbr="MIN"),
]


plot_biggest_deficit(
    json_name=f"{chart_base_path}/goto/twolves_leads_12_recent.json.gz",
    year_groups=eras,
    start_time=12,
    down_mode="max",
    game_filters=game_filters,
    cumulate=False,
    max_point_margin=-4,
)
