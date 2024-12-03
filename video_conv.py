import cv2
import os
import glob

# Definiere die Verzeichnisse
input_folder = './output'  # Ordner mit den Bildern
output_folder = './video_output'  # Ordner, in dem das Video gespeichert wird

# Stelle sicher, dass der Zielordner existiert
os.makedirs(output_folder, exist_ok=True)

# Hole alle Bilddateien im Ordner (angenommen, es sind PNG-Dateien)
image_files = sorted(glob.glob(os.path.join(input_folder, '*.png')))  # Du kannst auch .jpg oder andere Formate verwenden

# Wenn keine Bilder im Ordner gefunden wurden, abbrechen
if not image_files:
    print(f"Keine Bilder im Ordner {input_folder} gefunden!")
    exit()

# Lese das erste Bild, um die Video-Größe zu bestimmen
first_image = cv2.imread(image_files[0])
height, width, _ = first_image.shape  # Extrahiere Höhe und Breite des ersten Bildes

# Video-Writer konfigurieren (24 FPS und MP4-Codec)
video_filename = os.path.join(output_folder, 'output_video.mp4')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # wählt den MP4-Codec
video_writer = cv2.VideoWriter(video_filename, fourcc, 24, (width, height))

# Füge alle Bilder zum Video hinzu
for image_file in image_files:
    img = cv2.imread(image_file)  # Lese das Bild
    video_writer.write(img)  # Füge das Bild dem Video hinzu

# Schließe den Video-Writer
video_writer.release()

print(f"Video wurde erfolgreich unter {video_filename} gespeichert!")
