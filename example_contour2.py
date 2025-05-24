import cv2
import numpy as np
import matplotlib.pyplot as plt

# Create an example image with a ring around a square
image = np.zeros((200, 200), dtype=np.uint8)
cv2.rectangle(image, (50, 50), (150, 150), 255, -1)  # Solid inner square
cv2.rectangle(image, (40, 40), (160, 160), 0, -1)  # Outer square (to erase inside)
cv2.rectangle(image, (40, 40), (160, 160), 255, 5)  # Ring (white border)

# Find contours
contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Convert to color image for visualization
image_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

# Draw contours and label them
for i, cnt in enumerate(contours):
    cv2.drawContours(image_color, [cnt], -1, (0, 255, 0), 2)
    # cv2.putText(image_color, f'{i}', tuple(cnt[0][0]), cv2.FONT_HERSHEY_SIMPLEX,
    #             0.5, (0, 0, 255), 1)

# Display using matplotlib
plt.figure(figsize=(6, 6))
plt.imshow(cv2.cvtColor(image_color, cv2.COLOR_BGR2RGB))
plt.title("Contours with Labels")
plt.axis("off")
plt.show()
