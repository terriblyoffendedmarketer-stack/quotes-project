# Marginalia

> **Status**: In Progress | **Phase**: 28 (Reading Nook Kindle Bookerly Calibration & Immersive Canvas)  
> **Current**: Standardized all references across bookshelf views, cards, modals, and reader to 'Reading Nook'. Calibrated reader typography to Kindle Bookerly standard (tight 1.5 line height, 1.4em paragraph indents, elegant regular-weight headings with 1.65em h1). Converted top navigation into an auto-hiding immersive bar that slides down on mousemove near top or clicking reveal pill, maximizing vertical canvas in fullscreen and default windows. Converted bottom status bar into a seamless transparent Kindle footer without dividing border lines, while preserving the requested center spine divider. Bumped Service Worker cache to v13.  
> **Next**: User review of immersive Reading Nook experience.

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
- [x] Phase 16: My Reading Corner & Single Cohesive Curator Voice — Rebranded to My Reading Corner with cozy reading lamp emblem; single literate `✦ Curator's Note` replacing fragmented 4-box layout; 2-column unclipped Editorial layout; PWA manifest & service worker deployed to GitHub Pages
- [x] Phase 17: Library Integrity & Full Quote Enrichment — Separated Bad Pharma/Bad Science; corrected How to Research Anything, GothamChess, and Osho; resolved 33 new covers (539/620); Claude API daemon completing remaining quotes to reach 100% (620/620 titles)
- [x] Phase 18: In-Browser Reading Nook & GitHub Pages CI — Standalone client-side EPUB reader with IndexedDB offline storage and quote saving tool; automated GitHub Pages deploy pipeline; unclipped 2-column editorial cards with synopsis focus
- [x] Phase 19: Streamlined "Read in Nook" Flow, Apple Books/Kindle Viewport & Generous Editorial Posters — 1-click direct download via usercontent, Apple Books centered typography, generous unclipped posters, and new tab PWA isolation
- [x] Phase 20: Remove Cover Option, Classic Typographic Template Jacket & Persistence Guard — Dedicated cover removal button in modal and 1-click dossier action, no_cover localStorage and build script persistence guards, and elegant category-styled clothbound typographic jackets
- [x] Phase 21: Kindle Bifold Reader Spread, Tab Scope Isolation & Comprehensive Cover Renaissance — Two-page bifold spread with center spine crease, Kindle paragraph indents & justification, tab scope restriction to prevent PWA hijacking, named tab reuse, PDF direct handling, and full audit/fix of book covers (Riddler, Sandman, 4-Hour Chef, King, Burkeman, Screenplays)
- [x] Phase 22: Direct Nook Download Action, PWA Standalone Restoration & Zero Auto-Download on Shelf — Removed auto-download on shelf click, added 1-click direct download on Nook dropzone without Google Drive redirects, restored manifest scope to './' for PWA window reading
- [x] Phase 23: Editorial View Synopsis Unclamping & 1-Click Inline Expand — Expanded vertical synopsis clamp up to 13 lines to utilize card height alongside cover; added inline 'Read full synopsis ↓' expand toggle for extra-long blurbs; pinned cover with self-start
- [x] Phase 24: Header Button Responsive Sizing, Nooks Syntax Fix & Dropzone Hierarchy — Restored `async function initReader()` fixing drag-and-drop & file picker; re-ordered dropzone buttons (Button 1: Direct Download, Button 2: Browse); implemented adaptive header buttons ('Surprise Me' / 'Surprise', 'Copy TBR' / 'TBR') and CSS-level `-webkit-line-clamp` (6/7/7/9/11) with card `overflow-hidden` for non-fullscreen viewports
- [x] Phase 25: Daily-Seeded & Alphabetical Multi-View Sorting, Header Nooks Reader Button & Direct Ebook Downloads — Mulberry32 PRNG daily seeded shuffle default with A-Z, Z-A, Author, Quotes, and Category sorting across all 3 views; Open Nooks Reader header action; and direct named ebook downloading replacing Google Drive links
- [x] Phase 26: Universal EPUB/PDF Format Tagging & Surprise Me Modal Optimization — Standardized canonical format resolution across all 620 titles; added visible color-coded format badges (emerald EPUB, rose PDF, purple CBR) to Board View, Editorial View, Split View list & dossier, and drawer; and optimized Surprise Me modal with Read on Nooks primary button, named direct downloads, and responsive layout
- [x] Phase 27: Nook EPUB Reader Fullscreen & Bifold Spread Perfection — Eliminated 3rd column peek by removing theme column-gap/padding overrides; restored true geometric bifold spread; added rendition cleanup, iframe keyboard listener & debounced window resize handler; bumped SW cache to v12.
- [x] Phase 28: Reading Nook Kindle Bookerly Calibration & Immersive Canvas — Standardized name to 'Reading Nook' across entire app; calibrated Bookerly typography (tight 1.5 line height, 1.4em indents, 1.65em regular-weight headings); added auto-hiding top bar with mousemove sensor and reveal trigger; transformed footer to seamless Kindle indicator; preserved central spine divider; bumped SW cache to v13.

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
