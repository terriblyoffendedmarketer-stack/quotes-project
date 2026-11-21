#!/bin/bash
# scripts/refresh_bookshelf.sh — One command to pick up new Google Drive books and (optionally) publish the shelf
# Usage: bash scripts/refresh_bookshelf.sh                    # sync + build + enrich, local only
#        bash scripts/refresh_bookshelf.sh --tidy             # ...also rename VERIFIED Drive files to "Title - Author"
#                                                             #    and strip OceanofPDF watermarks from new EPUBs + PDFs
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
# - Only one run at a time (lock in .cache/refresh.lock); a second start exits quietly.
# - The Drive list is re-read after renames, before the watermark cleaners download files by path.
# - Waits up to 30 min for the network first: launchd fires it right after wake, often before Wi-Fi is up.

set -euo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
cd "$(dirname "$0")/.."

echo "=== Reading Corner refresh $(date '+%Y-%m-%d %H:%M') ==="
# One run at a time: the 09:15 job, the in-app Tidy button and manual runs all use this script.
# mkdir is atomic; a lock left by a crashed run (its process gone) is taken over.
LOCK=".cache/refresh.lock"
mkdir -p .cache
if ! mkdir "$LOCK" 2>/dev/null; then
  OLD=$(cat "$LOCK/pid" 2>/dev/null || echo "")
  if [[ -n "$OLD" ]] && kill -0 "$OLD" 2>/dev/null; then
    echo "Another refresh is already running (pid $OLD) - not starting a second one."
    exit 0
  fi
  echo "Removing a stale lock from a run that didn't finish."
  rm -rf "$LOCK"; mkdir "$LOCK"
fi
echo $$ > "$LOCK/pid"
trap 'rm -rf "$LOCK"' EXIT
# The Mac often runs this right after waking, before Wi-Fi is back (Nov 18-20: "Could not resolve host").
# Wait up to 30 min for DNS instead of failing the whole day.
for i in $(seq 1 60); do
  if /usr/bin/host -W 3 www.googleapis.com >/dev/null 2>&1; then break; fi
  [[ $i == 1 ]] && echo "Waiting for the internet..."
  sleep 30
done
if [[ " $* " == *" --publish "* ]]; then git pull --rebase --autostash origin main || echo "WARN: git pull failed"; fi
python3 scripts/sync_drive_catalog.py 2>&1 | grep -v "NOTICE: gdrive: This remote uses rclone's shared"
python3 scripts/build_independent_bookshelf_app.py
python3 scripts/enrich_new_books.py
python3 scripts/build_independent_bookshelf_app.py
# Covers checked against each new book file's own cover, and synopses checked for wrong-book text.
# Both cache per book, so only new books cost time (synopsis check: a few cents of Claude API per run).
python3 scripts/source_covers.py --apply >/dev/null 2>&1 || echo "WARN: cover sourcing failed"
python3 scripts/check_synopses.py --apply 2>&1 | tail -1 || echo "WARN: synopsis check failed"
python3 scripts/build_independent_bookshelf_app.py

if [[ " $* " == *" --tidy "* ]]; then
  echo "--- Tidying Drive file names (verified renames only) ---"
  python3 scripts/rename_drive_files.py --apply
  # Renames change file paths: re-read Drive BEFORE the cleaners download by path.
  python3 scripts/sync_drive_catalog.py 2>&1 | grep -v "NOTICE: gdrive: This remote uses rclone's shared"
  echo "--- Removing OceanofPDF watermarks from new/changed EPUBs ---"
  python3 scripts/clean_watermarks.py --apply || echo "WARN: watermark cleanup failed"
  python3 scripts/pdf_watermarks_daily.py || echo "WARN: PDF watermark check failed"
  python3 scripts/sync_drive_catalog.py 2>&1 | grep -v "NOTICE: gdrive: This remote uses rclone's shared"
  python3 scripts/build_independent_bookshelf_app.py
fi

if [[ " $* " == *" --publish "* ]]; then
  FILES=(bookshelf/data.json bookshelf/index.html docs/bookshelf.html content/gdrive_books_catalog.json content/book_names.json
         content/drive_name_history.json content/drive_rename_log.json content/drive_rename_review.md content/name_verification_cache.json
         content/book_overrides.json bookshelf/covers docs/covers content/watermark_scan.md content/watermark_log.json content/pdf_watermark_log.json
         content/cover_sourcing.json content/cover_sourcing.md content/synopsis_check.md content/name_confirmed.json
         content/state content/epub_metadata_log.json)
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
