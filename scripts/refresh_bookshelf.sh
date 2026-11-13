#!/bin/bash
# scripts/refresh_bookshelf.sh — One command to pick up new Google Drive books and (optionally) publish the shelf
# Usage: bash scripts/refresh_bookshelf.sh                    # sync + build + enrich, local only
#        bash scripts/refresh_bookshelf.sh --tidy             # ...also rename VERIFIED Drive files to "Title - Author"
#        bash scripts/refresh_bookshelf.sh --tidy --publish   # ...then commit the shelf files and push (GitHub Pages)
#        (flags in any order; the daily LaunchAgent and the in-app "Tidy Drive names" button use --tidy --publish)
# Requires: rclone remote `gdrive:`, python3, git with push credentials (osxkeychain). Runs daily via
#           ~/Library/LaunchAgents/com.local.reading-corner-refresh.plist (see scripts/launchd/).
#
# Gotchas:
# - launchd starts with a bare PATH, so /opt/homebrew/bin (rclone) must be added explicitly.
# - --publish stages ONLY the generated shelf/Drive-record files and commits what's staged. If you happen to
#   have other files staged by hand at 09:15 they'd ride along — unlikely, but commit or unstage your own work.
# - --tidy never renames a file whose new name isn't verified (see rename_drive_files.py); held ones are listed
#   in content/drive_rename_review.md.
# - Fixes saved from the app on any device are commits on GitHub (content/book_overrides.json), so the remote
#   is often ahead: it pulls (rebase, autostash) BEFORE building, so those fixes are in this build too.

set -euo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
cd "$(dirname "$0")/.."

echo "=== Reading Corner refresh $(date '+%Y-%m-%d %H:%M') ==="
if [[ " $* " == *" --publish "* ]]; then git pull --rebase --autostash origin main || echo "WARN: git pull failed"; fi
python3 scripts/sync_drive_catalog.py 2>&1 | grep -v "NOTICE: gdrive: This remote uses rclone's shared"
python3 scripts/build_independent_bookshelf_app.py
python3 scripts/enrich_new_books.py
python3 scripts/build_independent_bookshelf_app.py

if [[ " $* " == *" --tidy "* ]]; then
  echo "--- Tidying Drive file names (verified renames only) ---"
  python3 scripts/rename_drive_files.py --apply
  python3 scripts/sync_drive_catalog.py 2>&1 | grep -v "NOTICE: gdrive: This remote uses rclone's shared"
  python3 scripts/build_independent_bookshelf_app.py
fi

if [[ " $* " == *" --publish "* ]]; then
  FILES=(bookshelf/data.json bookshelf/index.html docs/bookshelf.html content/gdrive_books_catalog.json content/book_names.json
         content/drive_name_history.json content/drive_rename_log.json content/drive_rename_review.md content/name_verification_cache.json
         content/book_overrides.json bookshelf/covers docs/covers)
  for f in "${FILES[@]}"; do if [[ -e "$f" ]]; then git add -- "$f"; fi; done
  if git diff --cached --quiet; then
    echo "No shelf changes to publish."
    exit 0
  fi
  COUNT=$(python3 -c "import json;print(len(json.load(open('bookshelf/data.json'))))")
  git commit -m "chore(bookshelf): auto-refresh from Google Drive ($COUNT books)"
  git push origin HEAD || { git pull --rebase --autostash origin main && git push origin HEAD; }
  echo "Published."
fi
