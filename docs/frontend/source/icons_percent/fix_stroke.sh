#!/bin/bash
# Try to fix stroke rendering by using very high density

cd "$(dirname "$0")"

# Generate a single sample icon with very high density
magick nba-comeback-dashboard-percent-fixed.svg \
  -background none \
  -density 2400 \
  -resize 196x196 \
  favicon-196x196.png

echo "Generated high-density favicon-196x196.png"