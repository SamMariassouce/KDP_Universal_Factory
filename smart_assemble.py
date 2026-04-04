import os
import re
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

# --- HELPER FUNCTIONS ---

def read_guide(folder):
    """Finds and reads the assembly guide text file in the folder."""
    files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    if not files: return None
    with open(os.path.join(folder, files[0]), 'r', encoding='utf-8') as f:
        return f.read()

def get_dims(content):
    """Extracts width and height from the 'Trim size' line."""
    match = re.search(r"Trim size:\s*(\d+\.?\d*)\s*x\s*(\d+\.?\d*)", content, re.IGNORECASE)
    if match:
        return float(match.group(1)), float(match.group(2))
    return 8.5, 11.0  # Fallback

def get_margin(content, keyword):
    """Extracts margins safely."""
    match = re.search(rf"{keyword}.*?(\d+\.?\d*)", content, re.IGNORECASE)
    return float(match.group(1)) if match else 0.375

def get_text_block(content, keyword):
    """Intelligently grabs the text block below a specific header."""
    pattern = rf"{keyword}.*?\n[-]+\n(.*?)(?=\n[-]+|\Z)"
    match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""

def get_layout(content):
    """Reads the 'PAGE STRUCTURE' block with high flexibility for formatting."""
    layout = []
    # Finds everything between 'PAGE STRUCTURE' and the next '===' separator
    structure_match = re.search(r"PAGE STRUCTURE.*?\n(.*?)(?:\=\=\=|\Z)", content, re.IGNORECASE | re.DOTALL)
    if not structure_match:
        return layout
        
    lines = structure_match.group(1).strip().split('\n')
    for line in lines:
        line = line.strip()
        # Only process lines that start with "Page" to avoid getting confused by notes
        if not line.lower().startswith("page"): 
            continue
        
        # Matches: "Page 1: Title" or "Pages 5-111: template.svg"
        m = re.match(r"Page(?:s)?\s+(\d+)(?:-(\d+))?[:\s-]+(.*)", line, re.IGNORECASE)
        if m:
            start = int(m.group(1))
            end = int(m.group(2)) if m.group(2) else start
            desc = m.group(3).strip()
            layout.append({"start": start, "end": end, "desc": desc})
    return layout

def create_text_page(c, W, H, margin_x, title, body_text, is_title=False):
    """Draws text and automatically paginates if the text runs off the page."""
    pages_used = 1
    c.setFont("Helvetica-Bold", 22)
    
    if not is_title:
        c.drawCentredString(W/2, H - 100, title)
        
    c.setFont("Helvetica", 11 if not is_title else 14)
    line_height = 18
    width_limit = W - (margin_x * 2)
    
    if is_title:
        current_y = H - 200
        for line in body_text.split('\n\n'):
            wrapped = simpleSplit(line.strip(), "Helvetica", 14, width_limit)
            for w_line in wrapped:
                c.drawCentredString(W/2, current_y, w_line)
                current_y -= 22
            current_y -= 10
        c.showPage()
    else:
        current_y = H - 160
        text_object = c.beginText(margin_x, current_y)
        text_object.setLeading(line_height)
        
        for para in body_text.split('\n\n'):
            wrapped = simpleSplit(para.replace('\n', ' ').strip(), "Helvetica", 11, width_limit)
            for line in wrapped:
                if current_y < 72: 
                    c.drawText(text_object)
                    c.showPage()
                    pages_used += 1
                    current_y = H - 72
                    c.setFont("Helvetica", 11)
                    text_object = c.beginText(margin_x, current_y)
                    text_object.setLeading(line_height)
                    
                text_object.textLine(line)
                current_y -= line_height
            text_object.textLine("") 
            current_y -= line_height
            
        c.drawText(text_object)
        c.showPage()
        
    return pages_used

