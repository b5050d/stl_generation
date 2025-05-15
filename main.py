from src.matrix.png_to_matrix import (
    load_png_to_gray_matrix,
    convert_matrix_to_binary,
)
from utils.plotting import plot_image_matrix

if __name__ == "__main__":
    png_path = "images/c.png"
    matrix = load_png_to_gray_matrix(png_path)
    plot_image_matrix(matrix)
    
