# 🌆 Infinite Road Generator 

This Python project simulates the growth of a city road network using a directional grid-like logic, enhanced with spatial awareness and terrain rules like rivers and terrain exclusion.

## 🚀 Features

- **Infinite procedural growth** of roads and intersections
- **River-aware pathfinding**: avoids generating roads across defined river areas
- **Smooth performance** using spatial indexing (`KDTree`)
- **Color-coded aging** of roads (green = new, red = old)
- **Glowing visualization** with matplotlib for a futuristic look