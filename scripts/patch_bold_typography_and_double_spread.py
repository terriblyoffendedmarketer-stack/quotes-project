# patch_bold_typography_and_double_spread.py — Enforces distinct bold vs regular typography and sets double spread as default
# Usage: python3 scripts/patch_bold_typography_and_double_spread.py
# Requires: Python 3.8+ (standard library only)
#
# Gotchas:
# - Iframes in EPUB.js do NOT inherit parent window Google Fonts; we must inject the full
#   webfont stylesheet (weights 400 through 800) into every chapter using rendition.hooks.content.register().
# - Many EPUBs (e.g. The Courage to be Disliked) use publisher-specific classes like .txbfb or .txbf
#   with missing fallback fonts ("EBGaramond-Bold"); defining explicit 700-weight serif rules ensures
#   speaker labels and emphasis render with prominent bold contrast.
# - Setting minSpreadWidth to 640 and spreadMode to 'always' ensures double spread is active by default
#   across normal laptop and windowed desktop layouts.

import os

FILES_TO_PATCH = [
    os.path.abspath("bookshelf/reader.html"),
    os.path.abspath("docs/reader.html")
]

def patch_file(filepath):
    print(f"Patching {filepath}...")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update Google Fonts in <head> to include full font weights (400, 500, 600, 700, 800)
    old_font_link = """  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Inter:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400;1,6..72,500&display=swap" rel="stylesheet">"""
    new_font_link = """  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Inter:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;0,6..72,800;1,6..72,400;1,6..72,500;1,6..72,600;1,6..72,700&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;0,7..72,700;1,7..72,400;1,7..72,700&display=swap" rel="stylesheet">"""

    if old_font_link in content:
        content = content.replace(old_font_link, new_font_link)
        print("  ✓ Updated Google Fonts in <head> with full bold weights")
    else:
        print("  ⚠ Could not find exact old_font_link")

    # 2. Update default spreadMode state to "always"
    old_spread_mode = """    let spreadMode = (window.innerWidth >= 1024) ? "always" : "none";"""
    new_spread_mode = """    let spreadMode = "always"; // Double spread is default"""

    if old_spread_mode in content:
        content = content.replace(old_spread_mode, new_spread_mode)
        print("  ✓ Set spreadMode = 'always' as default")
    else:
        print("  ⚠ Could not find exact old_spread_mode")

    # 3. Update renderBook to inject webfonts into iframe & set minSpreadWidth to 640
    old_render_book_start = """    function renderBook(targetCfi) {
      if (rendition) {
        try { rendition.destroy(); } catch (e) {}
        rendition = null;
      }
      viewerEl.innerHTML = "";

      const isTwoPage = (spreadMode === "always" && !isContinuousScroll && window.innerWidth >= 800);
      centerSpine.style.display = isTwoPage ? "block" : "none";
      updateSpreadButtonStyles();

      rendition = book.renderTo("viewer", {
        width: "100%",
        height: "100%",
        flow: isContinuousScroll ? "scrolled-doc" : "paginated",
        spread: spreadMode,
        minSpreadWidth: 800
      });"""

    new_render_book_start = """    function renderBook(targetCfi) {
      if (rendition) {
        try { rendition.destroy(); } catch (e) {}
        rendition = null;
      }
      viewerEl.innerHTML = "";

      const isTwoPage = (spreadMode === "always" && !isContinuousScroll && window.innerWidth >= 640);
      centerSpine.style.display = isTwoPage ? "block" : "none";
      updateSpreadButtonStyles();

      rendition = book.renderTo("viewer", {
        width: "100%",
        height: "100%",
        flow: isContinuousScroll ? "scrolled-doc" : "paginated",
        spread: spreadMode,
        minSpreadWidth: 640
      });

      // Inject webfonts into iframe so bold & serif fonts render with crisp distinction
      rendition.hooks.content.register(contents => {
        contents.addStylesheet("https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;0,6..72,800;1,6..72,400;1,6..72,700&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;0,7..72,700;1,7..72,400;1,7..72,700&display=swap");
      });"""

    if old_render_book_start in content:
        content = content.replace(old_render_book_start, new_render_book_start)
        print("  ✓ Injected font stylesheet hook and updated minSpreadWidth to 640")
    else:
        print("  ⚠ Could not find exact old_render_book_start")

    # 4. Update window resize handler to use 640 breakpoint
    old_resize = """          const isTwoPage = (spreadMode === "always" && !isContinuousScroll && window.innerWidth >= 800);"""
    new_resize = """          const isTwoPage = (spreadMode === "always" && !isContinuousScroll && window.innerWidth >= 640);"""

    if old_resize in content:
        content = content.replace(old_resize, new_resize)
        print("  ✓ Updated resize handler breakpoint to 640")
    else:
        print("  ⚠ Could not find exact old_resize")

    # 5. In applyThemeToRendition, add explicit bold vs regular styling rules
    old_headings = """        "h1, h2, h3, h4": {
          "font-family": "'Bookerly', 'Newsreader', Georgia, serif !important",
          "font-weight": "400 !important",
          "line-height": "1.25 !important",
          "margin-top": "2.2em !important",
          "margin-bottom": "1em !important",
          "text-align": "left !important",
          "letter-spacing": "-0.01em !important"
        },
        "h1": {
          "font-size": "1.65em !important"
        },
        "h2": {
          "font-size": "1.35em !important"
        },
        "h3": {
          "font-size": "1.18em !important"
        },
        "::selection": {
          background: "rgba(125, 211, 252, 0.45) !important"
        }"""

    new_headings = """        "h1, h2, h3, h4": {
          "font-family": "'Newsreader', 'Bookerly', 'Literata', Georgia, serif !important",
          "font-weight": "500 !important",
          "line-height": "1.25 !important",
          "margin-top": "2.2em !important",
          "margin-bottom": "1em !important",
          "text-align": "left !important",
          "letter-spacing": "-0.01em !important"
        },
        "h1": {
          "font-size": "1.65em !important"
        },
        "h2": {
          "font-size": "1.35em !important"
        },
        "h3": {
          "font-size": "1.18em !important"
        },
        "b, strong, b *, strong *, [class*='bold'], [class*='txbf'], .txbfb, .txbf, .sgc2, .sgc13": {
          "font-family": "'Newsreader', 'Bookerly', 'Literata', Georgia, serif !important",
          "font-weight": "700 !important",
          "-webkit-font-smoothing": "antialiased"
        },
        "em, i, em *, i *, [class*='italic'], .sgc8": {
          "font-style": "italic !important"
        },
        "b em, em b, strong em, em strong": {
          "font-family": "'Newsreader', 'Bookerly', 'Literata', Georgia, serif !important",
          "font-weight": "700 !important",
          "font-style": "italic !important"
        },
        "::selection": {
          background: "rgba(125, 211, 252, 0.45) !important"
        }"""

    if old_headings in content:
        content = content.replace(old_headings, new_headings)
        print("  ✓ Added explicit bold font-weight: 700 rules for bold text and publisher classes")
    else:
        print("  ⚠ Could not find exact old_headings")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ Saved {filepath}")

def main():
    for f in FILES_TO_PATCH:
        if os.path.exists(f):
            patch_file(f)
        else:
            print(f"File not found: {f}")

if __name__ == "__main__":
    main()
