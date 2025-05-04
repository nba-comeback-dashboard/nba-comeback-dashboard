#!/usr/bin/env python3
"""
Generate PNG icons from SVG using cairosvg, which has better stroke rendering.
"""

import os
import sys
from pathlib import Path

try:
    import cairosvg
except ImportError:
    print("CairoSVG not installed. Attempting to install...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "cairosvg", "--user"])
        import cairosvg
        print("CairoSVG installed successfully!")
    except:
        print("Error installing CairoSVG. Please install it manually:")
        print("pip install cairosvg --user")
        sys.exit(1)

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
    
    # Path to the SVG source file - using the fixed SVG with explicit stroke attributes
    svg_source = script_dir / 'nba-comeback-dashboard-percent-fixed.svg'
    
    if not svg_source.exists():
        print(f"Error: SVG source file not found: {svg_source}")
        return
    
    # Read the SVG content
    with open(svg_source, 'r') as f:
        svg_content = f.read()
    
    # Generate square icons
    for filename, size in ICON_SIZES.items():
        output_path = script_dir / filename
        print(f"Generating {filename} ({size}x{size})...")
        cairosvg.svg2png(bytestring=svg_content, 
                        write_to=str(output_path), 
                        output_width=size, 
                        output_height=size,
                        dpi=300)
        print(f"Successfully created {filename}")
    
    # Generate rectangular icons
    for filename, (width, height) in RECTANGULAR_ICONS.items():
        output_path = script_dir / filename
        print(f"Generating {filename} ({width}x{height})...")
        cairosvg.svg2png(bytestring=svg_content, 
                        write_to=str(output_path), 
                        output_width=width, 
                        output_height=height,
                        dpi=300)
        print(f"Successfully created {filename}")
    
    print("\nIcon generation complete!")

if __name__ == "__main__":
    main()