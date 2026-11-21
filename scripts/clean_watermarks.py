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
# - Books are downloaded whole with `rclone cat` (all EPUBs = ~3 GB). Range reads through `rclone serve http`
#   took 15-20 s per piece and returned wrong bytes for some files (false "not a zip file").
# - Don't run it while source_covers.py runs: whichever started `rclone serve` stops it when done, and the
#   other's reads then fail (368 BadZipFile errors once). Failed reads are retried on the next run.
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

STATE = CONTENT / "state" / "epub_watermarks.json"   # in git: survives a new Mac
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


LOCAL = None      # --local DIR: books already downloaded there (rclone copy gdrive:Books DIR --include "*.epub")
OTHER_MARKS = re.compile(r"z-?library|z-lib\.|1lib\.|libgen|dokumen\.pub|ebook3000|it-ebooks|vk\.com/|pdfdrive|"
                         r"freebookspot|epubpub|bookfrom\.net|ebooksclub|wowebook|allitebooks|anna[’']?s archive", re.I)


def download(e):
    if LOCAL:
        data = (Path(LOCAL) / e["path"]).read_bytes()
        if len(data) != int(e["size_bytes"]):
            raise IOError("local copy differs from Drive (re-download)")
        return data
    r = subprocess.run(["rclone", "cat", f"gdrive:Books/{e['path']}"], capture_output=True, timeout=900)
    if r.returncode or len(r.stdout) != int(e["size_bytes"]):
        raise IOError(f"download failed/short ({len(r.stdout)} of {e['size_bytes']} bytes)")
    return r.stdout


