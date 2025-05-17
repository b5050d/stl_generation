
from matrix_to_edges import hollow_out_shapes


import pytest
import numpy as np

@pytest.fixture
def get_5x5_ones_matrix():
    return np.ones((5, 5), dtype=int)

@pytest.fixture
def get_3x3_in_5x5_matrix():
    return np.array([
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ])


def test_hollow_out_shapes(get_5x5_ones_matrix):
    mat5x5 = get_5x5_ones_matrix
    
    hollowed_out = hollow_out_shapes(mat5x5)
    
    expected = np.array([
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ])

    assert hollowed_out.shape == mat5x5.shape
    assert hollow
    