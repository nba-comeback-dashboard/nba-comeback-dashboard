#!/bin/bash

# Find all Python files except our test script
for file in $(find . -name "*.py" | grep -v "form_nba_chart_test_plots.py"); do
  echo "Running $file..."
  python-main "$file"
done