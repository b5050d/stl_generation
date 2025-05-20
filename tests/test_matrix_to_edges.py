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
