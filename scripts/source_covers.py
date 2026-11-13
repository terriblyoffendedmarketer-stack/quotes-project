# source_covers.py — Finds the RIGHT, best-quality cover for every shelf book, checked against the book file itself
# Usage: python3 scripts/source_covers.py                 # scan (cached) -> content/cover_sourcing.json + .md report
#        python3 scripts/source_covers.py --limit 20      # first 20 books only (calibration)
#        python3 scripts/source_covers.py --only <shelf-id or title words>
#        python3 scripts/source_covers.py --apply         # write chosen covers into content/book_overrides.json
#                                                         # and save file-covers to bookshelf/covers + docs/covers
# Requires: Python 3 + Pillow (Homebrew python3 has it), rclone remote gdrive:, macOS `sips` (PDFs).
#           Rebuild the shelf afterwards (python3 scripts/build_independent_bookshelf_app.py).
#
# How a cover is chosen (per book):
#   1. Reference = the cover inside the book file (EPUB cover image -> else the first page's image; PDF page 1;
#      CBZ first image). Low quality, but it's the exact edition the user owns, so it is the ground truth.
#   2. Candidates = Apple Books (big, clean) + Google Books + Open Library by ISBN + the cover we have now.
#   3. A candidate is used only if it LOOKS LIKE the reference (grayscale correlation >= MATCH). Best res wins.
#   4. No candidate matches -> the file's own cover (saved as covers/<drive_id>.jpg). No file cover -> keep
#      the current cover only if it passed, else typographic jacket. Covers the user set by hand (source
#      "user" in book_overrides.json) are never touched.
#
# Gotchas:
# - Don't read the books through the Drive API key: ~60 parallel range requests got this Mac's IP a Google
#   "Sorry... unusual traffic" block (403) for a while. Files are read through `rclone serve http` on
#   127.0.0.1:8977 (rclone's own login, cached folder listing, Range support), started/stopped by this script.
# - EPUBs are read with HTTP Range requests (zip central directory + cover only), never fully downloaded.
#   PDFs have no such shortcut: downloaded one at a time to .cache/, page 1 rendered with sips, then deleted.
# - Apple Search API allows ~20 requests/min; requests are spaced 3.2 s apart (slowest part of a full run).
# - Google Books answers 429 to keyless requests and the Drive key isn't enabled for it, so google() is unused.
# - Store results are full of foreign / graphic-novel / summary editions: is_clean() drops them (English check
#   on Apple's description). Most user files are odd editions, so an exact visual match is the exception.
# - Results are cached per Drive id in .cache/covers/state.json — delete an entry to re-check a book.

import io
import json
import os
import re
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor
from difflib import SequenceMatcher
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image, ImageChops, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shelf_common import CONTENT, DATA_PATH, OVERRIDES_PATH, ROOT, load_json, norm, save_json  # noqa: E402

CACHE = ROOT / ".cache" / "covers"
REF_DIR = CACHE / "ref"
STATE_PATH = CACHE / "state.json"
OUT_JSON = CONTENT / "cover_sourcing.json"
OUT_MD = CONTENT / "cover_sourcing.md"
COVER_DIRS = [ROOT / "bookshelf" / "covers", ROOT / "docs" / "covers"]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
MATCH = 0.80          # grayscale correlation needed to call two covers "the same cover" (calibrated, see report)
SIG_W, SIG_H = 24, 36

_lock = threading.Lock()
_apple_next = [0.0]


SERVE = "http://127.0.0.1:8977/"


def http(url, headers=None, timeout=25):
    h = {"User-Agent": UA}
    h.update(headers or {})
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=timeout) as r:
        return r.read()


def file_url(path):
    return SERVE + urllib.parse.quote(path)


