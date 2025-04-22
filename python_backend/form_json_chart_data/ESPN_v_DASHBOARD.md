# ESPN vs Dashboard Win Probability Implementation

## Overview

This document summarizes the implementation of comparing ESPN's win probability data with NBA Dashboard calculated probabilities. The functionality allows creating visual comparisons between ESPN's live win probability predictions and our own mathematical models based on historical NBA data.

## Implementation Details

### New Files and Functions

1. **New Module**: `form_nba_chart_json_data_espn_v_dashboard.py`
   - Contains classes and functions for fetching, processing, and visualizing ESPN win probability data
   - Implements comparison with Dashboard-calculated probabilities

2. **New API Function**: `plot_espn_versus_dashboard` in `form_nba_chart_json_data_api.py`
   - Main entry point for creating comparison visualizations
   - Takes ESPN game ID, year groups, and game filters as parameters
   - Produces a JSON file that can be consumed by the frontend visualization code

3. **New Plot Line Classes**:
   - `EspnLine`: Represents ESPN win probability data
   - `DashboardLine`: Represents Dashboard-calculated win probability data

### Key Functionality

1. **ESPN Data Fetching**:
   - Connect to ESPN API to fetch game data for specific games
   - Extract play-by-play data and associated win probability values
   - Process data into format suitable for visualization

2. **Dashboard Probability Calculation**:
   - Use existing `PointsDownLine` methodology to calculate win probabilities
   - Support for different time points (minutes elapsed)
   - Intelligent handling of point margins (positive/negative)
   - Support for different game filters (home/away teams)

3. **Time Vector Handling**:
   - Support for regular time periods plus overtime periods
   - Handling of sub-minute time intervals in final minute
   - Consistent time representation across both data sources

4. **Visualization Data**:
   - Generate comparison JSON data for frontend consumption
   - Include metadata like team names, game date, etc.
   - Support URL linking for further exploration

## Usage

The function can be called as follows:

```python
plot_espn_versus_dashboard(
    json_name=f"{chart_base_path}/goto/espn_v_dashboard_all_time_401705718.json.gz",
    espn_game_id="401705718",
    year_groups=eras,
    game_filters=game_filters,
)
```

Where:
- `json_name`: Path to save the output JSON file
- `espn_game_id`: ESPN's unique identifier for the game
- `year_groups`: List of (start_year, end_year) tuples for Dashboard calculations
- `game_filters`: Optional filters for Dashboard calculations

## Frontend Integration

The output JSON files follow the same structure as other chart data files, with additional fields specific to the ESPN vs Dashboard comparison. The frontend code will need to be updated to properly render this new chart type.

## Technical Implementation Notes

1. **Data Interpolation**: Uses interpolation to handle missing data points

2. **Game Filter Logic**: Intelligently applies game filters based on point margin:
   - When home team is leading: Uses away team filter for Dashboard calculations
   - When away team is leading: Uses home team filter for Dashboard calculations

3. **Year Range Support**: 
   - Full historical data (1996-2024)
   - Modern era data only (2017-2024)

4. **Legend Handling**:
   - Automatic generation of appropriate legends based on filters and year groups
   - Proper team attribution in legends

5. **URL Construction**:
   - Creates URLs for the frontend to link to additional chart data
   - Includes year and filter parameters

## Next Steps

1. Update the frontend code to properly render the new chart type
2. Consider additional comparison metrics between ESPN and Dashboard probabilities
3. Explore model enhancements based on observed differences
4. Add support for real-time updates during live games