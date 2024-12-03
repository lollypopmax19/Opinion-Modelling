import os
from PIL import Image

# Pfad zum Ordner mit den PNG-Dateien
input_folder = r"C:\Users\crisk\Documents\uni\Semester3\ModSim\backup\output"  # Ersetze mit deinem Ordnerpfad
output_folder = r"C:\Users\crisk\Documents\uni\Semester3\ModSim\backup\oout"  # Ersetze mit dem Pfad für die neuen Bilder

# Überprüfen, ob der Ausgabepfad existiert, falls nicht, erstelle ihn
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Neue Zielgröße (1280x720)
new_size = (1280, 720)

# Alle Dateien im Ordner durchgehen
for filename in os.listdir(input_folder):
    if filename.endswith(".png"):
        # Erstelle den vollständigen Pfad zur Datei
        input_path = os.path.join(input_folder, filename)
        
        # Öffne das Bild
        img = Image.open(input_path)
        
        # Skaliere das Bild auf die neue Größe
        img_resized = img.resize(new_size)
        
        # Speichern des Bildes im Ausgabeverzeichnis
        output_path = os.path.join(output_folder, filename)
        img_resized.save(output_path)
        
        print(f"Bild {filename} wurde auf {new_size[0]}x{new_size[1]} skaliert und gespeichert.")

