#!/usr/bin/env python3
# enrich_with_claude.py — Automated quote bank companion note enrichment via Claude API
# Usage: caffeinate -dimsu python3 scripts/enrich_with_claude.py
# Requires: Python standard library, .env with ANTHROPIC_API_KEY
#
# Gotchas:
# - Anthropic Messages API endpoint: https://api.anthropic.com/v1/messages
# - Required headers: 'x-api-key', 'anthropic-version: 2023-06-01', 'content-type: application/json'
# - Model name: 'claude-haiku-4-5-20251001' (verified active on this account)
# - Pacing: 1.5s between requests gives ~40 requests/min, staying well within tier rate limits.

import json
import time
import urllib.request
import urllib.error
import sys
import signal
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QB_PATH = ROOT / "content" / "quote-bank.json"
ENV_PATH = ROOT / ".env"
PROMPT_FILE = ROOT / "prompts" / "shelf_explanation_prompt.txt"
LOG_FILE = ROOT / "scripts" / "claude_enrichment_progress.log"

CLAUDE_MODELS = [
    "claude-haiku-4-5-20251001",
    "claude-haiku-5-5",
    "claude-sonnet-4-5-20250929"
]

REQUEST_DELAY = 1.5

def load_api_key():
    if not ENV_PATH.exists():
        return None
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("ANTHROPIC_API_KEY="):
                return line.strip().split("=", 1)[1].strip()
    return None

def call_claude(key, prompt_text, model_name):
    url = "https://api.anthropic.com/v1/messages"
    payload = json.dumps({
        "model": model_name,
        "max_tokens": 800,
        "temperature": 0.35,
        "messages": [
            {"role": "user", "content": prompt_text}
        ]
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        text = ""
        for block in data.get("content", []):
            if block.get("type") == "text":
                text += block.get("text", "")
        return text.strip()

def clean_explanation(raw_text):
    if "***" in raw_text:
        raw_text = raw_text.split("***")[-1]
    elif "---" in raw_text:
        raw_text = raw_text.split("---")[-1]

    lines = raw_text.splitlines()
    filtered = []
    for line in lines:
        l = line.strip()
        if l in ["***", "---", "___"]:
            continue
        if l.startswith("#"):
            continue
        if l.lower().startswith("**explanation") or l.lower().startswith("**companion note"):
            continue
        for prefix in ["**Paragraph 1:**", "**Paragraph 2:**", "Paragraph 1:", "Paragraph 2:", "**The Predicament:**", "**The Mirror:**", "The Predicament:", "The Mirror:"]:
            if l.startswith(prefix):
                l = l[len(prefix):].strip()
        filtered.append(l)

    text = "\n".join(filtered)
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    return "\n\n".join(paras)

def is_already_enriched(exp):
    if not exp:
        return False
    paragraphs = [p.strip() for p in exp.split("\n\n") if p.strip()]
    return len(paragraphs) >= 2 and len(exp.split()) >= 100

def save_quote_bank(qb):
    with open(QB_PATH, "w", encoding="utf-8") as f:
        json.dump(qb, f, indent=2, ensure_ascii=False)

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

def sync_docs_and_prototype():
    try:
        subprocess.run(["python3", str(ROOT / "tools" / "sync_quote_bank_md.py")], check=True, capture_output=True)
        subprocess.run(["python3", str(ROOT / "tools" / "build_prototype.py")], check=True, capture_output=True)
        log("🔄 Auto-synced quote-bank.md and rebuilt web prototype.")
    except Exception as e:
        log(f"⚠ Sync warning: {e}")

def main():
    key = load_api_key()
    if not key:
        log("ERROR: ANTHROPIC_API_KEY not found in .env")
        sys.exit(1)

    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    with open(QB_PATH, "r", encoding="utf-8") as f:
        qb = json.load(f)

    total = len(qb)
    already_done = sum(1 for q in qb if is_already_enriched(q.get("explanation", "")))
    log(f"Starting Claude Quote Enrichment Pipeline...")
    log(f"Total Quotes: {total} | Already Enriched: {already_done} | Remaining: {total - already_done}")

    def handle_exit(signum, frame):
        log("Received termination signal. Saving database and exiting safely...")
        save_quote_bank(qb)
        sync_docs_and_prototype()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    success_count = 0
    consecutive_errors = 0
    model_idx = 0

    for idx, entry in enumerate(qb):
        exp = entry.get("explanation", "")
        if is_already_enriched(exp):
            continue

        author = entry.get("author", "Unknown")
        work = entry.get("work", "Unknown")
        quote = entry.get("quote", "")

        prompt = prompt_template.format(work=work, author=author, quote=quote)

        attempt = 0
        success = False

        while attempt < 4 and not success:
            active_model = CLAUDE_MODELS[model_idx]
            try:
                raw = call_claude(key, prompt, active_model)
                cleaned = clean_explanation(raw)

                if is_already_enriched(cleaned):
                    entry["explanation"] = cleaned
                    words = len(cleaned.split())
                    log(f"[{idx+1}/{total}] ✓ [{active_model}] {author} — {work} ({words}w)")
                    success = True
                    success_count += 1
                    consecutive_errors = 0

                    # Save every 5 quotes
                    if success_count % 5 == 0:
                        save_quote_bank(qb)

                    # Sync markdown & prototype every 50 quotes
                    if success_count % 50 == 0:
                        sync_docs_and_prototype()

                    time.sleep(REQUEST_DELAY)
                else:
                    log(f"[{idx+1}/{total}] ⚠ Incomplete response from {active_model} ({len(cleaned.split())}w). Retrying...")
                    attempt += 1
                    time.sleep(2)

            except urllib.error.HTTPError as e:
                attempt += 1
                err_body = ""
                try:
                    err_body = e.read().decode("utf-8")
                except:
                    pass

                if e.code == 429:
                    log(f"[{idx+1}/{total}] ⚠ Rate limit (429) on {active_model}. Sleeping 15s...")
                    time.sleep(15)
                elif e.code == 404:
                    log(f"[{idx+1}/{total}] ⚠ Model {active_model} not found. Rotating model...")
                    model_idx = (model_idx + 1) % len(CLAUDE_MODELS)
                else:
                    log(f"[{idx+1}/{total}] ✗ HTTP Error {e.code} on {active_model}: {err_body[:100]}")
                    time.sleep(5)
            except Exception as e:
                attempt += 1
                log(f"[{idx+1}/{total}] ✗ Error on {active_model}: {e}. Retrying in 5s...")
                time.sleep(5)

        if not success:
            consecutive_errors += 1
            log(f"[{idx+1}/{total}] ⚠ Skipped {author} — {work} after repeated attempts.")
            if consecutive_errors >= 8:
                log("CRITICAL: 8 consecutive failures. Pausing pipeline to avoid error loop. Saving database.")
                save_quote_bank(qb)
                sync_docs_and_prototype()
                sys.exit(1)

    save_quote_bank(qb)
    sync_docs_and_prototype()
    log(f"PIPELINE COMPLETE! Enriched {success_count} quotes successfully via Claude.")

if __name__ == "__main__":
    main()
