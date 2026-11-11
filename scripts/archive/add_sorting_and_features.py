# scripts/add_sorting_and_features.py — Adds daily-seeded & alphabetical sorting across all 3 views, header 'Open Nooks Reader' button, direct named ebook downloads, and clean direct-reader empty states
# Usage: python3 scripts/add_sorting_and_features.py
# Requires: scripts/build_independent_bookshelf_app.py, bookshelf/reader.html, docs/reader.html, bookshelf/sw.js, docs/sw.js
#
# Gotchas:
# - In build_independent_bookshelf_app.py, HTML templates are inside a Python f-string; any literal curly braces in JS/CSS must be doubled ({{ and }}).
# - Daily random sorting uses a seeded PRNG (Mulberry32) keyed to YYYYMMDD, ensuring 100% consistent ordering throughout the day across all 3 views, while naturally rotating each midnight.
# - Drive downloads use drive.usercontent.google.com/download?id={id}&export=download to bypass the Google Drive web preview page and trigger direct browser file download named after the book title.

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def patch_build_script(file_path: Path):
    content = file_path.read_text(encoding="utf-8")

    # 1. Add "Open Nooks Reader" button in Header Controls (before Surprise Me)
    old_surprise_btn = re.search(r'<!-- Surprise Me -->\s*<button\s*onclick="openSurpriseModal\(\)"', content)
    if old_surprise_btn and 'openDirectNookReader()' not in content:
        nook_btn = """<!-- Open Nooks Reader -->
        <button 
          onclick="openDirectNookReader()" 
          title="Open Nooks Reader in Reading Room (open any EPUB directly)"
          class="shrink-0 px-2.5 sm:px-3 py-1.5 bg-[var(--terracotta)] text-white hover:bg-[var(--terracotta-hover)] rounded-xl text-xs font-bold transition flex items-center gap-1.5 shadow-sm cursor-pointer">
          <span>📖</span>
          <span class="hidden 2xl:inline">Open Nooks Reader</span>
          <span class="hidden md:inline 2xl:hidden">Nooks Reader</span>
          <span class="inline md:hidden">Nooks</span>
        </button>

        <!-- Surprise Me -->
        <button 
          onclick="openSurpriseModal()" """
        content = content[:old_surprise_btn.start()] + nook_btn + content[old_surprise_btn.end():]

    # 2. Add Sort Dropdown to Filter Ribbon
    # Replace existing Quotes Only container with Sort Dropdown + Quotes Only
    old_ribbon_right = re.search(
        r'<div class="flex items-center gap-3 text-xs text-\[var\(--text-muted\)\] shrink-0">[\s\S]*?<label class="flex items-center gap-1\.5 cursor-pointer font-medium hover:text-\[var\(--text-heading\)\] select-none">[\s\S]*?</label>',
        content
    )
    if old_ribbon_right:
        new_ribbon_right = """<div class="flex items-center gap-2.5 sm:gap-3 text-xs text-[var(--text-muted)] shrink-0">
        <!-- Sort Control -->
        <div class="flex items-center gap-1.5 bg-[var(--card-bg)] border border-[var(--border)] rounded-xl px-2.5 py-1 text-xs shadow-2xs">
          <span class="text-[var(--text-muted)] text-[11px] font-medium hidden sm:inline">Sort:</span>
          <select id="shelfSortSelect" onchange="handleSortChange(this.value)" class="bg-transparent text-[var(--text-heading)] font-semibold text-xs focus:outline-none cursor-pointer">
            <option value="daily">🎲 Daily Shuffle (Default)</option>
            <option value="title-asc">🔤 Title (A → Z)</option>
            <option value="title-desc">🔤 Title (Z → A)</option>
            <option value="author-asc">✍️ Author (A → Z)</option>
            <option value="quotes-desc">★ Most Quotes</option>
            <option value="category">📁 Category</option>
          </select>
        </div>

        <label class="flex items-center gap-1.5 cursor-pointer font-medium hover:text-[var(--text-heading)] select-none">
          <input type="checkbox" id="filterQuotesOnly" onchange="renderCurrentView()" class="rounded border-[var(--border)] accent-[var(--terracotta)] w-3.5 h-3.5" />
          <span class="hidden sm:inline">Quotes Only ({quote_count})</span>
          <span class="sm:hidden">Quotes ({quote_count})</span>
        </label>"""
        content = content[:old_ribbon_right.start()] + new_ribbon_right + content[old_ribbon_right.end():]

    # 3. Replace Surprise Drive button with Direct Download button in HTML modal
    content = content.replace(
        '<button id="surpriseDriveBtn" onclick="" class="px-4 py-2 bg-[var(--canvas)] border border-[var(--border)] hover:border-[var(--terracotta)] rounded-xl text-xs font-semibold text-[var(--text-heading)]">\n            Open in Drive ↗\n          </button>',
        '<button id="surpriseDownloadBtn" onclick="" class="px-4 py-2 bg-[var(--canvas)] border border-[var(--border)] hover:border-[var(--terracotta)] rounded-xl text-xs font-semibold text-[var(--text-heading)] flex items-center gap-1.5 cursor-pointer">\n            <span>⬇</span>\n            <span>Download Ebook</span>\n          </button>'
    )

    # 4. Replace Drive File ↗ in Split View Dossier with Download Ebook button
    split_drive_pattern = re.search(
        r'\$\{\{b\.drive_url \?\s*`\s*<a href="\$\{\{b\.drive_url\}\}" target="_blank" rel="noopener noreferrer" class="px-3\.5 py-2 bg-\[var\(--canvas\)\] border border-\[var\(--border\)\] hover:border-\[var\(--terracotta\)\] text-xs font-semibold text-\[var\(--text-heading\)\] rounded-xl transition flex items-center gap-1\.5">\s*<span>📁</span>\s*<span>Drive File ↗</span>\s*</a>\s*` : \'\'\}\}',
        content
    )
    if split_drive_pattern:
        new_split_download = """${{(b.drive_url || b.direct_download_url) ? `
                <button onclick="downloadBookFile(event, '${{b.id}}')" class="px-3.5 py-2 bg-[var(--canvas)] border border-[var(--border)] hover:border-[var(--terracotta)] text-xs font-semibold text-[var(--text-heading)] rounded-xl transition flex items-center gap-1.5 shadow-2xs cursor-pointer" title="Download ${{b.title}} directly">
                  <span>⬇</span>
                  <span>Download ${{(b.format && b.format.toUpperCase()) || 'Ebook'}}</span>
                </button>
              ` : ''}}"""
        content = content[:split_drive_pattern.start()] + new_split_download + content[split_drive_pattern.end():]

    # 5. Replace Drive File ↗ in Mobile Drawer with Download Ebook button
    drawer_drive_pattern = re.search(
        r'\$\{\{b\.drive_url \?\s*`\s*<a href="\$\{\{b\.drive_url\}\}" target="_blank" rel="noopener noreferrer" class="px-3 py-1\.5 bg-\[var\(--canvas\)\] border border-\[var\(--border\)\] text-xs font-semibold rounded-lg">\s*Drive File ↗\s*</a>\s*` : \'\'\}\}',
        content
    )
    if drawer_drive_pattern:
        new_drawer_download = """${{(b.drive_url || b.direct_download_url) ? `
                <button onclick="downloadBookFile(event, '${{b.id}}')" class="px-3 py-1.5 bg-[var(--canvas)] border border-[var(--border)] hover:border-[var(--terracotta)] text-xs font-semibold text-[var(--text-heading)] rounded-lg transition flex items-center gap-1.5 cursor-pointer">
                  <span>⬇</span>
                  <span>Download ${{(b.format && b.format.toUpperCase()) || 'Ebook'}}</span>
                </button>
              ` : ''}}"""
        content = content[:drawer_drive_pattern.start()] + new_drawer_download + content[drawer_drive_pattern.end():]

    # 6. Add sorting functions, openDirectNookReader, and downloadBookFile in JavaScript
    old_get_filtered = re.search(r'function getFilteredBooks\(\) \{\{[\s\S]*?return SHELF_DATA\.filter[\s\S]*?\n    \}\}', content)
    if old_get_filtered:
        new_filtering_and_sorting = """let activeSortMode = "daily";

    function handleSortChange(sortMode) {{
      activeSortMode = sortMode;
      renderCurrentView();
    }}

    function getDailySeed() {{
      const now = new Date();
      return now.getFullYear() * 10000 + (now.getMonth() + 1) * 100 + now.getDate();
    }}

    function mulberry32(a) {{
      return function() {{
        let t = a += 0x6D2B79F5;
        t = Math.imul(t ^ (t >>> 15), t | 1);
        t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
      }};
    }}

    function seededShuffle(array, seed) {{
      const prng = mulberry32(seed);
      const copy = array.slice();
      for (let i = copy.length - 1; i > 0; i--) {{
        const j = Math.floor(prng() * (i + 1));
        [copy[i], copy[j]] = [copy[j], copy[i]];
      }}
      return copy;
    }}

    function applyShelfSorting(books, sortMode) {{
      const arr = books.slice();
      if (sortMode === "daily") {{
        return seededShuffle(arr, getDailySeed());
      }} else if (sortMode === "title-asc") {{
        return arr.sort((a, b) => (a.title || "").localeCompare(b.title || "", undefined, {{ numeric: true, sensitivity: 'base' }}));
      }} else if (sortMode === "title-desc") {{
        return arr.sort((a, b) => (b.title || "").localeCompare(a.title || "", undefined, {{ numeric: true, sensitivity: 'base' }}));
      }} else if (sortMode === "author-asc") {{
        return arr.sort((a, b) => (a.author || "").localeCompare(b.author || "", undefined, {{ numeric: true, sensitivity: 'base' }}));
      }} else if (sortMode === "quotes-desc") {{
        return arr.sort((a, b) => ((b.quotes ? b.quotes.length : 0) - (a.quotes ? a.quotes.length : 0)));
      }} else if (sortMode === "category") {{
        return arr.sort((a, b) => (a.category || "").localeCompare(b.category || "") || (a.title || "").localeCompare(b.title || ""));
      }}
      return arr;
    }}

    function getFilteredBooks() {{
      const q = document.getElementById("searchInput").value.toLowerCase().trim();
      const quotesOnly = document.getElementById("filterQuotesOnly").checked;

      let list = SHELF_DATA.filter(b => {{
        if (activeCategory !== "All" && b.category !== activeCategory) return false;
        if (quotesOnly && !b.has_quote_bank) return false;
        if (q) {{
          const matchTitle = (b.title || "").toLowerCase().includes(q);
          const matchAuthor = (b.author || "").toLowerCase().includes(q);
          const matchPitch = (b.pitch || "").toLowerCase().includes(q);
          const matchQuotes = (b.quotes || []).some(item => (item.quote || "").toLowerCase().includes(q));
          if (!matchTitle && !matchAuthor && !matchPitch && !matchQuotes) return false;
        }}
        return true;
      }});

      return applyShelfSorting(list, activeSortMode);
    }}

    function openDirectNookReader() {{
      window.open('./reader.html', '_blank');
    }}

    function downloadBookFile(event, bookId) {{
      if (event) {{
        event.stopPropagation();
        event.preventDefault();
      }}
      const b = SHELF_DATA.find(item => item.id === bookId);
      if (!b) return;

      const rawFmt = (b.format && b.format.toLowerCase()) || '';
      const fmt = rawFmt === 'cbr' ? 'cbr' : (rawFmt === 'pdf' || (b.title && b.title.toLowerCase().endsWith('.pdf')) ? 'pdf' : 'epub');
      const filename = `${{b.title}}.${{fmt}}`;

      let targetUrl = b.direct_download_url;
      if (!targetUrl && b.drive_id) {{
        targetUrl = `https://drive.usercontent.google.com/download?id=${{b.drive_id}}&export=download`;
      }} else if (!targetUrl && b.drive_url) {{
        const m = b.drive_url.match(/\\/d\\/([a-zA-Z0-9_-]+)/) || b.drive_url.match(/id=([a-zA-Z0-9_-]+)/);
        if (m) {{
          targetUrl = `https://drive.usercontent.google.com/download?id=${{m[1]}}&export=download`;
        }} else {{
          targetUrl = b.drive_url;
        }}
      }}

      if (targetUrl) {{
        const a = document.createElement("a");
        a.href = targetUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(() => a.remove(), 1000);
        showToast(`Downloading "${{filename}}" directly...`);
      }} else {{
        showToast("No download link found for this book.");
      }}
    }}"""
        content = content[:old_get_filtered.start()] + new_filtering_and_sorting + content[old_get_filtered.end():]

    # 7. Update Surprise Modal button logic in spinSurprise
    old_surprise_drive = re.search(r'const driveBtn = document\.getElementById\("surpriseDriveBtn"\);[\s\S]*?driveBtn\.style\.display = "none";\s*\}\s*\}', content)
    if old_surprise_drive:
        new_surprise_download = """const downloadBtn = document.getElementById("surpriseDownloadBtn");
      if (chosen.drive_url || chosen.direct_download_url) {{
        downloadBtn.style.display = "inline-flex";
        downloadBtn.onclick = (e) => downloadBookFile(e, chosen.id);
      }} else {{
        downloadBtn.style.display = "none";
      }}
    }}"""
        content = content[:old_surprise_drive.start()] + new_surprise_download + content[old_surprise_drive.end():]

    file_path.write_text(content, encoding="utf-8")
    print(f"Patched build script: {file_path}")

