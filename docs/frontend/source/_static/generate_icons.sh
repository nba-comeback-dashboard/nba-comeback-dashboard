#!/bin/bash
# Script to generate the various icon sizes needed for web apps

# Define source image
SOURCE_IMG="nbacd_v2.png"
ICONS_DIR="icons"

# Create directory if it doesn't exist
mkdir -p "$ICONS_DIR"

# Generate Android icons
convert "$SOURCE_IMG" -resize 192x192 "$ICONS_DIR/android-chrome-192x192.png"
convert "$SOURCE_IMG" -resize 512x512 "$ICONS_DIR/android-chrome-512x512.png"

# Generate Apple touch icons
convert "$SOURCE_IMG" -resize 180x180 "$ICONS_DIR/apple-touch-icon.png"
convert "$SOURCE_IMG" -resize 152x152 "$ICONS_DIR/apple-touch-icon-152x152.png"
convert "$SOURCE_IMG" -resize 144x144 "$ICONS_DIR/apple-touch-icon-144x144.png"
convert "$SOURCE_IMG" -resize 120x120 "$ICONS_DIR/apple-touch-icon-120x120.png"
convert "$SOURCE_IMG" -resize 114x114 "$ICONS_DIR/apple-touch-icon-114x114.png"
convert "$SOURCE_IMG" -resize 76x76 "$ICONS_DIR/apple-touch-icon-76x76.png"
convert "$SOURCE_IMG" -resize 72x72 "$ICONS_DIR/apple-touch-icon-72x72.png"
convert "$SOURCE_IMG" -resize 57x57 "$ICONS_DIR/apple-touch-icon-57x57.png"

# Generate favicon icons
convert "$SOURCE_IMG" -resize 32x32 "$ICONS_DIR/favicon-32x32.png"
convert "$SOURCE_IMG" -resize 16x16 "$ICONS_DIR/favicon-16x16.png"

# Generate Microsoft tile icon
convert "$SOURCE_IMG" -resize 144x144 "$ICONS_DIR/mstile-144x144.png"

echo "Icon generation complete!"