from stl_generation.png_to_matrix import (
    load_png_to_gray_matrix,
    convert_matrix_to_binary,
    pad_matrix,
)
from stl_generation.utils.plotting import plot_image_matrix, plot_edge_array
from stl_generation.matrix_to_edges import (
    hollow_out_shapes,
    collect_edges,
    smoothing_routine_1,
    scale_edges,
    drop_points_on_edges,
)
from stl_generation.tesselation import tesselate

from matplotlib import pyplot as plt

if __name__ == "__main__":
    png_path = "images/c.png"
    matrix = load_png_to_gray_matrix(png_path)
    matrix = pad_matrix(matrix, 0.1)
    # plot_image_matrix(matrix)

    binary_matrix = convert_matrix_to_binary(matrix, 128)
    if 1:
        plot_image_matrix(binary_matrix)

    hollowed_out = hollow_out_shapes(binary_matrix)
    if 1:
        plot_image_matrix(hollowed_out)

    edges = collect_edges(hollowed_out)

    plot_edge_array(edges[0])

    edges = scale_edges(edges, 256)
    plot_edge_array(edges[0])

    edges = smoothing_routine_1(edges)
    plt.title("Smoothing (First)")
    plot_edge_array(edges[0])

    edges = smoothing_routine_1(edges)
    plt.title("Smoothing (Second)")
    plot_edge_array(edges[0])

    edges = smoothing_routine_1(edges)
    plt.title("Smoothing (Third)")
    plot_edge_array(edges[0])

    edges = drop_points_on_edges(edges, 2)
    plt.title("Drop Points 1")
    plot_edge_array(edges[0])

    edges = smoothing_routine_1(edges)
    plt.title("Smoothing (Fourth)")
    plot_edge_array(edges[0])

    edges = drop_points_on_edges(edges, 2)
    plt.title("Drop Points 2")
    plot_edge_array(edges[0])

    print(edges[0])
    print(type(edges[0]))

    print(edges[0].shape)

    tesselate(edges[0], True)
