import os
import fitz  # PyMuPDF library

# --- Font Configuration (DISCARDED CUSTOM FONTS) ---
# We are now relying exclusively on built-in PDF fonts (Helvetica) for stability.
# ---------------------------------------------------

# Ensure we are in the correct directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Check if we need to change directory (if script is run from elsewhere)
if os.path.basename(os.getcwd()) != os.path.basename(script_dir):
    os.chdir(script_dir)
print("Working directory set to:", os.getcwd())


def replace_static_pdf_text(input_pdf_path: str, output_pdf_path: str, replacements_config: list):
    """
    Replaces text in a PDF using the reliable built-in PDF fonts (helv, helv-bold).
    
    This approach guarantees bolding functionality and consistent font rendering
    without relying on external TTF files.
    """
    doc = None
    try:
        if not os.path.exists(input_pdf_path):
            print(f"Error: The input file was not found at '{input_pdf_path}'. Please check the path.")
            return

        # Open the original PDF document
        doc = fitz.open(input_pdf_path)
        replaced_count = 0

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            insert_data = []
            redaction_applied = False
            
            # 1. First Pass: Collect all redaction and insertion data
            for config in replacements_config:
                old_text = config['old_text']
                new_text = config['new_text']
                # Use a functional default offset multiplier for vertical positioning
                offset_multiplier = config.get('offset_multiplier', 0.8) 
                
                # Get the point offset 
                size_offset_pts = config.get('fontsize_offset_pts', 0.0) 
                
                # Use the built-in font key ('helv' or 'helv-bold')
                font_key = config.get('font_to_use', 'helv') 
                
                text_instances = page.search_for(old_text)
                
                if text_instances:
                    print(f"Found {len(text_instances)} instances of '{old_text}' on page {page_num + 1}.")
                    
                    for inst in text_instances:
                        # CALCULATE BASE SIZE: Use 90% of the original text's bounding box height 
                        default_calculated_size = inst.height * 0.9 
                        
                        # APPLY OFFSET: Add the point offset to the base size.
                        final_fontsize = default_calculated_size + size_offset_pts
                        
                        print(f"  Final Font Size: {final_fontsize:.2f}pts, Font Name: {font_key}")
                        
                        # Add the redaction annotation
                        redact_area = fitz.Rect(inst)
                        page.add_redact_annot(redact_area)
                        redaction_applied = True
                        
                        # Calculate insertion position (top-left point)
                        top_left_point = fitz.Point(inst.tl.x, inst.tl.y + inst.height * offset_multiplier)
                        
                        # Store the insertion details
                        insert_data.append({
                            'point': top_left_point, 
                            'text': new_text,
                            'fontsize': final_fontsize,
                            'fontname': font_key # Pass the built-in font name
                        })
                        
                        replaced_count += 1
            
            # 2. Second Pass: Apply Redactions and Insert Text
            if redaction_applied:
                # A. Apply all redactions (This physically removes the old text)
                page.apply_redactions()

                # B. Insert the new text into the now-empty space
                for item in insert_data:
                    # Use insert_text, passing the fontname for built-in fonts
                    page.insert_text(
                        item['point'], 
                        item['text'], 
                        fontsize=item['fontsize'], 
                        fontname=item['fontname'] 
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

# ----------------------------------------------------------------------
## User Configuration
# ----------------------------------------------------------------------

# 1. Define the input and output file paths
INPUT_FILE = "original_document.pdf"
OUTPUT_FILE = "invoice_modified_offset_final.pdf" 

# 2. Define the exact text replacements.
REPLACEMENTS_CONFIG = [
    {
        "old_text": "Receipt", 
        "new_text": "Invoice", 
        "offset_multiplier": 0.8,
        # Now using the reliable built-in Helvetica Bold
        "font_to_use": "Helvetica-Bold", 
        "fontsize_offset_pts": 0
    },
    {
        "old_text": "Andrew Johson", 
        "new_text": "Christan Versteeg", 
        "offset_multiplier": 0.8,
        # Now using the reliable built-in Helvetica Regular
        "font_to_use": "helv",
        "fontsize_offset_pts": -1
    },
    {
        "old_text": "anicver@gmail.com", 
        "new_text": "chrisjaver@gmail.com", 
        "offset_multiplier": 0.8,
        # Now using the reliable built-in Helvetica Regular
        "font_to_use": "helv",
        "fontsize_offset_pts": -1
    }
]

# --- Execution ---
if __name__ == "__main__":
    replace_static_pdf_text(INPUT_FILE, OUTPUT_FILE, REPLACEMENTS_CONFIG)
