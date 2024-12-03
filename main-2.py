
import re 
from network import Network
from view import NetworkView
from dynamics import Dynamics
import numpy as np
import keyboard
import Global
from gpuDynamics import GPUDynamics
import csv

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
        import re

    with open('beeinflusste_knoten.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # Schreibe die Kopfzeile
        writer.writerow(["Netzwerk", "C_star", "Beeinflusste Knoten"])
        # Schreibe die Ergebnisse für das aktuelle Netzwerk und C_star in die CSV
        for i in range(1, 11):  # Schleife von 1 bis 10

            filename = f"./Netzwerk/{i}Netzwerk1000.pk1"  # Dynamischer Dateiname        

            try:
            # Extrahiere die führende Zahl und den Netzwerknamen
                match = re.search(r"(\d+)Netzwerk(\d+)", filename)
                if match:
                    leading_number = int(match.group(1))  # Führende Zahl extrahieren (1 bis 10)
                    network_number = int(match.group(2))  # Netzwerknummer extrahieren (1000)
                    Global.num_nodes = network_number
                    #print(f"Netzwerk mit führender Zahl {leading_number} und {Global.num_nodes} Knoten wird geladen.")
                else:
                    print(f"Der Dateiname '{filename}' entspricht nicht dem erwarteten Muster.")
                    continue  # Überspringe diese Iteration
        
                # Lade das Netzwerk
                graph_model = Network(load_from_file=filename)
                print(f"Netzwerk '{filename}' wurde erfolgreich geladen.")
    
            except FileNotFoundError:
                print(f"Die Datei '{filename}' wurde nicht gefunden. Überspringe diese Datei.")
                continue  # Fahre mit der nächsten Datei fort

            graph_view = NetworkView(graph_model)
            if Global.RENDER_MODE == 0:
                #gpuD = GPUDynamics(graph_model, graph_view)
                for c_star in range(5, 201, 5):
                        influenced_nodes_count = GPUDynamics.count_influenced_nodes(graph_model, c_star)
                        writer.writerow([i, c_star, influenced_nodes_count])
            elif Global.RENDER_MODE == 1:
                if Global.num_nodes > 500 or Global.num_iterations > 500:
                    raise ValueError("Inproper use. CPU mode only meant for demonstration purpose!")
        
                # dynamics = Dynamics(graph_model, graph_view)
                # graph_model.set_node_positions()
                # graph_view.plot_graph(0, Global.c_star, np.zeros(Global.num_iterations), Global.W_D)
                # print("Drücke die Leertaste, um die Meinungsaktualisierung zu starten...")
                # keyboard.wait('space')
                # dynamics.update_graph()
                # graph_view.hold()
        else:
            print("Ungültige Eingabe. Beende das Programm.")
            return


        

if __name__ == "__main__":
    main()