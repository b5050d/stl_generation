import numpy as np

# Sample 2D matrix
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

rows, cols = matrix.shape

# Loop through each element
for i in range(rows):
    for j in range(cols):
        current = matrix[i, j]
        print(f"Current: matrix[{i},{j}] = {current}")

        # Check up
        if i > 0:
            print(f"  Up: {matrix[i-1, j]}")

        # Check right
        if j < cols - 1:
            print(f"  Right: {matrix[i, j+1]}")

        # Check down
        if i < rows - 1:
            print(f"  Down: {matrix[i+1, j]}")

        # Check left
        if j > 0:
            print(f"  Left: {matrix[i, j-1]}")
