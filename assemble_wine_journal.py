import os
import re
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

PAGE_WIDTH = 8.5 * 72
PAGE_HEIGHT = 11 * 72
GUTTER_MARGIN = 0.5 * 72
OUTSIDE_MARGIN = 0.375 * 72

def build_book():
    output_filename = "Finished_Wine_Journal.pdf"
    c = canvas.Canvas(output_filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    # Looking for your SVG files based on your 'ls' output
    templates = [
        "the-90-day-tasting-wine-journal-wine-cellar-inventory-template.svg",
        "the-90-day-tasting-wine-journal-monthly-acquisition-template.svg",
        "the-90-day-tasting-wine-journal-vintage-comparison-template.svg",
        "the-90-day-tasting-wine-journal-detailed-tasting-template.svg"
    ]
    
    print("Starting assembly of your 184-page journal...")
    
    current_page = 1
    # Simple logic: 1 Intro, 1 Monthly, 1 Vintage, then 181 Tasting pages
    # You can adjust these numbers later!
    for i, svg_path in enumerate(templates):
        if os.path.exists(svg_path):
            drawing = svg2rlg(svg_path)
            # Scale to fit
            factor = (PAGE_WIDTH - (GUTTER_MARGIN + OUTSIDE_MARGIN)) / drawing.width
            drawing.width *= factor
            drawing.height *= factor
            drawing.scale(factor, factor)
            
            # If it's the last template (Tasting), repeat it 181 times
            repeats = 181 if i == 3 else 1
            
            for _ in range(repeats):
                x_offset = GUTTER_MARGIN if current_page % 2 != 0 else OUTSIDE_MARGIN
                renderPDF.draw(drawing, c, x_offset, (PAGE_HEIGHT - drawing.height) / 2)
                c.showPage()
                current_page += 1
        else:
            print(f"Skipping missing file: {svg_path}")

    c.save()
    print(f"SUCCESS! Created {output_filename} with {current_page-1} pages.")

if __name__ == "__main__":
    build_book()
