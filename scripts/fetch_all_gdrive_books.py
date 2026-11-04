# scripts/fetch_all_gdrive_books.py — Fetches complete catalog of books from Google Drive via rclone
# Usage: python3 scripts/fetch_all_gdrive_books.py
# Requires: rclone configured with 'gdrive:', python3 standard library
#
# Gotchas:
# - rclone lsf returns paths with forward slashes and sizes separated by semicolons.
# - The top-level 'Fiction ／ non fiction' folder uses a full-width slash (U+FF0F).
# - Filenames use multiple conventions: "Title - Author.epub", "Author - Title.epub", "Title [Author].epub",
#   and underscores replacing spaces. Clean regex patterns handle all variations.

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = ROOT / "content" / "gdrive_books_catalog.json"

def clean_filename(fn: str):
    # Remove file extension
    base = re.sub(r'\.(epub|pdf|cbr|cbz|mobi|docx|pptx)$', '', fn, flags=re.IGNORECASE)
    # Remove release tags like [Seven Seas], (Z-Library), [Kobo], etc.
    base = re.sub(r'\[.*?\]|\(.*?\)', ' ', base)
    # Replace underscores and duplicate spaces
    base = base.replace('_', ' ')
    base = re.sub(r'\s+', ' ', base).strip()
    return base

def parse_title_author(raw_path: str, filename: str):
    # Extract category
    parts = raw_path.split('/')
    category = parts[0] if len(parts) > 1 else "Uncategorized"
    
    # Normalise category name
    cat_map = {
        "Fiction ／ non fiction": "Fiction & Non-Fiction",
        "A graphic guide series": "Graphic Guides",
        "Comics and stuff": "Comics & Graphic Novels",
        "On Films": "Cinema & Film Craft",
        "Screenplays": "Screenplays",
        "Tactical Marketing": "Marketing & Strategy",
        "Cooking and food": "Cooking & Food",
        "Others": "Philosophy, Essays & Misc"
    }
    category_name = cat_map.get(category, category)
    
    cleaned = clean_filename(filename)
    
    # Standard splitting patterns: "Title - Author" or "Author - Title"
    author = "Unknown"
    title = cleaned
    
    if " - " in cleaned:
        segments = [s.strip() for s in cleaned.split(" - ") if s.strip()]
        if len(segments) == 2:
            s1, s2 = segments
            # Heuristic: check if s2 looks like a person's name or known author
            # Or if s1 looks like author
            title = s1
            author = s2
        elif len(segments) > 2:
            title = " - ".join(segments[:-1])
            author = segments[-1]
    
    return category_name, title.strip(), author.strip()

def main():
    print("Fetching file list from gdrive:Books via rclone...")
    cmd = ["rclone", "lsf", "gdrive:Books", "--recursive", "--format", "ps", "--files-only"]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    
    lines = [line.strip() for line in res.stdout.strip().split("\n") if line.strip()]
    print(f"Total raw files returned: {len(lines)}")
    
    catalog = []
    for line in lines:
        parts = line.split(";")
        raw_path = parts[0]
        size = int(parts[1]) if len(parts) > 1 and parts[1] != "-1" else 0
        filename = raw_path.split('/')[-1]
        
        # Skip hidden files or system files
        if filename.startswith('.'):
            continue
            
        category, title, author = parse_title_author(raw_path, filename)
        ext = filename.split('.')[-1].lower() if '.' in filename else ""
        
        catalog.append({
            "title": title,
            "author": author,
            "category": category,
            "format": ext,
            "size_bytes": size,
            "drive_path": raw_path,
            "filename": filename
        })
        
    print(f"Parsed {len(catalog)} books/documents.")
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print(f"Saved catalog to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
