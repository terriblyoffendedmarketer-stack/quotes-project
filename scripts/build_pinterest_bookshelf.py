# scripts/build_pinterest_bookshelf.py — Compiles the redesigned Pinterest-style Visual Board & Bookshelf Split View
# Usage: python3 scripts/build_pinterest_bookshelf.py
# Requires: content/books_curated_shelf.json, content/tbr_clean_list.txt
#
# Gotchas:
# - Default view must be the Pinterest visual board where book covers take center stage.
# - Seamless toggle between 'Pinterest Board' and 'Bookshelf Split' (two-pane with dossier on right).
# - Curated 'Surprise Me' engine draws exclusively from fun fiction and non-fiction by novelists.
# - High-end editorial typography with serif fonts and physical book jacket aesthetics.

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHELF_JSON = ROOT / "content" / "books_curated_shelf.json"
TBR_CLEAN_LIST = ROOT / "content" / "tbr_clean_list.txt"

SHELF_HTML_PROTO = ROOT / "prototype" / "shelf.html"
SHELF_HTML_DOCS = ROOT / "docs" / "shelf.html"
ARTIFACT_PATH = Path("/Users/apple/.gemini/antigravity/brain/81ccc3e6-122f-446d-b723-e563a56f7ea9/dynamic_bookshelf.html")

