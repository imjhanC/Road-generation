import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.colors import LinearSegmentedColormap
from collections import deque
from scipy.spatial import KDTree
from matplotlib.collections import LineCollection

class InfiniteCityGenerator:
    def __init__(self):
        self.node_positions = []  # List of (x, y) tuples
        self.road_graph = nx.Graph()
        self.road_ages = {}
        self.growth_queue = deque()
        self.current_time = 0
        self.min_distance = 0.03
        self.kd_tree = None
        self.kd_tree_dirty = False
        self.rng = np.random.default_rng()

        self.fig, self.ax = plt.subplots(figsize=(10, 10), facecolor='black')
        self.ax.set_facecolor((0.01, 0.02, 0.02, 0.05))

        self.cmap = LinearSegmentedColormap.from_list(
            'road_age', ['green', 'yellow', 'orange', 'red'])

        # Initialize first node
        self._add_node((0.0, 0.0))

        # For persistent collections
        self.lc_main = None
        self.lc_glow = None

    def _update_spatial_index(self):
        if self.node_positions:
            self.kd_tree = KDTree(self.node_positions)
        self.kd_tree_dirty = False

    def _is_valid_position(self, pos):
        if self.kd_tree_dirty:
            self._update_spatial_index()
        if not self.kd_tree:
            return True
        distance, _ = self.kd_tree.query([pos], k=1)
        return distance[0] >= self.min_distance

    def _find_valid_position(self, base_pos, angle):
        distances = np.linspace(self.min_distance, 2 * self.min_distance, 5)
        x = base_pos[0] + distances * np.cos(angle)
        y = base_pos[1] + distances * np.sin(angle)
        positions = np.stack([x, y], axis=1)
        for pos in positions:
            if self._is_valid_position(tuple(pos)):
                return tuple(pos)
        return None

    def _add_node(self, pos):
        if not self._is_valid_position(pos):
            return None

        node_id = len(self.node_positions)
        self.node_positions.append(pos)
        self.road_graph.add_node(node_id, pos=pos)
        self.growth_queue.append(node_id)
        self.kd_tree_dirty = True

        return node_id

    def _add_road(self, node1, node2):
        if node1 == node2:
            return
        road_id = (min(node1, node2), max(node1, node2))
        if road_id not in self.road_ages:
            self.road_graph.add_edge(node1, node2)
            self.road_ages[road_id] = self.current_time

    def grow_city(self):
        if not self.growth_queue:
            if self.node_positions:
                self.growth_queue.append(self.rng.integers(0, len(self.node_positions)))
            return

        self.current_time += 1
        node_id = self.growth_queue.popleft()
        pos = self.node_positions[node_id]

        for _ in range(self.rng.integers(1, 4)):
            angle = self.rng.uniform(0, 2 * np.pi)
            new_pos = self._find_valid_position(pos, angle)
            if new_pos:
                # Check if node already exists nearby
                if self.kd_tree_dirty:
                    self._update_spatial_index()
                dist, idx = self.kd_tree.query([new_pos], k=1)
                if dist[0] < self.min_distance * 0.5:
                    self._add_road(node_id, idx[0])
                else:
                    new_node_id = self._add_node(new_pos)
                    if new_node_id is not None:
                        self._add_road(node_id, new_node_id)

    def optimized_render(self):
        segments_main = []
        segments_glow = []
        colors_main = []
        colors_glow = []
        widths_main = []
        widths_glow = []

        for (u, v), time_added in self.road_ages.items():
            age = self.current_time - time_added
            norm_age = min(1.0, age / 50)
            pos_u = self.node_positions[u]
            pos_v = self.node_positions[v]

            segments_main.append([pos_u, pos_v])
            colors_main.append(self.cmap(norm_age))
            widths_main.append(1.5)

            segments_glow.append([pos_u, pos_v])
            colors_glow.append(self.cmap(norm_age))
            widths_glow.append(4.0)

        if self.lc_main:
            self.lc_main.set_paths(segments_main)
            self.lc_main.set_color(colors_main)
            self.lc_main.set_linewidth(widths_main)
        else:
            self.lc_main = LineCollection(segments_main, colors=colors_main, linewidths=widths_main, alpha=0.9, capstyle='round')
            self.ax.add_collection(self.lc_main)

        if self.lc_glow:
            self.lc_glow.set_paths(segments_glow)
            self.lc_glow.set_color(colors_glow)
            self.lc_glow.set_linewidth(widths_glow)
        else:
            self.lc_glow = LineCollection(segments_glow, colors=colors_glow, linewidths=widths_glow, alpha=0.2, capstyle='round')
            self.ax.add_collection(self.lc_glow)

        all_pos = np.array(self.node_positions)
        min_coords = all_pos.min(axis=0) - 0.1
        max_coords = all_pos.max(axis=0) + 0.1
        self.ax.set_xlim(min_coords[0], max_coords[0])
        self.ax.set_ylim(min_coords[1], max_coords[1])

        self.ax.text(0.02, 0.98,
                     f"Roads: {len(self.road_ages)}\nNodes: {len(self.node_positions)}",
                     transform=self.ax.transAxes,
                     color='white', fontsize=10, verticalalignment='top',
                     bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))

        self.ax.axis('off')
        plt.pause(0.001)


def main():
    print("Starting high-performance city generator... Press Ctrl+C to stop")
    plt.ion()
    generator = InfiniteCityGenerator()
    frame = 0

    try:
        while True:
            for _ in range(15):  # More growth steps per render
                generator.grow_city()

            if frame % 2 == 0:
                generator.optimized_render()

            frame += 1

    except KeyboardInterrupt:
        print("\nSimulation ended.")
        print(f"Final stats: Roads={len(generator.road_ages)}, Nodes={len(generator.node_positions)}")
        plt.savefig("final_city.png", dpi=300, bbox_inches='tight', facecolor='black')
        plt.close()


if __name__ == '__main__':
    main()
