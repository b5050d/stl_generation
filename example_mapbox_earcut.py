import mapbox_earcut as earcut
import numpy as np
import matplotlib.pyplot as plt

# Define the polygon's vertices
vertices = np.array([
    [0.0, 0.0],
    [2.0, 0.0],
    [2.0, 2.0],
    [1.0, 3.0],
    [0.0, 2.0]
], dtype=np.float64)

# Define the rings array
rings = np.array([len(vertices)], dtype=np.uint32)

# Perform triangulation
indices = earcut.triangulate_float64(vertices, rings)

# Plotting the result
for i in range(0, len(indices), 3):
    triangle = vertices[indices[i:i+3]]
    plt.fill(*zip(*triangle), alpha=0.4, edgecolor='black')

# Plot original polygon outline
px, py = zip(*vertices)
plt.plot(px + (px[0],), py + (py[0],), 'r--')
plt.scatter(px, py, color='red')
plt.gca().set_aspect('equal')
plt.title("Triangulated Polygon (mapbox_earcut)")
plt.show()
