"""
The purpose of these methods is to start from a binary matrix and end up with a list of edges
"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# for dev only
from utils.plotting import plot_image_matrix

def check_8_neighbors(matrix: np.ndarray, i: int, j: int):
    """
    Returns the 8 neighbors of a given point in a matrix in CW order starting from up
    """
    # Must go in CW Order starting from up
    rows, cols = matrix.shape
    neighbors = []
    # Up
    if i > 0: 
        neighbors.append(matrix[i-1, j])
    # Upper right
    if i > 0 and j < cols - 1:
        neighbors.append(matrix[i-1, j+1])
    # Right
    if j < cols - 1:
        neighbors.append(matrix[i, j+1])
    # Lower Right
    if i < rows - 1 and j < cols - 1:
        neighbors.append(matrix[i+1, j+1])
    # Down
    if i < rows - 1:
        neighbors.append(matrix[i+1, j])
    # Lower Left
    if i < rows - 1 and j > 0:
        neighbors.append(matrix[i+1, j-1])
    # Left
    if j > 0:
        neighbors.append(matrix[i, j-1])
    # Upper Left
    if i > 0 and j > 0:
        neighbors.append(matrix[i-1, j-1])
    return neighbors

def recreate_shape_from_counts(count_matrix: np.ndarray):
    threshold = 3
    result_matrix = np.where(count_matrix < threshold, 1, 0)
    return result_matrix
    
def create_count_matrix(matrix: np.ndarray):
    EMPTY = 1
    OCCUPIED = 0
    rows, cols = matrix.shape
    count_matrix = np.zeros((rows, cols), dtype=int)
    for i in range(rows):
        for j in range(cols):
            current = matrix[i, j]
            if current == OCCUPIED:
                neighbors = check_8_neighbors(matrix, i, j)
                score = neighbors.count(OCCUPIED)
                count_matrix[i,j] = score
    return count_matrix

def hollow_out_shapes(matrix: np.ndarray):
    """
    Removes the inner parts of shapes in a binary matrix
    # The strategy is to look for neighbors
    # who are also 0 (meaning they are the shape)

    """
    EMPTY = 1
    OCCUPIED = 0

    rows, cols = matrix.shape

    # copy the matrix
    last_matrix = matrix.copy()
    working_matrix = matrix.copy()

    # Need to repeat until there are no changes
    while True:
        # Count the number of neighbors for each point
        count_matrix = create_count_matrix(last_matrix)

        sns.heatmap(count_matrix, annot=True, fmt='d', cmap='YlGnBu')
        plt.title('Heatmap with Values')
        plt.show()

        working_matrix = recreate_shape_from_counts(count_matrix)
        if np.array_equal(working_matrix, last_matrix):
            break
        last_matrix = working_matrix


    # sns.heatmap(empty_matrix, annot=True, fmt='d', cmap='YlGnBu')
    # plt.title('Heatmap with Values')
    # plt.show()

    # plot_image_matrix(working_matrix)
    return working_matrix

    # for i in range(rows):
    #     for j in range(cols):
    #         current = matrix[i, j]
    #         if current == OCCUPIED:
    #             score = 0
    #             # Check up
    #             if i > 0:
    #                 if matrix[i-1, j] == OCCUPIED:
    #                     score += 1
    #             # Check right
    #             if j < cols - 1:
    #                 if matrix[i, j+1] == OCCUPIED:
    #                     score += 1
    #             # Check down
    #             if i < rows - 1:
    #                 if matrix[i+1, j] == OCCUPIED:
    #                     score += 1
    #             # Check left
    #             if j > 0:
    #                 if matrix[i, j-1] == OCCUPIED:
    #                     score += 1
    #             if score == 4 or score == 1:
    #                 empty_matrix[i, j] = EMPTY
    #             else:
    #                 empty_matrix[i, j] = matrix[i, j]
    # plot_image_matrix(empty_matrix)
    # return empty_matrix

if __name__ == "__main__":
    input_matrix = np.array([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ])
    plot_image_matrix(input_matrix)

    output_matrix = hollow_out_shapes(input_matrix)
    plot_image_matrix(output_matrix)
