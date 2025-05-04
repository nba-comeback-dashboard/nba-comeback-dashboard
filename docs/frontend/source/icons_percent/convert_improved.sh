#!/bin/bash
# Convert SVG to PNG with improved settings for stroke preservation

cd "$(dirname "$0")"

# Use the fixed SVG with explicit stroke attributes
SOURCE_SVG="nba-comeback-dashboard-percent-fixed.svg"

# Generate a sample icon to check quality
magick $SOURCE_SVG \
  -background none \
  -density 1200 \
  -quality 100 \
  favicon-196x196.png

# Generate favicon.ico with better quality
magick $SOURCE_SVG \
  -background none \
  -density 600 \
  -define icon:auto-resize=16,32,48 \
  favicon.ico

echo "Generated improved icons with fixed SVG"