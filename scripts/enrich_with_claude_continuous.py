#!/usr/bin/env python3
# scripts/enrich_with_claude_continuous.py — Fast, robust continuous background pipeline using Anthropic API
# Usage: python3 scripts/enrich_with_claude_continuous.py
# Enriches missing books with authentic quotes, 2-tier companion insights, and passionate book-nerd curator notes.

import json
import re
import time
import urllib.request
import urllib.error
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "bookshelf" / "data.json"
ENV_PATH = ROOT / ".env"
BUILD_SCRIPT = ROOT / "scripts" / "build_independent_bookshelf_app.py"

def load_api_key():
    if not ENV_PATH.exists():
        return None
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("ANTHROPIC_API_KEY="):
                return line.strip().split("=", 1)[1].strip()
    return None

def extract_quotes(raw_quotes):
    normalized = []
    if not isinstance(raw_quotes, list):
        return normalized
    for q in raw_quotes:
        if isinstance(q, str):
            q_clean = re.sub(r'^(Paraphrased summary|Summary|Quote):\s*', '', q, flags=re.I).strip()
            normalized.append({"quote": q_clean, "explanation": "", "tags": ["literature"]})
        elif isinstance(q, dict):
            quote_text = q.get("quote") or q.get("text") or q.get("passage") or q.get("line") or ""
            quote_text = re.sub(r'^(Paraphrased summary|Summary|Quote):\s*', '', quote_text, flags=re.I).strip()
            explanation = q.get("explanation") or q.get("insight") or q.get("notes") or ""
            tags = q.get("tags") or []
            if quote_text:
                normalized.append({
                    "quote": quote_text,
                    "explanation": explanation,
                    "tags": tags
                })
    return normalized

def call_claude(key, book):
    title = book.get("title", "")
    author = book.get("author", "")
    category = book.get("category", "")
    pitch = book.get("pitch", "")

    prompt = f"""You are an obsessed, literate book collector, culture nerd, and master essayist writing for a private curated library app called 'My Reading Corner'.

Book: '{title}' by {author}
Category: {category}
Existing Synopsis: {pitch}

Please provide:
1. 'curator_note': A single compelling, 1-2 paragraph editorial note (around 90-130 words) explaining why this book belongs in a personal reading corner. Write as an avid reader who loves books and culture. Focus on what is genuinely important—the prose rhythm, the author's wild obsession, why it altered how stories are told, historical context, or why it hits like a freight train. Write with authentic voice and ZERO generic boilerplate.
2. 'quotes': array of 1 to 2 quote objects. EACH object MUST have:
   - 'quote': an iconic, verbatim or highly accurate quote or key passage string.
   - 'explanation': two-tier companion insight (Paragraph 1: The Human Predicament/Crisis in the scene; Paragraph 2: The Mirror/Psychological resonance mirroring our own lives).
   - 'tags': array of 2-4 strings.

Respond ONLY with valid JSON with keys 'curator_note' and 'quotes'."""

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps({
            "model": "claude-haiku-5-5",
            "max_tokens": 2000,
            "thinking": {"type": "disabled"},
            "messages": [{"role": "user", "content": prompt}]
        }).encode(),
        headers={
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
    )

    with urllib.request.urlopen(req, timeout=25) as resp:
        res = json.loads(resp.read().decode())
        text = next((b["text"] for b in res.get("content", []) if b.get("type") == "text"), "")
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end != 0:
            return json.loads(text[start:end])
    return None

def main():
    key = load_api_key()
    if not key:
        print("Error: ANTHROPIC_API_KEY not found in .env")
        sys.exit(1)

    print("Loaded Anthropic API Key (thinking disabled for fast execution).")
    books = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    # Target books missing quotes
    missing = [b for b in books if len(b.get("quotes", [])) == 0]
    print(f"Total books needing quotes: {len(missing)} / {len(books)}")

    processed_in_session = 0

    for i, b in enumerate(missing):
        bid = b.get("id")
        title = b.get("title")
        author = b.get("author")
        print(f"[{i+1}/{len(missing)}] Enriching '{title}' by {author}...", end=" ", flush=True)

        try:
            result = call_claude(key, b)
            if result:
                raw_q = result.get("quotes", [])
                clean_quotes = extract_quotes(raw_q)
                if clean_quotes:
                    b["quotes"] = clean_quotes
                    b["has_quote_bank"] = True
                
                curator_note = result.get("curator_note", "")
                if curator_note and len(curator_note) > 40:
                    b["why_love"] = curator_note.strip()
                
                processed_in_session += 1
                print(f"✓ ({len(clean_quotes)} quotes, note: {len(b.get('why_love', ''))} chars)")
            else:
                print("⚠ Empty response")
        except Exception as e:
            print(f"✗ Error: {e}")

        # Save to disk every 5 books or on last book
        if (i + 1) % 5 == 0 or (i + 1) == len(missing):
            DATA_PATH.write_text(json.dumps(books, indent=2, ensure_ascii=False), encoding="utf-8")
            subprocess.run([sys.executable, str(BUILD_SCRIPT)], capture_output=True)
            print(f"  --> [CHECKPOINT] Saved & rebuilt apps ({processed_in_session} enriched).")

        # Periodically push to GitHub Pages every 25 books so user sees live updates
        if (i + 1) % 25 == 0 and processed_in_session > 0:
            try:
                subprocess.run(["git", "add", "bookshelf/data.json", "bookshelf/index.html", "docs/bookshelf.html"], cwd=ROOT, capture_output=True)
                subprocess.run(["git", "commit", "-m", f"chore(enrichment): auto-enrich batch ({processed_in_session} books enriched)"], cwd=ROOT, capture_output=True)
                subprocess.run(["git", "push", "origin", "main"], cwd=ROOT, capture_output=True)
                print(f"  --> [GITHUB SYNC] Pushed batch update to live GitHub Pages!")
            except Exception as e:
                print(f"  --> [GITHUB SYNC] Push skipped: {e}")

        time.sleep(0.8) # 0.8s pacing is well under Anthropic RPM limits

    # Final sync
    try:
        subprocess.run(["git", "add", "bookshelf/data.json", "bookshelf/index.html", "docs/bookshelf.html"], cwd=ROOT, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"feat(enrichment): complete full library quote coverage ({processed_in_session} books enriched)"], cwd=ROOT, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=ROOT, capture_output=True)
        print("  --> [FINAL GITHUB SYNC] Complete library pushed to GitHub Pages!")
    except Exception as e:
        pass

    print(f"\nDone! Enriched {processed_in_session} books in this run.")

if __name__ == "__main__":
    main()
