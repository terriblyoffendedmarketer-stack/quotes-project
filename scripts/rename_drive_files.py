# scripts/rename_drive_files.py — Renames book files on Google Drive to a clean "Title - Author.ext" convention
# Usage: python3 scripts/rename_drive_files.py            # DRY RUN: prints the plan, changes nothing
#        python3 scripts/rename_drive_files.py --apply    # renames on Drive (same folder), logs every change
#        python3 scripts/rename_drive_files.py --undo     # reverts everything in content/drive_rename_log.json
# Requires: rclone remote `gdrive:` with FULL drive scope (read-only scope fails with 403
#           ACCESS_TOKEN_SCOPE_INSUFFICIENT — fix with `rclone config reconnect gdrive:` choosing scope "drive"),
#           a fresh content/gdrive_books_catalog.json (run scripts/sync_drive_catalog.py first), content/book_names.json
#
# Gotchas:
# - Safe for the shelf: the bookshelf keys every book by Drive file id, and renames keep the id. Re-run
#   sync_drive_catalog.py afterwards so the catalog shows the new names.
# - Only files listed in book_names.json are touched; series folders (Watchmen issues, Punpun volumes),
#   the archive folder and non-book files are left alone.
# - Characters that break desktop sync (/ \ : * ? " < > |) are removed; a subtitle colon becomes an en dash
#   ("Title – Subtitle - Author") so the " - " before the author stays unambiguous.
# - Two files that would get the same name in one folder get " (2)" appended instead of clobbering.

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shelf_common import CATALOG_PATH, CONTENT, NAMES_PATH, load_json, save_json  # noqa: E402

LOG_PATH = CONTENT / "drive_rename_log.json"
REMOTE = "gdrive:Books"
SKIP_FOLDERS = {"Archive of bullshit"}


def clean_filename(title, author, ext):
    def fix(s):
        s = s.replace(": ", " – ").replace(":", " – ").replace("/", "-")
        s = re.sub(r'[\\*?"<>|]', "", s)
        return re.sub(r"\s+", " ", s).strip(" .")
    name = fix(title) if author in ("Anonymous", "Various Authors", "Unknown", "") else f"{fix(title)} - {fix(author)}"
    return f"{name[:180]}.{ext}" if ext else name[:180]


def plan():
    catalog = load_json(CATALOG_PATH, [])
    names = load_json(NAMES_PATH, {})
    moves, taken = [], {}
    for f in catalog:
        if f["folder"] in SKIP_FOLDERS or f["id"] not in names or len(f["path"].split("/")) > 2:
            continue
        n = names[f["id"]]
        folder = f["path"].rsplit("/", 1)[0] if "/" in f["path"] else ""
        new = clean_filename(n["title"], n["author"], f["ext"] if f["ext"] in {"epub", "pdf", "cbr", "cbz", "mobi"} else "")
        stem, dot, ext = new.rpartition(".") if "." in new else (new, "", "")
        k, i = (folder, new.lower()), 2
        while k in taken and taken[k] != f["id"]:
            new = f"{stem} ({i}){dot}{ext}"
            k, i = (folder, new.lower()), i + 1
        taken[k] = f["id"]
        if new != f["filename"]:
            moves.append({"id": f["id"], "from": f["path"], "to": f"{folder}/{new}" if folder else new})
    return moves


def rclone_move(src, dst):
    r = subprocess.run(["rclone", "moveto", f"{REMOTE}/{src}", f"{REMOTE}/{dst}"], capture_output=True, text=True)
    return r.returncode == 0, r.stderr.strip().splitlines()[-1:] if r.returncode else ""


def main():
    if "--undo" in sys.argv:
        log = load_json(LOG_PATH, [])
        for m in reversed(log):
            ok, err = rclone_move(m["to"], m["from"])
            print(("undo " if ok else "FAIL ") + f"{m['to']} -> {m['from']} {err or ''}")
        return
    moves = plan()
    for m in moves:
        print(f"{m['from']}\n    -> {m['to'].rsplit('/', 1)[-1]}")
    print(f"\n{len(moves)} file(s) would be renamed.")
    if "--apply" not in sys.argv:
        print("Dry run only. Re-run with --apply to rename on Google Drive.")
        return
    log = load_json(LOG_PATH, [])
    for m in moves:
        ok, err = rclone_move(m["from"], m["to"])
        print(("ok   " if ok else "FAIL ") + m["to"] + (f"  {err}" if err else ""))
        if ok:
            log.append({**m, "at": datetime.now().isoformat(timespec="seconds")})
            save_json(LOG_PATH, log)   # save after every move so a crash never loses the undo trail
    print("Now run: python3 scripts/sync_drive_catalog.py")


if __name__ == "__main__":
    main()
