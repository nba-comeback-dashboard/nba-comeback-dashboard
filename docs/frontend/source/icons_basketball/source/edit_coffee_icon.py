#!/usr/bin/env python3
"""
Simple script to edit the buy-me-coffee.svg icon to remove the bottom line 
and update the viewBox for better alignment.
"""

def edit_coffee_icon():
    input_file = "_static/icons/buy-me-coffee.svg"
    output_file = "_static/icons/buy-me-coffee.svg"
    
    # Read the original SVG
    with open(input_file, 'r') as file:
        svg_content = file.read()
    
    # Remove the bottom line by modifying the path
    # The "M4 19h16v2H4z" part is the bottom line
    svg_content = svg_content.replace(
        '<path d="M20 3H4v10c0 2.21 1.79 4 4 4h6c2.21 0 4-1.79 4-4v-3h2c1.11 0 2-.9 2-2V5c0-1.11-.89-2-2-2zm0 5h-2V5h2v3zM4 19h16v2H4z"/>',
        '<path d="M20 3H4v10c0 2.21 1.79 4 4 4h6c2.21 0 4-1.79 4-4v-3h2c1.11 0 2-.9 2-2V5c0-1.11-.89-2-2-2zm0 5h-2V5h2v3z"/>'
    )
    
    # Adjust the viewBox for better alignment
    svg_content = svg_content.replace(
        'viewBox="0 0 24 24"',
        'viewBox="0 0 24 22"'  # Reduce height from 24 to 22
    )
    
    # Write the modified SVG
    with open(output_file, 'w') as file:
        file.write(svg_content)
    
    print(f"Successfully edited {input_file}")

if __name__ == "__main__":
    edit_coffee_icon()