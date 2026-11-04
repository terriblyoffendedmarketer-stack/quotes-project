#!/usr/bin/env python3
# scripts/patch_specific_book_metadata.py — Fixes specific titles, author attributions, covers, and resolves missing jackets
# Usage: python3 scripts/patch_specific_book_metadata.py

import json
import re
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "bookshelf" / "data.json"
COVERS_CACHE_PATH = ROOT / "content" / "covers_cache.json"

MANUAL_FIXES = {
    "ben-goldacre-bad-pharma": {
        "title": "Bad Pharma: How Drug Companies Mislead Doctors and Harm Patients",
        "author": "Ben Goldacre",
        "category": "Philosophy, Essays & Misc",
        "cover_url": "https://covers.openlibrary.org/b/id/7289568-L.jpg",
        "pitch": "We like to imagine that medicine is based on evidence and the results of fair clinical trials. In reality, those tests are conducted by the pharmaceutical companies themselves, who frequently bury negative trials, conduct flawed studies with tiny participant groups, and distort research to market ineffective and dangerous drugs to doctors and patients.",
        "tags": ["medicine", "investigative", "science", "healthcare", "pharma"],
        "why_love": (
            "Ben Goldacre is the scourge of medical quackery and institutional deceit. In Bad Pharma, he lays bare the systemic corruption "
            "of clinical drug trials: how negative results are buried, how regulatory agencies are captured, and how doctors are misled into "
            "prescribing expensive, ineffective treatments to real patients. A furious, meticulously footnoted exposé that every scientifically "
            "minded citizen needs on their shelf."
        )
    },
    "ben-goldacre-bad-science": {
        "title": "Bad Science: Quacks, Hacks, and Big Pharma Flacks",
        "author": "Ben Goldacre",
        "category": "Philosophy, Essays & Misc",
        "cover_url": "https://covers.openlibrary.org/b/id/6680603-L.jpg",
        "pitch": "Full of spleen, this is a hilarious, invigorating and informative journey through the world of bad science. When Dr. Ben Goldacre saw someone on daytime TV dipping her feet in an 'Aqua Detox' footbath and releasing brown sludge, he tested it with a Barbie doll and salt water. An essential takedown of homeopaths, nutritionist gurus, and tabloid scaremongers.",
        "tags": ["pseudoscience", "critical-thinking", "media-literacy", "humor"],
        "why_love": (
            "Ben Goldacre opened his book with a Barbie doll sitting in a tub of brown sludge, and I have never trusted a footbath since. "
            "That opening is the whole book in miniature: a deadpan, slightly unhinged experiment, a flash of spleen, and then a sudden turn toward "
            "the serious business of asking how anyone knows what they claim to know. Reading it feels like being taken by the collar by a friend "
            "who happens to be a doctor and refuses to let you swallow a claim without checking the numbers."
        )
    },
    "how-to-research-anything-unknown": {
        "title": "How to Research Anything",
        "author": "Curated Dossier / Research Heuristics",
        "category": "Philosophy, Essays & Misc",
        "cover_url": None, # Strips incorrect poster; uses sleek typographic card
        "pitch": "A curated compendium of advanced web intelligence, investigative research workflows, search heuristics, and OSINT methodologies gathered from investigative journalists and research practitioners across the web.",
        "tags": ["research", "osint", "investigation", "methodology", "web-intelligence"],
        "why_love": (
            "This isn't a single corporate manual written by a single academic; it's a battle-tested compilation of heuristics, investigative workflows, "
            "and search tools gathered across the best research communities on the web. It belongs here as a practical field handbook for anyone who "
            "needs to cut through algorithmic clutter and find verifiable truth."
        )
    },
    "how-to-win-at-chess-1-levy-rozman": {
        "title": "How to Win at Chess: The Ultimate Guide for Beginners and Beyond",
        "author": "Levy Rozman (GothamChess)",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/14135096-L.jpg",
        "pitch": "YouTube's favorite chess educator, International Master Levy Rozman, demystifies the 64 squares with accessible, humorous, and ruthlessly practical lessons covering opening traps, positional control, and endgames.",
        "tags": ["chess", "strategy", "games", "tactics"],
        "why_love": (
            "Levy Rozman did what generations of Soviet grandmasters failed to do: he made chess strategy feel kinetic, hilarious, and genuinely fun. "
            "Instead of burying beginners in dry algebraic notation, he breaks down the psychology of mistakes, the joy of punishing blunders, "
            "and the fundamental habits that actually raise your rating. Pure chess joy."
        )
    },
    "how-to-win-at-chess-2-next-level-levy-rozman": {
        "title": "How to Win at Chess 2: Next Level",
        "author": "Levy Rozman (GothamChess)",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/14135096-L.jpg",
        "pitch": "The follow-up masterclass expanding into intermediate opening repertoires, piece sacrifice evaluations, middlegame planning, and calculation techniques.",
        "tags": ["chess", "strategy", "games", "tactics", "intermediate"],
        "why_love": (
            "Taking players beyond the beginner plateau, this second volume focuses on the murky middlegame where games are won and lost. "
            "Rozman teaches you how to form a coherent attack, spot tactical patterns under pressure, and think two moves ahead without getting paralyzed."
        )
    },
    "intimacy-trusting-oneself-and-the-other-by-osho": {
        "title": "Intimacy: Trusting Oneself and the Other",
        "author": "Osho",
        "category": "Philosophy, Essays & Misc",
        "cover_url": "https://covers.openlibrary.org/b/id/177935-L.jpg",
        "pitch": "An uncompromising exploration of why human beings crave profound connection yet run in terror from genuine vulnerability, revealing how fear of exposure and self-rejection undermine our closest relationships.",
        "tags": ["philosophy", "intimacy", "psychology", "vulnerability"],
        "why_love": (
            "Osho cuts through romantic sentimentalism to expose the fundamental paradox of modern relationships: we want to be loved deeply, "
            "yet we armor ourselves behind masks and performative control to keep from being seen. A provocative, meditative reflection on "
            "dropping defense mechanisms and learning to trust your own soul before demanding it from another."
        )
    },
    "barabara-oakley-a-mind-for-numbers": {
        "title": "A Mind for Numbers: How to Excel at Math and Science",
        "author": "Barbara Oakley",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/8352403-L.jpg"
    },
    "david-allen-getting-things-done-unknown": {
        "title": "Getting Things Done: The Art of Stress-Free Productivity",
        "author": "David Allen",
        "category": "Marketing & Strategy",
        "cover_url": "https://covers.openlibrary.org/b/id/109288-L.jpg"
    },
    "ed-catmull-amy-wallace-creativity-inc-overcoming-the-unseen-forces-that-stand-in-the-way-of-true-inspiration-libgen-li": {
        "title": "Creativity, Inc.: Overcoming the Unseen Forces That Stand in the Way of True Inspiration",
        "author": "Ed Catmull & Amy Wallace",
        "category": "Marketing & Strategy",
        "cover_url": "https://covers.openlibrary.org/b/id/13124793-L.jpg"
    },
    "master-shots-100-advanced-camera-techniques-to-get-an-expensive-look-on-your-low-budget-movie-unknown": {
        "title": "Master Shots: 100 Advanced Camera Techniques",
        "author": "Christopher Kenworthy",
        "category": "Cinema & Film Craft",
        "cover_url": "https://covers.openlibrary.org/b/id/7104834-L.jpg"
    },
    "40-rules-of-love-elif-shafak": {
        "title": "The Forty Rules of Love",
        "author": "Elif Shafak",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/9078986-L.jpg"
    },
    "everybody-lies-seth-stephens-davidowitz": {
        "title": "Everybody Lies: Big Data, New Data, and What the Internet Can Tell Us About Who We Really Are",
        "author": "Seth Stephens-Davidowitz",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/8294628-L.jpg"
    },
    "alex-verus-1-fated-benedict-jacka": {
        "title": "Fated (Alex Verus #1)",
        "author": "Benedict Jacka",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/7367355-L.jpg"
    },
    "a-self-help-guide-for-copywriters-dan-nelken": {
        "title": "A Self-Help Guide for Copywriters",
        "author": "Dan Nelken",
        "category": "Marketing & Strategy",
        "cover_url": "https://covers.openlibrary.org/b/id/12838741-L.jpg"
    },
    "chess-for-zebras-jonathan-rowson": {
        "title": "Chess for Zebras: Thinking Differently About Black and White",
        "author": "Jonathan Rowson",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/2144888-L.jpg"
    },
    "mikhail-tal-the-life-and-games-of-mikhail-tal-2012-everyman-chess-libgen-li": {
        "title": "The Life and Games of Mikhail Tal",
        "author": "Mikhail Tal",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/7946850-L.jpg"
    }
}

