# from stl_generation.png_to_matrix import (
#     load_png_to_gray_matrix,
#     # convert_matrix_to_binary,
#     pad_matrix,
# )
# from stl_generation.utils.plotting import (
#     # plot_image_matrix,
#     # plot_edge_array,
#     plot_stl_triangles,
# )
# from stl_generation.matrix_to_edges import (
#     create_single_edge_from_shape_in_shape,
#     # scale_edges,
#     immediate_neighbor_linear_smoothing,
#     drop_points_on_edge,
#     # remove_any_duplicate_points,
#     remove_useless_points_on_edge,
#     gen_circle,
# )
# from stl_generation.tesselation import (
#     tesselate,
# )

# # from stl_generation.stl_generation import (
# #     # is_ccw,
# # )
# from stl_generation.stl_generation import (
#     generate_triangles_from_tesselation,
#     # generate_triangles_for_slope,
#     generate_stl_walls,
#     generate_sloped_walls,
#     write_triangles_to_stl,
#     ensure_ccw,
#     convert_float_to_ieee754_bin,
#     split_4_bytes_into_4_uint8s,
# )

# # from stl_generation.utils.plotting import plot_stl_triangles

# from matplotlib import pyplot as plt
# import cv2
# import numpy as np

# if __name__ == "__main__":
#     # inner_edge = np.array([
#     #     [4, 3],
#     #     [5, 4],
#     #     [4, 5],
#     # #     [3, 4]
#     # # ])
#     # # outer_edge = np.array([
#     # #     [3, 1],
#     # #     [5, 1],
#     # #     [7, 4],
#     # #     [5, 7],
#     # #     [3, 7],
#     # #     [1, 4]
#     # # ])

#     # # combined_edge = np.array([
#     # #     [3, 1],
#     # #     [5, 1],
#     # #     [7, 4],
#     # #     [5, 4],
#     # #     [4, 3],
#     # #     [3, 4],
#     # #     [4, 5],
#     # #     [5, 4],
#     # #     [7, 4],
#     # #     [5, 7],
#     # #     [3, 7],
#     # #     [1, 4],
#     # # ])

#     # # indices = np.array([11, 0, 1, 1, 2, 3, 6, 7, 8, 8, 9, 10, 1, 3, 4, 6, 8, 10, 11, 1, 4, 5, 6, 10, 11, 4, 5, 5, 10, 11])

#     # # ans = generate_triangles_for_slope(
#     # #     indices,
#     # #     combined_edge,
#     # #     inner_edge,
#     # #     outer_edge,
#     # #     3
#     # # )

#     # # print(ans)

#     # # # Now we need to plot all these in 3D space
#     # # # for t in ans:
#     # # #     input(t)

#     # # plot_stl_triangles(ans)

#     # png_path = "images/dot.png"
#     # png_path = "images/star2.png"
#     # matrix = load_png_to_gray_matrix(png_path)
#     # matrix = pad_matrix(matrix, 0.1)

#     # # plot_image_matrix(matrix)

#     # # invert (white should indicate the shape)
#     # matrix = 255 - matrix
#     # # plot_image_matrix(matrix)

#     # # 20 pixels per cm
#     # pix_per_cm = 20
#     # scale_up = 256
#     # pix_per_cm = pix_per_cm * scale_up

#     # # todo we need to scale the image in real units to understand
#     # # how much we should dilate the shape, for now we dont care

#     # # Alright now lets blur the shape...
#     # original_shape = matrix.copy()

#     # # # Threshold the image to binary
#     # # _, binary_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

#     # # # Define kernel and dilate
#     # # kernel = np.ones((3, 3), np.uint8)
#     # # dilated_img = cv2.dilate(binary_img, kernel, iterations=1)

#     # intermediate_kernel = np.ones((10, 10), np.uint8)
#     # intermediate_shape = cv2.dilate(original_shape, intermediate_kernel, iterations=1)

#     # extreme_kernel = np.ones((40, 40), np.uint8)
#     # extreme_shape = cv2.dilate(intermediate_shape, extreme_kernel, iterations=1)

#     # # plot_image_matrix(intermediate_shape)
#     # # plot_image_matrix(extreme_shape)

#     # def get_outer_contour_as_edge(shape: np.ndarray):
#     #     """
#     #     Returns the outer contour of a shape as an edge
#     #     """
#     #     contours, _ = cv2.findContours(
#     #         shape,
#     #         cv2.RETR_EXTERNAL,
#     #         cv2.CHAIN_APPROX_NONE,
#     #     )
#     #     if contours:
#     #         return contours[0].reshape(-1, 2)
#     #     return np.array([])

#     # empty_matrix = np.zeros_like(original_shape)

#     # # Alright cool lets collect all the edges now

#     # original_edge = get_outer_contour_as_edge(original_shape)
#     # intermediate_edge = get_outer_contour_as_edge(intermediate_shape)
#     # extreme_edge = get_outer_contour_as_edge(extreme_shape)

#     # def experimental_edge_cleaning(edge):
#     #     edge = drop_points_on_edge(edge)
#     #     for i in range(1):
#     #         edge = immediate_neighbor_linear_smoothing(edge)
#     #     edge = drop_points_on_edge(edge)
#     #     edge = remove_useless_points_on_edge(edge)
#     #     return edge

#     # original_edge = experimental_edge_cleaning(original_edge)
#     # intermediate_edge = experimental_edge_cleaning(intermediate_edge)
#     # # extreme_edge = experimental_edge_cleaning(extreme_edge)

