#!/usr/bin/env python3
"""
Fourier Epicycle Animation Generator
Clean version with auto-detection and smart limits
"""

import numpy as np
from manim import *
from svgpathtools import svg2paths
import sys
import shutil
import os

# ============================================================================
# INPUT/OUTPUT
# ============================================================================

INPUT_SVG = "test_heart.svg"
OUTPUT_VIDEO = "media/output.mp4"

# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG = {
    # Timing
    "draw_time": 20,
    "duration": 40,
    "fps": 30,

    # Quality
    "animation_steps": 2000,
    "samples_per_path": 5000,
    "energy_threshold": 0.999,       # 99.9% energy (very high)
    "min_epicycles": 100,            # Safety minimum
    "max_epicycles": 2000,           # Safety maximum

    # Visual
    "resolution": (1080, 1920),
    "background_color": "#0a0a0a",
    "circle_color": "#3498db",
    "circle_opacity": 0.8,
    "circle_stroke_width": 1.8,
    "vector_color": "#2ecc71",
    "vector_opacity": 0.8,
    "vector_stroke_width": 1.8,
    "trace_color": "#ecf0f1",
    "trace_stroke_width": 2.5,
    "pen_color": "#e74c3c",
    "pen_size": 0.04,
    "scale_factor": 8.0,
}


# ============================================================================
# SVG PROCESSING
# ============================================================================

def load_and_process_svg(filepath):
    """Load and process SVG."""
    paths, _ = svg2paths(filepath)
    
    all_contours = []
    for path in paths:
        path_length = path.length()
        points = []
        
        for i in range(CONFIG['samples_per_path']):
            arc_length = (i / CONFIG['samples_per_path']) * path_length
            try:
                t = path.ilength(arc_length, error=1e-6, max_iterations=50)
            except:
                t = i / CONFIG['samples_per_path']
            
            point = path.point(t)
            points.append([point.real, -point.imag])
        
        all_contours.append(np.array(points))
    
    if len(all_contours) == 1:
        ordered_points = all_contours[0]
    else:
        ordered_points = connect_contours_tsp(all_contours)
    
    # Close path if needed
    if np.linalg.norm(ordered_points[0] - ordered_points[-1]) > 1e-6:
        ordered_points = np.vstack([ordered_points, ordered_points[0:1]])
    
    # Center and normalize
    center = np.mean(ordered_points, axis=0)
    ordered_points = ordered_points - center
    max_extent = np.max(np.abs(ordered_points))
    if max_extent > 0:
        ordered_points = ordered_points / max_extent * CONFIG['scale_factor']
    
    return ordered_points


def connect_contours_tsp(contours):
    """Connect multiple contours using greedy TSP."""
    ordered = []
    current_pos = contours[0][0]
    remaining = list(contours)
    
    while remaining:
        best_contour = None
        best_dist = float('inf')
        should_reverse = False
        
        for contour in remaining:
            dist_start = np.linalg.norm(current_pos - contour[0])
            if dist_start < best_dist:
                best_dist = dist_start
                best_contour = contour
                should_reverse = False
            
            dist_end = np.linalg.norm(current_pos - contour[-1])
            if dist_end < best_dist:
                best_dist = dist_end
                best_contour = contour
                should_reverse = True
        
        if should_reverse:
            best_contour = best_contour[::-1]
        ordered.append(best_contour)
        current_pos = best_contour[-1]
        remaining = [c for c in remaining if not np.array_equal(c, best_contour) and not np.array_equal(c, best_contour[::-1])]
    
    return np.concatenate(ordered)


# ============================================================================
# FOURIER ANALYSIS
# ============================================================================

def compute_fourier_coefficients(points):
    """Compute DFT coefficients."""
    N = len(points)
    z = points[:, 0] + 1j * points[:, 1]
    
    fft_result = np.fft.fft(z) / N
    frequencies = np.fft.fftfreq(N, d=1.0/N).astype(int)
    
    coefficients = {freq: coeff for freq, coeff in zip(frequencies, fft_result)}
    return coefficients


def find_optimal_epicycles(coefficients):
    """Find optimal number of epicycles with limits."""
    sorted_items = sorted(coefficients.items(), key=lambda x: abs(x[1]), reverse=True)
    
    # Calculate energies
    total_energy = sum(abs(c)**2 for _, c in sorted_items)
    cumulative_energy = 0
    optimal_count = 0
    
    # Find where we hit energy threshold
    for i, (freq, coeff) in enumerate(sorted_items, 1):
        cumulative_energy += abs(coeff)**2
        energy_ratio = cumulative_energy / total_energy
        
        if energy_ratio >= CONFIG['energy_threshold']:
            optimal_count = i
            break
    
    # If threshold never reached, use all
    if optimal_count == 0:
        optimal_count = len(sorted_items)
    
    # Apply min/max limits
    optimal_count = max(CONFIG['min_epicycles'], min(optimal_count, CONFIG['max_epicycles']))
    
    # Calculate final energy
    final_energy = sum(abs(sorted_items[i][1])**2 for i in range(optimal_count))
    final_ratio = final_energy / total_energy
    
    return optimal_count, sorted_items[:optimal_count], final_ratio


# ============================================================================
# ANIMATION PRE-COMPUTATION
# ============================================================================

