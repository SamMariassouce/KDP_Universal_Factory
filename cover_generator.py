import os
import re
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader

def get_val(folder, keyword):
    files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    if not files: return None
    with open(os.path.join(folder, files[0]), 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = rf"{keyword}.*?(\d+\.?\d*)"
    match = re.search(pattern, content, re.IGNORECASE)
    return float(match.group(1)) if match else None

def generate_base_cover():
    print("\n--- BLISSITY PUBLICATIONS: KDP BASE COVER ENGINE ---")
    raw_path = input("Drag and drop the book FOLDER here: ").strip()
    folder_path = raw_path.replace("'", "").replace('"', "").replace("\\ ", " ")
    
    if not os.path.isdir(folder_path):
        print(f"❌ Error: {folder_path} is not a folder.")
        return

    # 1. Get dimensions & page count
    width_in = get_val(folder_path, "Trim size") or 8.5
    height_in = 11.0 
    
    interior_pdf = next((f for f in os.listdir(folder_path) if f.endswith('_Interior.pdf')), None)
    if interior_pdf:
        reader = PdfReader(os.path.join(folder_path, interior_pdf))
        page_count = len(reader.pages)
    else:
        page_count = get_val(folder_path, "Target pages") or 184
    page_count = int(page_count)
    
    # 2. KDP Math
    spine_width = page_count * 0.00225
    bleed = 0.125
    
    total_w_pts = ((width_in * 2) + spine_width + (bleed * 2)) * 72
    total_h_pts = (height_in + (bleed * 2)) * 72
    
    # Let's also print the exact dimensions for Canva!
    canva_w_in = (total_w_pts / 72)
    canva_h_in = (total_h_pts / 72)
    
    output_path = os.path.join(folder_path, "Base_KDP_Cover_For_Canva.pdf")
    c = canvas.Canvas(output_path, pagesize=(total_w_pts, total_h_pts))
    
    # 3. Draw Background & Spine
    c.setFillColorRGB(0.05, 0.05, 0.05) # Dark Charcoal Base
    c.rect(0, 0, total_w_pts, total_h_pts, fill=1, stroke=0)
    
    # 4. Place the AI Background Image
    bg_img_path = os.path.join(folder_path, "background.png")
    front_start_pts = ((bleed + width_in) * 72) + (spine_width * 72)
    front_w_pts = (width_in + bleed) * 72
    
    if os.path.exists(bg_img_path):
        c.drawImage(bg_img_path, front_start_pts, 0, width=front_w_pts, height=total_h_pts, preserveAspectRatio=False)
    else:
        print("⚠️ 'background.png' not found. Creating a blank cover.")

    c.save()
    print(f"\n✅ SUCCESS: Text-Free Base Cover created!")
    print(f"📐 CANVA DIMENSIONS: {canva_w_in:.3f} x {canva_h_in:.3f} inches")
    print(f"File saved to: {output_path}")

if __name__ == "__main__":
    generate_base_cover()