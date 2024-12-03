import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Datei einlesen (Passe den Pfad an, falls notwendig)
file_path = 'csv_files\ModSimAuswertungComp.csv'

# CSV-Datei einlesen mit Semikolon als Trennzeichen
data = pd.read_csv(file_path, sep=';')

# Relevante Spalten auswählen und leere Werte entfernen
cleaned_data = data[['C_Star', 'Cost', 'Frames']].dropna()

# Funktion zur Berechnung des 95%-Konfidenzintervalls über Bootstrap
def bootstrap_confidence_interval(data, stat_function=np.median, n_bootstrap=1000, ci=95):
    bootstrapped_stats = [
        stat_function(np.random.choice(data, size=len(data), replace=True)) for _ in range(n_bootstrap)
    ]
    lower_bound = np.percentile(bootstrapped_stats, (100 - ci) / 2)
    upper_bound = np.percentile(bootstrapped_stats, 100 - (100 - ci) / 2)
    return lower_bound, upper_bound

# Gruppierung nach 'C_Star' und Berechnung der Konfidenzintervalle
confidence_intervals_cost = {}
confidence_intervals_frames = {}
for c_star, group in cleaned_data.groupby('C_Star'):
    # Konfidenzintervall für Cost
    ci_lower_cost, ci_upper_cost = bootstrap_confidence_interval(group['Cost'])
    confidence_intervals_cost[c_star] = (ci_lower_cost, ci_upper_cost)
    
    # Konfidenzintervall für Frames
    ci_lower_frames, ci_upper_frames = bootstrap_confidence_interval(group['Frames'])
    confidence_intervals_frames[c_star] = (ci_lower_frames, ci_upper_frames)

# Plot erstellen
fig, ax1 = plt.subplots(figsize=(12, 8))

# Linke Y-Achse: Konfidenzintervalle für Cost
for i, (c_star, (ci_lower, ci_upper)) in enumerate(confidence_intervals_cost.items()):
    ax1.plot([i, i], [ci_lower, ci_upper], color='blue', linewidth=4, label='Cost' if i == 0 else "")
    ax1.scatter([i], [ci_lower], color='blue', zorder=5)
    ax1.scatter([i], [ci_upper], color='blue', zorder=5)

# Rechte Y-Achse: Konfidenzintervalle für Frames
ax2 = ax1.twinx()
for i, (c_star, (ci_lower, ci_upper)) in enumerate(confidence_intervals_frames.items()):
    ax2.plot([i, i], [ci_lower, ci_upper], color='green', linewidth=4, label='Frames' if i == 0 else "")
    ax2.scatter([i], [ci_lower], color='green', zorder=5)
    ax2.scatter([i], [ci_upper], color='green', zorder=5)

# Achsen und Titel anpassen
ax1.set_ylabel('Cost (blue)', fontsize=12, color='blue')
ax2.set_ylabel('Frames (green)', fontsize=12, color='green')

# X-Achse anpassen: Beschriftungen in größeren Intervallen
step_size = 10  # Schrittgröße für die x-Achse
x_labels = list(confidence_intervals_cost.keys())
plt.xticks(ticks=range(0, len(x_labels), step_size), labels=x_labels[::step_size], fontsize=12)

# Titel und Raster
plt.title('95% Confidence Interval of Cost and Step Count', fontsize=14)
ax1.grid(axis='y', linestyle='--', alpha=0.7)
ax1.set_xlabel('Connectivity Level', fontsize=12)
ax1.xaxis.set_label_coords(0.95, -0.01)

# Diagramm anzeigen
plt.tight_layout()
plt.show()
