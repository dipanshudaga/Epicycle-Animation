# Fourier Epicycle Drawing 🎨✨

Turn any SVG drawing into a mesmerizing Fourier epicycle animation! Watch as circles spin and magically trace out your artwork.

![Demo Animation](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Manim](https://img.shields.io/badge/Manim-Community-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## What is this?

Remember those old spirograph toys? This is like that, but powered by math! The program takes any drawing (as an SVG file) and recreates it using spinning circles (called epicycles). Each circle rotates at a different speed, and when you stack them together, they draw your image perfectly. It's beautiful, hypnotic, and shows the magic of Fourier transforms in action!

## Features

- **Works with any SVG** - Doodles, logos, maps, portraits - if you can draw it, we can animate it
- **Smart optimization** - Automatically figures out how many circles you need
- **Beautiful output** - High-quality 1080p video at 30fps
- **Easy to use** - Just one command and you're done
- **Customizable** - Change colors, speed, and quality to your liking

## Quick Start

### 1. Install Dependencies

First, make sure you have Python 3.8 or higher. Then install the Python packages:

```bash
pip install -r requirements.txt
```

### 2. Install System Dependencies

Manim needs a few system tools to work properly:

**macOS:**
```bash
brew install py3cairo ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install build-essential python3-dev libcairo2-dev libpango1.0-dev ffmpeg
```

**Windows:**
Follow the [official Manim installation guide](https://docs.manim.community/en/stable/installation/windows.html)

### 3. Run It!

Try it with the included test heart:

```bash
python epicycles.py
```

That's it! Your video will be saved in `media/output.mp4`.

## Using Your Own Drawing

### Option 1: Edit the script (recommended)

Open `epicycles.py` and change line 18:

```python
INPUT_SVG = "your_drawing.svg"  # Change this to your file
```

Then run:
```bash
python epicycles.py
```

### Option 2: Command line

```bash
python epicycles.py path/to/your_drawing.svg
```

## Creating SVG Files

You can create SVG files using free tools like [Inkscape](https://inkscape.org/) or online at [Boxy SVG](https://boxy-svg.com/).

### Tips for best results:

1. **Use simple line drawings** - Outlines work better than filled shapes
2. **Single path is best** - The script can handle multiple paths, but one continuous line is ideal
3. **Not too complex** - Keep it under 1000-2000 points for reasonable render times

### Converting shapes to paths in Inkscape:

If your SVG has shapes (rectangles, circles) instead of paths:

1. Open your SVG in Inkscape
2. Select all (Ctrl+A or Cmd+A)
3. Go to Path → Object to Path
4. Save as "Plain SVG"

## Customization

Want to change how it looks? Edit the `CONFIG` dictionary in `epicycles.py`:

```python
CONFIG = {
    # How long the animation is
    "draw_time": 20,        # Time to draw once (seconds)
    "duration": 40,         # Total video length (seconds)
    "fps": 30,              # Frames per second

    # Quality (higher = more accurate but slower)
    "energy_threshold": 0.999,    # Use 99.9% of the "energy"
    "min_epicycles": 100,         # Minimum circles
    "max_epicycles": 2000,        # Maximum circles

    # Colors (use any hex color code)
    "background_color": "#0a0a0a",  # Dark background
    "circle_color": "#3498db",       # Blue spinning circles
    "trace_color": "#ecf0f1",        # White/light gray trace
    "pen_color": "#e74c3c",          # Red pen dot

    # Size
    "scale_factor": 8.0,    # Adjust if drawing appears too big/small
}
```

## How Long Will It Take?

Rendering time depends on complexity:

- **Simple drawings (50-100 circles)**: 5-10 minutes
- **Medium drawings (100-200 circles)**: 10-20 minutes
- **Complex drawings (200-500 circles)**: 20-60 minutes
- **Very complex (500+ circles)**: 1-3 hours

Your computer's speed matters too! Manim renders using a single CPU core, so be patient with complex drawings.

## Troubleshooting

### "No module named 'manim'"
```bash
pip install manim
```

### "cairo library not found"
You need to install the system dependencies (see Step 2 above).

### Drawing is too big/small
Change the `scale_factor` in CONFIG. Try values between 3.0 and 12.0.

### Drawing looks wrong or upside down
The script should handle this automatically, but if it doesn't:
- Open your SVG in Inkscape
- Save as "Plain SVG" (not Inkscape SVG)
- Try again

### Want better quality?
Increase the `energy_threshold` to 0.9999 (but this will use more circles and take longer to render).

### Want faster renders?
Decrease `max_epicycles` to 500 or lower.

## How Does It Work?

This project uses the **Fourier Transform** - a mathematical technique that breaks down any shape into a combination of spinning circles. Here's the magic:

1. Your SVG is converted into a series of points
2. The Fourier Transform finds the perfect combination of rotating circles
3. Each circle has a specific size and rotation speed
4. When you stack them all together, they draw your shape!

If you want to understand the math, check out [3Blue1Brown's amazing video](https://www.youtube.com/watch?v=r6sGWTCMz2k) on the topic.

## Examples

The project comes with `test_heart.svg` to get you started. Try creating epicycles for:
- Your signature
- A national flag or map
- Your favorite logo
- A simple portrait
- Mathematical symbols

## Technical Details

- **Language**: Python 3.8+
- **Animation**: Manim Community Edition
- **Math**: NumPy FFT (Fast Fourier Transform)
- **SVG Parsing**: svgpathtools
- **Output**: H.264 video (MP4)

## Contributing

Found a bug? Have an idea? Feel free to open an issue or submit a pull request!

## Credits & Inspiration

This project was inspired by:
- [3Blue1Brown's Fourier Series video](https://www.youtube.com/watch?v=r6sGWTCMz2k)
- [Mathologer's epicycle animations](https://www.youtube.com/watch?v=qS4H6PEcCCA)
- The amazing [Manim Community](https://www.manim.community/)

## License

MIT License - Feel free to use, modify, and share!

---

**Have fun creating mathematical art!** If you make something cool, I'd love to see it! 🎨

