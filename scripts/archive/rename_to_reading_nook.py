# rename_to_reading_nook.py — Standardizes 'Nooks Reader' / 'Read on Nooks' to 'Reading Nook'
# Usage: python3 scripts/rename_to_reading_nook.py
# Requires: Python 3.8+ (standard library only)
#
# Gotchas:
# - Replaces user-facing strings in build_independent_bookshelf_app.py first,
#   then builds bookshelf/index.html and docs/bookshelf.html to keep them 100% in sync.
# - Also updates bookshelf/reader.html and docs/reader.html for any stray 'Nooks' or 'Nook specializes'.

import os
import subprocess

def main():
    print("Renaming Nooks Reader references to Reading Nook...")
    
    # 1. Update scripts/build_independent_bookshelf_app.py
    build_script = os.path.abspath("scripts/build_independent_bookshelf_app.py")
    with open(build_script, "r", encoding="utf-8") as f:
        content = f.read()

    replacements = [
        ("title=\"Open Nooks Reader in Reading Room (open any EPUB directly)\"", "title=\"Open Reading Nook in Reading Room (open any EPUB directly)\""),
        ("<span class=\"hidden 2xl:inline\">Open Nooks Reader</span>", "<span class=\"hidden 2xl:inline\">Open Reading Nook</span>"),
        ("<span class=\"hidden md:inline 2xl:hidden\">Nooks Reader</span>", "<span class=\"hidden md:inline 2xl:hidden\">Reading Nook</span>"),
        ("<span class=\"inline md:hidden\">Nooks</span>", "<span class=\"inline md:hidden\">Reading Nook</span>"),
        ("<span id=\"surpriseReadBtnLabel\">Read on Nooks ↗</span>", "<span id=\"surpriseReadBtnLabel\">Reading Nook ↗</span>"),
        ("<span>${{ (fmt === 'PDF') ? '📄 Open PDF ↗' : '📖 Read on Nooks ↗' }}</span>", "<span>${{ (fmt === 'PDF') ? '📄 Open PDF ↗' : '📖 Reading Nook ↗' }}</span>"),
        ("<span>${{ (b.format && b.format.toLowerCase() === 'pdf') ? 'Open PDF ↗' : 'Read on Nooks ↗' }}</span>", "<span>${{ (b.format && b.format.toLowerCase() === 'pdf') ? 'Open PDF ↗' : 'Reading Nook ↗' }}</span>"),
        ("readBtnLabel.innerText = isPdf ? \"Open PDF ↗\" : \"Read on Nooks ↗\";", "readBtnLabel.innerText = isPdf ? \"Open PDF ↗\" : \"Reading Nook ↗\";"),
        ("function openDirectNookReader()", "function openDirectReadingNook()"),
        ("onclick=\"openDirectNookReader()\"", "onclick=\"openDirectReadingNook()\""),
    ]

    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"  ✓ Replaced in build script: {old[:40]}...")
        else:
            print(f"  ⚠ Not found in build script: {old[:40]}...")

    with open(build_script, "w", encoding="utf-8") as f:
        f.write(content)

    # 2. Run build_independent_bookshelf_app.py to generate bookshelf/index.html & docs/bookshelf.html
    print("Rebuilding bookshelf apps...")
    subprocess.run(["python3", build_script], check=True)

    # 3. Update reader.html files
    reader_files = ["bookshelf/reader.html", "docs/reader.html"]
    for rf in reader_files:
        rf_path = os.path.abspath(rf)
        if os.path.exists(rf_path):
            with open(rf_path, "r", encoding="utf-8") as f:
                r_content = f.read()
            r_content = r_content.replace(
                "<span>Nook specializes in reflowable EPUB typography.",
                "<span>Reading Nook specializes in reflowable EPUB typography."
            )
            with open(rf_path, "w", encoding="utf-8") as f:
                f.write(r_content)
            print(f"  ✓ Updated {rf}")

    print("✓ All Reading Nook naming updates complete!")

if __name__ == "__main__":
    main()
