# scripts/audit_covers.py — Finds and fixes wrong book covers by READING each cover (local OCR) and checking it
# Usage: python3 scripts/audit_covers.py            # audit only: writes content/cover_audit.md
#        python3 scripts/audit_covers.py --fix      # also apply verified replacements to content/book_overrides.json
#        python3 scripts/audit_covers.py --only "Title"   # audit one book (debugging)
# Requires: the local vision server (http://localhost:9090, SmolVLM; restart with
#           `launchctl load ~/Library/LaunchAgents/com.local.vision-tool.plist`), openlibrary.org, Python 3 stdlib.
#           Rebuild the shelf afterwards.
#
# Verdict per cover (text on the cover vs the book's title/author):
#   OK        — the cover text matches the title (or author + part of the title) and is in English (or the
#               book itself isn't English, e.g. Hindi titles)
#   FOREIGN   — right book, but a translated edition (e.g. Man's Search for Meaning showing the German cover)
#   WRONG     — cover text names something else
#   NO TEXT   — couldn't read any text (art-only cover): left alone
#   For FOREIGN/WRONG, --fix tries the other covers Open Library has for the matching works, OCRs them, and only
#   swaps in one that passes. If none passes: WRONG -> typographic jacket; FOREIGN -> keep (right book at least).
#
# Gotchas:
# - Author matches but title doesn't -> treated as FOREIGN (translated/retitled edition), never WRONG, so a
#   right-book cover is never downgraded to a jacket.
# - Don't judge covers by Open Library ids alone: OL keeps several duplicate "works" per book, so an id missing
#   from one work's list is often perfectly correct (1984, Harry Potter were false alarms that way).
# - SmolVLM ignores output-format instructions; use plain OCR text and judge in Python.
# - Spelled-out numbers: "Nineteen Eighty-Four" must match "1984" — NUMBER_ALIASES handles the known cases.
# - Covers set by hand in book_overrides.json (cover_url) are trusted and never touched.
# - OCR results are cached per cover id in content/cover_ocr_cache.json (each OCR takes ~3-4 s).

import json
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shelf_common import CONTENT, DATA_PATH, OVERRIDES_PATH, SMALL_WORDS, load_json, norm, save_json  # noqa: E402
from enrich_new_books import UA, get_json, main_title  # noqa: E402

OCR_CACHE = CONTENT / "cover_ocr_cache.json"
REPORT = CONTENT / "cover_audit.md"
TMP = Path("/tmp") / "reading-corner-covers"
VISION = "http://localhost:9090/caption"
L = "https://covers.openlibrary.org/b/id/{}-L.jpg"
NUMBER_ALIASES = {"1984": "nineteen eighty four", "451": "four hundred fifty one", "22": "twenty two"}
FOREIGN_WORDS = {
    "der", "die", "das", "und", "ein", "eine", "nicht", "zum", "von", "mit", "des",          # German
    "le", "la", "les", "et", "du", "une", "dans", "pour",                                    # French
    "el", "los", "las", "y", "del", "una", "por", "con",                                     # Spanish
    "il", "di", "della", "che", "gli",                                                       # Italian
    "het", "een", "van", "voor",                                                             # Dutch
    "os", "um", "uma", "dos", "das",                                                         # Portuguese
}
ENGLISH_HINTS = {"the", "and", "of", "a", "to", "in", "novel", "author", "bestselling", "by", "stories", "new", "york", "times"}


def cover_id(url):
    m = re.search(r"/b/id/(\d+)", url or "")
    return int(m.group(1)) if m else None


def ocr(cid, cache):
    key = str(cid)
    if key in cache:
        return cache[key]
    TMP.mkdir(exist_ok=True)
    img = TMP / f"{cid}.jpg"
    try:
        req = urllib.request.Request(f"https://covers.openlibrary.org/b/id/{cid}-M.jpg", headers=UA)
        img.write_bytes(urllib.request.urlopen(req, timeout=30).read())
        if img.stat().st_size < 1500:          # OL returns a tiny placeholder for missing covers
            cache[key] = ""
        else:
            body = json.dumps({"image": str(img), "task": "ocr"}).encode()
            r = urllib.request.Request(VISION, data=body, headers={"Content-Type": "application/json"})
            cache[key] = json.loads(urllib.request.urlopen(r, timeout=180).read())["result"]["text"]
    except Exception as e:
        print(f"    ! OCR failed for {cid}: {e}")
        return None                             # undecided; not cached
    finally:
        img.unlink(missing_ok=True)
    save_json(OCR_CACHE, cache)
    return cache[key]


def sig_words(s):
    s = norm(s)
    for k, v in NUMBER_ALIASES.items():
        s = s.replace(k, f"{k} {v}")
    return {w for w in s.split() if w not in SMALL_WORDS and len(w) > 1}


