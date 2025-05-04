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
import re
import argparse

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
    Era,
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
test_charts_html_path = "../../../docs/frontend/source/_static/test_charts.html"

# Convert relative json_base_path to an absolute path
json_base_path = os.path.abspath(os.path.join(script_dir, json_base_path))
loader.json_base_path = json_base_path

# Create test_plots directory if it doesn't exist
test_plots_dir = os.path.join(chart_base_path, "test_plots")
os.makedirs(test_plots_dir, exist_ok=True)

# Dictionary mapping test function names to their descriptions
test_functions = {
    "test_eras": "Testing year group combinations",
    "test_score_statistic_modes": "Testing score statistic modes",
    "test_cumulate": "Testing cumulate parameter",
    "test_game_filters": "Testing game filters",
    "test_calculate_occurrences": "Testing calculate_occurrences",
    "test_start_times": "Testing start times",
    "test_plot_percent_versus_time": "Testing plot_percent_versus_time",
    "test_plot_flags": "Testing plot flags",
    "test_playoff_series": "Testing playoff series",
    "test_espn_dashboard": "Testing ESPN vs Dashboard comparison",
}


def generate_test_charts_html():
    """Generate HTML file with links to all test chart JSONs."""
    # Get list of all JSON files in test_plots directory
    test_files = []
    for file in os.listdir(os.path.join(chart_base_path, "test_plots")):
        if file.endswith(".json") or file.endswith(".json.gz"):
            # Remove .gz extension if present
            base_file = file.replace(".gz", "") if file.endswith(".gz") else file
            test_files.append(base_file)

    # Group files by test categories
    test_categories = {}
    for file in test_files:
        # Extract category from filename
        parts = file.split("_")
        if len(parts) > 1:
            category = "_".join(parts[:-1])
            if category not in test_categories:
                test_categories[category] = []
            test_categories[category].append(file)

    # Generate HTML content with TOC
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>NBA Chart Test Visualizations</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        h2 { color: #444; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; }
        .toc { background-color: #f8f8f8; padding: 15px; border-radius: 5px; margin-bottom: 30px; }
        .toc h2 { margin-top: 0; padding-top: 0; border-top: none; }
        .toc ul { list-style-type: none; padding-left: 10px; }
        .toc li { margin-bottom: 8px; }
        .toc a { text-decoration: none; color: #0066cc; }
        .toc a:hover { text-decoration: underline; }
        .chart-container { margin: 20px 0; }
        .chart-link { margin-bottom: 10px; display: block; }
    </style>
    <script>DOCUMENTATION_OPTIONS = {pagename: 'dashboard/index'};</script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/hammer.js/2.0.8/hammer.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-zoom/2.2.0/chartjs-plugin-zoom.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pako/2.1.0/pako.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/basicLightbox/5.0.0/basicLightbox.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mathjs@11.8.0/lib/browser/math.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/fmin@0.0.4/build/fmin.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap-select@1.14.0-beta3/dist/js/bootstrap-select.min.js"></script>
    
    <!-- NBA Dashboard JS files -->
    <script src="/_static/js/nbacd_utils.js"></script>
    <script src="/_static/js/nbacd_saveas_image_dialog.js"></script>
    <script src="/_static/js/nbacd_plotter_plugins.js"></script>
    <script src="/_static/js/nbacd_dashboard_num.js"></script>
    <script src="/_static/js/nbacd_plotter_data.js"></script>
    <script src="/_static/js/nbacd_plotter_core.js"></script>
    <script src="/_static/js/nbacd_plotter_ui.js"></script>
    <script src="/_static/js/nbacd_chart_loader.js"></script>
    <script src="/_static/js/nbacd_dashboard_season_game_loader.js"></script>
    <script src="/_static/js/nbacd_dashboard_plot_primitives.js"></script>
    <script src="/_static/js/nbacd_dashboard_api.js"></script>
    <script src="/_static/js/nbacd_dashboard_state.js"></script>
    <script src="/_static/js/nbacd_dashboard_ui.js"></script>
    <script src="/_static/js/nbacd_dashboard_init.js"></script>
</head>
<body>
    <h1>NBA Chart Test Visualizations</h1>
    
    <div class="toc">
        <h2>Table of Contents</h2>
        <ul>
"""

    # Add TOC entries
    for category in sorted(test_categories.keys()):
        display_category = category.replace("_", " ").title()
        html_content += (
            f'            <li><a href="#{category}">{display_category}</a></li>\n'
        )

    html_content += """        </ul>
    </div>
    
"""

    # Add chart sections
    for category in sorted(test_categories.keys()):
        display_category = category.replace("_", " ").title()
        html_content += f'    <h2 id="{category}">{display_category}</h2>\n'

        for file in sorted(test_categories[category]):
            file_name = file.replace(".json", "")
            file_path = f"/_static/json/charts/test_plots/{file}"

            html_content += '    <div class="chart-container">\n'
            html_content += (
                f'        <div id="test_plots/{file_name}" class="nbacd-chart"></div>\n'
            )
            html_content += "    </div>\n"

    html_content += """</body>
</html>
"""

    # Write HTML file
    with open(test_charts_html_path, "w") as f:
        f.write(html_content)

    print(f"Generated test charts HTML at {test_charts_html_path}")


def run_tests(test_name_pattern=None):
    """Run all tests for the chart JSON data API with optional test name filter."""
    print("Starting API tests...")

    # Compile regex pattern if provided
    pattern = None
    if test_name_pattern:
        try:
            pattern = re.compile(test_name_pattern, re.IGNORECASE)
            print(f"Filtering tests with pattern: {test_name_pattern}")
        except re.error:
            print(f"Invalid regex pattern: {test_name_pattern}. Running all tests.")
            pattern = None

    # Track which tests were run
    tests_run = []

    # Run each test function if it matches the pattern or no pattern provided
    for test_name, test_description in test_functions.items():
        if pattern is None or pattern.search(test_name):
            print(f"Running test: {test_description}")
            # Get the function object from globals
            test_func = globals()[test_name]
            test_func()
            tests_run.append(test_name)
        else:
            print(f"Skipping test: {test_description}")

    if not tests_run:
        print(f"No tests matched the pattern: {test_name_pattern}")
    else:
        print(f"Completed {len(tests_run)} test(s): {', '.join(tests_run)}")

    # Generate HTML file with chart links
    generate_test_charts_html()

    print("All tests completed successfully!")


def test_eras():
    """Test different year group combinations."""

    # Test 1.1: Single year group (modern era)
    eras = [Era(2017, 2024)]
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/eras_modern.json",
        eras=eras,
        start_time=48,
        score_statistic_mode="min_point_margin",
        cumulate=True,
    )

    # Test 1.2: Multiple year groups (comparing eras)
    eras = [
        Era(1996, 2016),  # Older era
        Era(2017, 2024),  # Modern era
    ]
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/eras_compare_eras.json",
        eras=eras,
        start_time=48,
        score_statistic_mode="min_point_margin",
        cumulate=True,
    )

    # Test 1.3: Regular season vs Playoffs
    eras = [
        Era(1996, 2024, season_type="regular_season"),  # Regular season
        Era(1996, 2024, season_type="playoffs"),  # Playoffs
    ]
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/eras_reg_vs_playoffs.json",
        eras=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        cumulate=False,
    )


def test_score_statistic_modes():
    """Test different score statistic modes."""

    # Use one consistent era for all tests
    eras = [Era(1996, 2024)]

    # Test 2.1: point_margin_at_time mode (previously at_margin)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/score_statistic_mode_point_margin_at_time.json",
        eras=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        cumulate=False,
    )

    # Test 2.2: losing_point_margin_at_time mode (previously at_down)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/score_statistic_mode_losing_point_margin_at_time.json",
        eras=eras,
        start_time=24,
        score_statistic_mode="losing_point_margin_at_time",
        cumulate=False,
    )

    # Test 2.3: min_point_margin mode (previously max)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/score_statistic_mode_min_point_margin.json",
        eras=eras,
        start_time=24,
        score_statistic_mode="min_point_margin",
        cumulate=False,
    )

    # Test 2.4: final_team_score mode (previously score)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/score_statistic_mode_final_team_score.json",
        eras=eras,
        start_time=48,
        score_statistic_mode="final_team_score",
        min_score_statistic=-1000,
        max_score_statistic=1000,
    )


def test_cumulate():
    """Test the cumulate parameter with different settings."""

    eras = [Era(1996, 2024)]

    # Test 3.1: Without cumulate (exact points)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/cumulate_false.json",
        eras=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        cumulate=False,
    )

    # Test 3.2: With cumulate (or more points)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/cumulate_true.json",
        eras=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        cumulate=True,
    )


def test_game_filters():
    """Test different game filter combinations."""

    eras = [Era(1996, 2024)]

    # Test 4.1: Home vs Away filter
    game_filters = [
        GameFilter(for_at_home=True),  # Home team wins
        GameFilter(for_at_home=False),  # Away team wins
    ]

    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/filters_home_away.json",
        eras=eras,
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
        eras=eras,
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
        eras=eras,
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
        eras=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        game_filters=game_filters,
    )

    # Test 4.5: Playoff round filter
    eras = [Era(1996, 2024, season_type="Playoffs")]
    game_filters = [
        GameFilter(playoff_round=1),  # First round
        GameFilter(playoff_round=4),  # Finals
    ]

    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/filters_playoff_round.json",
        eras=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        game_filters=game_filters,
    )


def test_calculate_occurrences():
    """Test the calculate_occurrences parameter."""

    eras = [Era(1996, 2024)]

    # Test 5.1: Win probabilities (default)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/calc_occurr_false.json",
        eras=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        calculate_occurrences=False,
    )

    # Test 5.2: Occurrence percentages
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/calc_occurr_true.json",
        eras=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        calculate_occurrences=True,
    )

    # Test 5.3: Score distribution with occurrences
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/calc_occurr_score.json",
        eras=eras,
        start_time=48,
        score_statistic_mode="final_team_score",
        min_score_statistic=-1000,
        max_score_statistic=1000,
        calculate_occurrences=True,
    )


def test_start_times():
    """Test different start time values including special string times."""

    eras = [Era(1996, 2024)]

    # Test 6.1: Start from beginning (48 minutes)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/time_48min.json",
        eras=eras,
        start_time=48,
        score_statistic_mode="min_point_margin",
    )

    # Test 6.2: Start from halftime (24 minutes)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/time_24min.json",
        eras=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
    )

    # Test 6.3: Start from 4th quarter (12 minutes)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/time_12min.json",
        eras=eras,
        start_time=12,
        score_statistic_mode="point_margin_at_time",
    )

    # Test 6.4: Start from last minute (1 minute)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/time_1min.json",
        eras=eras,
        start_time=1,
        score_statistic_mode="point_margin_at_time",
    )

    # Test 6.5: Start from 45 seconds left (sub-minute string)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/time_45sec.json",
        eras=eras,
        start_time="45s",
        score_statistic_mode="point_margin_at_time",
    )

    # Test 6.6: Start from end of regulation (0 minutes)
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/time_0min.json",
        eras=eras,
        start_time=0,
        score_statistic_mode="point_margin_at_time",
    )


def test_plot_percent_versus_time():
    """Test the plot_percent_versus_time function with different parameters."""

    eras = [Era(1996, 2024)]

    # Test 7.1: Basic plot_percent_versus_time
    plot_percent_versus_time(
        json_name=f"{chart_base_path}/test_plots/percent_v_time_basic.json",
        eras=eras,
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
        eras=eras,
        start_time=24,
        percents=["10%", "1%"],
        game_filters=game_filters,
    )

    # Test 7.3: With guide lines
    plot_percent_versus_time(
        json_name=f"{chart_base_path}/test_plots/percent_v_time_guides.json",
        eras=eras,
        start_time=24,
        percents=["5%"],
        plot_2x_guide=True,
        plot_4x_guide=True,
    )


def test_plot_flags():
    """Test various plot flag options."""

    eras = [Era(1996, 2024)]

    # Test 8.1: Normal labels
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/flags_normal_labels.json",
        eras=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        use_normal_labels="at",
    )

    # Test 8.2: Linear y-axis
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/flags_linear_y_axis.json",
        eras=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        linear_y_axis=True,
    )

    # Test 8.3: Logit transformation
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/flags_logit.json",
        eras=eras,
        start_time=24,
        score_statistic_mode="point_margin_at_time",
        use_logit=True,
    )


def test_playoff_series():
    """Test playoff series analysis mode."""

    # Only use playoff data for playoff series analysis
    eras = [Era(1996, 2024, season_type="Playoffs")]

    # Test 9.1: Basic playoff series analysis
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/playoff_series_basic.json",
        eras=eras,
        start_time=48,
        score_statistic_mode="playoff_series_score",
    )

    # Test 9.2: Playoff series with occurrences
    create_score_statistic_v_probability_chart_json(
        json_name=f"{chart_base_path}/test_plots/playoff_series_occurrences.json",
        eras=eras,
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
        eras=eras,
        start_time=48,
        score_statistic_mode="playoff_series_score",
        game_filters=game_filters,
    )


def test_espn_dashboard():
    """Test ESPN vs Dashboard comparison."""

    # Example ESPN game ID - Minnesota vs Buck
    espn_game_id = "401705718"

    # Era for Dashboard calculations
    eras = [Era(1996, 2024)]

    # Test 10.1: Basic ESPN vs Dashboard comparison
    plot_espn_versus_dashboard(
        json_name=f"{chart_base_path}/test_plots/espn_dashboard_basic.json",
        espn_game_id=espn_game_id,
        eras=eras,
        show_team="away",  # Minnesota perspective
    )

    # Test 10.2: With home/away game filters
    plot_espn_versus_dashboard(
        json_name=f"{chart_base_path}/test_plots/espn_dashboard_home_away.json",
        espn_game_id=espn_game_id,
        eras=eras,
        use_home_away_game_filters=True,
        show_team="away",
    )


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Run test plots for NBA chart JSON data API"
    )
    parser.add_argument(
        "--test-name", type=str, help="Regex pattern to filter test names"
    )
    args = parser.parse_args()

    # Run tests with optional filter
    run_tests(args.test_name)
