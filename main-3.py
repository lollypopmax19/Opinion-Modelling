
import re 
from network import Network
from view import NetworkView
from dynamics import Dynamics
import numpy as np
import keyboard
import Global
from gpuDynamics import GPUDynamics
import copy

def main():
    print("Willkommen! Was möchtest du tun?")
    print("1: Neues Netzwerk erstellen")
    print("2: Bestehendes Netzwerk laden")
    auswahl = input("Bitte wählen (1 oder 2): ")

    graph_model = None  

    if auswahl == "1":
        print("Erstelle ein neues Netzwerk...")
        Global.num_nodes = int(input("Gib die Anzahl der Knoten für das neue Netzwerk ein: "))
        graph_model = Network() 
        filename = "./Netzwerk/" + input("Gib den Dateinamen ein, um das Netzwerk zu speichern (z.B. 'meinNetzwerk'): ") + ".pk1"
        graph_model.save_network(filename)
        print(f"Neues Netzwerk wurde erstellt und in '{filename}' gespeichert.")
    elif auswahl == "2":
        filename = "./Netzwerk/" + input("Gib den Dateinamen des Netzwerks ein, das geladen werden soll (z.B. 'meinNetzwerk'): ") + ".pk1"
        try:
            match = re.search(r"Netzwerk(\d+)", filename)
            if match:
                Global.num_nodes = int(match.group(1)) 
                print(f"Die Anzahl der Knoten wurde auf {Global.num_nodes} gesetzt.")
            else:
                print("Der Dateiname entspricht nicht dem erwarteten Muster.")
                return

            graph_model = Network(load_from_file=filename)
            print(f"Netzwerk '{filename}' wurde erfolgreich geladen.")
        except FileNotFoundError:
            print(f"Die Datei '{filename}' wurde nicht gefunden. Beende das Programm.")
            return
    else:
        print("Ungültige Eingabe. Beende das Programm.")
        return

    graph_view = NetworkView(graph_model)
    

    if Global.RENDER_MODE == 0:
        g = copy.deepcopy(graph_model)
        gpuD = GPUDynamics(g, graph_view)
        
    elif Global.RENDER_MODE == 1:
        if Global.num_nodes > 500 or Global.num_iterations > 10000:
            raise ValueError("Inproper use. CPU mode only meant for demonstration purpose!")
        
        dynamics = Dynamics(graph_model, graph_view)
        graph_model.set_node_positions()
        graph_view.plot_graph(0, Global.c_star, np.zeros(Global.num_iterations), Global.W_D)
        graph_view.hold()
        

if __name__ == "__main__":
    main()