# scripts/build_independent_bookshelf_app.py — Builds My Reading Corner (bookshelf/data.json + bookshelf/index.html + docs/bookshelf.html)
# Usage: python3 scripts/build_independent_bookshelf_app.py
#        (normally via scripts/refresh_bookshelf.sh, which syncs Drive first and enriches new books after)
# Requires: content/gdrive_books_catalog.json (from scripts/sync_drive_catalog.py), content/book_names.json,
#           content/book_overrides.json, content/quote-bank.json, scripts/templates/bookshelf.html
#
# How it works:
#   Drive catalog (what exists) + previous data.json (enrichment: covers, synopses, notes, quotes; keyed by
#   Drive file id) + book_names.json (authoritative title/author, keyed by Drive file id) + book_overrides.json
#   (per-book fixes keyed by shelf id) -> data.json -> template -> HTML.
#
# Gotchas:
# - The OLD build loaded data.json and returned early, never looking at Drive again. That is why books added to
#   Drive never showed up. The catalog is now always the source of what's on the shelf; data.json is only a cache
#   of enrichment, matched by Drive file id.
# - first_seen is set once, the first build a book appears in; the NEW badge keys off it, not the Drive date.
# - Never change an existing book's `id`: the web app stores per-device edits in localStorage keyed by id.
# - Names come from book_names.json, not from filenames. Unlisted (new) files get a parsed guess marked
#   name_source="parsed" until scripts/enrich_new_books.py verifies them.
# - JSON is embedded in a <script> tag, so "</" must be escaped or a title containing "</script>" breaks the page.

import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shelf_common import (BOOK_EXTS, BOOKSHELF_DIR, CATALOG_PATH, DATA_PATH, NAMES_PATH, OVERRIDES_PATH,  # noqa: E402
                          QUOTE_BANK_PATH, ROOT, load_json, norm, parse_filename, save_json, slugify)

TEMPLATE_PATH = ROOT / "scripts" / "templates" / "bookshelf.html"
OUTPUTS = [BOOKSHELF_DIR / "index.html", ROOT / "docs" / "bookshelf.html"]

EXCLUDED_FOLDERS = {"Archive of bullshit"}
FOLDER_CATEGORY = {
    "Fiction ／ non fiction": "Fiction & Non-Fiction",
    "A graphic guide series": "Graphic Guides",
    "Comics and stuff": "Comics & Graphic Novels",
    "On Films": "Cinema & Film Craft",
    "Screenplays": "Screenplays",
    "Tactical Marketing": "Marketing & Strategy",
    "Cooking and food": "Cooking & Food",
    "Others": "Philosophy, Essays & Misc",
    "HBR": "Harvard Business Review",
}
FUN_CATEGORIES = {"Fiction & Non-Fiction", "Comics & Graphic Novels", "Screenplays"}
# Multi-file works stored as a folder of issues/volumes: folder name -> shelf entry
SERIES_FOLDERS = {
    "Watchmen (Complete) (001-012) (1986)": ("Watchmen (The Complete Series)", "Alan Moore & Dave Gibbons", "CBR"),
    "Oyasumi Punpun": ("Goodnight Punpun (Complete Series)", "Inio Asano", "PDF"),
}
FORMAT_RANK = {"EPUB": 0, "PDF": 1, "CBZ": 2, "CBR": 2, "MOBI": 3}


def file_format(f):
    ext = f["ext"].upper()
    if ext.lower() in BOOK_EXTS:
        return ext
    mime = f.get("mime", "")
    if "pdf" in mime:
        return "PDF"
    if "epub" in mime:
        return "EPUB"
    return None  # Google Docs, folders-as-files, docx/pptx: not books


def drive_units(catalog):
    """Yield one unit per shelf book: a single file, or a series folder collapsed to one entry."""
    series = {}
    for f in catalog:
        if f["folder"] in EXCLUDED_FOLDERS:
            continue
        parts = f["path"].split("/")
        if len(parts) >= 3 and parts[-2] in SERIES_FOLDERS:
            series.setdefault(parts[-2], []).append(f)
            continue
        fmt = file_format(f)
        if fmt is None and f["ext"]:
            continue
        yield {"files": [f], "format": fmt, "series": None}
    for folder, files in series.items():
        yield {"files": sorted(files, key=lambda x: x["path"]), "format": SERIES_FOLDERS[folder][2], "series": folder}


def index_quote_bank():
    works = {}
    for q in load_json(QUOTE_BANK_PATH, []):
        key = norm(q.get("work", ""))
        if not key:
            continue
        w = works.setdefault(key, {"author": norm(q.get("author", "")), "quotes": [], "tags": set()})
        w["quotes"].append({"quote": q.get("quote"), "explanation": q.get("explanation")})
        w["tags"].update(q.get("tags", []))
    return works


def match_quotes(title, author, works):
    """Exact normalised title (or main title before ':') plus an overlapping author surname."""
    a_tokens = {t for t in norm(author).split() if len(t) > 2}
    for key in (norm(title), norm(title.split(":")[0])):
        w = works.get(key)
        if w and (not a_tokens or a_tokens & set(w["author"].split())):
            return w
    return None


def richness(b):
    return (bool(b.get("has_quote_bank")), bool(b.get("cover_url")), len(b.get("why_love") or ""),
            -FORMAT_RANK.get(b.get("format", ""), 9))


