#!/usr/bin/env python3
"""
Generate all required PNG icons from the SVG source for favicons
and Add to Homescreen functionality across all platforms.
"""

import os
import subprocess
from pathlib import Path

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
    'mstile-310x150.png': (310, 150),  # Wide tile
    'mstile-310x310.png': 310,
}

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Path to the SVG source file
    svg_source = script_dir / 'nba-comeback-dashboard-basketball.svg'
    
    if not svg_source.exists():
        print(f"Error: SVG source file not found: {svg_source}")
        return
    
    # Create a icons/tmp directory for temporary files if it doesn't exist
    tmp_dir = script_dir / 'tmp'
    tmp_dir.mkdir(exist_ok=True)
    
    # Generate all the icons
    for filename, size in ICON_SIZES.items():
        output_path = script_dir / filename
        
        if isinstance(size, tuple):
            # Handle rectangular icons (wide tiles)
            width, height = size
            size_str = f"{width}x{height}"
        else:
            # Handle square icons
            size_str = f"{size}x{size}"
        
        # Use ImageMagick's convert to create the PNG
        cmd = [
            'convert',
            '-background', 'none',  # Ensure transparency is preserved
            '-density', '300',      # High density for better quality
            str(svg_source),        # Input SVG
            '-resize', size_str,    # Resize to target dimensions
            str(output_path)        # Output PNG
        ]
        
        print(f"Generating {filename} ({size_str})...")
        try:
            subprocess.run(cmd, check=True)
            print(f"Successfully created {filename}")
        except subprocess.CalledProcessError as e:
            print(f"Error creating {filename}: {e}")
    
    # Remove the temporary directory if it's empty
    try:
        tmp_dir.rmdir()
    except OSError:
        pass
    
    print("\nIcon generation complete!")

if __name__ == "__main__":
    main()