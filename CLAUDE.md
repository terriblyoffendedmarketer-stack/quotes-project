# Marginalia

> **Status**: Active | **Phase**: 36 (Drive renames, cover OCR audit, tap-to-read, archive)  
> **Current**: Shelf rebuilds + tidies Drive names daily (LaunchAgent, 09:15); local helper with Tidy button always on at http://localhost:8899 (installed 2026-11-12). 455 Drive files renamed to "Title - Author" after multi-source verification (43 held: `content/drive_rename_review.md`). OCR cover audit (`scripts/audit_covers.py`) replacing wrong/foreign covers. Reader opens books straight from Drive via a per-device Drive API key. Archive/Restore in the app.  
> **Next**: tap-to-read set up on user's phone (2026-11-12). Audit wrong synopses (e.g. *In the Blink of an Eye* has invented text). rclone shared client_id retires in 2026.  
> **Keys**: Google Drive API key (browser key, referrer-restricted) is NOT in the repo — macOS Keychain "Reading Corner", `~/Documents/Claude Code/API-KEYS.md`, project `.env` (`GOOGLE_DRIVE_API_KEY`). Users paste it once per device ("Turn on tap-to-read").  
> **Incident (2026-11-11)**: a rename trashed one identical duplicate ("One Plus One Equals Three - Dave Trott .epub", in Drive trash); tool fixed.

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
- [x] Phase 29: Bold Typography Distinction, Double Spread Default & Mobile Audit Strategy — Injected full 400-800 weight font stylesheets into EPUB.js iframe; defined explicit font-weight: 700 rules for b, strong, and publisher classes (.txbfb, .sgc2); enforced double spread as active default with 640px threshold; drafted mobile optimization audit strategy; bumped SW cache to v14.
- [x] Phase 30: Reading Nook Regular Text Sturdiness & Subpixel Calibration — Enhanced regular serif text weight from thin 400 to sturdy book weight (460) across body and p, bumped default base font size to 18.5px, applied -webkit-font-smoothing: subpixel-antialiased, and calibrated bold contrast to 750 weight; bumped SW cache to v15.
- [x] Phase 31: Mobile Viewport Optimization & Balanced Reading Typography — Calibrated body regular weight to 430 with opsz 18 and bold to 630 semi-bold for golden contrast without ink bloat; implemented adaptive mobile app bar with 44px segmented view switcher; stacked mobile editorial cards with 4-line synopsis clamp; converted mobile dossier to native slide-up bottom sheet with drag handle; enabled EPUB.js portrait single-page fallback (< 640px) with iframe touch turn zones (25% prev, 25% next, 50% toggle chrome) & swipe navigation while preserving solidified laptop layout; bumped SW cache to v16.
- [x] Phase 32: Swapped Metadata Audit & Curated Multi-Category Tagging — Rectified 114 swapped author/title books (Snow Crash, Cryptonomicon, Infinite Jest, Project Hail Mary, etc.); added multi-category support with "Short Stories", "Essays", and "Literary Non-Fiction"; bumped SW cache to v18.
- [x] Phase 33: Craft Card "Steal It" Literary Purge & Polish — Audited all 113 cards in `content/cards.json` to eradicate all corporate, marketing, business, and SaaS jargon in "Steal It" sections; rewrote 22 cards to pure essay/fiction/memoir craft; verified 0 linter flags in `tools/lint_cards.py`.
- [x] Phase 34: Android Cache Invalidation Fix & Release APK Bundle — Fixed `Cards.load` and `QuoteBank.load` cache-delete bug where `assetCards.size >= cachedCards.size` (113 >= 113) purged downloaded cards; replaced with timestamp comparison against APK install time; reduced sync check interval to 15m; compiled signed release APK.
- [x] Phase 35: Bookshelf Drive Sync, Name Cleanup & Code Audit — build now driven by live Drive catalog (fixes new books never appearing: old build returned early on existing data.json); `book_names.json` (Drive-id keyed) fixes all swapped/underscored/Unknown names; `book_overrides.json` replaces 600 lines of hard-coded fixes; template extracted to `scripts/templates/bookshelf.html`; `refresh_bookshelf.sh` + LaunchAgent for daily pickup; Drive rename tool (dry-run). Pushed; LaunchAgent installed. Pending: Drive rename apply.
- [~] Phase 36: Verified Drive renames (455) with history/undo; OCR cover audit; phone book-sheet redesign; tap-to-read via Drive API key; Archive/Restore; local Tidy button.

## File map

