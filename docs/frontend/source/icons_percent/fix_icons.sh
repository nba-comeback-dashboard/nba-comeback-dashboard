#!/bin/bash
# Fix icon generation with higher quality settings

cd "$(dirname "$0")"

# Generate one icon with debug info to see what's happening
magick nba-comeback-dashboard-basketball.svg \
  -background none \
  -density 600 \
  -verbose \
  test-icon.png

# Try with higher density and specific rendering options
magick nba-comeback-dashboard-basketball.svg \
  -background none \
  -density 600 \
  -quality 100 \
  favicon-196x196.png

# Generate favicon.ico with better quality
magick nba-comeback-dashboard-basketball.svg \
  -background none \
  -density 300 \
  -define icon:auto-resize=16,32,48 \
  favicon.ico

echo "Generated test icons with higher quality settings"