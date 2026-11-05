# scripts/tune_reading_typography_and_mobile_nook.py — Calibrates Reading Nook balanced typography & mobile canvas ergonomics
# Usage: python3 scripts/tune_reading_typography_and_mobile_nook.py
# Requires: Python 3.8+ (standard library only)
#
# Gotchas:
# - In EPUB.js iframes, variable fonts (Newsreader, Literata) require explicit font-optical-sizing: auto
#   and font-variation-settings: 'opsz' 18 to prevent thin hairline display rendering at 18px body size.
# - Setting regular weight to 430 (sturdy) and bold weight to 630 (semi-bold) achieves the golden 200-unit
#   typographic distinction: clear, distinct bold without the oppressive ink-blot heaviness of 750.
# - On mobile portrait (< 640px), spread must be forced to 'none' (single page) with 16px margins to prevent
#   EPUB.js from squeezing 2-3 words per column; while desktop/laptop (>= 640px) retains bifold two-page spread.
# - Touch zones (left 25% prev, right 25% next, center 50% toggle chrome) must be registered directly on
#   contents.document inside rendition.hooks.content to capture touch events through the EPUB.js iframe.

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES_TO_PATCH = [
    ROOT / "bookshelf" / "reader.html",
    ROOT / "docs" / "reader.html"
]

