#!/bin/bash
# scripts/refresh_bookshelf.sh — One command to pick up new Google Drive books and (optionally) publish the shelf
# Usage: bash scripts/refresh_bookshelf.sh            # sync + build + enrich, local only
#        bash scripts/refresh_bookshelf.sh --publish  # ...then commit the shelf files and push (GitHub Pages)
# Requires: rclone remote `gdrive:`, python3, git with push credentials (osxkeychain). Runs daily via
#           ~/Library/LaunchAgents/com.local.reading-corner-refresh.plist (see scripts/launchd/).
#
# Gotchas:
# - launchd starts with a bare PATH, so /opt/homebrew/bin (rclone) must be added explicitly.
# - --publish commits ONLY the generated shelf files (pathspec commit), never other work in progress, and
#   skips the commit entirely when nothing changed.
# - If the push is rejected (remote ahead), it leaves the local commit in place and exits non-zero; run
#   `git pull --rebase && git push` by hand.

set -euo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
cd "$(dirname "$0")/.."

echo "=== Reading Corner refresh $(date '+%Y-%m-%d %H:%M') ==="
python3 scripts/sync_drive_catalog.py 2>&1 | grep -v "NOTICE: gdrive: This remote uses rclone's shared"
python3 scripts/build_independent_bookshelf_app.py
python3 scripts/enrich_new_books.py
python3 scripts/build_independent_bookshelf_app.py

if [[ "${1:-}" == "--publish" ]]; then
  FILES=(bookshelf/data.json bookshelf/index.html docs/bookshelf.html content/gdrive_books_catalog.json content/book_names.json)
  if git diff --quiet -- "${FILES[@]}"; then
    echo "No shelf changes to publish."
    exit 0
  fi
  COUNT=$(python3 -c "import json;print(len(json.load(open('bookshelf/data.json'))))")
  git commit -m "chore(bookshelf): auto-refresh from Google Drive ($COUNT books)" -- "${FILES[@]}"
  git push origin HEAD
  echo "Published."
fi
