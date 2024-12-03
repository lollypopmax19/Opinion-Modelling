import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx
import numpy as np
from network import Network
import Global

NUM_NODES = 1000
##tool script! Execute this script directly to visualize the influence of GAMMA in the network distribution

class NetworkView:
    def __init__(self, network):
        self.network = network
        self.fig, (self.ax_graph, self.ax_bar) = plt.subplots(
            2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]} 
        )
        self.fig.subplots_adjust(left=0.08, right=0.97, bottom=0.1, top=0.9, hspace=0.2) 
        plt.ion()
        self.fig.canvas.manager.set_window_title('Netzwerk Visualisierung')

        self.cmap = mcolors.LinearSegmentedColormap.from_list("custom_blue", ["#3487FF", "#09182E"])
        self.norm = None
        self.cbar = None

    def setup_colorbar(self, min_edges, max_edges):
        """Erstellt die Farbskala an der rechten Seite des Plots (einmalig)"""
        self.norm = mcolors.Normalize(vmin=0, vmax=100)
        sm = plt.cm.ScalarMappable(cmap=self.cmap, norm=self.norm)
        sm.set_array([])

        if self.cbar is None:
            self.cbar = self.fig.colorbar(sm, ax=self.ax_graph, orientation='vertical', pad=0.01, shrink=0.98)  
            self.cbar.ax.set_position([0.91, 0.4, 0.02, 0.5])
            self.cbar.set_label('Number of Edges')

        ticks = self.cbar.get_ticks()
        ticks[-1] = 100  # Stelle sicher, dass der letzte Wert immer noch 100 ist
        self.cbar.set_ticks(ticks)
        tick_labels = [str(int(tick)) if tick < 100 else '100+' for tick in ticks]
        self.cbar.set_ticklabels(tick_labels)

    def plot_graph(self):
        self.ax_graph.clear()

        node_sizes = [
            (100 + 400 * len(self.network.graph.edges(node)) / self.network.maxEdges) 
            for node in self.network.graph.nodes
        ]

        edge_counts = [len(self.network.graph.edges(node)) for node in self.network.graph.nodes]
        min_edges = min(edge_counts)
        max_edges = max(edge_counts)

        if self.norm is None:
            self.setup_colorbar(min_edges, max_edges)

        node_colors = [self.cmap(self.norm(edge_count)) for edge_count in edge_counts]

        nodes_sorted_by_edge_count = sorted(self.network.graph.nodes, key=lambda node: len(self.network.graph.edges(node)))
        node_sizes_sorted = [node_sizes[list(self.network.graph.nodes).index(node)] for node in nodes_sorted_by_edge_count]
        node_colors_sorted = [node_colors[list(self.network.graph.nodes).index(node)] for node in nodes_sorted_by_edge_count]

        for node, size, color in zip(nodes_sorted_by_edge_count, node_sizes_sorted, node_colors_sorted):
            pos = self.network.positions[node]
            zorder = 10 / size 
            self.ax_graph.scatter(
                pos[0], pos[1], s=size, c=[color], zorder=zorder
            )

        self.ax_graph.set_title("Network with " + str(Global.num_nodes) + " agents | "+ '\u03B3' + " = "+ str(round(self.network.GAMMA, 2)) + " | Median of Edges: " + str( round( (np.median(self.network.get_edge_array()) ), 2 ) ) )

        self.ax_graph.set_yticks([])  
        self.ax_graph.set_ylabel('') 

        self.plot_bar_chart()

        plt.draw()
        plt.pause(0.1)

    def plot_bar_chart(self):
        self.ax_bar.clear()

        edges = np.arange(self.network.minEdges, self.network.maxEdges + 1)
        probabilities = edges ** (-self.network.GAMMA)
        probabilities /= probabilities.sum()

        self.ax_bar.bar(edges, probabilities, color='steelblue')
        self.ax_bar.set_title("Distribution Curve")
        self.ax_bar.set_xlabel("Edge Count")
        self.ax_bar.set_ylabel("Relative Frequency")
        self.ax_bar.set_xlim(self.network.minEdges, self.network.maxEdges)

        self.adjust_layout()

    def save_plot(self, gamma):
        """Speichert den aktuellen Plot als Bild im network_renders Ordner"""
        output_folder = './network_renders'
        os.makedirs(output_folder, exist_ok=True)

        output_path = os.path.join(output_folder, f"gamma_{gamma}.png")
        self.fig.savefig(output_path, dpi=300)
        print(f"Bild gespeichert: {output_path}")

    def adjust_layout(self):
        self.ax_graph.set_position([0.08, 0.4, 0.83, 0.5])  # adjust the width of the graph
        self.ax_bar.set_position([0.08, 0.1, 0.90, 0.2])   # keep the bar chart the same


Global.num_nodes = NUM_NODES
network = Network()
view = NetworkView(network)

for gamma in np.arange(0.5, 2.0, 0.1):
        network.GAMMA = gamma
        network.setup_initial_graph()
        network.set_node_positions()
        
        view.plot_graph()
        view.adjust_layout()
        view.save_plot(gamma)

        plt.pause(0.1)

plt.show(block=True)
