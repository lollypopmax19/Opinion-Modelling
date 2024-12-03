import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem

# Daten laden
file_path = "csv_files\Beeinflusste_knoten.csv"  # Passen Sie den Pfad an
data = pd.read_csv(file_path)

# Daten nach C_star gruppieren und Statistik berechnen
grouped = data.groupby('C_star')['Beeinflusste Knoten']

# Mittelwerte und Konfidenzintervalle berechnen
means = grouped.mean()
conf_intervals = grouped.apply(lambda x: (np.mean(x) - 1.96 * sem(x), np.mean(x) + 1.96 * sem(x)))

# Untere und obere Grenzen des Konfidenzintervalls extrahieren
lower_bounds = conf_intervals.apply(lambda x: x[0])
upper_bounds = conf_intervals.apply(lambda x: x[1])

# Plot erstellen
plt.figure(figsize=(10, 6))
plt.plot(means.index, means, label="Mittlere Anzahl beeinflusster Knoten", color="blue", marker="o")
plt.fill_between(means.index, lower_bounds, upper_bounds, color="blue", alpha=0.2, label="95% Konfidenzintervall")

# Plot dekorieren
plt.title("Einfluss von $C^*$ auf beeinflusste Knoten", fontsize=14)
plt.xlabel("$C^*$", fontsize=12)
plt.ylabel("Beeinflusste Knoten", fontsize=12)
plt.legend()
plt.grid(alpha=0.4)
plt.show()
