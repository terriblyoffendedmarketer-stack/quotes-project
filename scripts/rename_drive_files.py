# scripts/rename_drive_files.py — Renames book files on Google Drive to "Title - Author.ext", but only after verifying the name
# Usage: python3 scripts/rename_drive_files.py              # DRY RUN: verify + print plan, change nothing
#        python3 scripts/rename_drive_files.py --apply      # rename VERIFIED files only; held ones are listed for review
#        python3 scripts/rename_drive_files.py --apply --limit 1   # rename just one (smoke test)
#        python3 scripts/rename_drive_files.py --undo       # revert every rename in content/drive_rename_log.json
# Requires: rclone remote `gdrive:` with FULL drive scope (read-only scope -> 403 ACCESS_TOKEN_SCOPE_INSUFFICIENT;
#           fix with `rclone config reconnect gdrive:` choosing scope "drive"); a fresh catalog from
#           scripts/sync_drive_catalog.py; content/book_names.json; network access to openlibrary.org.
#
# Verification (a file is renamed only if BOTH title and author are backed by independent evidence):
#   1. Filename evidence — every significant word of the new title / the author's surname already appears in
#      the ORIGINAL filename (from content/drive_name_history.json) AND every author is a real author (quote bank
#      or Open Library author index). The second half catches swaps: word overlap alone can't tell
#      "Greenlights - Matthew McConaughey" from "Matthew McConaughey - Greenlights", but "Greenlights" isn't an author.
#   2. Open Library — the exact (title, author) pair exists as a real book.
#   3. Quote bank — the book's quotes were attributed to the same title and author.
#   4. Embedded metadata — for EPUBs still unverified, the file's own dc:title / dc:creator (downloaded to a
#      temp dir, small files only).
#   Anything unproven is HELD: not renamed, written to content/drive_rename_review.md with the reason.
#
# Gotchas:
# - --apply and --undo re-sync the Drive catalog themselves: planning from a stale catalog (e.g. right after an
#   undo) targets the wrong files.
# - Safe for the shelf: the bookshelf keys every book by Drive file id, and a rename keeps the id.
# - Undo trail is double: content/drive_rename_log.json (from -> to, saved after EVERY move) and the append-only
#   content/drive_name_history.json (original name of every file ever seen). Google Drive's own Activity panel
#   also shows "renamed from ...".
# - NEVER rename onto an existing name: `rclone moveto` onto a file it considers identical deletes the SOURCE
#   (it trashed a duplicate copy once). We reserve every existing filename in the folder (spaces-insensitive)
#   and pass --ignore-existing as a second guard.
# - Only files listed in book_names.json are touched; series folders, the archive folder and non-book files are
#   skipped. Two files that would collide in one folder get " (2)".
# - Characters that break desktop sync (/ \ : * ? " < > |) are removed; a subtitle colon becomes an en dash
#   ("Title – Subtitle - Author") so the " - " before the author stays unambiguous.

import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shelf_common import (CATALOG_PATH, CONTENT, NAMES_PATH, QUOTE_BANK_PATH, SMALL_WORDS,  # noqa: E402
                          load_json, norm, save_json)
from enrich_new_books import best_match, search  # noqa: E402

LOG_PATH = CONTENT / "drive_rename_log.json"
HISTORY_PATH = CONTENT / "drive_name_history.json"
REVIEW_PATH = CONTENT / "drive_rename_review.md"
CACHE_PATH = CONTENT / "name_verification_cache.json"
REMOTE = "gdrive:Books"
SKIP_FOLDERS = {"Archive of bullshit"}
NO_AUTHOR = {"Anonymous", "Various Authors", "Unknown", ""}
JUNK = {"trans", "ed", "dir", "vol", "part", "complete", "series", "edition", "screenplay", "based"}
MAX_EPUB_BYTES = 25_000_000


def clean_filename(title, author, ext):
    def fix(s):
        s = s.replace(": ", " – ").replace(":", " – ").replace("/", "-")
        s = re.sub(r'[\\*?"<>|]', "", s)
        return re.sub(r"\s+", " ", s).strip(" .")
    name = fix(title) if author in NO_AUTHOR else f"{fix(title)} - {fix(author)}"
    return f"{name[:180]}.{ext}" if ext else name[:180]


def words(s):
    return {w for w in norm(s).split() if w not in SMALL_WORDS and w not in JUNK}


def main_title(t):
    return re.split(r"[:(–]", t)[0].strip()


def surnames(author):
    """Last word of each person in 'A B & C D, E F (trans. X)' -> {'b', 'd', 'f'}."""
    author = re.sub(r"\(.*?\)", "", author)
    out = set()
    for person in re.split(r"&|,| and ", author):
        toks = [t for t in norm(person).split() if t not in {"jr", "sr", "dr", "prof"}]
        if toks:
            out.add(toks[-1])
    return out


