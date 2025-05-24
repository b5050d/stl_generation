import numpy as np

import cv2
from matplotlib import pyplot as plt

# from stl_generation.utils.plotting import plot_edge_array


# vertices = np.array([
#     [0, 0],
#     [1, 0],
#     [2, 0],
#     [3, 0],
#     [4, 0],
#     [5, 0],
#     [6, 0],
#     [7, 0],

# ], dtype=np.uint32)

# matrix = np.array([
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 1, 1, 1, 1, 1, 1, 0],
#     [0, 1, 1, 1, 1, 1, 1, 0],
#     [0, 1, 1, 1, 1, 1, 1, 0],
#     [0, 1, 1, 1, 1, 1, 1, 0],
#     [0, 1, 1, 1, 1, 1, 1, 0],
#     [0, 1, 1, 1, 1, 1, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
# ], dtype=np.uint8)


def collect_edges(matrix: np.ndarray):
    """
    Should find all of the edges in a hollowed out
    shape
    """
    # Assuming the matrix is in the 1/0 format from earlier
    matrix = np.where(matrix == 1, 255, 0)
    matrix = matrix.astype(np.uint8)
    inverted = cv2.bitwise_not(matrix)
    contours, hierarchy = cv2.findContours(
        inverted, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )

    if contours is None or len(contours) == 0:
        return []

    result = []
    for contour in contours:
        result.append(contour.reshape(-1, 2))
    return contours, hierarchy


matrix = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 0, 1, 0],
        [0, 1, 0, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    dtype=np.uint8,
)

contours, hierarchy = collect_edges(matrix)
print(f"Contours: {contours}")
print(f"Hierarchy: {hierarchy}")


image_copy = np.zeros((matrix.shape[0], matrix.shape[1], 3), dtype=np.uint8)

for i, cnt in enumerate(contours):
    cv2.drawContours(image_copy, [cnt], -1, (0, 255, 0), 2)
    cv2.putText(
        image_copy,
        f"{i}",
        tuple(cnt[0][0]),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 0, 0),
        2,
    )

plt.imshow(image_copy)
plt.show()
