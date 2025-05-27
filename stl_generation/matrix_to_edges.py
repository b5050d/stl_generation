"""
The purpose of these methods is to start from a binary matrix and end up with a list of edges
"""

import numpy as np
import cv2

# import seaborn as sns
# from matplotlib import pyplot as plt

from stl_generation.utils.plotting import plot_image_matrix


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


def filter_sharp_edges(matrix: np.ndarray):
    """
    This uses a similar method to the hollowing but does not hollow
    """
    # needed to fix the duplicate points issue

    # Basically we are taking in an array with 255 is the shape and 0 is the background
    # we want everything that only has 1 neighbor to be romved
    OCCUPIED = 255
    rows, cols = matrix.shape
    count_matrix = np.zeros((rows, cols), dtype=int)
    for i in range(rows):
        for j in range(cols):
            current = matrix[i, j]
            if current == OCCUPIED:
                neighbors = check_8_neighbors(matrix, i, j)
                score = neighbors.count(OCCUPIED)
                count_matrix[i, j] = score

    ans = np.where(count_matrix > 2, 255, 0)

    return ans.astype(np.uint8)


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


def immediate_neighbor_linear_smoothing(edge):
    """
    The idea here is that every point should just be the average of its neighbors

    no values should not be an integer
    """
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
    return new_edge


def drop_points_on_edge(edge, factor: int = 2):
    return edge[::factor]


def get_unit_vector(p1, p2):
    """
    Compute the unit vector from point p1 to point p2.

    Parameters:
        p1 (array-like): Starting point (x1, y1)
        p2 (array-like): Ending point (x2, y2)

    Returns:
        numpy.ndarray: A 2D unit vector pointing from p1 to p2
    """
    v = p2 - p1
    norm = np.linalg.norm(v)
    if norm == 0:
        raise ValueError("Cannot compute unit vector for zero-length vector")
    return v / norm


def remove_any_duplicate_points(point_array):
    seen = set()
    cleaned_points = []
    for pt in point_array:
        t = tuple(pt)
        if t not in seen:
            seen.add(t)
            cleaned_points.append(pt)
    return np.array(cleaned_points)


def remove_useless_points_on_edge(edge):
    """
    Drops points that do not provide any new information
    """
    new_edge = []
    for i in range(len(edge)):
        current_point = edge[i]
        if i == 0:
            last_point = edge[-1]
        else:
            last_point = edge[i - 1]
        if i == len(edge) - 1:
            next_point = edge[0]
        else:
            next_point = edge[i + 1]

        assert not np.array_equal(last_point, current_point), "Error, repeated point"
        assert not np.array_equal(current_point, next_point), "Error, repeated point"
        assert not np.array_equal(last_point, next_point), "Error, repeated point"

        a = get_unit_vector(last_point, current_point)
        b = get_unit_vector(current_point, next_point)
        if np.array_equal(a, b):
            pass
        else:
            new_edge.append(current_point)

    return np.array(new_edge)


def find_closest_points(edge1, edge2):
    """
    Finds the closest points between two edges
    """
    min_so_far = ()
    min_distance = float("inf")
    checked = {}
    for point1 in edge1:
        for point2 in edge2:
            if (tuple(point1), tuple(point2)) in checked:
                # If we have already checked this pair, skip it
                continue
            elif (tuple(point2), tuple(point1)) in checked:
                # If we have already checked this pair in reverse, skip it
                continue
            # Calculate the distance between the two points
            distance = np.linalg.norm(point1 - point2)
            checked[(tuple(point1), tuple(point2))] = distance

            if distance < min_distance:
                min_distance = distance
                min_so_far = (tuple(point1), tuple(point2))

    # convert back to something that makes sense
    min_so_far = np.array(min_so_far)
    assert min_so_far.shape == (2, 2), "Expected shape to be (2, 2)"
    return min_so_far


def np_index(array, target):
    """
    A version of .index (for lists) that works with numpy arrays.

    Returns the index of the first occurrence of target in array.
    """
    matches = np.all(array == target, axis=1)
    index = np.where(matches)[0]
    return index[0]