def plan():
    catalog = load_json(CATALOG_PATH, [])
    names = load_json(NAMES_PATH, {})
    wanted = []
    for f in catalog:
        if f["folder"] in SKIP_FOLDERS or f["id"] not in names or len(f["path"].split("/")) > 2:
            continue
        n = names[f["id"]]
        folder = f["path"].rsplit("/", 1)[0] if "/" in f["path"] else ""
        ext = f["ext"] if f["ext"] in {"epub", "pdf", "cbr", "cbz", "mobi"} else ""
        wanted.append((f, n, folder, ext, clean_filename(n["title"], n["author"], ext)))

    def variants(base, ext):
        stem = base[: -len(ext) - 1] if ext else base
        yield base
        for i in range(2, 50):
            yield f"{stem} ({i}).{ext}" if ext else f"{stem} ({i})"

    # Files already sitting on a valid name (the base name or a " (n)" variant) keep it. Without this, two copies
    # of the same book would swap their " (2)" suffix on every run, depending on listing order.
    def key(folder, name):          # Drive treats "X .epub" and "X.epub" as different, but rclone saw them as one
        stem, dot, e = name.rpartition(".")
        return folder, (re.sub(r"\s+", " ", stem).strip().lower() + dot + e.lower()) if dot else name.strip().lower()
    wanted_ids = {f["id"] for f, *_ in wanted}
    taken, chosen = {}, {}
    # Every OTHER file already in the folder (duplicates, unlisted files) blocks its name: renaming onto it made
    # rclone treat the two as one file and trash the source (2026-11-11, "One Plus One Equals Three").
    for f in catalog:
        if f["id"] not in wanted_ids:
            folder = f["path"].rsplit("/", 1)[0] if "/" in f["path"] else ""
            taken[key(folder, f["filename"])] = f["id"]
    for f, n, folder, ext, base in wanted:
        if f["filename"] in set(list(variants(base, ext))[:10]) and key(folder, f["filename"]) not in taken:
            taken[key(folder, f["filename"])] = f["id"]
            chosen[f["id"]] = f["filename"]
    moves = []
    for f, n, folder, ext, base in wanted:
        if f["id"] not in chosen:
            new = next(v for v in variants(base, ext)
                       if key(folder, v) not in taken or taken[key(folder, v)] == f["id"])
            taken[key(folder, new)] = f["id"]
            chosen[f["id"]] = new
        new = chosen[f["id"]]
        if new != f["filename"]:
            moves.append({"id": f["id"], "from": f["path"], "to": f"{folder}/{new}" if folder else new,
                          "title": n["title"], "author": n["author"], "ext": f["ext"], "size": f["size_bytes"]})
    return moves


def author_exists(author, qb_authors, cache):
    """Every person in the author string is a known author (quote bank) or found in Open Library's author index."""
    from enrich_new_books import get_json
    import urllib.parse
    author = re.sub(r"\(.*?\)", "", author)
    for person in [p.strip() for p in re.split(r"&|,| and ", author) if p.strip()]:
        sn = surnames(person)
        if sn & qb_authors:
            continue
        key = f"author|{person}"
        if key not in cache:
            try:
                docs = get_json("https://openlibrary.org/search/authors.json?" + urllib.parse.urlencode({"q": person, "limit": 5})).get("docs", [])
                cache[key] = any(sn & set(norm(d.get("name", "")).split()) and d.get("work_count", 0) > 0 for d in docs)
            except Exception:
                return False          # network trouble: don't verify, try again next run
            save_json(CACHE_PATH, cache)
            time.sleep(0.3)
        if not cache[key]:
            return False
    return True


def quote_bank_index():
    idx = {}
    for q in load_json(QUOTE_BANK_PATH, []):
        idx.setdefault(norm(main_title(q.get("work", ""))), set()).update(surnames(q.get("author", "")))
    return idx


