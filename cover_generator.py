import os
import re
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader

def get_val(folder, keyword):
    """Finds values in the assembly guide .txt file"""
    files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    if not files: return None
    with open(os.path.join(folder, files[0]), 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = rf"{keyword}.*?(\d+\.?\d*)"
    match = re.search(pattern, content, re.IGNORECASE)
    return float(match.group(1)) if match else None

def generate_cover():
    print("\n--- BLISSITY PUBLICATIONS: COVER ENGINE ---")
    raw_path = input("Drag and drop the book FOLDER here: ").strip()
    # Clean the path for Mac
    folder_path = raw_path.replace("'", "").replace('"', "").replace("\\ ", " ")
    
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a folder. Please drag the folder icon.")
        return

    # 1. Get dimensions from Guide
    width_in = get_val(folder_path, "Trim size") or 8.5
    height_in = 11.0 # Standard height
    
    # 2. Find the Interior PDF to count pages
    interior_pdf = next((f for f in os.listdir(folder_path) if f.endswith('_Interior.pdf')), None)
    if not interior_pdf:
        print("Error: Could not find an '_Interior.pdf' in that folder. Build the interior first!")
        return
    
    reader = PdfReader(os.path.join(folder_path, interior_pdf))
    page_count = len(reader.pages)
    
    # 3. KDP Math for White Paper
    spine_width = page_count * 0.00225
    bleed = 0.125
    
    total_w = (width_in * 2) + spine_width + (bleed * 2)
    total_h = height_in + (bleed * 2)
    
    output_path = os.path.join(folder_path, "Final_KDP_Cover.pdf")
    # Convert inches to points (1 inch = 72 points)
    c = canvas.Canvas(output_path, pagesize=(total_w * 72, total_h * 72))
    
    # 4. Draw Layout
    # Black Background
    c.setFillColorRGB(0.05, 0.05, 0.05)
    c.rect(0, 0, total_w * 72, total_h * 72, fill=1)
    
    # Draw Spine Zone (Gray)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    spine_start = (bleed + width_in) * 72
    c.rect(spine_start, bleed * 72, spine_width * 72, height_in * 72, fill=1)
    
    # 5. Add Title to Front Cover (Right Side)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 36)
    # Center of the front panel
    front_center = (bleed + width_in + spine_width + (width_in / 2)) * 72
    c.drawCentredString(front_center, (total_h / 2) * 72, "WINE JOURNAL")
    
    c.save()
    print(f"\nSUCCESS: Cover created for {page_count} pages.")
    print(f"File saved to: {output_path}")

if __name__ == "__main__":
    generate_cover()