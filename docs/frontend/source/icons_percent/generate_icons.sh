#!/bin/bash
# Generate all icons from the SVG source

# Change to the directory where this script is located
cd "$(dirname "$0")"

# Run the Python script to generate the icons
python3 generate_icons.py

# Generate favicon.ico with multiple sizes
magick nba-comeback-dashboard-basketball.svg \
  -background none \
  -define icon:auto-resize=16,32,48 \
  favicon.ico

echo "Generated favicon.ico with multiple sizes"

# Create site.webmanifest file
cat > site.webmanifest << EOF
{
  "name": "NBA Comeback Dashboard",
  "short_name": "NBA Comeback",
  "icons": [
    {
      "src": "/web-app-manifest-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/web-app-manifest-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "theme_color": "#ffffff",
  "background_color": "#ffffff",
  "display": "standalone"
}
EOF

echo "Created site.webmanifest"
echo "Icon generation complete!"