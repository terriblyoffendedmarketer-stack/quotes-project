# scripts/sync_drive_catalog.py — Snapshot every file under gdrive:Books (path, size, modified time, Drive file id, mime type)
# Usage: python3 scripts/sync_drive_catalog.py
# Requires: rclone with a remote named `gdrive:` (read scope is enough), Python 3 standard library
# Output: content/gdrive_books_catalog.json  — consumed by scripts/build_independent_bookshelf_app.py
#
# Gotchas:
# - Key everything by Drive file id, never by filename: ids survive renames/moves, names don't. The old
#   catalog stored only paths, so a renamed file looked like a brand-new book plus a deleted one.
# - rclone `--format pstim` gives path;size;modtime;id;mime. Paths can contain ';'? No — Drive allows it but
#   none of ours do; we split from the RIGHT so a ';' in a filename still parses.
# - The top-level folder "Fiction ／ non fiction" uses a full-width slash (U+FF0F), not '/'.
# - rclone prints a NOTICE about its shared client_id being retired in 2026; when that lands, create your own
#   client id (https://rclone.org/drive/#making-your-own-client-id) and `rclone config reconnect gdrive:`.
# - Refuses to overwrite the catalog with an empty/near-empty listing (auth failure would otherwise wipe the shelf).

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = ROOT / "content" / "gdrive_books_catalog.json"
REMOTE = "gdrive:Books"


def list_drive():
    cmd = ["rclone", "lsf", REMOTE, "--recursive", "--files-only", "--format", "pstim", "--separator", ";"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"rclone failed ({res.returncode}):\n{res.stderr.strip()}")
    files = []
    for line in res.stdout.splitlines():
        if not line.strip():
            continue
        path, size, modified, file_id, mime = line.rsplit(";", 4)
        filename = path.rsplit("/", 1)[-1]
        if filename.startswith("."):
            continue
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        files.append({
            "id": file_id,
            "path": path,
            "filename": filename,
            "folder": path.split("/", 1)[0] if "/" in path else "",
            "ext": ext,
            "mime": mime,
            "size_bytes": int(size) if size.lstrip("-").isdigit() and int(size) >= 0 else 0,
            "modified": modified.replace(" ", "T"),
        })
    return sorted(files, key=lambda f: f["path"])


def main():
    files = list_drive()
    previous = json.loads(OUTPUT_FILE.read_text(encoding="utf-8")) if OUTPUT_FILE.exists() else []
    if len(files) < 0.5 * len(previous):
        sys.exit(f"Refusing to write: Drive returned {len(files)} files vs {len(previous)} last time. Check rclone auth.")
    prev_ids = {f.get("id") for f in previous}
    new = [f for f in files if f["id"] not in prev_ids]
    OUTPUT_FILE.write_text(json.dumps(files, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Drive catalog: {len(files)} files ({len(new)} new since last sync) -> {OUTPUT_FILE.relative_to(ROOT)}")
    for f in new[:50]:
        print(f"  + {f['path']}")


if __name__ == "__main__":
    main()