def epub_metadata(path):
    tmp = Path(tempfile.mkdtemp(prefix="epubmeta-"))
    try:
        r = subprocess.run(["rclone", "copyto", f"{REMOTE}/{path}", str(tmp / "book.epub")], capture_output=True)
        if r.returncode:
            return None
        z = zipfile.ZipFile(tmp / "book.epub")
        opf = next(n for n in z.namelist() if n.endswith(".opf"))
        x = z.read(opf).decode("utf-8", "ignore")
        t = re.findall(r"<dc:title[^>]*>(.*?)</dc:title>", x, re.S)
        a = re.findall(r"<dc:creator[^>]*>(.*?)</dc:creator>", x, re.S)
        return (t[0] if t else ""), " & ".join(a)
    except Exception:
        return None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def verify(moves, use_network=True):
    history = load_json(HISTORY_PATH, {})
    cache = load_json(CACHE_PATH, {})
    qb = quote_bank_index()
    qb_authors = set().union(*qb.values()) if qb else set()
    for m in moves:
        original = history.get(m["id"], {}).get("original", m["from"]).rsplit("/", 1)[-1]
        evidence_words = words(original) | words(m["from"].rsplit("/", 1)[-1])
        t_words = words(main_title(m["title"]))
        a_names = surnames(m["author"]) if m["author"] not in NO_AUTHOR else set()
        ev = []
        title_ok = bool(t_words) and t_words <= evidence_words
        author_ok = not a_names or bool(a_names & evidence_words)
        if title_ok and author_ok and a_names and use_network and not author_exists(m["author"], qb_authors, cache):
            title_ok = author_ok = False          # words match but the "author" isn't a known author: maybe swapped
        if title_ok and author_ok:
            ev.append("filename")
        if not (title_ok and author_ok):
            hit = qb.get(norm(main_title(m["title"])))
            if hit is not None and (not a_names or a_names & hit):
                title_ok = author_ok = True
                ev.append("quote bank")
        if not (title_ok and author_ok) and use_network:
            key = f"ol|{m['title']}|{m['author']}"
            if key not in cache:
                doc = best_match(search(main_title(m["title"]), "" if m["author"] in NO_AUTHOR else m["author"]),
                                 main_title(m["title"]), m["author"] if m["author"] not in NO_AUTHOR else "")
                cache[key] = bool(doc)
                save_json(CACHE_PATH, cache)
                time.sleep(0.4)
            if cache[key]:
                title_ok = author_ok = True
                ev.append("Open Library")
        if not (title_ok and author_ok) and use_network and m["ext"] == "epub" and m["size"] < MAX_EPUB_BYTES:
            key = f"epub|{m['id']}"
            if key not in cache:
                cache[key] = epub_metadata(m["from"])
                save_json(CACHE_PATH, cache)
            meta = cache[key]
            if meta:
                mt, ma = meta
                if not title_ok and t_words and t_words <= words(mt):
                    title_ok = True
                if not author_ok and a_names & words(ma):
                    author_ok = True
                if title_ok and author_ok:
                    ev.append("embedded metadata")
        m["verified"] = title_ok and author_ok
        m["evidence"] = ev
        m["reason"] = "" if m["verified"] else (
            ("title not confirmed" if not title_ok else "") + (" & " if not title_ok and not author_ok else "")
            + ("author not confirmed" if not author_ok else ""))
    return moves


def write_review(held):
    lines = ["# Drive renames held for review", "",
             "These files were NOT renamed because the new name couldn't be confirmed by the filename, Open Library,",
             "the quote bank, or the file's own metadata. If a proposed name is right, leave it; if wrong, fix it in",
             "`content/book_names.json` (keyed by the Drive id shown). Then run "
             "`python3 scripts/rename_drive_files.py --apply --include-held` to rename these too.", ""]
    for m in held:
        lines.append(f"- `{m['from']}` → **{m['to'].rsplit('/', 1)[-1]}** — {m['reason']} (id `{m['id']}`)")
    REVIEW_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def rclone_move(src, dst):
    # --ignore-existing: if anything already sits at dst, do nothing rather than merge/overwrite/trash
    r = subprocess.run(["rclone", "moveto", "--ignore-existing", f"{REMOTE}/{src}", f"{REMOTE}/{dst}"],
                       capture_output=True, text=True)
    return r.returncode == 0, (r.stderr.strip().splitlines() or [""])[-1] if r.returncode else ""


def resync():
    subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "sync_drive_catalog.py")],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)


def main():
    args = sys.argv[1:]
    if "--undo" in args:
        log = load_json(LOG_PATH, [])
        failed = []
        for m in reversed(log):
            ok, err = rclone_move(m["to"], m["from"])
            print(("undo " if ok else "FAIL ") + f"{m['to']} -> {m['from']} {err}")
            if not ok:
                failed.insert(0, m)
        save_json(LOG_PATH, failed)          # keep only what couldn't be reverted
        resync()
        return
    if "--apply" in args:
        resync()                             # never plan renames from a stale catalog
    moves = verify(plan())
    include_held = "--include-held" in args
    todo = [m for m in moves if m["verified"] or include_held]
    held = [m for m in moves if not m["verified"]]
    write_review(held)
    by_ev = {}
    for m in moves:
        for e in m["evidence"]:
            by_ev[e] = by_ev.get(e, 0) + 1
    print(f"{len(moves)} file(s) need a new name: {len(moves) - len(held)} verified "
          f"({', '.join(f'{k}: {v}' for k, v in by_ev.items())}), {len(held)} held -> {REVIEW_PATH.name}")
    if "--apply" not in args:
        for m in todo[:20]:
            print(f"  {m['from'].rsplit('/', 1)[-1]}\n     -> {m['to'].rsplit('/', 1)[-1]}   [{', '.join(m['evidence'])}]")
        print("Dry run only. Re-run with --apply to rename on Google Drive.")
        return
    if "--limit" in args:
        todo = todo[: int(args[args.index("--limit") + 1])]
    log = load_json(LOG_PATH, [])
    done = 0
    for m in todo:
        ok, err = rclone_move(m["from"], m["to"])
        print(("ok   " if ok else "FAIL ") + m["to"] + (f"  {err}" if err else ""))
        if ok:
            done += 1
            log.append({"id": m["id"], "from": m["from"], "to": m["to"], "evidence": m["evidence"],
                        "at": datetime.now().isoformat(timespec="seconds")})
            save_json(LOG_PATH, log)   # after EVERY move, so a crash never loses the undo trail
    print(f"Renamed {done}/{len(todo)}. Now run: python3 scripts/sync_drive_catalog.py")


if __name__ == "__main__":
    main()
