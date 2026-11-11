# scripts/enrich_new_books.py — Verifies names and fetches cover + synopsis for books newly added to Drive
# Usage: python3 scripts/enrich_new_books.py [--all-missing]
#        default: only books flagged needs_enrichment / name_source="parsed" by the build
#        --all-missing: also retry every book that still has no cover or no synopsis
# Requires: network access to openlibrary.org, Python 3 standard library. Run the build again afterwards
#           (scripts/refresh_bookshelf.sh does both).
#
# Gotchas:
# - Filename parsing can't always tell "Author - Title" from "Title - Author". We search Open Library both ways
#   and keep whichever orientation actually matches a real book, then save the verified name to
#   content/book_names.json (keyed by Drive file id) so it never has to be guessed again.
# - Only adopt Open Library's title when it normalises to the same words as ours: it restores apostrophes and
#   casing ("Giovannis Room" -> "Giovanni's Room") without swapping in a different edition's subtitle.
# - Open Library descriptions sometimes carry markdown link junk ("([source][1])", "----") — stripped here.
# - Open Library stores many titles in lowercase; re-capitalise with smart_title() before adopting them.
# - Be polite: sequential requests with a short pause and a generic User-Agent (no personal details).

import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shelf_common import DATA_PATH, NAMES_PATH, load_json, norm, save_json, smart_title  # noqa: E402

UA = {"User-Agent": "MyReadingCorner-bookshelf/1.0 (personal library tool)"}


def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=12) as r:
        return json.loads(r.read().decode("utf-8"))


def search(title, author):
    params = {"title": title, "limit": 5, "fields": "key,title,author_name,cover_i,first_publish_year"}
    if author and author != "Unknown":
        params["author"] = author
    try:
        return get_json("https://openlibrary.org/search.json?" + urllib.parse.urlencode(params)).get("docs", [])
    except Exception as e:  # network hiccup: skip this book, try next run
        print(f"    ! search failed: {e}")
        return []


def main_title(t):
    return norm(re.split(r"[:(]", t)[0])


def best_match(docs, title, author):
    a_tokens = {x for x in norm(author).split() if len(x) > 2}
    for d in docs:
        if main_title(d.get("title", "")) != main_title(title):
            continue
        names = norm(" ".join(d.get("author_name", [])))
        if not a_tokens or a_tokens & set(names.split()):
            return d
    return None


def clean_description(text):
    text = re.split(r"\n-{3,}|\n\*\*\*|\nContains:", text)[0]
    text = re.sub(r"\(\[[^\]]*\]\[\d+\]\)|\[([^\]]+)\]\[\d+\]|\[\d+\]: \S+", r"\1", text)
    text = re.sub(r"\s+\n", "\n", text).strip()
    if len(text) > 900:
        cut = text[:900].rsplit(". ", 1)[0]
        text = cut + "."
    return text


def description(work_key):
    try:
        w = get_json(f"https://openlibrary.org{work_key}.json")
    except Exception:
        return ""
    d = w.get("description", "")
    return clean_description(d.get("value", "") if isinstance(d, dict) else d or "")


def enrich(b):
    title, author = b["title"], b["author"]
    doc = best_match(search(title, author), title, author)
    swapped = False
    if not doc and b.get("name_source") == "parsed" and author != "Unknown":
        doc = best_match(search(author, title), author, title)       # maybe it was "Author - Title"
        swapped = bool(doc)
        time.sleep(0.4)
    if not doc:
        return False
    if swapped:
        title, author = author, title
    if main_title(doc["title"]) == main_title(title) and ":" not in title:
        title = smart_title(doc["title"])   # OL often stores titles lowercase ("A simple plan")
    if doc.get("author_name"):
        ol_author = doc["author_name"][0]
        if set(norm(author).split()) & set(norm(ol_author).split()) or author == "Unknown":
            author = ol_author if author == "Unknown" or norm(ol_author).replace(" ", "") == norm(author).replace(" ", "") \
                or len(ol_author) > len(author) else author
    b["title"], b["author"] = title, author
    if doc.get("cover_i") and not b.get("cover_url") and not b.get("no_cover"):
        b["cover_url"] = f"https://covers.openlibrary.org/b/id/{doc['cover_i']}-L.jpg"
    if not b.get("pitch"):
        time.sleep(0.3)
        b["pitch"] = description(doc["key"])
    return True


def main():
    retry_all = "--all-missing" in sys.argv
    books = load_json(DATA_PATH, [])
    names = load_json(NAMES_PATH, {})
    todo = [b for b in books if b.get("needs_enrichment") or b.get("name_source") == "parsed"
            or (retry_all and ((not b.get("cover_url") and not b.get("no_cover")) or not b.get("pitch")))]
    print(f"Enriching {len(todo)} book(s) via Open Library...")
    for b in todo:
        before = (b["title"], b["author"])
        ok = enrich(b)
        flag = "ok " if ok else "-- "
        change = f"  (was {before[0]} — {before[1]})" if (b["title"], b["author"]) != before else ""
        print(f"  {flag}{b['title']} — {b['author']}{change}  cover={'y' if b.get('cover_url') else 'n'} synopsis={'y' if b.get('pitch') else 'n'}")
        names[b["drive_id"]] = {"title": b["title"], "author": b["author"]}   # verified or best guess: pin it
        b.pop("name_source", None)
        b.pop("needs_enrichment", None)
        b["enriched"] = date.today().isoformat()
        time.sleep(0.4)
    save_json(DATA_PATH, books)
    save_json(NAMES_PATH, names, sort_keys=True)
    print("Done. Rebuild to publish: python3 scripts/build_independent_bookshelf_app.py")


if __name__ == "__main__":
    main()
