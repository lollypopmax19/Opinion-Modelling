import networkx as nx
import numpy as np
import pickle
import Global

class Network:

    overall_edge_count = None
    minEdges = None
    maxEdges = None
    GAMMA = None 
    sigmaStart = None
    sigmaEnd = None 

    def __init__(self, load_from_file=None):

        self.overall_edge_count = 0
        self.minEdges = 1
        self.maxEdges = Global.num_nodes-1
        self.GAMMA = 1.5
        self.sigmaStart = 0.5
        self.sigmaEnd = 0.1

        if load_from_file:
            self.load_network(load_from_file)
        else:
            self.num_nodes = Global.num_nodes
            self.graph = None
            self.positions = {}
            self.setup_initial_graph()
            self.meinungen = np.zeros(Global.num_nodes)
            for i in range(Global.num_nodes):
                _new_meinung = np.random.normal(loc=0, scale=self.calc_sigma(i))
                self.update_meinung(i, _new_meinung)
    

    def calc_sigma(self, index):
        _edgeCount = self.get_num_edges(index)
        _m = (0.5-0.1) / (1.0 - self.maxEdges) #Modell mit linearen Abfall!
        return _m * (_edgeCount - 1.0) + 0.5

    def setup_initial_graph(self):
        self.overall_edge_count = 0
        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(self.num_nodes))
        
        edges = np.arange(self.minEdges, self.maxEdges + 1)
        probabilities = edges ** (-self.GAMMA)
        probabilities /= probabilities.sum()

        for node in range(self.num_nodes):
            num_edges = np.random.choice(edges, p=probabilities)

            potential_neighbors = list(range(self.num_nodes))
            potential_neighbors.remove(node)

            num_edges = min(len(potential_neighbors), num_edges)
        

            neighbors = np.random.choice(potential_neighbors, num_edges, replace=False)

            for neighbor in neighbors:
                self.graph.add_edge(node, neighbor)

            self.overall_edge_count += num_edges

    def set_node_positions(self):
        self.positions = {
            i: (np.clip(self.meinungen[i], -1, 1), (i % 180 - 90) / 100.0) #basierend auf index wird mit mod die höhe gesetzt
            for i in range(self.num_nodes)
        }

    def update_meinung(self, node_index, new_meinung):
        if 0 <= node_index < self.num_nodes:
            self.meinungen[node_index] = np.clip(new_meinung, -1, 1)
            self.set_node_positions()
            
        else:
            print("Ungültiger Knotenindex.")

    def set_meinungen(self, new_meinung):
        self.meinungen = new_meinung
        self.set_node_positions()

    def get_num_edges(self, node_index):
        if 0 <= node_index < self.num_nodes:
            return len(self.graph.edges(node_index))
        else:
            print("Ungültiger Knotenindex.")
            return None

    def get_edge_array(self):
        array = np.zeros(self.num_nodes)
        for i in range(self.num_nodes):
            array[i] = self.get_num_edges(i)
        return array

    def get_meinung(self, node_index):
        if 0 <= node_index < self.num_nodes:
            return self.meinungen[node_index]
        else:
            print("Ungültiger Knotenindex.")
            return None

    def get_w(self):
        return self.meinungen

    def is_neighbor(self, i, j):
        if i < 0 or j < 0 or i >= self.num_nodes or j >= self.num_nodes:
            print(f"Ungültige Knotenindizes: {i}, {j}")
            return 0
        return int(self.graph.has_edge(i, j))

    def save_network(self, filename):
        data = {
            "num_nodes": self.num_nodes,
            "graph": self.graph,
            "positions": self.positions,
            "meinungen": self.meinungen,
        }
        with open(filename, "wb") as file:
            pickle.dump(data, file)
        print(f"Netzwerk erfolgreich in {filename} gespeichert.")

    def load_network(self, filename):
        with open(filename, "rb") as file:
            data = pickle.load(file)
        self.num_nodes = data["num_nodes"]
        self.graph = data["graph"]
        self.positions = data["positions"]
        self.meinungen = data["meinungen"]
        print(f"Netzwerk erfolgreich aus {filename} geladen.")