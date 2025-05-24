from stl_generation.stl_generation import generate_stl_walls

import numpy as np


def test_generate_stl_walls():
    edge = np.array([[1, 0], [3, 0], [4, 2], [3, 4], [1, 4], [0, 2]])

    floor_height = 0
    ceiling_height = 5

    walls = generate_stl_walls(edge, floor_height, ceiling_height)

    assert len(walls) == 12, "There should be 12 triangles"
    for triangle in walls:
        assert triangle.shape == (3, 3), "Each triangle should have 3 vertices"
        assert len(triangle) == 3, "Each triangle should have 3 vertices"
        for vertex in triangle:
            assert len(vertex) == 3, "Each vertex should have 3 coordinates (x, y, z)"
            assert vertex[2] in [
                floor_height,
                ceiling_height,
            ], "Z coordinate should be either floor_height or ceiling_height"
