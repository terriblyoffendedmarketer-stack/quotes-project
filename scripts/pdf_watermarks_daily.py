# pdf_watermarks_daily.py — Daily step: checks NEW or CHANGED PDFs on Drive for the OceanofPDF watermark and
#                           cleans them (run by refresh_bookshelf.sh --tidy). Old PDFs are skipped via a cache.
# Usage: python3 scripts/pdf_watermarks_daily.py           # check new/changed PDFs, clean + upload affected ones
#        python3 scripts/pdf_watermarks_daily.py --dry     # check only, change nothing
#        python3 scripts/pdf_watermarks_daily.py --seed    # mark every current PDF as already checked (no downloads)
# Requires: rclone remote gdrive:, uv at /opt/homebrew/bin/uv (creates .cache/pdfenv with pypdf on first need),
#           scripts/scan_pdf_watermarks.py (finder) and scripts/clean_pdf_watermarks.py (cleaner + checks).
#
# Each checked PDF is downloaded to a temp file and deleted afterwards. A cleaned PDF is uploaded over the same
# Drive file (same id; Drive keeps the old version 30 days) only if clean_pdf_watermarks.py's checks pass
# (same pages, same words apart from the watermark, same images, no reference left); otherwise it's listed as
# skipped. Cache: .cache/pdf_watermarks.json (Drive id -> modified time). Log: content/pdf_watermark_log.json.
#
# Gotchas:
# - Seeded on 2026-11-22 from a full scan (167 PDFs, only A Cup of Zen affected and cleaned), so the first
#   daily run doesn't download all 1.7 GB of PDFs again. Delete the cache to force a full re-check.
# - The cleaner knows calibre-made PDFs (link + footer text). An affected PDF it can't prove clean is left
#   untouched and named in the output.

import json
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shelf_common import CATALOG_PATH, CONTENT, ROOT, load_json, save_json  # noqa: E402
from scan_pdf_watermarks import scan  # noqa: E402

STATE = ROOT / ".cache" / "pdf_watermarks.json"
LOG = CONTENT / "pdf_watermark_log.json"
VENV = ROOT / ".cache" / "pdfenv"
UV = "/opt/homebrew/bin/uv"
EXCLUDED = {"Archive of bullshit"}


def ensure_pypdf():
    py = VENV / "bin" / "python"
    if py.exists():
        return str(py)
    subprocess.run([UV, "venv", "-q", str(VENV)], check=True)
    subprocess.run([UV, "pip", "install", "-q", "--python", str(py), "pypdf"], check=True)
    return str(py)


def main():
    args = sys.argv[1:]
    pdfs = [e for e in load_json(CATALOG_PATH, []) if e["ext"] == "pdf" and e["folder"] not in EXCLUDED]
    state = load_json(STATE, {})
    if "--seed" in args:
        for e in pdfs:
            state[e["id"]] = {"modified": e["modified"], "hits": 0, "seeded": True}
        save_json(STATE, state)
        print(f"Seeded {len(pdfs)} PDFs as checked.")
        return
    todo = [e for e in pdfs if state.get(e["id"], {}).get("modified") != e["modified"]]
    print(f"{len(todo)} new/changed PDF(s) to check (of {len(pdfs)}).")
    log = load_json(LOG, [])
    for e in todo:
        src = f"gdrive:Books/{e['path']}"
        with tempfile.TemporaryDirectory() as td:
            local, out = Path(td) / "in.pdf", Path(td) / "out.pdf"
            r = subprocess.run(["rclone", "copyto", src, str(local)], capture_output=True, text=True)
            if r.returncode or not local.exists():
                print(f"  could not download {e['filename']} (will retry next run)")
                continue
            res = scan(local)
            hits = res["uri"] + res["text"] + res["raw"]
            if not hits:
                state[e["id"]] = {"modified": e["modified"], "hits": 0}
                continue
            print(f"  watermark in {e['filename']} ({res['uri']} links, {res['text']} text)")
            if "--dry" in args:
                continue
            c = subprocess.run([ensure_pypdf(), str(ROOT / "scripts" / "clean_pdf_watermarks.py"), str(local), str(out)],
                               capture_output=True, text=True)
            if c.returncode or not out.exists():
                print(f"  SKIP {e['filename']}: cleaner couldn't prove it safe\n    " + c.stdout.strip()[-400:])
                state[e["id"]] = {"modified": e["modified"], "hits": hits, "skipped": True}
                continue
            u = subprocess.run(["rclone", "copyto", str(out), src], capture_output=True, text=True)
            if u.returncode:
                print(f"  FAIL upload {e['filename']}: {u.stderr.strip()[-200:]}")
                continue
            print(f"  cleaned {e['filename']}")
            log.append({"id": e["id"], "path": e["path"], "at": datetime.now().isoformat(timespec="seconds")})
            save_json(LOG, log)
            state[e["id"]] = {"modified": "(cleaned; re-check after next sync)", "hits": 0, "cleaned": True}
        save_json(STATE, state)
    save_json(STATE, state)


if __name__ == "__main__":
    main()