def patch_reader_html(filepath: Path):
    print(f"Patching {filepath}...")
    html = filepath.read_text(encoding="utf-8")

    # 1. Update Viewport Meta for Safe Area (Notch & Home Indicator)
    html = re.sub(
        r'<meta name="viewport" content="[^"]*">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">',
        html
    )

    # 2. Update CSS for mobile touch ergonomics & safe-area insets
    css_anchor = "    :root {"
    css_addition = """    :root {
      --safe-top: env(safe-area-inset-top, 0px);
      --safe-bottom: env(safe-area-inset-bottom, 0px);
      --safe-left: env(safe-area-inset-left, 0px);
      --safe-right: env(safe-area-inset-right, 0px);"""
    if "env(safe-area-inset-top" not in html:
        html = html.replace(css_anchor, css_addition, 1)

    # Add mobile-specific turn button hiding & touch target rules
    mobile_css = """
    /* Mobile Touch Turn Zones & Chevron Visibility */
    @media (max-width: 639px) {
      .turn-btn {
        display: none !important;
      }
      #readerViewport {
        padding-left: max(0.5rem, env(safe-area-inset-left)) !important;
        padding-right: max(0.5rem, env(safe-area-inset-right)) !important;
        padding-top: max(0.25rem, env(safe-area-inset-top)) !important;
        padding-bottom: max(0.25rem, env(safe-area-inset-bottom)) !important;
      }
      #topHeader {
        padding-top: env(safe-area-inset-top) !important;
        height: calc(3.5rem + env(safe-area-inset-top)) !important;
      }
      #statusBar {
        padding-bottom: env(safe-area-inset-bottom) !important;
        height: calc(2.2rem + env(safe-area-inset-bottom)) !important;
      }
    }
"""
    if "/* Mobile Touch Turn Zones & Chevron Visibility */" not in html:
        html = html.replace("  </style>", mobile_css + "  </style>", 1)

    # 3. Update Font Stylesheet Injection inside rendition.hooks.content
    old_fonts_hook = """      rendition.hooks.content.register(contents => {
        contents.addStylesheet("https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;0,6..72,800;1,6..72,400;1,6..72,700&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;0,7..72,700;1,7..72,400;1,7..72,700&display=swap");
      });"""

    new_fonts_hook = """      rendition.hooks.content.register(contents => {
        contents.addStylesheet("https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,500;0,7..72,600;0,7..72,700;1,7..72,400;1,7..72,600;1,7..72,700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;0,6..72,800;1,6..72,400;1,6..72,600;1,6..72,700&display=swap");

        // Touch & Tap Navigation inside EPUB.js iframe (Left 25% prev, Right 25% next, Center 50% toggle chrome)
        let touchStartX = 0;
        let touchStartY = 0;
        let touchStartTime = 0;

        contents.document.addEventListener('touchstart', (e) => {
          if (e.touches && e.touches[0]) {
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
            touchStartTime = Date.now();
          }
        }, { passive: true });

        contents.document.addEventListener('touchend', (e) => {
          if (!e.changedTouches || !e.changedTouches[0]) return;
          const deltaX = e.changedTouches[0].clientX - touchStartX;
          const deltaY = e.changedTouches[0].clientY - touchStartY;
          const duration = Date.now() - touchStartTime;

          // Guard: if user has active text selection, do not trigger turn
          const sel = contents.window.getSelection();
          if (sel && sel.toString().trim().length > 0) return;

          // Swipe gesture (horizontal swipe > 45px in < 500ms)
          if (Math.abs(deltaX) > 45 && Math.abs(deltaY) < 60 && duration < 500) {
            if (deltaX < 0) {
              nextPage();
            } else {
              prevPage();
            }
            return;
          }

          // Single tap detection
          if (Math.abs(deltaX) < 15 && Math.abs(deltaY) < 15 && duration < 400) {
            const width = contents.window.innerWidth || window.innerWidth;
            const tapX = e.changedTouches[0].clientX;
            if (tapX < width * 0.28) {
              prevPage();
            } else if (tapX > width * 0.72) {
              nextPage();
            } else {
              toggleHeaderVisible();
            }
          }
        }, { passive: true });

        contents.document.addEventListener('click', (e) => {
          // Guard touch-emulated clicks
          if (e.detail === 0 || Date.now() - touchStartTime < 500) return;
          const sel = contents.window.getSelection();
          if (sel && sel.toString().trim().length > 0) return;
          if (window.innerWidth < 640) {
            const width = contents.window.innerWidth || window.innerWidth;
            const clickX = e.clientX;
            if (clickX < width * 0.28) {
              prevPage();
            } else if (clickX > width * 0.72) {
              nextPage();
            } else {
              toggleHeaderVisible();
            }
          }
        });
      });"""

    if old_fonts_hook in html:
        html = html.replace(old_fonts_hook, new_fonts_hook)
        print("  ✓ Updated iframe content hook with touch navigation and dual webfonts")
    else:
        print("  ⚠ Could not find exact old_fonts_hook block")

    # 4. Update renderBook spread mode: auto-switch to single page below 640px
    old_render_block = """      const isTwoPage = (spreadMode === "always" && !isContinuousScroll && window.innerWidth >= 640);
      centerSpine.style.display = isTwoPage ? "block" : "none";
      updateSpreadButtonStyles();

      rendition = book.renderTo("viewer", {
        width: "100%",
        height: "100%",
        flow: isContinuousScroll ? "scrolled-doc" : "paginated",
        spread: spreadMode,
        minSpreadWidth: 640
      });"""

    new_render_block = """      const isMobilePortrait = window.innerWidth < 640;
      const effectiveSpread = isMobilePortrait ? "none" : spreadMode;
      const isTwoPage = (effectiveSpread === "always" && !isContinuousScroll && window.innerWidth >= 640);
      centerSpine.style.display = isTwoPage ? "block" : "none";
      updateSpreadButtonStyles();

      rendition = book.renderTo("viewer", {
        width: "100%",
        height: "100%",
        flow: isContinuousScroll ? "scrolled-doc" : "paginated",
        spread: effectiveSpread,
        minSpreadWidth: 640
      });"""

    if old_render_block in html:
        html = html.replace(old_render_block, new_render_block)
        print("  ✓ Updated renderBook to auto-switch to single page below 640px")
    else:
        print("  ⚠ Could not find exact old_render_block")

    # 5. Update debounced resize listener to re-evaluate single vs double spread
    old_resize_block = """    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        if (rendition) {
          rendition.resize();
          const isTwoPage = (spreadMode === "always" && !isContinuousScroll && window.innerWidth >= 640);
          centerSpine.style.display = isTwoPage ? "block" : "none";
        }
      }, 150);
    });"""

    new_resize_block = """    let lastWindowWidth = window.innerWidth;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        if (rendition) {
          const widthChanged = (window.innerWidth < 640) !== (lastWindowWidth < 640);
          lastWindowWidth = window.innerWidth;
          if (widthChanged && book) {
            renderBook(currentCfi);
          } else {
            rendition.resize();
            const isMobilePortrait = window.innerWidth < 640;
            const effectiveSpread = isMobilePortrait ? "none" : spreadMode;
            const isTwoPage = (effectiveSpread === "always" && !isContinuousScroll && window.innerWidth >= 640);
            centerSpine.style.display = isTwoPage ? "block" : "none";
          }
        }
      }, 150);
    });"""

    if old_resize_block in html:
        html = html.replace(old_resize_block, new_resize_block)
        print("  ✓ Updated debounced resize listener for mobile boundary detection")
    else:
        print("  ⚠ Could not find exact old_resize_block")

    # 6. Calibrate Balanced Bookerly/Literata Typography (430 regular, 630 bold, optical size 18)
    old_theme_setup = """      // Kindle Bookerly Typography Configuration:
      // Substantial 18.5px size, sturdy 460 weight (no thin hairlines), 1.52 line-height, 1.4em indents
      const baseFontSize = 18.5 * (currentFontSize / 100);

      const bodyStyles = {
        background: `${bgColor} !important`,
        color: `${textColor} !important`,
        "font-family": "'Bookerly', 'Newsreader', 'Literata', 'Charter', 'Georgia', serif !important",
        "font-size": `${baseFontSize}px !important`,
        "font-weight": "460 !important",
        "line-height": "1.52 !important",
        margin: "0 !important",
        "-webkit-font-smoothing": "subpixel-antialiased"
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
          "font-size": `${baseFontSize}px !important`,
          "font-weight": "460 !important",
          "text-indent": "1.4em !important",
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
          "font-weight": "750 !important",
          "-webkit-font-smoothing": "antialiased"
        },
        "em, i, em *, i *, [class*='italic'], .sgc8": {
          "font-style": "italic !important"
        },
        "b em, em b, strong em, em strong": {
          "font-family": "'Newsreader', 'Bookerly', 'Literata', Georgia, serif !important",
          "font-weight": "750 !important",
          "font-style": "italic !important"
        },
        "::selection": {
          background: "rgba(125, 211, 252, 0.45) !important"
        }
      });"""

    new_theme_setup = """      // Balanced Bookerly & Literata Typography Calibration:
      // Regular: Sturdy 430 book weight (subpixel-antialiased, opsz 18 text optical size, 1.54 line height)
      // Bold: Calibrated 630 semi-bold (clean, unmistakable distinction without the oppressive 750 extra-bold ink blot)
      const isMobile = window.innerWidth < 640;
      const baseFontSize = (isMobile ? 17.5 : 18.5) * (currentFontSize / 100);

      const bodyStyles = {
        background: `${bgColor} !important`,
        color: `${textColor} !important`,
        "font-family": "'Bookerly', 'Literata', 'Newsreader', 'Charter', 'Georgia', serif !important",
        "font-size": `${baseFontSize}px !important`,
        "font-weight": "430 !important",
        "font-optical-sizing": "auto !important",
        "font-variation-settings": "'opsz' 18, 'wght' 430 !important",
        "line-height": "1.54 !important",
        margin: "0 !important",
        "-webkit-font-smoothing": "subpixel-antialiased",
        "-moz-osx-font-smoothing": "auto"
      };

      if (isContinuousScroll) {
        bodyStyles.padding = isMobile ? "16px 12px !important" : "24px 20px !important";
      }

      rendition.themes.default({
        html: {
          margin: "0 !important"
        },
        body: bodyStyles,
        p: {
          "font-size": `${baseFontSize}px !important`,
          "font-weight": "430 !important",
          "font-optical-sizing": "auto !important",
          "font-variation-settings": "'opsz' 18, 'wght' 430 !important",
          "text-indent": "1.4em !important",
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
          "font-family": "'Literata', 'Newsreader', 'Bookerly', Georgia, serif !important",
          "font-weight": "550 !important",
          "font-optical-sizing": "auto !important",
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
          "font-family": "'Bookerly', 'Literata', 'Newsreader', Georgia, serif !important",
          "font-weight": "630 !important",
          "font-optical-sizing": "auto !important",
          "font-variation-settings": "'opsz' 18, 'wght' 630 !important",
          "-webkit-font-smoothing": "antialiased"
        },
        "em, i, em *, i *, [class*='italic'], .sgc8": {
          "font-style": "italic !important"
        },
        "b em, em b, strong em, em strong": {
          "font-family": "'Bookerly', 'Literata', 'Newsreader', Georgia, serif !important",
          "font-weight": "630 !important",
          "font-optical-sizing": "auto !important",
          "font-variation-settings": "'opsz' 18, 'wght' 630 !important",
          "font-style": "italic !important"
        },
        "::selection": {
          background: "rgba(125, 211, 252, 0.45) !important"
        }
      });"""

    if old_theme_setup in html:
        html = html.replace(old_theme_setup, new_theme_setup)
        print("  ✓ Calibrated typography weights (430 regular / 630 bold / opsz 18)")
    else:
        print("  ⚠ Could not find exact old_theme_setup block")

    filepath.write_text(html, encoding="utf-8")
    print(f"  ✓ Saved updates to {filepath}")

def main():
    for f in FILES_TO_PATCH:
        if f.exists():
            patch_reader_html(f)
        else:
            print(f"File not found: {f}")

if __name__ == "__main__":
    main()
