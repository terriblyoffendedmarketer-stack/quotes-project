#!/usr/bin/env python3
# test_gemini_api.py — Quick connectivity and auth test for Gemini API
# Usage: python3 scripts/test_gemini_api.py
# Requires: Python standard library, .env file with GEMINI_API_KEY

import json
import os
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"

def load_api_key():
    if not ENV_PATH.exists():
        return None
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip()
    return None

def test_api():
    key = load_api_key()
    if not key:
        print("Error: GEMINI_API_KEY not found in .env")
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    req = urllib.request.Request(url)

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = [m["name"] for m in data.get("models", []) if "generateContent" in m.get("supportedGenerationMethods", [])]
            print("Available models:")
            for m in models:
                print(" -", m)
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8")
        print(f"HTTP Error {e.code}: {err}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
