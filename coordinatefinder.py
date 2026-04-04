import fitz  # PyMuPDF

def find_my_coordinates(pdf_path, page_num=0):
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    
    # This prints the size of your page (usually 612 x 792 for Letter)
    print(f"Page Size: {page.rect.width} x {page.rect.height}")
    print("--- INSTRUCTIONS ---")
    print("Open your PDF in a viewer like Preview (Mac) or Acrobat.")
    print("Hover your mouse over the buttons. The top-left is (x0, y0).")
    print("The bottom-right is (x1, y1).")

find_my_coordinates("PDF_the_90_day_wine.pdf")