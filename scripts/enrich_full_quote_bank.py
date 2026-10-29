#!/usr/bin/env python3
# enrich_full_quote_bank.py — Continuous background pipeline to enrich the full quote bank via Gemini Free Tier
# Usage: python3 scripts/enrich_full_quote_bank.py
# Requires: Python standard library, .env file with GEMINI_API_KEY

import json
import time
import urllib.request
import urllib.error
import sys
import signal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QB_PATH = ROOT / "content" / "quote-bank.json"
ENV_PATH = ROOT / ".env"
PROMPT_FILE = ROOT / "prompts" / "shelf_explanation_prompt.txt"
LOG_FILE = ROOT / "scripts" / "enrichment_progress.log"

MODEL_NAME = "gemini-3.5-flash-lite"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"

# Pacing: 5.0 seconds between requests = 12.0 requests/minute (Safely under Free Tier ceiling of 15 RPM)
REQUEST_DELAY = 5.0

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
            "temperature": 0.4,
            "maxOutputTokens": 600
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

def is_already_enriched(exp):
    if not exp:
        return False
    # Check for two distinct paragraphs and substantive word count (>120 words)
    paragraphs = [p.strip() for p in exp.split("\n\n") if p.strip()]
    return len(paragraphs) >= 2 and len(exp.split()) >= 120

def save_quote_bank(qb):
    with open(QB_PATH, "w", encoding="utf-8") as f:
        json.dump(qb, f, indent=2, ensure_ascii=False)

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

def main():
    key = load_api_key()
    if not key:
        log("ERROR: GEMINI_API_KEY not found in .env")
        sys.exit(1)

    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    with open(QB_PATH, "r", encoding="utf-8") as f:
        qb = json.load(f)

    total = len(qb)
    already_done = sum(1 for q in qb if is_already_enriched(q.get("explanation", "")))
    log(f"Starting Quote Bank Enrichment Pipeline...")
    log(f"Total Quotes: {total} | Already Enriched: {already_done} | Remaining: {total - already_done}")

    # Graceful exit handling
    def handle_exit(signum, frame):
        log("Received termination signal. Saving database and exiting safely...")
        save_quote_bank(qb)
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    success_count = 0
    consecutive_errors = 0

    for idx, entry in enumerate(qb):
        exp = entry.get("explanation", "")
        if is_already_enriched(exp):
            continue

        author = entry.get("author", "Unknown")
        work = entry.get("work", "Unknown")
        quote = entry.get("quote", "")

        prompt = prompt_template.format(work=work, author=author, quote=quote)

        # Call with retries for rate limits
        attempt = 0
        success = False
        while attempt < 5 and not success:
            try:
                raw = call_gemini(key, prompt)
                cleaned = raw.replace("**Paragraph 1:**", "").replace("**Paragraph 2:**", "")
                cleaned = cleaned.replace("Paragraph 1:", "").replace("Paragraph 2:", "").strip()

                entry["explanation"] = cleaned
                words = len(cleaned.split())
                log(f"[{idx+1}/{total}] ✓ {author} — {work} ({words}w)")
                success = True
                success_count += 1
                consecutive_errors = 0

                # Auto-save every 5 quotes
                if success_count % 5 == 0:
                    save_quote_bank(qb)

                time.sleep(REQUEST_DELAY)

            except urllib.error.HTTPError as e:
                attempt += 1
                if e.code == 429:
                    log(f"[{idx+1}/{total}] ⚠ Rate limited (429). Sleeping 60s before retry (attempt {attempt}/5)...")
                    time.sleep(60)
                else:
                    log(f"[{idx+1}/{total}] ✗ HTTP Error {e.code}: {e.reason}")
                    time.sleep(5)
            except Exception as e:
                attempt += 1
                log(f"[{idx+1}/{total}] ✗ Error: {e}. Retrying in 10s...")
                time.sleep(10)

        if not success:
            consecutive_errors += 1
            log(f"[{idx+1}/{total}] ⚠ Skipped {author} — {work} after 5 failed attempts.")
            if consecutive_errors >= 5:
                log("CRITICAL: 5 consecutive failures. Pausing pipeline to avoid error loop. Saving database.")
                save_quote_bank(qb)
                sys.exit(1)

    save_quote_bank(qb)
    log(f"PIPELINE COMPLETE! Enriched {success_count} quotes successfully.")

if __name__ == "__main__":
    main()
