#!/usr/bin/env python3
# test_gemini_quote.py — Generates a 2-tier scene explanation using Gemini 3.5 Flash Lite
# Usage: python3 scripts/test_gemini_quote.py

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
PROMPT_FILE = ROOT / "prompts" / "shelf_explanation_prompt.txt"

def load_api_key():
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("GEMINI_API_KEY="):
                return line.strip().split("=", 1)[1].strip()
    return None

def main():
    key = load_api_key()
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    # Test with Kurt Vonnegut — Cat's Cradle
    prompt = prompt_template.format(
        work="Cat's Cradle",
        author="Kurt Vonnegut",
        quote="All of the true things I am about to tell you are shameless lies."
    )

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={key}"
    payload = json.dumps({
        "contents": [
            {
                "parts": [
                    {"text": prompt}
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

    print("Sending request to Gemini 3.5 Flash Lite...")
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        ans = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        print("\n=== GEMINI RESPONSE ===")
        print(ans)

if __name__ == "__main__":
    main()
