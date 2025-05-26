import numpy as np
import cv2
from matplotlib import pyplot as plt
import os


def load_png_to_gray_matrix(png_path: str):
    """
    Loads a png image into a grayscale matrix
    """
    assert os.path.exists(png_path), "File does not exist"
    image = cv2.imread(png_path, cv2.IMREAD_GRAYSCALE)

    # Force matrix to be 300x300
    image = cv2.resize(image, (300, 300))

    assert np.max(image) != np.min(image), "Error, no information in image!"
    return image


def convert_matrix_to_binary(matrix: np.ndarray, cutoff: int):
    """
    Converts a grayscale matrix to a binary matrix
    """
    assert cutoff >= 0 and cutoff <= 255, "Cutoff must be between 0 and 255"
    matrix = matrix > cutoff
    matrix = matrix * 255
    return matrix


def pad_matrix(matrix: np.ndarray, padding_percent: float):
    """
    Pads a matrix with 0's
    """
    assert (
        padding_percent >= 0 and padding_percent <= 1
    ), "Padding percent must be between 0 and 1"
    padding0 = int(matrix.shape[0] * padding_percent)
    padding1 = int(matrix.shape[1] * padding_percent)
    return np.pad(
        matrix,
        ((padding0, padding0), (padding1, padding1)),
        mode="constant",
        constant_values=255,
    )


def pad_to_360(matrix):
    padding0 = int((360 - matrix.shape[0]) / 2)
    padding1 = int((360 - matrix.shape[1]) / 2)
    return np.pad(
        matrix,
        ((padding0, padding0), (padding1, padding1)),
        mode="constant",
        constant_values=255,
    )


def load_and_process_image(png_path):
    matrix = load_png_to_gray_matrix(png_path)

    # matrix = pad_matrix(matrix, .1)
    matrix = pad_to_360(matrix)

    # TODO - display to user to make sure the scale is
    # correct and stuff

    # TODO - Query user on where to threshold the binary
    matrix = convert_matrix_to_binary(matrix, 128)

    # invert so white is our shape and black is the background
    matrix = 255 - matrix

    # Alright now we should ask the user how we want to scale
    # the image (actually I think that should get done later, when we have the points)

    return matrix.astype(np.uint8)


if __name__ == "__main__":
    png_path = "images/c.png"
    matrix = load_png_to_gray_matrix(png_path)
    print(matrix)
    print(type(matrix))
    plt.imshow(matrix, cmap="gray")
    plt.show()
