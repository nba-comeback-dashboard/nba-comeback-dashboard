#!/bin/bash

# Run the test plots script with optional test name regex filter
echo "Running form_nba_chart_test_plots.py..."

# Change to the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

rm ../../../docs/frontend/source/_static/json/charts/test_plots/*
# Run the script with all arguments passed
python-main "./form_nba_chart_test_plots.py" "$@"