- `bookshelf/`: Decoupled, standalone reading shelf web app (**My Reading Corner**) ready for independent git repository (`index.html`, `data.json`).
- **Bookshelf pipeline** (run `bash scripts/refresh_bookshelf.sh [--publish]`):
  - `scripts/sync_drive_catalog.py`: rclone listing of gdrive:Books (path, size, modified, Drive id, mime) → `content/gdrive_books_catalog.json`.
  - `scripts/build_independent_bookshelf_app.py`: catalog + names + overrides + previous data.json → `bookshelf/data.json`, `bookshelf/index.html`, `docs/bookshelf.html`.
  - `scripts/enrich_new_books.py`: verifies parsed names of new books on Open Library, adds cover + synopsis, pins names in book_names.json.
  - `scripts/shelf_common.py`: shared paths, `norm()`, filename → (title, author) parser.
  - `scripts/templates/bookshelf.html`: the web app (plain HTML/JS; `@@TOKENS@@` filled by the build).
  - `content/book_names.json`: **source of truth for every title/author**, keyed by Drive file id. Edit here to fix a name.
  - `content/book_overrides.json`: per-book fixes keyed by shelf id (cover_url, no_cover, pitch, why_love, category, extra_categories).
  - `scripts/rename_drive_files.py`: renames Drive files to "Title - Author.ext" (dry run default, `--apply`, `--undo`; log in `content/drive_rename_log.json`).
  - `scripts/launchd/com.local.reading-corner-refresh.plist`: daily 09:15 refresh + tidy + publish (install command inside).
  - `scripts/launchd/com.local.reading-corner-server.plist`: always-on local helper (http://localhost:8899).
  - `scripts/serve_bookshelf.py`: local helper — serves the shelf, `/api/tidy` (Tidy Drive Names button), `/api/archive`.
  - `scripts/audit_covers.py`: OCR-verifies every cover via local vision server (localhost:9090); `--fix` swaps in verified covers.
  - `content/drive_name_history.json` / `drive_rename_log.json`: original name of every Drive file / every rename (undo trail).
  - `content/cover_audit.md`, `content/drive_rename_review.md`: latest audit reports for manual review.
  - `scripts/migrations/`: one-time scripts that produced book_names.json and the template (history only).
  - `scripts/archive/`: retired bookshelf patch scripts — do not run.
- `scripts/audit_steal_it_marketing.py`: Audits all 113 cards in `content/cards.json` for corporate, marketing, or business jargon.
- `scripts/revise_cards_content.py`: Automation script replacing corporate/marketing jargon in `cards.json` with pure prose craft.
- `scripts/enrich_key_missing_quotes.py`: Curated engine injecting iconic quotes and two-tier companion insights for screenwriting, cinema craft, graphic novels, and literature classics.
- `content/book_metadata_cache.json`: Cache of Open Library works metadata, high-resolution cover IDs, and publisher descriptions.
- `content/covers_cache.json`: Cache of Open Library and custom resolved book cover URLs.
- `content/gdrive_file_ids.json`: Cache of Google Drive file IDs mapping every book to its direct view link (`https://drive.google.com/file/d/{id}/view`).
- `scripts/enrich_covers_and_editorial.py`: Batch engine querying Open Library concurrently for covers and synopses, and injecting four-tier accolades and trivia.
- `content/cards.json`: Single source of truth for all Marginalia craft cards (untouched).
- `content/quote-bank.json`: Structured storage for the master multi-book quote bank (1,882 quotes across 423 books).
- `content/quote-bank.md`: Human-readable quote bank catalog grouped by book.
- `content/authors.md`: Master author library (classic, contemporary, memoir, nonfiction) and their strengths.
- `content/gdrive_books_catalog.json`: Live index of every file under gdrive:Books with Drive ids (regenerated by sync_drive_catalog.py).
- `content/books_curated_shelf.json`: Audited and cleaned dynamic shelf containing 620 high-conviction works with pitches, reader notes, and tags.
- `content/tbr_clean_list.txt`: Clean, 1-click copy-pastable `Title — Author` list of 620 books for TBR trackers.
- `scripts/verify_mobile_and_desktop_audit.py`: Automated 22-rule verification suite for shelf and reader across mobile (375px) and laptop (1440px).
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
- My Reading Corner bookshelf (needs `rclone` remote `gdrive:`; see `~/Documents/Claude Code/Mac Storage/MACHINE.md` before installing anything):
  - Pick up new Drive books + rebuild: `bash scripts/refresh_bookshelf.sh` (add `--publish` to commit shelf files and push)
  - Rebuild only (no network): `python3 scripts/build_independent_bookshelf_app.py`
  - Preview locally: `python3 -m http.server 8899 --directory bookshelf`
  - Fix a wrong title/author: edit `content/book_names.json`, then rebuild
- GitHub sync:
  - Push updates: `git add . && git commit -m "..." && git push origin main`
