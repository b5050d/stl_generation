"""
Bringing everything together for something functional here

"""

# Handle imports
from stl_generation.png_to_matrix import (
    load_and_process_image,
)
from stl_generation.utils.plotting import (
    plot_image_matrix,
    plot_edge_array,
    plot_stl_triangles,
)
from stl_generation.matrix_to_edges import (
    process_matrix,
)
from stl_generation.stl_generation import (
    write_triangles_to_stl,
)

from stl_generation.cookie_cutter_shape_collector import build_cookie_cutter_triangles

if __name__ == "__main__":
    png_path = "images/dot.png"
    # png_path = "images/too_big_tree.png"
    png_path = "images/maple_leaf.png"
    # png_path = "images/a_solid.png"

    # Now we need to load in the image
    matrix = load_and_process_image(png_path)
    if False:
        plot_image_matrix(matrix)

    # Now we need to collect edges from the image
    # ans = process_matrix(matrix)
    # plot_image_matrix(ans)
    original_edge, intermediate_edge, big_circle, little_circle = process_matrix(matrix)

    plot_edge_array(original_edge, False)
    plot_edge_array(big_circle, False)
    plot_edge_array(little_circle, False)
    plot_edge_array(intermediate_edge, True)

    # Now we need to get all the trianges
    slope_height = 6 * 256  # TODO - move 256 to a config file or something
    cut_height = 12 * 256
    triangles = build_cookie_cutter_triangles(
        original_edge,
        intermediate_edge,
        big_circle,
        little_circle,
        slope_height,
        cut_height,
    )

    if False:
        plot_stl_triangles(triangles, True)

    # Now we can save the triangles to a stl file
    desired_path = "generated_stl/test.stl"
    write_triangles_to_stl(desired_path, triangles)
