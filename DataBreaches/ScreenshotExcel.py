import os
import math
import pandas as pd
from PIL import Image
from playwright.sync_api import sync_playwright
from pptx import Presentation
from pptx.util import Inches
from pptx.oxml import parse_xml

def excel_to_animated_slide(excel_filename="data.xlsx", output_pptx_name="excel_animated_slide.pptx", sheet_name=0):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, excel_filename)

    if not os.path.exists(excel_path):
        print(f"Error: Could not find '{excel_filename}' in {script_dir}")
        return

    # 1. Read Excel file
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    html_content = df.to_html(index=False, classes='excel-table')
    
    # CSS styled without sticky headers so it only appears once at the very top
    styled_html = f"""
    <html>
    <head>
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
                margin: 0; 
                padding: 0;
                background-color: #ffffff;
            }}
            table.excel-table {{
                border-collapse: collapse;
                width: 100%;
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

    temp_chunk_prefix = os.path.join(script_dir, "temp_chunk_")
    chunk_files = []

    # 2. Render and capture chunks via Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        viewport_width = 1920
        viewport_height = 2000
        
        page = browser.new_page(
            viewport={"width": viewport_width, "height": viewport_height},
            device_scale_factor=1.5
        )
        page.goto(f"file://{temp_html}")
        
        total_height = page.evaluate("document.body.scrollHeight")
        num_chunks = math.ceil(total_height / viewport_height)
        
        print(f"Total layout height: {total_height}px. Capturing {num_chunks} clean chunks...")

        for i in range(num_chunks):
            y_offset = i * viewport_height
            page.evaluate(f"window.scrollTo(0, {y_offset});")
            page.wait_for_timeout(200)
            
            chunk_path = f"{temp_chunk_prefix}{i}.png"
            page.screenshot(path=chunk_path)
            chunk_files.append(chunk_path)

        browser.close()

    # 3. Calculate exact proportions and total table height in inches
    target_slide_width_inches = 13.333
    slide_height_inches = 7.5
    
    chunk_dimensions = []
    total_table_height_inches = 0
    for cf in chunk_files:
        with Image.open(cf) as img:
            w, h = img.size
            img_height_inches = target_slide_width_inches * (h / w)
            chunk_dimensions.append((cf, img_height_inches))
            total_table_height_inches += img_height_inches

    # 4. Initialize presentation with standard widescreen layout
    prs = Presentation()
    prs.slide_width = Inches(target_slide_width_inches)
    prs.slide_height = Inches(slide_height_inches)
    
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 5. Import and position chunks edge-to-edge
    print("Importing, positioning, and grouping chunks...")
    shape_objects = []
    current_top = Inches(0)
    left_pos = Inches(0)

    for chunk_path, img_h in chunk_dimensions:
        pic = slide.shapes.add_picture(chunk_path, left_pos, current_top, width=Inches(target_slide_width_inches))
        shape_objects.append(pic)
        current_top += Inches(img_h)

    # Group all picture slices into a single master object
    group_shape = slide.shapes.add_group_shape(shape_objects)
    
    # Enforce ID and name mapping required by the animation XML
    group_shape._element.nvGrpSpPr.cNvPr.set('id', '32')
    group_shape._element.nvGrpSpPr.cNvPr.set('name', 'Group 31')

    # 6. Dynamically calculate cumulative scroll paths across 100 sequential parts (59s each)
    scroll_ratio = max(0.0, (total_table_height_inches - slide_height_inches) / slide_height_inches)
    num_steps = 100
    step_ratio = scroll_ratio / num_steps
    dur_per_step = 59000  # Max 59 seconds per segment

    print(f"Total scroll ratio: {scroll_ratio:.4f} (Split into {num_steps} cumulative steps)")

    # Generate the 100 cumulatively linked click-triggered animation blocks
    anim_blocks_xml = ""
    for i in range(num_steps):
        node_id = 5 + (i * 2)
        bhvr_id = 6 + (i * 2)
        
        start_val = i * step_ratio
        end_val = (i + 1) * step_ratio
        
        anim_blocks_xml += f"""
        <p:par>
            <p:cTn id="{node_id}" presetID="42" presetClass="path" presetSubtype="0" accel="0" decel="0" fill="hold" nodeType="clickEffect">
                <p:stCondLst>
                    <p:cond delay="0"/>
                </p:stCondLst>
                <p:childTnLst>
                    <p:animMotion origin="layout" path="M 0 -{start_val:.4f} L 0 -{end_val:.4f} E" pathEditMode="relative" ptsTypes="">
                        <p:cBhvr>
                            <p:cTn id="{bhvr_id}" dur="{dur_per_step}" fill="hold"/>
                            <p:tgtEl>
                                <p:spTgt spid="32"/>
                            </p:tgtEl>
                            <p:attrNameLst>
                                <p:attrName>ppt_x</p:attrName>
                                <p:attrName>ppt_y</p:attrName>
                            </p:attrNameLst>
                        </p:cBhvr>
                    </p:animMotion>
                </p:childTnLst>
            </p:cTn>
        </p:par>
        """

    # 7. Inject the complete Animation XML structure with click-ready sequence configuration
    timing_xml = f"""
    <p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
        <p:tnLst>
            <p:par>
                <p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
                    <p:childTnLst>
                        <p:seq concurrent="1" nextAc="seek">
                            <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
                                <p:childTnLst>
                                    <p:par>
                                        <p:cTn id="3" fill="hold">
                                            <p:stCondLst>
                                                <p:cond delay="indefinite"/>
                                            </p:stCondLst>
                                            <p:childTnLst>
                                                <p:par>
                                                    <p:cTn id="4" fill="hold">
                                                        <p:stCondLst>
                                                            <p:cond delay="0"/>
                                                        </p:stCondLst>
                                                        <p:childTnLst>
                                                            {anim_blocks_xml}
                                                        </p:childTnLst>
                                                    </p:cTn>
                                                </p:par>
                                            </p:childTnLst>
                                        </p:cTn>
                                    </p:par>
                                </p:childTnLst>
                            </p:cTn>
                        </p:seq>
                    </p:childTnLst>
                </p:cTn>
            </p:par>
        </p:tnLst>
    </p:timing>
    """
    timing_element = parse_xml(timing_xml)
    slide._element.append(timing_element)

    # Save presentation
    output_pptx_path = os.path.join(script_dir, output_pptx_name)
    prs.save(output_pptx_path)

    # Clean up temporary chunk files and html
    for cf in chunk_files:
        if os.path.exists(cf):
            os.remove(cf)
    if os.path.exists(temp_html):
        os.remove(temp_html)

    print(f"Success! Cumulative 100-step slide saved to: {output_pptx_path}")

if __name__ == "__main__":
    excel_to_animated_slide("data.xlsx", "excel_animated_slide.pptx")