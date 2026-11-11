# tune_regular_font_weight_and_size.py — Gives regular body text sturdy book weight (460) and generous 18.5px size
# Usage: python3 scripts/tune_regular_font_weight_and_size.py
# Requires: Python 3.8+ (standard library only)
#
# Gotchas:
# - On macOS retina displays, -webkit-font-smoothing: antialiased strips subpixel hinting, making
#   weight 400 serifs look hair-thin. Switching to subpixel-antialiased and setting font-weight: 460
#   reproduces Bookerly's solid ink appearance.
# - Bumping baseFontSize from 17.5px to 18.5px ensures body text is immediately legible without being bulky.
# - Keep bold at 750 weight so bold headings, speaker tags, and emphasized phrases stand out crisply.

import os

FILES_TO_PATCH = [
    os.path.abspath("bookshelf/reader.html"),
    os.path.abspath("docs/reader.html")
]

def patch_file(filepath):
    print(f"Tuning regular font weight and size in {filepath}...")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    old_theme_block = """      // Kindle Bookerly Typography Configuration:
      // Tight 1.5 line-height, elegant regular-weight headings, 1.4em indents, full justification
      const baseFontSize = 17.5 * (currentFontSize / 100);

      const bodyStyles = {
        background: `${bgColor} !important`,
        color: `${textColor} !important`,
        "font-family": "'Bookerly', 'Newsreader', 'Literata', 'Iowan Old Style', 'Charter', 'Georgia', serif !important",
        "font-size": `${baseFontSize}px !important`,
        "line-height": "1.5 !important",
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
        }
      });"""

    new_theme_block = """      // Kindle Bookerly Typography Configuration:
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

    if old_theme_block in content:
        content = content.replace(old_theme_block, new_theme_block)
        print("  ✓ Successfully updated typography weight (460) and size (18.5px)")
    else:
        print("  ⚠ Could not find exact old_theme_block")

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
