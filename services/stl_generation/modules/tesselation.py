import numpy as np
import mapbox_earcut as earcut
from matplotlib import pyplot as plt


def tesselate(shape: np.ndarray, plot=False):
    # Alright we need to tesselate a shape here

    # What form does mapbox_earcut need the shape in?
    # looks like numpy array of (x,2)

    assert shape.ndim == 2, "Shape must be a 2D array"

    # not sure why this is done
    rings = np.array([len(shape)], dtype=np.uint32)

    indices = earcut.triangulate_float64(shape, rings)

    if plot:
        print(f"Shape: {shape}")
        print(f"Indices: {indices}")
        print(f"Rings: {rings}")

        # Plotting the result
        for i in range(0, len(indices), 3):
            triangle = shape[indices[i : i + 3]]
            plt.fill(*zip(*triangle), alpha=0.4, edgecolor="black")
        plt.show()

    return indices


if __name__ == "__main__":
    # # Test the function with a sample shape
    # sample_shape = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    # tesselate(sample_shape)

    inner_edge = np.array([[4, 3], [5, 4], [4, 5], [3, 4]])
    outer_edge = np.array([[3, 1], [5, 1], [7, 4], [5, 7], [3, 7], [1, 4]])

    combined_edge = np.array(
        [
            [3, 1],
            [5, 1],
            [7, 4],
            [5, 4],
            [4, 3],
            [3, 4],
            [4, 5],
            [5, 4],
            [7, 4],
            [5, 7],
            [3, 7],
            [1, 4],
        ]
    )

    indices = np.array(
        [
            11,
            0,
            1,
            1,
            2,
            3,
            6,
            7,
            8,
            8,
            9,
            10,
            1,
            3,
            4,
            6,
            8,
            10,
            11,
            1,
            4,
            5,
            6,
            10,
            11,
            4,
            5,
            5,
            10,
            11,
        ]
    )

    ans = tesselate(combined_edge, plot=True)
