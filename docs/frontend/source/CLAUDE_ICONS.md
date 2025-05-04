# Icon Switching System

This documentation describes how to switch between different icon sets for the NBA Comeback Dashboard.

## Available Icon Sets

The project currently has two icon sets:

1. **Basketball Icon Set** (`icons_basketball/`)
   - Features a basketball design
   - Main icon: `nba-comeback-dashboard-basketball.svg`

2. **Percent Icon Set** (`icons_percent/`)
   - Features a percentage symbol design
   - Main icon: `nba-comeback-dashboard-basketball.svg` (contains percent design)

## How to Switch Icon Sets

To switch between icon sets, you need to update two settings in `conf.py`:

1. Change the logo reference in `html_theme_options`:
   ```python
   "logo": {
       "text": "NBA Comeback Dashboard",
       "image_light": "/nba-comeback-dashboard-basketball.svg",  # Change to desired icon
   },
   ```

2. Change the favicon and extra path references:
   ```python
   # Favicon and web app configuration
   html_favicon = "icons_percent/nba-comeback-dashboard-basketball.svg"  # Change to desired icon
   
   # Extra files to copy to output directory
   html_extra_path = ["icons_percent"]  # Change to desired directory
   ```

Simply change both references to point to the desired icon set directory (`icons_basketball` or `icons_percent`).

## Generating Icons

Each icon set directory includes scripts to generate all required icon sizes from the SVG source:

```bash
cd /path/to/icon/directory
./generate_icons.sh
```

This script generates:
- Multiple favicon sizes
- iOS home screen icons
- Android home screen icons
- Windows tiles
- Web app manifest

## Requirements

The icon generation script requires:
- ImageMagick (for the `convert` command)
- Bash shell

## Icon Files Generated

Running the generation script creates:
- favicon.ico (containing 16×16, 32×32, and 48×48 sizes)
- Multiple PNG favicons (16x16, 32x32, 96x96, 196x196)
- iOS touch icons (57x57 to 180x180)
- Android home screen icons (192x192, 512x512)
- Windows tiles (70x70 to 310x310)
- site.webmanifest for Progressive Web App configuration