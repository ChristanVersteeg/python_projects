import fitz  # PyMuPDF
from PIL import Image # Pillow library for image processing
import os
import io

def compress_pdf(input_pdf_path, output_pdf_path, img_quality=75):
    """
    Compresses a PDF file by extracting images, recompressing them using Pillow,
    and then re-inserting them into a new PDF document. This method offers
    more aggressive compression for image-heavy PDFs. It also skips empty pages.

    Args:
        input_pdf_path (str): The path to the input PDF file.
        output_pdf_path (str): The path where the compressed PDF will be saved.
        img_quality (int): Image compression quality (0-100). Lower values mean
                           more compression but lower image quality. Default is 75.
                           For aggressive compression, try values like 50 or lower.
    """
    try:
        # Open the input PDF file with PyMuPDF
        doc = fitz.open(input_pdf_path)
        
        # Create a new, empty PDF document to build the compressed version
        new_doc = fitz.open()
        
        skipped_pages_count = 0

        # Iterate through each page of the original document
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)

            # --- Check if the page is empty ---
            # A page is considered empty if it has no text, no images, and no drawings.
            has_text = bool(page.get_text().strip()) # Check for non-whitespace text
            has_images = len(page.get_images(full=False)) > 0 # Check for images
            has_drawings = len(page.get_drawings()) > 0 # Check for vector graphics/drawings

            if not has_text and not has_images and not has_drawings:
                skipped_pages_count += 1
                continue # Skip this page if it's empty
            # --- End of empty page check ---

            # Render the page to a pixmap (image)
            page_pix = page.get_pixmap()

            # Convert to RGB if not already (important for JPEG compression)
            if page_pix.n - page_pix.alpha > 3:  # CMYK or other non-RGB/grayscale
                page_pix = fitz.Pixmap(fitz.csRGB, page_pix)

            # Save the page pixmap to a temporary in-memory JPEG
            page_img_bytes = io.BytesIO(page_pix.tobytes("jpeg"))
            page_img = Image.open(page_img_bytes)

            # Recompress the page image using Pillow
            output_page_img_bytes = io.BytesIO()
            page_img.save(output_page_img_bytes, format='JPEG', quality=img_quality, optimize=True)
            output_page_img_bytes.seek(0)

            # Insert the recompressed page image into the new document
            # Create a new page in the new document
            new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
            
            # Insert the image to fill the entire page
            new_page.insert_image(
                fitz.Rect(0, 0, page.rect.width, page.rect.height), # Bounding box for the image
                stream=output_page_img_bytes.read(),
                overlay=True # Overlay on existing content (though new page is empty)
            )
            
            # Clean up pixmap
            page_pix = None # Release memory
        
        doc.close() # Close the original document

        # Save the new document with the recompressed page images
        new_doc.save(
            output_pdf_path,
            deflate=True, # Apply general stream compression
            garbage=3,    # Remove unused objects
            clean=True,   # Perform thorough cleanup
            linear=True,  # Optimize for web viewing
            pretty=True   # Make PDF structure readable
        )
        new_doc.close()

        # Get file sizes for comparison
        original_size = os.path.getsize(input_pdf_path)
        compressed_size = os.path.getsize(output_pdf_path)

        print(f"PDF compression attempt completed using PyMuPDF and Pillow!")
        print(f"Original size: {original_size / (1024 * 1024):.2f} MB")
        print(f"Compressed size: {compressed_size / (1024 * 1024):.2f} MB")
        print(f"Saved to: {output_pdf_path}")
        print(f"Skipped {skipped_pages_count} empty pages.")

        if compressed_size < original_size:
            print(f"\nCompression ratio: {((original_size - compressed_size) / original_size) * 100:.2f}% reduction.")
            print(f"Image quality set to: {img_quality}")
            print("Note: This method flattens the PDF by converting each page into a compressed image.")
            print("Text and vector graphics will no longer be selectable or searchable in the output PDF.")
        else:
            print("\nNote: No significant compression was achieved. This might be because the PDF")
            print("is already highly optimized, or the chosen image quality was too high.")
            print("Try reducing the 'img_quality' parameter (e.g., to 50 or lower) for more aggressive compression.")
            print("Be aware that this method flattens the PDF, making text unselectable.")


    except FileNotFoundError:
        print(f"Error: The file '{input_pdf_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Fixed input and output PDF file names
    input_pdf = "Manuscript.pdf"
    output_pdf = "CompManuscript.pdf"

    # You can adjust the img_quality parameter here (0-100)
    # Lower values mean more compression, but lower image quality.
    # For very high compression, try 50 or even lower.
    desired_image_quality = 95
    compress_pdf(input_pdf, output_pdf, img_quality=desired_image_quality)