def precompute_animation(coefficients, num_steps):
    """Pre-compute animation states."""
    path_points = []
    epicycle_states = []
    
    for step in range(num_steps):
        t = step / num_steps
        
        z = complex(0, 0)
        for freq, coeff in coefficients:
            z += coeff * np.exp(2j * np.pi * freq * t)
        path_points.append(np.array([z.real, z.imag, 0]))
        
        circles = []
        vectors = []
        current_z = complex(0, 0)
        prev_pos = np.array([0, 0, 0])
        
        for freq, coeff in coefficients:
            radius = abs(coeff)
            
            circles.append({
                'center': prev_pos.copy(),
                'radius': radius
            })
            
            next_z = current_z + coeff * np.exp(2j * np.pi * freq * t)
            next_pos = np.array([next_z.real, next_z.imag, 0])
            
            vectors.append({
                'start': prev_pos.copy(),
                'end': next_pos.copy()
            })
            
            current_z = next_z
            prev_pos = next_pos
        
        epicycle_states.append({'circles': circles, 'vectors': vectors})
    
    return np.array(path_points), epicycle_states


# ============================================================================
# MANIM SCENE
# ============================================================================

class EpicycleAnimation(Scene):
    def __init__(self, path_points, epicycle_states, **kwargs):
        self.path_points = path_points
        self.epicycle_states = epicycle_states
        self.num_steps = len(path_points)
        super().__init__(**kwargs)
    
    def construct(self):
        self.camera.background_color = CONFIG['background_color']
        
        num_loops = int(np.ceil(CONFIG['duration'] / CONFIG['draw_time']))
        
        pen = Dot(color=CONFIG['pen_color'], radius=CONFIG['pen_size'])
        pen.move_to(self.path_points[0])
        
        trace = TracedPath(
            pen.get_center,
            stroke_width=CONFIG['trace_stroke_width'],
            stroke_color=CONFIG['trace_color'],
            dissipating_time=None
        )
        
        epicycles = VGroup()
        self.add(trace, epicycles, pen)
        
        for loop_num in range(num_loops):
            remaining_time = CONFIG['duration'] - (loop_num * CONFIG['draw_time'])
            this_loop_duration = min(CONFIG['draw_time'], remaining_time)
            
            if this_loop_duration <= 0:
                break
            
            def update_animation(mob, alpha):
                step_idx = int(alpha * (self.num_steps - 1))
                pen.move_to(self.path_points[step_idx])
                state = self.epicycle_states[step_idx]
                epicycles.become(self.create_epicycles_from_state(state))
            
            self.play(
                UpdateFromAlphaFunc(epicycles, update_animation),
                run_time=this_loop_duration,
                rate_func=linear
            )
    
    def create_epicycles_from_state(self, state):
        circles = VGroup()
        vectors = VGroup()
        
        for circle_data in state['circles']:
            circle = Circle(
                radius=circle_data['radius'],
                stroke_color=CONFIG['circle_color'],
                stroke_width=CONFIG['circle_stroke_width'],
                stroke_opacity=CONFIG['circle_opacity'],
                fill_opacity=0
            )
            circle.move_to(circle_data['center'])
            circles.add(circle)
        
        for vector_data in state['vectors']:
            vector = Line(
                vector_data['start'],
                vector_data['end'],
                stroke_color=CONFIG['vector_color'],
                stroke_width=CONFIG['vector_stroke_width'],
                stroke_opacity=CONFIG['vector_opacity']
            )
            vectors.add(vector)
        
        return VGroup(circles, vectors)


# ============================================================================
# MAIN
# ============================================================================

def main():
    svg_filepath = sys.argv[1] if len(sys.argv) >= 2 else INPUT_SVG
    
    print("━" * 60)
    print("  EPICYCLE ANIMATION")
    print("━" * 60)
    
    # Process SVG
    print(f"\n✓ Input: {svg_filepath}")
    points = load_and_process_svg(svg_filepath)
    print(f"✓ Sampled: {len(points)} points")
    
    # Compute Fourier
    coefficients = compute_fourier_coefficients(points)
    
    # Find optimal epicycles
    num_epicycles, optimal_coeffs, energy = find_optimal_epicycles(coefficients)
    print(f"✓ Epicycles: {num_epicycles} circles ({energy*100:.1f}% energy)")
    
    # Pre-compute animation
    print(f"✓ Pre-computing animation...")
    path_points, epicycle_states = precompute_animation(optimal_coeffs, CONFIG['animation_steps'])
    
    # Render
    print(f"✓ Rendering {CONFIG['draw_time']}s @ {CONFIG['fps']}fps...")
    
    config.pixel_width = CONFIG['resolution'][0]
    config.pixel_height = CONFIG['resolution'][1]
    config.frame_rate = CONFIG['fps']
    config.background_color = CONFIG['background_color']
    config.verbosity = "WARNING"
    
    scene = EpicycleAnimation(path_points, epicycle_states)
    scene.render()
    
    # Move output
    manim_output = scene.renderer.file_writer.movie_file_path
    os.makedirs(os.path.dirname(OUTPUT_VIDEO) if os.path.dirname(OUTPUT_VIDEO) else ".", exist_ok=True)
    shutil.move(manim_output, OUTPUT_VIDEO)
    
    print("\n" + "━" * 60)
    print(f"✓ DONE → {OUTPUT_VIDEO}")
    print("━" * 60)


if __name__ == "__main__":
    main()