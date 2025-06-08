"""
Bringing everything together for something functional here

"""

# Handle imports
from stl_generation.modules.png_to_matrix import load_and_process_byte_stream

from stl_generation.modules.matrix_to_edges import (
    process_matrix,
)

from stl_generation.modules.stl_generation import (
    write_triangles_to_io_buffer,
)

from stl_generation.modules.cookie_cutter_shape_collector import (
    build_cookie_cutter_triangles,
)


def cookie_cutter(buffer_data):
    """
    Generate STL from buffer
    """
    matrix = load_and_process_byte_stream(buffer_data)

    original_edge, intermediate_edge, big_circle, little_circle = process_matrix(matrix)

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

    # Fix the STL Scaling...
    triangles = triangles / 3

    # write triangles to stl
    response = write_triangles_to_io_buffer(triangles)

    return response
