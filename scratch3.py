import cv2
import numpy as np
import matplotlib.pyplot as plt

# Create a binary image with a closed black trail (0 = shape, 255 = background)
binary_image = np.array([
    [255, 255, 255, 255, 255],
    [255,   0,   0,   0, 255],
    [255,   0, 255,   0, 255],
    [255,   0,   0,   0, 255],
    [255, 255, 255, 255, 255],
], dtype=np.uint8)

binary_image = np.array([
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [255, 255,   0,   0,   0, 255, 255, 255, 255, 255, 255, 255],
    [255,   0, 255, 255, 255,   0,   0, 255, 255, 255, 255, 255],
    [255,   0, 255, 255, 255, 255, 255,   0, 255, 255, 255, 255],
    [255,   0, 255, 255, 255, 255, 255,   0, 255, 255, 255, 255],
    [255,   0, 255, 255, 255, 255, 255,   0, 255, 255, 255, 255],
    [255,   0, 255, 255, 255, 255, 255,   0, 255, 255, 255, 255],
    [255, 255,   0,   0,   0,   0,   0, 255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
], dtype=np.uint8)


# Invert image so shape is white on black (as required by OpenCV)
inverted = cv2.bitwise_not(binary_image)

# Find contours: RETR_EXTERNAL = outer contour, CHAIN_APPROX_NONE = every point
contours, hierarchy = cv2.findContours(inverted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Extract the first (and only) contour
contour = contours[0]  # Shape: (N, 1, 2)

# Convert to list of (row, col)
points = [tuple(pt[0]) for pt in contour]

print("Contour points (CW):")
for p in points:
    print(p)

# Optional: visualize
plt.imshow(binary_image, cmap='gray')
pts = np.array(points)
plt.plot(pts[:, 0], pts[:, 1], 'r-')  # Note: x is column, y is row
plt.scatter(pts[0, 0], pts[0, 1], c='blue', label="Start")
plt.legend()
plt.title("Extracted Contour")
plt.gca().invert_yaxis()
plt.show()
