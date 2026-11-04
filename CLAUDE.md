# Marginalia

> **Status**: Complete | **Phase**: 13 (Pinterest Visual Board & Editorial Bookshelf Redesign)  
> **Current**: Total redesign of UI/UX. Default view set to a high-density Pinterest-style visual book board where cover jackets take center stage. Built a toggleable Bookshelf Split View (scrollable shelf on the left, sticky reading dossier on the right with the synopsis, quotes, and companion notes). Curated the "Surprise Me" engine strictly around joyful, unputdownable fiction, craft essays by novelists, and accessible philosophy (excluding chores/textbooks). Re-architected cover rendering with physical jacket textures, genre palettes, and OpenLibrary cover integration.  
> **Next**: Ready for visual browsing, mood-based reading discovery, and TBR exports.

## Roadmap

- [x] Phase 1: Foundational directives — update CLAUDE.md and VOICE.md to strip out marketing/SaaS slant
- [x] Phase 2: Content audit and revision — rewrite 69 cards in `content/cards.json` to focus on writing craft
- [x] Phase 3: Validation — verify zero flags in `python3 tools/lint_cards.py` and clean `build_prototype.py`
- [x] Phase 4: Curate stronger quotes — add 5 gold-standard cards (Manto, Baldwin, Didion, Dillard, Burkeman) & expand `content/quote-bank.md`
- [x] Phase 5: GitHub synchronization — commit and push updates to `terriblyoffendedmarketer-stack/quotes-project`
- [x] Phase 6: Master Quote Bank mining — extract 800–1,200 quotes across 400+ books using local offline AI without token burnout (Reached 1,871 quotes / 416 books)
- [x] Phase 7: Quote Bank UI & Integration — Thematic horizons web reader, dynamic tag discovery, and dual-mode Android widget integration
- [x] Phase 8: In-App UX Polish, Boundary Fixes & Dostoevsky Trifles Curation (APK release compiled, boundary margins fixed)
- [x] Phase 9: Shelf Quote Explanation Renaissance — Two-tier cognitive standard, zero-spoiler ground truth, and Gemini Free Tier pipeline (458 quotes enriched)
- [x] Phase 10: Web App Edition & GitHub Pages Live Deployment — Fully responsive mobile/desktop web app with APK download, OpenGraph previews, and dual-collection browsing
- [x] Phase 11: Google Drive Library Dynamic Shelf & TBR Recommender — Full drive indexing (676 files), 631 unique shelf cards, 587 clean TBR entries, and interactive recommendation web app
- [x] Phase 12: Library Audit, Bullshit Purge & Strict Attribution — Purged 30 tactical hustle PDFs/lead magnets, separated HBR books, restored correct titles (Heartburn, Foundations of Screenwriting), and generated Google Drive move script
- [x] Phase 13: Pinterest Visual Board & Editorial Bookshelf Redesign — Pinterest board grid, dual-mode split view, curated joy-of-reading engine, and voice-driven editorial dossiers

## File map

- `content/cards.json`: Single source of truth for all 108 cards (quote, hook, lookCloser, stealIt, aroundIt).
- `QUOTE_BANK_ARCHITECTURE.md`: Master architectural blueprint for the 800-1,200 quote bank, anti-fatigue UX, and local Ollama pipeline.
- `content/quote-bank.json`: Structured storage for the master multi-book quote bank (1,882 quotes across 423 books).
- `content/quote-bank.md`: Human-readable quote bank catalog grouped by book.
- `content/authors.md`: Master author library (classic, contemporary, memoir, nonfiction) and their strengths.
- `content/gdrive_books_catalog.json`: Raw index of all 676 book files across Google Drive with paths and sizes.
- `content/books_curated_shelf.json`: Audited and cleaned dynamic shelf containing 620 high-conviction works with pitches, reader notes, and tags.
- `content/covers_cache.json`: Cache of Open Library and custom resolved book cover URLs.
- `content/tbr_clean_list.txt`: Clean, 1-click copy-pastable `Title — Author` list of 620 books for TBR trackers.
- `scripts/build_pinterest_bookshelf.py`: Compiles the visual Pinterest board and two-pane bookshelf split reader.
- `scripts/fetch_covers_and_enhance_content.py`: Concurrently fetches Open Library covers and injects rich editorial pitches.
- `scripts/move_drive_files.sh`: Shell script to move 30 tactical lead magnets to `Books/Archive of bullshit` and HBR books to `Books/HBR`.
- `prototype/shelf.html` & `docs/shelf.html`: Redesigned visual Pinterest board and Bookshelf reader.
- `scripts/mine_quote_bank.py`: Local extraction engine using Ollama (`gemma3:4b`) to scout literary quotes from EPUBs.
- `scripts/mine_full_library.py`: Continuous automated full-library mining engine with Dublin Core metadata reader and zero-spoiler gating.
- `scripts/harmonize_quote_bank.py`: Harmonization utility ensuring all 1,871 quotes share the unified reading companion schema.
- `scripts/serve_preview.py`: Zero-install local HTTP preview server for Marginalia Visual Studio in browser.
- `tools/build_prototype.py`: Rebuilds the browser review prototype in `prototype/index.html`.
- `android/`: Android app and adaptive dual-mode home-screen widget source code.
- `android/marginalia.apk`: Signed release build ready for sideloading.
- `prototype/`: Web-based reader with single-page thematic horizons, instant search, and tag filtering.

## Setup & run instructions

- Python tools require only the Python 3 standard library:
  - Run linter: `python3 tools/lint_cards.py`
  - Rebuild web prototype: `python3 tools/build_prototype.py`
  - Rebuild Pinterest shelf app: `python3 scripts/build_pinterest_bookshelf.py`
- GitHub sync:
  - Push updates: `git add . && git commit -m "..." && git push origin main`
