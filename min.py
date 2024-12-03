import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Pfad zur CSV-Datei
file_path = 'csv_files/ModSimAuswertungComp.csv'

# CSV-Datei einlesen und relevante Spalten auswählen
data = pd.read_csv(file_path, sep=';')
cleaned_data = data[['C_Star', 'Cost', 'Frames']].dropna()

# Mittelwerte von Cost und Frames pro C_Star berechnen
mean_values = cleaned_data.groupby('C_Star').agg({'Cost': 'mean', 'Frames': 'mean'})

print(mean_values)

# Berechnung der maximalen Werte für Cost und Frames
max_cost = mean_values['Cost'].max()
max_frames = mean_values['Frames'].max()

print(max_cost)
print(max_frames)


# Berechnung der Formel für jedes C_Star
mean_values['Formula'] = 0.5 * (mean_values['Cost'] / max_cost + mean_values['Frames'] / max_frames)

# Plot erstellen
fig, ax = plt.subplots(figsize=(12, 8))

# Plot der Formel gegen C_Star
ax.plot(mean_values.index, mean_values['Formula'], marker='o', linestyle='-', color='blue')

# Achsenbeschriftungen und Titel anpassen
ax.set_xlabel('Connectivity Level', fontsize=12)
ax.xaxis.set_label_coords(0.93, -0.05)

# y-Achse mit Subscript-Formatierung
ax.set_ylabel(r'$f (c_i)$', fontsize=14)
ax.yaxis.set_label_coords(-0.01, 0.97)

# Titel mit LaTeX-Formel
# ax.set_title(
#     r'Let Q = $\{c_i, i = 5, 10, \dots, 200\}$. ' 
#     r'$f(c_i) = 0.5 \left(\frac{\text{Cost}(c_i)}{\max(\text{Cost}(Q))} + \frac{\text{Frames}(c_i)}{\max(\text{Frames}(Q))} \right)$', 
#     fontsize=14
# )

# Gitterlinien hinzufügen
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Diagramm optisch anpassen und anzeigen
plt.tight_layout()
plt.show()
