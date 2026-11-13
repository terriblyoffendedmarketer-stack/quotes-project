# check_synopses.py — Finds shelf synopses that describe the WRONG book (e.g. War and Peace showing Anna
#                     Karenina's blurb) and replaces them with a verified one
# Usage: python3 scripts/check_synopses.py            # check (cached) -> content/synopsis_check.md, no changes
#        python3 scripts/check_synopses.py --apply    # also write replacements into content/book_overrides.json
#        python3 scripts/check_synopses.py --only "war and peace"
# Requires: `anthropic` Python SDK (installed for Homebrew python3), ANTHROPIC_API_KEY in project .env,
#           content/cover_sourcing.json from scripts/source_covers.py (Apple Books + in-file descriptions),
#           openlibrary.org. Rebuild the shelf afterwards. A full run costs well under $2.
#
# How: Claude reads title + author + synopsis (15 books per request) and says right book / wrong book /
# not a synopsis / not English. For anything not "right", candidate texts are tried in order — Apple Books
# description of the matched edition, the description inside the EPUB, Open Library's — and the first one
# Claude confirms is used. If none passes, the synopsis is blanked (better empty than about another book).
#
# Gotchas:
# - Synopses the user typed in the app (pitch_source "user" in book_overrides.json) are never touched.
# - Verdicts are cached per text in .cache/synopsis_verdicts.json (sha1 of title|author|text), so re-runs
#   only pay for new or changed synopses.
# - Claude Opus 5.5 can't disable thinking; effort "low" keeps it quick and cheap for this yes/no job.

import hashlib
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shelf_common import CONTENT, DATA_PATH, OVERRIDES_PATH, ROOT, load_json, save_json  # noqa: E402

CACHE_PATH = ROOT / ".cache" / "synopsis_verdicts.json"
SOURCING = CONTENT / "cover_sourcing.json"
REPORT = CONTENT / "synopsis_check.md"
MODEL = "claude-opus-5-5"
BATCH = 15
UA = {"User-Agent": "MyReadingCorner-bookshelf/1.0 (personal library tool)"}

SCHEMA = {
    "type": "object",
    "properties": {"results": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "n": {"type": "integer"},
            "verdict": {"type": "string", "enum": ["right", "wrong_book", "not_a_synopsis", "not_english", "unsure"]},
            "actually_about": {"type": "string"},
        },
        "required": ["n", "verdict", "actually_about"],
        "additionalProperties": False}}},
    "required": ["results"],
    "additionalProperties": False,
}
PROMPT = """You check a personal bookshelf. For each numbered item: does the text describe THIS book (title + author given)?

verdict:
- right: it is a synopsis/blurb/description of this book (publisher blurbs, review quotes about this book and translator notes are fine)
- wrong_book: it describes a different book (say which in actually_about) - e.g. a War and Peace entry whose text is about Anna Karenina
- not_a_synopsis: generic filler that could fit any book, a table of contents, a bare list, a placeholder, or about the author only
- not_english: mainly not in English
- unsure: you genuinely can't tell (obscure book and nothing contradicts it)
Judge by content: character names, plot, subject. Be strict about wrong_book; don't flag a right blurb because it's promotional.
actually_about: short, e.g. "Anna Karenina by Tolstoy", or "" if right.

"""


def env_key():
    for line in (ROOT / ".env").read_text().splitlines():
        if line.startswith("ANTHROPIC_API_KEY="):
            return line.split("=", 1)[1].strip()
    sys.exit("ANTHROPIC_API_KEY missing from .env")


def clean(text, limit=1400):
    text = html.unescape(re.sub(r"<[^>]+>", " ", text or ""))
    text = re.sub(r"[ \t\r\f\v]+", " ", re.sub(r"\n\s*\n+", "\n\n", text)).strip()
    if len(text) > limit:
        cut = text[:limit]
        text = cut[:max(cut.rfind(". "), cut.rfind(".\n")) + 1] or cut
    return text


def key(b, text):
    return hashlib.sha1(f"{b['title']}|{b.get('author')}|{text}".encode()).hexdigest()


