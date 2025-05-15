import os
import pytest
import numpy as np
import cv2

from src.matrix.png_to_matrix import (
    load_png_to_gray_matrix,
    convert_matrix_to_binary
)

# Create a test image for consistent testing
def create_test_image(filename='test_image.png', size=(100, 100)):
    test_image = np.random.randint(0, 256, size=size, dtype=np.uint8)
    cv2.imwrite(filename, test_image)
    return filename

def test_load_png_to_matrix_success():
    # Create a test image
    test_image_path = create_test_image()
    
    try:
        # Load the image
        matrix = load_png_to_gray_matrix(test_image_path)
        
        # Check matrix is numpy array
        assert isinstance(matrix, np.ndarray), 'Result should be a numpy array'
        
        # Check matrix dimensions
        assert matrix.shape == (100, 100), 'Matrix should match test image dimensions'
        
        # Check matrix is grayscale (2D)
        assert len(matrix.shape) == 2, 'Matrix should be 2D (grayscale)'
        
        # Check pixel values are within valid range
        assert matrix.min() >= 0 and matrix.max() <= 255, 'Pixel values should be between 0 and 255'
    
    finally:
        # Clean up test image
        os.remove(test_image_path)

def test_load_png_to_matrix_invalid_path():
    # Test handling of invalid image path
    with pytest.raises(Exception):
        load_png_to_gray_matrix('non_existent_image.png')


def test_convert_matrix_to_binary_oob_input():
    # Test handling of bad input
    with pytest.raises(Exception):
        convert_matrix_to_binary(np.array([[0, 1, 2], [3, 4, 5]]), 256)
    with pytest.raises(Exception):
        convert_matrix_to_binary(np.array([[0, 1, 2], [3, 4, 5]]), -1)

def test_convert_matrix_to_binary():
    # Test handling of invalid image path
    ans = convert_matrix_to_binary(np.array([[0, 50, 100], [150, 200, 255]]), 101)
    assert ans.shape == (2, 3), 'Matrix should match test image dimensions'
    assert ans.min() == 0 and ans.max() == 1, 'Matrix should be binary'
    assert (ans == np.array([[0, 0, 0], [1, 1, 1]])).all(), 'Matrix should be binary'


def test_pad_image_matrix():
    starting_array = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    