"""Build the prototype page by inlining content/cards.json and content/quote-bank.json into prototype/template.html.

Usage: python3 tools/build_prototype.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
cards_path = ROOT / "content" / "cards.json"
bank_path = ROOT / "content" / "quote-bank.json"

cards = json.loads(cards_path.read_text())
bank = json.loads(bank_path.read_text()) if bank_path.exists() else []

for card in cards:
    for phrase in card.get("highlights", []):
        if phrase not in card["quote"]:
            raise SystemExit(f"{card['id']}: highlight not found in quote: {phrase!r}")

template = (ROOT / "prototype" / "template.html").read_text()
page = template.replace("/*CARDS*/[]", json.dumps(cards, ensure_ascii=False))
page = page.replace("/*QUOTE_BANK*/[]", json.dumps(bank, ensure_ascii=False))
(ROOT / "prototype" / "index.html").write_text(page)
print(f"Built prototype/index.html with {len(cards)} cards and {len(bank)} quote bank entries")
