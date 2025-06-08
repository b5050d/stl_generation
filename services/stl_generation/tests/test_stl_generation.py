from stl_generation.modules.stl_generation import (
    generate_stl_walls,
    compute_inward_normals,
    is_ccw,
    generate_triangles_from_tesselation,
    # generate_triangles_for_slope,
    generate_sloped_walls,
    compute_3d_norm,
    write_triangles_to_stl,
    write_triangles_to_io_buffer,
)
import os
import pickle
import numpy as np
import io


# def test_generate_stl_walls():
#     edge = np.array([[1, 0], [3, 0], [4, 2], [3, 4], [1, 4], [0, 2]])

#     floor_height = 0
#     ceiling_height = 5

#     walls = generate_stl_walls(edge, floor_height, ceiling_height)

#     assert len(walls) == 12, "There should be 12 triangles"
#     for triangle in walls:
#         assert triangle.shape == (3, 3), "Each triangle should have 3 vertices"
#         assert len(triangle) == 3, "Each triangle should have 3 vertices"
#         for vertex in triangle:
#             assert len(vertex) == 3, "Each vertex should have 3 coordinates (x, y, z)"
#             assert vertex[2] in [
#                 floor_height,
#                 ceiling_height,
#             ], "Z coordinate should be either floor_height or ceiling_height"


def test_is_ccw():
    edge = np.array([[1, 0], [3, 0], [4, 2], [3, 4], [1, 4], [0, 2]])
    ans = is_ccw(edge)

    assert ans, "The edge should be counter-clockwise"

    edge = np.array(
        [
            [2, 2],
            [3, 4],
            [4, 2],
        ]
    )
    ans = is_ccw(edge)
    assert not ans, "The edge should be counter-clockwise"


def test_compute_inward_normals():
    edge = np.array(
        [
            [2, 1],
            [3, 2],
            [2, 3],
        ]
    )

    normals = compute_inward_normals(edge)
    assert len(normals) == 3, "There should be 3 normals"
    expected_normals = np.array([[-1, 1], [-1, -1], [1, 0]])

    assert np.array_equal(
        normals, expected_normals
    ), "Normals do not match expected values"


def test_generate_triangles_from_tesselation():
    edge = np.array([[1, 0], [3, 0], [4, 2], [3, 4], [1, 4], [0, 2]])

    # tesselated_indices = tesselate(edge, plot=True)
    tesselated_indices = np.array([4, 5, 0, 0, 1, 2, 2, 3, 4, 4, 0, 2])

    ans = generate_triangles_from_tesselation(
        indices=tesselated_indices, edge=edge, floor_or_ceiling="floor", roof_height=0
    )

    assert len(ans) == 4
    for a in ans:
        for i in range(1, 4):
            assert a[i, 2] == 0, "Z coordinate should be 0 for ceiling triangles"
        assert a.shape == (4, 3), "Each triangle should have 3 vertices and a norm"
        assert np.array_equal(
            a[0], np.array([0, 0, -1])
        ), "The normal vector should be [0, 0, -1] for floor triangles"

    ans = generate_triangles_from_tesselation(
        indices=tesselated_indices,
        edge=edge,
        floor_or_ceiling="ceiling",
        roof_height=4,
    )
    assert len(ans) == 4
    for a in ans:
        for i in range(1, 4):
            assert a[i, 2] == 4, "Z coordinate should be 4 for ceiling triangles"
        assert a.shape == (4, 3), "Each triangle should have 3 vertices and a norm"
        assert np.array_equal(
            a[0], np.array([0, 0, 1])
        ), "The normal vector should be [0, 0, -1] for floor triangles"


def test_compute_3d_norm():
    A = np.array([0, 0, 0])
    B = np.array([1, 0, 0])
    C = np.array([0, 1, 0])

    normal = compute_3d_norm(A, B, C)
    assert normal.shape == (3,), "Normal should be a 3D vector"
    assert np.array_equal(
        normal, [0, 0, 1]
    ), "The normal should be [0, 0, 1] for the given triangle"

    A = np.array([0, 0, 0])
    B = np.array([1, 0, 0])
    C = np.array([0, 1, 0])

    normal = compute_3d_norm(A, B, C)
    assert normal.shape == (3,), "Normal should be a 3D vector"
    assert np.array_equal(
        normal, [0, 0, 1]
    ), "The normal should be [0, 0, 1] for the given triangle"


def test_generate_sloped_walls():
    outer_shape = np.array(
        [
            [0, 0],
            [3, 0],
            [3, 3],
            [0, 3],
        ]
    )
    inner_shape = np.array(
        [
            [1, 1],
            [2, 1],
            [2, 2],
            [1, 2],
        ]
    )

    lower_height = 0
    upper_height = 3

    ans = generate_sloped_walls(outer_shape, inner_shape, lower_height, upper_height)

    assert len(ans) == 8
    assert ans.shape == (8, 4, 3)
    for t in ans:
        for p in t[1:]:
            assert p[2] in [0, 3]


def test_generate_stl_walls():
    outer_shape = np.array(
        [
            [0, 0],
            [3, 0],
            [3, 3],
            [0, 3],
        ]
    )

    ans = generate_stl_walls(outer_shape, 0, 5, "inner")
    assert len(ans) == 8


def test_write_triangles_to_stl(tmp_path):
    to_save = str(tmp_path) + "\\test.stl"

    currdir = os.path.dirname(__file__)
    with open(currdir + "\\test_hawaii_triangles.pkl", "rb") as f:
        data = pickle.load(f)

    write_triangles_to_stl(to_save, data)

    assert os.path.exists(to_save)


def test_write_triangles_to_io_buffer():
    currdir = os.path.dirname(__file__)
    with open(currdir + "\\test_hawaii_triangles.pkl", "rb") as f:
        data = pickle.load(f)

    ans = write_triangles_to_io_buffer(data)
    assert type(ans) is io.BytesIO


# def test_generate_triangles_for_slope():
#     indices = np.array([0, 1, 2, 2, 3, 0])
#     edge = np.array([[1, 0], [3, 0], [4, 2], [3, 4], [1, 4], [0, 2]])
#     inner_edge = np.array(
#         [[1.5, 0.5], [2.5, 0.5], [3.5, 1.5], [2.5, 3.5], [1.5, 3.5], [0.5, 1.5]]
#     )
#     outer_edge = np.array([[0, 0], [4, 0], [4, 4], [0, 4]])
#     roof_height = 6

#     triangles = generate_triangles_for_slope(
#         indices, edge, inner_edge, outer_edge, roof_height
#     )

#     assert len(triangles) == len(indices) // 3
#     for triangle in triangles:
#         assert triangle.shape == (3, 3), "Each triangle should have 3 vertices"
