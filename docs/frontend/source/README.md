# App Icons

These placeholder icons need to be properly generated at the correct sizes for optimal display on mobile devices.

## How to Generate Proper Icons

### Method 1: Using the Python Script

1. Install the Pillow library if you don't have it:
   ```
   pip install pillow
   ```

2. Run the provided Python script from the `_static` directory:
   ```
   cd /path/to/_static
   python generate_icons.py
   ```

### Method 2: Using Online Tools

1. Visit a favicon generator website like [RealFaviconGenerator](https://realfavicongenerator.net/)
2. Upload the original `nbacd_v2.png` image
3. Configure settings for Android, iOS, and Windows
4. Download the generated package
5. Replace the files in this directory with the generated ones

## Required Icon Sizes

- android-chrome-192x192.png (192x192)
- android-chrome-512x512.png (512x512)
- apple-touch-icon.png (180x180)
- favicon-32x32.png (32x32)
- favicon-16x16.png (16x16)
- mstile-144x144.png (144x144)

These icons ensure that when users add the site to their home screen on iOS and Android devices, a proper app icon will appear.