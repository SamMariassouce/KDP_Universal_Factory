import fitz  # PyMuPDF
import os
import glob

# --- SECTION 1: THE BRAIN (Universal Proportions) ---
# [x_start, y_start, width, height]
# These are percentages (0.0 to 1.0). 
# Adjust these numbers once to fit your SVG tabs perfectly.
BUTTON_PROPORTIONS = {
    "welcome.svg": [
        {"name": "Start", "rect": [0.4, 0.8, 0.2, 0.05], "target": 1}
    ],
    "inventory.svg": [
        {"name": "To Logs", "rect": [0.8, 0.05, 0.15, 0.05], "target": 2}
    ],
    "tasting_log.svg": [
        # Sidebar Tabs Example:
        {"name": "Tab_Inventory", "rect": [0.92, 0.1, 0.08, 0.1], "target": 1},
        {"name": "Tab_Home", "rect": [0.92, 0.25, 0.08, 0.1], "target": 0}
    ]
}

def process_hub():
    # Setup Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, "_TO_PROCESS")
    output_dir = os.path.join(base_dir, "_FINISHED_DIGITAL")

    print(f"\n--- 🚀 BLISSITY DIGITAL FACTORY STARTING ---")
    print(f"🔍 Checking Hub: {input_dir}")

    # Create folders if they are missing
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Find all subfolders in the In-Tray
    folders = [f for f in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, f))]
    
    if not folders:
        print("❌ No project folders found in _TO_PROCESS.")
        return

    print(f"📁 Found {len(folders)} project(s) to process.\n")

    for book_folder in folders:
        folder_path = os.path.join(input_dir, book_folder)
        all_files = os.listdir(folder_path)
        
        # FLEXIBLE SEARCH: Find ANY pdf and ANY txt guide
        pdfs = [f for f in all_files if f.lower().endswith(".pdf")]
        guides = [f for f in all_files if f.lower().endswith(".txt")]

        if pdfs and guides:
            target_pdf = os.path.join(folder_path, pdfs[0])
            target_guide = os.path.join(folder_path, guides[0])
            
            output_name = f"DIGITAL_{pdfs[0]}"
            save_path = os.path.join(output_dir, output_name)
            
            print(f"🛠️  Processing Folder: '{book_folder}'")
            print(f"   📄 Using PDF: {pdfs[0]}")
            print(f"   📝 Using Guide: {guides[0]}")
            
            inject_links(target_pdf, target_guide, save_path)
        else:
            print(f"⚠️  Skipping '{book_folder}': Missing a .pdf or a .txt guide.")

def inject_links(pdf_path, guide_path, save_path):
    try:
        doc = fitz.open(pdf_path)
        
        # Load the assembly guide (Blueprint)
        with open(guide_path, 'r', encoding='utf-8') as f:
            blueprint = [line.strip().lower() for line in f.readlines() if line.strip()]

        for i, page in enumerate(doc):
            w, h = page.rect.width, page.rect.height
            
            # Map the page to its original SVG template name
            # If the guide is shorter than the book, we default to the tasting log
            template_filename = blueprint[i] if i < len(blueprint) else "tasting_log.svg"

            # Check if we have buttons defined for this specific SVG
            if template_filename in BUTTON_PROPORTIONS:
                for btn in BUTTON_PROPORTIONS[template_filename]:
                    px, py, pw, ph = btn["rect"]
                    
                    # Convert Percentages -> PDF points (works for 6x9 AND 18x11.5)
                    link_rect = fitz.Rect(px*w, py*h, (px+pw)*w, (py+ph)*h)
                    
                    page.insert_link({
                        "kind": fitz.LINK_GOTO,
                        "from": link_rect,
                        "page": btn["target"]
                    })

        doc.save(save_path)
        doc.close()
        print(f"✅ SUCCESS: Created {os.path.basename(save_path)}\n")
    except Exception as e:
        print(f"❌ ERROR processing: {e}")

if __name__ == "__main__":
    process_hub()
    print(f"--- 🏁 FACTORY SHUTDOWN: ALL JOBS DONE ---")