import os
import re

# Pfad zum Ordner mit den PNG-Dateien
input_folder = r"C:\Users\crisk\Documents\uni\Semester3\ModSim\backup\output"  # Ersetze mit deinem Ordnerpfad

# Liste der PNG-Dateien im Ordner
files = [f for f in os.listdir(input_folder) if f.endswith(".png")]

# Sortiere die Dateien nach der Nummer im Namen
# Die Zahl wird extrahiert und die Liste wird entsprechend sortiert
files.sort(key=lambda x: int(re.search(r'(\d+)', x).group()))

# Umbenennen der Dateien
for i, filename in enumerate(files, start=1):
    # Extrahiere die Nummer und ersetze "_" durch "-"
    new_name = f"frame-{i}.png"
    
    # Erstelle den vollständigen Pfad zur aktuellen Datei
    old_path = os.path.join(input_folder, filename)
    
    # Erstelle den vollständigen Pfad zur neuen Datei
    new_path = os.path.join(input_folder, new_name)
    
    # Umbenennen der Datei
    os.rename(old_path, new_path)
    
    print(f"Datei {filename} wurde umbenannt in {new_name}")
