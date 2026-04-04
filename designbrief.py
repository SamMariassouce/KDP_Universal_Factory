import os
import re

def get_guide_metadata(folder):
    files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    if not files: return {}
    try:
        with open(os.path.join(folder, files[0]), 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception: return {}
    
    # Matches your specific Guide headers
    title_match = re.search(r"(?:GUIDE|TITLE PAGE)[—:\s]+(.*)", content, re.I)
    audience_match = re.search(r"Target audience[:\s]+(.*)", content, re.I)
    
    return {
        "title": title_match.group(1).strip() if title_match else "Journal",
        "audience": audience_match.group(1).strip() if audience_match else "General"
    }

def main():
    base_path = "."
    subfolders = [d for d in os.listdir(base_path) 
                  if os.path.isdir(os.path.join(base_path, d)) and not d.startswith('.')]

    for folder_name in subfolders:
        folder_path = os.path.join(base_path, folder_name)
        meta = get_guide_metadata(folder_path)
        title = meta.get('title')
        
        # Define the specific icon based on the folder name/title
        if "wine" in title.lower() or "tasting" in title.lower():
            icon_desc = "a single elegant gold foil silhouette of a grapevine leaf"
        else:
            icon_desc = "a single elegant minimalist gold foil icon representing the theme"

        # THE REFINED UNIVERSAL PROMPT
        prompt = (
            f"[Reference Name: background.png] Professional KDP Book Cover Background for '{title}'. "
            f"Style: Minimalist Premium. Color Palette: Deep Charcoal with a subtle paper texture and Matte Gold Foil accents. "
            f"Composition: {icon_desc}, centered and sized to occupy only the middle 30% of the canvas. "
            f"Layout: Ensure massive empty negative space on all sides (top, bottom, and edges) to allow for professional title typography. "
            f"High Resolution 300DPI. CRITICAL: NO TEXT, NO LETTERS, NO WORDS."
        )

        with open(os.path.join(folder_path, "cover_prompt.txt"), "w", encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"🎨 Optimized Brief created for: {title}")

if __name__ == "__main__":
    main()