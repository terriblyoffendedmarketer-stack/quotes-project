# run_batch.py — Mines quotes across a batch of EPUBs using local gemma3:4b
# Usage: python3 scripts/run_batch.py
#
# Gotchas:
# - Runs locally against Ollama on port 11434.
# - Appends output directly to content/batch_results.json.

import json
from pathlib import Path
import sys

# Import mine_epub from mine_quote_bank
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mine_quote_bank import mine_epub

SCRATCH = Path("/Users/apple/.gemini/antigravity/brain/6282abf0-33f0-44df-ac5d-1d65c90f0f65/scratch")
OUT_FILE = Path("/Users/apple/Documents/Claude Code/quotes-project/content/batch_2_raw.json")

BATCH = [
    {
        "epub": SCRATCH / "What_I_Talk_About_When_I_Talk_About_Running_-_Haruki_Murakami.epub",
        "author": "Haruki Murakami",
        "title": "What I Talk About When I Talk About Running",
        "year": 2007,
        "translator": "Philip Gabriel",
        "chunks": 7,
    },
    {
        "epub": SCRATCH / "Cats_Cradle_-_Kurt_Vonnegut_Jr.epub",
        "author": "Kurt Vonnegut",
        "title": "Cat's Cradle",
        "year": 1963,
        "translator": None,
        "chunks": 7,
    },
    {
        "epub": SCRATCH / "Auster, Paul - The Invention of Solitude (2007, Penguin (Non-Classics)) - libgen.li.epub",
        "author": "Paul Auster",
        "title": "The Invention of Solitude",
        "year": 1982,
        "translator": None,
        "chunks": 7,
    },
    {
        "epub": SCRATCH / "Meditations for Mortals_ Four Weeks to Embrace Your Limitations and Make Time for What Counts{Oliver Burkeman}(2024, Farrar, Straus and Giroux){107217730} libgen.li.epub",
        "author": "Oliver Burkeman",
        "title": "Meditations for Mortals",
        "year": 2024,
        "translator": None,
        "chunks": 7,
    },
]

def main():
    all_results = []
    for item in BATCH:
        p = item["epub"]
        if not p.exists():
            print(f"Skipping missing: {p}")
            continue

        print(f"\n==========================================")
        print(f"Mining: {item['title']} by {item['author']}")
        print(f"==========================================")
        quotes = mine_epub(
            str(p),
            item["author"],
            item["title"],
            item["year"],
            item["translator"],
            max_chunks=item["chunks"]
        )
        print(f"Found {len(quotes)} quotes from {item['title']}")
        all_results.extend(quotes)

    OUT_FILE.write_text(json.dumps(all_results, indent=2, ensure_ascii=False))
    print(f"\nCompleted Batch! Wrote {len(all_results)} quotes to {OUT_FILE}")

if __name__ == "__main__":
    main()
