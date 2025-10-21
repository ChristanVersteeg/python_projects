import os
import cv2
import numpy as np

os.chdir(os.path.dirname(os.path.abspath(__file__)))


# Define the hex colors to remove
hex_colors = ['89866a']

# Convert hex to BGR format used by OpenCV
def hex_to_bgr(hex_color):
    h = hex_color.lstrip('#')
    return [int(h[i:i+2], 16) for i in (4, 2, 0)]  # Reverse to BGR

# Set tolerance for color similarity
tolerance = 15  # Adjust as needed

# Load image (change path as needed)
img = cv2.imread('maria1.png', cv2.IMREAD_UNCHANGED)

if img is None:
    raise FileNotFoundError("Image not found. Check the path.")

# Ensure image has alpha channel
if img.shape[2] == 3:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

# Create mask to hold regions to remove
mask = np.zeros(img.shape[:2], dtype=np.uint8)

# Mark pixels matching any of the target colors within tolerance
for hex_color in hex_colors:
    bgr = np.array(hex_to_bgr(hex_color))
    lower = np.clip(bgr - tolerance, 0, 255)
    upper = np.clip(bgr + tolerance, 0, 255)
    color_mask = cv2.inRange(img[:, :, :3], lower, upper)
    mask = cv2.bitwise_or(mask, color_mask)

# Optional: Smooth edges using morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Remove small noise
mask = cv2.GaussianBlur(mask, (5, 5), 0)  # Feather the edges

# Apply transparency to masked pixels
img[:, :, 3] = cv2.bitwise_and(img[:, :, 3], 255 - mask)

# Save result
cv2.imwrite('output.png', img)

print("Done. Output saved as 'output.png'")
