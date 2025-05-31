"""
Test script for the methods in tesselation.py
"""

# import pytest
import numpy as np

from stl_generation.modules.tesselation import tesselate


def test_tesselation():
    sample_shape = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])

    ans = tesselate(sample_shape)

    assert len(ans) == 2 * 3
    for item in ans:
        assert item >= 0
        assert item < len(ans)
        for i in range(0, len(ans), 3):
            a = ans[i]
            b = ans[i + 1]
            c = ans[i + 2]

            assert a != b
            assert a != c
            assert b != c
