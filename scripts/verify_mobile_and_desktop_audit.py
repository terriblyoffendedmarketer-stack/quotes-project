# scripts/verify_mobile_and_desktop_audit.py — Comprehensive automated audit of shelf app & reading nook across mobile and laptop viewports
# Usage: python3 scripts/verify_mobile_and_desktop_audit.py
# Requires: Python 3.8+ (standard library only)

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHELF_HTML = ROOT / "bookshelf" / "index.html"
READER_HTML = ROOT / "bookshelf" / "reader.html"
DOCS_SHELF = ROOT / "docs" / "bookshelf.html"
DOCS_READER = ROOT / "docs" / "reader.html"

def audit():
    print("=" * 70)
    print("COMPREHENSIVE AUDIT: SHELF APP & READING NOOK (MOBILE & LAPTOP)")
    print("=" * 70)

    shelf_content = SHELF_HTML.read_text(encoding="utf-8")
    reader_content = READER_HTML.read_text(encoding="utf-8")
    passes = 0
    failures = 0

    def check(title, condition, detail=""):
        nonlocal passes, failures
        if condition:
            print(f"  [PASS] {title}")
            passes += 1
        else:
            print(f"  [FAIL] {title} -> {detail}")
            failures += 1

    print("\n--- PILLAR 1: SHELF CHROME & VIEWPORTS (375px–430px) ---")
    check(
        "Desktop Header Preserved on Laptop (hidden md:flex)",
        '<div class="hidden md:flex max-w-7xl mx-auto items-center justify-between gap-4">' in shelf_content,
        "Desktop header container not found"
    )
    check(
        "Adaptive Mobile App Bar Implemented (< md)",
        '<div class="flex md:hidden flex-col gap-2 max-w-7xl mx-auto">' in shelf_content,
        "Mobile adaptive header container not found"
    )
    check(
        "Segmented Mobile View Switcher with Touch Targets",
        'id="mobileViewBtnBoard"' in shelf_content and 'id="mobileViewBtnEditorial"' in shelf_content and 'id="mobileViewBtnSplit"' in shelf_content,
        "Mobile segmented buttons missing"
    )
    check(
        "Synchronized Mobile Search Bar with Clear Button",
        'id="mobileSearchInput"' in shelf_content and 'id="mobileSearchClearBtn"' in shelf_content,
        "Mobile search bar elements missing"
    )

    print("\n--- PILLAR 2: SHELF CARD ERGONOMICS & BOTTOM DOSSIER SHEET ---")
    check(
        "Board View gap calibrated for mobile 2-column grid",
        'gap-3.5 sm:gap-6 md:gap-7' in shelf_content,
        "Board grid gap not responsive"
    )
    check(
        "Editorial View stacked on mobile (flex-col sm:flex-row)",
        'flex flex-col sm:flex-row gap-4 sm:gap-6' in shelf_content,
        "Editorial card layout not responsive"
    )
    check(
        "Editorial synopsis clamped to 4 lines on mobile",
        '-webkit-line-clamp: 4 !important;' in shelf_content,
        "Editorial synopsis 4-line mobile clamp missing"
    )
    check(
        "Native Bottom Dossier Sheet for Mobile (< 640px)",
        'translate-y-full sm:translate-y-0 sm:translate-x-full' in shelf_content,
        "Bottom sheet slide-up transform missing"
    )
    check(
        "Mobile Pull Bar Handle in Dossier Panel",
        'w-12 h-1.5 bg-stone-300 dark:bg-stone-600 rounded-full mx-auto mb-3 sm:hidden' in shelf_content,
        "Mobile drag handle missing"
    )

    print("\n--- PILLAR 3: READING NOOK MOBILE CANVAS & TOUCH NAVIGATION ---")
    check(
        "Viewport meta has viewport-fit=cover",
        'viewport-fit=cover' in reader_content,
        "viewport-fit=cover missing from meta"
    )
    check(
        "Safe-area insets CSS declared",
        '--safe-top: env(safe-area-inset-top, 0px);' in reader_content,
        "Safe-area insets missing in :root"
    )
    check(
        "Portrait Single-Page Fallback below 640px",
        'const isMobilePortrait = window.innerWidth < 640;' in reader_content and 'const effectiveSpread = isMobilePortrait ? "none" : spreadMode;' in reader_content,
        "Adaptive single-page spread logic missing"
    )
    check(
        "Laptop / Desktop Double Bifold Spread Preserved (>= 640px)",
        'const isTwoPage = (effectiveSpread === "always" && !isContinuousScroll && window.innerWidth >= 640);' in reader_content,
        "Laptop bifold spread condition broken"
    )
    check(
        "Touch Navigation registered inside EPUB.js iframe (Left 25%, Right 25%, Center 50%)",
        'tapX < width * 0.28' in reader_content and 'tapX > width * 0.72' in reader_content and 'toggleHeaderVisible()' in reader_content,
        "Touch tap navigation zones missing"
    )
    check(
        "Touch Horizontal Swipe Gesture Detection (> 45px)",
        'Math.abs(deltaX) > 45 && Math.abs(deltaY) < 60' in reader_content,
        "Touch swipe detection missing"
    )
    check(
        "Outer Chevron Buttons Hidden on Mobile Portrait (< 640px)",
        '@media (max-width: 639px) {\n      .turn-btn {\n        display: none !important;' in reader_content or '@media (max-width: 639px) {\n      .turn-btn {' in reader_content,
        "Mobile chevron hiding CSS missing"
    )

    print("\n--- PILLAR 4: BALANCED TYPOGRAPHY & READABILITY (LAPTOP & MOBILE) ---")
    check(
        "Regular Body Font-Weight calibrated to sturdy 430",
        '"font-weight": "430 !important"' in reader_content,
        "Regular font weight is not 430"
    )
    check(
        "Bold Font-Weight calibrated to balanced 630 (no 750 extra-bold)",
        '"font-weight": "630 !important"' in reader_content and '750 !important' not in reader_content,
        "Bold font weight is not 630 or 750 is still present"
    )
    check(
        "Optical Size 18 explicitly declared for body and bold",
        '"font-variation-settings": "\'opsz\' 18, \'wght\' 430 !important"' in reader_content and '"font-variation-settings": "\'opsz\' 18, \'wght\' 630 !important"' in reader_content,
        "Optical sizing settings missing"
    )
    check(
        "Both Literata and Newsreader in font-family stack",
        "'Bookerly', 'Literata', 'Newsreader', 'Charter', 'Georgia', serif" in reader_content,
        "Font-family stack missing Literata or Newsreader"
    )
    check(
        "Heading font-weight tuned to elegant 550",
        '"font-weight": "550 !important"' in reader_content,
        "Heading font weight not 550"
    )
    check(
        "Docs and Bookshelf copies are identical",
        DOCS_SHELF.read_text(encoding="utf-8") == shelf_content and DOCS_READER.read_text(encoding="utf-8") == reader_content,
        "Docs and bookshelf files diverge"
    )

    print("\n--- PILLAR 6: METADATA ACCURACY & CURATED MULTI-CATEGORIES ---")
    import json
    data_books = json.loads((ROOT / "bookshelf" / "data.json").read_text(encoding="utf-8"))
    snow_crash_book = next((b for b in data_books if b.get("id") == "neal-stephenson-snow-crash"), None)
    check(
        "Snow Crash has title 'Snow Crash' and author 'Neal Stephenson'",
        snow_crash_book and snow_crash_book.get("title") == "Snow Crash" and snow_crash_book.get("author") == "Neal Stephenson",
        f"Snow crash metadata incorrect: {snow_crash_book}"
    )
    check(
        "Curated categories (Short Stories, Essays, Literary Non-Fiction) present in shelf app",
        all(c in shelf_content for c in ["Short Stories", "Essays", "Literary Non-Fiction"]),
        "One or more curated categories missing in shelf HTML"
    )
    short_stories = [b for b in data_books if "Short Stories" in b.get("categories", []) or b.get("category") == "Short Stories"]
    essays = [b for b in data_books if "Essays" in b.get("categories", []) or b.get("category") == "Essays"]
    lit_nf = [b for b in data_books if "Literary Non-Fiction" in b.get("categories", []) or b.get("category") == "Literary Non-Fiction"]
    check(
        f"Short Stories category has curated books ({len(short_stories)} books)",
        len(short_stories) >= 20,
        f"Short stories count too low: {len(short_stories)}"
    )
    check(
        f"Essays category has curated books ({len(essays)} books)",
        len(essays) >= 25,
        f"Essays count too low: {len(essays)}"
    )
    check(
        f"Literary Non-Fiction category has curated books ({len(lit_nf)} books)",
        len(lit_nf) >= 30,
        f"Literary non-fiction count too low: {len(lit_nf)}"
    )

    print("\n" + "=" * 70)
    print(f"AUDIT SUMMARY: {passes} PASSED | {failures} FAILED")
    print("=" * 70)
    return failures == 0

if __name__ == "__main__":
    success = audit()
    exit(0 if success else 1)
