# Marginalia

> **Status**: In Progress | **Phase**: 9 (Two-Tier Companion Note Standardization & Gemini Free Tier Pipeline)  
> **Current**: Perfected the companion note prompt specification through rigorous collaborative iteration (1984, Kino, Cat's Cradle). Paragraph 1 grounds the character's psychological defense posture and immediate stakes without decorative filler; Paragraph 2 captures author intent and universal human truth without re-stating plot danger. Prompt saved at `prompts/shelf_explanation_prompt.txt`. Gemini 3.5 Flash Lite pipeline verified on Google AI Studio Free Tier (15 RPM / ₹0 cost).  
> **Next**: Apply the 10 verified test quotes to `content/quote-bank.json`, sync to Android assets, and scale across priority batches.

## Roadmap

- [x] Phase 1: Foundational directives — update CLAUDE.md and VOICE.md to strip out marketing/SaaS slant
- [x] Phase 2: Content audit and revision — rewrite 69 cards in `content/cards.json` to focus on writing craft
- [x] Phase 3: Validation — verify zero flags in `python3 tools/lint_cards.py` and clean `build_prototype.py`
- [x] Phase 4: Curate stronger quotes — add 5 gold-standard cards (Manto, Baldwin, Didion, Dillard, Burkeman) & expand `content/quote-bank.md`
- [x] Phase 5: GitHub synchronization — commit and push updates to `terriblyoffendedmarketer-stack/quotes-project`
- [x] Phase 6: Master Quote Bank mining — extract 800–1,200 quotes across 400+ books using local offline AI without token burnout (Reached 1,871 quotes / 416 books)
- [x] Phase 7: Quote Bank UI & Integration — Thematic horizons web reader, dynamic tag discovery, and dual-mode Android widget integration
- [x] Phase 8: In-App UX Polish, Boundary Fixes & Dostoevsky Trifles Curation (APK release compiled, boundary margins fixed)
- [~] Phase 9: Shelf Quote Explanation Renaissance — Two-tier cognitive standard, zero-spoiler ground truth, and Gemini Free Tier pipeline (Gold standard validated on 10 quotes)

## File map

- `content/cards.json`: Single source of truth for all 108 cards (quote, hook, lookCloser, stealIt, aroundIt).
- `QUOTE_BANK_ARCHITECTURE.md`: Master architectural blueprint for the 800-1,200 quote bank, anti-fatigue UX, and local Ollama pipeline.
- `content/quote-bank.json`: Structured storage for the master multi-book quote bank.
- `content/quote-bank.md`: Human-readable quote bank catalog grouped by book.
- `content/authors.md`: Master author library (classic, contemporary, memoir, nonfiction) and their strengths.
- `scripts/mine_quote_bank.py`: Local extraction engine using Ollama (`gemma3:4b`) to scout literary quotes from EPUBs.
- `scripts/mine_full_library.py`: Continuous automated full-library mining engine with Dublin Core metadata reader and zero-spoiler gating.
- `scripts/harmonize_quote_bank.py`: Harmonization utility ensuring all 1,871 quotes share the unified reading companion schema.
- `scripts/enrich_explanations.py`: Enriches scene explanations with narrative setting and emotional stakes without reductive takeaways.
- `scripts/serve_preview.py`: Zero-install local HTTP preview server for Marginalia Visual Studio in browser.
- `scripts/run_batch.py`: Batch orchestrator to mine clusters of books and output candidate JSON.
- `tools/lint_cards.py`: Linter enforcing word limits, banned AI shapes, triads, and opener variety.
- `tools/build_prototype.py`: Rebuilds the browser review prototype in `prototype/index.html`.
- `tools/sync_quote_bank_md.py`: Synchronizes `content/quote-bank.md` from `content/quote-bank.json`.
- `tools/add_cards.py`: Batch helper to append verified cards without duplicates or broken highlights.
- `scripts/add_dostoevsky_quotes.py`: Curates and updates iconic Dostoevsky passages with 2-tier scene context and philosophical depth.
- `scripts/audit_and_rewrite.py`: Automation script for content audit, rewriting, and testing craft exercises.
- `android/`: Android app and adaptive dual-mode home-screen widget source code.
- `android/marginalia.apk`: Signed release build ready for sideloading.
- `prototype/`: Web-based reader with single-page thematic horizons, instant search, and tag filtering.

## Setup & run instructions

- Python tools require only the Python 3 standard library:
  - Run linter: `python3 tools/lint_cards.py`
  - Rebuild web prototype: `python3 tools/build_prototype.py`
- GitHub sync:
  - Push updates: `git add . && git commit -m "..." && git push origin main`
  - The Android app auto-downloads `content/cards.json` from the GitHub repo every few hours.

## Key decisions & content rules

- **Focus**: Pure writing craft, personal essays, storytelling, observation, and prose rhythm. Never pivot to marketing, SaaS, corporate, or sales jargon.
- **Android, always**: Home-screen widget + full-screen reader. Slides drawn directly into widget views (no StackView or RemoteViewsService adapters).
- **JSON backwards compatibility**: `content/cards.json` is fetched by live app installs. Adding fields is fine; renaming or deleting fields breaks installed apps.
- **Slide structure**:
  1. *How to (Hook)*: The job, as large as it fits, plus author name.
  2. *The line*: The quote (punchy one-liner or passage up to ~120 words). Passes the cold-reader test.
  3. *Look closer*: The unexpected craft angle (close reading, structural move, dead metaphor, or scene).
  4. *Steal it*: One concrete writing exercise under 60 words for essays, articles, or prose. No SaaS/marketing.
  5. *Around it*: True contextual/biographical facts ending on an open question. Under 100 words.
- **Verification**: Every quote verified against published text. Name translator for translated works.
- **Oliver Burkeman**: Owner's favourite book is *Four Thousand Weeks*. Burkeman cards are prime models for working passages.
