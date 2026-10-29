# Quote Bank & Reading Companion: Master Specification Document

> **Grounding Truth**: This document serves as the canonical specification for the **Quote Bank** expansion of Marginalia. It defines the distinction between the original Craft Widget and the Library Quote Bank, establishes the UX architecture, specifies the data schema, and details the unified widget integration.

---

## 1. Core Vision & The Two Distinct Products

The project consists of two complementary but distinct products designed for different moments and purposes:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MARGINALIA ECOSYSTEM                            │
├───────────────────────────────────┬────────────────────────────────────┤
│ PRODUCT 1: THE CRAFT WIDGET       │ PRODUCT 2: THE LIBRARY QUOTE BANK  │
│ (`content/cards.json` — 108 cards)│ (`content/quote-bank.json` — ~1.5k)│
├───────────────────────────────────┼────────────────────────────────────┤
│ • Goal: Daily writing technique   │ • Goal: Full personal library      │
│ • Audience: Daily phone glance    │   coverage (~392 EPUBs)            │
│ • Mindset: "How great prose works"│ • Mindset: "Why I own this book    │
│ • Structure: Strict 5-slide deck  │   and must read it tonight"        │
│   (`job`, `lookCloser`, `stealIt`,│ • Structure: Pure arresting prose  │
│   `aroundIt`)                     │   + plain-English scene context    │
│ • Constraints: Max 60-word        │ • Constraints: Room to breathe     │
│   exercises, writing hooks        │   (1–5 sentences), zero spoilers   │
└───────────────────────────────────┴────────────────────────────────────┘
```

### The Separation Rule
- **Never force the Quote Bank into the Craft Widget framework.** Quote Bank entries do not need "How to..." craft hooks, copywriting exercises, or marketing analysis.
- **Never force quotes into reductive self-help or corporate life advice.** Literature loses its magic when an AI turns a chilling line from Stephen King or a philosophical observation from Tolstoy into a generic "actionable takeaway." The Quote Bank is an invitation to read literature, not an executive coaching summary.

---

## 2. The Quote Bank Schema: Natural Reading Companion

Each entry in `content/quote-bank.json` is clean, lightweight, and focused on reader delight:

```json
{
  "id": "project-hail-mary-01",
  "quote": "‘It must be your decision,’ said Stratt. ‘I will not have someone on my crew who is there against their will. You must come of your own volition.’",
  "work": "Project Hail Mary",
  "author": "Andy Weir",
  "year": 2021,
  "explanation": "Eva Stratt has total global authority to draft anyone on Earth for a desperate suicide mission to save humanity from an extinction-level solar parasite. Yet she refuses to force the protagonist at gunpoint: she knows that when a human is locked in a tin can millions of miles from Earth with zero hope of return, conscription fails. They have to have chosen it themselves.",
  "tags": [
    "high-stakes",
    "isolation",
    "willpower"
  ]
}
```

### Schema Field Rules
1. **`quote`**: 1 to 5 sentences (up to ~120 words). Must pass the **cold-reader test** (intriguing on its own to someone who has never touched the book).
2. **`work` & `author`**: Authoritative Dublin Core metadata extracted directly from the EPUB's `content.opf`.
3. **`explanation`**: 2–3 plain-English sentences providing the dramatic or thematic context of the scene without spoiling key plot climaxes. Answers: *What is actually happening here, and why does this moment land with such force?*
4. **`tags`**: Rich thematic descriptors (see Section 3).

---

## 3. UX Architecture: High Visibility, Anti-Overwhelm

A flat, unorganized dump of 1,500 quotes causes scrolling paralysis. However, nested folders prohibit visibility and bury gems. The UX balances discoverability, thematic depth, and calm reading.

### A. The "No-Folders" Rule (Continuous Thematic Plane)
- **Zero Nested Folders**: Content is never buried inside submenus, folders, or modal trees.
- **Thematic Separators on a Single Page**: The reader browses a continuous, fluid surface divided by rich thematic horizons with sticky or inline section dividers.

### B. Rich Thematic Horizons (Beyond "Funny / Informational")
Quotes are grouped into evocative emotional and intellectual atmospheres:
- **Human Folly & Social Pretense**: Satire, vanity, hypocrisy, and the absurd comedies of manners.
- **Atmospheric Dread & The Uncanny**: Slow-burning tension, ominous landscapes, and quiet psychological chills.
- **Solitude, Stillness & Finitude**: Time slipping away, quiet rooms, mortality, and the ache of memory.
- **High Stakes & Moral Friction**: Crises of conscience, impossible choices, and humans under existential pressure.
- **Sharp Bites of Irony**: Cynicism, dry wit, devastating understatements, and paradoxical truths.
- **The Machinery of Power & History**: The sweep of empires, ideological madness, institutional rot, and collective human scale.

### C. Search & Interactive Tag Exploration
- **Instant Global Search**: Real-time query matching across quote text, author names, and book titles.
- **Dynamic Tag Filtering**: Tapping any tag pill (e.g. `#solitude`, `#grim-humor`, `#cosmic-scale`) dynamically filters the continuous view to show related quotes across the entire library instantly—without page reloads, navigation redirects, or losing the user's reading position.

