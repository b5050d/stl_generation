import numpy as np

from matplotlib import pyplot as plt


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


def generate_stl_walls(edge, floor_height, ceiling_height):
    """
    Generate the walls of the STL from the edges.
    """

    first_loop = True
    for i in range(len(edge)):
        a = edge[i]
        b = edge[(i + 1) % len(edge)]

        t1 = np.array(
            [
                [a[0], a[1], floor_height],
                [b[0], b[1], floor_height],
                [a[0], a[1], ceiling_height],
            ]
        )

        t2 = np.array(
            [
                [b[0], b[1], floor_height],
                [b[0], b[1], ceiling_height],
                [a[0], a[1], ceiling_height],
            ]
        )
        new_triangles = np.array([t1, t2])

        if first_loop:
            triangles = new_triangles
            first_loop = False
        else:
            triangles = np.concatenate((triangles, new_triangles), axis=0)

    return triangles


if __name__ == "__main__":
    edge = np.array([[1, 0], [3, 0], [4, 2], [3, 4], [1, 4], [0, 2]])

    floor_height = 0
    ceiling_height = 5

    walls = generate_stl_walls(edge, floor_height, ceiling_height)

    plot_triangles(walls)
