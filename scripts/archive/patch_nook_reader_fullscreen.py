# patch_nook_reader_fullscreen.py — Eliminates 3rd column peek and fixes bifold spread in Nook reader
# Usage: python3 scripts/patch_nook_reader_fullscreen.py
# Requires: Python 3.8+ (standard library only)
#
# Gotchas:
# - Do NOT inject custom `column-gap` or horizontal `padding` into rendition themes in paginated mode!
#   EPUB.js internally calculates exact column width and gaps based on the iframe width. Overriding
#   `column-gap` (e.g. 4rem) or `padding: 20px 5%` shrinks the body content box below EPUB.js's calculated
#   geometry, forcing CSS Multi-Column layout to wrap text into a 3rd column that peeks into the outer margins!
# - Always call `rendition.destroy()` and clear `viewer.innerHTML` before re-rendering `book.renderTo()`
#   to prevent lingering DOM nodes or detached resize handlers.
# - Always add a debounced `window.resize` handler calling `rendition.resize()` so fullscreen toggling
#   and window resizing instantly recalculate the two-page spread without column overflow.

import re
import os

FILES_TO_PATCH = [
    os.path.abspath("bookshelf/reader.html"),
    os.path.abspath("docs/reader.html")
]

def patch_file(filepath):
    print(f"Patching {filepath}...")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update renderBook: add rendition cleanup, minSpreadWidth, rendition.on("keydown", handleKeyNav)
    old_render_book = """    function renderBook(targetCfi) {
      const isTwoPage = (spreadMode === "always" && !isContinuousScroll);
      centerSpine.style.display = isTwoPage ? "block" : "none";
      updateSpreadButtonStyles();

      rendition = book.renderTo("viewer", {
        width: "100%",
        height: "100%",
        flow: isContinuousScroll ? "scrolled-doc" : "paginated",
        spread: spreadMode
      });

      applyThemeToRendition();
      rendition.display(targetCfi || currentCfi || undefined);

      rendition.on("relocated", location => {
        currentCfi = location.start.cfi;
        updateProgress();
      });

      rendition.on("selected", (cfiRange, contents) => {
        book.getRange(cfiRange).then(range => {
          const text = range.toString().trim();
          if (text.length > 3) {
            currentSelection = {
              text: text,
              cfiRange: cfiRange,
              range: range
            };
            showHighlightTooltip(range, contents);
          }
        });
      });

      rendition.on("click", () => {
        hideHighlightTooltip();
      });
    }"""

    new_render_book = """    function renderBook(targetCfi) {
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
      });

      applyThemeToRendition();
      rendition.display(targetCfi || currentCfi || undefined);

      rendition.on("relocated", location => {
        currentCfi = location.start.cfi;
        updateProgress();
      });

      rendition.on("selected", (cfiRange, contents) => {
        book.getRange(cfiRange).then(range => {
          const text = range.toString().trim();
          if (text.length > 3) {
            currentSelection = {
              text: text,
              cfiRange: cfiRange,
              range: range
            };
            showHighlightTooltip(range, contents);
          }
        });
      });

      rendition.on("click", () => {
        hideHighlightTooltip();
      });

      rendition.on("keydown", handleKeyNav);
    }"""

    if old_render_book in content:
        content = content.replace(old_render_book, new_render_book)
        print("  ✓ Successfully replaced renderBook()")
    else:
        print("  ⚠ Could not find exact old_render_book, checking if already patched...")

    # 2. Add debounced resize listener after updateSpreadButtonStyles
    old_spread_buttons = """    function updateSpreadButtonStyles() {
      if (spreadMode === "always") {
        spreadTwoBtn.className = "p-2 rounded-xl border border-[var(--terracotta)] bg-[var(--terracotta-soft)] text-[var(--terracotta)] font-semibold text-[11px] flex items-center justify-center gap-1.5 transition shadow-sm";
        spreadOneBtn.className = "p-2 rounded-xl border border-[var(--reader-border)] text-stone-500 hover:text-[var(--reader-text)] font-semibold text-[11px] flex items-center justify-center gap-1.5 transition shadow-sm";
      } else {
        spreadOneBtn.className = "p-2 rounded-xl border border-[var(--terracotta)] bg-[var(--terracotta-soft)] text-[var(--terracotta)] font-semibold text-[11px] flex items-center justify-center gap-1.5 transition shadow-sm";
        spreadTwoBtn.className = "p-2 rounded-xl border border-[var(--reader-border)] text-stone-500 hover:text-[var(--reader-text)] font-semibold text-[11px] flex items-center justify-center gap-1.5 transition shadow-sm";
      }
    }"""

    new_spread_buttons = """    function updateSpreadButtonStyles() {
      if (spreadMode === "always") {
        spreadTwoBtn.className = "p-2 rounded-xl border border-[var(--terracotta)] bg-[var(--terracotta-soft)] text-[var(--terracotta)] font-semibold text-[11px] flex items-center justify-center gap-1.5 transition shadow-sm";
        spreadOneBtn.className = "p-2 rounded-xl border border-[var(--reader-border)] text-stone-500 hover:text-[var(--reader-text)] font-semibold text-[11px] flex items-center justify-center gap-1.5 transition shadow-sm";
      } else {
        spreadOneBtn.className = "p-2 rounded-xl border border-[var(--terracotta)] bg-[var(--terracotta-soft)] text-[var(--terracotta)] font-semibold text-[11px] flex items-center justify-center gap-1.5 transition shadow-sm";
        spreadTwoBtn.className = "p-2 rounded-xl border border-[var(--reader-border)] text-stone-500 hover:text-[var(--reader-text)] font-semibold text-[11px] flex items-center justify-center gap-1.5 transition shadow-sm";
      }
    }

    // Debounced window resize handler: re-fits rendition and adapts spine
    let resizeTimer = null;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        if (rendition) {
          rendition.resize();
          const isTwoPage = (spreadMode === "always" && !isContinuousScroll && window.innerWidth >= 800);
          centerSpine.style.display = isTwoPage ? "block" : "none";
        }
      }, 150);
    });"""

    if old_spread_buttons in content:
        content = content.replace(old_spread_buttons, new_spread_buttons)
        print("  ✓ Successfully added debounced resize listener")
    else:
        print("  ⚠ Could not find exact old_spread_buttons, checking if already patched...")

    # 3. Fix applyThemeToRendition: remove conflicting column-gap and padding
    old_apply_theme = """    function applyThemeToRendition() {
      if (!rendition) return;

      const isNight = document.body.classList.contains('theme-night');
      const isSepia = document.body.classList.contains('theme-sepia');
      const isWhite = document.body.classList.contains('theme-white');

      let textColor = '#2c2523';
      let bgColor = '#fbf8f3';

      if (isNight) {
        textColor = '#e2ded9';
        bgColor = '#151311';
      } else if (isSepia) {
        textColor = '#3c2f21';
        bgColor = '#f4ebd9';
      } else if (isWhite) {
        textColor = '#1a1a1a';
        bgColor = '#ffffff';
      }

      // Professional Kindle / Apple Books Typography:
      // Justified text, paragraph indents, no paragraph margin bottoms, generous line-height
      const baseFontSize = 18 * (currentFontSize / 100);

      rendition.themes.default({
        html: {
          "column-gap": "4rem !important",
          "-webkit-column-gap": "4rem !important"
        },
        body: {
          background: `${bgColor} !important`,
          color: `${textColor} !important`,
          "font-family": "'Bookerly', 'Newsreader', 'Literata', 'Iowan Old Style', 'Charter', 'Georgia', serif !important",
          "font-size": `${baseFontSize}px !important`,
          "line-height": "1.68 !important",
          padding: "20px 5% !important",
          "column-gap": "4rem !important",
          "-webkit-column-gap": "4rem !important",
          "-webkit-font-smoothing": "antialiased",
          "-moz-osx-font-smoothing": "grayscale"
        },
        p: {
          "text-indent": "1.5em !important",
          "margin-top": "0 !important",
          "margin-bottom": "0 !important",
          "text-align": "justify !important",
          "text-justify": "inter-word !important",
          "hyphens": "auto !important",
          "-webkit-hyphens": "auto !important"
        },
        "p:first-of-type, h1 + p, h2 + p, h3 + p, h4 + p, blockquote + p": {
          "text-indent": "0 !important"
        },
        "h1, h2, h3, h4": {
          "font-family": "'Bookerly', 'Newsreader', Georgia, serif !important",
          "line-height": "1.3 !important",
          "margin-top": "1.6em !important",
          "margin-bottom": "0.8em !important",
          "text-align": "left !important"
        },
        "::selection": {
          background: "rgba(125, 211, 252, 0.45) !important"
        }
      });
    }"""

    new_apply_theme = """    function applyThemeToRendition() {
      if (!rendition) return;

      const isNight = document.body.classList.contains('theme-night');
      const isSepia = document.body.classList.contains('theme-sepia');
      const isWhite = document.body.classList.contains('theme-white');

      let textColor = '#2c2523';
      let bgColor = '#fbf8f3';

      if (isNight) {
        textColor = '#e2ded9';
        bgColor = '#151311';
      } else if (isSepia) {
        textColor = '#3c2f21';
        bgColor = '#f4ebd9';
      } else if (isWhite) {
        textColor = '#1a1a1a';
        bgColor = '#ffffff';
      }

      // Professional Kindle / Apple Books Typography:
      // Justified text, paragraph indents, zero paragraph margins, generous line-height
      const baseFontSize = 18 * (currentFontSize / 100);

      const bodyStyles = {
        background: `${bgColor} !important`,
        color: `${textColor} !important`,
        "font-family": "'Bookerly', 'Newsreader', 'Literata', 'Iowan Old Style', 'Charter', 'Georgia', serif !important",
        "font-size": `${baseFontSize}px !important`,
        "line-height": "1.68 !important",
        margin: "0 !important",
        "-webkit-font-smoothing": "antialiased",
        "-moz-osx-font-smoothing": "grayscale"
      };

      if (isContinuousScroll) {
        bodyStyles.padding = "24px 20px !important";
      }

      rendition.themes.default({
        html: {
          margin: "0 !important"
        },
        body: bodyStyles,
        p: {
          "text-indent": "1.5em !important",
          "margin-top": "0 !important",
          "margin-bottom": "0 !important",
          "text-align": "justify !important",
          "text-justify": "inter-word !important",
          "hyphens": "auto !important",
          "-webkit-hyphens": "auto !important"
        },
        "p:first-of-type, h1 + p, h2 + p, h3 + p, h4 + p, blockquote + p": {
          "text-indent": "0 !important"
        },
        "h1, h2, h3, h4": {
          "font-family": "'Bookerly', 'Newsreader', Georgia, serif !important",
          "line-height": "1.3 !important",
          "margin-top": "1.6em !important",
          "margin-bottom": "0.8em !important",
          "text-align": "left !important"
        },
        "::selection": {
          background: "rgba(125, 211, 252, 0.45) !important"
        }
      });

      try {
        rendition.themes.fontSize(`${baseFontSize}px`);
      } catch (e) {}
    }"""

    if old_apply_theme in content:
        content = content.replace(old_apply_theme, new_apply_theme)
        print("  ✓ Successfully updated applyThemeToRendition()")
    else:
        print("  ⚠ Could not find exact old_apply_theme, checking if already patched...")

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
