# Infinite City Generator

A procedural city growth simulation using Python, NetworkX, and Matplotlib. Generates organic-looking city road networks with visual aging effects.

![Example City](final_city_grid.png)

## Features

- **Procedural Growth**: Cities expand organically from a central point
- **Optimized Rendering**: Uses KD-trees and batch rendering for performance
- **Visual Aging**: Roads change color as they "age" (green → yellow → orange → red)
- **Multiple Algorithms**: Includes different generation styles:
  - Pure random growth
  - Directional bias (cardinal directions)
  - Grid-based structured growth
- **Interactive Visualization**: Watch the city grow in real-time

## Requirements

- Python 3.7+
- Required packages:
  - numpy
  - matplotlib
  - networkx
  - scipy

## Controls 
- The simulation runs automatically.
- Watch the city grow in real-time.
- Press Ctrl+C to: 
  - Stop the simulation
  - Save the current city as png file
  - Print final statistics (road/node counts)

## 🛠️ Customization
- **min_distance** : Controls node spacing (smaller = denser)
- **grid_size** : Grid alignment spacing in structured versions
- **LinearSegmentedColormap** : Change the road age color gradient
- Growth steps : How many growth steps occur per frame
- Angle options : Change direction bias (e.g. N/S/E/W only)

## 🧠 How It Works
- **Initialization**
  - Starts with a single node at (x, y) — usually (0, 0) or near it
  - Sets up growth queue and spatial index (KDTree)
- **Growth Cycle**
  - Picks a node
  - Chooses 1–3 directions (with directional bias + noise)
  - Validates potential new positions (distance & terrain check)
  - Adds road and new node if valid
- **Rendering**
  - Uses matplotlib.LineCollection for fast batch drawing
  - Glow effect via double-drawing lines (bright + transparent)
  - Auto-scales the viewport as the city expands

## 🚀 Key Optimizations
- **KD-Tree** spatial indexing for fast nearest-neighbor lookups
- **Deferred rendering** — multiple growth steps per frame
- **Persistent LineCollections** — reusing instead of recreating lines
- **Grid snapping** for clean layouts in structured versions

## 🌈 Road Aging System
Each road stores a creation timestamp. The age is visualized through color gradients:
| Age (Steps) | Color   |
|-------------|---------|
| 0–15        | Green   |
| 15–30       | Yellow  |
| 30–50       | Orange  |
| 50+         | Red     |
This helps you see how the city evolved over time.

## Installation

```bash
git clone https://github.com/yourusername/infinite-city-generator.git
cd infinite-city-generator
pip install -r requirements.txt
