"""
Script to test out the dilation of shapes and the collection of edges
"""

from stl_generation.png_to_matrix import (
    load_png_to_gray_matrix,
    # convert_matrix_to_binary,
    pad_matrix,
)
from stl_generation.utils.plotting import (
    plot_image_matrix,
    plot_edge_array,
)
from stl_generation.matrix_to_edges import (
    # hollow_out_shapes,
    # collect_edges,
    smoothing_routine_1,
    scale_edges,
    drop_points_on_edges,
    create_single_edge_from_shape_in_shape,
    # find_closest_points,
    # np_index,
)
from stl_generation.tesselation import (
    tesselate,
)

from stl_generation.stl_generation import (
    is_ccw,
)

from matplotlib import pyplot as plt
import cv2
import numpy as np

if __name__ == "__main__":
    png_path = "images/dot.png"
    png_path = "images/star.png"
    matrix = load_png_to_gray_matrix(png_path)
    matrix = pad_matrix(matrix, 0.1)

    plot_image_matrix(matrix)

    # invert (white should indicate the shape)
    matrix = 255 - matrix
    # plot_image_matrix(matrix)

    # 20 pixels per cm
    pix_per_cm = 20
    scale_up = 256
    pix_per_cm = pix_per_cm * scale_up

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

    def simple_edge_filtering(edges):
        edges = scale_edges(edges, 256)

        edges = smoothing_routine_1(edges)
        edges = drop_points_on_edges(edges, 2)
        edges = smoothing_routine_1(edges)
        edges = drop_points_on_edges(edges, 2)

        return edges

    edges = [original_edge, intermediate_edge, extreme_edge]
    edges = simple_edge_filtering(edges)

    combined_edge_cutting = create_single_edge_from_shape_in_shape(edges[0], edges[1])

    combined_edge_holding = create_single_edge_from_shape_in_shape(edges[0], edges[2])

    plot_edge_array(combined_edge_cutting, False)
    plot_edge_array(combined_edge_holding, False)

    assert is_ccw(combined_edge_cutting), "The cutting edge should be counter-clockwise"
    assert is_ccw(combined_edge_holding), "The holding edge should be counter-clockwise"

    # Alright generating the walls

    plt.show()

    tesselated_cutting = tesselate(combined_edge_cutting, True)
    tesselated_holding = tesselate(combined_edge_holding, True)
