import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os
import tkinter as tk
import Global

nodeScale = 0.1
WINDOW_X = 1280
WINDOW_Y = 720

class NetworkView:
    def __init__(self, network):
        self.network = network

        self.window_width = WINDOW_X  
        self.window_height = WINDOW_Y

        self.fig_width = self.window_width / 100  
        self.fig_height = self.window_height / 100  


        self.fig, (self.ax_graph, self.ax_bar) = plt.subplots(
            2, 1, figsize=(self.fig_width, self.fig_height),
            gridspec_kw={'height_ratios': [4, 1]}  
        )
        self.fig.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, hspace=0.3)
        plt.ion()  

        self.fig.canvas.manager.resize(self.window_width, self.window_height)
        self.fig.canvas.manager.set_window_title('Meinungs-Graph mit Säulendiagramm')

        self.fontSize = 8  
        self.nodeSizeBase = 100  

        self.output_folder = './output'
        os.makedirs(self.output_folder, exist_ok=True)

    def plot_graph(self, frameCount, c_star, u, W_D=None):
        self.ax_graph.clear()

        # fügt vertikale Linien für die Meinungs-Skala hinzu
        self.add_vertical_lines()

        node_colors = []
        node_sizes = []
        
        # Durchlaufen der Knoten im Graph
        for node in self.network.graph.nodes:
            degree = len(self.network.graph.edges(node))
            if degree >= Global.c_star:
                node_colors.append('red')
            else:
                node_colors.append('skyblue')

            node_sizes.append(self.nodeSizeBase * degree * nodeScale)

        # Zeichne den Graphen
        nx.draw(
            self.network.graph,
            pos=self.network.positions,
            with_labels=False,  # Keine Beschriftungen
            node_color=node_colors,
            node_size=node_sizes,  
            ax=self.ax_graph,
        )

        self.fig.canvas.manager.set_window_title(
            f'Meinungs-Graph - Frame: {frameCount} - Connectivity >= {c_star}'
        )
        self.ax_graph.set_xlim(-1.2, 1.2)
        self.ax_graph.set_ylim(-1, 1)

        # füge die Meinungs-Skala hinzu
        self.add_opinion_scale()

        # Wenn W_D nicht None ist, zeichne eine zusätzliche Linie bei W_D
        if W_D is not None:
            # Zeichne eine vertikale Linie bei W_D im gleichen Stil wie die anderen Linien
            self.ax_graph.plot([W_D, W_D], [-1, 1], color='gray', lw=1, linestyle='--', zorder=-10)
            
            # Füge eine Beschriftung für W_D hinzu
            self.ax_graph.text(W_D, 1.05, f'W_D = {W_D:.2f}', ha='center', va='bottom', fontsize=self.fontSize)

        # Restlicher Plot-Code für das Säulendiagramm
        if u is not None:
            self.ax_bar.clear()
            n = len(u)
            x = range(n)
            self.ax_bar.bar(x, u, color="steelblue", width = 1)
            _average = (1.0 / Global.num_nodes) * sum(self.network.meinungen)               
            _curU = u[frameCount]
            self.ax_bar.set_title(
                f"Let f(n) := abs({r'${u*}_n$'}) | abs({f'${{u*}}_{{{frameCount+1}}}$'}) = " + str(round(_curU, 5)) + " | "
                f"{f'$\\bar{{\\omega}}_{{{frameCount+1}}}$'} = " + str(round(_average, 5)) + " | "
                f"{f'${{Effort}}_{{{frameCount+1}}}$'} = " + str(round(sum(u), 5))
            )



            
            self.ax_bar.set_xlabel("Number of Time Steps", fontsize=10)
            self.ax_bar.set_ylabel("f(n)", fontsize=10)

            step = int(Global.num_iterations / 10)
            xticks = list(range(0, n, step))  
            if n - 1 not in xticks: 
                xticks.append(n - 1)
            self.ax_bar.set_xticks(xticks)

            max_u = max(u)
            self.ax_bar.set_ylim(0, max_u * 1.1)

        # Speichern des Plots
        self.save_plot(frameCount)

        plt.draw()
        plt.pause(0.1)  # Kurze Pause für das Update



    def add_opinion_scale(self):
        self.ax_graph.plot([-1, 1], [1.05, 1.05], color='black', lw=2)

        opinion_ticks = np.linspace(-1, 1, 5)
        for tick in opinion_ticks:
            self.ax_graph.text(tick, 1.07, f'{tick:.2f}', ha='center', va='bottom', fontsize=self.fontSize)

    def add_vertical_lines(self):
        opinion_ticks = np.linspace(-1, 1, 5)
        for tick in opinion_ticks:
            self.ax_graph.plot([tick, tick], [-1, 1], color='gray', lw=1, linestyle='--', zorder=-10)

    def save_plot(self, frameCount):
        output_path = os.path.join(self.output_folder, f"frame_{frameCount:03d}.png")
        self.fig.savefig(output_path, dpi=300)
        print(f"Bild gespeichert: {output_path}")

    def hold(self):
        plt.show(block=True)
