# apply_kindle_reader_config.py — Applies Kindle typography, auto-hiding header, and seamless footer to Reading Nook
# Usage: python3 scripts/apply_kindle_reader_config.py
# Requires: Python 3.8+ (standard library only)
#
# Gotchas:
# - Mousemove events inside EPUB.js iframe do NOT bubble to the parent window; we must bind
#   rendition.on("mousemove", handleGlobalMouseMove) so moving cursor near top reveals the header.
# - Do NOT remove #centerSpine; the user requested to keep the central spine line active.
# - Keep line-height at 1.5 and h1 at 1.65em (font-weight: 400) to replicate Bookerly's native density.

import os

FILES_TO_PATCH = [
    os.path.abspath("bookshelf/reader.html"),
    os.path.abspath("docs/reader.html")
]

def patch_file(filepath):
    print(f"Applying Kindle config to {filepath}...")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add CSS for auto-hiding header and top reveal button in <style>
    old_style_end = """    @media (hover: none) {
      .turn-btn {
        opacity: 0.35;
      }
    }
  </style>"""

    new_style_end = """    @media (hover: none) {
      .turn-btn {
        opacity: 0.35;
      }
    }
    #topHeader {
      transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.2s ease;
    }
    .header-immersive {
      position: absolute !important;
      top: 0;
      left: 0;
      right: 0;
      z-index: 50;
      transform: translateY(-100%);
      opacity: 0;
      pointer-events: none;
    }
    .header-immersive.header-visible,
    .header-immersive:hover,
    .header-immersive:focus-within {
      transform: translateY(0) !important;
      opacity: 1 !important;
      pointer-events: auto !important;
    }
    #headerRevealBtn {
      transition: opacity 0.2s ease, transform 0.2s ease;
    }
    #headerRevealBtn:hover {
      opacity: 1 !important;
      transform: translate(-50%, 2px) scale(1.05);
    }
  </style>"""

    if old_style_end in content:
        content = content.replace(old_style_end, new_style_end)
        print("  ✓ Added immersive header CSS")
    else:
        print("  ⚠ Could not find exact old_style_end")

    # 2. Add id="topHeader" to <header> and add #headerRevealBtn and #topHoverTrigger
    old_header = """  <!-- Top App Bar -->
  <header class="h-14 border-b border-[var(--reader-border)] px-4 flex items-center justify-between z-30 shrink-0 bg-[var(--reader-bg)]/95 backdrop-blur-sm">"""

    new_header = """  <!-- Discreet Top Hover Sensor & Reveal Button for Kindle-Style Full Screen -->
  <div id="topHoverTrigger" class="fixed top-0 left-0 right-0 h-4 z-40 pointer-events-auto" onmouseenter="showHeader()"></div>
  <button id="headerRevealBtn" onclick="toggleHeaderVisible()" class="fixed top-1 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full bg-black/5 dark:bg-white/10 hover:bg-[var(--terracotta)] hover:text-white text-stone-400 dark:text-stone-500 text-[10px] tracking-wider uppercase font-sans z-30 transition-all opacity-0 hover:opacity-100 pointer-events-auto cursor-pointer shadow-xs" title="Click or hover to reveal controls" style="display: none;">
    •••
  </button>

  <!-- Top App Bar (Auto-hiding in Reading Mode) -->
  <header id="topHeader" class="h-14 border-b border-[var(--reader-border)] px-4 flex items-center justify-between z-50 shrink-0 bg-[var(--reader-bg)]/95 backdrop-blur-md shadow-xs">"""

    if old_header in content:
        content = content.replace(old_header, new_header)
        print("  ✓ Updated header markup with top hover trigger and reveal button")
    else:
        print("  ⚠ Could not find exact old_header")

    # 3. Update readerViewport padding and running header style
    old_viewport = """    <!-- 2. Centered Reading Viewport (Kindle Bifold Spread with Center Spine & Running Header) -->
    <div id="readerViewport" class="hidden w-full h-full max-w-5xl lg:max-w-6xl mx-auto px-4 sm:px-8 lg:px-12 py-2 sm:py-3 flex flex-col justify-center relative z-10">
      <!-- Running Header (Book Title Centered in Small Caps) -->
      <div id="runningHeader" class="text-center py-1 font-serif text-[11px] tracking-widest uppercase text-stone-400 dark:text-stone-500 truncate pointer-events-none select-none shrink-0"></div>"""

    new_viewport = """    <!-- 2. Centered Reading Viewport (Kindle Bifold Spread with Center Spine & Running Header) -->
    <div id="readerViewport" class="hidden w-full h-full max-w-5xl lg:max-w-6xl mx-auto px-4 sm:px-8 lg:px-12 pt-3 pb-1 flex flex-col justify-center relative z-10">
      <!-- Running Header (Book Title Centered in Subtle Small Caps, Kindle Style) -->
      <div id="runningHeader" class="text-center pb-2 font-serif text-[10px] sm:text-[11px] tracking-[0.2em] uppercase text-stone-400/90 dark:text-stone-500/90 truncate pointer-events-none select-none shrink-0"></div>"""

    if old_viewport in content:
        content = content.replace(old_viewport, new_viewport)
        print("  ✓ Updated readerViewport and runningHeader layout")
    else:
        print("  ⚠ Could not find exact old_viewport")

    # 4. Update bottom status bar: seamless Kindle style without border line
    old_status_bar = """  <!-- Bottom Reader Status Bar -->
  <footer id="statusBar" class="h-9 border-t border-[var(--reader-border)] px-4 flex items-center justify-between text-[11px] z-30 shrink-0 bg-[var(--reader-bg)] text-stone-500 font-mono">
    <div id="chapterDisplay" class="truncate max-w-[200px] sm:max-w-md font-serif italic text-xs"></div>
    <div class="flex items-center gap-3">
      <span id="pageProgressDisplay">0%</span>
    </div>
  </footer>"""

    new_status_bar = """  <!-- Bottom Reader Status Bar (Seamless Kindle Style) -->
  <footer id="statusBar" class="h-8 px-6 sm:px-12 flex items-center justify-between text-[11px] z-20 shrink-0 bg-transparent text-stone-400 dark:text-stone-500 font-serif select-none pointer-events-none">
    <div id="chapterDisplay" class="truncate max-w-[200px] sm:max-w-md italic text-[11px] text-stone-400 dark:text-stone-500 font-serif"></div>
    <div class="flex items-center gap-2">
      <span id="pageProgressDisplay" class="text-[11px] text-stone-400 dark:text-stone-500 font-serif tracking-wide">0%</span>
    </div>
  </footer>"""

    if old_status_bar in content:
        content = content.replace(old_status_bar, new_status_bar)
        print("  ✓ Updated statusBar to seamless Kindle footer")
    else:
        print("  ⚠ Could not find exact old_status_bar")

    # 5. Add Immersive Mode controller functions and mousemove handler
    old_init_reader = """    async function initReader() {
      chapterDisplay.innerText = "";
      updateQuotesCount();

      // Check if this book is already cached in IndexedDB
      try {
        const cachedBuffer = await loadBookFromDB(bookId);
        if (cachedBuffer) {
          loadEpubData(cachedBuffer);
          return;
        }
      } catch (err) {
        console.warn("IndexedDB check:", err);
      }

      // If not in cache, show clean dropzone without blocking or hanging
      dropZone.style.display = 'flex';
      readerViewport.classList.add('hidden');
    }"""

    new_init_reader = """    // Immersive Header State Controls
    let isImmersiveMode = false;
    let headerHideTimer = null;

    function setImmersiveMode(enable) {
      isImmersiveMode = enable;
      const topHeader = document.getElementById('topHeader');
      const revealBtn = document.getElementById('headerRevealBtn');
      if (enable) {
        topHeader.classList.add('header-immersive');
        if (revealBtn) revealBtn.style.display = 'block';
      } else {
        topHeader.classList.remove('header-immersive', 'header-visible');
        if (revealBtn) revealBtn.style.display = 'none';
      }
    }

    function showHeader() {
      if (!isImmersiveMode) return;
      clearTimeout(headerHideTimer);
      const topHeader = document.getElementById('topHeader');
      if (topHeader) topHeader.classList.add('header-visible');
    }

    function scheduleHideHeader(delay = 600) {
      if (!isImmersiveMode) return;
      const appearanceMenu = document.getElementById('appearanceMenu');
      const tocDrawer = document.getElementById('tocDrawer');
      const quotesDrawer = document.getElementById('quotesDrawer');
      if (
        (appearanceMenu && !appearanceMenu.classList.contains('hidden')) ||
        (tocDrawer && !tocDrawer.classList.contains('-translate-x-full')) ||
        (quotesDrawer && !quotesDrawer.classList.contains('translate-x-full'))
      ) {
        return;
      }
      clearTimeout(headerHideTimer);
      headerHideTimer = setTimeout(() => {
        const topHeader = document.getElementById('topHeader');
        if (topHeader) topHeader.classList.remove('header-visible');
      }, delay);
    }

    function toggleHeaderVisible() {
      const topHeader = document.getElementById('topHeader');
      if (topHeader && topHeader.classList.contains('header-visible')) {
        scheduleHideHeader(0);
      } else {
        showHeader();
      }
    }

    function handleGlobalMouseMove(e) {
      if (!isImmersiveMode) return;
      if (e.clientY < 56) {
        showHeader();
      } else if (e.clientY > 80) {
        scheduleHideHeader(800);
      }
    }
    window.addEventListener('mousemove', handleGlobalMouseMove);

    async function initReader() {
      chapterDisplay.innerText = "";
      updateQuotesCount();

      // Check if this book is already cached in IndexedDB
      try {
        const cachedBuffer = await loadBookFromDB(bookId);
        if (cachedBuffer) {
          loadEpubData(cachedBuffer);
          return;
        }
      } catch (err) {
        console.warn("IndexedDB check:", err);
      }

      // If not in cache, show clean dropzone with pinned header
      setImmersiveMode(false);
      dropZone.style.display = 'flex';
      readerViewport.classList.add('hidden');
    }"""

    if old_init_reader in content:
        content = content.replace(old_init_reader, new_init_reader)
        print("  ✓ Added immersive header logic to initReader")
    else:
        print("  ⚠ Could not find exact old_init_reader")

    # 6. Update loadEpubData to enable immersive mode and renderBook to listen to mousemove
    old_load_epub = """    function loadEpubData(data) {
      dropZone.style.display = 'none';
      readerViewport.classList.remove('hidden');"""

    new_load_epub = """    function loadEpubData(data) {
      dropZone.style.display = 'none';
      readerViewport.classList.remove('hidden');
      setImmersiveMode(true);"""

    if old_load_epub in content:
        content = content.replace(old_load_epub, new_load_epub)
        print("  ✓ Added setImmersiveMode(true) in loadEpubData")
    else:
        print("  ⚠ Could not find exact old_load_epub")

    # In renderBook: add rendition.on("mousemove", handleGlobalMouseMove)
    old_render_bindings = """      rendition.on("click", () => {
        hideHighlightTooltip();
      });

      rendition.on("keydown", handleKeyNav);
    }"""

    new_render_bindings = """      rendition.on("click", () => {
        hideHighlightTooltip();
      });

      rendition.on("keydown", handleKeyNav);
      rendition.on("mousemove", handleGlobalMouseMove);
    }"""

    if old_render_bindings in content:
        content = content.replace(old_render_bindings, new_render_bindings)
        print("  ✓ Added mousemove binding on rendition in renderBook")
    else:
        print("  ⚠ Could not find exact old_render_bindings")

    # 7. Update applyThemeToRendition with Bookerly typography: line-height 1.5, regular-weight h1-h4, 1.4em indents
    old_typography = """      // Professional Kindle / Apple Books Typography:
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
      });"""

    new_typography = """      // Kindle Bookerly Typography Configuration:
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
        }
      });"""

    if old_typography in content:
        content = content.replace(old_typography, new_typography)
        print("  ✓ Updated typography to Kindle Bookerly spec")
    else:
        print("  ⚠ Could not find exact old_typography")

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
