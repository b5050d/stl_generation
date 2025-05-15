"""
The purpose of these methods is to start from a binary matrix and end up with a list of edges
"""

import numpy as np


def hollow_out_shapes(matrix: np.ndarray):
    """
    Removes the inner parts of shapes in a binary matrix
    """
    rows, cols = matrix.shape

    for i in range(rows):
        for j in range(cols):
            current = matrix[i, j]
            if current == 1:
                # Check up
                if i > 0:
                    if matrix[i-1, j] == 0:
                        matrix[i, j] = 0
                # Check right
                if j < cols - 1:
                    if matrix[i, j+1] == 0:
                        matrix[i, j] = 0
                # Check down
                if i < rows - 1:
                    if matrix[i+1, j] == 0:
                        matrix[i, j] = 0
                # Check left
                if j > 0:
                    if matrix[i, j-1] == 0:
                        matrix[i, j] = 0
                