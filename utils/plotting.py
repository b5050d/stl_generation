import numpy as np
from matplotlib import pyplot as plt

def plot_image_matrix(matrix: np.ndarray):
    """
    Plots a grayscale matrix
    """
    plt.imshow(matrix, cmap='gray')
    plt.show()

