import os
import re
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader

def get_val(folder, keyword):
    files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    if not files: return None
    for file in files:
        with open(os.path.join(folder, file), 'r', encoding='utf-8') as f:
            content = f.read()
        pattern = rf"{keyword}.*?(\d+\.?\d*)"
        match = re.search(pattern, content, re.IGNORECASE)
        if match: return float(match.group(1))
    return None

def generate_hardcover():
    print("\n--- BLISSITY: HARDCOVER ENGINE (NO-STRETCH) ---")
    raw_path = input("Drag and drop the book FOLDER: ").strip()
    folder_path = raw_path.replace("'", "").replace('"', "").replace("\\ ", " ")
    
    if not os.path.isdir(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return

    # 1. Dimensions
    width_in = 8.5  # Matching your paperback
    height_in = 11.0 
    
    interior_pdf = next((f for f in os.listdir(folder_path) if f.endswith('_Interior.pdf')), None)
    if interior_pdf:
        page_count = len(PdfReader(os.path.join(folder_path, interior_pdf)).pages)
    else:
        page_count = int(get_val(folder_path, "Target pages") or 184)

    # 2. Hardcover Math
    spine_w = page_count * 0.00225 
    wrap = 0.591    
    hinge = 0.394   
    overhang = 0.118 
    
    total_w = (width_in * 2) + spine_w + (hinge * 2) + (wrap * 2)
    total_h = height_in + (overhang * 2) + (wrap * 2)
    
    output_path = os.path.join(folder_path, "Final_Hardcover_Ready.pdf")
    c = canvas.Canvas(output_path, pagesize=(total_w * 72, total_h * 72))
    
    # 3. Find Image
    bg_img = None
    for f in os.listdir(folder_path):
        if f.lower() in ['background.jpg', 'background.png', 'background.jpeg']:
            bg_img = os.path.join(folder_path, f)
            break

    if bg_img:
        # THE FIX: We draw the image across the ENTIRE canvas.
        # This prevents the "squeezing" into the front board.
        c.drawImage(bg_img, 0, 0, width=total_w * 72, height=total_h * 72, preserveAspectRatio=False)
        print(f"✅ Image applied correctly across full spread.")
    else:
        print("❌ Error: No background.jpg found in folder.")
        return

    c.save()
    print(f"\n🚀 DONE: {total_w:.3f} x {total_h:.3f} inches saved to folder.")

if __name__ == "__main__":
    generate_hardcover()