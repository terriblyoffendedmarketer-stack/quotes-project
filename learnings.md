# Project learnings

- marketing/SaaS skew across 69 cards | CLAUDE.md and VOICE.md originally prompted cards to target 'a B2B SaaS marketer' and 'ideally on marketing copy' | stripped marketing directives from CLAUDE.md/VOICE.md and systematically rewrote stealIt slides to focus purely on general prose craft, essays, observation, and storytelling
- triad and banned word linter flags during card drafting | lint_cards.py strictly enforces 60-word stealIt limit, bans triads ('X, Y and Z'), and flags adjectives/verbs like 'elevate' | refactored phrasing to paired items and concrete physical verbs
- Ollama gemma3:4b bare list format error | when prompt requested a bare JSON list under format: "json", gemma3:4b returned an empty `{}` | updated prompt to request an explicit JSON root object `{"quotes": [...]}`
- EPUB chapter filter false positives | substring check `skip in low` with `"about"` dropped all chapters of books with "about" in the title (e.g. Murakami's *What I Talk About When I Talk About Running*) | switched to exact stem matching and regex boundary patterns
- Mac sleep halts unattended Ollama mining | macOS power management sleeps system after idle timer during long scripts | invoked background automation via `caffeinate -dimsu` to keep Apple Silicon CPU/GPU awake
- rclone ls path parsing failure | `rclone ls` outputs byte size prefix before file path causing 'directory not found' | parsed clean path via regex `^\s*(\d+)\s+(.+)$`
- EPUB metadata naming mismatches | filenames alternate between Title-Author and Author-Title | parsed authoritative `dc:title` and `dc:creator` tags directly from `content.opf` inside the EPUB zip
