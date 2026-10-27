# Marginalia

> **Status**: Complete | **Phase**: 5 (GitHub Synchronization)  
> **Current**: Successfully audited, purged all corporate/marketing/SaaS skew from cards, populated 5 new high-caliber cards (108 total), verified with linter and prototype builder, and synced to GitHub  
> **Next**: Ready for daily widget consumption and future author additions

## Roadmap

- [x] Phase 1: Foundational directives — update CLAUDE.md and VOICE.md to strip out marketing/SaaS slant
- [x] Phase 2: Content audit and revision — rewrite 69 cards in `content/cards.json` to focus on writing craft
- [x] Phase 3: Validation — verify zero flags in `python3 tools/lint_cards.py` and clean `build_prototype.py`
- [x] Phase 4: Curate stronger quotes — add 5 gold-standard cards (Manto, Baldwin, Didion, Dillard, Burkeman) & expand `content/quote-bank.md`
- [x] Phase 5: GitHub synchronization — commit and push updates to `terriblyoffendedmarketer-stack/quotes-project`

## File map

- `content/cards.json`: Single source of truth for all 108 cards (quote, hook, lookCloser, stealIt, aroundIt).
- `content/VOICE.md`: Core writing and tone rules for drafting cards without AI tropes or corporate jargon.
- `content/authors.md`: Master author library (classic, contemporary, memoir, nonfiction) and their strengths.
- `content/quote-bank.md`: Staging area for verified quotes and research dossiers waiting for card creation.
- `tools/lint_cards.py`: Linter enforcing word limits, banned AI shapes, triads, and opener variety.
- `tools/build_prototype.py`: Rebuilds the browser review prototype in `prototype/index.html`.
- `tools/add_cards.py`: Batch helper to append verified cards without duplicates or broken highlights.
- `scripts/audit_and_rewrite.py`: Automation script for content audit, rewriting, and testing craft exercises.
- `android/`: Android app and home-screen widget source code (Kotlin / Jetpack Compose).
- `prototype/`: Web-based card previewer for rapid visual review.

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
