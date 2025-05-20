import triangle as tr
from triangle import plot
import matplotlib.pyplot as plt

# Define the polygon
points = [
    (0, 0),    # 0
    (2, 0),    # 1
    (2, 2),    # 2
    (1, 3),    # 3
    (0, 2)     # 4
]

# Define polygon edges
segments = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 0)
]

# Build input dictionary for triangulation
A = {
    'vertices': points,
    'segments': segments
}

# Perform constrained Delaunay triangulation
t = tr.triangulate(A, 'p')  # 'p' = preserve segments

# Plot
plot.plot(plt, **t)
plt.gca().set_aspect('equal')
plt.title("Triangulated Pentagon")
plt.show()
