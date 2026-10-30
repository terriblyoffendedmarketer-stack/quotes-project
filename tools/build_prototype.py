"""Build the web and prototype pages by inlining content/cards.json and content/quote-bank.json into prototype/template.html.
Outputs to both prototype/index.html (for local visual studio) and docs/index.html (for GitHub Pages).

Usage: python3 tools/build_prototype.py
"""
import json
import shutil
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

# 1. Local prototype
proto_dir = ROOT / "prototype"
proto_dir.mkdir(exist_ok=True)
(proto_dir / "index.html").write_text(page)

# 2. GitHub Pages web deployment
docs_dir = ROOT / "docs"
docs_dir.mkdir(exist_ok=True)
(docs_dir / "index.html").write_text(page)
(docs_dir / ".nojekyll").touch(exist_ok=True)

# 3. Bundle release APK for one-click web downloads
apk_src = ROOT / "marginalia.apk"
candidate = ROOT / "android" / "app" / "build" / "outputs" / "apk" / "release" / "app-release.apk"
if candidate.exists():
    shutil.copy(candidate, apk_src)

if apk_src.exists():
    shutil.copy(apk_src, proto_dir / "marginalia.apk")
    shutil.copy(apk_src, docs_dir / "marginalia.apk")
    print(f"Bundled marginalia.apk ({apk_src.stat().st_size / 1024 / 1024:.1f} MB) into docs/ and prototype/")

print(f"Built prototype/index.html and docs/index.html with {len(cards)} cards and {len(bank)} quote bank entries")
