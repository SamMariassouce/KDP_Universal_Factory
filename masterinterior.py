import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

def draw_header(can, title, width, height):
    """Draws the consistent title at the top of every page """
    can.setFont("Helvetica-Bold", 14)
    can.setFillColor(colors.black)
    # Positions the Title: THE KOREAN CALLIGRAPHY JOURNAL [cite: 1]
    can.drawCentredString(width / 2, height - 50, title.upper())
    can.setStrokeColor(colors.black)
    can.setLineWidth(1)
    can.line(72, height - 60, width - 72, height - 60)

def draw_grid_layout(can, width, height):
    """GRID: Draws the actual calligraphy practice boxes"""
    grid_size = 60 # Large boxes for calligraphy practice
    can.setStrokeColor(colors.lightgrey)
    can.setLineWidth(0.5)
    
    # Starting positions to leave margins
    margin_x = 72
    margin_y = 100
    
    for x in range(margin_x, int(width - margin_x), grid_size):
        for y in range(margin_y, int(height - 120), grid_size):
            # Draw the main square
            can.setDash(1, 0)
            can.rect(x, y, grid_size, grid_size)
            
            # Draw the internal 'cross-hair' guides for centering characters
            can.setDash(1, 2) 
            can.line(x + grid_size/2, y, x + grid_size/2, y + grid_size) # Vertical guide
            can.line(x, y + grid_size/2, x + grid_size, y + grid_size/2) # Horizontal guide

def create_interior():
    print("\n--- BLISSITY: SMART INTERIOR ENGINE ---")
    raw_path = input("Drag and drop the book FOLDER: ").strip()
    folder_path = raw_path.replace("'", "").replace('"', "").replace("\\ ", " ")
    
    # The Brain: Keyword detection for your 100 niches
    niche_map = {
        "grid": ["calligraphy", "korean", "japanese", "chinese", "kanji", "practice"],
        "log": ["wine", "coffee", "whiskey", "tasting", "review"],
        "tracker": ["exercise", "fitness", "food", "workout"]
    }

    niche_input = input("What is the Niche? (e.g. Korean): ").strip().lower()
    title = input("Enter the Book Title: ").strip() # e.g. THE KOREAN CALLIGRAPHY JOURNAL [cite: 1]

    # Smart Logic to pick the layout
    chosen_layout = "log" 
    for layout, keywords in niche_map.items():
        if any(word in niche_input for word in keywords):
            chosen_layout = layout
            break

    output_path = os.path.join(folder_path, f"{title.replace(' ', '_')}_Interior.pdf")
    can = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    print(f"🚀 Generating 100-page {chosen_layout.upper()} interior...")

    for i in range(1, 101): # Generate exactly 100 pages 
        draw_header(can, title, width, height)
        
        if chosen_layout == "grid":
            draw_grid_layout(can, width, height)
        else:
            # Fallback text if layout isn't grid
            can.setFont("Helvetica", 12)
            can.drawCentredString(width / 2, height / 2, "Template Content Placeholder")
            
        can.showPage()

    can.save()
    print(f"\n✅ SUCCESS: Created {output_path}")

if __name__ == "__main__":
    create_interior()
    