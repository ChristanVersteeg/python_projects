import os
from rembg import remove
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ============================
# 🛠️ CONFIGURATION CONSTANTS
# ============================

# Name of the input image in the root folder (supports PNG, JPG, etc.)
INPUT_IMAGE_NAME = "maria2.jpg"  # Change to your actual image file

# Name of the output image with background removed
OUTPUT_IMAGE_NAME = "output_image.png"

# Aggressiveness of background removal (True = more aggressive, can eat into fine edges)
CUT_BOUNDARY_TIGHT = True

# Enable alpha matting for better edges (e.g. hair)
USE_ALPHA_MATTING = True

# Controls how far the matting algorithm will look around the object (higher = more background included)
ALPHA_MATTING_FOREGROUND_THRESHOLD = 5

# Minimum size of object to keep during matting (lower = keeps smaller features)
ALPHA_MATTING_ERODE_SIZE = 120

# Background blur (optional, for soft transitions). 0 = no blur
POST_PROCESS_BLUR_RADIUS = 0

# ==================================
# 🚀 MAIN LOGIC - DO NOT MODIFY BELOW
# ==================================

def remove_background():
    if not os.path.exists(INPUT_IMAGE_NAME):
        print(f"Input file '{INPUT_IMAGE_NAME}' not found.")
        return

    with open(INPUT_IMAGE_NAME, "rb") as input_file:
        input_data = input_file.read()

        result = remove(
            input_data,
            alpha_matting=USE_ALPHA_MATTING,
            alpha_matting_foreground_threshold=ALPHA_MATTING_FOREGROUND_THRESHOLD,
            alpha_matting_erode_size=ALPHA_MATTING_ERODE_SIZE,
            only_mask=False,
            post_process_mask=True,
            cut_boundary_tight=CUT_BOUNDARY_TIGHT,
        )

        with open(OUTPUT_IMAGE_NAME, "wb") as output_file:
            output_file.write(result)

    # Optional: Apply post-blur for softer edges (PIL doesn't support alpha blur directly)
    if POST_PROCESS_BLUR_RADIUS > 0:
        img = Image.open(OUTPUT_IMAGE_NAME).convert("RGBA")
        from PIL import ImageFilter
        img = img.filter(ImageFilter.GaussianBlur(POST_PROCESS_BLUR_RADIUS))
        img.save(OUTPUT_IMAGE_NAME)

    print(f"Background removed. Saved as '{OUTPUT_IMAGE_NAME}'.")


if __name__ == "__main__":
    remove_background()
