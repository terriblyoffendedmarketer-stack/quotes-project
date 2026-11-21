# fix_epub_metadata.py — Fixes the hidden title/author fields inside EPUBs on Drive (download-site junk like
#                        "Atomic habits ( PDFDrive.com ).epub", "... - libgen.li", "Downloaded from Z-Library")
#                        and adds a missing `mimetype` entry (Dead Souls). Plain code, no AI.
# Usage: python3 scripts/fix_epub_metadata.py --local .cache/epubs            # dry run: list what would change
#        python3 scripts/fix_epub_metadata.py --local .cache/epubs --apply    # fix + upload over the same Drive files
# Requires: rclone remote gdrive:, a local mirror of the EPUBs (rclone copy gdrive:Books .cache/epubs --include "*.epub"),
#           content/book_names.json (the real title/author), content/gdrive_books_catalog.json.
#
# Only the package file (.opf) and toc.ncx change: dc:title / docTitle become the shelf title, an "Unknown"
# dc:creator becomes the shelf author, and a description that is just a download-site credit is removed.
# Every other file is copied byte for byte (checked), and both XML files must still parse. Drive keeps the
# previous version 30 days; uploads update the same file (same id). Log: content/epub_metadata_log.json.
#
# Gotchas:
# - `mimetype` must be the FIRST zip entry and STORED (uncompressed), content "application/epub+zip".
# - Escape & < > when writing titles into XML ("Simon & Schuster" style names broke a parse once in testing).

import io
import json
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shelf_common import CATALOG_PATH, CONTENT, NAMES_PATH, ROOT, load_json, save_json  # noqa: E402

JUNK = re.compile(r"pdfdrive|z-?library|z-lib|libgen|1lib|dokumen\.pub|anna[’']?s archive|oceanofpdf|\.epub\b", re.I)
LOG = CONTENT / "epub_metadata_log.json"
STAGING = ROOT / ".cache" / "metadata_fix"


def parses(t):
    try:
        ET.fromstring(re.sub(r"&(?!amp;|lt;|gt;|quot;|apos;|#)[a-zA-Z0-9]+;", " ", t))
        return True
    except ET.ParseError:
        return False


def fix_xml(text, title, author, kind):
    changes = []
    if kind == "opf":
        def t_sub(m):
            if JUNK.search(m.group(2)):
                changes.append(f"title: {m.group(2)[:70]!r} -> {title!r}")
                return m.group(1) + escape(title) + m.group(3)
            return m.group(0)
        text = re.sub(r"(<dc:title\b[^>]*>)(.*?)(</dc:title>)", t_sub, text, count=1, flags=re.S)

        def c_sub(m):
            if m.group(2).strip().lower() in ("unknown", "") or JUNK.search(m.group(2)):
                changes.append(f"author: {m.group(2)!r} -> {author!r}")
                return m.group(1) + escape(author) + m.group(3)
            return m.group(0)
        if author and author.lower() not in ("unknown", "unknown author"):
            text = re.sub(r"(<dc:creator\b[^>]*>)(.*?)(</dc:creator>)", c_sub, text, count=1, flags=re.S)

        def d_sub(m):
            if JUNK.search(m.group(1)) and len(re.sub(r"<[^>]+>", "", m.group(1))) < 80:
                changes.append(f"removed description {m.group(1)[:60]!r}")
                return ""
            return m.group(0)
        text = re.sub(r"<dc:description\b[^>]*>(.*?)</dc:description>\s*", d_sub, text, flags=re.S)
    else:  # ncx
        def n_sub(m):
            if JUNK.search(m.group(2)):
                changes.append(f"toc title -> {title!r}")
                return m.group(1) + escape(title) + m.group(3)
            return m.group(0)
        text = re.sub(r"(<docTitle>\s*<text>)(.*?)(</text>)", n_sub, text, count=1, flags=re.S)
    return text, changes


def fix_epub(data, title, author):
    zin = zipfile.ZipFile(io.BytesIO(data))
    names = zin.namelist()
    changes, problems, out_files = [], [], {}
    for n in names:
        raw = zin.read(n)
        if re.search(r"\.(opf|ncx)$", n, re.I):
            t = raw.decode("utf-8", "ignore")
            new, ch = fix_xml(t, title, author, "opf" if n.lower().endswith(".opf") else "ncx")
            if ch:
                if parses(t) and not parses(new):
                    problems.append(f"{n} would no longer parse")
                changes += ch
                raw = new.encode("utf-8")
        out_files[n] = raw
    add_mimetype = "mimetype" not in names          # only books missing it entirely (Dead Souls); order left alone
    if add_mimetype:
        changes.append("added/moved mimetype entry")
    if not changes:
        return None, [], []
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zout:
        zi = zipfile.ZipInfo("mimetype", (2020, 1, 1, 0, 0, 0))
        zi.compress_type = zipfile.ZIP_STORED
        zout.writestr(zi, out_files.pop("mimetype", b"application/epub+zip"))
        for n in names:
            if n == "mimetype":
                continue
            info = zin.getinfo(n)
            z = zipfile.ZipInfo(n, info.date_time)
            z.compress_type, z.external_attr = info.compress_type, info.external_attr
            zout.writestr(z, out_files[n])
    out = buf.getvalue()
    z2 = zipfile.ZipFile(io.BytesIO(out))
    if z2.testzip() is not None or z2.namelist()[0] != "mimetype":
        problems.append("rebuilt zip invalid")
    for n in names:
        if n != "mimetype" and not re.search(r"\.(opf|ncx)$", n, re.I) and z2.read(n) != zin.read(n):
            problems.append(f"{n} changed unexpectedly")
    return (None if problems else out), changes, problems


def main():
    args = sys.argv[1:]
    local = Path(args[args.index("--local") + 1])
    apply = "--apply" in args
    names = load_json(NAMES_PATH, {})
    cat = [e for e in load_json(CATALOG_PATH, []) if e["ext"] == "epub" and e["folder"] != "Archive of bullshit"]
    shutil.rmtree(STAGING, ignore_errors=True)
    ready = []
    for e in cat:
        p = local / e["path"]
        if not p.exists() or p.stat().st_size != int(e["size_bytes"]):
            continue
        n = names.get(e["id"], {})
        try:
            out, changes, problems = fix_epub(p.read_bytes(), n.get("title", ""), n.get("author", ""))
        except zipfile.BadZipFile:
            continue
        if problems:
            print(f"SKIP {e['filename']}: {problems}")
        elif out:
            print(f"fix  {e['filename']}: " + "; ".join(changes))
            dst = STAGING / e["path"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(out)
            ready.append((e, changes))
    print(f"{len(ready)} EPUB(s) to fix.")
    if not apply or not ready:
        print("Dry run." if not apply else "")
        return
    r = subprocess.run(["rclone", "copy", str(STAGING), "gdrive:Books", "--transfers", "16", "--checkers", "16"],
                       capture_output=True, text=True)
    if r.returncode:
        print("Upload problems:", r.stderr.strip()[-600:])
        return
    log = load_json(LOG, [])
    for e, ch in ready:
        log.append({"id": e["id"], "path": e["path"], "changes": ch, "at": datetime.now().isoformat(timespec="seconds")})
        shutil.copyfile(STAGING / e["path"], local / e["path"])
    save_json(LOG, log)
    shutil.rmtree(STAGING, ignore_errors=True)
    print(f"Uploaded {len(ready)}. Re-sync the catalog: python3 scripts/sync_drive_catalog.py")


if __name__ == "__main__":
    main()
