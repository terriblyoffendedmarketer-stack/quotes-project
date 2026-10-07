"""Append cards from a JSON file to content/cards.json, refusing duplicates and bad highlights.

Usage: python3 tools/add_cards.py new_cards.json
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
path = ROOT / "content" / "cards.json"
cards = json.loads(path.read_text())
new = json.loads(Path(sys.argv[1]).read_text())
ids = {c["id"] for c in cards}
for card in new:
    if card["id"] in ids:
        raise SystemExit(f"duplicate id {card['id']}")
    for h in card["highlights"]:
        if h not in card["quote"]:
            raise SystemExit(f"{card['id']}: highlight not in quote: {h!r}")
    card.setdefault("translator", None)
    ids.add(card["id"])
path.write_text(json.dumps(cards + new, ensure_ascii=False, indent=2) + "\n")
print(f"Added {len(new)} cards, {len(cards) + len(new)} total")
