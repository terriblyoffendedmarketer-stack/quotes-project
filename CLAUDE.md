# Marginalia

> **Status**: Complete | **Phase**: 12 (Library Audit, Bullshit Purge & Strict Attribution)  
> **Current**: Strict title/author audit completed. Fixed quote-bank loose substring match bug (preventing "Foundations of Screenwriting" from being mislabeled as Asimov's "Foundation", restored Nora Ephron's "Heartburn", Tony Fadell's "Build", and Laura Harvey's "Class"). Purged 30 tactical hustle brochures, cold email templates, and lead magnets from active shelf and TBR lists. Prepared automated Google Drive reorganization script (`scripts/move_drive_files.sh`).  
> **Next**: Ready for reading discovery with clean literary attribution.

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

## File map

- `content/cards.json`: Single source of truth for all 108 cards (quote, hook, lookCloser, stealIt, aroundIt).
- `QUOTE_BANK_ARCHITECTURE.md`: Master architectural blueprint for the 800-1,200 quote bank, anti-fatigue UX, and local Ollama pipeline.
- `content/quote-bank.json`: Structured storage for the master multi-book quote bank (1,882 quotes across 423 books).
- `content/quote-bank.md`: Human-readable quote bank catalog grouped by book.
- `content/authors.md`: Master author library (classic, contemporary, memoir, nonfiction) and their strengths.
- `content/gdrive_books_catalog.json`: Raw index of all 676 book files across Google Drive with paths and sizes.
- `content/books_curated_shelf.json`: Audited and cleaned dynamic shelf containing 620 high-conviction works with pitches, reader notes, and tags.
- `content/tbr_clean_list.txt`: Clean, 1-click copy-pastable `Title — Author` list of 620 books for TBR trackers.
- `scripts/fetch_all_gdrive_books.py`: Rclone drive indexing script scanning `gdrive:Books` recursively.
- `scripts/build_dynamic_bookshelf.py`: Compiles, normalizes, and enriches drive catalog into interactive shelf web app.
- `scripts/reorganize_drive_and_audit_library.py`: Strict title verification, tactical fluff purging, and move script generator.
- `scripts/move_drive_files.sh`: Shell script to move 30 tactical lead magnets to `Books/Archive of bullshit` and HBR books to `Books/HBR`.
- `prototype/shelf.html` & `docs/shelf.html`: Interactive dynamic shelf and "What Should I Read Next?" recommender.
- `scripts/mine_quote_bank.py`: Local extraction engine using Ollama (`gemma3:4b`) to scout literary quotes from EPUBs.
- `scripts/mine_full_library.py`: Continuous automated full-library mining engine with Dublin Core metadata reader and zero-spoiler gating.
- `scripts/harmonize_quote_bank.py`: Harmonization utility ensuring all 1,871 quotes share the unified reading companion schema.
- `scripts/enrich_explanations.py`: Enriches scene explanations with narrative setting and emotional stakes without reductive takeaways.
- `scripts/enrich_with_claude.py`: Claude API (`claude-haiku-4-5-20251001`) enrichment engine generating 2-tier companion notes.
- `scripts/update_three_body_explanations.py`: Dedicated updater for deep 2-tier companion notes on The Three-Body Problem shelf quotes.
- `scripts/serve_preview.py`: Zero-install local HTTP preview server for Marginalia Visual Studio in browser.
- `scripts/run_batch.py`: Batch orchestrator to mine clusters of books and output candidate JSON.
- `tools/lint_cards.py`: Linter enforcing word limits, banned AI shapes, triads, and opener variety.
- `tools/build_prototype.py`: Rebuilds the browser review prototype in `prototype/index.html`.
- `tools/sync_quote_bank_md.py`: Synchronizes `content/quote-bank.md` from `content/quote-bank.json`.
- `tools/add_cards.py`: Batch helper to append verified cards without duplicates or broken highlights.
- `scripts/add_dostoevsky_quotes.py`: Curates and updates iconic Dostoevsky passages with 2-tier scene context and philosophical depth.
- `scripts/audit_and_rewrite.py`: Automation script for content audit, rewriting, and testing craft exercises.
- `android/`: Android app and adaptive dual-mode home-screen widget source code.
- `android/app/src/main/java/com/marginalia/QuoteCardAdapter.kt`: RecyclerView adapter for the Android Library stream with expandable notes and tags.
- `android/marginalia.apk`: Signed release build ready for sideloading.
- `prototype/`: Web-based reader with single-page thematic horizons, instant search, and tag filtering.

## Setup & run instructions

- Python tools require only the Python 3 standard library:
  - Run linter: `python3 tools/lint_cards.py`
  - Rebuild web prototype: `python3 tools/build_prototype.py`
  - Rebuild dynamic bookshelf & TBR list: `python3 scripts/build_dynamic_bookshelf.py`
  - Run audit & clean pass: `python3 scripts/reorganize_drive_and_audit_library.py`
- GitHub sync:
  - Push updates: `git add . && git commit -m "..." && git push origin main`
  - The Android app auto-downloads `content/cards.json` from the GitHub repo every few hours.

## Key decisions & content rules

- **Focus**: Pure writing craft, personal essays, storytelling, observation, and prose rhythm. Never pivot to marketing, SaaS, corporate, or sales jargon.
- **Android, always**: Home-screen widget + full-screen reader. Slides drawn directly into widget views (no StackView or RemoteViewsService adapters).
- **JSON backwards compatibility**: `content/cards.json` is fetched by live app installs. Adding fields is fine; renaming or deleting fields breaks installed apps.
- **Verification**: Every quote verified against published text. Name translator for translated works.
- **Oliver Burkeman**: Owner's favourite book is *Four Thousand Weeks*. Burkeman cards are prime models for working passages.
