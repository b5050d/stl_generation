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
    plt.scatter(edge_array[:, 0], edge_array[:, 1])
    # plt.gca().invert_yaxis()       # match image coords (optional)
    if actually_plot:
        plt.show()


def plot_triangles(triangles):
    """
    Plot the triangles in 3D.
    """

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    for triangle in triangles:
        # input(triangle)
        for point in triangle:
            # input(point)
            x = point[0]
            y = point[1]
            z = point[2]
            print(f"Point: {point}, x: {x}, y: {y}, z: {z}")
            ax.scatter(x, y, z, color="b")

        ax.plot(
            [triangle[0, 0], triangle[1, 0]],
            [triangle[0, 1], triangle[1, 1]],
            [triangle[0, 2], triangle[1, 2]],
            color="blue",
        )
        ax.plot(
            [triangle[1, 0], triangle[2, 0]],
            [triangle[1, 1], triangle[2, 1]],
            [triangle[1, 2], triangle[2, 2]],
            color="red",
        )
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()


def plot_stl_triangles(triangles):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    for triangle in triangles:
        A = triangle[0]
        B = triangle[1]
        C = triangle[2]

        ax.plot([A[0], B[0]], [A[1], B[1]], [A[2], B[2]], color="blue")
        ax.plot([B[0], C[0]], [B[1], C[1]], [B[2], C[2]], color="red")
        ax.plot([C[0], A[0]], [C[1], A[1]], [C[2], A[2]], color="green")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()
