#!/usr/bin/env python3
"""
Create the most essential icons for the site using Python's PIL library.
This script creates a smaller set of icons to ensure basic functionality.
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image
    import cairosvg
except ImportError:
    print("Required libraries not found. Install them with:")
    print("pip install pillow cairosvg")
    sys.exit(1)

# Define the essential icon sizes
ESSENTIAL_ICONS = {
    # Basic favicons
    'favicon-16x16.png': (16, 16),
    'favicon-32x32.png': (32, 32),
    'favicon-96x96.png': (96, 96),
    
    # iOS home screen
    'apple-touch-icon.png': (180, 180),
    
    # Android home screen
    'web-app-manifest-192x192.png': (192, 192),
    'web-app-manifest-512x512.png': (512, 512),
}

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Path to the SVG source file
    svg_source = script_dir / 'nba-comeback-dashboard-basketball.svg'
    
    if not svg_source.exists():
        print(f"Error: SVG source file not found: {svg_source}")
        return
    
    print(f"Creating PNG icons from {svg_source}...")
    
    # Create a temporary PNG at a high resolution first
    temp_png = script_dir / 'temp_icon.png'
    cairosvg.svg2png(url=str(svg_source), write_to=str(temp_png), output_width=1024, output_height=1024)
    
    # Open the temporary file
    img = Image.open(temp_png)
    
    # Generate the essential icons
    for filename, size in ESSENTIAL_ICONS.items():
        output_path = script_dir / filename
        print(f"Creating {filename} ({size[0]}x{size[1]})...")
        
        # Resize the image
        resized = img.resize(size, Image.LANCZOS)
        
        # Save the resized image
        resized.save(output_path)
        print(f"Saved {output_path}")
    
    # Clean up the temporary file
    temp_png.unlink()
    
    print("\nIcon generation complete!")

if __name__ == "__main__":
    main()