def build():
    catalog = load_json(CATALOG_PATH, None)
    if not catalog or "id" not in catalog[0]:
        sys.exit("content/gdrive_books_catalog.json is missing or outdated — run scripts/sync_drive_catalog.py first.")
    names = load_json(NAMES_PATH, {})
    overrides = load_json(OVERRIDES_PATH, {}).get("books", {})
    previous = load_json(DATA_PATH, [])
    by_drive_id = {b["drive_id"]: b for b in previous if b.get("drive_id")}
    known_authors = {v["author"] for v in names.values()}
    canon_author = {norm(a): a for a in known_authors}
    works = index_quote_bank()
    used_ids = {b["id"] for b in previous}

    books = []
    for unit in drive_units(catalog):
        files = unit["files"]
        # Reuse the existing entry if any file of this unit is already on the shelf
        prev = next((by_drive_id[f["id"]] for f in files if f["id"] in by_drive_id), None)
        main = next((f for f in files if prev and f["id"] == prev["drive_id"]), files[0])
        b = dict(prev) if prev else {}
        b.pop("rating", None)

        if main["id"] in names:
            b["title"], b["author"] = names[main["id"]]["title"], names[main["id"]]["author"]
            b.pop("name_source", None)
        elif unit["series"]:
            b["title"], b["author"] = SERIES_FOLDERS[unit["series"]][:2]
        elif not prev or b.get("name_source") == "parsed":
            t, a = parse_filename(main["filename"], known_authors)
            b["title"], b["author"] = t, canon_author.get(norm(a), a)
            b["name_source"] = "parsed"

        if not prev:
            bid = slugify(f"{b['title']}-{b['author']}")
            while bid in used_ids:
                bid += "-x"
            used_ids.add(bid)
            b.update({"id": bid, "category": FOLDER_CATEGORY.get(main["folder"], "Philosophy, Essays & Misc"),
                      "cover_url": "", "pitch": "", "why_love": "", "quotes": [], "has_quote_bank": False,
                      "tags": [], "needs_enrichment": True})

        b["drive_id"] = main["id"]
        b["drive_url"] = f"https://drive.google.com/file/d/{main['id']}/view"
        b["direct_download_url"] = f"https://drive.usercontent.google.com/download?id={main['id']}&export=download"
        b["format"] = unit["format"] or b.get("format") or "EPUB"
        b["added"] = max(f["modified"] for f in files)[:10]          # Drive upload/modified date
        b["first_seen"] = b.get("first_seen") or ("" if prev else date.today().isoformat())  # drives the NEW badge

        if not b.get("has_quote_bank"):
            w = match_quotes(b["title"], b["author"], works)
            if w:
                b.update({"has_quote_bank": True, "quotes": w["quotes"],
                          "tags": sorted(set(b.get("tags", [])) | w["tags"])})

        ov = overrides.get(b["id"], {})
        for k, v in ov.items():
            if k != "extra_categories":
                b[k] = v
        if b.get("no_cover"):
            b["cover_url"] = None
        b["categories"] = [b["category"]] + [c for c in ov.get("extra_categories", []) if c != b["category"]]
        if not b.get("tags"):
            b["tags"] = [slugify(b["category"])]
        b["is_fun_pick"] = b["category"] in FUN_CATEGORIES or b.get("is_fun_pick", False)
        books.append(b)

    # Same book stored twice on Drive (e.g. an .epub and a .pdf): keep the richer/better-format copy
    best = {}
    for b in books:
        # Keep bracketed parts in the key: "Bakemonogatari (Part 1)" and "(Part 2)" are different books
        key = tuple(re.sub(r"[^a-z0-9]+", " ", x.lower()).strip() for x in (b["title"], b["author"]))
        if key not in best or richness(b) > richness(best[key]):
            best[key] = b
    dropped = len(books) - len(best)
    books = sorted(best.values(), key=lambda x: (x["category"], x["title"].lower()))

    kept_ids = {x["id"] for x in books}
    new_titles = [f"{b['title']} — {b['author']}" for b in books if b["id"] not in {p["id"] for p in previous}]
    removed = [b["title"] for b in previous if b["id"] not in kept_ids]
    save_json(DATA_PATH, books)
    render(books)

    print(f"Shelf: {len(books)} books ({len(new_titles)} new, {len(removed)} gone from Drive or merged, "
          f"{dropped} duplicate copies collapsed)")
    print(f"  covers: {sum(1 for b in books if b.get('cover_url'))}  quotes: {sum(1 for b in books if b.get('has_quote_bank'))}"
          f"  awaiting enrichment: {sum(1 for b in books if b.get('needs_enrichment'))}")
    for t in new_titles:
        print(f"  + {t}")
    for t in removed:
        print(f"  - {t}")


def render(books):
    import json
    shelf_json = json.dumps(books, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE_PATH.read_text(encoding="utf-8")
    for token, value in {
        "@@SHELF_JSON@@": shelf_json,
        "@@TOTAL_BOOKS@@": str(len(books)),
        "@@COVERS_COUNT@@": str(sum(1 for b in books if b.get("cover_url"))),
        "@@QUOTE_COUNT@@": str(sum(1 for b in books if b.get("has_quote_bank"))),
        "@@TBR_COUNT@@": str(len(books)),
        "@@BUILD_DATE@@": date.today().isoformat(),
    }.items():
        html = html.replace(token, value)
    for out in OUTPUTS:
        out.parent.mkdir(exist_ok=True)
        out.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    build()
