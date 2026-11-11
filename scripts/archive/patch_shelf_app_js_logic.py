# scripts/patch_shelf_app_js_logic.py — Updates JS logic in build_independent_bookshelf_app.py for mobile search sync, view switcher, and bottom sheet
# Usage: python3 scripts/patch_shelf_app_js_logic.py
# Requires: Python 3.8+ (standard library only)

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET_SCRIPT = ROOT / "scripts" / "build_independent_bookshelf_app.py"

def patch_js():
    print(f"Patching JS logic in {TARGET_SCRIPT}...")
    content = TARGET_SCRIPT.read_text(encoding="utf-8")

    # 1. Update toggleDarkMode
    old_dark_mode = """    function toggleDarkMode() {{
      isDark = !isDark;
      document.body.classList.toggle("dark-mode", isDark);
      document.getElementById("themeIcon").innerText = isDark ? "☀️" : "🌙";
    }}"""

    new_dark_mode = """    function toggleDarkMode() {{
      isDark = !isDark;
      document.body.classList.toggle("dark-mode", isDark);
      const icon = isDark ? "☀️" : "🌙";
      const dIcon = document.getElementById("themeIcon");
      const mIcon = document.getElementById("mobileThemeIcon");
      if (dIcon) dIcon.innerText = icon;
      if (mIcon) mIcon.innerText = icon;
    }}"""

    if old_dark_mode in content:
        content = content.replace(old_dark_mode, new_dark_mode, 1)
        print("  ✓ Updated toggleDarkMode for dual desktop/mobile icon sync")
    else:
        print("  ⚠ Could not find exact old_dark_mode")

    # 2. Update getFilteredBooks for dual input search query
    old_filtered = """    function getFilteredBooks() {{
      const q = document.getElementById("searchInput").value.toLowerCase().trim();"""

    new_filtered = """    function getFilteredBooks() {{
      const dInput = document.getElementById("searchInput");
      const mInput = document.getElementById("mobileSearchInput");
      const q = ((dInput ? dInput.value : "") || (mInput ? mInput.value : "")).toLowerCase().trim();"""

    if old_filtered in content:
        content = content.replace(old_filtered, new_filtered, 1)
        print("  ✓ Updated getFilteredBooks for dual search input sync")
    else:
        print("  ⚠ Could not find exact old_filtered")

    # 3. Update handleSearch and switchView
    old_search_and_switch = """    function handleSearch() {{
      renderCurrentView();
    }}

    function switchView(view) {{
      activeView = view;
      const board = document.getElementById("boardView");
      const editorial = document.getElementById("editorialView");
      const split = document.getElementById("splitView");
      const btnBoard = document.getElementById("viewBtnBoard");
      const btnEditorial = document.getElementById("viewBtnEditorial");
      const btnSplit = document.getElementById("viewBtnSplit");

      [board, editorial, split].forEach(el => el.classList.add("hidden"));
      [btnBoard, btnEditorial, btnSplit].forEach(btn => {{
        btn.className = "px-3 py-1 rounded-lg font-medium transition text-[var(--text-muted)] hover:text-[var(--text-heading)] flex items-center gap-1.5";
      }});

      if (view === "board") {{
        board.classList.remove("hidden");
        btnBoard.className = "px-3 py-1 rounded-lg font-semibold transition bg-[var(--terracotta)] text-white shadow-sm flex items-center gap-1.5";
      }} else if (view === "editorial") {{
        editorial.classList.remove("hidden");
        btnEditorial.className = "px-3 py-1 rounded-lg font-semibold transition bg-[var(--terracotta)] text-white shadow-sm flex items-center gap-1.5";
      }} else {{
        split.classList.remove("hidden");
        btnSplit.className = "px-3 py-1 rounded-lg font-semibold transition bg-[var(--terracotta)] text-white shadow-sm flex items-center gap-1.5";
      }}
      renderCurrentView();
    }}"""

    new_search_and_switch = """    function handleSearch(val) {{
      const dInput = document.getElementById("searchInput");
      const mInput = document.getElementById("mobileSearchInput");
      const clearBtn = document.getElementById("mobileSearchClearBtn");
      const query = (val !== undefined ? val : (dInput?.value || mInput?.value || "")).trim();

      if (dInput && dInput.value !== query) dInput.value = query;
      if (mInput && mInput.value !== query) mInput.value = query;
      if (clearBtn) clearBtn.classList.toggle("hidden", !query);

      renderCurrentView();
    }}

    function clearSearchInput() {{
      handleSearch("");
    }}

    function switchView(view) {{
      activeView = view;
      const board = document.getElementById("boardView");
      const editorial = document.getElementById("editorialView");
      const split = document.getElementById("splitView");
      const btnBoard = document.getElementById("viewBtnBoard");
      const btnEditorial = document.getElementById("viewBtnEditorial");
      const btnSplit = document.getElementById("viewBtnSplit");
      const mBtnBoard = document.getElementById("mobileViewBtnBoard");
      const mBtnEditorial = document.getElementById("mobileViewBtnEditorial");
      const mBtnSplit = document.getElementById("mobileViewBtnSplit");

      [board, editorial, split].forEach(el => el.classList.add("hidden"));
      [btnBoard, btnEditorial, btnSplit].forEach(btn => {{
        if (btn) btn.className = "px-3 py-1 rounded-lg font-medium transition text-[var(--text-muted)] hover:text-[var(--text-heading)] flex items-center gap-1.5";
      }});
      [mBtnBoard, mBtnEditorial, mBtnSplit].forEach(btn => {{
        if (btn) btn.className = "flex-1 py-1.5 rounded-lg font-medium transition text-[var(--text-muted)] hover:text-[var(--text-heading)] flex items-center justify-center gap-1 min-h-[38px]";
      }});

      if (view === "board") {{
        board.classList.remove("hidden");
        if (btnBoard) btnBoard.className = "px-3 py-1 rounded-lg font-semibold transition bg-[var(--terracotta)] text-white shadow-sm flex items-center gap-1.5";
        if (mBtnBoard) mBtnBoard.className = "flex-1 py-1.5 rounded-lg font-semibold transition bg-[var(--terracotta)] text-white shadow-xs flex items-center justify-center gap-1 min-h-[38px]";
      }} else if (view === "editorial") {{
        editorial.classList.remove("hidden");
        if (btnEditorial) btnEditorial.className = "px-3 py-1 rounded-lg font-semibold transition bg-[var(--terracotta)] text-white shadow-sm flex items-center gap-1.5";
        if (mBtnEditorial) mBtnEditorial.className = "flex-1 py-1.5 rounded-lg font-semibold transition bg-[var(--terracotta)] text-white shadow-xs flex items-center justify-center gap-1 min-h-[38px]";
      }} else {{
        split.classList.remove("hidden");
        if (btnSplit) btnSplit.className = "px-3 py-1 rounded-lg font-semibold transition bg-[var(--terracotta)] text-white shadow-sm flex items-center gap-1.5";
        if (mBtnSplit) mBtnSplit.className = "flex-1 py-1.5 rounded-lg font-semibold transition bg-[var(--terracotta)] text-white shadow-xs flex items-center justify-center gap-1 min-h-[38px]";
      }}
      renderCurrentView();
    }}"""

    if old_search_and_switch in content:
        content = content.replace(old_search_and_switch, new_search_and_switch, 1)
        print("  ✓ Updated handleSearch & switchView for desktop/mobile synchronization")
    else:
        print("  ⚠ Could not find exact old_search_and_switch")

    # 4. Update openDrawer / closeDrawer for Bottom Sheet
    old_drawer_funcs = """      overlay.classList.remove("hidden");
      setTimeout(() => panel.classList.remove("translate-x-full"), 10);
    }}

    function closeDrawer() {{
      const overlay = document.getElementById("drawerOverlay");
      const panel = document.getElementById("drawerPanel");
      panel.classList.add("translate-x-full");
      setTimeout(() => overlay.classList.add("hidden"), 240);
    }}"""

    new_drawer_funcs = """      overlay.classList.remove("hidden");
      setTimeout(() => {{
        if (window.innerWidth < 640) {{
          panel.classList.remove("translate-y-full");
        }} else {{
          panel.classList.remove("sm:translate-x-full");
        }}
      }}, 10);
    }}

    function closeDrawer() {{
      const overlay = document.getElementById("drawerOverlay");
      const panel = document.getElementById("drawerPanel");
      if (window.innerWidth < 640) {{
        panel.classList.add("translate-y-full");
      }} else {{
        panel.classList.add("sm:translate-x-full");
      }}
      setTimeout(() => overlay.classList.add("hidden"), 240);
    }}

    function handleDrawerOverlayClick(e) {{
      if (e.target.id === "drawerOverlay") {{
        closeDrawer();
      }}
    }}"""

    if old_drawer_funcs in content:
        content = content.replace(old_drawer_funcs, new_drawer_funcs, 1)
        print("  ✓ Updated openDrawer & closeDrawer for responsive slide-up bottom sheet")
    else:
        print("  ⚠ Could not find exact old_drawer_funcs")

    # 5. Update openDrawer content header: make cover and buttons wrap nicely on mobile
    old_drawer_header = """        <div class="flex gap-4 items-start mb-6">
          <div class="w-28 shrink-0 aspect-[2/3] book-cover ${{jacketCls}} shadow-md relative overflow-hidden rounded-[8px] bg-[var(--border-subtle)]/40 p-1">
            ${{b.cover_url && !b.no_cover ? `
              <img src="${{b.cover_url}}" alt="${{b.title}}" class="w-full h-full object-contain drop-shadow-xs rounded-lg" onerror="this.onerror=null;this.style.display='none';this.parentElement.querySelector('.fallback-drawer').style.display='block';" />
              <div class="fallback-drawer hidden absolute inset-0 z-10 w-full h-full">
                ${{renderTypographicJacket(b)}}
              </div>
            ` : `
              <div class="w-full h-full">
                ${{renderTypographicJacket(b)}}
              </div>
            `}}
          </div>
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--terracotta)]">${{b.category}}</span>
              ${{getFormatBadgeHtml(getCleanFormat(b))}}
            </div>
            <h3 class="font-serif font-bold text-lg text-[var(--text-heading)] mt-0.5 leading-snug">${{b.title}}</h3>
            <p class="text-xs text-[var(--text-muted)] font-medium">by ${{b.author}}</p>
            <div class="flex flex-wrap items-center gap-2 mt-3">
              <button onclick="openBookInNook(event, '${{b.id}}')" class="px-3 py-1.5 bg-[var(--terracotta)] hover:bg-[var(--terracotta-hover)] text-white text-xs font-bold rounded-lg shadow-sm transition flex items-center gap-1.5 cursor-pointer">
                <span>📖</span>
                <span>Read in Nook ↗</span>
              </button>"""

    new_drawer_header = """        <div class="flex flex-col sm:flex-row gap-4 items-center sm:items-start mb-6 text-center sm:text-left">
          <div class="w-28 shrink-0 aspect-[2/3] book-cover ${{jacketCls}} shadow-md relative overflow-hidden rounded-[8px] bg-[var(--border-subtle)]/40 p-1 mx-auto sm:mx-0">
            ${{b.cover_url && !b.no_cover ? `
              <img src="${{b.cover_url}}" alt="${{b.title}}" class="w-full h-full object-contain drop-shadow-xs rounded-lg" onerror="this.onerror=null;this.style.display='none';this.parentElement.querySelector('.fallback-drawer').style.display='block';" />
              <div class="fallback-drawer hidden absolute inset-0 z-10 w-full h-full">
                ${{renderTypographicJacket(b)}}
              </div>
            ` : `
              <div class="w-full h-full">
                ${{renderTypographicJacket(b)}}
              </div>
            `}}
          </div>
          <div class="flex-1 w-full">
            <div class="flex items-center justify-center sm:justify-start gap-2 mb-1">
              <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--terracotta)]">${{b.category}}</span>
              ${{getFormatBadgeHtml(getCleanFormat(b))}}
            </div>
            <h3 class="font-serif font-bold text-lg text-[var(--text-heading)] mt-0.5 leading-snug">${{b.title}}</h3>
            <p class="text-xs text-[var(--text-muted)] font-medium">by ${{b.author}}</p>
            <div class="flex flex-wrap items-center justify-center sm:justify-start gap-2 mt-3.5">
              <button onclick="openBookInNook(event, '${{b.id}}')" class="flex-1 sm:flex-none px-4 py-2 min-h-[40px] bg-[var(--terracotta)] hover:bg-[var(--terracotta-hover)] text-white text-xs font-bold rounded-xl shadow-xs transition flex items-center justify-center gap-1.5 cursor-pointer">
                <span>${{ (b.format && b.format.toLowerCase() === 'pdf') ? '📄' : '📖' }}</span>
                <span>${{ (b.format && b.format.toLowerCase() === 'pdf') ? 'Open PDF ↗' : 'Read in Nook ↗' }}</span>
              </button>"""

    if old_drawer_header in content:
        content = content.replace(old_drawer_header, new_drawer_header, 1)
        print("  ✓ Updated drawer content header for mobile centered layout & 40px touch buttons")
    else:
        print("  ⚠ Could not find exact old_drawer_header")

    TARGET_SCRIPT.write_text(content, encoding="utf-8")
    print(f"  ✓ Saved updates to {TARGET_SCRIPT}")

if __name__ == "__main__":
    patch_js()
