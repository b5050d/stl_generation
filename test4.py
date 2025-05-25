from stl_generation.utils.plotting import plot_stl_triangles
import numpy as np
from stl_generation.stl_generation import generate_sloped_walls


outer_shape = np.array(
    [
        [0, 0],
        [3, 0],
        [3, 3],
        [0, 3],
    ]
)
inner_shape = np.array(
    [
        [1, 1],
        [2, 1],
        [2, 2],
        [1, 2],
    ]
)

lower_height = 0
upper_height = 3

ans = generate_sloped_walls(outer_shape, inner_shape, lower_height, upper_height)

plot_stl_triangles(ans)
