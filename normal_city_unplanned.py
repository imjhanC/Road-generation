import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.colors import LinearSegmentedColormap
import random
from collections import deque
from scipy.spatial import KDTree  # For fast spatial queries

class InfiniteCityGenerator:
    def __init__(self):
        self.road_graph = nx.Graph()
        self.road_ages = {}  # Track road creation times
        self.node_positions = {}  # NodeID → (x,y)
        self.position_to_node = {}  # (x,y) → NodeID (for fast lookups)
        self.growth_queue = deque()
        self.current_time = 0
        self.min_distance = 0.03
        self.fig, self.ax = plt.subplots(figsize=(10, 10) , facecolor='black')
        
        # Optimized colormap
        self.cmap = LinearSegmentedColormap.from_list(
            'road_age', ['green','yellow', 'orange', 'red'])
        
        # Initialize spatial index
        self.kd_tree = None
        self._add_node((0, 0))
    
    def _update_spatial_index(self):
        """Update the KDTree with current node positions"""
        if self.node_positions:
            self.kd_tree = KDTree(list(self.node_positions.values()))
    
    def _is_valid_position(self, pos):
        """Fast position validation using KDTree"""
        if not self.kd_tree:
            return True
        distances, _ = self.kd_tree.query([pos], k=1)
        return distances[0] >= self.min_distance
    
    def _find_valid_position(self, base_pos, angle):
        """Find valid position using binary search pattern"""
        for distance in np.linspace(self.min_distance, 2*self.min_distance, 5):
            new_pos = (
                base_pos[0] + distance * np.cos(angle),
                base_pos[1] + distance * np.sin(angle)
            )
            if self._is_valid_position(new_pos):
                return new_pos
        return None
    
    def _add_node(self, pos):
        """Optimized node addition with spatial indexing"""
        if not self._is_valid_position(pos):
            return None
        
        node_id = len(self.node_positions)
        self.node_positions[node_id] = pos
        self.position_to_node[pos] = node_id
        self.road_graph.add_node(node_id, pos=pos)
        self.growth_queue.append(node_id)
        
        # Update spatial index periodically (not every time for performance)
        if node_id % 10 == 0:
            self._update_spatial_index()
        
        return node_id
    
    def _add_road(self, node1, node2):
        """Optimized road addition"""
        if node1 == node2:
            return
        
        road_id = (min(node1, node2), max(node1, node2))
        if road_id not in self.road_ages:
            self.road_graph.add_edge(node1, node2)
            self.road_ages[road_id] = self.current_time
    
    def grow_city(self):
        """Optimized growth algorithm"""
        if not self.growth_queue:
            if self.node_positions:
                self.growth_queue.append(random.choice(list(self.node_positions.keys())))
            return
        
        self.current_time += 1
        node_id = self.growth_queue.popleft()
        pos = self.node_positions[node_id]
        
        # Generate 1-3 new roads in random directions
        for _ in range(random.randint(1, 3)):
            angle = random.uniform(0, 2*np.pi)
            new_pos = self._find_valid_position(pos, angle)
            
            if new_pos is not None:
                # Check if position already exists (for merging roads)
                existing_node = self.position_to_node.get(new_pos)
                if existing_node is not None:
                    self._add_road(node_id, existing_node)
                else:
                    new_node = self._add_node(new_pos)
                    if new_node is not None:
                        self._add_road(node_id, new_node)
    
    def optimized_render(self):
        """Massively optimized rendering"""
        self.ax.clear()
        self.ax.set_facecolor((0.01,0.02, 0.02, 0.05))
        
        # Precompute all road segments and colors
        segments = []
        colors = []
        widths = []
        
        for (u, v), time_added in self.road_ages.items():
            age = self.current_time - time_added
            normalized_age = min(1.0, age / 50)
            
            pos_u = self.node_positions[u]
            pos_v = self.node_positions[v]
            
            # Main line
            segments.append([pos_u, pos_v])
            colors.append(self.cmap(normalized_age))
            widths.append(1.5)
            
            # Glow effect
            segments.append([pos_u, pos_v])
            colors.append(self.cmap(normalized_age))
            widths.append(4.0)
        
        # Batch draw all lines
        from matplotlib.collections import LineCollection
        lc_main = LineCollection(
            segments[::2],  # Main lines
            colors=colors[::2],
            linewidths=widths[::2],
            alpha=0.9,
            capstyle='round'
        )
        lc_glow = LineCollection(
            segments[1::2],  # Glow effects
            colors=colors[1::2],
            linewidths=widths[1::2],
            alpha=0.2,
            capstyle='round'
        )
        
        self.ax.add_collection(lc_glow)
        self.ax.add_collection(lc_main)
        
        stats_text = f"Roads: {len(self.road_ages)}\nNodes: {len(self.node_positions)}"
        self.ax.text(
            0.02, 0.98, stats_text,
            transform=self.ax.transAxes,
            color='white',
            fontsize=10,
            verticalalignment='top',
            bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))

        # Adjust view
        if self.node_positions:
            all_pos = np.array(list(self.node_positions.values()))
            min_coords = all_pos.min(axis=0) - 0.1
            max_coords = all_pos.max(axis=0) + 0.1
            self.ax.set_xlim(min_coords[0], max_coords[0])
            self.ax.set_ylim(min_coords[1], max_coords[1])
        
        self.ax.axis('off')
        plt.pause(0.001)  # Reduced pause time

def main():
    print("Starting optimized city generator...")
    print("Press Ctrl+C to stop")
    
    plt.ion()
    generator = InfiniteCityGenerator()
    
    try:
        while True:
            # Process multiple growth steps per frame for faster simulation
            for _ in range(10):  # Process 10 growth steps per render
                generator.grow_city()
            
            generator.optimized_render()
                
    except KeyboardInterrupt:
        print("\nFinal stats:")
        print(f"Roads: {len(generator.road_ages)}")
        print(f"Nodes: {len(generator.node_positions)}")
        plt.savefig('fast_city.png', dpi=300, bbox_inches='tight', facecolor='black')
        plt.close()

if __name__ == "__main__":
    main()