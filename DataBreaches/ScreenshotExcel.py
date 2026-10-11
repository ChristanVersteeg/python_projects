import os
import math
import pandas as pd
from PIL import Image
from playwright.sync_api import sync_playwright

def excel_to_stitched_screenshot(excel_filename="data.xlsx", output_image_path="excel_screenshot.png", sheet_name=0):
    """
    Takes an Excel file, converts it to HTML, and stitches together multiple 
    viewport screenshots to avoid Chromium's maximum height limitation.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, excel_filename)

    if not os.path.exists(excel_path):
        print(f"Error: Could not find '{excel_filename}' in {script_dir}")
        return

    # 1. Read Excel file
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    html_content = df.to_html(index=False, classes='excel-table')
    
    # 2. Generate styled HTML representation
    styled_html = f"""
    <html>
    <head>
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
                margin: 0; 
                padding: 20px;
                background-color: #ffffff;
            }}
            table.excel-table {{
                border-collapse: collapse;
                width: max-content;
                font-size: 13px;
                color: #333333;
            }}
            table.excel-table th, table.excel-table td {{
                border: 1px solid #d0d7de;
                padding: 8px 12px;
                text-align: left;
                white-space: nowrap;
            }}
            table.excel-table th {{
                background-color: #f6f8fa;
                font-weight: 600;
                position: sticky;
                top: 0;
                z-index: 10;
            }}
            table.excel-table tr:nth-child(even) {{
                background-color: #fcfcfc;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    temp_html = os.path.join(script_dir, "temp_excel_view.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(styled_html)

    output_path = os.path.join(script_dir, output_image_path)
    temp_chunk_prefix = os.path.join(script_dir, "temp_chunk_")

    # 3. Use Playwright to capture the page chunk by chunk
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        viewport_width = 1600
        viewport_height = 2000  # Large viewport height per chunk
        
        page = browser.new_page(viewport={"width": viewport_width, "height": viewport_height})
        page.goto(f"file://{temp_html}")
        
        # Get total dimensions of the rendered page content
        total_width = page.evaluate("document.body.scrollWidth")
        total_height = page.evaluate("document.body.scrollHeight")
        
        print(f"Spreadsheet layout size: {total_width}x{total_height}px. Processing chunks...")

        # Calculate how many chunks we need
        num_chunks = math.ceil(total_height / viewport_height)
        chunk_files = []

        for i in range(num_chunks):
            y_offset = i * viewport_height
            # Scroll down to the specific chunk location
            page.evaluate(f"window.scrollTo(0, {y_offset});")
            
            # Brief pause to let any rendering settle
            page.wait_for_timeout(200)
            
            chunk_path = f"{temp_chunk_prefix}{i}.png"
            page.screenshot(path=chunk_path)
            chunk_files.append(chunk_path)

        browser.close()

    # 4. Stitch the chunks together using Pillow
    print("Stitching chunks together into a single master image...")
    images = [Image.open(cf) for cf in chunk_files]
    
    # Final image dimensions
    final_width = images[0].width
    final_height = sum(img.height for img in images)
    
    master_image = Image.new("RGB", (final_width, final_height))
    
    current_y = 0
    for img in images:
        master_image.paste(img, (0, current_y))
        current_y += img.height

    # Save final composite screenshot
    master_image.save(output_path, "PNG")

    # Clean up temporary chunk images and html file
    for cf in chunk_files:
        if os.path.exists(cf):
            os.remove(cf)
    if os.path.exists(temp_html):
        os.remove(temp_html)

    print(f"Success! Stitched full screenshot saved to: {output_path}")

if __name__ == "__main__":
    excel_to_stitched_screenshot("data.xlsx", "excel_screenshot.png")