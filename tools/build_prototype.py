"""Build the prototype page by inlining content/cards.json into prototype/template.html.

Usage: python3 build.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
cards = json.loads((ROOT / "content" / "cards.json").read_text())

for card in cards:
    for phrase in card["highlights"]:
        if phrase not in card["quote"]:
            raise SystemExit(f"{card['id']}: highlight not found in quote: {phrase!r}")

template = (ROOT / "prototype" / "template.html").read_text()
page = template.replace("/*CARDS*/[]", json.dumps(cards, ensure_ascii=False))
(ROOT / "prototype" / "index.html").write_text(page)
print(f"Built prototype/index.html with {len(cards)} cards")
