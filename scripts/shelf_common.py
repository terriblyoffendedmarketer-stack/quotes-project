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
    # download-site watermarks: "OceanofPDF.com_", "(z-library.sk, 1lib.sk, z-lib.sk)", "dokumen.pub_", "[Anna's Archive]"
    base = re.sub(r"(?:www\.)?[a-z0-9-]+\.(?:com|org|net|pub|sk|li|se|io|to|ru|ws|cc|me|lol|is|gs|rs|ec)(?![a-z])",
                  " ", base, flags=re.I)
    base = re.sub(r"libgen|z-library|z-lib|\b1lib\b|pdfdrive|-pdfread|\bpdfread\b|anna[’']?s archive|ebook-hunter|"
                  r"oceanofpdf|\bwww\b", " ", base, flags=re.I)
    base = re.sub(r"[(\[]\s*[,;\s]*[)\]]", " ", base)                         # brackets left empty by the above
    core = base.strip(" _-")
    if " " not in core and "_" not in core and core.count("-") >= 2:
        base = core.replace("-", " ")                                            # "atomic-habits-james-clear"
    base = re.sub(r"\)?\s*(?:pdf|epub)\s*$", lambda m: ")" if m.group(0).startswith(")") else "", base, flags=re.I)
    base = re.sub(r"\(\s*\d+\s*\)\s*$", "", base)                               # "(1)" copies
    base = base.replace("_-_", " - ").replace("__", ": ").replace("_ ", ": ").replace("_", " ")
    return re.sub(r"\s+", " ", base).strip(" :.-")


def parse_filename(filename, known_authors=()):
    """Best-effort (title, author) from a Drive filename. Author 'Unknown' when it can't tell."""
    base = clean_base(filename)
    m = re.search(r"\{([^}]+)\}", base) or re.search(r"\[([a-z][a-z\- ]+)\]", base)   # "{Author}" / "[author-name]"
    tag_author = m.group(1).replace("-", " ").title() if m and not m.group(1).isdigit() else None
    if not tag_author:                                       # "Klara and the Sun (Kazuo Ishiguro)"
        tag_author = next((p.strip() for p in re.findall(r"\(([^)]+)\)", base) if looks_like_person(p.strip())
                           and len(p.split()) >= 2 and not re.search(r"(?i)\b(issue|vol|volume|part|edition|book|series|"
                                                                      r"complete|collection|digital|omnibus)\b", p)), None)
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
        if len(base[idx + 4:].strip()) >= 3:                 # not "...Translated by G" (truncated names)
            title, author = base[:idx], base[idx + 4:]
            author = author.title() if author.islower() else author
    if tag_author and author == "Unknown":
        author = tag_author
    title = smart_title(re.sub(r"\s+", " ", title).strip(" -:"))
    author = re.sub(r"\s+", " ", author).strip(" -:") or "Unknown"
    return title, author


def drive_unchanged(path, data_md5):
    """True if the Drive file at gdrive:Books/<path> still has exactly the bytes we downloaded (same md5).
    Called right before uploading a cleaned file, so a book you replaced or edited mid-run is never overwritten."""
    import subprocess
    r = subprocess.run(["rclone", "lsjson", "--hash", "--hash-type", "md5", f"gdrive:Books/{path}"],
                       capture_output=True, text=True)
    try:
        info = json.loads(r.stdout)[0]
    except Exception:
        return False
    return info.get("Hashes", {}).get("md5") == data_md5
