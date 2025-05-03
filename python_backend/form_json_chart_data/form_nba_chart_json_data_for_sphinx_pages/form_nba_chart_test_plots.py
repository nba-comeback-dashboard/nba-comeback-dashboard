"""
Test script for NBA chart JSON data API.

This script tests all the main features of the form_nba_chart_json_data_api by making
calls with different parameters to ensure all functionality works as expected.

The script was created to provide a central place for testing all API features and
to make it easy to add new test cases as the API evolves. If new functionality is
added to the API, new test cases should be added to this script.

All test outputs go to the '/test_plots/' directory instead of specific feature directories
used in the original scripts.
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
    plot_espn_versus_dashboard,
    GameFilter,
)

import form_nba_chart_json_data_season_game_loader as loader

# Calculate script directory from __file__
print(f"Script directory: {script_dir}")

# Change working directory to the script's location
os.chdir(script_dir)
print(f"Working directory changed to: {os.getcwd()}")

# Base paths for input and output files
json_base_path = "../../../docs/frontend/source/_static/json/seasons"
chart_base_path = "../../../docs/frontend/source/_static/json/charts"

# Convert relative json_base_path to an absolute path
json_base_path = os.path.abspath(os.path.join(script_dir, json_base_path))
loader.json_base_path = json_base_path

# Create test_plots directory if it doesn't exist
test_plots_dir = os.path.join(chart_base_path, "test_plots")
os.makedirs(test_plots_dir, exist_ok=True)


def run_tests():
    """Run all tests for the chart JSON data API."""
    print("Starting API tests...")

    # Test 1: Basic create_score_statistic_v_probability_chart_json with different year groups
    print("Test 1: Testing create_score_statistic_v_probability_chart_json with different year groups")
    test_year_groups()

    # Test 2: Different score statistic modes
    print("Test 2: Testing different score statistic modes")
    test_score_statistic_modes()

    # Test 3: Testing cumulate parameter
    print("Test 3: Testing cumulate parameter")
    test_cumulate()

    # Test 4: Test game filters
    print("Test 4: Testing game filters")
    test_game_filters()

    # Test 5: Test calculate_occurrences
    print("Test 5: Testing calculate_occurrences")
    test_calculate_occurrences()

    # Test 6: Test special time strings and different start_times
    print("Test 6: Testing special time strings and different start_times")
    test_start_times()

    # Test 7: Test plot_percent_versus_time
    print("Test 7: Testing plot_percent_versus_time")
    test_plot_percent_versus_time()

    # Test 8: Test plot flags (normal labels, linear y axis, logit)
    print("Test 8: Testing plot flags")
    test_plot_flags()

    # Test 9: Test playoff series analysis
    print("Test 9: Testing playoff series analysis")
    test_playoff_series()

    # Test 10: Test ESPN vs Dashboard comparison
    print("Test 10: Testing ESPN vs Dashboard comparison")
    test_espn_dashboard()

    print("All tests completed successfully!")


def test_year_groups():
    """Test different year group combinations."""

    # Test 1.1: Single year group (modern era)
    eras = [(2017, 2024)]
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/year_groups_modern.json",
        year_groups=eras,
        start_time=48,
        score_statistic_mode="min_point_margin",
        cumulate=True,
    )

    # Test 1.2: Multiple year groups (comparing eras)
    eras = [
        (1996, 2016),  # Older era
        (2017, 2024),  # Modern era
    ]
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/year_groups_compare_eras.json",
        year_groups=eras,
        start_time=48,
        score_statistic_mode="min_point_margin",
        cumulate=True,
    )

    # Test 1.3: Regular season vs Playoffs
    eras = [
        ("R1996", 2024),  # Regular season
        ("P1996", 2024),  # Playoffs
    ]
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/year_groups_reg_vs_playoffs.json",
        year_groups=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        cumulate=False,
    )


def test_score_statistic_modes():
    """Test different score statistic modes."""

    # Use one consistent era for all tests
    eras = [(1996, 2024)]

    # Test 2.1: point_margin_at_time mode (previously at_margin)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/score_statistic_mode_point_margin_at_time.json",
        year_groups=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        cumulate=False,
    )

    # Test 2.2: losing_point_margin_at_time mode (previously at_down)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/score_statistic_mode_losing_point_margin_at_time.json",
        year_groups=eras,
        start_time=24,
        score_statistic_mode="losing_point_margin_at_time",
        cumulate=False,
    )

    # Test 2.3: min_point_margin mode (previously max)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/score_statistic_mode_min_point_margin.json",
        year_groups=eras,
        start_time=24,
        score_statistic_mode="min_point_margin",
        cumulate=False,
    )

    # Test 2.4: final_team_score mode (previously score)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/score_statistic_mode_final_team_score.json",
        year_groups=eras,
        start_time=48,
        score_statistic_mode="final_team_score",
        min_score_statistic=-1000,
        max_score_statistic=1000,
    )


def test_cumulate():
    """Test the cumulate parameter with different settings."""

    eras = [(1996, 2024)]

    # Test 3.1: Without cumulate (exact points)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/cumulate_false.json",
        year_groups=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        cumulate=False,
    )

    # Test 3.2: With cumulate (or more points)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/cumulate_true.json",
        year_groups=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        cumulate=True,
    )


def test_game_filters():
    """Test different game filter combinations."""

    eras = [(1996, 2024)]

    # Test 4.1: Home vs Away filter
    game_filters = [
        GameFilter(for_at_home=True),  # Home team wins
        GameFilter(for_at_home=False),  # Away team wins
    ]

    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/filters_home_away.json",
        year_groups=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        game_filters=game_filters,
    )

    # Test 4.2: Team ranking filter
    game_filters = [
        GameFilter(for_rank="top_10"),  # Top 10 team wins
        GameFilter(for_rank="bot_10"),  # Bottom 10 team wins
    ]

    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/filters_team_rank.json",
        year_groups=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        game_filters=game_filters,
    )

    # Test 4.3: Matchup filter
    game_filters = [
        GameFilter(for_rank="top_10", vs_rank="bot_10"),  # Top 10 vs Bottom 10
    ]

    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/filters_matchup.json",
        year_groups=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        game_filters=game_filters,
    )

    # Test 4.4: Team-specific filter
    game_filters = [
        GameFilter(for_team_abbr="MIN"),  # Minnesota wins
    ]

    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/filters_specific_team.json",
        year_groups=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        game_filters=game_filters,
    )

    # Test 4.5: Playoff round filter
    eras = [("P1996", 2024)]
    game_filters = [
        GameFilter(playoff_round=1),  # First round
        GameFilter(playoff_round=4),  # Finals
    ]

    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/filters_playoff_round.json",
        year_groups=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        game_filters=game_filters,
    )


def test_calculate_occurrences():
    """Test the calculate_occurrences parameter."""

    eras = [(1996, 2024)]

    # Test 5.1: Win probabilities (default)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/calc_occurr_false.json",
        year_groups=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        calculate_occurrences=False,
    )

    # Test 5.2: Occurrence percentages
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/calc_occurr_true.json",
        year_groups=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        calculate_occurrences=True,
    )

    # Test 5.3: Score distribution with occurrences
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/calc_occurr_score.json",
        year_groups=eras,
        start_time=48,
        score_statistic_mode="final_team_score",
        min_score_statistic=-1000,
        max_score_statistic=1000,
        calculate_occurrences=True,
    )


def test_start_times():
    """Test different start time values including special string times."""

    eras = [(1996, 2024)]

    # Test 6.1: Start from beginning (48 minutes)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/time_48min.json",
        year_groups=eras,
        start_time=48,
        score_statistic_mode="min_point_margin",
    )

    # Test 6.2: Start from halftime (24 minutes)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/time_24min.json",
        year_groups=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
    )

    # Test 6.3: Start from 4th quarter (12 minutes)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/time_12min.json",
        year_groups=eras,
        start_time=12,
        score_statistic_mode="point_margin_at_time",
    )

    # Test 6.4: Start from last minute (1 minute)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/time_1min.json",
        year_groups=eras,
        start_time=1,
        score_statistic_mode="point_margin_at_time",
    )

    # Test 6.5: Start from 45 seconds left (sub-minute string)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/time_45sec.json",
        year_groups=eras,
        start_time="45s",
        score_statistic_mode="point_margin_at_time",
    )

    # Test 6.6: Start from end of regulation (0 minutes)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/time_0min.json",
        year_groups=eras,
        start_time=0,
        score_statistic_mode="point_margin_at_time",
    )


def test_plot_percent_versus_time():
    """Test the plot_percent_versus_time function with different parameters."""

    eras = [(1996, 2024)]

    # Test 7.1: Basic plot_percent_versus_time
    plot_percent_versus_time(
        json_name=f"{chart_base_path}/test_plots/percent_v_time_basic.json",
        year_groups=eras,
        start_time=24,
        percents=["20%", "10%", "5%", "1%"],
    )

    # Test 7.2: With game filters
    game_filters = [
        GameFilter(for_at_home=True),
        GameFilter(for_at_home=False),
    ]

    plot_percent_versus_time(
        json_name=f"{chart_base_path}/test_plots/percent_v_time_filters.json",
        year_groups=eras,
        start_time=24,
        percents=["10%", "1%"],
        game_filters=game_filters,
    )

    # Test 7.3: With guide lines
    plot_percent_versus_time(
        json_name=f"{chart_base_path}/test_plots/percent_v_time_guides.json",
        year_groups=eras,
        start_time=24,
        percents=["5%"],
        plot_2x_guide=True,
        plot_4x_guide=True,
    )


def test_plot_flags():
    """Test various plot flag options."""

    eras = [(1996, 2024)]

    # Test 8.1: Normal labels
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/flags_normal_labels.json",
        year_groups=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        use_normal_labels="at",
    )

    # Test 8.2: Linear y-axis
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/flags_linear_y_axis.json",
        year_groups=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        linear_y_axis=True,
    )

    # Test 8.3: Logit transformation
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/flags_logit.json",
        year_groups=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        use_logit=True,
    )


def test_playoff_series():
    """Test playoff series analysis mode."""

    # Only use playoff data for playoff series analysis
    eras = [("P1996", 2024)]

    # Test 9.1: Basic playoff series analysis
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/playoff_series_basic.json",
        year_groups=eras,
        start_time=48,
        score_statistic_mode="playoff_series_score",
    )

    # Test 9.2: Playoff series with occurrences
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/playoff_series_occurrences.json",
        year_groups=eras,
        start_time=48,
        score_statistic_mode="playoff_series_score",
        calculate_occurrences=True,
    )

    # Test 9.3: Playoff series with home/away filters
    game_filters = [
        GameFilter(playoff_for_home=True),
        GameFilter(playoff_for_home=False),
    ]

    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/playoff_series_home_away.json",
        year_groups=eras,
        start_time=48,
        score_statistic_mode="playoff_series_score",
        game_filters=game_filters,
    )


def test_espn_dashboard():
    """Test ESPN vs Dashboard comparison."""

    # Example ESPN game ID - Minnesota vs Denver 2022-04-26
    espn_game_id = "401430254"

    # Era for Dashboard calculations
    eras = [(1996, 2024)]

    # Test 10.1: Basic ESPN vs Dashboard comparison
    plot_espn_versus_dashboard(
        json_name=f"{chart_base_path}/test_plots/espn_dashboard_basic.json",
        espn_game_id=espn_game_id,
        year_groups=eras,
        show_team="away",  # Minnesota perspective
    )

    # Test 10.2: With home/away game filters
    plot_espn_versus_dashboard(
        json_name=f"{chart_base_path}/test_plots/espn_dashboard_home_away.json",
        espn_game_id=espn_game_id,
        year_groups=eras,
        use_home_away_game_filters=True,
        show_team="away",
    )


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test_year_groups":
        test_year_groups()
    else:
        run_tests()