def clean_title_author_for_search(title, author):
    # Strip libgen, noisy prefixes/suffixes
    t = re.sub(r"libgen\.li|libgen|\(20\d\d.*?\)|\{.*?\}", "", title, flags=re.I)
    t = re.sub(r"^[A-Z][a-z]+ [A-Z][a-z]+ - ", "", t) # remove Author - prefix from title
    t = re.sub(r"[_\-]+", " ", t).strip()
    
    a = re.sub(r"libgen\.li|libgen|\(dir\..*?\)|Unknown", "", author, flags=re.I).strip()
    return t, a

def search_openlibrary_cover(clean_title, clean_author):
    query = f"{clean_title} {clean_author}".strip()
    if not query:
        return None
    url = f"https://openlibrary.org/search.json?q={urllib.parse.quote(query)}&limit=3"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "QuotesShelf/2.0"})
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode())
            for d in data.get("docs", []):
                if "cover_i" in d:
                    return f"https://covers.openlibrary.org/b/id/{d['cover_i']}-L.jpg"
    except Exception:
        pass
    return None

def main():
    if not DATA_PATH.exists():
        print("Data path not found.")
        return

    books = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    covers_cache = json.loads(COVERS_CACHE_PATH.read_text(encoding="utf-8")) if COVERS_CACHE_PATH.exists() else {}

    patched_manual = 0
    new_covers_found = 0

    for b in books:
        bid = b.get("id")

        # Apply specific manual fixes
        if bid in MANUAL_FIXES:
            fix = MANUAL_FIXES[bid]
            for k, v in fix.items():
                b[k] = v
            patched_manual += 1
            print(f"✓ Patched manual fix: {b['title']} by {b['author']}")

        # If book still has no cover, attempt search
        if not b.get("cover_url"):
            ct, ca = clean_title_author_for_search(b.get("title", ""), b.get("author", ""))
            cache_key = f"{ct}|{ca}"
            if cache_key in covers_cache and covers_cache[cache_key]:
                b["cover_url"] = covers_cache[cache_key]
                new_covers_found += 1
            else:
                found_url = search_openlibrary_cover(ct, ca)
                if found_url:
                    b["cover_url"] = found_url
                    covers_cache[cache_key] = found_url
                    new_covers_found += 1
                    print(f"  + Found cover for: {b['title']} -> {found_url}")

    DATA_PATH.write_text(json.dumps(books, indent=2, ensure_ascii=False), encoding="utf-8")
    if covers_cache:
        COVERS_CACHE_PATH.write_text(json.dumps(covers_cache, indent=2), encoding="utf-8")

    print(f"\nDone! Patched {patched_manual} specific titles.")
    print(f"Resolved {new_covers_found} new covers. Books with covers now: {sum(1 for b in books if b.get('cover_url'))} / {len(books)}")

if __name__ == "__main__":
    main()
