import os
import pytest
import numpy as np
import cv2

from stl_generation.modules.png_to_matrix import (
    load_png_to_gray_matrix,
    convert_matrix_to_binary,
    pad_matrix,
    pad_to_360,
    get_edge_values,
    load_and_process_byte_stream,
    detect_edge_color,
)


# Create a test image for consistent testing
def create_test_image(filename="test_image.png", size=(100, 100)):
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
        assert isinstance(matrix, np.ndarray), "Result should be a numpy array"

        # Check matrix dimensions
        # TODO specify the file size in a config somewhere
        assert matrix.shape == (300, 300), "Matrix should match specified dimensions"

        # Check matrix is grayscale (2D)
        assert len(matrix.shape) == 2, "Matrix should be 2D (grayscale)"

        # Check pixel values are within valid range
        assert (
            matrix.min() >= 0 and matrix.max() <= 255
        ), "Pixel values should be between 0 and 255"

    finally:
        # Clean up test image
        os.remove(test_image_path)


def test_load_png_to_matrix_invalid_path():
    # Test handling of invalid image path
    with pytest.raises(Exception):
        load_png_to_gray_matrix("non_existent_image.png")


def test_convert_matrix_to_binary_oob_input():
    # Test handling of bad input
    with pytest.raises(Exception):
        convert_matrix_to_binary(np.array([[0, 1, 2], [3, 4, 5]]), 256)
    with pytest.raises(Exception):
        convert_matrix_to_binary(np.array([[0, 1, 2], [3, 4, 5]]), -1)


def test_convert_matrix_to_binary():
    # Test handling of invalid image path
    ans = convert_matrix_to_binary(np.array([[0, 50, 100], [150, 200, 255]]), 101)
    assert ans.shape == (2, 3), "Matrix should match test image dimensions"
    assert ans.min() == 0 and ans.max() == 255, "Matrix should be binary"
    assert (
        ans == np.array([[0, 0, 0], [255, 255, 255]])
    ).all(), "Matrix should be binary"


def test_pad_image_matrix():
    starting_array = np.ones((100, 100), dtype=int)
    padded_array = pad_matrix(starting_array, 0.1)
    assert padded_array.shape == (120, 120), "Matrix should match test image dimensions"
    assert (
        padded_array[10:110, 10:110] == starting_array
    ).all(), "Matrix should match test image dimensions"
    assert padded_array[0, 0] == 255
    assert padded_array[119, 119] == 255

    padded_array = pad_matrix(starting_array, 0.2)
    assert padded_array.shape == (140, 140), "Matrix should match test image dimensions"
    assert (
        padded_array[20:120, 20:120] == starting_array
    ).all(), "Matrix should match test image dimensions"
    assert padded_array[0, 0] == 255
    assert padded_array[139, 139] == 255


def test_pad_to_360():
    starting_array = np.ones((100, 100), dtype=int)
    padded_array = pad_to_360(starting_array)
    assert padded_array.shape == (360, 360)
    assert padded_array[0, 0] == 255
    assert padded_array[359, 359] == 255


def test_get_edge_values():
    sample_matrix = np.array(
        [
            [10, 14, 14, 13, 12],
            [1, 3, 5, 3, 11],
            [2, 5, 8, 5, 10],
            [3, 3, 5, 3, 9],
            [4, 5, 6, 7, 8],
        ]
    )

    ans = get_edge_values(sample_matrix)
    assert type(ans) is list

    assert np.min(ans) == 1
    assert np.max(ans) == 14


def test_detect_edge_color():
    sample_matrix = np.array(
        [
            [0, 0, 0, 0, 0],
            [0, 255, 255, 0, 0],
            [0, 0, 255, 0, 0],
            [0, 0, 255, 0, 0],
            [0, 0, 0, 255, 0],
            [0, 0, 0, 0, 0],
        ]
    )

    ans = detect_edge_color(sample_matrix)
    assert type(ans) is int
    assert ans == 0

    sample_matrix = np.array(
        [
            [255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255],
        ]
    )

    ans = detect_edge_color(sample_matrix)
    assert type(ans) is int
    assert ans == 255

    sample_matrix = np.array(
        [
            [255, 255, 255, 255, 255],
            [0, 255, 255, 255, 255],
            [255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255],
        ]
    )
    with pytest.raises(AssertionError):
        ans = detect_edge_color(sample_matrix)


def test_load_and_process_byte_stream():
    currdir = os.path.dirname(__file__)
    with open(currdir + "\\test_hawaii_white.bin", "rb") as f:
        data = f.read()

    matrix = load_and_process_byte_stream(data)
    assert type(matrix) is np.ndarray
    assert matrix.shape == (360, 360)
    ans = detect_edge_color(matrix)
    assert ans == 0

    with open(currdir + "\\test_hawaii_black.bin", "rb") as f:
        data = f.read()

    matrix = load_and_process_byte_stream(data)
    assert type(matrix) is np.ndarray
    assert matrix.shape == (360, 360)
    ans = detect_edge_color(matrix)
    assert ans == 0

    with open(currdir + "\\test_bad_border.bin", "rb") as f:
        data = f.read()

    with pytest.raises(AssertionError):
        matrix = load_and_process_byte_stream(data)

    with open(currdir + "\\test_hawaii_nonbinary.bin", "rb") as f:
        data = f.read()

    matrix = load_and_process_byte_stream(data)
    assert type(matrix) is np.ndarray
    assert matrix.shape == (360, 360)
    ans = detect_edge_color(matrix)
    assert ans == 0
