#!/usr/bin/env python3
# test_claude_api.py — Verifies Anthropic Claude API key with sample prompt
# Usage: python3 scripts/test_claude_api.py
# Requires: Python standard library, .env with ANTHROPIC_API_KEY
#
# Gotchas:
# - Anthropic API requires headers: 'x-api-key', 'anthropic-version: 2023-06-01', 'content-type: application/json'
# - Messages API endpoint: https://api.anthropic.com/v1/messages

import json
import os
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"

def load_key():
    if not ENV_PATH.exists():
        return None
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("ANTHROPIC_API_KEY="):
                return line.strip().split("=", 1)[1].strip()
    return None

def test():
    key = load_key()
    if not key:
        print("ERROR: ANTHROPIC_API_KEY not found in .env")
        return

    url = "https://api.anthropic.com/v1/messages"
    models_to_test = [
        "claude-3-5-haiku-20241022",
        "claude-3-haiku-20240307",
        "claude-3-5-sonnet-20241022"
    ]

    for model in models_to_test:
        print(f"\n--- Testing model: {model} ---")
        payload = {
            "model": model,
            "max_tokens": 600,
            "messages": [
                {
                    "role": "user",
                    "content": "Write a 2-sentence literary reflection on why people buy books they will never have time to read."
                }
            ]
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = ""
                for block in data.get("content", []):
                    if block.get("type") == "text":
                        text += block.get("text", "")
                print(f"✓ Success with {model}!\nResponse:\n{text.strip()}\n")
                return model
        except urllib.error.HTTPError as e:
            err = ""
            try:
                err = e.read().decode("utf-8")
            except:
                pass
            print(f"✗ HTTP Error {e.code} on {model}: {e.reason}\nBody: {err}")
        except Exception as e:
            print(f"✗ Error on {model}: {e}")

if __name__ == "__main__":
    test()
