# scripts/patch_shelf_app_mobile_optimization.py — Patches build_independent_bookshelf_app.py with mobile ergonomics & responsive header
# Usage: python3 scripts/patch_shelf_app_mobile_optimization.py
# Requires: Python 3.8+ (standard library only)
#
# Gotchas:
# - Laptop view (widths >= 768px / 1024px) MUST remain completely intact and identical to its solidified state.
# - Mobile view (< 768px / 640px) uses adaptive layout: compact app bar with touch icons, 44px segmented view switcher,
#   2-column Pinterest board, stacked editorial cards, and native bottom slide-up dossier sheet.
# - Search and view switcher inputs must be synchronized across desktop and mobile DOM IDs.

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET_SCRIPT = ROOT / "scripts" / "build_independent_bookshelf_app.py"

def patch_shelf_script():
    print(f"Patching {TARGET_SCRIPT}...")
    content = TARGET_SCRIPT.read_text(encoding="utf-8")

    # 1. Update CSS in generate_app_html for mobile scrollbar, safe areas, and bottom sheet
    old_css_marker = "    .editorial-synopsis.expanded {"
    new_css = """    /* Mobile Safe Area & Touch Ergonomics */
    :root {
      --safe-top: env(safe-area-inset-top, 0px);
      --safe-bottom: env(safe-area-inset-bottom, 0px);
      --safe-left: env(safe-area-inset-left, 0px);
      --safe-right: env(safe-area-inset-right, 0px);
    }

    @media (max-width: 639px) {
      .editorial-synopsis {
        display: -webkit-box !important;
        -webkit-box-orient: vertical !important;
        -webkit-line-clamp: 4 !important;
        overflow: hidden !important;
      }
    }

    .editorial-synopsis.expanded {"""

    if "/* Mobile Safe Area & Touch Ergonomics */" not in content:
        content = content.replace(old_css_marker, new_css, 1)
        print("  ✓ Added mobile safe area and editorial synopsis clamp CSS")

    # 2. Update Header: Provide Desktop bar (hidden < md) and Mobile bar (visible < md)
    old_header_start = """  <!-- Header -->
  <header class="sticky top-0 z-40 bg-[var(--canvas)]/95 backdrop-blur-md border-b border-[var(--border)] px-4 md:px-8 py-3.5">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-4">"""

    new_header_start = """  <!-- Header -->
  <header class="sticky top-0 z-40 bg-[var(--canvas)]/95 backdrop-blur-md border-b border-[var(--border)] px-4 md:px-8 py-2.5 md:py-3.5">
    <!-- Desktop Header: Exactly Solidified Layout (hidden on mobile < md) -->
    <div class="hidden md:flex max-w-7xl mx-auto items-center justify-between gap-4">"""

    if old_header_start in content:
        content = content.replace(old_header_start, new_header_start, 1)
        print("  ✓ Scoped desktop header to hidden on mobile (hidden md:flex)")
    else:
        print("  ⚠ Could not find exact old_header_start block")

    # Wrap the end of desktop header controls and append mobile header
    old_desktop_controls_end = """        <!-- Theme Toggle -->
        <button 
          onclick="toggleDarkMode()" 
          class="p-2 bg-[var(--card-bg)] border border-[var(--border)] text-[var(--text-muted)] hover:text-[var(--text-heading)] rounded-xl text-xs shadow-sm">
          <span id="themeIcon">🌙</span>
        </button>
      </div>
    </div>
  </header>"""

    new_desktop_controls_end = """        <!-- Theme Toggle -->
        <button 
          onclick="toggleDarkMode()" 
          class="p-2 bg-[var(--card-bg)] border border-[var(--border)] text-[var(--text-muted)] hover:text-[var(--text-heading)] rounded-xl text-xs shadow-sm">
          <span id="themeIcon">🌙</span>
        </button>
      </div>
    </div>

    <!-- Mobile Adaptive Header (< md: 375px–430px iPhone & Android) -->
    <div class="flex md:hidden flex-col gap-2 max-w-7xl mx-auto">
      <!-- Row 1: Logo & Title + Fast Touch Actions -->
      <div class="flex items-center justify-between gap-2">
        <div class="flex items-center gap-2.5 min-w-0">
          <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-[#8A2814] via-[#C85A32] to-[#E08736] p-0.5 shadow-sm flex items-center justify-center shrink-0 border border-[#F59E0B]/25">
            <svg class="w-5 h-5" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M7 31 H12" stroke="#FEF3C7" stroke-width="1.6" stroke-linecap="round"/>
              <path d="M9.5 31 V17 C9.5 10 14.5 7 21 8" stroke="#FEF3C7" stroke-width="1.6" stroke-linecap="round"/>
              <path d="M19.5 8 L24.5 11.5 L21.5 13.5 Z" fill="#FDE68A"/>
              <path d="M22 13 L15 28 L29 28 Z" fill="#FDE68A" fill-opacity="0.22"/>
              <path d="M15 28 C17.5 26.8 20 26.8 22 28 C24 26.8 26.5 26.8 29 28 V23 C26.5 21.8 24 21.8 22 23 C20 21.8 17.5 21.8 15 23 Z" fill="#FFF7ED" stroke="#B45309" stroke-width="0.8"/>
              <path d="M22 23 V28" stroke="#C85A32" stroke-width="0.8"/>
            </svg>
          </div>
          <div class="min-w-0">
            <h1 class="font-serif font-bold text-base text-[var(--text-heading)] tracking-tight leading-none truncate">
              My Reading Corner
            </h1>
            <p class="text-[9px] font-medium text-[var(--text-muted)] truncate mt-0.5">{total_books} Books • Reflowable EPUB</p>
          </div>
        </div>

        <!-- Fast Touch Actions (40px touch minimum) -->
        <div class="flex items-center gap-1.5 shrink-0">
          <button 
            onclick="openDirectReadingNook()" 
            class="px-2.5 py-1.5 min-h-[38px] bg-[var(--terracotta)] text-white hover:bg-[var(--terracotta-hover)] rounded-xl text-xs font-bold transition flex items-center gap-1 shadow-2xs"
            title="Open Reading Nook">
            <span>📖</span>
            <span class="text-[11px]">Nook</span>
          </button>
          <button 
            onclick="openSurpriseModal()" 
            class="p-2 min-h-[38px] min-w-[38px] flex items-center justify-center bg-[var(--amber-bg)] text-[var(--terracotta)] border border-[var(--terracotta)]/30 rounded-xl text-xs font-bold transition shadow-2xs"
            title="Surprise Book">
            <span>✨</span>
          </button>
          <button 
            onclick="toggleDarkMode()" 
            class="p-2 min-h-[38px] min-w-[38px] flex items-center justify-center bg-[var(--card-bg)] border border-[var(--border)] text-[var(--text-muted)] rounded-xl text-xs shadow-2xs"
            title="Toggle Theme">
            <span id="mobileThemeIcon">🌙</span>
          </button>
        </div>
      </div>

      <!-- Row 2: Search Bar -->
      <div class="relative w-full">
        <input 
          type="text" 
          id="mobileSearchInput" 
          oninput="handleSearch(this.value)"
          placeholder="Search 620 books, authors, quotes..." 
          class="w-full pl-9 pr-8 py-2 bg-[var(--card-bg)] border border-[var(--border)] rounded-full text-xs text-[var(--text-heading)] placeholder-[var(--text-muted)] focus:outline-none focus:ring-2 focus:ring-[var(--terracotta)]/30 focus:border-[var(--terracotta)] shadow-2xs transition min-h-[40px]"
        />
        <span class="absolute left-3.5 top-2.5 text-[var(--text-muted)] text-xs">🔍</span>
        <button id="mobileSearchClearBtn" onclick="clearSearchInput()" class="absolute right-3 top-2 text-[var(--text-muted)] hover:text-[var(--text-heading)] text-xs p-1 hidden" title="Clear search">✕</button>
      </div>

      <!-- Row 3: Segmented View Switcher Pill Bar (44px Apple HIG Touch Minimum) -->
      <div class="bg-[var(--card-bg)] p-1 rounded-xl border border-[var(--border)] flex items-center text-xs shadow-2xs w-full">
        <button 
          id="mobileViewBtnBoard" 
          onclick="switchView('board')" 
          class="flex-1 py-1.5 rounded-lg font-semibold transition bg-[var(--terracotta)] text-white shadow-xs flex items-center justify-center gap-1 min-h-[38px]">
          <span>📌</span>
          <span class="text-[11px]">Covers</span>
        </button>
        <button 
          id="mobileViewBtnEditorial" 
          onclick="switchView('editorial')" 
          class="flex-1 py-1.5 rounded-lg font-medium transition text-[var(--text-muted)] hover:text-[var(--text-heading)] flex items-center justify-center gap-1 min-h-[38px]">
          <span>📰</span>
          <span class="text-[11px]">Editorial</span>
        </button>
        <button 
          id="mobileViewBtnSplit" 
          onclick="switchView('split')" 
          class="flex-1 py-1.5 rounded-lg font-medium transition text-[var(--text-muted)] hover:text-[var(--text-heading)] flex items-center justify-center gap-1 min-h-[38px]">
          <span>📚</span>
          <span class="text-[11px]">Bookshelf</span>
        </button>
      </div>
    </div>
  </header>"""

    if old_desktop_controls_end in content:
        content = content.replace(old_desktop_controls_end, new_desktop_controls_end, 1)
        print("  ✓ Appended adaptive mobile header with segmented view switcher")
    else:
        print("  ⚠ Could not find exact old_desktop_controls_end block")

    # 3. Update Filter Ribbon for Responsive Mobile Stacking
    old_filter_ribbon = """  <!-- Filter Ribbon -->
  <div class="border-b border-[var(--border-subtle)] bg-[var(--card-bg)]/60 px-4 md:px-8 py-2">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-4">
      <div class="flex items-center gap-1.5 overflow-x-auto py-1 no-scrollbar" id="categoryTabs">
        <!-- Populated dynamically -->
      </div>
      <div class="flex items-center gap-2.5 sm:gap-3 text-xs text-[var(--text-muted)] shrink-0">"""

    new_filter_ribbon = """  <!-- Filter Ribbon -->
  <div class="border-b border-[var(--border-subtle)] bg-[var(--card-bg)]/60 px-4 md:px-8 py-2">
    <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2.5 sm:gap-4">
      <div class="flex items-center gap-1.5 overflow-x-auto py-1 no-scrollbar shrink min-w-0" id="categoryTabs">
        <!-- Populated dynamically -->
      </div>
      <div class="flex items-center justify-between sm:justify-end gap-2.5 sm:gap-3 text-xs text-[var(--text-muted)] shrink-0">"""

    if old_filter_ribbon in content:
        content = content.replace(old_filter_ribbon, new_filter_ribbon, 1)
        print("  ✓ Made filter ribbon responsive for mobile touch scrolling and alignment")
    else:
        print("  ⚠ Could not find exact old_filter_ribbon block")

    # 4. Update Board View & Editorial View Grid Classes on Mobile
    old_board_grid = """    <!-- 1. Visual Jackets Board View (Default: 5 columns max on desktop, larger covers) -->
    <div id="boardView" class="block">
      <div id="boardGrid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6 md:gap-7">
        <!-- Populated dynamically -->
      </div>
    </div>"""

    new_board_grid = """    <!-- 1. Visual Jackets Board View (Default: 5 columns on desktop, 2-column Pinterest grid on mobile) -->
    <div id="boardView" class="block">
      <div id="boardGrid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3.5 sm:gap-6 md:gap-7">
        <!-- Populated dynamically -->
      </div>
    </div>"""

    if old_board_grid in content:
        content = content.replace(old_board_grid, new_board_grid, 1)
        print("  ✓ Calibrated board grid gap for mobile 2-column cards")
    else:
        print("  ⚠ Could not find exact old_board_grid block")

    # 5. Update Editorial Card Template: Stack cover above synopsis on mobile (< 640px)
    old_editorial_card_start = """          <div class="editorial-card bg-[var(--card-bg)] border border-[var(--border)] hover:border-[var(--terracotta)]/40 rounded-2xl p-4 sm:p-5 md:p-6 flex flex-row gap-4 sm:gap-6 hover:shadow-lg transition-all duration-200 cursor-pointer group items-stretch overflow-hidden" onclick="openBookDetail('${{b.id}}')">
            <!-- Cover (Left: substantial horizontal real estate, perfectly proportioned, 4 cards visible on screen) -->
            <div class="w-32 sm:w-40 md:w-48 lg:w-56 shrink-0 aspect-[2/3] book-cover ${{jacketCls}} relative rounded-xl overflow-hidden shadow-sm border border-black/10 flex items-center justify-center bg-[var(--border-subtle)]/40 p-1 self-start">"""

    new_editorial_card_start = """          <div class="editorial-card bg-[var(--card-bg)] border border-[var(--border)] hover:border-[var(--terracotta)]/40 rounded-2xl p-4 sm:p-5 md:p-6 flex flex-col sm:flex-row gap-4 sm:gap-6 hover:shadow-lg transition-all duration-200 cursor-pointer group items-stretch overflow-hidden" onclick="openBookDetail('${{b.id}}')">
            <!-- Cover (Mobile: centered 2:3 card; Desktop: left-aligned proportional jacket) -->
            <div class="w-32 sm:w-40 md:w-48 lg:w-56 shrink-0 aspect-[2/3] mx-auto sm:mx-0 book-cover ${{jacketCls}} relative rounded-xl overflow-hidden shadow-sm border border-black/10 flex items-center justify-center bg-[var(--border-subtle)]/40 p-1 self-center sm:self-start">"""

    if old_editorial_card_start in content:
        content = content.replace(old_editorial_card_start, new_editorial_card_start, 1)
        print("  ✓ Updated editorial card to stack on mobile (flex-col sm:flex-row)")
    else:
        print("  ⚠ Could not find exact old_editorial_card_start block")

    # 6. Update Drawer / Dossier Modal: Bottom Sheet on Mobile (< 640px), Side Drawer on Desktop (>= 640px)
    old_drawer_html = """  <!-- Slide-Out Drawer for Mobile or Board Click -->
  <div id="drawerOverlay" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex justify-end hidden">
    <div id="drawerPanel" class="w-full max-w-xl bg-[var(--card-bg)] border-l border-[var(--border)] h-full overflow-y-auto p-6 md:p-8 shadow-2xl transition-transform transform translate-x-full">
      <div class="flex items-center justify-between pb-4 border-b border-[var(--border)] mb-6">
        <span class="text-xs font-bold uppercase tracking-widest text-[var(--terracotta)]">Reading Dossier</span>
        <button onclick="closeDrawer()" class="text-[var(--text-muted)] hover:text-[var(--text-heading)] text-xl font-bold p-1">✕</button>
      </div>
      <div id="drawerContent">
        <!-- Populated dynamically -->
      </div>
    </div>
  </div>"""

    new_drawer_html = """  <!-- Slide-Out Drawer / Mobile Bottom Sheet for Board & Editorial Click -->
  <div id="drawerOverlay" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-end sm:items-stretch sm:justify-end hidden" onclick="handleDrawerOverlayClick(event)">
    <div id="drawerPanel" class="w-full sm:max-w-xl bg-[var(--card-bg)] border-t sm:border-t-0 sm:border-l border-[var(--border)] h-[88vh] sm:h-full max-h-[92vh] sm:max-h-none rounded-t-3xl sm:rounded-t-none overflow-y-auto p-5 sm:p-6 md:p-8 shadow-2xl transition-transform duration-300 transform translate-y-full sm:translate-y-0 sm:translate-x-full">
      <!-- Mobile Pull Bar Handle -->
      <div class="w-12 h-1.5 bg-stone-300 dark:bg-stone-600 rounded-full mx-auto mb-3 sm:hidden"></div>
      <div class="flex items-center justify-between pb-3 sm:pb-4 border-b border-[var(--border)] mb-4 sm:mb-6">
        <span class="text-xs font-bold uppercase tracking-widest text-[var(--terracotta)]">Reading Dossier</span>
        <button onclick="closeDrawer()" class="text-[var(--text-muted)] hover:text-[var(--text-heading)] text-xl font-bold p-2 min-w-[40px] min-h-[40px] flex items-center justify-center">✕</button>
      </div>
      <div id="drawerContent">
        <!-- Populated dynamically -->
      </div>
    </div>
  </div>"""

    if old_drawer_html in content:
        content = content.replace(old_drawer_html, new_drawer_html, 1)
        print("  ✓ Updated drawer container for native mobile bottom sheet with drag handle")
    else:
        print("  ⚠ Could not find exact old_drawer_html block")

    # 7. Update JavaScript: Synchronize search inputs, update switchView, update openDrawer & closeDrawer
    old_switch_view = """    function switchView(view) {
      activeView = view;

      // Update button styles
      ["board", "editorial", "split"].forEach(v => {
        const btn = document.getElementById(`viewBtn${v.charAt(0).toUpperCase() + v.slice(1)}`);
        if (v === view) {
          btn.className = "px-3 py-1 rounded-lg font-semibold transition bg-[var(--terracotta)] text-white shadow-sm flex items-center gap-1.5";
        } else {
          btn.className = "px-3 py-1 rounded-lg font-medium transition text-[var(--text-muted)] hover:text-[var(--text-heading)] flex items-center gap-1.5";
        }
      });"""

    new_switch_view = """    function switchView(view) {
      activeView = view;

      // Update desktop and mobile button styles
      ["board", "editorial", "split"].forEach(v => {
        const cap = v.charAt(0).toUpperCase() + v.slice(1);
        const dBtn = document.getElementById(`viewBtn${cap}`);
        const mBtn = document.getElementById(`mobileViewBtn${cap}`);

        if (dBtn) {
          if (v === view) {
            dBtn.className = "px-3 py-1 rounded-lg font-semibold transition bg-[var(--terracotta)] text-white shadow-sm flex items-center gap-1.5";
          } else {
            dBtn.className = "px-3 py-1 rounded-lg font-medium transition text-[var(--text-muted)] hover:text-[var(--text-heading)] flex items-center gap-1.5";
          }
        }

        if (mBtn) {
          if (v === view) {
            mBtn.className = "flex-1 py-1.5 rounded-lg font-semibold transition bg-[var(--terracotta)] text-white shadow-xs flex items-center justify-center gap-1 min-h-[38px]";
          } else {
            mBtn.className = "flex-1 py-1.5 rounded-lg font-medium transition text-[var(--text-muted)] hover:text-[var(--text-heading)] flex items-center justify-center gap-1 min-h-[38px]";
          }
        }
      });"""

    if old_switch_view in content:
        content = content.replace(old_switch_view, new_switch_view, 1)
        print("  ✓ Updated switchView to synchronize desktop & mobile view buttons")
    else:
        print("  ⚠ Could not find exact old_switch_view block")

    # 8. Update handleSearch and clearSearchInput
    old_handle_search = """    function handleSearch() {
      searchQuery = document.getElementById("searchInput").value.trim();
      renderCurrentView();
    }"""

    new_handle_search = """    function handleSearch(val) {
      const q = (val !== undefined ? val : (document.getElementById("searchInput")?.value || document.getElementById("mobileSearchInput")?.value || "")).trim();
      const dInput = document.getElementById("searchInput");
      const mInput = document.getElementById("mobileSearchInput");
      const clearBtn = document.getElementById("mobileSearchClearBtn");

      if (dInput && dInput.value !== q) dInput.value = q;
      if (mInput && mInput.value !== q) mInput.value = q;
      if (clearBtn) clearBtn.classList.toggle("hidden", !q);

      searchQuery = q;
      renderCurrentView();
    }

    function clearSearchInput() {
      handleSearch("");
    }"""

    if old_handle_search in content:
        content = content.replace(old_handle_search, new_handle_search, 1)
        print("  ✓ Updated handleSearch to synchronize dual desktop/mobile inputs with 1-click clear")
    else:
        print("  ⚠ Could not find exact old_handle_search block")

    # 9. Update toggleDarkMode to sync mobileThemeIcon
    old_toggle_dark = """    function toggleDarkMode() {
      document.body.classList.toggle("dark-mode");
      const isDark = document.body.classList.contains("dark-mode");
      document.getElementById("themeIcon").innerText = isDark ? "☀️" : "🌙";
      localStorage.setItem("exlibris_theme", isDark ? "dark" : "light");
    }"""

    new_toggle_dark = """    function toggleDarkMode() {
      document.body.classList.toggle("dark-mode");
      const isDark = document.body.classList.contains("dark-mode");
      const icon = isDark ? "☀️" : "🌙";
      if (document.getElementById("themeIcon")) document.getElementById("themeIcon").innerText = icon;
      if (document.getElementById("mobileThemeIcon")) document.getElementById("mobileThemeIcon").innerText = icon;
      localStorage.setItem("exlibris_theme", isDark ? "dark" : "light");
    }"""

    if old_toggle_dark in content:
        content = content.replace(old_toggle_dark, new_toggle_dark, 1)
        print("  ✓ Synchronized mobile theme icon in toggleDarkMode")
    else:
        print("  ⚠ Could not find exact old_toggle_dark block")

    # 10. Update openDrawer and closeDrawer for Bottom Sheet animation
    old_open_drawer_end = """      overlay.classList.remove("hidden");
      setTimeout(() => panel.classList.remove("translate-x-full"), 10);
    }

    function closeDrawer() {
      const panel = document.getElementById("drawerPanel");
      panel.classList.add("translate-x-full");
      setTimeout(() => {
        document.getElementById("drawerOverlay").classList.add("hidden");
      }, 200);
    }"""

    new_open_drawer_end = """      overlay.classList.remove("hidden");
      setTimeout(() => {
        if (window.innerWidth < 640) {
          panel.classList.remove("translate-y-full");
        } else {
          panel.classList.remove("sm:translate-x-full");
        }
      }, 10);
    }

    function closeDrawer() {
      const panel = document.getElementById("drawerPanel");
      if (window.innerWidth < 640) {
        panel.classList.add("translate-y-full");
      } else {
        panel.classList.add("sm:translate-x-full");
      }
      setTimeout(() => {
        document.getElementById("drawerOverlay").classList.add("hidden");
      }, 220);
    }

    function handleDrawerOverlayClick(e) {
      if (e.target.id === "drawerOverlay") {
        closeDrawer();
      }
    }"""

    if old_open_drawer_end in content:
        content = content.replace(old_open_drawer_end, new_open_drawer_end, 1)
        print("  ✓ Updated openDrawer/closeDrawer for responsive slide-up bottom sheet")
    else:
        print("  ⚠ Could not find exact old_open_drawer_end block")

    # Save target script
    TARGET_SCRIPT.write_text(content, encoding="utf-8")
    print(f"  ✓ Saved updates to {TARGET_SCRIPT}")

if __name__ == "__main__":
    patch_shelf_script()
