#!/usr/bin/env python3
# enrich_full_quote_bank.py — Continuous background pipeline to enrich the full quote bank via Gemini Free Tier
# Usage: python3 scripts/enrich_full_quote_bank.py
# Requires: Python standard library, .env file with GEMINI_API_KEY
#
# Gotchas:
# - gemini-3.5-flash and gemini-3.1-flash-lite default to thinking mode unless thinkingBudget: 0 is explicitly set.
#   Without thinkingBudget: 0, internal thought tokens consume the token budget and cause premature MAX_TOKENS truncations.
# - gemini-3.5-flash-lite rejects thinkingConfig with HTTP 400, so only pass thinkingConfig to models that support it.
# - Free tier quotas have per-model 500-1500 RPD caps. Rotating between active models prevents pipeline pauses.

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

MODELS = [
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite"
]

# Pacing: 4.5 seconds between requests = 13.3 requests/minute (under Free Tier ceiling of 15 RPM)
REQUEST_DELAY = 4.5

def load_api_key():
    if not ENV_PATH.exists():
        return None
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("GEMINI_API_KEY="):
                return line.strip().split("=", 1)[1].strip()
    return None

def call_gemini(key, prompt_text, model_name):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"
    
    gen_config = {
        "temperature": 0.35,
        "maxOutputTokens": 1200
    }
    # Only models with extended thinking support thinkingBudget
    if "flash-lite" not in model_name or "3.1" in model_name:
        gen_config["thinkingConfig"] = {"thinkingBudget": 0}

    payload = json.dumps({
        "contents": [
            {
                "parts": [
                    {"text": prompt_text}
                ]
            }
        ],
        "generationConfig": gen_config
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        candidates = data.get("candidates", [])
        if not candidates:
            raise ValueError(f"No candidates returned: {data}")
        parts = candidates[0].get("content", {}).get("parts", [])
        if not parts:
            raise ValueError(f"No content parts returned: {data}")
        return parts[0].get("text", "").strip()

def clean_explanation(raw_text):
    # If the model produced a split with dividers, take the final companion note section
    if "***" in raw_text:
        raw_text = raw_text.split("***")[-1]
    elif "---" in raw_text:
        raw_text = raw_text.split("---")[-1]

    lines = raw_text.splitlines()
    filtered = []
    for line in lines:
        l = line.strip()
        # Skip divider lines or title/label lines
        if l in ["***", "---", "___"]:
            continue
        if l.startswith("#"):
            continue
        if l.lower().startswith("**explanation") or l.lower().startswith("**companion note"):
            continue
        # Strip inline paragraph labels
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
    model_idx = 0

    for idx, entry in enumerate(qb):
        exp = entry.get("explanation", "")
        if is_already_enriched(exp):
            continue

        author = entry.get("author", "Unknown")
        work = entry.get("work", "Unknown")
        quote = entry.get("quote", "")

        prompt = prompt_template.format(work=work, author=author, quote=quote)

        # Call with retries and model rotation
        attempt = 0
        success = False
        models_tried = 0

        while attempt < 6 and not success:
            active_model = MODELS[model_idx]
            try:
                raw = call_gemini(key, prompt, active_model)
                cleaned = clean_explanation(raw)

                if is_already_enriched(cleaned):
                    entry["explanation"] = cleaned
                    words = len(cleaned.split())
                    log(f"[{idx+1}/{total}] ✓ [{active_model}] {author} — {work} ({words}w)")
                    success = True
                    success_count += 1
                    consecutive_errors = 0

                    # Auto-save every 5 quotes
                    if success_count % 5 == 0:
                        save_quote_bank(qb)

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
                    is_daily_cap = "Quota exceeded" in err_body or "Resource has been exhausted" in err_body
                    if is_daily_cap:
                        log(f"[{idx+1}/{total}] ⚠ Model {active_model} daily quota exhausted. Rotating...")
                        model_idx = (model_idx + 1) % len(MODELS)
                        models_tried += 1
                        if models_tried >= len(MODELS):
                            log("All models currently rate-limited. Sleeping 90s before next round...")
                            time.sleep(90)
                            models_tried = 0
                    else:
                        log(f"[{idx+1}/{total}] ⚠ RPM rate limited on {active_model}. Sleeping 15s...")
                        time.sleep(15)
                else:
                    log(f"[{idx+1}/{total}] ✗ HTTP Error {e.code} on {active_model}: {e.reason}")
                    time.sleep(5)
            except Exception as e:
                attempt += 1
                log(f"[{idx+1}/{total}] ✗ Error on {active_model}: {e}. Retrying in 8s...")
                time.sleep(8)

        if not success:
            consecutive_errors += 1
            log(f"[{idx+1}/{total}] ⚠ Skipped {author} — {work} after repeated attempts.")
            if consecutive_errors >= 8:
                log("CRITICAL: 8 consecutive failures. Pausing pipeline to avoid error loop. Saving database.")
                save_quote_bank(qb)
                sys.exit(1)

    save_quote_bank(qb)
    log(f"PIPELINE COMPLETE! Enriched {success_count} quotes successfully.")

if __name__ == "__main__":
    main()
