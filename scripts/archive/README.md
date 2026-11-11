# scripts/archive — retired one-off scripts (kept for history, do NOT run)

These patched the old bookshelf build script or its generated HTML with regex edits (Phases 18–33), or
fetched the old path-only Drive catalog. Since 2026-11-11 the HTML lives in `scripts/templates/bookshelf.html`
and the build is driven by `scripts/refresh_bookshelf.sh`, so re-running any of these would corrupt it.
Their effects are already baked into the template / `content/book_names.json` / `content/book_overrides.json`.