def strip_framing(text):
    """SmolVLM sometimes wraps OCR in English ('The cover of a book titled "X" by Y.'), which hides the language."""
    t = re.sub(r'^\s*(the )?(cover|image|front cover)( of)?( a| the)? book( is)?( titled| called| with the title)?\s*', "", text, flags=re.I)
    t = re.sub(r'^(this is|it is|it reads)\s*', "", t, flags=re.I)
    return t.strip()


DESCRIPTIVE = re.compile(r"\b(the image|background|depict|illustration of|picture of|photo of|is written in)\b", re.I)


def fuzzy_hits(want, seen):
    """Words of `want` found in `seen`, tolerating OCR slips (LOCIGOMIX/Logicomix, conjurer/conjuror)."""
    from difflib import SequenceMatcher
    hits = set()
    for w in want:
        if w in seen or (len(w) >= 4 and any(SequenceMatcher(None, w, s).ratio() >= 0.75 for s in seen if len(s) >= 4)):
            hits.add(w)
    return hits


def judge(text, b, in_ol=False):
    if in_ol:
        return "OK"                     # Open Library lists this cover under a matching edition: trust it
    if not text or len(text.strip()) < 3:
        return "NO TEXT"
    text = strip_framing(text)
    if DESCRIPTIVE.search(text) and not re.search(r'"[^"]{3,}"', text):
        return "NO TEXT"                # the model described the picture instead of reading text
    t_words, seen = sig_words(main_title(b["title"])), sig_words(text)
    full_words = sig_words(b["title"])
    surnames = {w for w in sig_words(re.sub(r"\(.*?\)", "", b["author"])) if len(w) > 2} - {"anonymous", "various", "authors"}
    hit_t = len(fuzzy_hits(t_words, seen)) / max(1, len(t_words))
    hit_full = len(fuzzy_hits(full_words, seen)) / max(1, len(full_words))
    hit_a = bool(fuzzy_hits(surnames, seen))
    matches = hit_t >= 0.6 or hit_full >= 0.6 or (hit_a and hit_t > 0) or (hit_a and not t_words)
    words = re.findall(r"[a-zà-ÿ]+", text.lower())
    foreign = sum(w in FOREIGN_WORDS for w in words) >= 2 and sum(w in ENGLISH_HINTS for w in words) == 0
    non_latin = bool(re.search(r"[Ѐ-ӿ֐-ۿ぀-ヿ一-鿿가-힯]", text))
    book_is_latin = not re.search(r"[^\x00-ɏ]", b["title"])
    if book_is_latin and (foreign or non_latin) and (matches or hit_a):
        return "FOREIGN"
    if matches:
        return "OK"
    if hit_a:
        return "FOREIGN"      # right author, different title: almost always a translated/retitled edition
    if len(seen) < 2:
        return "NO TEXT"      # too little readable text to call it wrong
    return "WRONG"


SPINOFF = re.compile(r"summar|adapt|study guide|workbook|analysis|sparknotes|cliffs|young readers|abridged", re.I)


def ol_cover_set(b, cache):
    """Every cover id Open Library has for editions whose title starts with ours (any language). Cached."""
    import urllib.parse
    key = f"olset|{b['title']}|{b['author']}"
    if key in cache:
        return set(cache[key])
    want = norm(main_title(b["title"]))
    surname = norm(re.split(r"&|,", re.sub(r"\(.*?\)", "", b["author"]))[0]).split()[-1:] \
        if b["author"] not in ("Anonymous", "Various Authors") else []
    q = f'title:"{main_title(b["title"])}"' + (f" author:{surname[0]}" if surname else "")
    ids = set()
    try:
        docs = get_json("https://openlibrary.org/search.json?" + urllib.parse.urlencode(
            {"q": q, "limit": 10, "fields": "key,title,cover_i,editions,editions.title,editions.cover_i"})).get("docs", [])
    except Exception:
        return set()
    for d in docs:
        if d.get("cover_i"):
            ids.add(d["cover_i"])
        for e in d.get("editions", {}).get("docs", []):
            if e.get("cover_i"):
                ids.add(e["cover_i"])
        try:
            ids.update(c for c in get_json(f"https://openlibrary.org{d['key']}.json").get("covers", []) if c and c > 0)
        except Exception:
            pass
        time.sleep(0.2)
    cache[key] = sorted(ids)
    save_json(OCR_CACHE, cache)
    return ids


