#!/usr/bin/env python3
"""
Script to convert basketball icon PNG files to have transparent backgrounds.
Uses PyGame which might be more commonly available than Pillow.
"""

import os
import sys
import pygame

def make_transparent(input_path, output_path=None):
    """Convert white background to transparent in a PNG image using PyGame."""
    if output_path is None:
        output_path = input_path
    
    try:
        # Initialize pygame
        pygame.init()
        
        # Load the image
        img = pygame.image.load(input_path)
        
        # Convert to have alpha channel
        img = img.convert_alpha()
        
        # Get the size
        width, height = img.get_size()
        
        # Create a pixel array
        pxarray = pygame.PixelArray(img)
        
        # White color to check against (with some tolerance)
        white = pygame.Color(240, 240, 240)
        
        # Loop through pixels
        for x in range(width):
            for y in range(height):
                pixel = img.get_at((x, y))
                # If pixel is white or very close to white
                if pixel[0] > 240 and pixel[1] > 240 and pixel[2] > 240:
                    # Set fully transparent
                    pxarray[x, y] = (255, 255, 255, 0)
        
        # Delete the pixel array to unlock the surface
        del pxarray
        
        # Save the file
        pygame.image.save(img, output_path)
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
        import pygame
        process_all_icons()
    except ImportError:
        print("Error: PyGame library not found.")