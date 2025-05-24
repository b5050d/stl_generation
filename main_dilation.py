# Alright so what


from stl_generation.png_to_matrix import (
    load_png_to_gray_matrix,
    # convert_matrix_to_binary,
    pad_matrix,
)
from stl_generation.utils.plotting import (
    # plot_image_matrix,
    plot_edge_array,
)
from stl_generation.matrix_to_edges import (
    # hollow_out_shapes,
    # collect_edges,
    smoothing_routine_1,
    scale_edges,
    drop_points_on_edges,
)
from stl_generation.tesselation import tesselate

from matplotlib import pyplot as plt
import cv2
import numpy as np

if __name__ == "__main__":
    png_path = "images/dot.png"
    png_path = "images/star.png"
    matrix = load_png_to_gray_matrix(png_path)
    matrix = pad_matrix(matrix, 0.1)

    # plot_image_matrix(matrix)

    # invert (white should indicate the shape)
    matrix = 255 - matrix
    # plot_image_matrix(matrix)

    # todo we need to scale the image in real units to understand
    # how much we should dilate the shape, for now we dont care

    # Alright now lets blur the shape...
    original_shape = matrix.copy()

    # # Threshold the image to binary
    # _, binary_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

    # # Define kernel and dilate
    # kernel = np.ones((3, 3), np.uint8)
    # dilated_img = cv2.dilate(binary_img, kernel, iterations=1)

    intermediate_kernel = np.ones((15, 15), np.uint8)
    intermediate_shape = cv2.dilate(original_shape, intermediate_kernel, iterations=1)

    extreme_kernel = np.ones((40, 40), np.uint8)
    extreme_shape = cv2.dilate(intermediate_shape, extreme_kernel, iterations=1)

    # plot_image_matrix(intermediate_shape)
    # plot_image_matrix(extreme_shape)

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

    empty_matrix = np.zeros_like(original_shape)

    # Alright cool lets collect all the edges now

    original_edge = get_outer_contour_as_edge(original_shape)
    intermediate_edge = get_outer_contour_as_edge(intermediate_shape)
    extreme_edge = get_outer_contour_as_edge(extreme_shape)

    # plot_edge_array(original_edge, False)
    # plot_edge_array(intermediate_edge, False)
    # plot_edge_array(extreme_edge, False)
    # plt.show()

    def simple_edge_filtering(edges):
        edges = scale_edges(edges, 256)

        edges = smoothing_routine_1(edges)
        edges = drop_points_on_edges(edges, 2)
        edges = smoothing_routine_1(edges)
        edges = drop_points_on_edges(edges, 2)

        return edges

    edges = [original_edge, intermediate_edge, extreme_edge]
    edges = simple_edge_filtering(edges)

    # plot_edge_array(edges[0], False)
    # plot_edge_array(edges[1], False)
    # plot_edge_array(edges[2], False)
    # plt.show()

    # Now we need to find the closest points between the edges

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

        # closest_points = []
        # for point in edge1:
        #     distances = np.linalg.norm(edge2 - point, axis=1)
        #     closest_index = np.argmin(distances)
        #     closest_points.append(edge2[closest_index])
        # return np.array(closest_points)

    closest_points_cutting = find_closest_points(edges[0], edges[1])
    print(closest_points_cutting)
    closest_points_holding = find_closest_points(edges[0], edges[2])
    print(closest_points_holding)

    # plot_edge_array(edges[0], False)
    # plot_edge_array(edges[1], False)
    # plot_edge_array(closest_points, False)
    # # plot_edge_array(edges[2], False)
    # plt.show()

    def np_index(array, target):
        matches = np.all(array == target, axis=1)
        index = np.where(matches)[0]
        return index[0]

    def create_single_edge_from_shape_in_shape(edge1, edge2, closest_points):
        """
        Creates a single edge from a shape in shape
        """
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

    combined_edge_cutting = create_single_edge_from_shape_in_shape(
        edges[0], edges[1], closest_points_cutting
    )

    combined_edge_holding = create_single_edge_from_shape_in_shape(
        edges[0], edges[2], closest_points_holding
    )

    plot_edge_array(combined_edge_cutting, False)
    plot_edge_array(combined_edge_holding, False)
    plt.show()

    tesselated_cutting = tesselate(combined_edge_cutting, True)
    tesselated_holding = tesselate(combined_edge_holding, True)
