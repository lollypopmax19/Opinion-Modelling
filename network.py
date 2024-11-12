import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
import numpy as np

# Parameter für die Simulation
N = 10000  # Anzahl der Knoten
m0 = 5   # Anzahl der Startknoten
m = 3    # Anzahl der neuen Verbindungen pro neuen Knoten
max_edges = 20  # Maximale Anzahl der Kanten pro Knoten
min_edges = 1   # Minimale Anzahl der Kanten pro Knoten

# Starte mit einem kleinen vollständigen Netzwerk
G = nx.complete_graph(m0)

# Zuweisung von Meinungswerten zu den Knoten mit Normalverteilung und Begrenzung auf [-1, 1]
opinions = {node: np.clip(np.random.normal(0, 0.5), -1, 1) for node in G.nodes()}

# Funktion zur Berechnung der Ähnlichkeit von Meinungswerten
def opinion_similarity(op1, op2):
    return 1 - abs(op1 - op2)  # Höhere Ähnlichkeit bei kleineren Differenzen

# Füge neue Knoten hinzu und berechne die Wahrscheinlichkeit basierend auf der Meinungssimilarität
for i in range(m0, N):
    G.add_node(i)
    opinions[i] = np.clip(np.random.normal(0, 0.5), -1, 1)
    targets = set()
    while len(targets) < m:
        node = random.choice(list(G.nodes()))
        if node != i and G.degree[node] < max_edges:
            similarity = opinion_similarity(opinions[i], opinions[node])
            if random.random() < similarity:  # Höhere Wahrscheinlichkeit bei höherer Ähnlichkeit
                targets.add(node)
    for t in targets:
        G.add_edge(i, t)
    if G.degree[i] < min_edges:
        while G.degree[i] < min_edges:
            extra_node = random.choice(list(G.nodes()))
            if extra_node != i and G.degree[extra_node] < max_edges:
                G.add_edge(i, extra_node)

# Positionierung der Knoten basierend auf ihren Meinungswerten
pos = {node: (opinions[node], random.uniform(0, 1)) for node in G.nodes()}

# Bestimme die Knoten mit den meisten Verbindungen (Top 10%)
num_top_nodes = max(1, N // 10)  # Anzahl der Top-Knoten
top_nodes = sorted(G.degree, key=lambda x: x[1], reverse=True)[:num_top_nodes]

# Benutzerdefinierter Farbverlauf von #1E90FF bis #104E8B
cmap = mcolors.LinearSegmentedColormap.from_list("custom_blue", ["#1E90FF", "#104E8B"])

# Farbverlauf basierend auf der Anzahl der Kanten
max_degree = max(dict(G.degree()).values())
min_degree = min(dict(G.degree()).values())
colors = cmap(np.linspace(0, 1, max_degree - min_degree + 1))

# Farbe und Label der Knoten basierend auf ihrer Anzahl von Kanten und Meinungswerten
node_colors = []
labels = {}
for node in G.nodes():
    opinion = opinions[node]
    degree = G.degree[node]
    color_index = degree - min_degree
    node_colors.append(colors[color_index])
    labels[node] = f"{opinion:.2f}"

# Zeichne das Netzwerk mit hervorgehobenen Knoten und Meinungswerten
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor('grey')  # Setze den Hintergrund der gesamten Abbildung auf grau
ax.set_facecolor('grey')  # Setze den Hintergrund der Achse auf grau
nx.draw(G, pos, with_labels=True, labels=labels, node_size=700, node_color=node_colors, edge_color="gray", font_size=10, font_color="white", ax=ax)

# Hinzufügen der Farbverlauflegende
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min_degree, vmax=max_degree))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label('Anzahl der Kanten')

ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-0.1, 1.1)
plt.show()
