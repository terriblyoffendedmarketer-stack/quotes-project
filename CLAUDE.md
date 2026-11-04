# Marginalia

> **Status**: In Progress | **Phase**: 16 (My Reading Corner — Rebranding, 3x2 Editorial Cards, Bespoke Logo & Landmark Quotes Enrichment)  
> **Current**: Rebranded the reading shelf app to **My Reading Corner** with an artisanal literary crest logo (arc reading lamp casting ambient light over an open book). Delivered 3 distinct views: 5-column spacious Covers view with instant hover context, 3x2 Editorial view with side-by-side jacket & synopsis/hook cards, and Bookshelf split-view. Quote companion insights are collapsed by default with single-open exclusive accordion. Enriched 37 landmark missing books (McKee, Truby, Syd Field, Snyder, Tarkovsky, Watchmen, Sandman, Punpun, Akira, Arundhati Roy, Morrison, Bong Joon-ho screenplays, etc.) boosting active quote coverage to 351 books (1,550+ quotes). Live preview running on zero-cache server port 8899.  
> **Next**: Continue mining and enriching remaining 269 titles to achieve 100% full quote coverage across all 620 shelf titles.

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
- [x] Phase 15: Cover Renaissance & High-Octane Editorial Dossiers — 498 high-res covers fetched; authentic Goodreads synopses; structured accolade, cultural impact & trivia dossiers injected; clean unobstructed cover UI
- [~] Phase 16: My Reading Corner & Complete Quote Coverage — Rebranded to My Reading Corner with cozy reading lamp emblem; 3x2 Editorial & 5-column Covers layout; single-open quote accordion; 351 books with quotes (37 landmark books enriched); continuing to 100% quote coverage

## File map

- `bookshelf/`: Decoupled, standalone reading shelf web app (**My Reading Corner**) ready for independent git repository (`index.html`, `data.json`).
- `scripts/enrich_key_missing_quotes.py`: Curated engine injecting iconic quotes and two-tier companion insights for screenwriting, cinema craft, graphic novels, and literature classics.
- `scripts/serve_bookshelf.py`: Lightweight zero-cache local server serving My Reading Corner on port 8899.
- `content/book_metadata_cache.json`: Cache of Open Library works metadata, high-resolution cover IDs, and publisher descriptions.
- `content/covers_cache.json`: Cache of Open Library and custom resolved book cover URLs.
- `content/gdrive_file_ids.json`: Cache of Google Drive file IDs mapping every book to its direct view link (`https://drive.google.com/file/d/{id}/view`).
- `scripts/enrich_covers_and_editorial.py`: Batch engine querying Open Library concurrently for covers and synopses, and injecting four-tier accolades and trivia.
- `content/cards.json`: Single source of truth for all Marginalia craft cards (untouched).
- `content/quote-bank.json`: Structured storage for the master multi-book quote bank (1,882 quotes across 423 books).
- `content/quote-bank.md`: Human-readable quote bank catalog grouped by book.
- `content/authors.md`: Master author library (classic, contemporary, memoir, nonfiction) and their strengths.
- `content/gdrive_books_catalog.json`: Raw index of all 676 book files across Google Drive with paths and sizes.
- `content/books_curated_shelf.json`: Audited and cleaned dynamic shelf containing 620 high-conviction works with pitches, reader notes, and tags.
- `content/tbr_clean_list.txt`: Clean, 1-click copy-pastable `Title — Author` list of 620 books for TBR trackers.
- `scripts/build_independent_bookshelf_app.py`: Compiles the standalone My Reading Corner reading shelf app (`bookshelf/index.html`, `bookshelf/data.json`, `docs/bookshelf.html`).
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