def create_single_edge_from_shape_in_shape(edge1, edge2):
    """
    Creates a single edge from an edge that has another shape inside it.
    """

    closest_points = find_closest_points(
        edge1, edge2
    )  # Ensure the closest points are calculated

    index1 = np_index(edge1, closest_points[0])
    index2 = np_index(edge2, closest_points[1])

    new_list = edge1[:index1]
    new_list = np.concatenate((new_list, closest_points), axis=0)
    new_list = np.concatenate((new_list, edge2[:index2][::-1]), axis=0)
    new_list = np.concatenate((new_list, edge2[index2 + 1 :][::-1]), axis=0)
    new_list = np.concatenate((new_list, closest_points[::-1]), axis=0)
    new_list = np.concatenate((new_list, edge1[index1 + 1 :]), axis=0)

    assert new_list.shape[1] == 2, "Expected shape to be (N, 2)"
    return new_list


def gen_circle(center_point, radius, num_points):
    """
    Generate a list of 2D points representing a circle.

    Parameters:
        center_point (tuple or array-like): (x, y) center of the circle.
        radius (float): Radius of the circle.
        num_points (int): Number of points to generate.

    Returns:
        numpy.ndarray: Array of shape (num_points, 2), each row a 2D point on the circle.
    """
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = center_point[0] + radius * np.cos(angles)
    y = center_point[1] + radius * np.sin(angles)
    return np.stack((x, y), axis=-1)


def get_outer_contour_as_edge(shape: np.ndarray):
    """
    Returns the outer contour of a shape as an edge
    """
    contours, _ = cv2.findContours(
        shape,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE,
    )
    if contours:
        return contours[0].reshape(-1, 2)
    return np.array([])


def edge_cleaning(edge):
    edge = drop_points_on_edge(edge)
    for i in range(1):
        edge = immediate_neighbor_linear_smoothing(edge)
    edge = drop_points_on_edge(edge)
    edge = remove_any_duplicate_points(edge)
    edge = remove_useless_points_on_edge(edge)
    return edge


def process_matrix(matrix):
    # SCALE_FACTOR = 256  # TODO - Define in a config or something

    # matrix = filter_sharp_edges(matrix) # This doesnt seem to be necessary

    plot_image_matrix(matrix)

    original_shape = matrix.copy()

    # How do we know how much to blur???
    # if we lock at 300 300, then 12 equates to a blur
    # of 6, meaning we get about 2 mm of blur, which is good
    intermediate_kernel = np.ones((12, 12), np.uint8)
    intermediate_shape = cv2.dilate(original_shape, intermediate_kernel, iterations=1)

    original_edge = get_outer_contour_as_edge(original_shape)
    intermediate_edge = get_outer_contour_as_edge(intermediate_shape)

    original_edge = edge_cleaning(original_edge)
    intermediate_edge = edge_cleaning(intermediate_edge)

    # Scale the EDGES
    # original_edge = original_edge * SCALE_FACTOR
    # intermediate_edge = intermediate_edge * SCALE_FACTOR

    # Now we can generate the circles for the shape
    centroid = np.mean(intermediate_edge, axis=0)

    distances = np.linalg.norm(intermediate_edge - centroid, axis=1)
    furthest_index = np.argmax(distances)
    furthest_point = intermediate_edge[furthest_index]
    print("Furthest point:", furthest_point)

    radius = np.linalg.norm(furthest_point - centroid)
    print("Radius:", radius)
    numpoints = 32
    big_circ = gen_circle(centroid, int(radius * 1.2), 32)
    lil_circ = gen_circle(centroid, int(radius * 1.05), 32)
    assert len(big_circ) == numpoints, "Expected 64 points in the circle"
    return original_edge, intermediate_edge, big_circ, lil_circ


if __name__ == "__main__":
    pass
    # inner_edge = np.array([[4, 3], [5, 4], [4, 5], [3, 4]])
    # outer_edge = np.array([[3, 1], [5, 1], [7, 4], [5, 7], [3, 7], [1, 4]])

    # combined_edge = create_single_edge_from_shape_in_shape(outer_edge, inner_edge)

    # print(combined_edge)

    # combined_edge = np.array(
    #     [[3, 1][5, 1][7, 4][5, 4][4, 3][3, 4][4, 5][5, 4][7, 4][5, 7][3, 7][1, 4]]
    # )

    # sample_edges = [
    #     np.array([[0, 0], [16, 0], [16, 16], [32, 16], [32, 32]]),
    # ]

    # ans = smoothing_routine_1(sample_edges)
    # print(ans)
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
