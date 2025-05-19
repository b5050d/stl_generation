import numpy as np

# count_matrix = np.array([
#     [0, 1, 2],
#     [3, 4, 5],
#     [6, 7, 8],
# ])


# from matrix_to_edges import final_hollowing

# ans = final_hollowing(count_matrix)
# print(ans)

# ans = np.where(count_matrix < 4, 1, 0)
# print(ans)

# ans = np.where(count_matrix > 6, 1, 0)
# print(ans)

sample = np.array([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ])


indices = np.where(sample == 0)
print(indices)


def find_first_zero(img):
    """Find first 0 pixel as starting point."""
    coords = np.argwhere(img == 0)
    return tuple(coords[0]) if coords.size > 0 else None

print(find_first_zero(sample))


# import numpy as np

# # Define 8-connected neighbors in CW order (starting from top-left)
# MOORE_NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1),
#                    (0, 1),  (1, 1), (1, 0),
#                    (1, -1), (0, -1)]


# def trace_contour(image):
#     h, w = image.shape
#     start = find_first_zero(image)
#     if start is None:
#         return []

#     contour = []
#     curr = start
#     prev_dir = 7  # Start looking from the "west" of the pixel

#     while True:
#         contour.append(curr)
#         for i in range(8):
#             # Look around in CW order starting from prev_dir + 1
#             direction = (prev_dir + i) % 8
#             dr, dc = MOORE_NEIGHBORS[direction]
#             nr, nc = curr[0] + dr, curr[1] + dc

#             if 0 <= nr < h and 0 <= nc < w and image[nr, nc] == 0:
#                 curr = (nr, nc)
#                 prev_dir = (direction + 5) % 8  # This sets new search direction (trick from algorithm)
#                 break
#         else:
#             break  # No next pixel found

#         if curr == start:
#             break

#     return contour

    

    