def patch_reader_direct_open(file_path: Path):
    if not file_path.exists():
        return
    content = file_path.read_text(encoding="utf-8")

    # Update initialization in reader.html when opened directly without query params
    old_init_block = re.search(r'document\.title = `\$\{bookTitle\} • Reading Nook`;[\s\S]*?runningHeader\.innerText = `\$\{bookAuthor\.toUpperCase\(\)\} • \$\{bookTitle\.toUpperCase\(\)\}`;', content)
    if old_init_block:
        new_init_block = """const isDirectOpen = !urlParams.get('title');
    document.title = isDirectOpen ? 'Reading Nook • Reflowable EPUB Reader' : `${bookTitle} • Reading Nook`;
    bookTitleDisplay.innerText = isDirectOpen ? 'Reading Nook' : bookTitle;
    bookAuthorDisplay.innerText = isDirectOpen ? '' : `by ${bookAuthor}`;
    emptyStateTitle.innerText = isDirectOpen ? 'Welcome to Reading Nook' : bookTitle;
    emptyStateAuthor.innerText = isDirectOpen ? 'Reflowable typography, bifold spread & instant Quote Bank highlights.' : `by ${bookAuthor}`;
    runningHeader.innerText = isDirectOpen ? 'READING NOOK' : `${bookAuthor.toUpperCase()} • ${bookTitle.toUpperCase()}`;"""
        content = content[:old_init_block.start()] + new_init_block + content[old_init_block.end():]

    # Hide download button when there is no download link available (direct open)
    old_download_btn_logic = re.search(r'const hasDownloadTarget = directDownloadUrl[\s\S]*?if \(!hasDownloadTarget && !driveUrl\) \{[\s\S]*?\} else \{[\s\S]*?\}', content)
    if old_download_btn_logic:
        new_download_btn_logic = """const hasDownloadTarget = directDownloadUrl || (driveUrl && (driveUrl.includes('/d/') || driveUrl.includes('id=')));
    if (!hasDownloadTarget && !driveUrl) {
      if (downloadDirectBtn) {
        downloadDirectBtn.style.display = 'none';
      }
    } else {
      if (downloadDirectBtn) {
        downloadDirectBtn.style.display = 'flex';
      }
      if (downloadBtnLabel) downloadBtnLabel.innerText = `Download "${bookTitle}.epub" Directly`;
    }"""
        content = content[:old_download_btn_logic.start()] + new_download_btn_logic + content[old_download_btn_logic.end():]

    file_path.write_text(content, encoding="utf-8")
    print(f"Patched reader direct open state: {file_path}")

def bump_sw_version(sw_path: Path):
    if not sw_path.exists():
        return
    text = sw_path.read_text(encoding="utf-8")
    new_text = re.sub(r'mrc-cache-v\d+', 'mrc-cache-v10', text)
    sw_path.write_text(new_text, encoding="utf-8")
    print(f"Bumped cache version to v10 in {sw_path}")

def main():
    patch_build_script(ROOT / "scripts" / "build_independent_bookshelf_app.py")
    patch_reader_direct_open(ROOT / "bookshelf" / "reader.html")
    patch_reader_direct_open(ROOT / "docs" / "reader.html")
    bump_sw_version(ROOT / "bookshelf" / "sw.js")
    bump_sw_version(ROOT / "docs" / "sw.js")

if __name__ == "__main__":
    main()
