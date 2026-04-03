import os
import re
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

def get_val(folder, keyword):
    """Searches the .txt guide for numbers like Trim Size or Margins"""
    files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    if not files: return None
    with open(os.path.join(folder, files[0]), 'r', encoding='utf-8') as f:
        content = f.read()
    # Find decimal or integer after the keyword
    pattern = rf"{keyword}.*?(\d+\.?\d*)"
    match = re.search(pattern, content, re.IGNORECASE)
    return float(match.group(1)) if match else None

def get_text_block(folder, section_keyword):
    """Extracts text sections from the guide based on Page markers"""
    files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    if not files: return ""
    with open(os.path.join(folder, files[0]), 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = {
        "TITLE": ("PAGE 1", "PAGE 2"),
        "COPYRIGHT": ("PAGE 2", "PAGE 3"),
        "HOW_TO_USE": ("PAGE 3", "PAGE 4"),
        "THANK_YOU": ("LAST PAGE", "====")
    }
    try:
        start_key, end_key = sections[section_keyword]
        text_block = content.split(start_key)[1].split(end_key)[0]
        # Clean up dashed lines and instructions
        lines = [l for l in text_block.split('\n') if "---" not in l and "Affinity" not in l and l.strip() != ""]
        return "\n\n".join(lines)
    except:
        return ""

def create_text_page(c, W, H, margin_x, title, body_text, is_title=False):
    """Draws a professional text page using margins from the guide"""
    c.setFont("Helvetica-Bold", 22)
    if not is_title:
        c.drawCentredString(W/2, H - 100, title)
    
    c.setFont("Helvetica", 11 if not is_title else 14)
    line_height = 18
    width_limit = W - (margin_x * 2)
    
    if is_title:
        # Centered layout for Title Page
        current_y = H - 200
        for line in body_text.split('\n\n'):
            wrapped = simpleSplit(line.strip(), "Helvetica", 14, width_limit)
            for w_line in wrapped:
                c.drawCentredString(W/2, current_y, w_line)
                current_y -= 22
            current_y -= 10
    else:
        # Paragraph layout for Interior pages
        text_object = c.beginText(margin_x, H - 160)
        text_object.setLeading(line_height)
        for para in body_text.split('\n\n'):
            wrapped = simpleSplit(para.replace('\n', ' ').strip(), "Helvetica", 11, width_limit)
            for line in wrapped:
                text_object.textLine(line)
            text_object.textLine("") 
        c.drawText(text_object)
    c.showPage()

def draw_template(c, folder, svg_pattern, p_num, W, H, GUTTER, OUTSIDE):
    """Finds an SVG by keyword and draws it with alternating Gutter margins"""
    all_files = os.listdir(folder)
    # Finds any file containing the keyword (e.g., 'inventory')
    svg_file = next((f for f in all_files if svg_pattern in f.lower() and f.endswith('.svg')), None)
    
    if svg_file:
        drawing = svg2rlg(os.path.join(folder, svg_file))
        scale = (W - GUTTER - OUTSIDE) / drawing.width
        drawing.width *= scale
        drawing.height *= scale
        drawing.scale(scale, scale)
        
        # Alternating margins: Odd = Left Gutter, Even = Right Gutter
        x_offset = GUTTER if p_num % 2 != 0 else OUTSIDE
        renderPDF.draw(drawing, c, x_offset, (H - drawing.height) / 2)
    c.showPage()

def main():
    print("\n--- BLISSITY PUBLICATIONS: UNIVERSAL ASSEMBLY ENGINE ---")
    raw_path = input("Drag and drop the book folder here, then press Enter: ").strip()
    # Clean the path (removes extra quotes or backslashes Mac adds on drag-and-drop)
    folder_path = raw_path.replace("'", "").replace('"', "").replace("\\ ", " ")
    
    if not os.path.isdir(folder_path):
        print(f"Error: Could not find folder at {folder_path}")
        return

    # 1. READ SETTINGS DYNAMICALLY FROM THE GUIDE
    width_in = get_val(folder_path, "Trim size") or 8.5
    # Height is usually fixed at 11 or 9, but we can pull it if listed
    height_in = 11.0 if width_in > 7 else 9.0 
    
    gutter_in = get_val(folder_path, r"Inside (gutter)") or 0.5
    outside_in = get_val(folder_path, "Outside") or 0.375
    
    # Convert inches to points
    W, H = width_in * 72, height_in * 72
    GUTTER, OUTSIDE = gutter_in * 72, outside_in * 72
    
    output_name = os.path.basename(folder_path.rstrip('/')) + "_Interior.pdf"
    output_path = os.path.join(folder_path, output_name)
    
    c = canvas.Canvas(output_path, pagesize=(W, H))
    print(f"Processing: {width_in}x{height_in} book...")

    # 2. RUN ASSEMBLY
    # Page 1-3: Fixed Text Pages
    create_text_page(c, W, H, GUTTER, "", get_text_block(folder_path, "TITLE"), True)
    create_text_page(c, W, H, GUTTER, "Copyright", get_text_block(folder_path, "COPYRIGHT"))
    create_text_page(c, W, H, GUTTER, "How to Use This Journal", get_text_block(folder_path, "HOW_TO_USE"))

    # Pages 4-182: The Templates (Looking for keywords in filenames)
    for p in range(4, 19): draw_template(c, folder_path, "inventory", p, W, H, GUTTER, OUTSIDE)
    for p in range(19, 159): draw_template(c, folder_path, "tasting", p, W, H, GUTTER, OUTSIDE)
    for p in range(159, 169): draw_template(c, folder_path, "comparison", p, W, H, GUTTER, OUTSIDE)
    for p in range(169, 183): draw_template(c, folder_path, "acquisition", p, W, H, GUTTER, OUTSIDE)

    # Final Page: Thank You
    create_text_page(c, W, H, GUTTER, "Thank You", get_text_block(folder_path, "THANK_YOU"))

    c.save()
    print(f"SUCCESS: Created {output_name} inside the book folder.")

if __name__ == "__main__":
    main()