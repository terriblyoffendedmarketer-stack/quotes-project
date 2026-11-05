# scripts/patch_format_tags_and_surprise.py — Normalizes format metadata (EPUB/PDF/CBR) across all 620 books, adds visible format badges to all 3 shelf views, and optimizes the Surprise Me modal with Read on Nooks and direct downloads
# Usage: python3 scripts/patch_format_tags_and_surprise.py
# Requires: scripts/build_independent_bookshelf_app.py, bookshelf/sw.js, docs/sw.js
#
# Gotchas:
# - In build_independent_bookshelf_app.py, double-curly braces {{ and }} must be used for JS/CSS inside Python f-strings.
# - Some books had missing or corrupted format strings (e.g. ' SUNSTEIN'); get_canonical_format guarantees every book has a valid format (EPUB, PDF, CBR, CBZ, MOBI).
# - Format tags must appear visibly in both image cover and typographic jacket states across Board, Editorial, Split, and Surprise views.

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def patch():
    build_script = ROOT / "scripts" / "build_independent_bookshelf_app.py"
    content = build_script.read_text(encoding="utf-8")

    # 1. Update MANUAL_BOOK_FIXES to fix the non-standard format books
    fixes_to_add = """
    "nudge-richard-h-thaler-prof-cass-r-sunstein": {
        "title": "Nudge: Improving Decisions About Health, Wealth, and Happiness",
        "author": "Richard H. Thaler & Cass R. Sunstein",
        "format": "EPUB"
    },
    "reading-order-unknown": {
        "title": "Fyodor Dostoevsky: Reading Order & Chronological Guide",
        "author": "Fyodor Dostoevsky",
        "format": "PDF"
    },
    "rilke-letters-to-a-young-poet": {
        "title": "Letters to a Young Poet",
        "author": "Rainer Maria Rilke",
        "format": "EPUB"
    },
    "hbr-on-communication-unknown": {
        "title": "HBR's 10 Must Reads on Communication",
        "author": "Harvard Business Review",
        "format": "PDF"
    },
    "build-an-unorthodox-guide-to-making-things-worth-making-tony-fadell": {
        "title": "Build: An Unorthodox Guide to Making Things Worth Making",
        "author": "Tony Fadell",
        "format": "EPUB"
    },
    "user-story-mapping-jeff-patton-peter-economy": {
        "title": "User Story Mapping: Discover the Whole Story, Build the Right Product",
        "author": "Jeff Patton & Peter Economy",
        "format": "EPUB"
    },
"""
    if '"nudge-richard-h-thaler-prof-cass-r-sunstein"' not in content:
        content = content.replace("MANUAL_BOOK_FIXES = {", "MANUAL_BOOK_FIXES = {" + fixes_to_add)

    # 2. Add canonical format cleanup in Python build()
    old_build_loop = re.search(r'for b in shelf_books:\s*bid = b\.get\("id"\)', content)
    canonical_fmt_py = """def get_canonical_format_py(b):
    fmt = (b.get("format") or "").strip().upper()
    bid = b.get("id", "")
    t = (b.get("title") or "").lower()
    fn = (b.get("filename") or "").lower()
    if "sunstein" in fmt.lower() or bid == "nudge-richard-h-thaler-prof-cass-r-sunstein":
        return "EPUB"
    if bid in ["reading-order-unknown", "hbr-on-communication-unknown"]:
        return "PDF"
    if bid in ["rilke-letters-to-a-young-poet", "build-an-unorthodox-guide-to-making-things-worth-making-tony-fadell", "user-story-mapping-jeff-patton-peter-economy"]:
        return "EPUB"
    if fmt in ["EPUB", "PDF", "CBR", "CBZ", "MOBI"]:
        return fmt
    if t.endswith(".pdf") or fn.endswith(".pdf"):
        return "PDF"
    if t.endswith(".cbr") or fn.endswith(".cbr"):
        return "CBR"
    if t.endswith(".cbz") or fn.endswith(".cbz"):
        return "CBZ"
    if t.endswith(".mobi") or fn.endswith(".mobi"):
        return "MOBI"
    return "EPUB"

"""
    if "def get_canonical_format_py" not in content:
        content = content.replace("def build():", canonical_fmt_py + "def build():")
        content = content.replace(
            '            b["drive_id"] = fid',
            '            b["format"] = get_canonical_format_py(b)\n            b["drive_id"] = fid'
        )

    # 3. Update Surprise Modal HTML markup
    old_surprise_modal_footer = re.search(
        r'<div class="flex items-center justify-between pt-4 border-t border-\[var\(--border\)\]">[\s\S]*?</div>\s*</div>\s*</div>\s*<!-- Edit Details',
        content
    )
    if old_surprise_modal_footer:
        new_surprise_modal_footer = """<div class="flex flex-wrap items-center justify-between gap-3 pt-4 border-t border-[var(--border)]">
        <button onclick="spinSurprise()" class="px-4 py-2.5 bg-[var(--canvas)] hover:bg-[var(--card-hover)] border border-[var(--border)] text-[var(--text-heading)] text-xs font-bold rounded-xl shadow-2xs transition flex items-center gap-2 cursor-pointer">
          <span>🎲</span>
          <span>Spin Again</span>
        </button>
        <div class="flex flex-wrap items-center gap-2">
          <button id="surpriseReadBtn" onclick="" class="px-4 py-2.5 bg-[var(--terracotta)] hover:bg-[var(--terracotta-hover)] text-white rounded-xl text-xs font-bold transition flex items-center gap-1.5 shadow-xs cursor-pointer">
            <span>📖</span>
            <span id="surpriseReadBtnLabel">Read on Nooks ↗</span>
          </button>
          <button id="surpriseDownloadBtn" onclick="" class="px-3.5 py-2.5 bg-[var(--canvas)] border border-[var(--border)] hover:border-[var(--terracotta)] rounded-xl text-xs font-semibold text-[var(--text-heading)] flex items-center gap-1.5 cursor-pointer">
            <span>⬇</span>
            <span id="surpriseDownloadBtnLabel">Download Ebook</span>
          </button>
          <button onclick="copySingleTbr(currentSurpriseBook.title, currentSurpriseBook.author)" class="px-3.5 py-2.5 bg-[var(--canvas)] border border-[var(--border)] rounded-xl text-xs font-medium text-[var(--text-muted)] hover:text-[var(--text-heading)] transition flex items-center gap-1.5 cursor-pointer">
            <span>📋</span>
            <span>Copy TBR</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Edit Details"""
        content = content[:old_surprise_modal_footer.start()] + new_surprise_modal_footer + content[old_surprise_modal_footer.end() - len('<!-- Edit Details'):]

    # 4. Inject format badge helpers in JavaScript
    js_helpers = """    function getCleanFormat(b) {{
      let fmt = (b.format || '').trim().toUpperCase();
      if (fmt.includes('SUNSTEIN') || !fmt) {{
        if (b.title && b.title.toLowerCase().endsWith('.pdf')) return 'PDF';
        if (b.title && b.title.toLowerCase().endsWith('.cbr')) return 'CBR';
        return (b.id && (b.id.includes('reading-order') || b.id.includes('hbr'))) ? 'PDF' : 'EPUB';
      }}
      return fmt;
    }}

    function getFormatBadgeHtml(format) {{
      const fmt = (format || 'EPUB').toUpperCase();
      if (fmt === 'PDF') {{
        return `<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[9px] font-bold tracking-wider uppercase bg-rose-500/15 text-rose-700 dark:text-rose-300 border border-rose-500/30 shrink-0" title="PDF Document">PDF</span>`;
      }} else if (fmt === 'CBR' || fmt === 'CBZ') {{
        return `<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[9px] font-bold tracking-wider uppercase bg-purple-500/15 text-purple-700 dark:text-purple-300 border border-purple-500/30 shrink-0" title="Comic Book Archive">${{fmt}}</span>`;
      }} else {{
        return `<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[9px] font-bold tracking-wider uppercase bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30 shrink-0" title="Reflowable EPUB">EPUB</span>`;
      }}
    }}
"""
    if "function getFormatBadgeHtml" not in content:
        content = content.replace("function getFilteredBooks() {{", js_helpers + "\n    function getFilteredBooks() {{")

    # 5. Patch Board View: ensure format badge is on cover top-left AND in metadata beneath card
    # Cover top-left badge (for both cover and fallback)
    old_board_card = re.search(r'function renderBoard\(books\) \{\{[\s\S]*?grid\.innerHTML = books\.map\(b => \{\{[\s\S]*?return `\s*<div class="book-card[\s\S]*?<!-- Meta Beneath -->[\s\S]*?<\/div>\s*<\/div>\s*`;\s*\}\}\)\.join\(""\);', content)
    if old_board_card:
        new_board_code = """function renderBoard(books) {{
      const grid = document.getElementById("boardGrid");
      if (books.length === 0) {{
        grid.innerHTML = `<div class="col-span-full py-20 text-center text-sm text-[var(--text-muted)]">No matching books found.</div>`;
        return;
      }}

      grid.innerHTML = books.map(b => {{
        const jacketCls = getJacketStyle(b.category);
        const hasCover = !!b.cover_url && !b.no_cover;
        const hook = extractFirstWhyReadHook(b.why_love);
        const fmt = getCleanFormat(b);

        return `
          <div class="book-card group cursor-pointer relative" onclick="openBookDetail('${{b.id}}')">
            <!-- Book Cover -->
            <div class="book-cover ${{jacketCls}} relative overflow-hidden rounded-[8px] shadow-md transition-all duration-200 group-hover:shadow-2xl group-hover:-translate-y-1.5 aspect-[2/3]">
              ${{hasCover ? `
                <img src="${{b.cover_url}}" alt="${{b.title}}" loading="lazy" class="w-full h-full object-cover z-0" onerror="this.onerror=null;this.style.display='none';this.parentElement.querySelector('.fallback-jacket').style.display='block';" />
                <div class="fallback-jacket hidden absolute inset-0 z-0 w-full h-full">
                  ${{renderTypographicJacket(b)}}
                </div>
              ` : `
                ${{renderTypographicJacket(b)}}
              `}}

              <!-- Top-Left Permanent Format Badge -->
              <div class="absolute top-2 left-2 z-10 flex items-center gap-1.5 pointer-events-none">
                ${{getFormatBadgeHtml(fmt)}}
              </div>

              <!-- Hover Peek Card Overlay (Context on Hover) -->
              <div class="hover-preview opacity-0 pointer-events-none group-hover:opacity-100 group-hover:pointer-events-auto transition-opacity duration-200 absolute inset-0 bg-[#151311]/95 text-white p-4 flex flex-col justify-between rounded-[8px] z-20 backdrop-blur-xs shadow-inner">
                <div>
                  <div class="flex items-center justify-between mb-1.5">
                    <div class="flex items-center gap-1.5">
                      ${{getFormatBadgeHtml(fmt)}}
                      <span class="text-[9px] font-mono uppercase tracking-wider text-amber-300 font-bold truncate max-w-[100px]">${{b.category}}</span>
                    </div>
                    ${{b.has_quote_bank ? `<span class="text-[9px] font-bold text-amber-300 shrink-0">★ ${{b.quotes.length}} Quotes</span>` : ''}}
                  </div>
                  <h4 class="font-serif font-bold text-xs sm:text-sm text-white leading-snug line-clamp-2">${{b.title}}</h4>
                  <p class="text-[10px] text-white/70 mt-0.5 line-clamp-1">by ${{b.author}}</p>

                  <div class="mt-3 pt-2 border-t border-white/15">
                    <span class="text-[9px] font-bold uppercase tracking-wider text-amber-300 block mb-1">✦ Curator's Hook:</span>
                    <p class="text-[10px] text-white/90 leading-relaxed line-clamp-4">${{hook}}</p>
                  </div>
                </div>

                <div class="pt-2 border-t border-white/15 flex items-center justify-between text-[10px]">
                  <button onclick="openBookInNook(event, '${{b.id}}')" class="text-amber-300 font-bold hover:underline flex items-center gap-1">
                    <span>${{ (fmt === 'PDF') ? '📄 Open PDF ↗' : '📖 Read on Nooks ↗' }}</span>
                  </button>
                  <span class="text-white/80 font-semibold">Dossier →</span>
                </div>
              </div>
            </div>

            <!-- Meta Beneath -->
            <div class="pt-2.5 px-0.5">
              <h4 class="font-serif font-bold text-xs sm:text-sm text-[var(--text-heading)] group-hover:text-[var(--terracotta)] transition leading-snug line-clamp-2">
                ${{b.title}}
              </h4>
              <p class="text-[11px] text-[var(--text-muted)] font-medium mt-0.5 line-clamp-1">
                ${{b.author}}
              </p>
              <div class="flex items-center gap-1.5 mt-1.5 text-[10px]">
                <span class="text-[var(--terracotta)] font-semibold truncate">${{b.category}}</span>
                ${{getFormatBadgeHtml(fmt)}}
                ${{b.has_quote_bank ? `<span class="text-[var(--text-muted)]">• ${{b.quotes.length}} Quotes</span>` : ''}}
              </div>
            </div>
          </div>
        `;
      }}).join("");"""
        content = content[:old_board_card.start()] + new_board_code + content[old_board_card.end():]

    # 6. Patch Editorial View: include format badge in header row
    old_ed_header = re.search(
        r'<div class="flex items-center justify-between gap-2 mb-1\.5">\s*<span class="text-\[10px\] font-bold uppercase tracking-wider text-\[var\(--terracotta\)\] truncate">\$\{\{b\.category\}\}</span>',
        content
    )
    if old_ed_header:
        new_ed_header = """<div class="flex items-center justify-between gap-2 mb-1.5">
                  <div class="flex items-center gap-2 truncate">
                    <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--terracotta)] truncate">${{b.category}}</span>
                    ${{getFormatBadgeHtml(getCleanFormat(b))}}
                  </div>"""
        content = content[:old_ed_header.start()] + new_ed_header + content[old_ed_header.end():]

    # 7. Patch Split View: include format badge in left list item and in dossier
    old_split_meta = re.search(
        r'<div class="flex items-center gap-2 mt-1 text-\[10px\]">\s*<span class="text-\[var\(--terracotta\)\] font-semibold">\$\{\{b\.category\}\}</span>',
        content
    )
    if old_split_meta:
        new_split_meta = """<div class="flex items-center gap-1.5 mt-1 text-[10px]">
                <span class="text-[var(--terracotta)] font-semibold truncate">${{b.category}}</span>
                ${{getFormatBadgeHtml(getCleanFormat(b))}}"""
        content = content[:old_split_meta.start()] + new_split_meta + content[old_split_meta.end():]

    old_dossier_cat = re.search(
        r'<span class="text-\[10px\] font-bold uppercase tracking-wider text-\[var\(--terracotta\)\]">\$\{\{b\.category\}\}</span>\s*<h2 class="font-serif font-bold text-2xl md:text-3xl text-\[var\(--text-heading\)\] mt-1 leading-tight">\s*\$\{\{b\.title\}\}',
        content
    )
    if old_dossier_cat:
        new_dossier_cat = """<div class="flex items-center gap-2 mb-1">
              <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--terracotta)]">${{b.category}}</span>
              ${{getFormatBadgeHtml(getCleanFormat(b))}}
            </div>
            <h2 class="font-serif font-bold text-2xl md:text-3xl text-[var(--text-heading)] mt-0.5 leading-tight">
              ${{b.title}}"""
        content = content[:old_dossier_cat.start()] + new_dossier_cat + content[old_dossier_cat.end():]

    # 8. Patch Mobile Drawer: include format badge
    old_drawer_cat = re.search(
        r'<div>\s*<span class="text-\[10px\] font-bold uppercase tracking-wider text-\[var\(--terracotta\)\]">\$\{\{b\.category\}\}</span>\s*<h3 class="font-serif font-bold text-lg text-\[var\(--text-heading\)\] mt-0\.5 leading-snug">\$\{\{b\.title\}\}</h3>',
        content
    )
    if old_drawer_cat:
        new_drawer_cat = """<div>
            <div class="flex items-center gap-2 mb-1">
              <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--terracotta)]">${{b.category}}</span>
              ${{getFormatBadgeHtml(getCleanFormat(b))}}
            </div>
            <h3 class="font-serif font-bold text-lg text-[var(--text-heading)] mt-0.5 leading-snug">${{b.title}}</h3>"""
        content = content[:old_drawer_cat.start()] + new_drawer_cat + content[old_drawer_cat.end():]

    # 9. Patch Surprise Me spinSurprise logic to wire Read on Nooks and Download button
    old_spin_surprise = re.search(r'function spinSurprise\(\) \{\{[\s\S]*?currentSurpriseBook = chosen;[\s\S]*?res\.innerHTML = `[\s\S]*?const downloadBtn = document\.getElementById\("surpriseDownloadBtn"\);[\s\S]*?downloadBtn\.style\.display = "none";\s*\}\s*\}\s*\}', content)
    if old_spin_surprise:
        new_spin_surprise = """function spinSurprise() {{
      const pool = SHELF_DATA.filter(b => b.is_fun_pick);
      const chosen = pool[Math.floor(Math.random() * pool.length)] || SHELF_DATA[Math.floor(Math.random() * SHELF_DATA.length)];
      currentSurpriseBook = chosen;

      const res = document.getElementById("surpriseResult");
      const jacketCls = getJacketStyle(chosen.category);
      const cleanFmt = getCleanFormat(chosen);

      res.innerHTML = `
        <div class="flex flex-col sm:flex-row gap-5 items-start p-4 md:p-5 bg-[var(--canvas)] border border-[var(--border)] rounded-2xl max-h-[60vh] overflow-y-auto">
          <div class="w-28 md:w-32 shrink-0 aspect-[2/3] book-cover ${{jacketCls}} shadow-md relative overflow-hidden rounded-[8px] bg-[var(--border-subtle)]/40 p-1">
            ${{chosen.cover_url && !chosen.no_cover ? `
              <img src="${{chosen.cover_url}}" alt="${{chosen.title}}" class="w-full h-full object-contain drop-shadow-xs rounded-lg" onerror="this.onerror=null;this.style.display='none';this.parentElement.querySelector('.fallback-surprise').style.display='block';" />
              <div class="fallback-surprise hidden absolute inset-0 z-10 w-full h-full">
                ${{renderTypographicJacket(chosen)}}
              </div>
            ` : `
              <div class="w-full h-full">
                ${{renderTypographicJacket(chosen)}}
              </div>
            `}}
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--terracotta)]">${{chosen.category}}</span>
              ${{getFormatBadgeHtml(cleanFmt)}}
              ${{chosen.has_quote_bank ? `<span class="text-[9px] font-bold text-amber-950 bg-amber-300/90 px-1.5 py-0.5 rounded">★ ${{chosen.quotes.length}} Quotes</span>` : ''}}
            </div>
            <h3 class="font-serif font-bold text-lg md:text-xl text-[var(--text-heading)] mt-0.5 leading-snug">${{chosen.title}}</h3>
            <p class="text-xs text-[var(--text-muted)] font-medium">by ${{chosen.author}}</p>

            <div class="mt-3 p-3 bg-[var(--card-bg)] border border-[var(--border-subtle)] rounded-xl">
              <span class="block text-[10px] font-bold uppercase tracking-wider text-[var(--text-muted)] mb-1">Back of the Book:</span>
              <p class="text-xs text-[var(--text-heading)] font-serif leading-relaxed">${{chosen.pitch}}</p>
            </div>
            <div class="mt-3 p-3.5 bg-gradient-to-br from-[var(--amber-bg)] to-[var(--card-bg)] border border-[var(--terracotta)]/25 rounded-xl space-y-1.5">
              <span class="block text-[10px] font-bold uppercase tracking-wider text-[var(--terracotta)]">✦ Curator's Note:</span>
              <div class="editorial-prose text-xs leading-relaxed space-y-2">
                ${{formatWhyRead(chosen.why_love)}}
              </div>
            </div>
          </div>
        </div>
      `;

      const readBtn = document.getElementById("surpriseReadBtn");
      const readBtnLabel = document.getElementById("surpriseReadBtnLabel");
      const downloadBtn = document.getElementById("surpriseDownloadBtn");
      const downloadBtnLabel = document.getElementById("surpriseDownloadBtnLabel");

      const isPdf = cleanFmt === 'PDF' || (chosen.title && chosen.title.toLowerCase().endsWith('.pdf'));

      if (readBtn) {{
        readBtn.onclick = (e) => openBookInNook(e, chosen.id);
        if (readBtnLabel) {{
          readBtnLabel.innerText = isPdf ? "Open PDF ↗" : "Read on Nooks ↗";
        }}
      }}

      if (downloadBtn) {{
        if (chosen.drive_url || chosen.direct_download_url) {{
          downloadBtn.style.display = "inline-flex";
          downloadBtn.onclick = (e) => downloadBookFile(e, chosen.id);
          if (downloadBtnLabel) {{
            downloadBtnLabel.innerText = `Download ${{cleanFmt}}`;
          }}
        }} else {{
          downloadBtn.style.display = "none";
        }}
      }}
    }}"""
        content = content[:old_spin_surprise.start()] + new_spin_surprise + content[old_spin_surprise.end():]

    build_script.write_text(content, encoding="utf-8")
    print(f"Patched {build_script}")

def bump_sw_version(sw_path: Path):
    if not sw_path.exists():
        return
    text = sw_path.read_text(encoding="utf-8")
    new_text = re.sub(r'mrc-cache-v\d+', 'mrc-cache-v11', text)
    sw_path.write_text(new_text, encoding="utf-8")
    print(f"Bumped cache version to v11 in {sw_path}")

def main():
    patch()
    bump_sw_version(ROOT / "bookshelf" / "sw.js")
    bump_sw_version(ROOT / "docs" / "sw.js")

if __name__ == "__main__":
    main()
