# scripts/apply_layout_and_reader_fixes.py — Applies responsive layout fixes for header buttons & editorial cards, and fixes Nooks EPUB reader async syntax & button hierarchy
# Usage: python3 scripts/apply_layout_and_reader_fixes.py
# Requires: bookshelf/reader.html, docs/reader.html, scripts/build_independent_bookshelf_app.py, bookshelf/sw.js, docs/sw.js
#
# Gotchas:
# - initReader() uses await loadBookFromDB(bookId), so it MUST be declared as async function initReader().
#   Omitting async causes a fatal SyntaxError in JavaScript engines before listeners can attach, breaking drag-and-drop.
# - Standard Tailwind CDN does not generate line-clamp above 6 by default. Explicit CSS with -webkit-line-clamp
#   must be injected into the <style> block for reliable responsive clamping across mobile, laptop, and desktop.
# - Direct Google Drive downloads must use drive.usercontent.google.com/download?id={id}&export=download to bypass
#   the Google Drive web preview page and trigger direct browser file download.

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def patch_reader_html(file_path: Path):
    if not file_path.exists():
        print(f"Warning: {file_path} not found.")
        return

    content = file_path.read_text(encoding="utf-8")

    # 1. Fix async initReader and triggerDirectDownload syntax
    content = re.sub(
        r'async\s+function\s+triggerDirectDownload\(\)',
        'function triggerDirectDownload()',
        content
    )
    content = re.sub(
        r'(?<!async\s)function\s+initReader\(\)',
        'async function initReader()',
        content
    )

    # 2. Update triggerDirectDownload and element initialization
    content = re.sub(
        r'const driveActionRow\s*=\s*document\.getElementById\(\'driveActionRow\'\);\s*\n\s*const driveDownloadBtn\s*=\s*document\.getElementById\(\'driveDownloadBtn\'\);',
        "const downloadDirectBtn = document.getElementById('downloadDirectBtn');\n    const downloadBtnLabel = document.getElementById('downloadBtnLabel');",
        content
    )

    old_download_wiring = re.search(
        r'if\s*\(directDownloadUrl\)\s*\{\s*driveActionRow\.classList\.remove[\s\S]*?\}\s*else\s*if\s*\(driveUrl\)\s*\{[\s\S]*?\}',
        content
    )
    if old_download_wiring:
        new_download_wiring = """const hasDownloadTarget = directDownloadUrl || (driveUrl && (driveUrl.includes('/d/') || driveUrl.includes('id=')));
    if (!hasDownloadTarget && !driveUrl) {
      if (downloadDirectBtn) {
        downloadDirectBtn.classList.add('opacity-50', 'cursor-not-allowed');
        if (downloadBtnLabel) downloadBtnLabel.innerText = "No Download Link Available";
      }
    } else {
      if (downloadBtnLabel) downloadBtnLabel.innerText = `Download "${bookTitle}.epub" Directly`;
    }"""
        content = content[:old_download_wiring.start()] + new_download_wiring + content[old_download_wiring.end():]

    old_download_func = re.search(r'function triggerDirectDownload\(\)\s*\{[\s\S]*?\n    \}', content)
    new_download_func = r"""function triggerDirectDownload() {
      let targetUrl = directDownloadUrl;
      if (!targetUrl && driveUrl) {
        const m = driveUrl.match(/\/d\/([a-zA-Z0-9_-]+)/) || driveUrl.match(/id=([a-zA-Z0-9_-]+)/);
        if (m) {
          targetUrl = `https://drive.usercontent.google.com/download?id=${m[1]}&export=download`;
        } else {
          targetUrl = driveUrl;
        }
      }

      if (targetUrl) {
        const a = document.createElement("a");
        a.href = targetUrl;
        a.download = `${bookTitle}.epub`;
        document.body.appendChild(a);
        a.click();
        setTimeout(() => a.remove(), 1000);
        showToast(`Downloading "${bookTitle}.epub" directly...`);
      } else {
        showToast("No download link found for this book.");
      }
    }"""
    if old_download_func:
        content = content[:old_download_func.start()] + new_download_func + content[old_download_func.end():]

    # 3. Update dropZone UI:
    # Button 1 (Top/Primary): Direct Download
    # Button 2 (Secondary): Open / Browse from Downloads
    # Drag & Drop Zone Box
    old_dropzone = re.search(r'<div id="dropZone"[\s\S]*?(?=<!-- 2\. Centered Reading Viewport)', content)
    if old_dropzone:
        new_dropzone = """<div id="dropZone" class="flex flex-col items-center justify-center p-6 text-center max-w-lg mx-auto z-20">
      <div class="w-16 h-16 rounded-2xl bg-[var(--terracotta-soft)] text-[var(--terracotta)] flex items-center justify-center text-3xl mb-4 shadow-inner">
        📖
      </div>
      <h2 id="emptyStateTitle" class="font-serif font-bold text-xl sm:text-2xl mb-1 leading-snug">Open in Reading Nook</h2>
      <p id="emptyStateAuthor" class="text-xs text-stone-500 mb-6">Kindle & Apple Books bifold typography with instant Quote Bank highlights.</p>

      <!-- 1st Button: Direct Download -->
      <button id="downloadDirectBtn" onclick="triggerDirectDownload()" class="w-full py-3.5 px-5 bg-[var(--terracotta)] hover:bg-[var(--terracotta-hover)] text-white text-sm font-bold rounded-2xl shadow-md transition flex items-center justify-center gap-2 mb-2.5 cursor-pointer">
        <span class="text-base">⬇</span>
        <span id="downloadBtnLabel">Download .epub File Directly</span>
      </button>

      <!-- 2nd Button: Open / Browse (from Downloads) -->
      <button onclick="document.getElementById('filePicker').click()" class="w-full py-3 px-5 border-2 border-[var(--terracotta)] text-[var(--terracotta)] hover:bg-[var(--terracotta-soft)] text-sm font-semibold rounded-2xl transition flex items-center justify-center gap-2 mb-3 cursor-pointer">
        <span class="text-base">📂</span>
        <span>Open / Browse .epub File (from Downloads)</span>
      </button>

      <!-- Drag & Drop Target Zone -->
      <div id="dropTargetBox" class="w-full border-2 border-dashed border-[var(--reader-border)] hover:border-[var(--terracotta)] rounded-2xl p-5 transition-colors bg-[var(--reader-bg)]/60 cursor-pointer mb-4 group" onclick="document.getElementById('filePicker').click()">
        <p class="font-semibold text-xs group-hover:text-[var(--terracotta)] transition">or drag & drop your <span class="text-[var(--terracotta)] font-mono">.epub</span> file here</p>
      </div>

      <!-- PDF Notice -->
      <div class="w-full mt-2 p-3 bg-stone-100 dark:bg-stone-800/50 rounded-xl text-left border border-[var(--reader-border)] text-[11px] text-stone-500 dark:text-stone-400 leading-relaxed">
        <p class="font-semibold text-stone-700 dark:text-stone-300 flex items-center gap-1 mb-0.5">
          <span>ℹ️</span><span>Reading a PDF book?</span>
        </p>
        <span>Nook specializes in reflowable EPUB typography. For PDF books, simply double-click the downloaded file to read in your browser or system PDF viewer.</span>
      </div>
    </div>

    """
        content = content[:old_dropzone.start()] + new_dropzone + content[old_dropzone.end():]

    # 4. Enhance drag-and-drop listeners with stopPropagation and active box feedback
    old_drag_block = re.search(r'// Drag and Drop support[\s\S]*?(?=async function processFile)', content)
    if old_drag_block:
        new_drag_block = """// Drag and Drop support
    window.addEventListener('dragover', e => {
      e.preventDefault();
      e.stopPropagation();
    });
    window.addEventListener('drop', e => {
      e.preventDefault();
      e.stopPropagation();
      if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) {
        processFile(e.dataTransfer.files[0]);
      }
    });

    const dropTargetBox = document.getElementById('dropTargetBox');
    if (dropTargetBox) {
      dropTargetBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropTargetBox.classList.add('border-[var(--terracotta)]', 'bg-[var(--terracotta-soft)]/20');
      });
      dropTargetBox.addEventListener('dragleave', (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropTargetBox.classList.remove('border-[var(--terracotta)]', 'bg-[var(--terracotta-soft)]/20');
      });
      dropTargetBox.addEventListener('drop', (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropTargetBox.classList.remove('border-[var(--terracotta)]', 'bg-[var(--terracotta-soft)]/20');
        if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) {
          processFile(e.dataTransfer.files[0]);
        }
      });
    }

    function handleFileSelect(e) {
      if (e.target.files && e.target.files[0]) {
        processFile(e.target.files[0]);
      }
    }

    """
        content = content[:old_drag_block.start()] + new_drag_block + content[old_drag_block.end():]

    file_path.write_text(content, encoding="utf-8")
    print(f"Patched {file_path}")

