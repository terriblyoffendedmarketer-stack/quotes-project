# Marginalia

> **Status**: Complete | **Phase**: 14 (Standalone Ex Libris Bookshelf & Remote Reorganization)  
> **Current**: Successfully executed server-side Google Drive reorganization via rclone moving 30 tactical hustle/lead magnet files to `Books/Archive of bullshit` and 4 HBR books to `Books/HBR`. Restored and locked Marginalia codebase completely untouched (`prototype/index.html`, `docs/index.html`, `content/cards.json`). Built the reading shelf as an independent, standalone web application called **Ex Libris** in `bookshelf/` (ready for an independent repository) featuring a joyful, warm cream/terracotta visual design, Pinterest visual jacket board, two-pane bookshelf split reader, live search & category filters, direct Google Drive file view links for all 620 books, full Quote Bank matching across 314 books with >1,500 quotes, and a fun-reading "Surprise Me" engine.  
> **Next**: Independent repository extraction for `bookshelf/` or further reading shelf feature enhancements.

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
- [x] Phase 14: Standalone Ex Libris Bookshelf & Remote Reorganization — Server-side rclone moves executed; Ex Libris built in `bookshelf/` decoupled from Marginalia; 314 books linked with Quote Bank; direct Drive links on all 620 titles; warm joyful aesthetic applied

## File map

- `bookshelf/`: Decoupled, standalone reading shelf web app (**Ex Libris**) ready for independent git repository (`index.html`, `data.json`).
- `content/gdrive_file_ids.json`: Cache of Google Drive file IDs mapping every book to its direct view link (`https://drive.google.com/file/d/{id}/view`).
- `content/cards.json`: Single source of truth for all Marginalia craft cards (untouched).
- `content/quote-bank.json`: Structured storage for the master multi-book quote bank (1,882 quotes across 423 books).
- `content/quote-bank.md`: Human-readable quote bank catalog grouped by book.
- `content/authors.md`: Master author library (classic, contemporary, memoir, nonfiction) and their strengths.
- `content/gdrive_books_catalog.json`: Raw index of all 676 book files across Google Drive with paths and sizes.
- `content/books_curated_shelf.json`: Audited and cleaned dynamic shelf containing 620 high-conviction works with pitches, reader notes, and tags.
- `content/covers_cache.json`: Cache of Open Library and custom resolved book cover URLs.
- `content/tbr_clean_list.txt`: Clean, 1-click copy-pastable `Title — Author` list of 620 books for TBR trackers.
- `scripts/build_independent_bookshelf_app.py`: Compiles the standalone Ex Libris reading shelf app (`bookshelf/index.html`, `bookshelf/data.json`, `docs/bookshelf.html`).
- `scripts/move_drive_files.sh`: Shell script used to move 30 tactical lead magnets to `Books/Archive of bullshit` and HBR books to `Books/HBR`.
- `prototype/index.html` & `docs/index.html`: Marginalia craft card web reader (untouched, independent project).
- `android/`: Marginalia Android app and home-screen widget source code.
- `android/marginalia.apk`: Signed release build ready for sideloading.
- `prototype/`: Web-based reader with single-page thematic horizons, instant search, and tag filtering.

## Setup & run instructions

- Python tools require only the Python 3 standard library:
  - Run linter: `python3 tools/lint_cards.py`
  - Rebuild web prototype: `python3 tools/build_prototype.py`
  - Rebuild Pinterest shelf app: `python3 scripts/build_pinterest_bookshelf.py`
- GitHub sync:
  - Push updates: `git add . && git commit -m "..." && git push origin main`
