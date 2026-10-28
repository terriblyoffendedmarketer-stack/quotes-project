#!/usr/bin/env python3
"""
sync_quote_bank_md.py — Regenerates content/quote-bank.md from content/quote-bank.json
Usage: python3 tools/sync_quote_bank_md.py
"""

import json
from pathlib import Path
from collections import OrderedDict

ROOT = Path(__file__).resolve().parent.parent
QB_JSON = ROOT / "content" / "quote-bank.json"
QB_MD = ROOT / "content" / "quote-bank.md"

def sync():
    with open(QB_JSON, "r", encoding="utf-8") as f:
        quotes = json.load(f)

    # Group by (author, work, year, translator)
    books = OrderedDict()
    for q in quotes:
        key = (q["author"], q["work"], q.get("year"), q.get("translator"))
        if key not in books:
            books[key] = []
        books[key].append(q)

    lines = [
        "# Master Quote Bank",
        "",
        "A personal anthology of memorable lines, working passages, and craft moments mined across the owner's library, curated to rekindle enthusiasm for unread books.",
        "",
        f"**Total Vetted Quotes:** {len(quotes)} | **Total Books Represented:** {len(books)}",
        "",
        "---",
        ""
    ]

    for (author, work, year, translator), b_quotes in books.items():
        year_str = f" ({year})" if year else ""
        lines.append(f"## {author}, {work}{year_str}")
        if translator:
            lines.append(f"*Trans. {translator}*")
        lines.append("")
        lines.append("| Line | Craft Job | Tags |")
        lines.append("|---|---|---|")
        for q in b_quotes:
            # Clean newlines for table cells
            q_clean = q["quote"].replace("\n", " ").replace("|", "\\|")
            hook_clean = q["hook"].replace("|", "\\|")
            tags_clean = ", ".join(q.get("tags", []))
            lines.append(f"| “{q_clean}” | {hook_clean} | {tags_clean} |")
        lines.append("")
        lines.append("---")
        lines.append("")

    QB_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Successfully synced {QB_MD}! {len(quotes)} quotes across {len(books)} books.")

if __name__ == "__main__":
    sync()
