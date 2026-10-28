# Quote Bank Architecture & Expansion Master Plan

This document establishes the architecture for expanding Marginalia from a daily 100-card widget into an unhurried discovery engine for the owner's personal 400+ book library, mitigating choice fatigue and avoiding API token constraints.

---

## 1. Core Vision

- **Rekindle Reading Hunger**: The user has hundreds of books downloaded with enthusiasm that sit unread. The Quote Bank extracts the most arresting lines from each book to showcase why it was collected and trigger the impulse: *"I want to open this book tonight."*
- **Target Scale**: ~400+ books at 2–5 quotes each = **800 to 1,200 curated quotes**.
- **No Compromise on Quality**: Every line must pass the **cold-reader test** (intriguing on its own, without requiring plot context).

---

## 2. The Two-Part Architecture

### Part A: The Master Quote Bank (Repository Layer)
- **`content/quote-bank.json`**: Machine-readable single source of truth containing every quote, author, work, year, translator, hook/job, emotional justification, and source file.
- **`content/quote-bank.md`**: Human-readable catalog grouped by author/book.
- **No Heavy Parsing Required**: Unlike full Marginalia cards, entries in the Quote Bank do not require full 5-slide breakdowns (`lookCloser`, `stealIt`, `aroundIt`). They store the pure quote, attribution, and a 1-line hook/job.
- **The Graduation Pipeline**: Over time, the top ~100 quotes from the Bank get selected, given full research dossiers, and graduated into `content/cards.json` for the Android widget.

### Part B: The UX Design for 1,000+ Quotes (Anti-Overwhelm System)
A flat list of 1,000 items creates scrolling paralysis and choice fatigue. The app and prototype UX will solve this with 4 core mechanisms:

1. **The Serendipity Shuffle (One Card at a Time)**:
   - Opening the Quote Bank does not present a giant wall of text.
   - It displays **one single surprise quote** drawn from the library, framed with:
     - The Book & Author
     - The Quote (set beautifully in Literata)
     - *"Why this book is on your shelf"* (the hook)
   - A single primary action: **"Surprise Me"** (or swipe) to flip to another book.
2. **The "Want to Read Next" Spark Queue**:
   - Each quote card features a bookmark button: **“Spark: Read this book next”**.
   - Tapping it saves the book into an active personal reading queue, solving the "forgotten library" problem.
3. **The Digital Bookshelf (Grouped by Work)**:
   - For structured browsing, the user sees an alphabetical bookshelf grid of book titles, not loose quotes. Tapping a title opens only its 2–5 quotes.
4. **The 5 Emotional & Craft Moods**:
   - *Sensory Shock & Observation*
   - *Time, Finitude & Mortality*
   - *Grief, Love & Longing*
   - *Absurdity & Dark Humor*
   - *Pristine Prose & Rhythm*

---

## 3. The Extraction & Mining Pipeline (Zero-Cost Scale)

To avoid burning API tokens or hitting context window limits when parsing 400+ full-length books, mining uses a **Supervisor-Worker architecture**:

```
[ Google Drive (via rclone) ]
              │
              ▼
1. Local Orchestrator (`scripts/mine_quote_bank.py`)
   • Downloads EPUBs on demand to isolated scratch storage.
   • Cleans chapters into manageable 1,000–1,500 word narrative blocks.
              │
              ▼
2. Worker Agent: Local Ollama `gemma3:4b` (Offline, Metal-Accelerated, Zero Tokens)
   • Reads the text with actual literary comprehension.
   • Extracts 4–8 candidate quotes per book with stylistic justification.
              │
              ▼
3. Supervisor Agent: Antigravity / Claude (Taste, Quality Control & Taxonomy)
   • Enforces the cold-reader test from VOICE.md.
   • Refines the "How to..." craft hook.
   • Determines volume: 2–3 quotes for concise works; 5–8 quotes for dense masterpieces.
              │
              ▼
4. Master Storage (`content/quote-bank.json` & `content/quote-bank.md`)
   • Appends clean, verified entries ready for the reader app.
```

---

## 4. Execution Roadmap

- [ ] **Phase 1: Proof of Concept & Tooling**
  - Verify local `gemma3:4b` extraction pipeline on a test batch (*Men Without Women*, *A Short Stay in Hell*).
  - Review sample output and tune extraction prompts.
- [ ] **Phase 2: Systematic Mining Runs (Clusters 1 to 15)**
  - Group ~400 clean books into 15 thematic clusters (25 books each).
  - Execute mining pass per cluster, yielding ~60–80 quotes per run.
- [ ] **Phase 3: Prototype & App Integration**
  - Wire `content/quote-bank.json` into `prototype/index.html` with the Serendipity Shuffle and Bookshelf view.
  - Implement Quote Bank activity/screen in Android app (`android/`).
- [ ] **Phase 4: Card Graduation**
  - Select standout candidates from the Bank for full 5-slide card authoring into `content/cards.json`.
