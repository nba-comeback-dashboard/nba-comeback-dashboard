#!/usr/bin/env python3
"""
Script to check the content of ESPN vs Dashboard JSON files.
"""

import json
import gzip
import sys
import os

def check_json_file(file_path):
    """Checks x_values in the JSON file for the sub-minute entries."""
    try:
        with gzip.open(file_path, 'rt') as f:
            data = json.load(f)
        
        print(f"File: {file_path}")
        print(f"Title: {data.get('title', 'No title')}")
        
        # Check for lines
        lines = data.get('lines', [])
        print(f"Number of lines: {len(lines)}")
        
        # Print out x_values for each line
        for i, line in enumerate(lines):
            legend = line.get('legend', f'Line {i+1}')
            print(f"\nLine: {legend}")
            
            # Get x_values directly if present
            if 'x_values' in line:
                x_values = line['x_values']
                print(f"Direct x_values: {sorted(set(x_values))}")
            
            # Check y_values array which contains x_value properties
            y_values = line.get('y_values', [])
            if y_values and isinstance(y_values, list) and isinstance(y_values[0], dict):
                x_values = [point.get('x_value') for point in y_values]
                print(f"x_values from y_values: {sorted(set(x_values))}")
                
                # Check specifically for values between 47 and 48
                sub_minute_values = [x for x in x_values if isinstance(x, (int, float)) and 47 <= x < 48]
                if sub_minute_values:
                    print(f"Sub-minute values (47-48): {sorted(set(sub_minute_values))}")
                    
                    # Map the values to the corresponding time strings
                    time_mapping = {
                        47.0: "1m",
                        47.25: "45s",
                        47.5: "30s",
                        47.75: "15s",
                        47.833: "10s",
                        47.917: "5s"
                    }
                    
                    # Print the mapping
                    for val in sorted(set(sub_minute_values)):
                        time_str = time_mapping.get(val, f"Unknown ({val})")
                        print(f"  {val} => {time_str}")
                else:
                    print("No sub-minute values found.")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    # Check both files
    file1 = "/Users/ajcarter/workspace/GIT_NBACD/docs/frontend/source/_static/json/charts/goto/espn_v_dashboard_all_time_401705718.json.gz"
    file2 = "/Users/ajcarter/workspace/GIT_NBACD/docs/frontend/source/_static/json/charts/goto/espn_v_dashboard_all_time_401705392.json.gz"
    
    check_json_file(file1)
    print("\n" + "="*50 + "\n")
    check_json_file(file2)