def scan_one(e):
    z = zipfile.ZipFile(io.BytesIO(download(e)))
    n = 0
    sample = ""
    other = {}
    extra = []
    if z.testzip() is not None:
        extra.append("damaged zip entry")
    names = z.namelist()
    if "mimetype" not in names:
        extra.append("no mimetype (some readers refuse it)")
    if "META-INF/encryption.xml" in names:
        enc = z.read("META-INF/encryption.xml").decode("utf-8", "ignore")
        if re.search(r"EncryptionMethod[^>]+Algorithm=\"(?!http://www\.idpf\.org/2008/embedding|"
                     r"http://ns\.adobe\.com/pdf/enc#RC)", enc):
            extra.append("copy-protected (DRM): can't be cleaned or read in the Nook")
    for name in names:
        if TEXT_EXT.search(name):
            t = z.read(name).decode("utf-8", "ignore")
            for m in MARK.finditer(t):
                n += 1
                sample = sample or t[max(0, m.start() - 160):m.end() + 80].replace("\n", " ")
            for m in OTHER_MARKS.finditer(t):
                k = m.group(0).lower()
                other[k] = other.get(k, 0) + 1
    return {"hits": n, "sample": sample, "other_marks": other, "issues": extra}


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
    global LOCAL
    LOCAL = args[args.index("--local") + 1] if "--local" in args else None
    apply = "--apply" in args
    limit = int(args[args.index("--limit") + 1]) if "--limit" in args else None
    only = args[args.index("--only") + 1].lower() if "--only" in args else None
    cat = [e for e in load_json(CATALOG_PATH, []) if e["ext"] == "epub" and e["folder"] not in EXCLUDED]
    if only:
        cat = [e for e in cat if only in e["filename"].lower()]
    state = load_json(STATE, {})
    todo = [e for e in cat if e["id"] not in state or state[e["id"]].get("modified") != e["modified"]
            or state[e["id"]].get("hits") == -1]                       # failed reads are retried
    from concurrent.futures import ThreadPoolExecutor
    import threading
    lock, count = threading.Lock(), [0]

    def work(e):
        try:
            r = scan_one(e)
        except Exception as ex:
            r = {"hits": -1, "error": f"{type(ex).__name__}: {ex}"[:200]}
        r["modified"], r["path"] = e["modified"], e["path"]
        with lock:
            state[e["id"]] = r
            count[0] += 1
            if count[0] % 10 == 0 or count[0] == len(todo):
                save_json(STATE, state)
                print(f"  scanned {count[0]}/{len(todo)}", flush=True)

    with ThreadPoolExecutor(10 if LOCAL else 4) as ex:   # rclone cat downloads 4 at a time; local copies 10
        list(ex.map(work, todo))
    affected = [e for e in cat if state.get(e["id"], {}).get("hits", 0) > 0]
    errors = [e for e in cat if state.get(e["id"], {}).get("hits") == -1]
    lines = [f"# OceanofPDF watermark scan — {time.strftime('%Y-%m-%d')}", "",
             f"{len(cat)} EPUBs scanned: {len(affected)} have the watermark, {len(errors)} couldn't be read.", ""]
    lines += [f"- {e['filename']} — {state[e['id']]['hits']}x" for e in affected]
    if errors:
        lines += ["", "Couldn't read:"] + [f"- {e['filename']} — {state[e['id']].get('error')}" for e in errors]
    others = [e for e in cat if state.get(e["id"], {}).get("other_marks")]
    if others:
        lines += ["", "Other download-site marks found (not removed; tell Claude if they should be):"]
        lines += [f"- {e['filename']} — {state[e['id']]['other_marks']}" for e in others]
    issues = [e for e in cat if state.get(e["id"], {}).get("issues")]
    if issues:
        lines += ["", "Other problems:"] + [f"- {e['filename']} — {'; '.join(state[e['id']]['issues'])}" for e in issues]
    if not only:                         # a one-book test run must not overwrite the full report
        REPORT.write_text("\n".join(lines) + "\n")
    print(f"{len(affected)} of {len(cat)} EPUBs have the watermark -> {REPORT.name}")
    if not apply:
        return
    # Clean everything locally first (all checks), then upload the passing books in ONE rclone run: it updates
    # each Drive file in place (same id, Drive keeps the old version 30 days), 16 uploads at a time.
    log = load_json(LOG, [])
    staging = ROOT / ".cache" / "watermark_clean"
    import shutil
    shutil.rmtree(staging, ignore_errors=True)
    ready, skipped = [], 0
    import hashlib
    for e in affected[:limit] if limit else affected:
        data = download(e)
        out, info = clean_epub(data)
        info["src_md5"] = hashlib.md5(data).hexdigest()
        if out and not info["removed"]:
            print(f"--   {e['filename']}: nothing to remove")
            continue
        if not out:
            skipped += 1
            print(f"SKIP {e['filename']}: {'; '.join(info['problems'])[:300]}")
            state[e["id"]]["skipped"] = info["problems"]
            continue
        dst = staging / e["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(out)
        ready.append((e, info))
    # Last-moment guard: if a book changed on Drive since we downloaded it (you replaced or edited it mid-run),
    # don't overwrite it; it's re-checked on the next run.
    from shelf_common import drive_unchanged
    still = []
    for e, info in ready:
        if drive_unchanged(e["path"], info["src_md5"]):
            still.append((e, info))
        else:
            print(f"LATER {e['filename']}: changed on Drive during this run, left alone")
            (staging / e["path"]).unlink(missing_ok=True)
            state[e["id"]]["modified"] = "(changed mid-run; re-check)"
    ready = still
    print(f"{len(ready)} cleaned and checked, {skipped} skipped. Uploading…", flush=True)
    if ready:
        r = subprocess.run(["rclone", "copy", str(staging), "gdrive:Books", "--transfers", "16", "--checkers", "16",
                            "--no-update-modtime"], capture_output=True, text=True)
        if r.returncode:
            print("Upload problems:", r.stderr.strip()[-600:])
        sizes = {}
        ls = subprocess.run(["rclone", "lsjson", "-R", "--files-only", str(staging)], capture_output=True, text=True)
        local_sizes = {x["Path"]: x["Size"] for x in json.loads(ls.stdout or "[]")}
        remote = subprocess.run(["rclone", "lsjson", "-R", "--fast-list", "--files-only", "--include", "*.epub", "gdrive:Books"],
                                capture_output=True, text=True)
        sizes = {x["Path"]: x["Size"] for x in json.loads(remote.stdout or "[]")}
        for e, info in ready:
            ok = sizes.get(e["path"]) == local_sizes.get(e["path"])
            print(("ok   " if ok else "FAIL ") + f"{e['filename']}: removed {info['removed']}")
            if ok:
                log.append({"id": e["id"], "path": e["path"], "removed": info["removed"],
                            "at": datetime.now().isoformat(timespec="seconds")})
                state[e["id"]].update(hits=0, cleaned=True)
        save_json(LOG, log)
        save_json(STATE, state)
        if LOCAL:      # keep the local mirror in step with Drive
            for e, _ in ready:
                shutil.copyfile(staging / e["path"], Path(LOCAL) / e["path"])
    shutil.rmtree(staging, ignore_errors=True)
    print(f"Done. Re-sync the catalog: python3 scripts/sync_drive_catalog.py")


if __name__ == "__main__":
    main()
