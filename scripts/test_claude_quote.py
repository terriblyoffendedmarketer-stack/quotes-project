#!/usr/bin/env python3
# test_claude_quote.py — Tests Claude API on an un-enriched quote from quote-bank.json
# Usage: python3 scripts/test_claude_quote.py
# Requires: Python standard library, .env with ANTHROPIC_API_KEY

import json
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
PROMPT_PATH = ROOT / "prompts" / "shelf_explanation_prompt.txt"
QB_PATH = ROOT / "content" / "quote-bank.json"

def main():
    key = None
    with open(ENV_PATH) as f:
        for line in f:
            if line.startswith("ANTHROPIC_API_KEY="):
                key = line.split("=", 1)[1].strip()

    if not key:
        print("Missing ANTHROPIC_API_KEY in .env")
        return

    with open(PROMPT_PATH) as f:
        template = f.read()

    with open(QB_PATH) as f:
        qb = json.load(f)

    # Find first un-enriched quote
    sample = None
    for q in qb:
        exp = q.get("explanation", "")
        paras = [p.strip() for p in exp.split("\n\n") if p.strip()]
        if len(paras) < 2 or len(exp.split()) < 100:
            sample = q
            break

    if not sample:
        print("All quotes already enriched!")
        return

    author = sample.get("author", "Unknown")
    work = sample.get("work", "Unknown")
    quote = sample.get("quote", "")

    print(f"Sample Quote: {author} — {work}")
    print(f"Text: \"{quote}\"\n")

    prompt = template.format(work=work, author=author, quote=quote)

    payload = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 800,
        "temperature": 0.35,
        "messages": [{"role": "user", "content": prompt}]
    }

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode(),
        headers={
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
    )

    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        text = data["content"][0]["text"].strip()
        print("=== CLAUDE OUTPUT ===")
        print(text)
        print("\nWord count:", len(text.split()))
        print("Paragraphs:", len([p for p in text.split("\n\n") if p.strip()]))

if __name__ == "__main__":
    main()
