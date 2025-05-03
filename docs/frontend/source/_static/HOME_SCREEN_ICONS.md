# Home Screen Icons Implementation

This document explains how the home screen icons are implemented for the NBA Comeback Dashboard website.

## Overview

When users add the website to their home screen on mobile devices (iOS or Android), they will see a proper app icon instead of a generic screenshot or blank icon.

## Components

The implementation consists of several key components:

1. **Web App Manifest** (`site.webmanifest`): JSON file that tells Android devices how to display the website when added to home screen.

2. **Favicon Icons**: Multiple size icons for browser tabs and bookmarks.

3. **Apple Touch Icons**: Special icons for iOS devices when added to home screen.

4. **Meta Tags**: HTML meta tags in the page template that tell mobile browsers how to handle the website when added to home screen.

## Files and Locations

- `_static/site.webmanifest`: Web app manifest file for Android devices
- `_static/icons/`: Directory containing all icon files:
  - `android-chrome-192x192.png`: Android home screen icon (192x192px)
  - `android-chrome-512x512.png`: Android home screen icon (512x512px)
  - `apple-touch-icon.png`: iOS home screen icon (180x180px)
  - `favicon-32x32.png`: Favicon for browsers (32x32px)
  - `favicon-16x16.png`: Favicon for browsers (16x16px)
  - `mstile-144x144.png`: Microsoft tile icon (144x144px)
- `_templates/layout.html`: Custom Sphinx template that adds the necessary meta tags and links

## Implementation Details

### HTML Meta Tags (in `_templates/layout.html`)

The implementation adds the following meta tags to the HTML head:

```html
<!-- Apple Touch Icons -->
<link rel="apple-touch-icon" sizes="180x180" href="{{ pathto('_static/icons/apple-touch-icon.png', 1) }}">
<link rel="icon" type="image/png" sizes="32x32" href="{{ pathto('_static/icons/favicon-32x32.png', 1) }}">
<link rel="icon" type="image/png" sizes="16x16" href="{{ pathto('_static/icons/favicon-16x16.png', 1) }}">

<!-- Web App Manifest -->
<link rel="manifest" href="{{ pathto('_static/site.webmanifest', 1) }}">

<!-- iOS Meta Tags -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="NBA Comeback Dashboard">

<!-- MS/Windows Meta Tags -->
<meta name="msapplication-TileColor" content="#2b5797">
<meta name="msapplication-TileImage" content="{{ pathto('_static/icons/mstile-144x144.png', 1) }}">
<meta name="theme-color" content="#ffffff">
```

### Web App Manifest (in `site.webmanifest`)

The web app manifest contains information about how the website should behave when added to the home screen:

```json
{
  "name": "NBA Comeback Dashboard",
  "short_name": "NBA Comeback",
  "description": "NBA Comeback statistics and analysis",
  "icons": [
    {
      "src": "_static/icons/android-chrome-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "_static/icons/android-chrome-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "theme_color": "#ffffff",
  "background_color": "#ffffff",
  "display": "standalone",
  "start_url": "/"
}
```

### Sphinx Configuration (in `conf.py`)

The Sphinx configuration is updated to use the favicon and include the manifest file:

```python
# Favicon and web app configuration
html_favicon = "_static/icons/favicon-32x32.png"

# Extra files to copy to output directory
html_extra_path = ["_static/site.webmanifest"]
```

## Testing

To test the home screen icons:

1. **On iOS**:
   - Visit the website in Safari
   - Tap the Share button (box with arrow pointing up)
   - Select "Add to Home Screen"
   - Verify the icon appears correctly on your home screen

2. **On Android**:
   - Visit the website in Chrome
   - Tap the menu button (three dots)
   - Select "Add to Home Screen" or "Install app"
   - Verify the icon appears correctly on your home screen

## Troubleshooting

If icons don't appear correctly:

1. Make sure all icon files are properly generated at the correct sizes
2. Check the browser console for any 404 errors related to icon files
3. Verify that the web app manifest is accessible (no 404 errors)
4. Clear browser cache and try again

## Resources

- [Web App Manifest Specification](https://w3c.github.io/manifest/)
- [Apple Web App Documentation](https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html)
- [Google Progressive Web Apps](https://web.dev/progressive-web-apps/)