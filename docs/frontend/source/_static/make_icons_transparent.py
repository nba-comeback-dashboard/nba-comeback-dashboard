#!/usr/bin/env python3
"""
Script to convert the basketball icon PNG files to have transparent backgrounds.
Requires Pillow (PIL) library.
"""

import os
from PIL import Image

def make_transparent(input_path, output_path=None):
    """Convert white background to transparent in a PNG image."""
    if output_path is None:
        output_path = input_path
    
    try:
        # Open the image
        img = Image.open(input_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Get the data
        data = img.getdata()
        
        # Create a new data list with the same colors but with white pixels made transparent
        new_data = []
        for item in data:
            # Check if the pixel is white (or very close to white)
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                # Replace with a transparent pixel
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        
        # Update the image with the new data
        img.putdata(new_data)
        
        # Save the new image
        img.save(output_path, 'PNG')
        print(f"Successfully made {input_path} transparent.")
        
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def process_all_icons():
    """Process all icon files in the project."""
    # Main logo images
    make_transparent('_static/nbacd_v2.png')
    make_transparent('_static/nbacd_v2_small.png')
    
    # Icon directory files
    icon_dir = '_static/icons/'
    for filename in os.listdir(icon_dir):
        if filename.endswith('.png'):
            filepath = os.path.join(icon_dir, filename)
            make_transparent(filepath)

if __name__ == "__main__":
    try:
        from PIL import Image
        process_all_icons()
    except ImportError:
        print("Error: Pillow library not found. Please install it with 'pip install Pillow'")