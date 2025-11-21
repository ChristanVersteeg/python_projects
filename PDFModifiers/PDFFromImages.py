"""
images_to_pdf.py

Combine images in ./images into a single PDF (one page per image).

- Defaults to ./images relative to this script.
- Sorts files by the numeric part of the filename (e.g. IMG_0960.jpg).
- Fixes EXIF orientation.
- Optional global rotation (e.g. --rotate 90).
"""

import argparse
import re
from pathlib import Path

from PIL import Image, ImageOps


def extract_number(path: Path) -> int:
    """Extract last integer found in filename (without extension)."""
    match = re.findall(r"(\d+)", path.stem)
    return int(match[-1]) if match else 0


def collect_images(folder: Path):
    """Return a list of image paths sorted by the numeric part of the filename."""
    exts = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
    files = [p for p in folder.iterdir() if p.suffix.lower() in exts and p.is_file()]
    files.sort(key=extract_number)
    return files


def load_and_prepare_image(path: Path, rotate: int | None = None) -> Image.Image:
    """
    Open image, apply EXIF orientation, optional manual rotation,
    and convert to RGB for PDF.
    """
    img = Image.open(path)
    # Fix orientation based on EXIF
    img = ImageOps.exif_transpose(img)
    # Optional user-specified rotation
    if rotate:
        img = img.rotate(-rotate, expand=True)  # PIL rotates counter-clockwise
    return img.convert("RGB")


def images_to_pdf(image_paths, output_file: Path, rotate: int | None = None):
    """Create a PDF from a list of image paths."""
    if not image_paths:
        raise ValueError("No image files found to convert.")

    pil_images = [load_and_prepare_image(p, rotate=rotate) for p in image_paths]

    first_image, *rest = pil_images
    first_image.save(output_file, save_all=True, append_images=rest)
    print(f"Saved PDF with {len(pil_images)} pages to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Combine images into a PDF.")
    parser.add_argument(
        "--folder",
        type=str,
        default="images",
        help="Folder containing images (default: ./images)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output.pdf",
        help="Output PDF filename (default: output.pdf in project root)",
    )
    parser.add_argument(
        "--rotate",
        type=int,
        choices=[-270, -180, -90, 0, 90, 180, 270],
        default=0,
        help="Rotate all images by this many degrees clockwise (e.g. 90).",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    folder = (script_dir / args.folder).resolve()

    if not folder.is_dir():
        raise SystemExit(f"Not a directory: {folder}")

    image_paths = collect_images(folder)
    if not image_paths:
        raise SystemExit(f"No images found in folder: {folder}")

    rotate = args.rotate if args.rotate != 0 else None
    output_file = script_dir / args.output
    images_to_pdf(image_paths, output_file, rotate=rotate)


if __name__ == "__main__":
    main()
