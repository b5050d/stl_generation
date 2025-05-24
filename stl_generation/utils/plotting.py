import numpy as np
from matplotlib import pyplot as plt


def plot_image_matrix(matrix: np.ndarray):
    """
    Plots a grayscale matrix
    """
    plt.imshow(matrix, cmap="gray")
    plt.gca().invert_yaxis()  # match image coords (optional)
    plt.show()


def plot_edge_array(edge_array: np.ndarray, actually_plot: bool = True):
    # edge arrays are of shape (len, 2)

    plt.plot(edge_array[:, 0], edge_array[:, 1], "r-")
    # plt.gca().invert_yaxis()       # match image coords (optional)
    if actually_plot:
        plt.show()
