"""
The purpose of these methods is to start from a binary matrix and end up with a list of edges
"""

import numpy as np
import cv2


def check_8_neighbors(matrix: np.ndarray, i: int, j: int):
    """
    Returns the 8 neighbors of a given point in a matrix in CW order starting from up
    """
    # Must go in CW Order starting from up
    rows, cols = matrix.shape
    neighbors = []
    # Up
    if i > 0:
        neighbors.append(matrix[i - 1, j])
    # Upper right
    if i > 0 and j < cols - 1:
        neighbors.append(matrix[i - 1, j + 1])
    # Right
    if j < cols - 1:
        neighbors.append(matrix[i, j + 1])
    # Lower Right
    if i < rows - 1 and j < cols - 1:
        neighbors.append(matrix[i + 1, j + 1])
    # Down
    if i < rows - 1:
        neighbors.append(matrix[i + 1, j])
    # Lower Left
    if i < rows - 1 and j > 0:
        neighbors.append(matrix[i + 1, j - 1])
    # Left
    if j > 0:
        neighbors.append(matrix[i, j - 1])
    # Upper Left
    if i > 0 and j > 0:
        neighbors.append(matrix[i - 1, j - 1])
    return neighbors


def recreate_shape_from_counts(count_matrix: np.ndarray):
    threshold = 3
    result_matrix = np.where(count_matrix < threshold, 1, 0)
    return result_matrix


def create_count_matrix(matrix: np.ndarray):
    OCCUPIED = 0
    rows, cols = matrix.shape
    count_matrix = np.zeros((rows, cols), dtype=int)
    for i in range(rows):
        for j in range(cols):
            current = matrix[i, j]
            if current == OCCUPIED:
                neighbors = check_8_neighbors(matrix, i, j)
                score = neighbors.count(OCCUPIED)
                count_matrix[i, j] = score
    return count_matrix


def final_hollowing(count_matrix: np.ndarray):
    result_matrix = np.where((count_matrix >= 4) & (count_matrix <= 6), 0, 1)
    return result_matrix


def hollow_out_shapes(matrix: np.ndarray):
    """
    Removes the inner parts of shapes in a binary matrix
    # The strategy is to look for neighbors
    # who are also 0 (meaning they are the shape)

    """
    # copy the matrix
    last_matrix = matrix.copy()
    working_matrix = matrix.copy()

    # Need to repeat until there are no changes
    while True:
        # Count the number of neighbors for each point
        count_matrix = create_count_matrix(last_matrix)

        working_matrix = recreate_shape_from_counts(count_matrix)
        if np.array_equal(working_matrix, last_matrix):
            break
        last_matrix = working_matrix

    count_matrix = create_count_matrix(working_matrix)

    # Now need to get rid of threes and 8s and such
    working_matrix = final_hollowing(count_matrix)
    return working_matrix


def collect_edges(matrix: np.ndarray):
    """
    Should find all of the edges in a hollowed out
    shape
    """
    # Assuming the matrix is in the 1/0 format from earlier
    matrix = np.where(matrix == 1, 255, 0)
    matrix = matrix.astype(np.uint8)
    inverted = cv2.bitwise_not(matrix)
    contours, hierarchy = cv2.findContours(
        inverted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )

    result = []
    for contour in contours:
        result.append(contour.reshape(-1, 2))
    return result


def scale_edges(edges: list, scalar: int):
    """
    Scales the edges by a given factor
    """
    assert scalar in [2, 4, 8, 16, 32, 64, 128, 256], "Invalid scale factor"
    scaled_edges = []
    for edge in edges:
        scaled_edge = edge * scalar
        scaled_edges.append(scaled_edge)
    return scaled_edges


def smoothing_routine_1(edges: list):
    """
    Smoothing routine 1

    The idea here is that every point should just be the average of its neighbors

    no values should not be an integer
    """
    new_edges = []
    for edge in edges:
        new_edge = np.copy(edge)
        for i in range(len(edge)):
            if i == len(edge) - 1:
                # We are at the end
                before = edge[i - 1]
                after = edge[0]
            elif i == 0:
                before = edge[-1]
                after = edge[i + 1]
            else:
                before = edge[i - 1]
                after = edge[i + 1]

            new_edge[i] = np.mean((before, after), axis=0)
        new_edges.append(new_edge)
    return new_edges


def drop_points_on_edges(edges, factor: int = 2):
    new_edges = []
    for edge in edges:
        new_edges.append(edge[::factor])
    return new_edges


if __name__ == "__main__":
    sample_edges = [
        np.array([[0, 0], [16, 0], [16, 16], [32, 16], [32, 32]]),
    ]

    ans = smoothing_routine_1(sample_edges)
    print(ans)
    # input_matrix = np.array([
    #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #     [1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1],
    #     [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    #     [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    #     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    #     [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    #     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #     [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    # ])
    # sample_matrix = np.array(
    #     [
    #         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #         [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    #         [1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
    #         [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    #         [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    #         [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    #         [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    #         [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    #         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #     ],
    #     dtype=np.uint8,
    # )

    # edges = collect_edges(sample_matrix)
    # print(edges)
    # plot_image_matrix(input_matrix)

    # output_matrix = hollow_out_shapes(input_matrix)
    # plot_image_matrix(output_matrix)
