#!/usr/bin/env python3
"""
Generate all required PNG icons from the SVG source for favicons
and Add to Homescreen functionality across all platforms.
Uses Python's PIL library instead of ImageMagick.
"""

import os
import sys
from pathlib import Path
from PIL import Image
import cairosvg  # You might need to install this with: pip install cairosvg

# Define all the icon sizes we need to generate
ICON_SIZES = {
    # Favicons
    'favicon-16x16.png': 16,
    'favicon-32x32.png': 32, 
    'favicon-96x96.png': 96,
    'favicon-196x196.png': 196,
    
    # iOS icons
    'apple-touch-icon-57x57.png': 57,
    'apple-touch-icon-60x60.png': 60,
    'apple-touch-icon-72x72.png': 72,
    'apple-touch-icon-76x76.png': 76,
    'apple-touch-icon-114x114.png': 114,
    'apple-touch-icon-120x120.png': 120,
    'apple-touch-icon-144x144.png': 144,
    'apple-touch-icon-152x152.png': 152,
    'apple-touch-icon.png': 180,  # The default 180x180 icon
    
    # Android icons
    'web-app-manifest-192x192.png': 192,
    'web-app-manifest-512x512.png': 512,
    
    # Windows tiles
    'mstile-70x70.png': 70,
    'mstile-144x144.png': 144,  # Duplicate of apple-touch-icon-144x144 but with different name
    'mstile-150x150.png': 150,
    'mstile-310x310.png': 310,
}

# Add wide tile separately
RECTANGULAR_ICONS = {
    'mstile-310x150.png': (310, 150),  # Wide tile
}

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Path to the SVG source file - using the percent icon
    svg_source = script_dir / 'nba-comeback-dashboard-basketball.svg'
    
    if not svg_source.exists():
        print(f"Error: SVG source file not found: {svg_source}")
        return
    
    # Create tmp directory if it doesn't exist
    tmp_dir = script_dir / 'tmp'
    tmp_dir.mkdir(exist_ok=True)
    
    # First convert the SVG to a large PNG to use as source
    temp_png = tmp_dir / 'temp_large.png'
    cairosvg.svg2png(url=str(svg_source), write_to=str(temp_png), output_width=1024, output_height=1024)
    
    # Generate square icons
    source_img = Image.open(temp_png)
    for filename, size in ICON_SIZES.items():
        output_path = script_dir / filename
        img_resized = source_img.resize((size, size), Image.LANCZOS)
        img_resized.save(output_path)
        print(f"Successfully created {filename}")
    
    # Generate rectangular icons
    for filename, (width, height) in RECTANGULAR_ICONS.items():
        output_path = script_dir / filename
        img_resized = source_img.resize((width, height), Image.LANCZOS)
        img_resized.save(output_path)
        print(f"Successfully created {filename}")
    
    # Create site.webmanifest file
    webmanifest_path = script_dir / 'site.webmanifest'
    with open(webmanifest_path, 'w') as f:
        f.write('''{
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
}''')
    print("Created site.webmanifest")
    
    # Try to remove the temp directory and files
    try:
        os.remove(temp_png)
        tmp_dir.rmdir()
    except OSError:
        pass
    
    print("\nIcon generation complete!")

if __name__ == "__main__":
    main()