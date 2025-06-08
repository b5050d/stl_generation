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


def pad_to_360(matrix, color=255):
    padding0 = int((360 - matrix.shape[0]) / 2)
    padding1 = int((360 - matrix.shape[1]) / 2)
    return np.pad(
        matrix,
        ((padding0, padding0), (padding1, padding1)),
        mode="constant",
        constant_values=color,
    )


def load_and_process_image(png_path):
    matrix = load_png_to_gray_matrix(png_path)

    matrix = pad_to_360(matrix)

    matrix = convert_matrix_to_binary(matrix, 128)

    # invert so white is our shape and black is the background
    matrix = 255 - matrix

    return matrix.astype(np.uint8)


def load_byte_stream_to_gray_matrix(data):
    nparr = np.frombuffer(data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    # Force the matrix to be 300x300
    image = cv2.resize(image, (300, 300))

    assert np.max(image) != np.min(image), "Error, no information in image!"
    return image


def get_edge_values(arr):
    """
    Given a 2D NumPy array, return a list of all the values on its edge.
    """
    top = arr[0, :]
    bottom = arr[-1, :]
    left = arr[1:-1, 0]
    right = arr[1:-1, -1]

    edge_values = np.concatenate([top, right, bottom[::-1], left[::-1]])
    return edge_values.tolist()


def detect_edge_color(data):
    """
    Given a 2D NumPy array, find the edge color (but if there is no single
    color present on the edge, it will error out)
    """
    edge_values = get_edge_values(data)
    data_max = max(edge_values)
    data_min = min(edge_values)
    assert data_max == data_min, "Error, not a clean shape in the image"
    return data_max


def load_and_process_byte_stream(data):
    """
    Load and process the byte stream into a matrix
    """
    matrix = load_byte_stream_to_gray_matrix(data)

    # Forcing to cut off at 128
    matrix = convert_matrix_to_binary(matrix, 128)

    # Get the edges of the matrix
    color = detect_edge_color(matrix)
    if color == 0:
        pass
    else:
        # invert so white is our shape and black is the background
        matrix = 255 - matrix

    # Pad to 360 for ease of edge collection
    matrix = pad_to_360(matrix, color=0)

    return matrix.astype(np.uint8)


if __name__ == "__main__":
    png_path = "images/c.png"
    matrix = load_png_to_gray_matrix(png_path)
    print(matrix)
    print(type(matrix))
    plt.imshow(matrix, cmap="gray")
    plt.show()
