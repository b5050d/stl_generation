from src.png_to_matrix import (
    load_png_to_gray_matrix,
    convert_matrix_to_binary,
    pad_matrix,
)
from utils.plotting import plot_image_matrix, plot_edge_array
from src.matrix_to_edges import hollow_out_shapes, collect_edges

if __name__ == "__main__":
    png_path = "images/c.png"
    matrix = load_png_to_gray_matrix(png_path)
    matrix = pad_matrix(matrix, 0.1)
    plot_image_matrix(matrix)

    binary_matrix = convert_matrix_to_binary(matrix, 128)
    plot_image_matrix(binary_matrix)

    hollowed_out = hollow_out_shapes(binary_matrix)
    plot_image_matrix(hollowed_out)

    edges = collect_edges(hollowed_out)

    plot_edge_array(edges[0])
