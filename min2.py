import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Datei einlesen (Passe den Pfad an, falls notwendig)
file_path = 'csv_files\Beeinflusste_knoten.csv'
data = pd.read_csv(file_path, sep=',')

# Relevante Spalten auswählen und leere Werte entfernen
cleaned_data = data[['C_star', 'Beeinflusste_Knoten']].dropna()

# Funktion zur Berechnung des 95%-Konfidenzintervalls über Bootstrap
def bootstrap_confidence_interval(data, stat_function=np.median, n_bootstrap=1000, ci=95):
    bootstrapped_stats = [
        stat_function(np.random.choice(data, size=len(data), replace=True)) for _ in range(n_bootstrap)
    ]
    lower_bound = np.percentile(bootstrapped_stats, (100 - ci) / 2)
    upper_bound = np.percentile(bootstrapped_stats, 100 - (100 - ci) / 2)
    return lower_bound, upper_bound

# Berechnung des Konfidenzintervalls für jede C_star-Gruppe
confidence_intervals = {}
for c_star, group in cleaned_data.groupby('C_star'):
    ci_lower, ci_upper = bootstrap_confidence_interval(group['Beeinflusste_Knoten'])
    confidence_intervals[c_star] = (ci_lower, ci_upper)

# Plot erstellen
fig, ax = plt.subplots(figsize=(12, 8))

# Plot der Konfidenzintervalle für jede C_star
for i, (c_star, (ci_lower, ci_upper)) in enumerate(confidence_intervals.items()):
    ax.plot([i, i], [ci_lower, ci_upper], color='blue', linewidth=4)  # Konfidenzintervall als Linie
    ax.scatter([i], [ci_lower], color='blue', zorder=5)  # Untere Grenze
    ax.scatter([i], [ci_upper], color='blue', zorder=5)  # Obere Grenze

# Achsen und Titel anpassen
ax.set_xlabel('C_star', fontsize=12)
ax.set_ylabel('Beeinflusste Knoten (95% CI)', fontsize=12)
ax.set_title('95% Konfidenzintervall für die Anzahl der Beeinflussten Knoten', fontsize=14)

# X-Achse anpassen: Wenn C_star viele Werte hat, kann man die Beschriftungen drehen
ax.set_xticks(range(len(confidence_intervals)))
ax.set_xticklabels(confidence_intervals.keys(), rotation=45, ha='right', fontsize=12)

# Raster hinzufügen
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Diagramm anzeigen
plt.tight_layout()
plt.show()
