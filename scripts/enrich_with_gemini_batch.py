#!/usr/bin/env python3
# enrich_with_gemini_batch.py — Enriches shelf quote explanations via Gemini 3.5 Flash Lite API (100% Free Tier)
# Usage: python3 scripts/enrich_with_gemini_batch.py [--apply]
# Requires: Python standard library, .env file with GEMINI_API_KEY

import json
import time
import urllib.request
import urllib.error
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QB_PATH = ROOT / "content" / "quote-bank.json"
ASSET_PATH = ROOT / "android" / "app" / "src" / "main" / "assets" / "quote-bank.json"
ENV_PATH = ROOT / ".env"
PROMPT_FILE = ROOT / "prompts" / "shelf_explanation_prompt.txt"
OUTPUT_PREVIEW = ROOT / "scripts" / "batch_10_gemini_live.json"

MODEL_NAME = "gemini-3.5-flash-lite"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"

# The 10 high-rotation test quotes:
# 93: Orwell (1984)
# 2: Murakami (Men Without Women - Squash racket)
# 3: Murakami (Men Without Women - Kino)
# 12: Vonnegut (Cat's Cradle - Shameless lies)
# 13: Vonnegut (Cat's Cradle - Caesar)
# 17: Auster (Invention of Solitude - Country of work)
# 10: Peck (A Short Stay in Hell - Grammatically correct)
# 42: Camus (Myth of Sisyphus - Habit)
# 114: Baldwin (The Fire Next Time - Drowning in suffering)
# 5: Murakami (Running - Halloween tax collector)
TARGET_INDICES = [93, 2, 3, 12, 13, 17, 10, 42, 114, 5]

def load_api_key():
    if not ENV_PATH.exists():
        return None
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("GEMINI_API_KEY="):
                return line.strip().split("=", 1)[1].strip()
    return None

def call_gemini(key, prompt_text):
    url = f"{API_URL}?key={key}"
    payload = json.dumps({
        "contents": [
            {
                "parts": [
                    {"text": prompt_text}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 400
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()

def main():
    key = load_api_key()
    if not key:
        print("Error: GEMINI_API_KEY not found in .env")
        sys.exit(1)

    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    with open(QB_PATH, "r", encoding="utf-8") as f:
        qb = json.load(f)

    results = []
    print(f"Enriching {len(TARGET_INDICES)} quotes using Gemini ({MODEL_NAME}) on Free Tier...\n")

    for rank, idx in enumerate(TARGET_INDICES, 1):
        if idx >= len(qb):
            continue
        entry = qb[idx]
        author = entry.get("author", "Unknown")
        work = entry.get("work", "Unknown")
        quote = entry.get("quote", "")
        old_exp = entry.get("explanation", "")

        print(f"[{rank}/{len(TARGET_INDICES)}] Enriching: {author} — {work}")
        prompt = prompt_template.format(work=work, author=author, quote=quote)

        try:
            generated = call_gemini(key, prompt)
            # Clean up any potential markdown labels
            cleaned = generated.replace("**Tier 1:**", "").replace("**Tier 2:**", "")
            cleaned = cleaned.replace("Tier 1:", "").replace("Tier 2:", "").strip()

            results.append({
                "index": idx,
                "author": author,
                "work": work,
                "quote": quote,
                "old_explanation": old_exp,
                "new_explanation": cleaned,
                "word_count": len(cleaned.split())
            })
            print(f"  ✓ Success ({len(cleaned.split())} words)")
            # Respect free tier rate limits (15 requests/minute = 4 second delay)
            time.sleep(3.5)
        except Exception as e:
            print(f"  ✗ Failed: {e}")

    # Save to live preview
    with open(OUTPUT_PREVIEW, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nSaved live batch preview to {OUTPUT_PREVIEW}")

    if "--apply" in sys.argv:
        for r in results:
            qb[r["index"]]["explanation"] = r["new_explanation"]
        with open(QB_PATH, "w", encoding="utf-8") as f:
            json.dump(qb, f, indent=2, ensure_ascii=False)
        print(f"Applied updates to {QB_PATH}!")
        if ASSET_PATH.exists():
            with open(ASSET_PATH, "w", encoding="utf-8") as f:
                json.dump(qb, f, indent=2, ensure_ascii=False)
            print(f"Synced to {ASSET_PATH}!")

if __name__ == "__main__":
    main()
