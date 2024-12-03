import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

class LinearDecayModel:
    def __init__(self, max_edges):
        """
        Initialize the model with the maximum number of edges.
        
        :param max_edges: Maximum number of edges
        """
        self.maxEdges = max_edges

    def linear_function(self, edge_count):
        """
        Calculate the value of the linear function y(edgeCount).
        
        :param edge_count: Current number of edges
        :return: Computed value y(edgeCount)
        """
        _m = (0.5 - 0.1) / (1.0 - self.maxEdges)
        return _m * (edge_count - 1.0) + 0.5

    def plot_model(self, edge_count):
        """
        Visualize the linear function and the corresponding normal distribution curve.
        
        :param edge_count: The current parameter to be visualized.
        """
        if edge_count < 1 or edge_count > self.maxEdges:
            raise ValueError("edge_count must be between 1 and maxEdges.")
        
        # Calculate values for the linear function
        x_vals = np.linspace(1, self.maxEdges, 500)
        y_vals = self.linear_function(x_vals)
        
        # Determine the current y-value
        y_edge = self.linear_function(edge_count)
        
        # Calculate the normal distribution
        x_normal = np.linspace(-3, 3, 500)
        y_normal = norm.pdf(x_normal, loc=0, scale=y_edge)  # Mean 0, σ = y_edge
        
        # Create the plot with 3:2 aspect ratio
        fig, ax = plt.subplots(2, 1, figsize=(9, 6))  # Width 9, Height 6 for 3:2 ratio
        
        # 1. Plot the linear function
        ax[0].plot(x_vals, y_vals, label='Linear Function: y(edgeCount)')
        ax[0].scatter([edge_count], [y_edge], color='red', label=f'Current Value: edgeCount={edge_count}, y={y_edge:.2f}')
        ax[0].set_title('Linear Decay Function')
        ax[0].set_xlabel('edgeCount')
        ax[0].set_ylabel('y(edgeCount)')
        ax[0].legend()
        ax[0].grid(True)
        
        # 2. Plot the normal distribution
        ax[1].plot(x_normal, y_normal, label=f'Normal Distribution: σ={y_edge:.2f}')
        ax[1].set_title('Normal Distribution (Mean 0)')
        ax[1].set_xlabel('x')
        ax[1].set_ylabel('Density')
        ax[1].legend()
        ax[1].grid(True)
        
        # Format the y-axis ticks with two decimal places
        ax[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}'))

        plt.tight_layout()
        plt.show()

# Example: Initialize the model and visualize
max_edges = 20  # Maximum number of edges
model = LinearDecayModel(max_edges)

# Step-by-step visualization
for edge_count in range(1, max_edges + 1, 1):  # Step size 1
    model.plot_model(edge_count)
