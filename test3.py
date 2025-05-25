from stl_generation.png_to_matrix import (
    load_png_to_gray_matrix,
    # convert_matrix_to_binary,
    pad_matrix,
)
from stl_generation.utils.plotting import (
    # plot_image_matrix,
    # plot_edge_array,
    plot_stl_triangles,
)
from stl_generation.matrix_to_edges import (
    create_single_edge_from_shape_in_shape,
    # scale_edges,
    immediate_neighbor_linear_smoothing,
    drop_points_on_edge,
    # remove_any_duplicate_points,
    remove_useless_points_on_edge,
    gen_circle,
)
from stl_generation.tesselation import (
    tesselate,
)

# from stl_generation.stl_generation import (
#     # is_ccw,
# )
from stl_generation.stl_generation import (
    generate_triangles_from_tesselation,
    # generate_triangles_for_slope,
    generate_stl_walls,
    generate_sloped_walls,
    ensure_ccw,
)

# from stl_generation.utils.plotting import plot_stl_triangles

# from matplotlib import pyplot as plt
import cv2
import numpy as np

if __name__ == "__main__":
    # inner_edge = np.array([
    #     [4, 3],
    #     [5, 4],
    #     [4, 5],
    #     [3, 4]
    # ])
    # outer_edge = np.array([
    #     [3, 1],
    #     [5, 1],
    #     [7, 4],
    #     [5, 7],
    #     [3, 7],
    #     [1, 4]
    # ])

    # combined_edge = np.array([
    #     [3, 1],
    #     [5, 1],
    #     [7, 4],
    #     [5, 4],
    #     [4, 3],
    #     [3, 4],
    #     [4, 5],
    #     [5, 4],
    #     [7, 4],
    #     [5, 7],
    #     [3, 7],
    #     [1, 4],
    # ])

    # indices = np.array([11, 0, 1, 1, 2, 3, 6, 7, 8, 8, 9, 10, 1, 3, 4, 6, 8, 10, 11, 1, 4, 5, 6, 10, 11, 4, 5, 5, 10, 11])

    # ans = generate_triangles_for_slope(
    #     indices,
    #     combined_edge,
    #     inner_edge,
    #     outer_edge,
    #     3
    # )

    # print(ans)

    # # Now we need to plot all these in 3D space
    # # for t in ans:
    # #     input(t)

    # plot_stl_triangles(ans)

    png_path = "images/dot.png"
    png_path = "images/star.png"
    matrix = load_png_to_gray_matrix(png_path)
    matrix = pad_matrix(matrix, 0.1)

    # plot_image_matrix(matrix)

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

    intermediate_kernel = np.ones((10, 10), np.uint8)
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

    def experimental_edge_cleaning(edge):
        edge = drop_points_on_edge(edge)
        for i in range(1):
            edge = immediate_neighbor_linear_smoothing(edge)
        edge = drop_points_on_edge(edge)
        edge = remove_useless_points_on_edge(edge)
        return edge

    original_edge = experimental_edge_cleaning(original_edge)
    intermediate_edge = experimental_edge_cleaning(intermediate_edge)
    # extreme_edge = experimental_edge_cleaning(extreme_edge)

    # plot_edge_array(original_edge,True)
    # plot_edge_array(intermediate_edge,True)

    # Need to find the circular housing for the base
    centroid = np.mean(intermediate_edge, axis=0)

    # find the furthest point from the centroid
    distances = np.linalg.norm(intermediate_edge - centroid, axis=1)
    furthest_index = np.argmax(distances)
    furthest_point = intermediate_edge[furthest_index]
    print("Furthest point:", furthest_point)

    radius = np.linalg.norm(furthest_point - centroid)
    print("Radius:", radius)
    numpoints = 32
    big_circ = gen_circle(centroid, int(radius * 1.2), 32)
    big_circ = ensure_ccw(big_circ)  # Ensure the circle is counter-clockwise
    lil_circ = gen_circle(centroid, int(radius * 1.05), 32)
    lil_circ = ensure_ccw(lil_circ)  # Ensure the circle is counter-clockwise
    assert len(big_circ) == numpoints, "Expected 64 points in the circle"
    # plot_edge_array(big_circ, False)
    # plot_edge_array(intermediate_edge, False)
    # plt.plot(centroid[0], centroid[1], "bo")  # Plot the centroid
    # plot_edge_array(lil_circ, True)

    # plt.plot(furthest_point[0], furthest_point[1], "go")  # Plot the furthest point
    # # plot_edge_array(, True)
    # plt.show()

    # Alright now that we have a circle

    big_circ = ensure_ccw(big_circ)
    lil_circ = ensure_ccw(lil_circ)
    original_edge = ensure_ccw(original_edge)
    intermediate_edge = ensure_ccw(intermediate_edge)

    ############################################################
    # GET SHAPE 1 : Cut shape + big circ
    ############################################################
    base_edge = create_single_edge_from_shape_in_shape(big_circ, original_edge)
    base_tesselation = tesselate(base_edge, False)
    # TOOD - free some of the memory
    base_shape = generate_triangles_from_tesselation(
        base_tesselation, base_edge, "floor", 0
    )
    # plot_stl_triangles(base_shape)

    ############################################################
    # GET SHAPE 2: Outerslope (big circ to lil circ)
    ############################################################
    slope_shape = generate_sloped_walls(big_circ, lil_circ, 0, 5)
    # plot_stl_triangles(slope_shape)

    ############################################################
    # GET SHAPE 3: Inner walls (Original shape)
    ############################################################
    inner_walls_shape = generate_stl_walls(original_edge, 0, 8)
    # plot_stl_triangles(inner_walls_shape)

    ############################################################
    # GET SHAPE 4: Falt surface (Dilated Cut + lil circ)
    ############################################################
    face_edge = create_single_edge_from_shape_in_shape(lil_circ, intermediate_edge)
    face_tesselation = tesselate(face_edge, False)
    face_shape = generate_triangles_from_tesselation(
        face_tesselation, face_edge, "ceiling", 5
    )
    # plot_stl_triangles(face_shape)

    ############################################################
    # GET SHAPE 5: Outer walls of cutting element
    ############################################################
    outer_walls_shape = generate_stl_walls(intermediate_edge, 5, 8)
    # plot_stl_triangles(outer_walls_shape)

    ############################################################
    # GET SHAPE 6: Top surface of cutting element
    ############################################################
    top_edge = create_single_edge_from_shape_in_shape(intermediate_edge, original_edge)
    top_tesselation = tesselate(top_edge, False)
    top_shape = generate_triangles_from_tesselation(
        top_tesselation, top_edge, "ceiling", 8
    )
    plot_stl_triangles(top_shape)

    # plot_edge_array(extreme_edge,True)

    # # ans = smoothing_routine_1(ans)
    # # input(ans)
    # # ans = drop_points_on_edges(ans)
    # # input(ans)

    # # ans = remove_useless_points_on_edges(ans)
    # # input(ans[0])
    # # plot_edge_array(ans[0], True)

    # # import sys

    # # sys.exit(1)
    # # input("kill")

    # # def simple_edge_filtering(edges):
    # #     edges = scale_edges(edges, 256)

    # #     edges = smoothing_routine_1(edges)
    # #     edges = drop_points_on_edges(edges, 2)
    # #     edges = smoothing_routine_1(edges)
    # #     edges = drop_points_on_edges(edges, 2)

    # #     edges = remove_useless_points_on_edges(edges, 2)

    # #     return edges

    # edges = [original_edge, intermediate_edge, extreme_edge]
    # # edges = simple_edge_filtering(edges)

    # # for e in edges:
    # #     plot_edge_array(e, False)
    # # plt.show()

    # # input("kill")

    # # combined_edge_cutting = create_single_edge_from_shape_in_shape(edges[0], edges[1])
    # # combined_edge_holding = create_single_edge_from_shape_in_shape(edges[0], edges[2])
    # # combined_edge_slope = create_single_edge_from_shape_in_shape(edges[1], edges[2])

    # # plot_edge_array(combined_edge_cutting, True)
    # # plot_edge_array(combined_edge_holding, False)
    # # plot_edge_array(combined_edge_slope, False)
    # # plt.show()

    # # Alright now we need to do something special for the slope

    # # Compute the centroid
    # centroid = np.mean(edges[1], axis=0)

    # print("Centroid:", centroid)

    # # find the furthest point from the centroid
    # distances = np.linalg.norm(edges[1] - centroid, axis=1)
    # furthest_index = np.argmax(distances)
    # furthest_point = edges[1][furthest_index]
    # print("Furthest point:", furthest_point)

    # radius = np.linalg.norm(furthest_point - centroid)
    # print("Radius:", radius)

    # def gen_circle(center_point, radius, num_points):
    #     """
    #     Generate a list of 2D points representing a circle.

    #     Parameters:
    #         center_point (tuple or array-like): (x, y) center of the circle.
    #         radius (float): Radius of the circle.
    #         num_points (int): Number of points to generate.

    #     Returns:
    #         numpy.ndarray: Array of shape (num_points, 2), each row a 2D point on the circle.
    #     """
    #     angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    #     x = center_point[0] + radius * np.cos(angles)
    #     y = center_point[1] + radius * np.sin(angles)
    #     return np.stack((x, y), axis=-1)

    # numpoints = 32
    # circ = gen_circle(centroid, int(radius * 1.2), 32)
    # circ = ensure_ccw(circ)  # Ensure the circle is counter-clockwise
    # assert len(circ) == numpoints, "Expected 64 points in the circle"
    # plot_edge_array(circ, False)
    # plot_edge_array(edges[0], False)  # Plot the original edge
    # plt.plot(centroid[0], centroid[1], "bo")  # Plot the centroid
    # plt.plot(furthest_point[0], furthest_point[1], "go")  # Plot the furthest point
    # plot_edge_array(edges[1], True)

    # comb_edge = create_single_edge_from_shape_in_shape(
    #     ensure_ccw(edges[1]), ensure_ccw(circ)
    # )
    # plot_edge_array(comb_edge, True)
    # plt.show()

    # tes = tesselate(comb_edge, True)

    # # Now

    # # now I need a list of pooints that form a circle. Should be 20

    # # tesselate_slope = tesselate(combined_edge_cutting, True)
    # # tesselate_slope = tesselate(combined_edge_slope, True)

    # # assert is_ccw(combined_edge_cutting), "The cutting edge should be counter-clockwise"
    # # assert is_ccw(combined_edge_holding), "The holding edge should be counter-clockwise"

    # # # Alright generating the walls

    # # plt.show()

    # # tesselated_cutting = tesselate(combined_edge_cutting, True)

    # # tesselated_holding = tesselate(combined_edge_holding, True)
