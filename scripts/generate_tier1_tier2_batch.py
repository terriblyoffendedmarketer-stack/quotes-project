#!/usr/bin/env python3
# generate_tier1_tier2_batch.py — Generates 2-tier scene explanations using local Ollama
# Usage: python3 scripts/generate_tier1_tier2_batch.py [--apply]
# Requires: local Ollama running at http://localhost:11434 with gemma3:4b

import json
import urllib.request
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QB_PATH = ROOT / "content" / "quote-bank.json"
OUTPUT_PREVIEW = ROOT / "scripts" / "batch_10_preview.json"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"

PROMPT_TEMPLATE = """You are a master literary editor writing companion notes for an anthology app.
You are given a book title, author, and a specific quote from the book.
Your task is to write an explanation in exactly TWO paragraphs (Tier 1 and Tier 2), totaling 80 to 110 words.

Book: {work}
Author: {author}
Quote: "{quote}"

TIER 1 RULES (The Scene & Intrigue — ~40–50 words):
1. Immediately ground the situation in plain, physical reality: who is here, what pressure are they under, what is physically happening in this scene?
2. Zero spoilers. Never describe the outcome of the book, whether someone dies later, or how the plot resolves. Only describe the crossroads or crisis the character is standing in right now.
3. Make the reader hungry to read the book.

TIER 2 RULES (The Human Truth / The Core Insight — ~40–60 words):
1. Do not repeat Tier 1. Move from the specific plot to the universal human insight.
2. Directly illuminate the core word or phrase in the quote.
3. Plain, muscular English. No essayist meta-language ("This symbolizes...", "Here the author explores...", "The word X carries..."). Just state the truth directly.
4. Ban the artificial "It's not X, it's Y" contrast unless it genuinely clarifies a physical difference.

TONE & STYLE CONSTRAINTS:
- No academic jargon (no 'litotes', 'chiasmus', 'interiority', 'liminal').
- No corporate takeaways, self-help lessons, or preachy life advice.
- Natural storytelling rhythm—reads like someone talking across a table who understands the human heart.

Output format:
Respond with ONLY the two paragraphs separated by a single blank line. Do not include labels like 'Tier 1' or 'Paragraph 1'. Do not include markdown headers or bullet points. Just the two clean paragraphs.
"""

# Target indices of the 10 selected quotes
TARGET_INDICES = [93, 2, 3, 12, 13, 17, 10, 42, 114, 5]

def call_ollama(work, author, quote):
    prompt = PROMPT_TEMPLATE.format(work=work, author=author, quote=quote)
    payload = json.dumps({
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "top_p": 0.9,
            "num_predict": 300
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res.get("response", "").strip()

def main():
    print(f"Loading quote bank from {QB_PATH}...")
    with open(QB_PATH, "r", encoding="utf-8") as f:
        qb = json.load(f)

    results = []
    print(f"Generating 2-tier explanations for {len(TARGET_INDICES)} test quotes via {MODEL_NAME}...\n")

    for rank, idx in enumerate(TARGET_INDICES, 1):
        if idx >= len(qb):
            continue
        entry = qb[idx]
        author = entry.get("author", "Unknown")
        work = entry.get("work", "Unknown")
        quote = entry.get("quote", "")
        old_exp = entry.get("explanation", "")

        print(f"[{rank}/{len(TARGET_INDICES)}] Generating for: {author} — {work}")
        print(f"  Quote: \"{quote[:70]}...\"")

        try:
            generated = call_ollama(work, author, quote)
            # Clean up any potential markdown headers or labels
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
            print(f"  Done ({len(cleaned.split())} words)\n")
        except Exception as e:
            print(f"  Failed: {e}\n")

    # Save to preview JSON
    with open(OUTPUT_PREVIEW, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Saved preview to {OUTPUT_PREVIEW}")

    # If --apply flag is given, update the quote bank directly
    if "--apply" in sys.argv:
        for r in results:
            qb[r["index"]]["explanation"] = r["new_explanation"]
        with open(QB_PATH, "w", encoding="utf-8") as f:
            json.dump(qb, f, indent=2, ensure_ascii=False)
        print(f"Applied updates to {QB_PATH}!")

if __name__ == "__main__":
    main()
