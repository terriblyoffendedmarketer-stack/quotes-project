# clean_watermarks.py — Removes the "OceanofPDF.com" watermark from the EPUBs on Google Drive (plain code, no AI)
# Usage: python3 scripts/clean_watermarks.py                  # SCAN only: which EPUBs have it -> content/watermark_scan.md
#        python3 scripts/clean_watermarks.py --apply --limit 3 # clean 3 books (smoke test), upload over the same Drive file
#        python3 scripts/clean_watermarks.py --apply           # clean every affected EPUB
#        python3 scripts/clean_watermarks.py --only "<title words>" [--apply]
#        python3 scripts/clean_watermarks.py --dry-clean <file.epub>   # clean a LOCAL copy, report, no upload
# Requires: rclone remote gdrive: (full scope), Python 3 stdlib. Rebuild nothing: Drive ids don't change.
#
# What it removes (only these; every other byte of the book is copied as is):
#   - <a href="...oceanofpdf...">…</a> links, and paragraphs/divs/spans whose only text is the watermark
#   - any leftover "OceanofPDF.com" / "www.oceanofpdf.com" text, plus "Downloaded from" leftovers
# Safety (deterministic, on EVERY book; any failure = book skipped and listed, never uploaded):
#   - word-by-word diff of every page: the only change allowed is DELETING watermark words ("OceanofPDF.com",
#     "Downloaded from"...). Any other word lost, added, changed or moved -> skip. So nothing can shift order.
#   - same link targets (ids), same images in the same order, same headings, same number of page breaks
#   - elements carrying an id or a page break are never deleted, only emptied (layout stays put)
#   - every file that had no watermark (images, fonts, other chapters) is byte-for-byte identical
#   - still unzips, same file list, XHTML that parsed before still parses, no watermark left. Otherwise it's skipped and listed. Drive keeps the previous version of every file for
#   30 days (right-click > Manage versions), and the upload updates the SAME file, so shelf links, ids and
#   reading positions are unaffected. Log of every cleaned file: content/watermark_log.json.
#
# Gotchas:
# - The mimetype entry must stay first and STORED (uncompressed) or readers reject the EPUB.
# - Don't regex-strip whole tags across the file: books nest <span>s; only innermost elements whose text is
#   watermark-only are removed (repeated until nothing changes).
# - No local backups of originals: this Mac must keep >20 GB free. Drive's version history is the undo.

import io
import json
import re
import subprocess
import sys
import tempfile
import time
import zipfile
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shelf_common import CATALOG_PATH, CONTENT, ROOT, load_json, save_json  # noqa: E402
import source_covers as S  # noqa: E402  (DriveRangeFile + rclone serve helpers)

STATE = ROOT / ".cache" / "watermarks.json"
REPORT = CONTENT / "watermark_scan.md"
LOG = CONTENT / "watermark_log.json"
MARK = re.compile(r"(?:https?://)?(?:www\.)?oceanofpdf(?:\.com)?/?", re.I)   # no spaces: "an ocean of pdfs" is prose
TEXT_EXT = re.compile(r"\.(x?html?|xml|ncx|opf|css|svg)$", re.I)
EXCLUDED = {"Archive of bullshit"}


def visible(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"&[a-z#0-9]+;", " ", html))).strip()


def leftover_is_junk(text):
    t = MARK.sub("", text)
    t = re.sub(r"(?i)\b(downloaded|download|from|visit|get|more|books?|free|at|on|by|via|ebooks?|pdfs?)\b", "", t)
    return not re.sub(r"[\s\W_]+", "", t)


LAYOUT_ATTR = re.compile(r"\bid\s*=|break|page", re.I)   # anchors (TOC links) and page/chapter breaks


def clean_text(src):
    out = src
    inner = re.compile(r"(<(p|div|span|h[1-6]|li|small|footer|header|center|b|i|em|strong|font)\b[^>]*>)"
                       r"((?:(?!<\2\b)[^<]|<(?!/?\2\b)[^>]*>)*?)(</\2\s*>)", re.I | re.S)

    def drop(m):
        body = m.group(3)
        if not (MARK.search(visible(body) or body) and leftover_is_junk(visible(body))):
            return m.group(0)
        # An element that carries an id (something may link to it) or a page/chapter break keeps its tag and
        # only loses the watermark text, so breaks and links stay exactly where they were.
        return m.group(1) + m.group(4) if LAYOUT_ATTR.search(m.group(1)) else ""

    for _ in range(6):
        new = inner.sub(drop, out)
        if new == out:
            break
        out = new
    out = re.sub(r"<a\b[^>]*oceanofpdf[^>]*>.*?</a>", "", out, flags=re.I | re.S)   # links inside real text
    out = re.sub(r"(?i)(downloaded\s+from\s*:?\s*)?" + MARK.pattern, "", out)
    return out


