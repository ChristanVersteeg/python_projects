import fitz  # PyMuPDF
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print("Working directory set to:", os.getcwd())

def extract_fonts_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    fonts = set()

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # Get the fonts on the page
        font_info = page.get_fonts(full=True)
        for font in font_info:
            # font is a tuple, usually with font name at index 3
            fonts.add(font[3])

    return fonts

if __name__ == "__main__":
    pdf_file = "original_document.pdf"  # Replace with your PDF file path
    fonts = extract_fonts_from_pdf(pdf_file)
    print("Fonts used in the PDF:")
    for font in fonts:
        print(font)