def candidate_covers(b, current):
    """Covers of ENGLISH EDITIONS whose title starts with ours. Edition-level search matters: OL files some works under
    their original title (Man's Search for Meaning lives under "Trotzdem Ja zum Leben sagen"), so work-title
    matching misses them, but `editions.*` fields + language:eng return the English edition and its cover."""
    import urllib.parse
    want = norm(main_title(b["title"]))
    surname = norm(re.split(r"&|,", re.sub(r"\(.*?\)", "", b["author"]))[0]).split()[-1:] if b["author"] not in ("Anonymous", "Various Authors") else []
    q = f'title:"{main_title(b["title"])}"' + (f" author:{surname[0]}" if surname else "")
    seen, out = {current}, []
    for lang in ("language:eng", ""):
        params = {"q": f"{q} {lang}".strip(), "limit": 8, "sort": "editions",
                  "fields": "key,title,cover_i,editions,editions.title,editions.cover_i,editions.language"}
        try:
            docs = get_json("https://openlibrary.org/search.json?" + urllib.parse.urlencode(params)).get("docs", [])
        except Exception:
            return out
        for d in docs:
            for e in d.get("editions", {}).get("docs", []):
                t = e.get("title", "")
                c = e.get("cover_i")
                if c and c not in seen and norm(t).startswith(want) and not SPINOFF.search(t):
                    seen.add(c)
                    out.append(c)
            if lang == "" and norm(d.get("title", "")).startswith(want) and not SPINOFF.search(d.get("title", "")):
                c = d.get("cover_i")
                if c and c not in seen:
                    seen.add(c)
                    out.append(c)
        time.sleep(0.3)
        if out:
            break
    return out[:8]


def main():
    fix = "--fix" in sys.argv
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    books = load_json(DATA_PATH, [])
    ov = load_json(OVERRIDES_PATH, {"books": {}})
    cache = load_json(OCR_CACHE, {})
    rows = {k: [] for k in ("OK", "FOREIGN", "WRONG", "NO TEXT", "FIXED", "JACKET")}
    todo = [b for b in books if cover_id(b.get("cover_url")) and "cover_url" not in ov["books"].get(b["id"], {})
            and (not only or only.lower() in b["title"].lower())]
    print(f"Reading {len(todo)} covers...", flush=True)
    for i, b in enumerate(todo, 1):
        cid = cover_id(b["cover_url"])
        text = ocr(cid, cache)
        if text is None:
            continue
        verdict = judge(text, b)
        if verdict in ("FOREIGN", "WRONG", "NO TEXT") and cid in ol_cover_set(b, cache):
            verdict = "OK" if verdict != "FOREIGN" else verdict     # listed by OL for this book: not a wrong book
        note = text[:90].replace("\n", " ")
        if verdict in ("FOREIGN", "WRONG") and fix:
            replacement = None
            for c in candidate_covers(b, cid):
                t = ocr(c, cache)
                if t and judge(t, b) == "OK":
                    replacement = c
                    break
            entry = ov["books"].setdefault(b["id"], {})
            if replacement:
                entry["cover_url"] = L.format(replacement)
                entry.pop("no_cover", None)
                rows["FIXED"].append((b, f"{verdict.lower()} → {L.format(replacement)} (cover reads: {note})"))
                verdict = None
            elif verdict == "WRONG":
                entry["cover_url"], entry["no_cover"] = None, True
                rows["JACKET"].append((b, f"cover read “{note}”; no matching cover found"))
                verdict = None
            elif not entry:
                ov["books"].pop(b["id"])          # FOREIGN with no English option: keep current cover
            save_json(OVERRIDES_PATH, ov)
        if verdict:
            rows[verdict].append((b, note))
        if i % 25 == 0:
            print(f"  ...{i}/{len(todo)}  ok {len(rows['OK'])} fixed {len(rows['FIXED'])} jacket {len(rows['JACKET'])} "
                  f"foreign {len(rows['FOREIGN'])} wrong {len(rows['WRONG'])}", flush=True)

    titles = {"FIXED": "Replaced with a verified cover", "JACKET": "Wrong cover removed (typographic jacket now)",
              "WRONG": "Wrong cover (not fixed — run with --fix)", "FOREIGN": "Right book, foreign-language edition (no English cover found)",
              "NO TEXT": "No readable text on cover (left alone — check by eye)"}
    lines = ["# Cover audit (OCR-verified)", "", " · ".join(f"{k.lower()}: {len(v)}" for k, v in rows.items()), ""]
    for k, head in titles.items():
        if rows[k]:
            lines += [f"## {head}", ""] + [f"- **{b['title']}** — {b['author']}: {n}" for b, n in rows[k]] + [""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(" · ".join(f"{k}: {len(v)}" for k, v in rows.items()), f"-> {REPORT.relative_to(CONTENT.parent)}")


if __name__ == "__main__":
    main()