def words(html):
    return visible(html).split()


def check_same_book(before, after):
    """Deterministic proof that only the watermark went: -> list of problems (empty = safe)."""
    import difflib
    problems = []
    a, b = words(before), words(after)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        if op != "delete":           # anything added, replaced or moved = the text changed, not just lost a mark
            problems.append(f"text changed near: {' '.join(a[max(0, i1 - 6):i2 + 6])[:120]!r}")
        elif not leftover_is_junk(" ".join(a[i1:i2])):
            problems.append(f"real text removed: {' '.join(a[i1:i2])[:120]!r}")
    ids = lambda t: re.findall(r"\bid\s*=\s*[\"']([^\"']+)", t)
    if ids(before) != ids(after):
        problems.append("link targets (ids) changed")
    imgs = lambda t: re.findall(r"<(?:img|image)\b[^>]*?(?:src|href)\s*=\s*[\"']([^\"']+)", t, re.I)
    if imgs(before) != imgs(after):
        problems.append("images changed")
    brk = lambda t: len(re.findall(r"page-break|break-(?:before|after)|pagebreak", t, re.I))
    if brk(before) != brk(after):
        problems.append("page/chapter breaks changed")
    heads = lambda t: [visible(h) for h in re.findall(r"<h[1-6]\b[^>]*>(.*?)</h[1-6]>", t, re.I | re.S)
                       if not leftover_is_junk(visible(h))]
    if heads(before) != heads(after):
        problems.append("headings changed")
    return problems


def parses(text):
    try:
        ET.fromstring(re.sub(r"&(?!amp;|lt;|gt;|quot;|apos;|#)[a-zA-Z0-9]+;", " ", text))
        return True
    except ET.ParseError:
        return False


def clean_epub(data):
    """bytes -> (cleaned bytes or None, info dict)"""
    zin = zipfile.ZipFile(io.BytesIO(data))
    buf = io.BytesIO()
    removed = changed_files = 0
    before_chars = after_chars = 0
    problems = []
    with zipfile.ZipFile(buf, "w") as zout:
        names = zin.namelist()
        order = (["mimetype"] if "mimetype" in names else []) + [n for n in names if n != "mimetype"]
        for name in order:
            info = zin.getinfo(name)
            raw = zin.read(name)
            if name == "mimetype":
                zi = zipfile.ZipInfo("mimetype", info.date_time)
                zi.compress_type = zipfile.ZIP_STORED
                zout.writestr(zi, raw)
                continue
            if TEXT_EXT.search(name):
                text = raw.decode("utf-8", "ignore") if raw[:3] != b"\xef\xbb\xbf" else raw[3:].decode("utf-8", "ignore")
                hits = len(MARK.findall(text))
                if hits:
                    new = clean_text(text)
                    if re.search(r"\.x?html?$", name, re.I) and parses(text) and not parses(new):
                        problems.append(f"{name}: no longer valid XHTML")
                    if re.search(r"\.(x?html?|xml|ncx|opf)$", name, re.I):
                        problems += [f"{name}: {p}" for p in check_same_book(text, new)]
                    b, a = len(visible(MARK.sub("", text))), len(visible(new))
                    before_chars += b
                    after_chars += a
                    removed += hits
                    changed_files += 1
                    raw = new.encode("utf-8")
            zi = zipfile.ZipInfo(name, info.date_time)
            zi.compress_type = info.compress_type
            zi.external_attr = info.external_attr
            zout.writestr(zi, raw)
    out = buf.getvalue()
    z2 = zipfile.ZipFile(io.BytesIO(out))
    if z2.testzip() is not None or sorted(z2.namelist()) != sorted(zin.namelist()):
        problems.append("rebuilt zip differs")
    import hashlib
    for n in zin.namelist():                     # every file without the watermark must be byte-for-byte identical
        if not TEXT_EXT.search(n) or not MARK.search(zin.read(n).decode("utf-8", "ignore")):
            if hashlib.sha256(zin.read(n)).digest() != hashlib.sha256(z2.read(n)).digest():
                problems.append(f"{n}: changed although it had no watermark")
    left = sum(len(MARK.findall(z2.read(n).decode("utf-8", "ignore"))) for n in z2.namelist() if TEXT_EXT.search(n))
    if left:
        problems.append(f"{left} watermark(s) left")
    lost = (before_chars - after_chars) / before_chars if before_chars else 0
    if lost > 0.01:
        problems.append(f"{lost:.1%} of the text would disappear")
    info = {"removed": removed, "files": changed_files, "lost": round(lost, 4), "problems": problems}
    return (None if problems else out), info


