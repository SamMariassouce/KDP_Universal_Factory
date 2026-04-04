import fitz

def get_percentage_coords(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0] # We test on the first page
    w, h = page.rect.width, page.rect.height
    
    print(f"\n--- BLISSITY COORDINATE FINDER ---")
    print(f"Target PDF: {pdf_path}")
    print(f"Detected Size: {w}pt x {h}pt") # Usually 612x792 or similar
    print("-" * 34)
    
    try:
        user_x = float(input("Enter X from your PDF viewer: "))
        user_y = float(input("Enter Y from your PDF viewer: "))
        
        # This calculates the 0.0 to 1.0 percentage
        perc_x = round(user_x / w, 3)
        perc_y = round(user_y / h, 3)
        
        print(f"\n✅ SUCCESS! Use these numbers in your digitalplanner.py:")
        print(f"x_percent: {perc_x}")
        print(f"y_percent: {perc_y}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Ensure this matches your filename exactly
    get_percentage_coords("PDF the 90 day wine.pdf")