def classify(client, items, cache):
    """items: [(book, text)] -> fills cache[key] = {verdict, actually_about}"""
    todo = [(b, t) for b, t in items if t and key(b, t) not in cache]
    for i in range(0, len(todo), BATCH):
        chunk = todo[i:i + BATCH]
        body = PROMPT + "\n\n".join(f"[{n}] TITLE: {b['title']}\nAUTHOR: {b.get('author') or 'unknown'}\nTEXT: {t[:1200]}"
                                    for n, (b, t) in enumerate(chunk))
        for attempt in range(4):
            try:
                r = client.messages.create(model=MODEL, max_tokens=8000, output_config={
                    "effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}},
                    messages=[{"role": "user", "content": body}])
                if r.stop_reason == "refusal":
                    raise RuntimeError("refusal")
                res = json.loads(next(x.text for x in r.content if x.type == "text"))["results"]
                break
            except (anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.InternalServerError):
                time.sleep(10 * (attempt + 1))
        else:
            print("  batch failed, skipping")
            continue
        for row in res:
            if 0 <= row["n"] < len(chunk):
                b, t = chunk[row["n"]]
                cache[key(b, t)] = {"verdict": row["verdict"], "actually_about": row["actually_about"]}
        save_json(CACHE_PATH, cache)
        print(f"  checked {min(i + BATCH, len(todo))}/{len(todo)}", flush=True)


def openlibrary_desc(b):
    try:
        q = urllib.parse.urlencode({"title": re.split(r"[:(]", b["title"])[0], "author": "" if "nknown" in (b.get("author") or "") else b.get("author", ""),
                                    "limit": 3, "fields": "key"})
        with urllib.request.urlopen(urllib.request.Request(f"https://openlibrary.org/search.json?{q}", headers=UA), timeout=15) as r:
            docs = json.loads(r.read())["docs"]
        for d in docs[:2]:
            with urllib.request.urlopen(urllib.request.Request(f"https://openlibrary.org{d['key']}.json", headers=UA), timeout=15) as r:
                w = json.loads(r.read())
            desc = w.get("description")
            desc = desc.get("value") if isinstance(desc, dict) else desc
            if desc and len(desc) > 80:
                return re.split(r"\n-{3,}|\n\*\*\*|\nContains:", desc)[0]
    except Exception:
        pass
    return ""


def main():
    args = sys.argv[1:]
    apply = "--apply" in args
    only = args[args.index("--only") + 1].lower() if "--only" in args else None
    client = anthropic.Anthropic(api_key=env_key())
    books = load_json(DATA_PATH, [])
    if only:
        books = [b for b in books if only in b["title"].lower()]
    overrides = load_json(OVERRIDES_PATH, {"books": {}})
    ob = overrides.setdefault("books", {})
    sourcing = {r["id"]: r for r in load_json(SOURCING, [])}
    cache = load_json(CACHE_PATH, {})
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)

    books = [b for b in books if (ob.get(b["id"]) or {}).get("pitch_source") != "user"]
    print(f"Checking {len(books)} synopses…")
    classify(client, [(b, clean(b.get("pitch"))) for b in books], cache)

    bad = [b for b in books if not clean(b.get("pitch")) or cache.get(key(b, clean(b.get("pitch"))), {}).get("verdict")
           in ("wrong_book", "not_a_synopsis", "not_english")]
    print(f"{len(bad)} need a new synopsis; gathering candidates…")
    cands = {}
    for b in bad:
        s = sourcing.get(b["id"], {})
        opts = [("Apple Books", clean(s.get("trusted_desc"))), ("book file", clean(s.get("epub_desc")))]
        cands[b["id"]] = [(src, t) for src, t in opts if len(t) > 80]
    classify(client, [(b, t) for b in bad for _, t in cands[b["id"]]], cache)
    for b in bad:      # Open Library only when the others didn't pass (slow, one lookup per book)
        if not any(cache.get(key(b, t), {}).get("verdict") == "right" for _, t in cands[b["id"]]):
            t = clean(openlibrary_desc(b))
            if len(t) > 80:
                cands[b["id"]].append(("Open Library", t))
    classify(client, [(b, t) for b in bad for _, t in cands[b["id"]]], cache)

    rows = []
    for b in bad:
        old = clean(b.get("pitch"))
        v = cache.get(key(b, old), {"verdict": "empty", "actually_about": ""}) if old else {"verdict": "empty", "actually_about": ""}
        pick = next(((src, t) for src, t in cands[b["id"]] if cache.get(key(b, t), {}).get("verdict") == "right"), None)
        rows.append((b, v, pick))
        if apply:
            o = ob.setdefault(b["id"], {})
            o["pitch"] = pick[1] if pick else ""
            o["pitch_source"] = f"verified ({pick[0]})" if pick else "blanked (no verified synopsis found)"
    lines = [f"# Synopsis check — {time.strftime('%Y-%m-%d')}", "",
             f"{len(books)} checked, {len(bad)} wrong/unusable. Replaced: {sum(1 for r in rows if r[2])}, "
             f"blanked: {sum(1 for r in rows if not r[2])}.", "",
             "| Book | Problem | Actually about | New synopsis from |", "|---|---|---|---|"]
    lines += [f"| {b['title']} — {b.get('author')} | {v['verdict']} | {v['actually_about']} | {p[0] if p else '— (blank)'} |"
              for b, v, p in rows]
    unsure = [b for b in books if cache.get(key(b, clean(b.get("pitch"))), {}).get("verdict") == "unsure"]
    if unsure:
        lines += ["", "Unsure (left as is): " + "; ".join(b["title"] for b in unsure)]
    REPORT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[2:3]))
    if apply:
        save_json(OVERRIDES_PATH, overrides)
        print("Applied to book_overrides.json — now rebuild the shelf.")


if __name__ == "__main__":
    main()
