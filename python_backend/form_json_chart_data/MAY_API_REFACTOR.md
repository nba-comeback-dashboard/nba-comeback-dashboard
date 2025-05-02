# May 2025 API Refactoring

This document tracks the comprehensive refactoring of the NBA Chart JSON Data API performed in May 2025.

## Overview

The original API was designed primarily for plotting win probability versus point margin, where negative point margin meant a team was down. Over time, this was extended to cover additional use cases with different data handling approaches. This refactoring standardizes terminology and clarifies the API interface.

## Key Term Changes

| Original Term | New Term |
|---------------|----------|
| `point_margin` | `score_statistic` |
| `down_mode` | `score_statistic_mode` |
| `point_margin_map` | `score_statistic_map` |

## Score Statistic Modes

The `down_mode` parameter has been renamed to `score_statistic_mode` with the following mappings:

| Original Mode | New Mode | Description |
|---------------|----------|-------------|
| "max" | "min_point_margin" | Finds the lowest point margin a team had from the given time to time 0 |
| "at" or "at_margin" | "point_margin_at_time" | The point margin at the given time (can be positive or negative) |
| "at_down" | "losing_point_margin_at_time" | The lowest (negative) point margin at that time |
| "score" | "final_team_score" | The final score a team has (two per game: winner's and loser's) |
| "playoff_series" | "playoff_series_score" | Maps playoff series scores (e.g., 1-0, 2-0, 3-0) to a numerical value for tracking |

## Files Modified

### API Library Files (`form_nba_chart_json_data_api/`)
1. `form_nba_chart_json_data_api.py`
2. `form_nba_chart_json_data_espn_v_dashboard.py`
3. `form_nba_chart_json_data_num.py`
4. `form_nba_chart_json_data_plot_primitives.py`
5. `form_nba_chart_json_data_season_game_loader.py`

### Client Script Files (`form_nba_chart_json_data_for_sphinx_pages/`)
1. `plot_nba_game_data_analysis_20_18.py`
2. `plot_nba_game_data_analysis_series_chances.py` 
3. `plot_nba_game_data_analysis_understand_charts.py`
4. `plot_nba_game_data_analysis_occurs.py`
5. `plot_nba_game_data_analysis_trends.py`
6. `plot_nba_game_data_analysis_playoffs.py`
7. `plot_nba_game_data_analysis_twolves_leads.py`
8. `plot_nba_game_data_analysis_create_plots_page.py`
9. `plot_nba_game_data_analysis_home_away.py`
10. `plot_nba_game_data_analysis_goto.py`
11. `plot_nba_game_data_analysis_calc_default.py`
12. `form_nba_chart_test_plots.py`

## JavaScript Translation Notes

These changes will need to be reflected in the JavaScript implementation as described in:
- `/Users/ajcarter/workspace/GIT_NBACD/docs/frontend/source/_static/CLAUDE.md`
- `/Users/ajcarter/workspace/GIT_NBACD/docs/frontend/source/_static/DASHBOARD.md`

## Detailed Changes

### Function Renames
1. `plot_biggest_deficit` → `create_score_statistic_v_probability_chart_json`

### Core Parameter Renames
1. The `create_score_statistic_v_probability_chart_json` function (previously `plot_biggest_deficit`):
   - `down_mode` → `score_statistic_mode`
   - `min_point_margin` → `min_score_statistic`
   - `max_point_margin` → `max_score_statistic`

2. PointsDownLine class:
   - `down_mode` → `score_statistic_mode`
   - `min_point_margin` → `min_score_statistic`
   - `max_point_margin` → `max_score_statistic`
   - `or_less_point_margin` → `or_less_score_statistic`
   - `or_more_point_margin` → `or_more_score_statistic`

### Class Renames
1. `PointMarginPercent` → `ScoreStatisticPercent`

### Method Renames
1. `get_point_margin_map_from_json()` → `get_score_statistic_map_from_json()`
2. `filter_max_point_margin()` → `filter_max_score_statistic()`
3. `clean_point_margin_map_end_points()` → `clean_score_statistic_map_end_points()`
4. `cumulate_point_totals()` → `cumulate_score_statistics()`

### Property Renames
1. Game class:
   - `point_margin_map` → `score_statistic_map`
2. PointsDownLine class:
   - `point_margin_map` → `score_statistic_map`
   - `point_margins` → `score_statistics`

### FinalPlot Changes
1. Plot type: 
   - `point_margin_v_win_percent` → `score_statistic_v_win_percent`
   
### Mode Value Mapping
All client code that used to call with `down_mode="max"` now calls with `score_statistic_mode="min_point_margin"`, etc.

### Documentation Updates
1. Updated function docstrings to explain new terminology
2. Updated parameter descriptions to be clearer
3. Renamed fields in JSON data structures correspondingly

### Note on Backward Compatibility
This refactoring does NOT maintain backward compatibility with the old parameter names, as per requirements. All client code must be updated to use the new parameter names.