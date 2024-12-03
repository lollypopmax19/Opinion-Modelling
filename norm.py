import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read files
file_path = 'csv_files/Beeinflusste_knoten.csv'
data = pd.read_csv(file_path, sep=',')
file_path2 = 'csv_files/ModSimAuswertungComp.csv'
data2 = pd.read_csv(file_path2, sep=';')

# Select relevant columns and remove missing values
cleaned_data = data[['C_Star', 'Beeinflusste_Knoten']].dropna()
cleaned_data2 = data2[['C_Star', 'Cost']].dropna()

# Group by C_Star and calculate the mean
grouped_influenced = cleaned_data.groupby('C_Star').mean()
grouped_cost = cleaned_data2.groupby('C_Star').mean()

# Normalize values to the range [0, 1]
max_influenced = grouped_influenced['Beeinflusste_Knoten'].max()
max_cost = grouped_cost['Cost'].max()

grouped_influenced['Normalized'] = grouped_influenced['Beeinflusste_Knoten'] / max_influenced
grouped_cost['Normalized'] = grouped_cost['Cost'] / max_cost

# Create plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot normalized data
ax.plot(grouped_influenced.index, grouped_influenced['Normalized'], marker='o', linestyle='-', color='blue', label='Influenced Nodes')
ax.plot(grouped_cost.index, grouped_cost['Normalized'], marker='o', linestyle='-', color='green', label='Cost')

# Customize axes and title
ax.set_xlabel('Connectivity', fontsize=12)
ax.set_ylabel('Normalized Values', fontsize=12)
ax.set_title('Normalized Values of Influenced Nodes and Cost', fontsize=14)

# Add legend and grid
ax.legend(fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Show plot
plt.tight_layout()
plt.show()