def build_app():
    print("Loading books catalog...")
    shelf_books = json.loads(SHELF_JSON.read_text(encoding="utf-8"))
    tbr_lines = [l.strip() for l in TBR_CLEAN_LIST.read_text(encoding="utf-8").split("\n") if l.strip()]

    print(f"Loaded {len(shelf_books)} books and {len(tbr_lines)} TBR items.")

    shelf_json_str = json.dumps(shelf_books, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Marginalia — Personal Reading Shelf & Visual Board</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;0,6..72,700;1,6..72,400;1,6..72,600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #0c0e12;
      --surface: #141820;
      --surface-hover: #1b212c;
      --surface-elevated: #1e2430;
      --border: #232834;
      --border-subtle: #1c202a;
      --text-main: #f1f3f7;
      --text-muted: #8b95a5;
      --text-dim: #5c6677;
      --gold: #d4a359;
      --gold-hover: #e5b56d;
      --gold-glow: rgba(212, 163, 89, 0.15);
    }}

    body {{
      background-color: var(--bg);
      color: var(--text-main);
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }}

    .font-serif {{
      font-family: 'Newsreader', Georgia, serif;
    }}

    /* Physical Book Cover Jacket Aesthetics */
    .book-cover {{
      position: relative;
      aspect-ratio: 2 / 3;
      border-radius: 4px 8px 8px 4px;
      overflow: hidden;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45), 0 1px 3px rgba(0, 0, 0, 0.2);
      transition: transform 0.25s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
    }}
    .book-cover::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      bottom: 0;
      width: 14px;
      background: linear-gradient(90deg, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0.02) 40%, rgba(0,0,0,0.3) 100%);
      z-index: 10;
      pointer-events: none;
    }}
    .book-cover::after {{
      content: '';
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      width: 2px;
      background: rgba(0,0,0,0.25);
      z-index: 10;
      pointer-events: none;
    }}
    .book-card:hover .book-cover {{
      transform: translateY(-5px);
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.65), 0 2px 6px rgba(0, 0, 0, 0.3);
    }}

    /* Genre Book Cover Palettes */
    .jacket-fiction {{ background: linear-gradient(145deg, #1e1b4b 0%, #0f0d2c 100%); border-top: 3px solid #818cf8; }}
    .jacket-marketing {{ background: linear-gradient(145deg, #4c0519 0%, #29020d 100%); border-top: 3px solid #fb7185; }}
    .jacket-philosophy {{ background: linear-gradient(145deg, #022c22 0%, #011812 100%); border-top: 3px solid #34d399; }}
    .jacket-cinema {{ background: linear-gradient(145deg, #451a03 0%, #240e02 100%); border-top: 3px solid #fbbf24; }}
    .jacket-screenplay {{ background: linear-gradient(145deg, #18181b 0%, #09090b 100%); border-top: 3px solid #a1a1aa; }}
    .jacket-comics {{ background: linear-gradient(145deg, #3b0764 0%, #200438 100%); border-top: 3px solid #c084fc; }}
    .jacket-guides {{ background: linear-gradient(145deg, #172554 0%, #0b1329 100%); border-top: 3px solid #60a5fa; }}
    .jacket-food {{ background: linear-gradient(145deg, #431407 0%, #220a04 100%); border-top: 3px solid #f97316; }}
    .jacket-hbr {{ background: linear-gradient(145deg, #7f1d1d 0%, #450a0a 100%); border-top: 3px solid #ef4444; }}

    /* Custom Scrollbars */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: var(--bg); }}
    ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: var(--text-dim); }}

    .line-clamp-2 {{ display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
    .line-clamp-3 {{ display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}
    .line-clamp-4 {{ display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden; }}
  </style>
</head>
<body class="min-h-screen">

  <!-- Top Navigation & Global Bar -->
  <header class="sticky top-0 z-40 bg-[var(--bg)]/90 backdrop-blur-md border-b border-[var(--border)] px-4 md:px-8 py-3.5">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <span class="text-2xl">📖</span>
        <div>
          <h1 class="font-serif font-bold text-lg md:text-xl tracking-tight text-[var(--text-main)]">Marginalia Shelf</h1>
          <p class="text-[11px] text-[var(--text-dim)] hidden sm:block">Curated personal library ({len(shelf_books)} volumes)</p>
        </div>
      </div>

      <!-- Center Search -->
      <div class="flex-1 max-w-md mx-2">
        <div class="relative">
          <input 
            type="text" 
            id="searchInput" 
            oninput="handleSearch()"
            placeholder="Search by title, author, themes, or quotes..." 
            class="w-full pl-9 pr-4 py-1.5 bg-[var(--surface)] border border-[var(--border)] rounded-full text-xs text-[var(--text-main)] placeholder-[var(--text-dim)] focus:outline-none focus:border-[var(--gold)] transition"
          />
          <span class="absolute left-3 top-2 text-[var(--text-dim)] text-xs">🔍</span>
        </div>
      </div>

      <!-- Actions & View Switcher -->
      <div class="flex items-center gap-2">
        <!-- View Toggle -->
        <div class="bg-[var(--surface)] p-0.5 rounded-lg border border-[var(--border)] flex items-center text-xs">
          <button 
            id="viewBtnBoard" 
            onclick="switchView('board')" 
            class="px-3 py-1 rounded-md font-medium transition bg-[var(--gold)] text-black shadow-sm flex items-center gap-1.5">
            <span>📌</span>
            <span class="hidden md:inline">Board</span>
          </button>
          <button 
            id="viewBtnSplit" 
            onclick="switchView('split')" 
            class="px-3 py-1 rounded-md font-medium transition text-[var(--text-muted)] hover:text-[var(--text-main)] flex items-center gap-1.5">
            <span>📚</span>
            <span class="hidden md:inline">Bookshelf</span>
          </button>
        </div>

        <!-- Surprise Me -->
        <button 
          onclick="openSurpriseModal()" 
          class="px-3 py-1.5 bg-[var(--gold-glow)] hover:bg-[var(--gold)]/25 text-[var(--gold)] border border-[var(--gold)]/40 rounded-lg text-xs font-semibold transition flex items-center gap-1.5">
          <span>✨</span>
          <span class="hidden sm:inline">Surprise Me</span>
        </button>

        <!-- Copy All TBR -->
        <button 
          onclick="copyAllTbr()" 
          title="Copy clean list for TBR trackers"
          class="px-3 py-1.5 bg-[var(--surface)] hover:bg-[var(--surface-hover)] border border-[var(--border)] text-[var(--text-muted)] hover:text-[var(--text-main)] rounded-lg text-xs font-medium transition flex items-center gap-1.5">
          <span>📋</span>
          <span class="hidden md:inline">Copy TBR ({len(tbr_lines)})</span>
        </button>
      </div>
    </div>
  </header>

  <!-- Category Filter Bar -->
  <div class="border-b border-[var(--border-subtle)] bg-[var(--surface)]/50 px-4 md:px-8 py-2">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-4">
      <div class="flex items-center gap-1.5 overflow-x-auto py-1 no-scrollbar" id="categoryTabs">
        <!-- Populated dynamically -->
      </div>
      <div class="flex items-center gap-3 text-xs text-[var(--text-dim)] shrink-0">
        <label class="flex items-center gap-1.5 cursor-pointer hover:text-[var(--text-muted)]">
          <input type="checkbox" id="filterQuotesOnly" onchange="renderCurrentView()" class="rounded border-[var(--border)] accent-[var(--gold)]" />
          <span>Has Quotes Only</span>
        </label>
        <span id="filteredCountBadge" class="font-mono text-[11px] px-2 py-0.5 bg-[var(--border-subtle)] rounded text-[var(--text-muted)]">
          {len(shelf_books)}
        </span>
      </div>
    </div>
  </div>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto p-4 md:p-8">

    <!-- 1. Pinterest Board View (Default) -->
    <div id="boardView" class="block">
      <div id="boardGrid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-6 md:gap-7">
        <!-- Rendered dynamically -->
      </div>
    </div>

    <!-- 2. Bookshelf Split View (Toggleable) -->
    <div id="splitView" class="hidden">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        <!-- Left Pane: Book List (5 columns) -->
        <div class="lg:col-span-5 bg-[var(--surface)] border border-[var(--border)] rounded-2xl p-4 max-h-[82vh] overflow-y-auto">
          <div class="text-xs font-semibold text-[var(--text-dim)] uppercase tracking-wider mb-3 px-2">Library Stream</div>
          <div id="splitList" class="space-y-2">
            <!-- Populated dynamically -->
          </div>
        </div>

        <!-- Right Pane: Reading Dossier (7 columns) -->
        <div class="lg:col-span-7 sticky top-24">
          <div id="splitDossier" class="bg-[var(--surface)] border border-[var(--border)] rounded-2xl p-6 md:p-8 shadow-xl">
            <!-- Populated dynamically with selected book -->
          </div>
        </div>
      </div>
    </div>

  </main>

  <!-- Slide-Out Drawer for Board View Inspector -->
  <div id="drawerOverlay" class="fixed inset-0 bg-black/75 backdrop-blur-sm z-50 flex justify-end hidden">
    <div id="drawerPanel" class="w-full max-w-xl bg-[var(--surface)] border-l border-[var(--border)] h-full overflow-y-auto p-6 md:p-8 shadow-2xl transition-transform transform translate-x-full">
      <div class="flex items-center justify-between pb-4 border-b border-[var(--border)] mb-6">
        <span class="text-xs font-bold uppercase tracking-widest text-[var(--gold)]">Book Dossier</span>
        <button onclick="closeDrawer()" class="text-[var(--text-muted)] hover:text-white text-xl font-bold p-1">✕</button>
      </div>
      <div id="drawerContent">
        <!-- Populated dynamically -->
      </div>
    </div>
  </div>

  <!-- Surprise Me / Joy of Reading Modal -->
  <div id="surpriseModal" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-[var(--surface)] border border-[var(--border)] rounded-2xl max-w-xl w-full p-6 md:p-8 shadow-2xl relative overflow-hidden">
      <div class="absolute -top-12 -right-12 w-48 h-48 bg-[var(--gold)]/10 rounded-full blur-3xl pointer-events-none"></div>

      <div class="flex items-center justify-between pb-4 border-b border-[var(--border)] mb-6">
        <div class="flex items-center gap-2.5">
          <span class="text-2xl">✨</span>
          <h2 class="font-serif font-bold text-xl text-[var(--text-main)]">What to Read Next</h2>
        </div>
        <button onclick="closeSurpriseModal()" class="text-[var(--text-muted)] hover:text-white text-lg font-bold">✕</button>
      </div>

      <p class="text-xs text-[var(--text-muted)] mb-5">
        Handpicked strictly from high-conviction fiction, craft essays by novelists, and engaging philosophy. Zero chores or dry textbooks.
      </p>

      <!-- Surprise Pick Result Card -->
      <div id="surpriseResult" class="mb-6">
        <!-- dynamically populated -->
      </div>

      <div class="flex items-center justify-between pt-4 border-t border-[var(--border)]">
        <button onclick="spinSurprise()" class="px-5 py-2.5 bg-[var(--gold)] hover:bg-[var(--gold-hover)] text-black text-xs font-bold rounded-xl shadow-md transition flex items-center gap-2">
          <span>🎲</span>
          <span>Spin Again</span>
        </button>
        <button onclick="copySingleTbr(currentSurpriseBook.title, currentSurpriseBook.author)" class="px-4 py-2 bg-[var(--surface-hover)] border border-[var(--border)] rounded-xl text-xs font-medium text-[var(--text-main)] hover:border-[var(--gold)]">
          Copy Title & Author
        </button>
      </div>
    </div>
  </div>

  <!-- Rename & Cover URL Modal -->
  <div id="editModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-[var(--surface)] border border-[var(--border)] rounded-2xl max-w-lg w-full p-6 shadow-2xl">
      <div class="flex items-center justify-between pb-3 border-b border-[var(--border)] mb-4">
        <h3 class="font-serif font-bold text-lg text-[var(--text-main)]">Edit Book Details & Cover</h3>
        <button onclick="closeEditModal()" class="text-[var(--text-dim)] hover:text-white font-bold">✕</button>
      </div>

      <input type="hidden" id="editBookId" />

      <div class="space-y-4 text-xs">
        <div>
          <label class="block font-semibold text-[var(--text-muted)] uppercase mb-1">Title</label>
          <input type="text" id="editTitle" class="w-full px-3 py-2 bg-[var(--bg)] border border-[var(--border)] rounded-lg text-[var(--text-main)] focus:border-[var(--gold)] focus:outline-none" />
        </div>
        <div>
          <label class="block font-semibold text-[var(--text-muted)] uppercase mb-1">Author</label>
          <input type="text" id="editAuthor" class="w-full px-3 py-2 bg-[var(--bg)] border border-[var(--border)] rounded-lg text-[var(--text-main)] focus:border-[var(--gold)] focus:outline-none" />
        </div>
        <div>
          <label class="block font-semibold text-[var(--text-muted)] uppercase mb-1">Cover Image URL</label>
          <input type="text" id="editCoverUrl" placeholder="https://..." class="w-full px-3 py-2 bg-[var(--bg)] border border-[var(--border)] rounded-lg text-[var(--text-main)] focus:border-[var(--gold)] focus:outline-none" />
          <div class="flex items-center gap-3 mt-1.5 text-[11px] text-[var(--gold)]">
            <button type="button" onclick="searchGoodreads()" class="hover:underline">🔎 Search Goodreads Cover</button>
            <button type="button" onclick="searchGoogleImages()" class="hover:underline">🖼️ Search Google Images</button>
          </div>
        </div>
        <div>
          <label class="block font-semibold text-[var(--text-muted)] uppercase mb-1">Back-Cover Pitch</label>
          <textarea id="editPitch" rows="3" class="w-full px-3 py-2 bg-[var(--bg)] border border-[var(--border)] rounded-lg text-[var(--text-main)] focus:border-[var(--gold)] focus:outline-none"></textarea>
        </div>
        <div>
          <label class="block font-semibold text-[var(--text-muted)] uppercase mb-1">Why Read It</label>
          <textarea id="editWhyLove" rows="2" class="w-full px-3 py-2 bg-[var(--bg)] border border-[var(--border)] rounded-lg text-[var(--text-main)] focus:border-[var(--gold)] focus:outline-none"></textarea>
        </div>
      </div>

      <div class="flex items-center justify-end gap-3 mt-5 pt-3 border-t border-[var(--border)]">
        <button onclick="closeEditModal()" class="px-4 py-2 border border-[var(--border)] rounded-lg text-xs text-[var(--text-muted)]">Cancel</button>
        <button onclick="saveEdit()" class="px-5 py-2 bg-[var(--gold)] text-black text-xs font-bold rounded-lg shadow">Save Changes</button>
      </div>
    </div>
  </div>

  <!-- Toast -->
  <div id="toast" class="fixed bottom-6 right-6 bg-[var(--text-main)] text-[var(--bg)] px-4 py-2.5 rounded-lg shadow-2xl text-xs font-semibold transform translate-y-16 opacity-0 transition-all pointer-events-none z-50">
    Copied to clipboard!
  </div>

  <script>
    let SHELF_DATA = {shelf_json_str};
    let activeCategory = "All";
    let activeView = "board"; // 'board' or 'split'
    let selectedBookId = SHELF_DATA[0] ? SHELF_DATA[0].id : null;
    let currentSurpriseBook = null;

    // Load any user overrides from localStorage
    try {{
      const saved = localStorage.getItem("marginalia_shelf_edits");
      if (saved) {{
        const overrides = JSON.parse(saved);
        SHELF_DATA = SHELF_DATA.map(b => overrides[b.id] ? Object.assign(b, overrides[b.id]) : b);
      }}
    }} catch (e) {{}}

    const CATEGORIES = [
      "All",
      "Fiction & Non-Fiction",
      "Cinema & Film Craft",
      "Screenplays",
      "Philosophy, Essays & Misc",
      "Comics & Graphic Novels",
      "Graphic Guides",
      "Marketing & Strategy",
      "Harvard Business Review"
    ];

    function showToast(msg) {{
      const t = document.getElementById("toast");
      t.innerText = msg;
      t.classList.remove("translate-y-16", "opacity-0");
      setTimeout(() => t.classList.add("translate-y-16", "opacity-0"), 2400);
    }}

    function copyToClipboard(text, msg) {{
      navigator.clipboard.writeText(text).then(() => showToast(msg || "Copied to clipboard!"));
    }}

    function copySingleTbr(title, author) {{
      copyToClipboard(`${{title}} — ${{author}}`, `Copied: "${{title}} — ${{author}}"`);
    }}

    function copyAllTbr() {{
      const filtered = getFilteredBooks();
      const lines = filtered.map(b => `${{b.title}} — ${{b.author}}`);
      copyToClipboard(lines.join("\\n"), `Copied ${{lines.length}} books to clipboard!`);
    }}

    function getJacketStyle(cat) {{
      if (cat.includes("Fiction")) return "jacket-fiction";
      if (cat.includes("Marketing")) return "jacket-marketing";
      if (cat.includes("Philosophy")) return "jacket-philosophy";
      if (cat.includes("Cinema")) return "jacket-cinema";
      if (cat.includes("Screenplay")) return "jacket-screenplay";
      if (cat.includes("Comics")) return "jacket-comics";
      if (cat.includes("Graphic Guide")) return "jacket-guides";
      if (cat.includes("Harvard")) return "jacket-hbr";
      if (cat.includes("Food")) return "jacket-food";
      return "jacket-fiction";
    }}

    function getFilteredBooks() {{
      const q = document.getElementById("searchInput").value.toLowerCase().trim();
      const quotesOnly = document.getElementById("filterQuotesOnly").checked;

      return SHELF_DATA.filter(b => {{
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
    }}

    function renderCategoryTabs() {{
      const container = document.getElementById("categoryTabs");
      container.innerHTML = CATEGORIES.map(cat => {{
        const isAct = cat === activeCategory;
        const count = cat === "All" ? SHELF_DATA.length : SHELF_DATA.filter(b => b.category === cat).length;
        if (count === 0) return "";
        return `
          <button 
            onclick="setCategory('${{cat}}')" 
            class="px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap transition ${{
              isAct 
                ? 'bg-[var(--gold)] text-black font-semibold' 
                : 'text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--surface-hover)]'
            }}">
            ${{cat}} <span class="opacity-70 text-[10px]">(${{count}})</span>
          </button>
        `;
      }}).join("");
    }}

    function setCategory(cat) {{
      activeCategory = cat;
      renderCategoryTabs();
      renderCurrentView();
    }}

    function handleSearch() {{
      renderCurrentView();
    }}

    function switchView(view) {{
      activeView = view;
      const board = document.getElementById("boardView");
      const split = document.getElementById("splitView");
      const btnBoard = document.getElementById("viewBtnBoard");
      const btnSplit = document.getElementById("viewBtnSplit");

      if (view === "board") {{
        board.classList.remove("hidden");
        split.classList.add("hidden");
        btnBoard.className = "px-3 py-1 rounded-md font-medium transition bg-[var(--gold)] text-black shadow-sm flex items-center gap-1.5";
        btnSplit.className = "px-3 py-1 rounded-md font-medium transition text-[var(--text-muted)] hover:text-[var(--text-main)] flex items-center gap-1.5";
      }} else {{
        board.classList.add("hidden");
        split.classList.remove("hidden");
        btnSplit.className = "px-3 py-1 rounded-md font-medium transition bg-[var(--gold)] text-black shadow-sm flex items-center gap-1.5";
        btnBoard.className = "px-3 py-1 rounded-md font-medium transition text-[var(--text-muted)] hover:text-[var(--text-main)] flex items-center gap-1.5";
      }}
      renderCurrentView();
    }}

    function renderCurrentView() {{
      const filtered = getFilteredBooks();
      document.getElementById("filteredCountBadge").innerText = `${{filtered.length}} books`;

      if (activeView === "board") {{
        renderBoard(filtered);
      }} else {{
        renderSplit(filtered);
      }}
    }}

    // Render Pinterest Board
    function renderBoard(books) {{
      const grid = document.getElementById("boardGrid");
      if (books.length === 0) {{
        grid.innerHTML = `<div class="col-span-full py-20 text-center text-[var(--text-dim)]">No books match your search.</div>`;
        return;
      }}

      grid.innerHTML = books.map(b => {{
        const jacketCls = getJacketStyle(b.category);
        const hasCover = !!b.cover_url;

        return `
          <div class="book-card group cursor-pointer" onclick="openBookDetail('${{b.id}}')">
            <!-- Cover Container -->
            <div class="book-cover ${{jacketCls}} flex flex-col justify-between p-3.5 relative">
              ${{hasCover ? `
                <img src="${{b.cover_url}}" alt="${{b.title}}" class="absolute inset-0 w-full h-full object-cover z-0" onerror="this.style.display='none'" />
                <div class="absolute inset-0 bg-gradient-to-t from-black/85 via-black/30 to-transparent z-0"></div>
              ` : ''}}
              
              <!-- Top Pill -->
              <div class="relative z-10 flex items-center justify-between">
                <span class="text-[9px] font-mono uppercase tracking-wider text-white/80 bg-black/40 px-1.5 py-0.5 rounded">
                  ${{b.format}}
                </span>
                ${{b.has_quote_bank ? `<span class="text-[10px] text-[var(--gold)]">★</span>` : ''}}
              </div>

              <!-- Center/Bottom Typographic Jacket (Fallback or Overlay) -->
              <div class="relative z-10 mt-auto pt-2">
                <h3 class="font-serif font-bold text-xs sm:text-sm text-white leading-tight tracking-tight drop-shadow-md line-clamp-3">
                  ${{b.title}}
                </h3>
                <p class="text-[11px] text-white/80 font-medium mt-0.5 line-clamp-1">
                  ${{b.author}}
                </p>
              </div>
            </div>

            <!-- Meta Underneath -->
            <div class="pt-2">
              <h4 class="font-serif font-bold text-xs text-[var(--text-main)] group-hover:text-[var(--gold)] transition leading-snug line-clamp-1">
                ${{b.title}}
              </h4>
              <p class="text-[11px] text-[var(--text-dim)] line-clamp-1">
                ${{b.author}}
              </p>
            </div>
          </div>
        `;
      }}).join("");
    }}

    // Render Bookshelf Split View
    function renderSplit(books) {{
      const list = document.getElementById("splitList");
      if (books.length === 0) {{
        list.innerHTML = `<div class="p-6 text-center text-xs text-[var(--text-dim)]">No books match.</div>`;
        document.getElementById("splitDossier").innerHTML = `<div class="p-8 text-center text-xs text-[var(--text-dim)]">Select a book from the list.</div>`;
        return;
      }}

      // Ensure active selected book exists in filtered
      if (!books.some(b => b.id === selectedBookId)) {{
        selectedBookId = books[0].id;
      }}

      list.innerHTML = books.map(b => {{
        const isSel = b.id === selectedBookId;
        const jacketCls = getJacketStyle(b.category);

        return `
          <div 
            onclick="selectBookForSplit('${{b.id}}')" 
            class="flex items-center gap-3 p-2.5 rounded-xl cursor-pointer transition ${{
              isSel 
                ? 'bg-[var(--surface-elevated)] border border-[var(--gold)]/50 shadow-sm' 
                : 'hover:bg-[var(--surface-hover)] border border-transparent'
            }}">
            <div class="w-10 h-14 shrink-0 book-cover ${{jacketCls}} relative overflow-hidden rounded">
              ${{b.cover_url ? `<img src="${{b.cover_url}}" class="w-full h-full object-cover" onerror="this.style.display='none'" />` : ''}}
            </div>
            <div class="flex-1 min-w-0">
              <h4 class="font-serif font-bold text-xs text-[var(--text-main)] truncate">${{b.title}}</h4>
              <p class="text-[11px] text-[var(--text-dim)] truncate">${{b.author}}</p>
              <div class="flex items-center gap-2 mt-1 text-[10px]">
                <span class="text-[var(--gold)] font-medium">${{b.category}}</span>
                ${{b.has_quote_bank ? `<span class="text-[var(--text-dim)]">• ${{b.quotes.length}} Quotes</span>` : ''}}
              </div>
            </div>
          </div>
        `;
      }}).join("");

      renderDossier(books.find(b => b.id === selectedBookId));
    }}

    function selectBookForSplit(bookId) {{
      selectedBookId = bookId;
      const filtered = getFilteredBooks();
      renderSplit(filtered);
    }}

    function renderDossier(b) {{
      const container = document.getElementById("splitDossier");
      if (!b) return;

      const jacketCls = getJacketStyle(b.category);
      const quotes = b.quotes || [];

      container.innerHTML = `
        <div class="flex flex-col md:flex-row gap-6 items-start mb-6 pb-6 border-b border-[var(--border)]">
          <!-- Hero Cover -->
          <div class="w-36 md:w-44 shrink-0 book-cover ${{jacketCls}} p-4 flex flex-col justify-between shadow-2xl relative">
            ${{b.cover_url ? `
              <img src="${{b.cover_url}}" alt="${{b.title}}" class="absolute inset-0 w-full h-full object-cover" onerror="this.style.display='none'" />
              <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent"></div>
            ` : ''}}
            <span class="relative z-10 text-[10px] font-mono text-white/80 uppercase">${{b.format}}</span>
            <div class="relative z-10">
              <h3 class="font-serif font-bold text-sm text-white leading-tight">${{b.title}}</h3>
              <p class="text-xs text-white/80 mt-0.5">${{b.author}}</p>
            </div>
          </div>

          <!-- Title & Actions -->
          <div class="flex-1 min-w-0">
            <span class="text-xs font-semibold uppercase tracking-wider text-[var(--gold)]">${{b.category}}</span>
            <h2 class="font-serif font-bold text-2xl md:text-3xl text-[var(--text-main)] mt-1 tracking-tight leading-tight">
              ${{b.title}}
            </h2>
            <p class="text-sm font-medium text-[var(--text-muted)] mt-1">by ${{b.author}}</p>

            <div class="flex flex-wrap items-center gap-2 mt-4">
              <button onclick="copySingleTbr('${{b.title.replace(/'/g, "\\\\\\'")}}', '${{b.author.replace(/'/g, "\\\\\\'")}}')" class="px-3.5 py-1.5 bg-[var(--gold)] text-black text-xs font-bold rounded-lg shadow-sm hover:bg-[var(--gold-hover)] transition flex items-center gap-1.5">
                <span>📋</span>
                <span>Copy to TBR</span>
              </button>
              <button onclick="openEditModal('${{b.id}}')" class="px-3 py-1.5 bg-[var(--surface-hover)] border border-[var(--border)] text-xs font-medium text-[var(--text-main)] rounded-lg hover:border-[var(--gold)] transition flex items-center gap-1.5">
                <span>✏️</span>
                <span>Rename / Cover</span>
              </button>
            </div>
          </div>
        </div>

        <!-- The Pitch -->
        <div class="mb-5">
          <h4 class="text-xs font-bold uppercase tracking-wider text-[var(--text-dim)] mb-2">The Pitch</h4>
          <p class="font-serif text-sm md:text-base text-[var(--text-main)] leading-relaxed">
            ${{b.pitch}}
          </p>
        </div>

        <!-- Why People Love It -->
        <div class="mb-6 p-4 bg-[var(--surface-hover)]/70 border border-[var(--border)] rounded-xl">
          <h4 class="text-xs font-bold text-[var(--gold)] uppercase tracking-wider mb-1">Why You Should Read It</h4>
          <p class="text-xs md:text-sm text-[var(--text-muted)] leading-relaxed">
            ${{b.why_love}}
          </p>
        </div>

        <!-- Excerpt Quotes & Notes from Marginalia -->
        ${{quotes.length > 0 ? `
          <div>
            <h4 class="text-xs font-bold uppercase tracking-wider text-[var(--text-dim)] mb-3 flex items-center gap-2">
              <span>★ Notable Passages from Quote Bank (${{quotes.length}})</span>
            </h4>
            <div class="space-y-4">
              ${{quotes.map(q => `
                <div class="p-4 bg-[var(--bg)] border border-[var(--border)] rounded-xl">
                  <div class="font-serif italic text-sm text-[var(--text-main)] leading-relaxed pl-3 border-l-2 border-[var(--gold)] mb-2.5">
                    “${{q.quote}}”
                  </div>
                  ${{q.explanation ? `
                    <div class="text-xs text-[var(--text-dim)] pt-2 border-t border-[var(--border-subtle)] leading-relaxed whitespace-pre-line">
                      <span class="text-[var(--text-muted)] font-semibold block mb-0.5">Scene & Companion Insight:</span>
                      ${{q.explanation}}
                    </div>
                  ` : ''}}
                </div>
              `).join("")}}
            </div>
          </div>
        ` : ''}}
      `;
    }}

    function openBookDetail(bookId) {{
      const b = SHELF_DATA.find(item => item.id === bookId);
      if (!b) return;

      if (window.innerWidth >= 1024) {{
        // Switch to split view and highlight
        switchView("split");
        selectBookForSplit(bookId);
      }} else {{
        // Open Slide-Out Drawer
        openDrawer(b);
      }}
    }}

    function openDrawer(b) {{
      const overlay = document.getElementById("drawerOverlay");
      const panel = document.getElementById("drawerPanel");
      const content = document.getElementById("drawerContent");
      const jacketCls = getJacketStyle(b.category);
      const quotes = b.quotes || [];

      content.innerHTML = `
        <div class="flex gap-4 items-start mb-6">
          <div class="w-28 shrink-0 book-cover ${{jacketCls}} p-2 relative shadow-lg">
            ${{b.cover_url ? `<img src="${{b.cover_url}}" class="absolute inset-0 w-full h-full object-cover" onerror="this.style.display='none'" />` : ''}}
            <span class="relative z-10 text-[9px] font-mono uppercase text-white/80">${{b.format}}</span>
          </div>
          <div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--gold)]">${{b.category}}</span>
            <h3 class="font-serif font-bold text-lg text-white mt-0.5 leading-snug">${{b.title}}</h3>
            <p class="text-xs text-[var(--text-muted)]">${{b.author}}</p>
            <div class="flex items-center gap-2 mt-3">
              <button onclick="copySingleTbr('${{b.title.replace(/'/g, "\\\\\\'")}}', '${{b.author.replace(/'/g, "\\\\\\'")}}')" class="px-3 py-1 bg-[var(--gold)] text-black text-xs font-bold rounded-lg">Copy TBR</button>
              <button onclick="openEditModal('${{b.id}}')" class="px-3 py-1 bg-[var(--surface-hover)] border border-[var(--border)] text-xs text-white rounded-lg">Edit</button>
            </div>
          </div>
        </div>

        <div class="mb-5">
          <h4 class="text-xs font-bold uppercase tracking-wider text-[var(--text-dim)] mb-1">The Pitch</h4>
          <p class="font-serif text-sm text-[var(--text-main)] leading-relaxed">${{b.pitch}}</p>
        </div>

        <div class="mb-5 p-3.5 bg-[var(--surface-hover)] rounded-xl border border-[var(--border)]">
          <h4 class="text-xs font-bold text-[var(--gold)] uppercase mb-1">Why Read It</h4>
          <p class="text-xs text-[var(--text-muted)] leading-relaxed">${{b.why_love}}</p>
        </div>

        ${{quotes.length > 0 ? `
          <div class="space-y-3">
            <h4 class="text-xs font-bold uppercase tracking-wider text-[var(--text-dim)]">Notable Passages</h4>
            ${{quotes.map(q => `
              <div class="p-3 bg-[var(--bg)] border border-[var(--border)] rounded-lg">
                <div class="font-serif italic text-xs text-white leading-relaxed mb-2 pl-2 border-l border-[var(--gold)]">“${{q.quote}}”</div>
                <div class="text-[11px] text-[var(--text-dim)] leading-relaxed whitespace-pre-line">${{q.explanation || ''}}</div>
              </div>
            `).join("")}}
          </div>
        ` : ''}}
      `;

      overlay.classList.remove("hidden");
      setTimeout(() => panel.classList.remove("translate-x-full"), 10);
    }}

    function closeDrawer() {{
      const overlay = document.getElementById("drawerOverlay");
      const panel = document.getElementById("drawerPanel");
      panel.classList.add("translate-x-full");
      setTimeout(() => overlay.classList.add("hidden"), 250);
    }}

    // Surprise Me Logic (Strictly Joy-of-Reading Pool)
    function openSurpriseModal() {{
      spinSurprise();
      document.getElementById("surpriseModal").classList.remove("hidden");
    }}

    function closeSurpriseModal() {{
      document.getElementById("surpriseModal").classList.add("hidden");
    }}

    function spinSurprise() {{
      // Filter exclusively to is_fun_pick
      const pool = SHELF_DATA.filter(b => b.is_fun_pick);
      const chosen = pool[Math.floor(Math.random() * pool.length)];
      currentSurpriseBook = chosen;

      const res = document.getElementById("surpriseResult");
      const jacketCls = getJacketStyle(chosen.category);

      res.innerHTML = `
        <div class="flex gap-5 items-start p-4 bg-[var(--surface-hover)] border border-[var(--border)] rounded-xl">
          <div class="w-24 md:w-28 shrink-0 book-cover ${{jacketCls}} p-2 relative shadow-lg">
            ${{chosen.cover_url ? `<img src="${{chosen.cover_url}}" class="absolute inset-0 w-full h-full object-cover" onerror="this.style.display='none'" />` : ''}}
            <span class="relative z-10 text-[9px] font-mono uppercase text-white/80">${{chosen.format}}</span>
          </div>
          <div class="flex-1 min-w-0">
            <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--gold)]">${{chosen.category}}</span>
            <h3 class="font-serif font-bold text-lg md:text-xl text-[var(--text-main)] mt-0.5 leading-snug">${{chosen.title}}</h3>
            <p class="text-xs text-[var(--text-muted)] font-medium">by ${{chosen.author}}</p>
            <div class="mt-3 text-xs text-[var(--text-main)] font-serif leading-relaxed line-clamp-3">
              ${{chosen.pitch}}
            </div>
            <div class="mt-2.5 text-[11px] text-[var(--gold)] font-medium">
              💡 ${{chosen.why_love}}
            </div>
          </div>
        </div>
      `;
    }}

    // Rename & Custom Cover Modal
    function openEditModal(bookId) {{
      const b = SHELF_DATA.find(item => item.id === bookId);
      if (!b) return;

      document.getElementById("editBookId").value = b.id;
      document.getElementById("editTitle").value = b.title;
      document.getElementById("editAuthor").value = b.author;
      document.getElementById("editCoverUrl").value = b.cover_url || "";
      document.getElementById("editPitch").value = b.pitch || "";
      document.getElementById("editWhyLove").value = b.why_love || "";

      document.getElementById("editModal").classList.remove("hidden");
    }}

    function closeEditModal() {{
      document.getElementById("editModal").classList.add("hidden");
    }}

    function saveEdit() {{
      const bookId = document.getElementById("editBookId").value;
      const b = SHELF_DATA.find(item => item.id === bookId);
      if (!b) return;

      b.title = document.getElementById("editTitle").value.trim();
      b.author = document.getElementById("editAuthor").value.trim();
      b.cover_url = document.getElementById("editCoverUrl").value.trim();
      b.pitch = document.getElementById("editPitch").value.trim();
      b.why_love = document.getElementById("editWhyLove").value.trim();

      // Persist to localStorage
      let saved = {{}};
      try {{ saved = JSON.parse(localStorage.getItem("marginalia_shelf_edits") || "{{}}"); }} catch (e) {{}}
      saved[b.id] = {{
        title: b.title,
        author: b.author,
        cover_url: b.cover_url,
        pitch: b.pitch,
        why_love: b.why_love
      }};
      localStorage.setItem("marginalia_shelf_edits", JSON.stringify(saved));

      closeEditModal();
      renderCurrentView();
      showToast(`Updated "${{b.title}}" and saved changes!`);
    }}

    function searchGoodreads() {{
      const t = document.getElementById("editTitle").value.trim();
      const a = document.getElementById("editAuthor").value.trim();
      window.open(`https://www.goodreads.com/search?q=${{encodeURIComponent(t + ' ' + a)}}`, '_blank');
    }}

    function searchGoogleImages() {{
      const t = document.getElementById("editTitle").value.trim();
      const a = document.getElementById("editAuthor").value.trim();
      window.open(`https://www.google.com/search?tbm=isch&q=${{encodeURIComponent(t + ' ' + a + ' book cover')}}`, '_blank');
    }}

    // Initial load
    renderCategoryTabs();
    renderCurrentView();
  </script>
</body>
</html>
"""
    SHELF_HTML_PROTO.parent.mkdir(exist_ok=True)
    SHELF_HTML_PROTO.write_text(html, encoding="utf-8")
    SHELF_HTML_DOCS.parent.mkdir(exist_ok=True)
    SHELF_HTML_DOCS.write_text(html, encoding="utf-8")
    ARTIFACT_PATH.parent.mkdir(exist_ok=True)
    ARTIFACT_PATH.write_text(html, encoding="utf-8")
    print(f"Generated prototype page: {SHELF_HTML_PROTO}")
    print(f"Generated docs page: {SHELF_HTML_DOCS}")
    print(f"Generated artifact page: {ARTIFACT_PATH}")

if __name__ == "__main__":
    build_app()
