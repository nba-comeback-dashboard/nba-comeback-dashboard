# Configuration Notes

- The `conf.py` file has been updated to include all CSS and JavaScript dependencies needed to match the `test_pages/test_dashboard.html` configuration.
- CSS files now include additional files for dashboard functionality and Bootstrap.
- JavaScript files are loaded in proper dependency order:
  1. External dependencies (Chart.js, Bootstrap, etc.)
  2. Base utilities (nbacd_utils.js, etc.)
  3. Numerical functions
  4. Core modules
  5. Dashboard modules
  6. UI module

## Theme Configuration Notes

- Dark mode is intentionally disabled due to significant rendering issues with plots, charts, and tables in dark mode
- Attempting to enable dark mode requires extensive CSS overrides to properly style all dashboard components
- If dark mode is needed in the future, a comprehensive testing and styling effort will be required that addresses:
  1. Chart backgrounds and grid colors
  2. Table formatting
  3. Interactive elements
  4. Data visualization color schemes

## Icon Configuration

- Icons are placed in the `/icons` directory and will be copied to the site root during build
- The site uses a combination of SVG and PNG icons for maximum compatibility:
  - SVG favicon for modern browsers (`favicon.svg`)
  - Traditional ICO favicon (`favicon.ico`)
  - PNG favicon fallback (`favicon-96x96.png`)
  - iOS home screen icon (`apple-touch-icon.png` - 180×180px)
  - Android/PWA home screen icons (`web-app-manifest-192x192.png` and `web-app-manifest-512x512.png`)
  - Web app manifest file (`site.webmanifest`) configures Progressive Web App behavior
- All icon paths in HTML reference the root level (e.g., `/favicon.svg` not `_static/icons/favicon.svg`)
- During build, the `/icons` directory is added to `html_extra_path` in `conf.py`

## Font Configuration Options

Four font options are available for the documentation:

### Font Choice #1: Original PyData Theme
- Sans-serif headers and body text (Lato/system-ui)
- Standard PyData Sphinx Theme typography
- Located in `_static/css/font_choice_1.css` and `_static/css/toc_entry_font_choice_1.css`
- To enable: Edit `conf.py` to comment out other font choices and uncomment both Font Choice #1 files

### Font Choice #2: Charter/Georgia Serif 
- Serif fonts for all text elements
- More bookish, traditional documentation style
- Located in `_static/css/font_choice_2.css` and `_static/css/toc_entry_font_choice_2.css`
- To enable: Edit `conf.py` to comment out other font choices and uncomment both Font Choice #2 files

### Font Choice #3: Hybrid Style (Baskerville/Sans-serif)
- Elegant Baskerville serif headings with sans-serif body text
- Combines modern readability with traditional heading style
- Located in `_static/css/font_choice_3.css` and `_static/css/toc_entry_font_choice_3.css`
- To enable: Edit `conf.py` to comment out other font choices and uncomment both Font Choice #3 files

### Font Choice #4: Baskerville Headers with Charter Body
- Baskerville headers (elegant serif from Choice #3 but with adjusted sizing)
- Charter/Georgia body text (traditional serif from Choice #2)
- Combines the most elegant aspects of both serif font choices
- Located in `_static/css/font_choice_4.css` and `_static/css/toc_entry_font_choice_4.css`
- To enable: Edit `conf.py` to comment out other font choices and uncomment both Font Choice #4 files

Note: The navigation bar logo text always remains in the PyData default font for brand consistency, controlled by `custom_logo.css`.

# Claude Code Documentation Guide

## Purpose
Document the experience of using Claude Code to develop the NBA Comeback Dashboard website. This will serve as a case study for AI-assisted development in a real-world project.

## Content in using_claude_code.rst
The documentation in `/docs/frontend/source/analysis/using_claude_code.rst` includes:

1. Introduction and choice of Claude Code vs other tools
   - Comparison with Cursor and other AI coding tools
   - Links to independent evaluations

2. Key Lessons Learned
   - Ask for small features, one at a time
   - Python-to-JavaScript translation strategy
   - Don't throw good money after bad (when to restart)
   - Rigorous testing is essential

3. Technical Implementation Challenges
   - Numeric optimization in JavaScript
   - Subtle logic bugs in translation
   - URL encoding and state management

4. Best Practices for AI-Assisted Development
   - Seven key recommendations based on experience

5. Links to relevant project resources
   - GitHub repository
   - Cross-references to other documentation pages

## Key Points Highlighted
1. Breaking development into small, well-defined tasks with commit-first approach
2. Using Python-to-JavaScript translation for complex calculations
3. Recognizing when to step back and restart rather than repeatedly asking for fixes
4. The importance of proper testing in the correct environment

## Python to JavaScript Translation
The documentation covers the translation of four key Python modules to JavaScript:
- form_nba_chart_json_data_api.py → nbacd_dashboard_api.js
- form_nba_chart_json_data_num.py → nbacd_dashboard_num.js
- form_nba_chart_json_data_plot_primitives.py → nbacd_dashboard_plot_primitives.js
- form_nba_chart_json_data_season_game_loader.py → nbacd_dashboard_season_game_loader.js

## Documentation Style Guidelines
1. Always use `.. list-table::` format for tables rather than other table formats
2. Follow the existing header style with over/under line patterns
3. Use `.. code::` for code blocks
4. Use `.. pull-quote::` for quotations
5. Use cross-references to other pages with `:doc:` directives

## Custom Typography and Fonts
We've implemented custom font styling to match the TOC entries style across all documentation:

- Added `custom_fonts.css` which overrides default heading styles with Charter/Georgia serif fonts
- Font styles are configured to match the toc-entry directive's appearance for consistency
- Default theme fonts are commented out in the CSS file for easy restoration if needed
- To revert to the original theme fonts:
  1. Edit `conf.py` to remove or comment out the "css/custom_fonts.css" line
  2. Or edit `_static/css/custom_fonts.css` to uncomment the original styles and comment out the new ones

The custom TOC entry directive is styled to use Charter/Georgia fonts with specific sizes:
- Title: 22px
- Subtitle: 15px
- Date: 11px

Regular documentation text styling:
- Body text: 17px (increased from standard 15px for better readability)
- Lists, definition lists, and other text elements: 17px
- Line height: 1.3 for comfortable reading spacing
- All text maintains the Charter/Georgia font family for consistency