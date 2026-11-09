# dump_all_steal_its.py — Prints all 113 stealIt entries from content/cards.json for thorough craft review
# Usage: python3 scripts/dump_all_steal_its.py
# Requires: json, pathlib

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARDS_FILE = ROOT / "content" / "cards.json"

with open(CARDS_FILE, "r", encoding="utf-8") as f:
    cards = json.load(f)

for i, card in enumerate(cards):
    cid = card.get("id")
    author = card.get("author")
    work = card.get("work")
    job = card.get("job")
    steal = card.get("stealIt")
    print(f"{i+1:03d}. [{cid}] {author} — {work}")
    print(f"     Job: {job}")
    print(f"     Steal: {steal}\n")
