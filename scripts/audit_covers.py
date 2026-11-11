# scripts/audit_covers.py — Finds (and optionally fixes) wrong book covers on My Reading Corner
# Usage: python3 scripts/audit_covers.py            # audit only: writes content/cover_audit.md
#        python3 scripts/audit_covers.py --fix      # also replace proven-wrong covers in content/book_overrides.json
# Requires: network access to openlibrary.org, Python 3 standard library. Rebuild afterwards.
#
# How a cover is judged (current cover = Open Library cover id N):
#   OK       — N is one of the covers attached to the Open Library WORK that matches this title + author
#   WRONG    — a matching work exists but N isn't among its covers (old pipeline guessed from a loose search,
#              so e.g. a study guide's or a different book's cover got attached). --fix swaps in the work's
#              own cover, or the typographic jacket if the work has none.
#   UNKNOWN  — no confident title+author match on Open Library; left alone and listed for a manual look.
#
# Gotchas:
# - Covers set by hand in book_overrides.json (cover_url) are trusted and never touched.
# - Work "covers" lists can be long and include translations; membership is what counts, not position.
# - Results are cached in content/cover_audit_cache.json, so re-runs only query new/changed books.

import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shelf_common import CONTENT, DATA_PATH, OVERRIDES_PATH, load_json, save_json  # noqa: E402
from enrich_new_books import best_match, get_json, main_title, search  # noqa: E402

CACHE = CONTENT / "cover_audit_cache.json"
REPORT = CONTENT / "cover_audit.md"
L = "https://covers.openlibrary.org/b/id/{}-L.jpg"


def cover_id(url):
    m = re.search(r"/b/id/(\d+)", url or "")
    return int(m.group(1)) if m else None


def work_info(title, author, cache):
    key = f"{title}|{author}"
    if key not in cache:
        a = "" if author in ("Anonymous", "Various Authors", "Unknown") else re.sub(r"\(.*?\)", "", author)
        doc = best_match(search(main_title(title) if ":" in title else title, a), title, a)
        info = None
        if doc:
            covers = []
            try:
                covers = [c for c in get_json(f"https://openlibrary.org{doc['key']}.json").get("covers", []) if c and c > 0]
            except Exception:
                return None                  # network trouble: undecided, retry next run (not cached)
            info = {"work": doc["key"], "cover_i": doc.get("cover_i"), "covers": covers}
            time.sleep(0.3)
        cache[key] = info
        save_json(CACHE, cache)
        time.sleep(0.3)
    return cache[key]


def main():
    fix = "--fix" in sys.argv
    books = load_json(DATA_PATH, [])
    ov = load_json(OVERRIDES_PATH, {"books": {}})
    cache = load_json(CACHE, {})
    rows = {"WRONG": [], "UNKNOWN": [], "OK": []}
    for i, b in enumerate(books):
        cid = cover_id(b.get("cover_url"))
        if not cid or "cover_url" in ov["books"].get(b["id"], {}):
            continue
        info = work_info(b["title"], b["author"], cache)
        if info is None:
            rows["UNKNOWN"].append((b, None))
        elif cid in info["covers"] or cid == info.get("cover_i"):
            rows["OK"].append((b, info))
        else:
            rows["WRONG"].append((b, info))
        if i % 50 == 0:
            print(f"  ...{i}/{len(books)}", flush=True)

    fixed = 0
    if fix:
        for b, info in rows["WRONG"]:
            new = info.get("cover_i") or (info["covers"][0] if info["covers"] else None)
            entry = ov["books"].setdefault(b["id"], {})
            if new:
                entry["cover_url"] = L.format(new)
            else:
                entry["cover_url"], entry["no_cover"] = None, True
            fixed += 1
        save_json(OVERRIDES_PATH, ov)

    lines = ["# Cover audit", "", f"OK: {len(rows['OK'])} · wrong: {len(rows['WRONG'])}"
             f"{' (fixed)' if fix else ''} · unverifiable: {len(rows['UNKNOWN'])}", "",
             "## Wrong covers (cover doesn't belong to the matching Open Library work)", ""]
    for b, info in rows["WRONG"]:
        new = info.get("cover_i")
        lines.append(f"- **{b['title']}** — {b['author']}: had {b.get('cover_url')} → "
                     f"{L.format(new) if new else 'typographic jacket'} (work {info['work']})")
    lines += ["", "## Unverifiable (no confident Open Library match — check by eye)", ""]
    lines += [f"- **{b['title']}** — {b['author']}: {b.get('cover_url')}" for b, _ in rows["UNKNOWN"]]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"OK {len(rows['OK'])}, wrong {len(rows['WRONG'])}{f' ({fixed} fixed)' if fix else ''}, "
          f"unverifiable {len(rows['UNKNOWN'])} -> {REPORT.relative_to(CONTENT.parent)}")


if __name__ == "__main__":
    main()
