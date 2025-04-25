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
    use_home_away_game_filters=False,
)

plot_espn_versus_dashboard(
    json_name=f"{chart_base_path}/goto/espn_v_dashboard_all_time_gsw_at_hou_401767823.json.gz",
    espn_game_id="401767823",
    year_groups=eras,
    use_home_away_game_filters=False,
)

plot_espn_versus_dashboard(
    json_name=f"{chart_base_path}/goto/espn_v_dashboard_all_time_min_at_lal_401767915.json.gz",
    espn_game_id="401767915",
    year_groups=eras,
    use_home_away_game_filters=False,
)


plot_espn_versus_dashboard(
    json_name=f"{chart_base_path}/goto/espn_v_dashboard_all_time_grizz_at_okc_401767903.json.gz",
    espn_game_id="401767903",
    year_groups=eras,
    use_home_away_game_filters=False,
)

plot_espn_versus_dashboard(
    json_name=f"{chart_base_path}/goto/espn_v_dashboard_all_time_lac_at_den_401768061.json.gz",
    espn_game_id="401768061",
    year_groups=eras,
    use_home_away_game_filters=True,
)


eras = [
    # ERA ONE
    (2017, 2024),
]

plot_espn_versus_dashboard(
    json_name=f"{chart_base_path}/20_18/espn_v_dashboard_modern_at_home_min_at_bucks_401705718.json.gz",
    espn_game_id="401705718",
    year_groups=eras,
    use_home_away_game_filters=True,
)

"""
Script for generating NBA game analysis charts for 2020-2018 seasons.

This script creates JSON chart data files for visualizing NBA game trends
and win probabilities, with a focus on the 2020-2018 seasons.
"""

import json
import gzip


def read_gzipped_json(filename):
    """
    Read a gzipped JSON file and return the decoded data.

    Args:
        filename (str): Path to the gzipped JSON file

    Returns:
        dict/list: Decoded JSON data
    """
    with gzip.open(filename, "rt", encoding="utf-8") as f:
        return json.load(f)


def write_gzipped_json(data, filename):
    """
    Write data to a gzipped JSON file.

    Args:
        data (dict/list): Data to serialize to JSON
        filename (str): Path where the gzipped JSON file should be written
    """
    with gzip.open(filename, "wt", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


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
    (1996, 2016)
]

plot_espn_versus_dashboard(
    json_name=f"/tmp/a.json.gz",
    espn_game_id="401705718",
    year_groups=eras,
    use_home_away_game_filters=False,
)

eras = [
    # ERA ONE
    (2017, 2024)
]

plot_espn_versus_dashboard(
    json_name=f"/tmp/b.json.gz",
    espn_game_id="401705718",
    year_groups=eras,
    use_home_away_game_filters=False,
)

json_name = f"{chart_base_path}/20_18/espn_v_dashboard_old_school_v_modern_min_at_bucks_401705718.json.gz"

a_data = read_gzipped_json(f"/tmp/a.json.gz")
b_data = read_gzipped_json(f"/tmp/b.json.gz")

a_data["title"] = a_data["title"].split(" | ")[0]

a_data["lines"].append(b_data["lines"][1])

del a_data["lines"][0]

write_gzipped_json(a_data, json_name)

eras = [
    # ERA ONE
    (1996, 2016)
]

plot_espn_versus_dashboard(
    json_name=f"/tmp/a.json.gz",
    espn_game_id="401767915",
    year_groups=eras,
    use_home_away_game_filters=False,
)

eras = [
    # ERA ONE
    (2017, 2024)
]

plot_espn_versus_dashboard(
    json_name=f"/tmp/b.json.gz",
    espn_game_id="401767915",
    year_groups=eras,
    use_home_away_game_filters=False,
)

json_name = f"{chart_base_path}/20_18/espn_v_dashboard_old_school_v_modern_min_at_lal_401767915.json.gz"

a_data = read_gzipped_json(f"/tmp/a.json.gz")
b_data = read_gzipped_json(f"/tmp/b.json.gz")

a_data["title"] = a_data["title"].split(" | ")[0]

a_data["lines"].append(b_data["lines"][1])

del a_data["lines"][0]

write_gzipped_json(a_data, json_name)