def start_rclone_serve():
    try:
        http(SERVE, timeout=3)
        return None                       # already running
    except Exception:
        pass
    proc = subprocess.Popen(["rclone", "serve", "http", "gdrive:Books", "--addr", "127.0.0.1:8977", "--read-only",
                             "--dir-cache-time", "2h", "--no-checksum"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        time.sleep(1)
        try:
            http(SERVE, timeout=5)
            return proc
        except Exception:
            pass
    proc.kill()
    sys.exit("rclone serve http did not start")


class DriveRangeFile(io.RawIOBase):
    """Seekable read-only view of a Drive file that fetches 256 KB blocks on demand (for zipfile)."""
    BLOCK = 256 * 1024

    def __init__(self, path, size):
        self.url, self.size, self.pos, self.blocks = file_url(path), size, 0, {}

    def readable(self): return True
    def seekable(self): return True
    def tell(self): return self.pos

    def seek(self, off, whence=0):
        self.pos = off if whence == 0 else self.pos + off if whence == 1 else self.size + off
        return self.pos

    def _block(self, i):
        if i not in self.blocks:
            a, b = i * self.BLOCK, min(self.size, (i + 1) * self.BLOCK) - 1
            for attempt in range(3):
                try:
                    self.blocks[i] = http(self.url, {"Range": f"bytes={a}-{b}"}, timeout=90)
                    if len(self.blocks[i]) != b - a + 1:
                        raise IOError("short/ignored range read")
                    break
                except Exception:
                    if attempt == 2:
                        raise
                    time.sleep(2)
        return self.blocks[i]

    def readinto(self, buf):
        if self.pos >= self.size:
            return 0
        i, off = divmod(self.pos, self.BLOCK)
        data = self._block(i)[off:off + len(buf)]
        buf[:len(data)] = data
        self.pos += len(data)
        return len(data)


# ---------- reference cover from the book file ----------

def _local(tag):
    return tag.rsplit("}", 1)[-1]


def _join(base, href):
    href = urllib.parse.unquote(href.split("#")[0])
    parts = (base.split("/")[:-1] if "/" in base else []) + href.split("/")
    out = []
    for p in parts:
        if p == "..":
            out and out.pop()
        elif p not in ("", "."):
            out.append(p)
    return "/".join(out)


def _first_image_in_xhtml(z, path):
    try:
        html = z.read(path).decode("utf-8", "ignore")
    except KeyError:
        return None
    m = re.search(r'<(?:img|image)\b[^>]*?(?:xlink:href|href|src)\s*=\s*["\']([^"\']+)', html, re.I)
    return _join(path, m.group(1)) if m else None


def epub_reference(path, size):
    """-> (PIL image or None, meta dict) reading only the needed parts of the zip."""
    z = zipfile.ZipFile(io.BufferedReader(DriveRangeFile(path, size), buffer_size=256 * 1024))
    names = set(z.namelist())
    meta = {}
    opf_path = None
    try:
        cont = ET.fromstring(z.read("META-INF/container.xml"))
        opf_path = next(e.get("full-path") for e in cont.iter() if _local(e.tag) == "rootfile")
    except Exception:
        opf_path = next((n for n in names if n.endswith(".opf")), None)
    cover = None
    if opf_path:
        opf = ET.fromstring(z.read(opf_path))
        manifest, spine, cover_id = {}, [], None
        for e in opf.iter():
            t = _local(e.tag)
            if t == "item":
                manifest[e.get("id")] = (e.get("href", ""), e.get("media-type", ""), e.get("properties", ""))
            elif t == "itemref":
                spine.append(e.get("idref"))
            elif t == "meta" and e.get("name") == "cover":
                cover_id = e.get("content")
            elif t == "reference" and (e.get("type") or "").lower() == "cover" and not cover:
                p = _join(opf_path, e.get("href", ""))
                cover = p if re.search(r"\.(jpe?g|png|gif)$", p, re.I) else _first_image_in_xhtml(z, p)
            elif t in ("title", "creator", "description") and e.text and t not in meta:
                meta[t] = e.text.strip()
            elif t == "identifier" and e.text:
                digits = re.sub(r"[^0-9Xx]", "", e.text)
                if len(digits) in (10, 13) and "isbn" not in meta:
                    meta["isbn"] = digits
        img_items = {i: v for i, v in manifest.items() if v[1].startswith("image/")}
        prop = next((v[0] for v in img_items.values() if "cover-image" in v[2]), None)
        if prop:
            cover = _join(opf_path, prop)
        elif cover_id and cover_id in img_items:
            cover = _join(opf_path, img_items[cover_id][0])
        elif cover_id:   # some books point meta cover at the image's href-ish id
            hit = next((v[0] for i, v in img_items.items() if cover_id.lower() in (i or "").lower()), None)
            cover = cover or (_join(opf_path, hit) if hit else None)
        if not cover and spine and spine[0] in manifest:      # user's rule: else the first page's image
            cover = _first_image_in_xhtml(z, _join(opf_path, manifest[spine[0]][0]))
        if not cover:
            hit = next((v[0] for i, v in img_items.items() if "cover" in (i or "").lower() + v[0].lower()), None)
            cover = _join(opf_path, hit) if hit else None
    img = None
    if cover and cover in names:
        try:
            img = Image.open(io.BytesIO(z.read(cover))).convert("RGB")
            if img.width < 150 or img.height < 150:
                img = None
        except Exception:
            img = None
    return img, meta


def pdf_reference(fid, path):
    tmp = CACHE / f"tmp_{fid}.pdf"
    out = CACHE / f"tmp_{fid}.jpg"
    try:
        tmp.write_bytes(http(file_url(path), timeout=600))
        subprocess.run(["sips", "-s", "format", "jpeg", "-Z", "900", str(tmp), "--out", str(out)],
                       capture_output=True, timeout=120)
        if not out.exists():
            return None
        img = Image.open(out).convert("RGB")
        img.load()
        return img
    finally:
        tmp.unlink(missing_ok=True)
        out.unlink(missing_ok=True)


def cbz_reference(path, size):
    z = zipfile.ZipFile(io.BufferedReader(DriveRangeFile(path, size), buffer_size=256 * 1024))
    imgs = sorted(n for n in z.namelist() if re.search(r"\.(jpe?g|png|webp)$", n, re.I) and "__MACOSX" not in n)
    return (Image.open(io.BytesIO(z.read(imgs[0]))).convert("RGB") if imgs else None), {}


# ---------- comparing covers ----------

def trim(img):
    """Cut flat borders/letterboxing so a framed scan compares with a clean store image."""
    g = img.convert("RGB")
    for _ in range(2):
        bg = Image.new("RGB", g.size, g.getpixel((0, 0)))
        diff = ImageChops.add(ImageChops.difference(g, bg), ImageChops.difference(g, bg), 2.0, -30)
        box = diff.getbbox()
        if not box or (box[2] - box[0]) < g.width * 0.5 or (box[3] - box[1]) < g.height * 0.5:
            break
        if box == (0, 0, g.width, g.height):
            break
        g = g.crop(box)
    return g


def signature(img):
    g = ImageOps.equalize(trim(img).convert("L").resize((SIG_W, SIG_H), Image.LANCZOS))
    px = list(g.get_flattened_data() if hasattr(g, "get_flattened_data") else g.getdata())
    m = sum(px) / len(px)
    sd = (sum((p - m) ** 2 for p in px) / len(px)) ** 0.5 or 1.0
    return [(p - m) / sd for p in px]


def similarity(a, b):
    return sum(x * y for x, y in zip(a, b)) / len(a)


# ---------- candidates ----------

def main_t(t):
    return norm(re.split(r"[:(]", t or "")[0])


def text_ok(title, author, c_title, c_author):
    a, b = main_t(title), main_t(c_title)
    if not a or not b:
        return False
    t_ok = a == b or (len(a) > 6 and (a in b or b in a)) or SequenceMatcher(None, a, b).ratio() >= 0.85
    surnames = [w for w in norm(author).split() if len(w) > 2]
    a_ok = not surnames or author in ("Unknown", "Unknown Author") or any(s in norm(c_author) for s in surnames)
    return t_ok and a_ok


def apple(title, author):
    with _lock:
        wait = _apple_next[0] - time.time()
        _apple_next[0] = max(time.time(), _apple_next[0]) + 3.2
    if wait > 0:
        time.sleep(wait)
    q = urllib.parse.urlencode({"term": f"{main_t(title)} {author if 'Unknown' not in author else ''}".strip(),
                                "media": "ebook", "entity": "ebook", "limit": 10, "country": "us"})
    try:
        res = json.loads(http(f"https://itunes.apple.com/search?{q}"))["results"]
    except Exception:
        return []
    out = []
    for r in res:
        art = r.get("artworkUrl100") or ""
        if art and text_ok(title, author, r.get("trackName", ""), r.get("artistName", "")):
            out.append({"src": "apple", "title": r.get("trackName"), "author": r.get("artistName"),
                        "cmp": art.replace("100x100bb", "600x600bb"), "url": art.replace("100x100bb", "1000x1000bb"),
                        "desc": re.sub(r"<[^>]+>", " ", r.get("description") or "").strip()})
    return out


def google(title, author, isbn):
    qs = [f"isbn:{isbn}"] if isbn else []
    qs.append(f'intitle:"{main_t(title)}"' + (f' inauthor:"{author}"' if "Unknown" not in author else ""))
    out = []
    for q in qs:
        try:
            items = json.loads(http("https://www.googleapis.com/books/v1/volumes?" + urllib.parse.urlencode(
                {"q": q, "maxResults": 6, "printType": "books"}))).get("items", [])
        except Exception:
            continue
        for it in items:
            v = it.get("volumeInfo", {})
            img = (v.get("imageLinks") or {}).get("thumbnail")
            if img and (q.startswith("isbn:") or text_ok(title, author, v.get("title", ""), " ".join(v.get("authors", [])))):
                base = f"https://books.google.com/books/content?id={it['id']}&printsec=frontcover&img=1"
                out.append({"src": "google", "title": v.get("title"), "author": ", ".join(v.get("authors", [])),
                            "cmp": base + "&zoom=1", "url": base + "&zoom=0", "desc": v.get("description") or ""})
        if out:
            break
    return out


def candidates(book, meta):
    title, author = book["title"], book.get("author") or "Unknown"
    cands = apple(title, author)        # Google Books: 429 for keyless requests, so not used (see Gotchas)
    if meta.get("isbn"):
        u = f"https://covers.openlibrary.org/b/isbn/{meta['isbn']}-L.jpg?default=false"
        cands.append({"src": "openlibrary-isbn", "cmp": u, "url": u.replace("?default=false", ""), "desc": ""})
    if book.get("cover_url") and not book["cover_url"].startswith("covers/"):
        cands.append({"src": "current", "cmp": book["cover_url"], "url": book["cover_url"], "desc": ""})
    seen, out = set(), []
    for c in cands:
        if c["cmp"] not in seen:
            seen.add(c["cmp"])
            out.append(c)
    return out[:12]


def fetch_img(url):
    try:
        img = Image.open(io.BytesIO(http(url, timeout=20))).convert("RGB")
        if img.width < 60 or img.height < 80 or (img.width > img.height * 1.3):
            return None            # placeholders / "image not available" banners
        return img
    except Exception:
        return None


# ---------- per book ----------

def reference_for(book, cat_entry):
    fid, ext = book["drive_id"], (cat_entry.get("ext") or "").lower()
    ref_path = REF_DIR / f"{fid}.jpg"
    meta_path = REF_DIR / f"{fid}.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text())
        return (Image.open(ref_path).convert("RGB") if ref_path.exists() else None), meta
    img, meta = None, {}
    try:
        if ext == "epub":
            img, meta = epub_reference(cat_entry["path"], int(cat_entry["size_bytes"]))
        elif ext == "pdf":
            img = pdf_reference(fid, cat_entry["path"])
        elif ext == "cbz":
            img, meta = cbz_reference(cat_entry["path"], int(cat_entry["size_bytes"]))
    except Exception as e:
        meta = {"error": f"{type(e).__name__}: {e}"[:200]}
    if img:
        img.thumbnail((900, 1350))
        img.save(ref_path, "JPEG", quality=88)
    meta_path.write_text(json.dumps(meta, ensure_ascii=False))
    return img, meta


def process(book, cat_entry):
    ref, meta = reference_for(book, cat_entry)
    result = {"id": book["id"], "drive_id": book["drive_id"], "title": book["title"], "author": book.get("author"),
              "format": book.get("format"), "has_ref": bool(ref), "ref_error": meta.get("error"),
              "isbn": meta.get("isbn"), "epub_desc": (meta.get("description") or "")[:4000], "candidates": []}
    ref_sig = signature(ref) if ref else None
    for c in candidates(book, meta):
        img = fetch_img(c["cmp"])
        if not img:
            continue
        c = dict(c, w=img.width, h=img.height)
        if ref_sig:
            c["sim"] = round(similarity(ref_sig, signature(img)), 3)
        result["candidates"].append(c)
    return result


VARIANT = re.compile(r"graphic novel|summary|study guide|sparknotes|cliffsnotes|young adult|analysis of|workbook|"
                     r"illustrated|annotated|abridged|for kids|edici[oó]n|edizione|ausgabe|urania|roman\b|novela|"
                     r"coloring|quotes from|trivia|unofficial", re.I)
EN_STOP = {"the", "and", "of", "to", "a", "in", "is", "that", "his", "her", "with", "for", "was", "as", "it", "this",
           "by", "an", "on", "who", "from", "their", "one", "has"}


def english(text):
    words = re.findall(r"[a-zA-Z\u00C0-\u024F']+", text.lower())
    return len(words) >= 12 and sum(w in EN_STOP for w in words) / len(words) >= 0.12


def is_clean(c, book):
    """Apple result that is the right book, in English, and not a spin-off/summary/translated edition."""
    if c["src"] != "apple" or "Unknown" in (book.get("author") or "Unknown"):
        return False
    a, b = main_t(book["title"]), main_t(c.get("title"))
    if not (a == b or SequenceMatcher(None, a, b).ratio() >= 0.92):
        return False
    extra = VARIANT.findall(c.get("title") or "")
    if any(x.lower() not in book["title"].lower() for x in extra):
        return False
    return english(c.get("desc") or "") if c.get("desc") else (c.get("title") or "").isascii()


def decide(r, book, user_set):
    """-> (decision, cover_url or None, trusted description or '')"""
    if user_set:
        return "user-set (kept)", book.get("cover_url"), ""
    matched = sorted([c for c in r["candidates"] if c.get("sim", -1) >= MATCH],
                     key=lambda c: ({"apple": 3, "google": 1, "openlibrary-isbn": 2, "current": 2}[c["src"]], c["w"] * c["h"]),
                     reverse=True)
    if matched:
        c = matched[0]
        desc = next((m["desc"] for m in matched if m.get("desc")), "")
        return f"matched {c['src']} (sim {c['sim']})", c["url"], desc
    clean = next((c for c in r["candidates"] if is_clean(c, book)), None)
    if clean:
        return "apple right book", clean["url"], clean.get("desc", "")
    if r["has_ref"]:
        return "file cover", f"covers/{r['drive_id']}.jpg", ""
    cur = next((c for c in r["candidates"] if c["src"] == "current"), None)
    if cur:
        return "no file cover: kept current (unverified)", cur["url"], ""
    return "jacket", None, ""


def main():
    args = sys.argv[1:]
    limit = int(args[args.index("--limit") + 1]) if "--limit" in args else None
    only = args[args.index("--only") + 1].lower() if "--only" in args else None
    apply = "--apply" in args
    REF_DIR.mkdir(parents=True, exist_ok=True)
    books = [b for b in load_json(DATA_PATH, []) if b.get("drive_id")]
    cat = load_json(CONTENT / "gdrive_books_catalog.json", [])
    cat = {e["id"]: e for e in (cat if isinstance(cat, list) else cat.get("files", []))}
    if only:
        books = [b for b in books if b["id"] == only or only in b["title"].lower()]
    if limit:
        books = books[:limit]
    state = load_json(STATE_PATH, {})
    for k in [k for k, r in state.items() if "403" in (r.get("ref_error") or "") or "BadZip" in (r.get("ref_error") or "")
              or "short/ignored" in (r.get("ref_error") or "")]:
        state.pop(k)                      # failed reads from the blocked run: retry
        (REF_DIR / f"{k}.json").unlink(missing_ok=True)
    todo = [b for b in books if b["drive_id"] not in state and b["drive_id"] in cat]
    print(f"{len(books)} books, {len(todo)} to scan ({len(books) - len(todo)} cached)")

    done = [0]

    def work(b):
        try:
            r = process(b, cat[b["drive_id"]])
        except Exception as e:
            r = {"id": b["id"], "drive_id": b["drive_id"], "title": b["title"], "error": str(e)[:200], "candidates": []}
        with _lock:
            state[b["drive_id"]] = r
            done[0] += 1
            if done[0] % 10 == 0:
                save_json(STATE_PATH, state)
                print(f"  {done[0]}/{len(todo)}", flush=True)
        return r

    proc = start_rclone_serve() if todo else None
    try:
        with ThreadPoolExecutor(4) as ex:
            list(ex.map(work, todo))
    finally:
        if proc:
            proc.terminate()
    save_json(STATE_PATH, state)

    overrides = load_json(OVERRIDES_PATH, {"books": {}})
    ob = overrides.setdefault("books", {})
    rows, counts = [], {}
    for b in books:
        r = state.get(b["drive_id"])
        if not r or r.get("error"):
            continue
        user_set = (ob.get(b["id"]) or {}).get("cover_source") == "user"
        decision, url, desc = decide(r, b, user_set)
        kind = decision.split(" (")[0].split(":")[0]
        counts[kind] = counts.get(kind, 0) + 1
        changed = (url or None) != (b.get("cover_url") or None)
        rows.append({"id": b["id"], "title": b["title"], "author": b.get("author"), "decision": decision,
                     "old": b.get("cover_url"), "new": url, "changed": changed, "trusted_desc": desc,
                     "epub_desc": r.get("epub_desc", ""),
                     "best_sim": max([c.get("sim", -1) for c in r["candidates"]] or [-1])})
        if apply and not user_set and changed:
            o = ob.setdefault(b["id"], {})
            if url and url.startswith("covers/"):
                for d in COVER_DIRS:
                    d.mkdir(parents=True, exist_ok=True)
                    img = Image.open(REF_DIR / f"{r['drive_id']}.jpg")
                    img.thumbnail((600, 900))
                    img.save(d / f"{r['drive_id']}.jpg", "JPEG", quality=82, optimize=True)
            if url:
                o["cover_url"], o["cover_source"] = url, "verified"
                o.pop("no_cover", None)
            else:
                o["cover_url"], o["no_cover"], o["cover_source"] = None, True, "verified"
    save_json(OUT_JSON, rows)
    lines = [f"# Cover sourcing — {time.strftime('%Y-%m-%d')}", "", "Counts: " + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())), "",
             "| Book | Decision | best sim | changed |", "|---|---|---|---|"]
    lines += [f"| {r['title']} — {r['author']} | {r['decision']} | {r['best_sim']} | {'yes' if r['changed'] else ''} |" for r in rows]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("Counts:", counts, f"| changed: {sum(r['changed'] for r in rows)}")
    if apply:
        save_json(OVERRIDES_PATH, overrides)
        print("Applied to book_overrides.json — now rebuild the shelf.")


if __name__ == "__main__":
    main()