### D. Reading Cadence (Anti-Doomscroll Philosophy)
The UX is designed to foster unhurried contemplation rather than mindless vertical flicking:
- **The Daily Library Spark**: A featured single quote of the day drawn from the unread library, presented in elegant typography with its context note.
- **"Spark: Read this book next"**: A one-tap bookmarking action that pins the book to a personal "Read Next" shelf, directly solving the "forgotten library" problem.

---

## 4. Unified Android Home-Screen Widget (Dual-Mode)

### The Aesthetic Challenge
Having multiple large widgets for related reading material clutters the home screen and degrades the minimalist aesthetic of the phone.

### The Solution: One Adaptive Widget with an In-Place Mode Toggle
A single 4×2 or 4×3 Android home-screen widget powered by Jetpack Compose / Glance:

```
┌───────────────────────────────────────────────────────────┐
│ MARGINALIA                         [ ⇄ Mode: Shelf Spark ]│
├───────────────────────────────────────────────────────────┤
│                                                           │
│  “‘It must be your decision,’ said Stratt.                │
│   ‘I will not have someone on my crew who is              │
│   there against their will.’”                             │
│                                                           │
│  — Project Hail Mary (Andy Weir)                          │
│                                                           │
│  Stratt has absolute legal authority to conscript anyone  │
│  on Earth, but recognizes deep-space suicide missions     │
│  break anyone who didn't choose the burden freely.        │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### Toggle Mechanics:
1. **Mode 1: The Craft Daily (Marginalia)**:
   - Displays the daily card from `content/cards.json`.
   - Focus: Sentence craft, writing techniques, and the 5-slide reader.
2. **Mode 2: The Shelf Spark (Quote Bank)**:
   - Displays a daily rotating passage from `content/quote-bank.json`.
   - Focus: Pure literary voice + the plain-English scene explanation to inspire the user to open that book today.
3. **Interactive Flip**:
   - A discreet mode-switch icon in the widget header (`[ ⇄ ]`) allows the user to tap and instantly toggle between the Craft Card and the Shelf Spark directly on the home screen.
   - State persists across widget updates without requiring app launch.

---

## 5. Mining Engine & Guardrails

The automated library mining engine ([`scripts/mine_full_library.py`](file:///Users/apple/Documents/Claude%20Code/quotes-project/scripts/mine_full_library.py)) runs locally to achieve 100% full-library coverage across all ~392 personal EPUBs:

1. **Zero API Cost**: 100% offline local inference via Ollama (`gemma3:4b`) using Apple Silicon Metal acceleration.
2. **Strict Zero-Spoiler Gate**: Evaluates chapters exclusively from the first 85% of each book, strictly ignoring climax, reveal, and conclusion files.
3. **Dublin Core Authenticity**: Reads `dc:title` and `dc:creator` directly from the EPUB's `content.opf` zip stream to avoid filename inversion bugs.
4. **Mac Sleep Prevention**: Executed under `caffeinate -dimsu` to ensure uninterrupted multi-hour processing without system sleep.
5. **Disk Space Hygiene**: Scratch EPUBs are unlinked in a `finally:` block immediately after chapter extraction, maintaining free disk space well above the 20 GB safety floor.
