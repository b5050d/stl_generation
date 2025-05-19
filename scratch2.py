import numpy as np

count_matrix = np.array([
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
])


from matrix_to_edges import final_hollowing

ans = final_hollowing(count_matrix)
print(ans)

ans = np.where(count_matrix < 4, 1, 0)
print(ans)

ans = np.where(count_matrix > 6, 1, 0)
print(ans)
