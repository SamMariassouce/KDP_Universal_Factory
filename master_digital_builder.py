import fitz  # PyMuPDF for links
import os

# 1. DEFINE THE BUTTON MAPS FOR YOUR 4 SVGS
# Coordinates: [x0, y0, x1, y1]
LINK_MAPS = {
    "welcome.svg": [
        {"rect": [450, 700, 550, 750], "target_page": 1}  # Link to Inventory
    ],
    "inventory.svg": [
        {"rect": [50, 20, 150, 50], "target_page": 0},    # Back to Welcome
        {"rect": [450, 20, 550, 50], "target_page": 2}    # Start Logs
    ],
    "tasting_log.svg": [
        {"rect": [520, 10, 580, 40], "target_page": 1},   # Back to Inventory Tab
        {"rect": [520, 50, 580, 80], "target_page": 0}    # Home Tab
    ]
}

def build_integrated_planner(pdf_input, guide_path):
    doc = fitz.open(pdf_input)
    
    # 2. READ ASSEMBLY GUIDE TO KNOW WHICH SVG IS ON WHICH PAGE
    with open(guide_path, 'r') as f:
        pages_setup = f.readlines() # e.g., ["welcome.svg", "inventory.svg", ...]

    for i, page in enumerate(doc):
        template_name = pages_setup[i].strip().lower()
        
        # 3. APPLY THE CORRECT BUTTONS
        if template_name in LINK_MAPS:
            for link in LINK_MAPS[template_name]:
                page.insert_link({
                    "kind": fitz.LINK_GOTO,
                    "from": fitz.Rect(link["rect"]),
                    "page": link["target_page"]
                })

    output_name = pdf_input.replace(".pdf", "_FINAL_DIGITAL.pdf")
    doc.save(output_name)
    print(f"✅ Created: {output_name}")

# Run: build_integrated_planner("wine_journal_assembled.pdf", "assembly_guide.txt")