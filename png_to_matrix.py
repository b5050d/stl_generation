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
    return image

def convert_matrix_to_binary(matrix: np.ndarray, cutoff: int):
    """
    Converts a grayscale matrix to a binary matrix
    """
    assert cutoff >= 0 and cutoff <= 255, "Cutoff must be between 0 and 255"
    return matrix > cutoff


if __name__ == "__main__":
    png_path = "images/c.png"
    matrix = load_png_to_gray_matrix(png_path)
    print(matrix)
    print(type(matrix))
    plt.imshow(matrix, cmap='gray')
    plt.show()

    