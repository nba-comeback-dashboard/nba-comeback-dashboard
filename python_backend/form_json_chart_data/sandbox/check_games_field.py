#!/usr/bin/env python3
"""Script to check if number_of_games field has been removed from JSON files."""

import json
import gzip
import os
import sys

def check_file(file_path):
    """Checks if the 'number_of_games' field is present in a JSON file."""
    with gzip.open(file_path, 'rt') as f:
        data = json.load(f)
    
    print(f"File: {file_path}")
    
    # Check lines for number_of_games
    lines = data.get('lines', [])
    for i, line in enumerate(lines):
        if 'number_of_games' in line:
            print(f"  Line {i+1} ({line.get('legend', 'Unknown')}): number_of_games field IS present!")
            print(f"  number_of_games = {line['number_of_games']}")
        else:
            print(f"  Line {i+1} ({line.get('legend', 'Unknown')}): number_of_games field is NOT present (good)")
    
    print()

# Check both ESPN vs Dashboard files
base_path = "/Users/ajcarter/workspace/GIT_NBACD/docs/frontend/source/_static/json/charts/goto"
files = [
    os.path.join(base_path, "espn_v_dashboard_all_time_401705718.json.gz"),
    os.path.join(base_path, "espn_v_dashboard_all_time_401705392.json.gz")
]

for file_path in files:
    if os.path.exists(file_path):
        check_file(file_path)
    else:
        print(f"File not found: {file_path}")