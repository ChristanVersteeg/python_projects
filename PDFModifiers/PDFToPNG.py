import os
from pdf2image import convert_from_path
from PIL import Image

def make_transparent(image):
    """
    Converts the white (or near-white) background of an image to transparent.
    """
    # Ensure the image is in RGBA mode (Red, Green, Blue, Alpha)
    image = image.convert("RGBA")
    data = image.getdata()

    new_data = []
    # Loop through every pixel
    for item in data:
        # Check if the pixel is white or very close to white (RGB values > 240)
        # item is a tuple: (R, G, B, A)
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            # Replace with a fully transparent pixel
            new_data.append((255, 255, 255, 0))
        else:
            # Keep the original pixel
            new_data.append(item)

    # Apply the new pixel data to the image
    image.putdata(new_data)
    return image

def process_pdfs():
    # Get the directory where the script is currently running
    current_dir = os.getcwd()
    
    # Find all files ending in .pdf
    pdf_files = [f for f in os.listdir(current_dir) if f.lower().endswith('.pdf')]

    if not pdf_files:
        print("No PDF files found in the current directory.")
        return

    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file}")
        pdf_path = os.path.join(current_dir, pdf_file)
        
        # Strip the .pdf extension to use for the output filename
        base_name = os.path.splitext(pdf_file)[0]

        try:
            # Convert PDF to a list of PIL Images
            # Note: poppler_path can be added here if Poppler isn't in your PATH
            # e.g., convert_from_path(pdf_path, poppler_path=r'C:\path\to\poppler\bin')
            pages = convert_from_path(pdf_path)

            for i, page in enumerate(pages):
                print(f"  Converting page {i + 1} to transparent PNG...")
                
                # Strip the background
                transparent_page = make_transparent(page)
                
                # Save the new image
                output_filename = f"{base_name}_page_{i + 1}.png"
                transparent_page.save(output_filename, "PNG")
                print(f"  Saved: {output_filename}")
                
        except Exception as e:
            print(f"Error processing {pdf_file}. Ensure Poppler is installed and in your PATH.\nDetails: {e}")

if __name__ == "__main__":
    print("Starting conversion process...")
    process_pdfs()
    print("All tasks completed!")