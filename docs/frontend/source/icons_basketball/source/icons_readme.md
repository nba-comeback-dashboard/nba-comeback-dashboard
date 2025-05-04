# Icon File Requirements

This document outlines the required icon files for proper cross-browser and cross-device support. All these files should be placed at the root level of the website.

## Required Icon Files

### Browser Favicons
- `favicon.ico` - Multi-size ICO file containing 16×16, 32×32, and 48×48 versions
- `favicon.svg` - Vector version for modern browsers
- `favicon-16x16.png` - 16×16 PNG fallback
- `favicon-32x32.png` - 32×32 PNG fallback 
- `favicon-96x96.png` - 96×96 PNG fallback
- `favicon-196x196.png` - 196×196 PNG for Android Chrome

### iOS Home Screen Icons
- `apple-touch-icon.png` - 180×180 PNG for iPhone 6+
- `apple-touch-icon-57x57.png` - iPhone non-retina
- `apple-touch-icon-60x60.png` - iPhone iOS 7+
- `apple-touch-icon-72x72.png` - iPad non-retina
- `apple-touch-icon-76x76.png` - iPad iOS 7+
- `apple-touch-icon-114x114.png` - iPhone retina
- `apple-touch-icon-120x120.png` - iPhone retina iOS 7+
- `apple-touch-icon-144x144.png` - iPad retina
- `apple-touch-icon-152x152.png` - iPad retina iOS 7+

### Android Home Screen Icons
- `web-app-manifest-192x192.png` - 192×192 PNG for Android Chrome
- `web-app-manifest-512x512.png` - 512×512 PNG for Android Chrome

### Windows Tiles
- `mstile-70x70.png` - Small tile
- `mstile-144x144.png` - Medium tile
- `mstile-150x150.png` - Medium tile
- `mstile-310x150.png` - Wide tile
- `mstile-310x310.png` - Large tile

### Web App Manifest
- `site.webmanifest` - Configures Progressive Web App behavior

## Icon Generation

To generate these icons from the SVG source:

1. Use an online favicon generator service like:
   - [RealFaviconGenerator](https://realfavicongenerator.net/)
   - [Favicon.io](https://favicon.io/favicon-converter/)

2. Upload the SVG file (`nba-comeback-dashboard-basketball.svg`)

3. Download the generated icons and place them in the `/icons` directory

4. During the build process, the icons directory will be copied to the root level of the website

## Icon Usage

All icons are referenced in the HTML template with root paths (e.g., `/favicon.svg`). The required HTML head elements are already configured in the layout.html template.