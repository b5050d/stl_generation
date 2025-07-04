"""
Bringing everything together for something functional here

"""

# Handle imports
from modules.png_to_matrix import load_and_process_image
from utils.plotting import (
    plot_image_matrix,
    # plot_edge_array,
    plot_stl_triangles,
)
from modules.matrix_to_edges import (
    process_matrix,
)
from modules.stl_generation import (
    write_triangles_to_stl,
)

from modules.cookie_cutter_shape_collector import (
    build_cookie_cutter_triangles,
)

import os
import pickle


if __name__ == "__main__":
    currdir = os.path.dirname(__file__)
    png_path = "images/dot.png"
    # png_path = "images/too_big_tree.png"
    png_path = "images/maple_leaf.png"
    # png_path = "images/a_solid.png"
    png_path = "images/maple_leaf_small.png"
    png_path = "images/teige2.png"
    png_path = currdir + "/images/hawaii.png"
    # png_path = "images/sun_2.png"
    # png_path = "images/sun_3.png"
    # NOTE: In order to process the sun images, I will need to filter the shape at the start after making binary. Similar to how I was doing the hollowing
    # png_path = "images/usa.png"
    # png_path = "images/bunny.png"
    # png_path = "images/tiny_pepper.png"
    # png_path = "images/giraffe.png"
    # png_path = "images/sasquatch.png"
    # png_path = "images/buddha.png"
    # png_path = "images/butterfly.png"
    # png_path = "images/manatee.png"

    # Now we need to load in the image
    matrix = load_and_process_image(png_path)
    if False:
        plot_image_matrix(matrix)

    # Now we need to collect edges from the image
    # ans = process_matrix(matrix)
    # plot_image_matrix(ans)
    original_edge, intermediate_edge, big_circle, little_circle = process_matrix(matrix)

    # plot_edge_array(original_edge, False)
    # plot_edge_array(big_circle, False)
    # plot_edge_array(little_circle, False)
    # plot_edge_array(intermediate_edge, True)

    # Now we need to get all the trianges
    slope_height = 6 * 3  # * 256  # TODO - move 256 to a config file or something
    cut_height = 12 * 3  # * 256
    triangles = build_cookie_cutter_triangles(
        original_edge,
        intermediate_edge,
        big_circle,
        little_circle,
        slope_height,
        cut_height,
    )

    triangles = triangles / 3

    if False:
        plot_stl_triangles(triangles, True)

    # Save the triangles for test purposes
    print(triangles[0:4])
    print(len(triangles))
    print(type(triangles))

    with open("data.pkl", "wb") as f:
        pickle.dump(triangles, f)
    input("Trianbges")

    # Now we can save the triangles to a stl file
    desired_path = "generated_stl/test.stl"
    write_triangles_to_stl(desired_path, triangles)
