from stl_generation.modules.matrix_to_edges import (
    create_single_edge_from_shape_in_shape,
)
from stl_generation.modules.tesselation import (
    tesselate,
)
from stl_generation.modules.stl_generation import (
    ensure_ccw,
    generate_triangles_from_tesselation,
    generate_sloped_walls,
    generate_stl_walls,
)

import numpy as np

# from stl_generation.utils.plotting import plot_stl_triangles


def build_cookie_cutter_triangles(
    original_edge,
    intermediate_edge,
    big_circle,
    little_circle,
    slope_height,
    cut_height,
):
    original_edge = ensure_ccw(original_edge)
    little_circle = ensure_ccw(little_circle)
    big_circle = ensure_ccw(big_circle)
    intermediate_edge = ensure_ccw(intermediate_edge)

    ############################################################
    # GET SHAPE 1 : Cut shape + big circ
    ############################################################
    base_edge = create_single_edge_from_shape_in_shape(big_circle, original_edge)
    base_tesselation = tesselate(base_edge, False)
    # TOOD - free some of the memory
    base_shape = generate_triangles_from_tesselation(
        base_tesselation, base_edge, "floor", 0
    )
    # plot_stl_triangles(base_shape, False)

    ############################################################
    # GET SHAPE 2: Outerslope (big circ to lil circ)
    ############################################################
    slope_shape = generate_sloped_walls(big_circle, little_circle, 0, slope_height)
    # plot_stl_triangles(slope_shape, False)

    ############################################################
    # GET SHAPE 3: Inner walls (Original shape)
    ############################################################
    inner_walls_shape = generate_stl_walls(original_edge, 0, cut_height)

    # plot_stl_triangles(inner_walls_shape, False)

    ############################################################
    # GET SHAPE 4: Falt surface (Dilated Cut + lil circ)
    ############################################################
    face_edge = create_single_edge_from_shape_in_shape(little_circle, intermediate_edge)
    face_tesselation = tesselate(face_edge, False)
    face_shape = generate_triangles_from_tesselation(
        face_tesselation, face_edge, "ceiling", slope_height
    )
    # plot_stl_triangles(face_shape, False)

    ############################################################
    # GET SHAPE 5: Outer walls of cutting element
    ############################################################
    outer_walls_shape = generate_stl_walls(
        intermediate_edge, slope_height, cut_height, "outer"
    )
    # plot_stl_triangles(outer_walls_shape, False)

    ############################################################
    # GET SHAPE 6: Top surface of cutting element
    ############################################################
    top_edge = create_single_edge_from_shape_in_shape(intermediate_edge, original_edge)
    top_tesselation = tesselate(top_edge, False)
    top_shape = generate_triangles_from_tesselation(
        top_tesselation, top_edge, "ceiling", cut_height
    )
    # plot_stl_triangles(top_shape, True)

    ############################################################
    # Alright so now we need to make our STL file
    ############################################################
    # collect all the triangles
    collected_triangles = base_shape.copy()
    collected_triangles = np.concatenate(
        (
            base_shape,
            slope_shape,
            inner_walls_shape,
            face_shape,
            outer_walls_shape,
            top_shape,
        ),
        axis=0,
    )
    assert len(collected_triangles) == len(base_shape) + len(slope_shape) + len(
        inner_walls_shape
    ) + len(face_shape) + len(outer_walls_shape) + len(top_shape)
    print(collected_triangles.shape)

    return collected_triangles
