# What the daily run has already checked

Machine-written records, one entry per Google Drive file id (with its last-changed time where it matters).
The daily refresh (`scripts/refresh_bookshelf.sh`) reads these to skip books it has already handled, and
commits them after every run, so they survive a new Mac. Safe to delete any file: that step just
re-checks everything once (slowly, harmlessly).

- `epub_watermarks.json` — OceanofPDF scan/clean status per EPUB (`scripts/clean_watermarks.py`)
- `pdf_watermarks.json` — same for PDFs (`scripts/pdf_watermarks_daily.py`)
- `covers.json` — cover candidates + visual-match scores per book (`scripts/source_covers.py`)
- `synopsis_verdicts.json` — Claude's right-book/wrong-book verdict per synopsis text (`scripts/check_synopses.py`)

Names already have their own records: `content/book_names.json`, `content/name_confirmed.json`,
`content/drive_name_history.json`.
