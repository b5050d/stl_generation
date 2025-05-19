

import pytest





def test_tesselation():
    sample_shape = np.array([
        [0, 0],
        [1, 0],
        [1, 1],
        [0, 1]
    ])
    ans = tesselate(sample_shape)
    assert ans.shape == (2, 3)
    