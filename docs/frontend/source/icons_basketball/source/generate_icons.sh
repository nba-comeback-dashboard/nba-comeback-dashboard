#!/bin/bash
# Generate all required PNG icons from the SVG source for favicons
# and Add to Homescreen functionality across all platforms.

# Check if ImageMagick is installed
if ! command -v magick &> /dev/null; then
    if ! command -v convert &> /dev/null; then
        echo "Error: ImageMagick is required but not installed."
        echo "Install it using: brew install imagemagick"
        exit 1
    else
        CONVERT_CMD="convert"
    fi
else
    CONVERT_CMD="magick convert"
fi

# Path to the SVG source file
SVG_SOURCE="nba-comeback-dashboard-basketball.svg"

if [ ! -f "$SVG_SOURCE" ]; then
    echo "Error: SVG source file not found: $SVG_SOURCE"
    exit 1
fi

echo "Generating icons from $SVG_SOURCE..."

# Favicons
echo "Creating favicon-16x16.png (16x16)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 16x16 "favicon-16x16.png"

echo "Creating favicon-32x32.png (32x32)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 32x32 "favicon-32x32.png"

echo "Creating favicon-96x96.png (96x96)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 96x96 "favicon-96x96.png"

echo "Creating favicon-196x196.png (196x196)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 196x196 "favicon-196x196.png"

# For Pixel phones - both 192x192 and 196x196
echo "Creating favicon-192x192.png (192x192)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 192x192 "favicon-192x192.png"

# iOS icons
echo "Creating apple-touch-icon-57x57.png (57x57)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 57x57 "apple-touch-icon-57x57.png"

echo "Creating apple-touch-icon-60x60.png (60x60)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 60x60 "apple-touch-icon-60x60.png"

echo "Creating apple-touch-icon-72x72.png (72x72)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 72x72 "apple-touch-icon-72x72.png"

echo "Creating apple-touch-icon-76x76.png (76x76)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 76x76 "apple-touch-icon-76x76.png"

echo "Creating apple-touch-icon-114x114.png (114x114)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 114x114 "apple-touch-icon-114x114.png"

echo "Creating apple-touch-icon-120x120.png (120x120)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 120x120 "apple-touch-icon-120x120.png"

echo "Creating apple-touch-icon-144x144.png (144x144)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 144x144 "apple-touch-icon-144x144.png"

echo "Creating apple-touch-icon-152x152.png (152x152)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 152x152 "apple-touch-icon-152x152.png"

echo "Creating apple-touch-icon-167x167.png (167x167)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 167x167 "apple-touch-icon-167x167.png"

echo "Creating apple-touch-icon.png (180x180)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 180x180 "apple-touch-icon.png"

# Android icons
echo "Creating web-app-manifest-192x192.png (192x192)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 192x192 "web-app-manifest-192x192.png"

echo "Creating web-app-manifest-512x512.png (512x512)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 512x512 "web-app-manifest-512x512.png"

# Windows tiles
echo "Creating mstile-70x70.png (70x70)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 70x70 "mstile-70x70.png"

echo "Creating mstile-144x144.png (144x144)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 144x144 "mstile-144x144.png"

echo "Creating mstile-150x150.png (150x150)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 150x150 "mstile-150x150.png"

echo "Creating mstile-310x150.png (310x150)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 310x150 "mstile-310x150.png"

echo "Creating mstile-310x310.png (310x310)..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -resize 310x310 "mstile-310x310.png"

# Also create favicon.ico with multiple sizes embedded
echo "Creating favicon.ico with multiple sizes..."
$CONVERT_CMD -background none -density 300 "$SVG_SOURCE" -define icon:auto-resize=16,32,48 "favicon.ico"

echo "Icon generation complete!"