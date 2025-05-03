#!/usr/bin/env python3
# Script to generate various icon sizes needed for web apps using Pillow

from PIL import Image
import os

def generate_icons(source_image_path, icons_dir):
    """Generate the various icon sizes needed for web apps."""
    # Create directory if it doesn't exist
    os.makedirs(icons_dir, exist_ok=True)
    
    # Open the source image
    img = Image.open(source_image_path)
    
    # Define the sizes for different icons
    sizes = {
        # Android icons
        'android-chrome-192x192.png': (192, 192),
        'android-chrome-512x512.png': (512, 512),
        
        # Apple touch icons
        'apple-touch-icon.png': (180, 180),
        'apple-touch-icon-152x152.png': (152, 152),
        'apple-touch-icon-144x144.png': (144, 144),
        'apple-touch-icon-120x120.png': (120, 120),
        'apple-touch-icon-114x114.png': (114, 114),
        'apple-touch-icon-76x76.png': (76, 76),
        'apple-touch-icon-72x72.png': (72, 72),
        'apple-touch-icon-57x57.png': (57, 57),
        
        # Favicon icons
        'favicon-32x32.png': (32, 32),
        'favicon-16x16.png': (16, 16),
        
        # Microsoft tile icon
        'mstile-144x144.png': (144, 144),
    }
    
    # Generate each icon size
    for icon_name, size in sizes.items():
        resized_img = img.resize(size, Image.LANCZOS)
        resized_img.save(os.path.join(icons_dir, icon_name))
    
    print(f"Generated {len(sizes)} icon files in {icons_dir}")

if __name__ == "__main__":
    source_img = "nbacd_v2.png"
    icons_dir = "icons"
    generate_icons(source_img, icons_dir)