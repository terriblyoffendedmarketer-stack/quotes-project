# scripts/shelf_common.py — Shared paths + name helpers for the My Reading Corner bookshelf pipeline
# Usage: imported by sync/build/enrich scripts (not run directly)
# Requires: Python 3 standard library
#
# Gotchas:
# - Filenames on Drive follow no single convention: "Title - Author", "Author - Title", "Title_-_Author",
#   "title-[author]", "Title by Author", "{Author}" tags, libgen/PDFDrive suffixes. parse_filename() handles
#   these, and decides which side of " - " is the author by checking the curated author list first, then a
#   person-name heuristic. Ties fall back to "Title - Author" (the convention used for new uploads).
# - Parsed names are a first guess only: the build marks them name_source="parsed" and enrich_new_books.py
#   verifies them against Open Library and writes the result to content/book_names.json.

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
CATALOG_PATH = CONTENT / "gdrive_books_catalog.json"
NAMES_PATH = CONTENT / "book_names.json"
OVERRIDES_PATH = CONTENT / "book_overrides.json"
QUOTE_BANK_PATH = CONTENT / "quote-bank.json"
BOOKSHELF_DIR = ROOT / "bookshelf"
DATA_PATH = BOOKSHELF_DIR / "data.json"

BOOK_EXTS = {"epub", "pdf", "cbr", "cbz", "mobi"}
SMALL_WORDS = {"a", "an", "the", "and", "but", "or", "nor", "for", "so", "yet", "at", "by", "in", "of", "on",
               "to", "up", "as", "is", "vs", "via", "with", "from", "into", "than"}
NOT_NAME_WORDS = SMALL_WORDS | {"how", "why", "what", "when", "who", "my", "your", "our", "we", "i", "you", "it",
                                "novel", "stories", "story", "book", "guide", "volume", "vol", "part", "complete",
                                "collection", "letters", "essays", "life", "art", "love", "war", "time"}


def load_json(path, default):
    return json.loads(Path(path).read_text(encoding="utf-8")) if Path(path).exists() else default


def save_json(path, data, sort_keys=False):
    Path(path).write_text(json.dumps(data, indent=1, ensure_ascii=False, sort_keys=sort_keys) + "\n", encoding="utf-8")


def norm(s):
    """Loose comparison key: lowercase ascii-ish words, no punctuation/brackets/extensions."""
    if not s:
        return ""
    s = s.lower().replace("_", " ").replace("-", " ").replace("&", " and ")
    s = re.sub(r"\[.*?\]|\(.*?\)|\{.*?\}", " ", s)
    s = re.sub(r"\.(epub|pdf|cbr|cbz|mobi|docx|pptx)$", "", s)
    s = re.sub(r"[^a-z0-9 ]", "", s)
    return " ".join(s.split())


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "book"


def smart_title(t):
    """Capitalise all-lowercase words; leave acronyms, mixed case (unMind) and non-Latin text alone."""
    out = []
    for i, w in enumerate(t.split(" ")):
        core = w.lstrip("(\"'“")
        lead = w[: len(w) - len(core)]
        if core and core.islower() and core.isascii() and (i == 0 or core.rstrip(":,") not in SMALL_WORDS
                                                            or (out and out[-1].endswith(":"))):
            w = lead + core[0].upper() + core[1:]
        out.append(w)
    return " ".join(out)


def looks_like_person(s):
    words = s.replace(".", ". ").split()
    if not 1 <= len(words) <= 5 or re.search(r"\d", s):
        return False
    if any(w.lower().strip(",.") in NOT_NAME_WORDS for w in words):
        return False
    return all(w[0].isupper() for w in words if w[0].isalpha())


def clean_base(filename):
    base = re.sub(r"\.(epub|pdf|cbr|cbz|mobi|docx|pptx)$", "", filename, flags=re.I)
    base = re.sub(r"\.(pdf|epub)$", "", base, flags=re.I)                      # double extensions
    base = re.sub(r"libgen\.li|z-library|pdfdrive|-pdfread|\bpdfread\b", " ", base, flags=re.I)
    base = re.sub(r"\(\s*\d+\s*\)\s*$", "", base)                               # "(1)" copies
    base = base.replace("_-_", " - ").replace("__", ": ").replace("_ ", ": ").replace("_", " ")
    return base


def parse_filename(filename, known_authors=()):
    """Best-effort (title, author) from a Drive filename. Author 'Unknown' when it can't tell."""
    base = clean_base(filename)
    m = re.search(r"\{([^}]+)\}", base) or re.search(r"\[([a-z][a-z\- ]+)\]", base)   # "{Author}" / "[author-name]"
    tag_author = m.group(1).replace("-", " ").title() if m and not m.group(1).isdigit() else None
    base = re.sub(r"\[.*?\]|\(.*?\)|\{.*?\}", " ", base)
    base = re.sub(r"\s+", " ", base).strip(" -:")
    known = {norm(a) for a in known_authors}

    title, author = base, "Unknown"
    parts = [p.strip(" :") for p in re.split(r"\s+-\s+", base) if p.strip(" :")]
    if len(parts) >= 2:
        first, last = parts[0], parts[-1]
        def score(p):
            return (3 if norm(p) in known else 0) + (1 if looks_like_person(p) else 0)
        if score(first) > score(last):
            author, title = first, " - ".join(parts[1:])
        else:
            title, author = " - ".join(parts[:-1]), last
        title = title.replace(" - ", ": ", 1) if title.count(" - ") == 1 else title
    elif " by " in base.lower():
        idx = base.lower().rindex(" by ")
        title, author = base[:idx], base[idx + 4:]
    if tag_author and author == "Unknown":
        author = tag_author
    title = smart_title(re.sub(r"\s+", " ", title).strip(" -:"))
    author = re.sub(r"\s+", " ", author).strip(" -:") or "Unknown"
    return title, author
