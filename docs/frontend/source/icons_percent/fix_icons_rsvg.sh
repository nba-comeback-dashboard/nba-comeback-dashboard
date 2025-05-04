#!/bin/bash
# Fix icon generation with better SVG handling

cd "$(dirname "$0")"

# Try a different approach using librsvg if available
if command -v rsvg-convert &> /dev/null; then
    echo "Using rsvg-convert for better SVG rendering..."
    rsvg-convert -h 196 -w 196 nba-comeback-dashboard-basketball.svg > favicon-196x196.png
    echo "Generated favicon-196x196.png with rsvg-convert"
else
    # Fallback to ImageMagick with explicit stroke preservation
    echo "Using ImageMagick with explicit stroke preservation..."
    
    # Ensure strokes are preserved
    magick nba-comeback-dashboard-basketball.svg \
      -background none \
      -density 600 \
      -stroke on \
      -strokewidth 1 \
      -resize 196x196 \
      favicon-196x196.png
      
    # Also try using inkscape if available
    if command -v inkscape &> /dev/null; then
        echo "Using Inkscape for alternative conversion..."
        inkscape --export-filename=favicon-196x196-inkscape.png \
                --export-width=196 --export-height=196 \
                nba-comeback-dashboard-basketball.svg
    fi
fi

echo "Generated improved icons"