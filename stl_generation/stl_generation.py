import numpy as np

# from matplotlib import pyplot as plt

# from stl_generation.utils.plotting import (
#     plot_triangles,
#     plot_stl_triangles,
# )
import struct


def generate_stl_walls(edge, floor_height, ceiling_height, inner_or_outer="inner"):
    """
    Generate the walls of the STL from the edges.
    """
    # TODO: Switch to ensure_ccw
    if inner_or_outer == "inner":
        # INNER = True
        OUTER = False
    elif inner_or_outer == "outer":
        # INNER = False
        OUTER = True
    else:
        raise Exception("Error input")

    assert is_ccw(edge), "The edge should be counter-clockwise"

    normies = compute_inward_normals(edge)
    # print(normies)

    first_loop = True
    for i in range(len(edge)):
        a = edge[i]
        b = edge[(i + 1) % len(edge)]

        norm = normies[i]
        if OUTER:
            norm = -1 * norm

        if OUTER:
            t1 = np.array(
                [
                    [norm[0], norm[1], 0],
                    [a[0], a[1], floor_height],
                    [b[0], b[1], floor_height],
                    [a[0], a[1], ceiling_height],
                ]
            )

            t2 = np.array(
                [
                    [norm[0], norm[1], 0],
                    [b[0], b[1], floor_height],
                    [b[0], b[1], ceiling_height],
                    [a[0], a[1], ceiling_height],
                ]
            )
        else:
            t1 = np.array(
                [
                    [norm[0], norm[1], 0],
                    [a[0], a[1], floor_height],
                    [a[0], a[1], ceiling_height],
                    [b[0], b[1], floor_height],
                ]
            )

            t2 = np.array(
                [
                    [norm[0], norm[1], 0],
                    [b[0], b[1], floor_height],
                    [a[0], a[1], ceiling_height],
                    [b[0], b[1], ceiling_height],
                ]
            )

        new_triangles = np.array([t1, t2])

        if first_loop:
            triangles = new_triangles
            first_loop = False
        else:
            triangles = np.concatenate((triangles, new_triangles), axis=0)

    return triangles


def generate_sloped_walls(outer_shape, inner_shape, lower_height, upper_height):
    """
    Note, for now this is assuming that the slope is upward in the z dir
    the outer shape is the base (lower)
    and the inner shape is the top (upper)
    """
    assert len(outer_shape) == len(inner_shape)
    outer_shape = ensure_ccw(outer_shape)
    inner_shape = ensure_ccw(inner_shape)

    first_loop = True
    for i in range(len(outer_shape)):
        a = outer_shape[i]
        b = outer_shape[(i + 1) % len(outer_shape)]
        c = inner_shape[i]
        d = inner_shape[(i + 1) % len(inner_shape)]

        A = np.array([a[0], a[1], lower_height])
        B = np.array([b[0], b[1], lower_height])
        C = np.array([c[0], c[1], upper_height])
        D = np.array([d[0], d[1], upper_height])

        t1 = np.array([compute_3d_norm(A, B, C), A, B, C])
        t2 = np.array([compute_3d_norm(B, D, C), B, D, C])

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
                norm_vec,
                [triangle_points[0, 0], triangle_points[0, 1], roof_height],
                [triangle_points[1, 0], triangle_points[1, 1], roof_height],
                [triangle_points[2, 0], triangle_points[2, 1], roof_height],
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


def convert_float_to_ieee754_bin(num):
    num = float(num)
    # https://stackoverflow.com/questions/51179116/ieee-754-python
    (bits,) = struct.unpack("!I", struct.pack("!f", num))
    return "{:032b}".format(bits)


def split_4_bytes_into_4_uint8s(binstr):
    a = binstr[0:8]
    b = binstr[8:16]
    c = binstr[16:24]
    d = binstr[24:32]
    a = int(a, 2)
    b = int(b, 2)
    c = int(c, 2)
    d = int(d, 2)
    return np.uint8(a), np.uint8(b), np.uint8(c), np.uint8(d)


def write_triangles_to_stl(filepath, collected_triangles):
    with open(filepath, "wb") as stl:
        for i in range(80):
            stl.write(np.uint8(0))
        number_of_triangles = len(collected_triangles)
        stl.write(np.uint32(number_of_triangles))

        # Now write each triangle
        for triangle in collected_triangles:
            for vertex in triangle:
                for value in vertex:
                    bin_str = convert_float_to_ieee754_bin(value)
                    a, b, c, d = split_4_bytes_into_4_uint8s(bin_str)
                    stl.write(d)
                    stl.write(c)
                    stl.write(b)
                    stl.write(a)
            stl.write(np.uint16(0))


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
