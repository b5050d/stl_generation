"""
"""
import pytest
import numpy as np

from stl_generation.matrix_to_edges import (
    hollow_out_shapes,
    check_8_neighbors,
    recreate_shape_from_counts,
    create_count_matrix,
    final_hollowing,
    collect_edges,
    scale_edges,
    immediate_neighbor_linear_smoothing,
    drop_points_on_edge,
    get_unit_vector,
    remove_any_duplicate_points,
    remove_useless_points_on_edge,
)

# from stl_generation.utils.plotting import plot_image_matrix


@pytest.fixture
def get_5x5_zeros_matrix():
    return np.zeros((5, 5), dtype=int)


@pytest.fixture
def get_3x3_in_5x5_matrix():
    return np.array(
        [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
        ]
    )


def test_check_8_neighbors(get_3x3_in_5x5_matrix):
    matrix = get_3x3_in_5x5_matrix
    assert check_8_neighbors(matrix, 1, 1) == [1, 1, 0, 0, 0, 1, 1, 1]
    assert check_8_neighbors(matrix, 1, 3) == [1, 1, 1, 1, 0, 0, 0, 1]
    assert check_8_neighbors(matrix, 2, 2) == [0] * 8


def test_recreate_shape_from_counts():
    count_matrix = np.array(
        [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
        ]
    )
    expected_matrix = np.array(
        [
            [1, 1, 1],
            [0, 0, 0],
            [0, 0, 0],
        ]
    )
    ans = recreate_shape_from_counts(count_matrix)
    assert np.array_equal(ans, expected_matrix)


def test_create_count_matrix(get_3x3_in_5x5_matrix):
    matrix = get_3x3_in_5x5_matrix
    count_matrix = create_count_matrix(matrix)
    expected_matrix = np.array(
        [
            [0, 0, 0, 0, 0],
            [0, 3, 5, 3, 0],
            [0, 5, 8, 5, 0],
            [0, 3, 5, 3, 0],
            [0, 0, 0, 0, 0],
        ]
    )
    assert np.array_equal(count_matrix, expected_matrix)


def test_final_hollowing():
    count_matrix = np.array(
        [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
        ]
    )
    expected_matrix = np.array(
        [
            [1, 1, 1],
            [1, 0, 0],
            [0, 1, 1],
        ]
    )
    ans = final_hollowing(count_matrix)
    assert np.array_equal(ans, expected_matrix)


def test_hollow_out_shapes(get_5x5_zeros_matrix, get_3x3_in_5x5_matrix):
    input_matrix = np.array(
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
    )

    expected_matrix = np.array(
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
    )

    hollowed_out = hollow_out_shapes(input_matrix)
    assert hollowed_out.shape == input_matrix.shape
    assert np.array_equal(hollowed_out, expected_matrix)


def test_collect_edges():
    sample_matrix = np.array(
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        dtype=np.uint8,
    )

    edges = collect_edges(sample_matrix)
    assert len(edges) == 1
    assert type(edges) is list
    assert type(edges[0]) is np.ndarray

    sample_matrix = np.array(
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1],
            [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        dtype=np.uint8,
    )

    edges = collect_edges(sample_matrix)
    assert len(edges) == 2
    assert type(edges) is list
    assert type(edges[0]) is np.ndarray
    assert type(edges[1]) is np.ndarray


def test_scale_edges():
    sample_edges = [
        np.array([[0, 0], [1, 0], [1, 1], [0, 1]]),
        np.array([[2, 2], [3, 2], [3, 3], [2, 3]]),
    ]
    scalar = 256
    scaled_edges = scale_edges(sample_edges, scalar)
    assert len(scaled_edges) == len(sample_edges)
    for i in range(len(sample_edges)):
        assert np.array_equal(scaled_edges[i], sample_edges[i] * scalar)


def test_immediate_neighbor_linear_smoothing():
    """
    What is smoothing routine 1?
    """
    edge0 = np.array([[0, 0], [16, 0], [16, 16], [32, 16], [32, 32]])
    expected_0 = np.array([[24, 16], [8, 8], [24, 8], [24, 24], [16, 8]])

    ans = immediate_neighbor_linear_smoothing(edge0)
    assert len(ans) == len(edge0)
    assert ans.shape == edge0.shape
    assert np.array_equal(ans, expected_0)

    edge1 = np.array([[128, 0], [0, 128], [128, 128]])
    expected_1 = np.array([[64, 128], [128, 64], [64, 64]])
    ans = immediate_neighbor_linear_smoothing(edge1)
    assert len(ans) == len(edge1)
    assert ans.shape == edge1.shape
    assert np.array_equal(ans, expected_1)


def test_drop_points_on_edges():
    edge0 = np.array([[0, 0], [16, 0], [16, 16], [32, 16], [32, 32]])
    ans = drop_points_on_edge(edge0)
    expected = np.array(
        [
            [0, 0],
            [16, 16],
            [32, 32],
        ]
    )
    assert np.array_equal(ans, expected)

    edge0 = np.array([[0, 0], [16, 0], [16, 16], [32, 16], [32, 32], [7, 7]])
    ans = drop_points_on_edge(edge0)
    assert np.array_equal(ans, expected)


def test_unit_vector():
    a = np.array([1, 1])
    b = np.array([2, 2])

    ans = get_unit_vector(a, b)

    assert np.allclose(ans, np.array([0.707, 0.707]), rtol=0.01, atol=0.01)


def test_remove_any_duplicate_points():
    edge0 = np.array(
        [
            [0, 0],
            [16, 0],
            [16, 16],
            [16, 16],
            [32, 16],
            [32, 32],
            [7, 7],
            [0, 0],
            [16, 0],
            [16, 0],
            [16, 0],
            [16, 0],
        ]
    )
    expected = np.array([[0, 0], [16, 0], [16, 16], [32, 16], [32, 32], [7, 7]])
    ans = remove_any_duplicate_points(edge0)
    assert np.array_equal(ans, expected)


def test_remove_useless_points_on_edge():
    edge0 = np.array(
        [
            [0, 0],
            [1, 0],
            [2, 0],
            [3, 0],
            [4, 0],
            [5, 2],
            [6, 4],
            [4, 5],
            [2, 6],
            [1, 3],
        ]
    )

    expected = np.array(
        [
            [0, 0],
            [4, 0],
            [6, 4],
            [2, 6],
        ]
    )

    ans = remove_useless_points_on_edge(edge0)
    assert np.array_equal(ans, expected)
