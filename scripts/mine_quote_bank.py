# mine_quote_bank.py — Extracts literary quotes from EPUBs using local Ollama (gemma3:4b)
# Usage: python3 scripts/mine_quote_bank.py <epub-path> <author> <title> [year] [translator]
# Requires: local Ollama running at localhost:11434 with gemma3:4b
#
# Gotchas:
# - Ollama with `format: "json"` requires the prompt to ask for a JSON object (not a bare list),
#   otherwise gemma3:4b may return an empty `{}`.
# - Some EPUBs have huge frontmatter/backmatter or copyright pages. We filter out files under 500 words.
# - To avoid context fragmentation, we chunk text on paragraph boundaries (~1,500 words).

import json
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"


def extract_chapters(epub_path):
    """Extracts cleaned text from each chapter of an EPUB."""
    chapters = []
    with zipfile.ZipFile(epub_path, "r") as z:
        # Sort html/xhtml files
        fnames = [f for f in z.namelist() if f.lower().endswith((".html", ".xhtml", ".htm"))]
        fnames.sort()

        for fname in fnames:
            # Skip common non-story pages (cover, toc, titlepage, copyright, ads)
            # Match whole stems or specific boundary patterns so book titles with 'about', 'ad', etc. aren't dropped
            stem = Path(fname).stem.lower()
            if stem in {"cover", "titlepage", "title_page", "title", "toc", "nav", "copyright", "colophon", "ad", "ads", "advertisement"}:
                continue
            if re.search(r"(about[-_]?author|also[-_]?by|praise[-_]?for|table[-_]?of[-_]?contents)", stem):
                continue

            raw = z.read(fname).decode("utf-8", errors="ignore")
            # Strip HTML tags
            clean = re.sub(r"<[^>]+>", " ", raw)
            clean = " ".join(clean.split())
            words = clean.split()

            # Ignore tiny fragments
            if len(words) > 300:
                chapters.append({"file": fname, "text": clean, "word_count": len(words)})

    return chapters


def chunk_text(text, target_words=1200):
    """Chunks text into narrative chunks of roughly target_words."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), target_words):
        chunk = " ".join(words[i : i + target_words])
        if len(chunk.split()) > 200:
            chunks.append(chunk)
    return chunks


def ask_local_model(chunk, author, title):
    """Calls local gemma3:4b via Ollama to scout for literary quotes."""
    prompt = f"""You are a master literary editor scouting for quotes for Marginalia.
Author: {author}
Work: {title}

Analyze this excerpt and extract 1 or 2 striking, self-contained quotes or working passages (1 to 4 sentences).
The quote MUST pass the cold-reader test: someone who has never heard of the book must find it arresting on its own.
Do NOT pick generic dialogue or lines that only make sense if you know the plot.

Respond with a JSON object with this exact structure:
{{
  "quotes": [
    {{
      "quote": "exact quote from the text",
      "hook": "How to [describe the craft job, e.g. How to fold three times into one sentence]",
      "why_it_lands": "Brief 1-sentence explanation of the craft move"
    }}
  ]
}}

Text excerpt:
{chunk}
"""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.3,
            "top_p": 0.9,
        },
    }

    try:
        req = urllib.request.Request(
            OLLAMA_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            res_text = data.get("response", "{}")
            parsed = json.loads(res_text)
            return parsed.get("quotes", [])
    except Exception as e:
        print(f"Error querying local model: {e}", file=sys.stderr)
        return []


def mine_epub(epub_path, author, title, year=None, translator=None, max_chunks=8):
    chapters = extract_chapters(epub_path)
    print(f"Loaded {len(chapters)} substantive chapters from {Path(epub_path).name}")

    all_chunks = []
    for ch in chapters:
        all_chunks.extend(chunk_text(ch["text"]))

    # Sample chunks evenly across the book if there are many
    if len(all_chunks) > max_chunks:
        step = len(all_chunks) / max_chunks
        sampled_chunks = [all_chunks[int(i * step)] for i in range(max_chunks)]
    else:
        sampled_chunks = all_chunks

    print(f"Analyzing {len(sampled_chunks)} sampled narrative chunks using local {MODEL_NAME}...")

    mined_quotes = []
    seen = set()

    for i, chunk in enumerate(sampled_chunks):
        candidates = ask_local_model(chunk, author, title)
        for c in candidates:
            q = c.get("quote", "").strip()
            # Clean quotes
            q = q.strip('“"”')
            if len(q.split()) < 6 or len(q.split()) > 150:
                continue
            if q in seen:
                continue
            seen.add(q)
            mined_quotes.append(
                {
                    "quote": q,
                    "author": author,
                    "work": title,
                    "year": year,
                    "translator": translator,
                    "hook": c.get("hook", ""),
                    "why_it_lands": c.get("why_it_lands", ""),
                }
            )
        print(f"  Chunk {i+1}/{len(sampled_chunks)} evaluated — total candidates: {len(mined_quotes)}", flush=True)

    return mined_quotes


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 scripts/mine_quote_bank.py <epub-path> <author> <title> [year] [translator]")
        sys.exit(1)

    epub = sys.argv[1]
    author = sys.argv[2]
    title = sys.argv[3]
    year = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4].isdigit() else None
    translator = sys.argv[5] if len(sys.argv) > 5 else None

    results = mine_epub(epub, author, title, year, translator)
    print(f"\nExtracted {len(results)} high-caliber quotes:")
    print(json.dumps(results, indent=2, ensure_ascii=False))
