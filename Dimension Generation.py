import re

def generate_dimensions_from_file(filename):
    try:
        with open(filename, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: '{filename}' not found. Place it in this folder.")
        return

    # Regex to pull Title, Pages, and Trim from your KDP format
    pattern = r"Book \d+ — (.*?) — TYPE A.*?Pages: (\d+).*?PAPERBACK_(\d+\.\d+)x(\d+\.\d+)"
    matches = re.findall(pattern, content, re.DOTALL)

    if not matches:
        print("No books found. Check if the file content matches your KDP checklist format.")
        return

    with open("final_book_dimensions.txt", "w") as out:
        out.write("BOOK COVER PRODUCTION DIMENSIONS (Includes Bleed)\n")
        out.write("=" * 60 + "\n\n")

        for title, pages, w, h in matches:
            p, w, h = int(pages), float(w), float(h)
            
            # Spine calculation for White Paper
            spine = p * 0.00225 
            
            # Paperback: Trim + Spine + 0.125" Bleed per side
            pb_w = 0.125 + w + spine + w + 0.125
            pb_h = 0.125 + h + 0.125
            
            # Hardcover: Trim + Spine + 0.563" Wrap per side
            hc_w = 0.563 + w + spine + w + 0.563
            hc_h = 0.563 + h + 0.563
            
            out.write(f"TITLE: {title.strip()}\n")
            out.write(f"  - Kindle:    1600 x 2560 px\n")
            out.write(f"  - Paperback: {round(pb_w, 4)}\" x {round(pb_h, 4)}\" (Spine: {round(spine, 4)}\")\n")
            out.write(f"  - Hardcover: {round(hc_w, 4)}\" x {round(hc_h, 4)}\"\n")
            out.write("-" * 50 + "\n")

    print(f"Success! Processed {len(matches)} books into 'final_book_dimensions.txt'.")

# Execute using your specific filename
generate_dimensions_from_file("cover-template-checklist.txt")