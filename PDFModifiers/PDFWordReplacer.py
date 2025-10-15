import os
import fitz  # PyMuPDF library

# --- Font and Directory Configuration ---
FONT_DIR = "Fonts"
FONT_REGULAR_FILE = "Inter-Regular.ttf"
FONT_SEMIBOLD_FILE = "Inter-SemiBold.ttf"
# ----------------------------------------

# Ensure we are in the correct directory (as requested by your provided code)
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print("Working directory set to:", os.getcwd())

# Pre-calculate the absolute paths for the font files
FONT_PATH_REGULAR = os.path.join(script_dir, FONT_DIR, FONT_REGULAR_FILE)
FONT_PATH_SEMIBOLD = os.path.join(script_dir, FONT_DIR, FONT_SEMIBOLD_FILE)

# Create a mapping of the font key (from REPLACEMENTS_CONFIG) to the actual file path
FONT_PATH_MAP = {
    "Inter-Regular": FONT_PATH_REGULAR,
    "Inter-SemiBold": FONT_PATH_SEMIBOLD
}


def replace_static_pdf_text(input_pdf_path: str, output_pdf_path: str, replacements_config: list):
    """
    Replaces text in a PDF using the page.insert_text(fontfile=...) method
    to bypass document-level font loading errors.
    """
    doc = None
    try:
        if not os.path.exists(input_pdf_path):
            print(f"Error: The input file was not found at '{input_pdf_path}'. Please check the path.")
            return

        # 1. Quick check to ensure font files exist before opening the document
        for path in FONT_PATH_MAP.values():
            if not os.path.exists(path):
                print(f"CRITICAL ERROR: Font file not found: {path}")
                print("Please ensure your font files are in the correct location.")
                return

        # Open the original PDF document
        doc = fitz.open(input_pdf_path)
        replaced_count = 0

        # Iterate through every page in the document
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            insert_data = []
            redaction_applied = False
            
            # 1. First Pass: Collect all redaction and insertion data
            for config in replacements_config:
                old_text = config['old_text']
                new_text = config['new_text']
                offset_multiplier = config['offset_multiplier']
                
                # Get the font path directly from the map
                font_key = config.get('font_to_use', 'Helvetica') 
                # This will be the file path string, or 'Helvetica' (if key is missing)
                font_file_path = FONT_PATH_MAP.get(font_key) 
                
                # Search for occurrences of the old text on the page
                text_instances = page.search_for(old_text)
                
                if text_instances:
                    print(f"Found {len(text_instances)} instances of '{old_text}' on page {page_num + 1}.")
                    
                    for inst in text_instances:
                        original_font_size = inst.height * 0.9 
                        
                        # Add the redaction annotation
                        redact_area = fitz.Rect(inst)
                        page.add_redact_annot(redact_area)
                        redaction_applied = True
                        
                        # Calculate a custom vertical offset based on the multiplier
                        offset_point = fitz.Point(inst.tl.x, inst.tl.y + inst.height * offset_multiplier)

                        # Store the insertion details
                        insert_data.append({
                            'point': offset_point,
                            'text': new_text,
                            'fontsize': original_font_size,
                            'font_path': font_file_path # Store the file path instead of a font ID
                        })
                        
                        replaced_count += 1
            
            # 2. Second Pass: Apply Redactions and Insert Text
            if redaction_applied:
                page.apply_redactions()

                for item in insert_data:
                    # **CRITICAL FIX**: Use the 'fontfile' parameter for insertion
                    # This tells PyMuPDF to load, embed, and use the font directly from the file path.
                    page.insert_text(
                        item['point'], 
                        item['text'], 
                        fontsize=item['fontsize'], 
                        fontfile=item['font_path'] 
                    )

        if replaced_count > 0:
            doc.save(output_pdf_path, garbage=3, deflate=True) 
            print(f"\nSuccess! Modified {replaced_count} items. The PDF was saved to: {output_pdf_path}")
        else:
            print("\nWarning: No text was replaced.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if doc:
            doc.close()

# --- User Configuration ---

# 1. Define the input and output file paths
INPUT_FILE = "original_document.pdf"
OUTPUT_FILE = "invoice_updated_static_inter_font.pdf"

# 2. Define the exact text replacements and their custom vertical offsets.
# The 'font_to_use' keys map to the paths defined at the top of the script.
REPLACEMENTS_CONFIG = [
    {
        "old_text": "Receipt", 
        "new_text": "Invoice", 
        "offset_multiplier": 0.8,
        "font_to_use": "Inter-SemiBold"  # Maps to Inter-SemiBold.ttf path
    },
    {
        "old_text": "Andrew Johson", 
        "new_text": "Christan Versteeg", 
        "offset_multiplier": 0.8,
        "font_to_use": "Inter-Regular"       # Maps to Inter-Regular.ttf path
    },
    {
        "old_text": "anicver@gmail.com", 
        "new_text": "chrisjaver@gmail.com", 
        "offset_multiplier": 0.8,
        "font_to_use": "Inter-Regular"       # Maps to Inter-Regular.ttf path
    }
]

# --- Execution ---
if __name__ == "__main__":
    replace_static_pdf_text(INPUT_FILE, OUTPUT_FILE, REPLACEMENTS_CONFIG)