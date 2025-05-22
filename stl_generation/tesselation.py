import numpy as np
import mapbox_earcut as earcut
from matplotlib import pyplot as plt

def tesselate(shape: np.ndarray):
    # Alright we need to tesselate a shape here

    # What form does mapbox_earcut need the shape in?
    # looks like numpy array of (x,2)

    assert shape.ndim == 2, "Shape must be a 2D array"


    # not sure why this is done
    rings = np.array([len(shape)], dtype=np.uint32)

    indices = earcut.triangulate_float64(shape, rings)

    print(f"Shape: {shape}")
    print(f"Indices: {indices}")
    print(f"Rings: {rings}")


    # Plotting the result
    for i in range(0, len(indices), 3):
        triangle = shape[indices[i:i+3]]
        plt.fill(*zip(*triangle), alpha=0.4, edgecolor='black')
    plt.show()

    return 1

if __name__ == "__main__":
    # Test the function with a sample shape
    sample_shape = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    tesselate(sample_shape)