def patch_build_script(file_path: Path):
    if not file_path.exists():
        print(f"Warning: {file_path} not found.")
        return

    content = file_path.read_text(encoding="utf-8")

    # 1. Add custom CSS rules for .editorial-synopsis and responsive line clamping
    css_insert = """
    /* Editorial Card & Responsive Synopsis Clamp */
    .editorial-synopsis {{
      display: -webkit-box;
      -webkit-box-orient: vertical;
      overflow: hidden;
      text-overflow: ellipsis;
      -webkit-line-clamp: 6; /* mobile default */
    }}
    @media (min-width: 640px) {{
      .editorial-synopsis {{
        -webkit-line-clamp: 7;
      }}
    }}
    @media (min-width: 768px) {{
      .editorial-synopsis {{
        -webkit-line-clamp: 7;
      }}
    }}
    @media (min-width: 1024px) {{
      .editorial-synopsis {{
        -webkit-line-clamp: 9;
      }}
    }}
    @media (min-width: 1280px) {{
      .editorial-synopsis {{
        -webkit-line-clamp: 11;
      }}
    }}
    .editorial-synopsis.expanded {{
      display: block !important;
      -webkit-line-clamp: unset !important;
      overflow: visible !important;
    }}
"""
    if ".editorial-synopsis {" not in content:
        # Insert before </style>
        content = content.replace("  </style>", css_insert + "  </style>")

    # 2. Patch Header Buttons: "Surprise Me" and "Copy TBR" for all viewports
    old_buttons_pattern = re.search(
        r'<!-- Surprise Me -->[\s\S]*?<!-- Theme Toggle -->',
        content
    )
    if old_buttons_pattern:
        new_buttons = """<!-- Surprise Me -->
        <button 
          onclick="openSurpriseModal()" 
          title="Surprise me with a random book"
          class="shrink-0 px-2.5 sm:px-3 py-1.5 bg-[var(--amber-bg)] text-[var(--terracotta)] border border-[var(--terracotta)]/30 hover:bg-[var(--terracotta)] hover:text-white rounded-xl text-xs font-bold transition flex items-center gap-1.5 shadow-sm">
          <span>✨</span>
          <span class="hidden lg:inline">Surprise Me</span>
          <span class="hidden sm:inline lg:hidden">Surprise</span>
        </button>

        <!-- Copy TBR -->
        <button 
          onclick="copyAllTbr()" 
          title="Copy clean list for TBR trackers ({len(tbr_lines)} books)"
          class="shrink-0 px-2.5 sm:px-3 py-1.5 bg-[var(--card-bg)] hover:bg-[var(--card-hover)] border border-[var(--border)] text-[var(--text-heading)] rounded-xl text-xs font-semibold transition flex items-center gap-1.5 shadow-sm">
          <span>📋</span>
          <span class="hidden lg:inline">Copy TBR ({len(tbr_lines)})</span>
          <span class="hidden sm:inline lg:hidden">TBR ({len(tbr_lines)})</span>
        </button>

        <!-- Theme Toggle -->"""
        content = content[:old_buttons_pattern.start()] + new_buttons + content[old_buttons_pattern.end() - len('<!-- Theme Toggle -->'):]

    # 3. Patch Editorial Card template in renderEditorial
    # Make sure editorial-card has overflow-hidden, clean responsive synopsis clamp, and mt-auto on bottom action row
    old_ed_card = re.search(r'<div class="editorial-card[\s\S]*?<!-- Bottom Row Action -->', content)
    if old_ed_card:
        new_ed_card = """<div class="editorial-card bg-[var(--card-bg)] border border-[var(--border)] hover:border-[var(--terracotta)]/40 rounded-2xl p-4 sm:p-5 md:p-6 flex flex-row gap-4 sm:gap-6 hover:shadow-lg transition-all duration-200 cursor-pointer group items-stretch overflow-hidden" onclick="openBookDetail('${{b.id}}')">
            <!-- Cover (Left: substantial horizontal real estate, perfectly proportioned, 4 cards visible on screen) -->
            <div class="w-32 sm:w-40 md:w-48 lg:w-56 shrink-0 aspect-[2/3] book-cover ${{jacketCls}} relative rounded-xl overflow-hidden shadow-sm border border-black/10 flex items-center justify-center bg-[var(--border-subtle)]/40 p-1 self-start">
              ${{hasCover ? `
                <img src="${{b.cover_url}}" alt="${{b.title}}" loading="lazy" class="w-full h-full object-contain drop-shadow-xs rounded-lg" onerror="this.onerror=null;this.style.display='none';this.parentElement.querySelector('.fallback-ed').style.display='block';" />
                <div class="fallback-ed hidden absolute inset-0 w-full h-full">
                  ${{renderTypographicJacket(b)}}
                </div>
              ` : `
                <div class="w-full h-full">
                  ${{renderTypographicJacket(b)}}
                </div>
              `}}
              <div class="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-r from-black/15 to-transparent pointer-events-none"></div>
            </div>

            <!-- Content (Right: Clean back-cover synopsis & 1-click Read) -->
            <div class="flex-1 min-w-0 flex flex-col justify-between py-0.5">
              <div>
                <div class="flex items-center justify-between gap-2 mb-1.5">
                  <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--terracotta)] truncate">${{b.category}}</span>
                  ${{b.has_quote_bank ? `<span class="text-[9px] font-bold text-amber-950 bg-amber-300/90 px-1.5 py-0.5 rounded shrink-0">★ ${{b.quotes.length}} Quotes</span>` : ''}}
                </div>
                <h3 class="font-serif font-bold text-base sm:text-lg md:text-xl text-[var(--text-heading)] group-hover:text-[var(--terracotta)] transition leading-snug line-clamp-2">
                  ${{b.title}}
                </h3>
                <p class="text-xs sm:text-[13px] text-[var(--text-muted)] font-medium mt-0.5 line-clamp-1">by ${{b.author}}</p>

                <!-- Back of the Book Synopsis (Spacious, Elegant & Readable) -->
                <p id="pitch-${{b.id}}" class="editorial-synopsis font-serif text-xs sm:text-[13px] md:text-sm text-[var(--text-heading)]/85 mt-2.5 leading-relaxed transition-all">
                  ${{b.pitch}}
                </p>
                ${{b.pitch && b.pitch.length > 280 ? `
                  <button type="button" onclick="toggleExpandPitch(event, '${{b.id}}')" class="expand-btn-${{b.id}} text-[11px] font-bold text-[var(--terracotta)] hover:underline mt-1.5 inline-flex items-center gap-1 select-none">
                    <span>Read full synopsis ↓</span>
                  </button>
                ` : ''}}
              </div>

              <!-- Bottom Row Action -->"""
        content = content[:old_ed_card.start()] + new_ed_card + content[old_ed_card.end() - len('<!-- Bottom Row Action -->'):]

    # 4. Patch toggleExpandPitch in scripts/build_independent_bookshelf_app.py
    old_expand_func = re.search(r'function toggleExpandPitch\(event, bookId\) \{\{[\s\S]*?\n    \}\}', content)
    if old_expand_func:
        new_expand_func = """function toggleExpandPitch(event, bookId) {{
      if (event) {{
        event.stopPropagation();
        event.preventDefault();
      }}
      const p = document.getElementById(`pitch-${{bookId}}`);
      const btn = document.querySelector(`.expand-btn-${{bookId}}`);
      if (!p) return;

      const isExpanded = p.classList.contains("expanded");
      if (isExpanded) {{
        p.classList.remove("expanded");
        if (btn) btn.innerHTML = '<span>Read full synopsis ↓</span>';
      }} else {{
        p.classList.add("expanded");
        if (btn) btn.innerHTML = '<span>Show less ↑</span>';
      }}
    }}"""
        content = content[:old_expand_func.start()] + new_expand_func + content[old_expand_func.end():]

    file_path.write_text(content, encoding="utf-8")
    print(f"Patched {file_path}")

def bump_sw_version(sw_path: Path):
    if not sw_path.exists():
        return
    text = sw_path.read_text(encoding="utf-8")
    new_text = re.sub(r'mrc-cache-v\d+', 'mrc-cache-v9', text)
    sw_path.write_text(new_text, encoding="utf-8")
    print(f"Bumped cache version to v9 in {sw_path}")

def main():
    patch_reader_html(ROOT / "bookshelf" / "reader.html")
    patch_reader_html(ROOT / "docs" / "reader.html")
    patch_build_script(ROOT / "scripts" / "build_independent_bookshelf_app.py")
    bump_sw_version(ROOT / "bookshelf" / "sw.js")
    bump_sw_version(ROOT / "docs" / "sw.js")

if __name__ == "__main__":
    main()
