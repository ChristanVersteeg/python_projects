import os
from rembg import remove
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ============================
# 🛠️ CONFIGURATION CONSTANTS
# ============================

# Naam van de invoerafbeelding
INPUT_IMAGE_NAME = "tri.jpg"  # Pas aan naar de juiste extensie (.jpg of .png)

# Naam van het resultaat
OUTPUT_IMAGE_NAME = "output_image.png"

# Minder agressief afsnijden zodat gelaatstrekken en randen behouden blijven
CUT_BOUNDARY_TIGHT = False

# Alpha matting inschakelen voor een nauwkeurige uitsnede van haren en randen
USE_ALPHA_MATTING = True

# Verlaag deze waarde zodat de achtergrond niet in de randen van je hoofd/kleding snijdt
ALPHA_MATTING_FOREGROUND_THRESHOLD = 240

# Verlaag het wegsnijden aan de randen om details (zoals je bril en kapsel) te beschermen
ALPHA_MATTING_ERODE_SIZE = 10

# Geen achtergrondvervaging om de uitsnede zo strak mogelijk te houden
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
