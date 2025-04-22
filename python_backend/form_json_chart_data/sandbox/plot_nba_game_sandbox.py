"""
Test script for verifying the ESPN vs Dashboard live probability implementation.
"""

import sys
import os

# Add the API directory to the path
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
form_nba_chart_json_data_api_dir = os.path.join(
    parent_dir, "form_nba_chart_json_data_api"
)
sys.path.append(form_nba_chart_json_data_api_dir)

# Import API functions
from form_nba_chart_json_data_api import (
    plot_espn_versus_dashboard,
    GameFilter,
)

# Import the loader module to set json_base_path
import form_nba_chart_json_data_season_game_loader as loader

# Set the path to the JSON season data
json_base_path = os.path.join(parent_dir, "..", "..", "docs", "frontend", "source", "_static", "json", "seasons")
json_base_path = os.path.abspath(json_base_path)
loader.json_base_path = json_base_path
print(f"JSON base path: {json_base_path}")

# Base path for output
output_path = os.path.join(script_dir, "test_output.json.gz")

# Set up era for analysis
eras = [
    (2021, 2024),
]

# Run the function
plot_espn_versus_dashboard(
    json_name=output_path,
    espn_game_id="401705392",  # Use the same ID as in goto script
    year_groups=eras,
    game_filters=None,
)

print(f"Test completed. Output written to: {output_path}")