#     # # plot_edge_array(original_edge,True)
#     # # plot_edge_array(intermediate_edge,True)

#     # # Need to find the circular housing for the base
#     # centroid = np.mean(intermediate_edge, axis=0)

#     # # find the furthest point from the centroid
#     # distances = np.linalg.norm(intermediate_edge - centroid, axis=1)
#     # furthest_index = np.argmax(distances)
#     # furthest_point = intermediate_edge[furthest_index]
#     # print("Furthest point:", furthest_point)

#     # radius = np.linalg.norm(furthest_point - centroid)
#     # print("Radius:", radius)
#     # numpoints = 32
#     # big_circ = gen_circle(centroid, int(radius * 1.2), 32)
#     # big_circ = ensure_ccw(big_circ)  # Ensure the circle is counter-clockwise
#     # lil_circ = gen_circle(centroid, int(radius * 1.05), 32)
#     # lil_circ = ensure_ccw(lil_circ)  # Ensure the circle is counter-clockwise
#     # assert len(big_circ) == numpoints, "Expected 64 points in the circle"
#     # # plot_edge_array(big_circ, False)
#     # # plot_edge_array(intermediate_edge, False)
#     # # plt.plot(centroid[0], centroid[1], "bo")  # Plot the centroid
#     # # plot_edge_array(lil_circ, True)

#     # # plt.plot(furthest_point[0], furthest_point[1], "go")  # Plot the furthest point
#     # # # plot_edge_array(, True)
#     # # plt.show()

#     # # Alright now that we have a circle

#     # big_circ = ensure_ccw(big_circ)
#     # lil_circ = ensure_ccw(lil_circ)
#     # original_edge = ensure_ccw(original_edge)
#     # intermediate_edge = ensure_ccw(intermediate_edge)

#     # ############################################################
#     # # GET SHAPE 1 : Cut shape + big circ
#     # ############################################################
#     # base_edge = create_single_edge_from_shape_in_shape(big_circ, original_edge)
#     # base_tesselation = tesselate(base_edge, False)
#     # # TOOD - free some of the memory
#     # base_shape = generate_triangles_from_tesselation(
#     #     base_tesselation, base_edge, "floor", 0
#     # )
#     # # plot_stl_triangles(base_shape, False)

#     # ############################################################
#     # # GET SHAPE 2: Outerslope (big circ to lil circ)
#     # ############################################################
#     # slope_shape = generate_sloped_walls(big_circ, lil_circ, 0, 5)
#     # # plot_stl_triangles(slope_shape, False)

#     # ############################################################
#     # # GET SHAPE 3: Inner walls (Original shape)
#     # ############################################################
#     # inner_walls_shape = generate_stl_walls(original_edge, 0, 8)

#     # # plot_stl_triangles(inner_walls_shape, True)

#     # ############################################################
#     # # GET SHAPE 4: Falt surface (Dilated Cut + lil circ)
#     # ############################################################
#     # face_edge = create_single_edge_from_shape_in_shape(lil_circ, intermediate_edge)
#     # face_tesselation = tesselate(face_edge, False)
#     # face_shape = generate_triangles_from_tesselation(
#     #     face_tesselation, face_edge, "ceiling", 5
#     # )
#     # # plot_stl_triangles(face_shape, False)

#     # ############################################################
#     # # GET SHAPE 5: Outer walls of cutting element
#     # ############################################################
#     # outer_walls_shape = generate_stl_walls(intermediate_edge, 5, 8)
#     # # plot_stl_triangles(outer_walls_shape, False)

#     # ############################################################
#     # # GET SHAPE 6: Top surface of cutting element
#     # ############################################################
#     # top_edge = create_single_edge_from_shape_in_shape(intermediate_edge, original_edge)
#     # top_tesselation = tesselate(top_edge, False)
#     # top_shape = generate_triangles_from_tesselation(
#     #     top_tesselation, top_edge, "ceiling", 8
#     # )
#     # plot_stl_triangles(top_shape, True)

#     ############################################################
#     # Alright so now we need to make our STL file
#     ############################################################
#     # collect all the triangles
#     # collected_triangles = base_shape.copy()
#     # collected_triangles = np.concatenate(
#     #     (
#     #         base_shape,
#     #         slope_shape,
#     #         inner_walls_shape,
#     #         face_shape,
#     #         outer_walls_shape,
#     #         top_shape
#     #     ),
#     #     axis=0,
#     #     )

#     edge = np.array(
#         [
#             [1, 1],
#             [3, 1],
#             [3, 3],
#             [1, 3],
#         ]
#     )

#     # Generate the base shape
#     top_height = 1
#     base_tesselation = tesselate(edge)
#     base_shape = generate_triangles_from_tesselation(base_tesselation, edge, "floor", 0)

#     outer_shape = generate_stl_walls(edge, 0, top_height, "inner")

#     top_tesselation = tesselate(edge)
#     top_shape = generate_triangles_from_tesselation(
#         top_tesselation, edge, "ceiling", top_height
#     )

#     collected_triangles = np.concatenate(
#         (base_shape, outer_shape, top_shape),
#         axis=0,
#     )

#     collected_triangles = collected_triangles * 60

#     plot_stl_triangles(collected_triangles, True)

#     filepath = "sample.stl"
#     write_triangles_to_stl(filepath, collected_triangles)