def scan_one(e):
    z = zipfile.ZipFile(io.BufferedReader(S.DriveRangeFile(e["path"], int(e["size_bytes"])), buffer_size=256 * 1024))
    n = 0
    sample = ""
    for name in z.namelist():
        if TEXT_EXT.search(name):
            t = z.read(name).decode("utf-8", "ignore")
            for m in MARK.finditer(t):
                n += 1
                sample = sample or t[max(0, m.start() - 160):m.end() + 80].replace("\n", " ")
    return {"hits": n, "sample": sample}


def main():
    args = sys.argv[1:]
    if "--dry-clean" in args:
        p = Path(args[args.index("--dry-clean") + 1])
        out, info = clean_epub(p.read_bytes())
        print(json.dumps(info, indent=1))
        if out:
            dst = Path(tempfile.gettempdir()) / f"cleaned-{p.name}"
            dst.write_bytes(out)
            print("cleaned copy:", dst)
        return
    apply = "--apply" in args
    limit = int(args[args.index("--limit") + 1]) if "--limit" in args else None
    only = args[args.index("--only") + 1].lower() if "--only" in args else None
    cat = [e for e in load_json(CATALOG_PATH, []) if e["ext"] == "epub" and e["folder"] not in EXCLUDED]
    if only:
        cat = [e for e in cat if only in e["filename"].lower()]
    state = load_json(STATE, {})
    todo = [e for e in cat if e["id"] not in state or state[e["id"]].get("modified") != e["modified"]]
    proc = S.start_rclone_serve() if todo else None
    try:
        for i, e in enumerate(todo, 1):
            try:
                r = scan_one(e)
            except Exception as ex:
                r = {"hits": -1, "error": f"{type(ex).__name__}: {ex}"[:200]}
            r["modified"], r["path"] = e["modified"], e["path"]
            state[e["id"]] = r
            if i % 10 == 0 or i == len(todo):
                save_json(STATE, state)
                print(f"  scanned {i}/{len(todo)}", flush=True)
    finally:
        if proc:
            proc.terminate()
    affected = [e for e in cat if state.get(e["id"], {}).get("hits", 0) > 0]
    errors = [e for e in cat if state.get(e["id"], {}).get("hits") == -1]
    lines = [f"# OceanofPDF watermark scan — {time.strftime('%Y-%m-%d')}", "",
             f"{len(cat)} EPUBs scanned: {len(affected)} have the watermark, {len(errors)} couldn't be read.", ""]
    lines += [f"- {e['filename']} — {state[e['id']]['hits']}x" for e in affected]
    if errors:
        lines += ["", "Couldn't read:"] + [f"- {e['filename']} — {state[e['id']].get('error')}" for e in errors]
    REPORT.write_text("\n".join(lines) + "\n")
    print(f"{len(affected)} of {len(cat)} EPUBs have the watermark -> {REPORT.name}")
    if not apply:
        return
    log = load_json(LOG, [])
    done = skipped = 0
    for e in affected[:limit] if limit else affected:
        with tempfile.TemporaryDirectory() as td:
            local = Path(td) / "book.epub"
            src = f"gdrive:Books/{e['path']}"
            subprocess.run(["rclone", "copyto", src, str(local)], check=True, capture_output=True)
            out, info = clean_epub(local.read_bytes())
            if out and not info["removed"]:
                print(f"--   {e['filename']}: nothing to remove")
                continue
            if not out:
                skipped += 1
                print(f"SKIP {e['filename']}: {'; '.join(info['problems'])}")
                state[e["id"]]["skipped"] = info["problems"]
                continue
            local.write_bytes(out)
            r = subprocess.run(["rclone", "copyto", str(local), src], capture_output=True, text=True)
            if r.returncode:
                skipped += 1
                print(f"FAIL upload {e['filename']}: {r.stderr.strip()[-200:]}")
                continue
            done += 1
            print(f"ok   {e['filename']}: removed {info['removed']} in {info['files']} file(s)")
            log.append({"id": e["id"], "path": e["path"], "removed": info["removed"], "at": datetime.now().isoformat(timespec="seconds")})
            save_json(LOG, log)
            state[e["id"]]["hits"] = 0
            state[e["id"]]["cleaned"] = True
            save_json(STATE, state)
    print(f"Cleaned {done}, skipped {skipped}. Re-sync the catalog: python3 scripts/sync_drive_catalog.py")


if __name__ == "__main__":
    main()
