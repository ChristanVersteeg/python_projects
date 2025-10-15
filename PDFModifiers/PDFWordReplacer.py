import os
import fitz  # PyMuPDF library

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print("Working directory set to:", os.getcwd())

# NOTE ON INSTALLATION:
# The PyMuPDF library is often imported as 'fitz'.
# Run `pip install PyMuPDF` in your terminal to install it.

def replace_static_pdf_text(input_pdf_path: str, output_pdf_path: str, replacements_config: list):
    """
    Attempts to search and replace arbitrary static text in a PDF document
    by redacting (erasing) the old text and inserting the new text in its place.

    WARNING: This method is highly unstable and fragile. It may fail or
    corrupt your PDF if the text is not simple or is broken up by PDF rendering commands.
    It works best on simple, computer-generated text.

    :param input_pdf_path: Path to the original static PDF file.
    :param output_pdf_path: Path where the new, modified PDF will be saved.
    :param replacements_config: A list of dictionaries, where each dict specifies
                                'old_text', 'new_text', 'offset_multiplier', and 'font_to_use'.
    """
    try:
        if not os.path.exists(input_pdf_path):
            print(f"Error: The input file was not found at '{input_pdf_path}'. Please check the path.")
            return

        # Open the original PDF document
        doc = fitz.open(input_pdf_path)

        # Flag to track if any replacement was successful
        replaced_count = 0

        # Iterate through every page in the document
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # --- START: Two-Pass Logic for Redaction and Insertion ---
            insert_data = []
            redaction_applied = False
            
            # 1. First Pass: Collect all redaction and insertion data
            for config in replacements_config:
                old_text = config['old_text']
                new_text = config['new_text']
                offset_multiplier = config['offset_multiplier']
                # Get the desired font. Use 'helv-bold' or 'helv' from config, defaulting to 'helv'.
                new_fontname = config.get('font_to_use', 'helv') 
                
                # Search for occurrences of the old text on the page
                text_instances = page.search_for(old_text)
                
                if text_instances:
                    print(f"Found {len(text_instances)} instances of '{old_text}' on page {page_num + 1}.")
                    
                    # For each match found, collect data for later insertion
                    for inst in text_instances:
                        # Estimate original font size (using 0.9 multiplier for better visibility)
                        original_font_size = inst.height * 0.9 
                        
                        # Add the redaction annotation
                        redact_area = fitz.Rect(inst)
                        page.add_redact_annot(redact_area)
                        redaction_applied = True
                        
                        # Calculate a custom vertical offset based on the multiplier
                        offset_point = fitz.Point(inst.tl.x, inst.tl.y + inst.height * offset_multiplier)

                        # Store the insertion details, including the specific font name
                        insert_data.append({
                            'point': offset_point, # Use the custom offset point
                            'text': new_text,
                            'fontsize': original_font_size,
                            'fontname': new_fontname # Store the correct font name
                        })
                        
                        replaced_count += 1
            
            # 2. Second Pass: Apply Redactions and Insert Text
            if redaction_applied:
                # A. Apply all redactions (This physically removes the old text)
                page.apply_redactions()

                # B. Insert the new text into the now-empty space
                for item in insert_data:
                    page.insert_text(
                        item['point'], 
                        item['text'], 
                        fontsize=item['fontsize'], 
                        fontname=item['fontname'] # Use the font specified for this item
                    )
            # --- END: Two-Pass Logic ---

        if replaced_count > 0:
            # 5. Write the modified content to the new output file
            # Save with compression and cleanup for a smaller, cleaner PDF.
            doc.save(output_pdf_path, garbage=3, deflate=True) 
            print(f"\nSuccess! Modified {replaced_count} items. The PDF was saved to: {output_pdf_path}")
        else:
            print("\nWarning: No text was replaced. Ensure the text in your PDF exactly matches the keys in the REPLACEMENTS_CONFIG.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if 'doc' in locals():
            doc.close()

# --- User Configuration ---

# 1. Define the input and output file paths
INPUT_FILE = "original_document.pdf"
OUTPUT_FILE = "invoice_updated_static.pdf"

# 2. Define the exact text replacements and their custom vertical offsets.
# Use "helv-bold" for the bold font and "helv" for the regular font.
REPLACEMENTS_CONFIG = [
    {
        "old_text": "Receipt", 
        "new_text": "Invoice", 
        "offset_multiplier": 0.8,
        "font_to_use": "Helvetica-Bold"  # 🌟 This makes "Invoice" bold
    },
    {
        "old_text": "Andrew Johson", 
        "new_text": "Christan Versteeg", 
        "offset_multiplier": 0.8,
        "font_to_use": "helv"       # Regular Font
    },
    {
        "old_text": "anicver@gmail.com", 
        "new_text": "chrisjaver@gmail.com", 
        "offset_multiplier": 0.8,
        "font_to_use": "helv"       # Regular Font
    }
]

# --- Execution ---
if __name__ == "__main__":
    replace_static_pdf_text(INPUT_FILE, OUTPUT_FILE, REPLACEMENTS_CONFIG)