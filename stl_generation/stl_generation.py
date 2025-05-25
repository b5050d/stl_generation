import numpy as np

# from matplotlib import pyplot as plt

# from stl_generation.utils.plotting import (
#     plot_triangles,
#     plot_stl_triangles,
# )


def generate_stl_walls(edge, floor_height, ceiling_height):
    """
    Generate the walls of the STL from the edges.
    """
    # TODO: Switch to ensure_ccw

    assert is_ccw(edge), "The edge should be counter-clockwise"

    first_loop = True
    for i in range(len(edge)):
        a = edge[i]
        b = edge[(i + 1) % len(edge)]

        t1 = np.array(
            [
                [a[0], a[1], floor_height],
                [a[0], a[1], ceiling_height],
                [b[0], b[1], floor_height],
                # now we add in the normal vector
            ]
        )

        t2 = np.array(
            [
                [b[0], b[1], floor_height],
                [a[0], a[1], ceiling_height],
                [b[0], b[1], ceiling_height],
                # now we add in the normal vector
            ]
        )

        new_triangles = np.array([t1, t2])

        if first_loop:
            triangles = new_triangles
            first_loop = False
        else:
            triangles = np.concatenate((triangles, new_triangles), axis=0)

    return triangles


def compute_inward_normals(points):
    normals = []
    n = len(points)

    for i in range(n):
        # Get segment endpoints
        p1 = np.array(points[i])
        p2 = np.array(points[(i + 1) % n])

        # Direction vector of the segment
        edge = p2 - p1

        # Compute left-hand normal (-dy, dx)
        normal = np.array([-edge[1], edge[0]])
        normalized = normal / np.max(np.abs(normal))

        normal = normalized

        normals.append(normal)
    normals = np.array(normals)
    return normals


def is_ccw(points):
    area = 0
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return area > 0


def ensure_ccw(points):
    return points if is_ccw(points) else points[::-1]


def ensure_cw(points):
    return points if not is_ccw(points) else points[::-1]


def generate_triangles_from_tesselation(indices, edge, floor_or_ceiling, roof_height):
    assert floor_or_ceiling in [
        "floor",
        "ceiling",
    ], "floor_or_ceiling must be either 'floor' or 'ceiling'"

    if floor_or_ceiling == "floor":
        FLOOR = True
        ROOF = False
    else:
        FLOOR = False
        ROOF = True

    # Alright we want a numpy array of triangles.

    first_loop = True

    for i in range(0, len(indices), 3):
        indices_of_triangle = indices[i : i + 3]
        # input(indices_of_triangle)

        # Alright now we need to get the points from the triangle and ensure CCW
        triangle_points = edge[indices_of_triangle]
        # input(triangle_points)

        if FLOOR:
            triangle_points = ensure_cw(triangle_points)
            norm_vec = [0, 0, -1]
        elif ROOF:
            triangle_points = ensure_ccw(triangle_points)
            norm_vec = [0, 0, 1]

        # print(type(triangle_points))
        # input(triangle_points)

        new_triangle = np.array(
            [
                [triangle_points[0, 0], triangle_points[0, 1], roof_height],
                [triangle_points[1, 0], triangle_points[1, 1], roof_height],
                [triangle_points[2, 0], triangle_points[2, 1], roof_height],
                norm_vec,
            ]
        )
        # input(new_triangle)
        if first_loop:
            triangles = np.array([new_triangle])
            first_loop = False
            # input(triangles)

        else:
            triangles = np.concatenate((triangles, [new_triangle]), axis=0)
            # input(triangles)

    return triangles


# def generate_triangles_from_edge(edge, floor_or_ceiling, roof_height):
#     """
#     Generate triangles from the edge of a shape.
#     """
#     assert is_ccw(edge), "The edge should be counter-clockwise"
#     indices = np.arange(len(edge))
#     return generate_triangles_from_tesselation(indices, edge, floor_or_ceiling, roof_height)


def compute_3d_norm(A, B, C):
    """
    Compute the 3D normal vector for a triangle defined by points A, B, C.
    """
    u = B - A
    v = C - A

    n = np.cross(u, v)

    norm = np.linalg.norm(n)
    n_unit = n / norm if norm != 0 else n  # Handle zero-length vector case

    return n_unit


def in_equivalent_for_numpy(target, to_search):
    for item in to_search:
        if np.array_equal(target, item):
            return True
    return False


# def generate_triangles_for_slope(indices, edge, inner_edge, outer_edge, roof_height):
#     """ """

#     first_loop = True

#     for i in range(0, len(indices), 3):
#         indices_of_triangle = indices[i : i + 3]

#         # Alright now we need to get the points from the triangle and ensure CCW
#         triangle_points = edge[indices_of_triangle]

#         # Now we need to generate the normals...
#         zs = []
#         for tp in triangle_points:
#             # print(inner_edge)
#             # input(tp)
#             if in_equivalent_for_numpy(tp, inner_edge):
#                 # print("found in inner_edge")
#                 zs.append(roof_height)
#             elif in_equivalent_for_numpy(tp, outer_edge):
#                 # print("found in outer_edge")
#                 zs.append(0)
#             else:
#                 raise ValueError("Point not found in either inner or outer edge")

#         A = np.array(
#             [triangle_points[0, 0], triangle_points[0, 1], zs[0]],
#         )
#         B = np.array(
#             [triangle_points[1, 0], triangle_points[1, 1], zs[1]],
#         )
#         C = np.array(
#             [triangle_points[2, 0], triangle_points[2, 1], zs[2]],
#         )
#         new_triangle = np.array([A, B, C, compute_3d_norm(A, B, C)])

#         if first_loop:
#             triangles = np.array([new_triangle])
#             first_loop = False
#         else:
#             triangles = np.concatenate((triangles, [new_triangle]), axis=0)

#     return triangles


if __name__ == "__main__":
    pass