def draw_template(c, folder, svg_pattern, p_num, W, H, GUTTER, OUTSIDE):
    """Finds and draws a specific SVG by checking if the pattern is in the filename."""
    all_files = os.listdir(folder)
    svg_file = next((f for f in all_files if svg_pattern.lower() in f.lower() and f.lower().endswith('.svg')), None)
    
    if svg_file:
        svg_path = os.path.join(folder, svg_file)
        drawing = svg2rlg(svg_path)
        
        if drawing is None:
            print(f"    ⚠️ ERROR: Found '{svg_file}' but svglib couldn't read it!")
        else:
            scale = (W - GUTTER - OUTSIDE) / drawing.width
            drawing.width *= scale
            drawing.height *= scale
            drawing.scale(scale, scale)
            x_offset = GUTTER if p_num % 2 != 0 else OUTSIDE
            renderPDF.draw(drawing, c, x_offset, (H - drawing.height) / 2)
    else:
        print(f"    ⚠️ WARNING: Missing SVG containing '{svg_pattern}' for Page {p_num}")
        
    c.showPage()

# --- THE BATCH MAIN LOOP ---

def main():
    print("\n--- BLISSITY PUBLICATIONS: BATCH ASSEMBLY ENGINE ---")
    raw_path = input("Drag and drop the CLAUDE COWORK folder here: ").strip()
    parent_folder = raw_path.replace("'", "").replace('"', "").replace("\\ ", " ")
    
    if not os.path.isdir(parent_folder):
        print(f"Error: Could not find folder at {parent_folder}")
        return

    subfolders = [os.path.join(parent_folder, f) for f in os.listdir(parent_folder) 
                  if os.path.isdir(os.path.join(parent_folder, f))]
    
    print(f"Found {len(subfolders)} books to process. Starting production...")

    for folder_path in subfolders:
        book_name = os.path.basename(folder_path)
        print(f"\n📦 Processing: {book_name}...")

        guide_content = read_guide(folder_path)
        if not guide_content:
            print(f"    ⚠️ SKIPPING: No assembly guide .txt file found.")
            continue

        width_in, height_in = get_dims(guide_content)
        gutter_in = get_margin(guide_content, r"Inside")
        outside_in = get_margin(guide_content, "Outside")
        
        W, H = width_in * 72, height_in * 72
        GUTTER, OUTSIDE = gutter_in * 72, outside_in * 72
        
        layout = get_layout(guide_content)
        if not layout:
            print(f"    ⚠️ SKIPPING: Could not find 'PAGE STRUCTURE' section.")
            continue

        output_name = f"{book_name}_Interior.pdf"
        output_path = os.path.join(folder_path, output_name)
        c = canvas.Canvas(output_path, pagesize=(W, H))

        for item in layout:
            start, end = item['start'], item['end']
            desc = item['desc'].lower()
            
            if ".svg" in desc:
                # Extract the SVG name even if there are parentheses around it
                svg_match = re.search(r"([a-zA-Z0-9_-]+\.svg)", item['desc'], re.IGNORECASE)
                svg_pattern = svg_match.group(1) if svg_match else desc
                for p in range(start, end + 1):
                    draw_template(c, folder_path, svg_pattern, p, W, H, GUTTER, OUTSIDE)
            elif "title" in desc:
                pages_used = create_text_page(c, W, H, GUTTER, "", get_text_block(guide_content, "TITLE"), True)
                for p in range(start + pages_used, end + 1): c.showPage()
            elif "copyright" in desc:
                pages_used = create_text_page(c, W, H, GUTTER, "Copyright", get_text_block(guide_content, "COPYRIGHT"))
                for p in range(start + pages_used, end + 1): c.showPage()
            elif "how to use" in desc:
                pages_used = create_text_page(c, W, H, GUTTER, "How to Use", get_text_block(guide_content, "HOW TO USE"))
                for p in range(start + pages_used, end + 1): c.showPage()
            elif "thank you" in desc:
                pages_used = create_text_page(c, W, H, GUTTER, "Thank You", get_text_block(guide_content, "THANK YOU"))
                for p in range(start + pages_used, end + 1): c.showPage()
            else:
                for p in range(start, end + 1): c.showPage()

        c.save()
        print(f"✅ Created: {output_name} ({width_in}x{height_in}, {end} pages)")

    print("\n🚀 ALL BOOKS COMPLETE. Batch factory finished.")

if __name__ == "__main__":
    main()