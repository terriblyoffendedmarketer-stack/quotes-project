# scripts/migrations/fix_bookshelf_template_2026_11.py — ONE-TIME bug-fix pass over scripts/templates/bookshelf.html
# Usage: python3 scripts/migrations/fix_bookshelf_template_2026_11.py  (run once on 2026-11-11; asserts every edit applies)
# Fixes: HTML escaping of book text, Copy-TBR quoting bug, stale title/author overrides in localStorage,
#        pinned Tailwind CDN, simplified format helpers, "Recently added" sort + NEW badge.
import re
from pathlib import Path
P = Path(__file__).resolve().parents[2] / "scripts" / "templates" / "bookshelf.html"
s = P.read_text(encoding="utf-8")

def sub(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, f"expected {count}x, found {n}: {old[:70]!r}"
    s = s.replace(old, new)

# 1. Pinned, official Tailwind v3 play CDN (was an internal gstatic "antigravity/dev" copy of v3)
sub('<script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>',
    '<script src="https://cdn.tailwindcss.com/3.4.16"></script>')

# 2. Stale localStorage overrides: old builds saved title/author on every cover toggle, which froze the
#    old (often swapped) names on the device. Migrate once: drop title/author from legacy entries.
sub('''      const saved = localStorage.getItem("exlibris_shelf_edits");
      if (saved) {
        const overrides = JSON.parse(saved);''',
'''      const saved = localStorage.getItem("exlibris_shelf_edits");
      if (saved) {
        const overrides = JSON.parse(saved);
        if (!localStorage.getItem("exlibris_edits_v2")) {
          Object.values(overrides).forEach(ov => { delete ov.title; delete ov.author; });
          localStorage.setItem("exlibris_shelf_edits", JSON.stringify(overrides));
          localStorage.setItem("exlibris_edits_v2", "1");
        }''')
sub('''      saved[b.id] = Object.assign(saved[b.id] || {}, {
        title: b.title,
        author: b.author,
        cover_url: b.cover_url,''', '''      saved[b.id] = Object.assign(saved[b.id] || {}, {
        cover_url: b.cover_url,''')

# 3. HTML-escape helper + id-based Copy TBR (titles with quotes broke the inline onclick)
sub('''    function showToast(msg) {''', '''    const ESC_MAP = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
    function esc(v) {
      return String(v == null ? "" : v).replace(/[&<>"']/g, ch => ESC_MAP[ch]);
    }

    function copyTbrById(bookId) {
      const b = SHELF_DATA.find(item => item.id === bookId);
      if (b) copySingleTbr(b.title, b.author);
    }

    function isNewBook(b) {
      if (!b.added) return false;
      return (Date.now() - new Date(b.added).getTime()) < 30 * 86400000;
    }

    function showToast(msg) {''')
old_copy = '''copySingleTbr('${b.title.replace(/'/g, "\\\\\\'")}', '${b.author.replace(/'/g, "\\\\\\'")}')'''
sub(old_copy, "copyTbrById('${b.id}')", count=2)

# 4. Escape every book-text interpolation inside HTML templates (not toasts / URLs / filenames, which
#    use innerText or encodeURIComponent and must stay raw)
FIELDS = r"(b|chosen)\.(title|author|category|pitch)"
out = []
for line in s.split("\n"):
    if not any(k in line for k in ("showToast(", "const filename", "readerUrl", "copyToClipboard")):
        line = re.sub(r"\$\{" + FIELDS + r"\}", lambda m: "${esc(" + m.group(1) + "." + m.group(2) + ")}", line)
        line = line.replace("${q.quote}", "${esc(q.quote)}").replace("${q.explanation}", "${esc(q.explanation)}")
        line = line.replace("${authorDisplay}", "${esc(authorDisplay)}").replace("${hook}", "${esc(hook)}")
        line = line.replace("b.categories.join(' • ') : b.category}", "esc(b.categories.join(' • ')) : esc(b.category)}")
    out.append(line)
s = "\n".join(out)
sub("mb-2.5 last:mb-0\">${p}</p>", "mb-2.5 last:mb-0\">${esc(p)}</p>")

# 5. Format helpers: build now normalises format, so drop the legacy SUNSTEIN/title-suffix hacks
sub('''        function getCleanFormat(b) {
      let fmt = (b.format || '').trim().toUpperCase();
      if (fmt.includes('SUNSTEIN') || !fmt) {
        if (b.title && b.title.toLowerCase().endsWith('.pdf')) return 'PDF';
        if (b.title && b.title.toLowerCase().endsWith('.cbr')) return 'CBR';
        return (b.id && (b.id.includes('reading-order') || b.id.includes('hbr'))) ? 'PDF' : 'EPUB';
      }
      return fmt;
    }''', '''    function getCleanFormat(b) {
      return ((b.format || "EPUB").trim().toUpperCase()) || "EPUB";
    }''')
sub('''      const rawFmt = (b.format && b.format.toLowerCase()) || '';
      const fmt = rawFmt === 'cbr' ? 'cbr' : (rawFmt === 'pdf' || (b.title && b.title.toLowerCase().endsWith('.pdf')) ? 'pdf' : 'epub');
      const filename = `${b.title}.${fmt}`;''', '''      const fmt = getCleanFormat(b).toLowerCase();
      const filename = `${b.title.replace(/[\\\\/:*?"<>|]+/g, " ").trim()}.${fmt}`;''')

# 6. "Recently added" sort (uses the Drive modified time the build now stores in b.added) + NEW badge
sub('''      } else if (sortMode === "category") {''', '''      } else if (sortMode === "recent") {
        return arr.sort((a, b) => (b.added || "").localeCompare(a.added || ""));
      } else if (sortMode === "category") {''')
s_before = s
s = re.sub(r'(<option value="title-asc"[^>]*>)', r'<option value="recent">Recently Added</option>\n            \1', s)
assert s != s_before, "sort <select> not found"
sub('''              <!-- Top-Left Permanent Format Badge -->
              <div class="absolute top-2 left-2 z-10 flex items-center gap-1.5 pointer-events-none">
                ${getFormatBadgeHtml(fmt)}''', '''              <!-- Top-Left Permanent Format Badge -->
              <div class="absolute top-2 left-2 z-10 flex items-center gap-1.5 pointer-events-none">
                ${getFormatBadgeHtml(fmt)}
                ${isNewBook(b) ? '<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[9px] font-bold tracking-wider uppercase bg-amber-400 text-amber-950 shadow-sm">New</span>' : ''}''')

P.write_text(s, encoding="utf-8")
print("template fixed")
