# Epicycle Animation

Turn any SVG drawing into a mesmerizing Fourier epicycle animation! Watch as spinning circles magically trace out your artwork.

## What is this?

This program takes any drawing (as an SVG file) and recreates it using spinning circles (called epicycles). Each circle rotates at a different speed, and when you stack them together, they draw your image perfectly. It's the magic of Fourier transforms in action!

## Features

- Works with any SVG drawing
- Automatically optimizes the number of epicycles needed
- High-quality 1080p video output
- Customizable colors and parameters

## Installation

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Install system dependencies:

**macOS:**
```bash
brew install py3cairo ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install build-essential python3-dev libcairo2-dev libpango1.0-dev ffmpeg
```

**Windows:**
Follow the [Manim installation guide](https://docs.manim.community/en/stable/installation/windows.html)

## Usage

Run with the included test heart:
```bash
python epicycles.py
```

Use your own SVG:
```bash
python epicycles.py path/to/your_drawing.svg
```

Or edit `INPUT_SVG` in `epicycles.py` (line 18).

The output video will be saved in `media/output.mp4`.

## Creating SVG Files

Use free tools like [Inkscape](https://inkscape.org/) or [Boxy SVG](https://boxy-svg.com/).

**Tips:**
- Use simple line drawings
- Single continuous paths work best
- Keep it under 1000-2000 points for reasonable render times

**Converting shapes to paths in Inkscape:**
1. Select all (Ctrl+A)
2. Path → Object to Path
3. Save as "Plain SVG"

## Customization

Edit the `CONFIG` dictionary in `epicycles.py`:

```python
CONFIG = {
    "draw_time": 20,              # Time to draw once (seconds)
    "duration": 40,               # Total video length (seconds)
    "energy_threshold": 0.999,    # Quality (higher = more accurate)
    "background_color": "#0a0a0a",
    "circle_color": "#3498db",
    "trace_color": "#ecf0f1",
    "pen_color": "#e74c3c",
    "scale_factor": 8.0,          # Adjust size
}
```

## How It Works

Uses the **Fourier Transform** to break down any shape into a combination of spinning circles:
1. SVG → series of points
2. Fourier Transform finds the perfect combination of rotating circles
3. Each circle has a specific size and rotation speed
4. When stacked together, they draw your shape!

Learn more: [3Blue1Brown's Fourier Series video](https://www.youtube.com/watch?v=r6sGWTCMz2k)

## Credits

Inspired by [3Blue1Brown](https://www.youtube.com/watch?v=r6sGWTCMz2k) and built with [Manim Community](https://www.manim.community/)

## License

MIT License
