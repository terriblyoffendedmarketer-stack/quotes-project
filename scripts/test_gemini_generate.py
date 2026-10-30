#!/usr/bin/env python3
# test_gemini_generate.py — Tests generateContent with gemini-2.5-flash
# Usage: python3 scripts/test_gemini_generate.py

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"

def load_api_key():
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("GEMINI_API_KEY="):
                return line.strip().split("=", 1)[1].strip()
    return None

def main():
    key = load_api_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={key}"
    payload = json.dumps({
        "contents": [
            {
                "parts": [
                    {"text": "Respond with: Ready for literary enrichment."}
                ]
            }
        ]
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            ans = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            print("API Response:", ans)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")

if __name__ == "__main__":
    main()
