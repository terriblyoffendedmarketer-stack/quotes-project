# mine_full_library.py — Continuous, automated full-library mining engine
# Usage: caffeinate -dimsu python3 scripts/mine_full_library.py
# Requires: rclone ('gdrive:'), local Ollama ('gemma3:4b'), python standard library
#
# Gotchas:
# - rclone ls output includes leading file sizes (e.g. '   1382371 File.epub'); must parse path with regex.
# - Mac will sleep during long unattended runs; MUST invoke with 'caffeinate -dimsu'.
# - EPUB filenames often invert author/title; extract dc:creator and dc:title from content.opf for 100% accuracy.
# - Immediately unlink downloaded scratch EPUB in finally: block to keep disk usage under 500MB and honor the 20GB floor.

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# Ensure unbuffered stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

ROOT = Path(__file__).resolve().parent.parent
QB_PATH = ROOT / "content" / "quote-bank.json"
SCRATCH = Path("/Users/apple/.gemini/antigravity/brain/6282abf0-33f0-44df-ac5d-1d65c90f0f65/scratch")
SCRATCH.mkdir(parents=True, exist_ok=True)
RCLONE = "/opt/homebrew/bin/rclone"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"

def get_epub_metadata(epub_path):
    """Extracts dc:creator and dc:title directly from EPUB's content.opf."""
    creator, title = None, None
    try:
        with zipfile.ZipFile(epub_path, "r") as z:
            opf_name = next((f for f in z.namelist() if f.lower().endswith(".opf")), None)
            if not opf_name:
                try:
                    c = z.read("META-INF/container.xml")
                    root = ET.fromstring(c)
                    for el in root.iter("{urn:oasis:names:tc:opendocument:xmlns:container}rootfile"):
                        opf_name = el.attrib.get("full-path")
                        break
                except Exception:
                    pass
            if opf_name and opf_name in z.namelist():
                opf_data = z.read(opf_name)
                root = ET.fromstring(opf_data)
                for el in root.iter("{http://purl.org/dc/elements/1.1/}title"):
                    if el.text and not title:
                        title = el.text.strip()
                for el in root.iter("{http://purl.org/dc/elements/1.1/}creator"):
                    if el.text and not creator:
                        creator = el.text.strip()
    except Exception:
        pass
    return creator, title

def parse_filename_fallback(fn):
    clean = re.sub(r"^\d+\s*", "", fn).replace(".epub", "").strip()
    clean = re.sub(r"\(.*?\)|\[.*?\]|\{.*?\}", "", clean).strip()
    clean = clean.replace("_", " ").strip()
    if " - " in clean:
        parts = clean.split(" - ")
        return parts[0].strip(), parts[1].strip()
    elif " by " in clean.lower():
        parts = re.split(r"\s+by\s+", clean, flags=re.I)
        return parts[1].strip(), parts[0].strip()
    return "Unknown", clean

def extract_chapters(epub_path):
    chapters = []
    with zipfile.ZipFile(epub_path, "r") as z:
        fnames = [f for f in z.namelist() if f.lower().endswith((".html", ".xhtml", ".htm"))]
        fnames.sort()
        for fname in fnames:
            stem = Path(fname).stem.lower()
            if stem in {"cover", "titlepage", "title_page", "title", "toc", "nav", "copyright", "colophon", "ad", "ads", "advertisement"}:
                continue
            if re.search(r"(about[-_]?author|also[-_]?by|praise[-_]?for|table[-_]?of[-_]?contents)", stem):
                continue
            raw = z.read(fname).decode("utf-8", errors="ignore")
            clean = re.sub(r"<[^>]+>", " ", raw)
            clean = " ".join(clean.split())
            if len(clean.split()) > 250:
                chapters.append({"file": fname, "text": clean, "words": len(clean.split())})
    return chapters

def chunk_text(text, target_words=1200):
    words = text.split()
    chunks = []
    for i in range(0, len(words), target_words):
        chunk = " ".join(words[i : i + target_words])
        if len(chunk.split()) > 200:
            chunks.append(chunk)
    return chunks

def ask_local_model(chunk, author, title):
    prompt = f"""You are a master literary editor scouting memorable passages for a personal library discovery companion.
Author: {author}
Work: {title}

Analyze this excerpt and extract 1 or 2 striking, self-contained quotes or passages (1 to 5 sentences, up to 120 words).

Requirements:
1. Cold-Reader Test: Arresting, beautiful, tragic, or witty on its own to someone who hasn't read the book.
2. Zero Spoilers: No climactic reveals, deaths, killer identities, or final endings.
3. Plain-English Explanation: 2-3 sentences explaining what is happening in the scene/argument and why this moment matters or lands with such force. Keep it conversational and grounded in the book—NO preachy life advice, NO corporate takeaways, and NO 'How to' hooks.

Respond with a JSON object with this exact structure:
{{
  "quotes": [
    {{
      "quote": "exact quote from the text",
      "explanation": "2-3 plain-English sentences explaining the scene context and why this moment is memorable without spoilers",
      "tags": ["tag1", "tag2"]
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
            parsed = json.loads(data.get("response", "{}"))
            return parsed.get("quotes", [])
    except Exception as e:
        print(f"  [Ollama error: {e}]", file=sys.stderr)
        return []

def download_from_gdrive(remote_filename: str) -> Path:
    target = SCRATCH / Path(remote_filename).name
    if target.exists() and target.stat().st_size > 0:
        return target
    remote_path = f"gdrive:Books/Fiction ／ non fiction/{remote_filename}"
    cmd = [RCLONE, "copyto", remote_path, str(target)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  [Error downloading {remote_filename}: {res.stderr.strip()}]")
        return None
    return target

def sync_and_commit(books_processed, total_quotes):
    try:
        print(f"\n--- Syncing & committing after {books_processed} books ({total_quotes} quotes) ---")
        subprocess.run(["python3", str(ROOT / "tools" / "sync_quote_bank_md.py")], check=True)
        subprocess.run(["python3", str(ROOT / "tools" / "build_prototype.py")], check=True)
        subprocess.run(["python3", str(ROOT / "tools" / "lint_cards.py")], check=True)
        subprocess.run(["git", "-C", str(ROOT), "add", "content/quote-bank.json", "content/quote-bank.md", "prototype/index.html"], check=True)
        commit_msg = f"feat(quotes): auto-sync continuous library sweep ({total_quotes} quotes in bank)"
        subprocess.run(["git", "-C", str(ROOT), "commit", "-m", commit_msg], check=False)
        subprocess.run(["git", "-C", str(ROOT), "push", "origin", "main"], check=False)
        print("--- Git commit and push complete! ---\n")
    except Exception as e:
        print(f"  [Sync warning: {e}]")

def run_continuous():
    with open(QB_PATH, "r", encoding="utf-8") as f:
        bank = json.load(f)

    existing_works = set(q["work"].lower().strip() for q in bank if "work" in q)
    existing_quotes = set(q["quote"].strip() for q in bank)

    def get_title_tokens(s):
        s = re.sub(r"\.(epub|mobi|pdf)$", "", s, flags=re.I)
        s = re.split(r"[:\-\(\[\{]", s)[0]
        return set(w for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) > 2)

    existing_titles = [q["work"] for q in bank if "work" in q]

    def is_already_mined(fn):
        fn_tokens = get_title_tokens(fn)
        if not fn_tokens:
            return False
        for et in existing_titles:
            et_tokens = get_title_tokens(et)
            if not et_tokens:
                continue
            overlap = fn_tokens & et_tokens
            if len(overlap) >= len(et_tokens) or (len(overlap) >= 2 and len(overlap) >= len(fn_tokens) * 0.7):
                return True
        return False

    with open(ROOT / "scripts" / "gdrive_file_list.txt") as f:
        raw_lines = [l.strip() for l in f if l.strip().endswith(".epub")]

    # Parse actual remote paths from rclone output (stripping leading file size)
    all_epubs = []
    for l in raw_lines:
        m = re.match(r"^\s*(\d+)\s+(.+)$", l)
        if m:
            all_epubs.append(m.group(2).strip())
        else:
            all_epubs.append(l.strip())

    # Exclude files already in bank
    unmined = [fn for fn in all_epubs if not is_already_mined(fn)]

    print(f"============================================================")
    print(f"CONTINUOUS FULL-LIBRARY RUNNER STARTING")
    print(f"Total EPUBs in Library: {len(all_epubs)}")
    print(f"Already Mined: {len(all_epubs) - len(unmined)}")
    print(f"Remaining to Process: {len(unmined)}")
    print(f"Current Bank Size: {len(bank)} quotes")
    print(f"============================================================")

    books_processed = 0
    quotes_added_total = 0

    for idx, remote_fn in enumerate(unmined, 1):
        print(f"\n[{idx}/{len(unmined)}] Processing: {remote_fn}")
        epub_path = download_from_gdrive(remote_fn)
        if not epub_path or not epub_path.exists():
            print(f"  Skipping {remote_fn} (download failed)")
            continue

        try:
            # Metadata from EPUB
            c_author, c_title = get_epub_metadata(epub_path)
            fb_author, fb_title = parse_filename_fallback(remote_fn)
            author = c_author or fb_author
            title = c_title or fb_title

            # Clean up author/title
            author = re.sub(r"\s+", " ", author).strip()
            title = re.sub(r"\s+", " ", title).strip()

            print(f"  Identified: '{title}' by {author}")

            # Check if this title is already substantially in bank
            if any(title.lower() == q.get("work", "").lower() for q in bank):
                print(f"  Already in bank under work name '{title}', skipping.")
                continue

            chapters = extract_chapters(epub_path)
            if not chapters:
                print(f"  No substantive chapters extracted, skipping.")
                continue

            # Anti-spoiler gate: sample only from the first 85% of chapters
            eligible_chapters = chapters[: max(1, int(len(chapters) * 0.85))]
            all_chunks = []
            for ch in eligible_chapters:
                all_chunks.extend(chunk_text(ch["text"]))

            if not all_chunks:
                print(f"  No valid text chunks found, skipping.")
                continue

            # Sample up to 10 chunks evenly across the eligible range
            step = max(1, len(all_chunks) // 10)
            sample = [all_chunks[i] for i in range(0, len(all_chunks), step)][:10]

            mined_candidates = []
            for c_idx, chunk in enumerate(sample, 1):
                candidates = ask_local_model(chunk, author, title)
                for c in candidates:
                    q_text = c.get("quote", "").strip()
                    if q_text and len(q_text) > 25 and q_text not in existing_quotes:
                        c["author"] = author
                        c["work"] = title
                        c["tags"] = c.get("tags", ["craft", "observation"])
                        mined_candidates.append(c)
                        existing_quotes.add(q_text)
                if len(mined_candidates) >= 5:
                    break

            # Pick top 4-5 quotes per book
            selected = mined_candidates[:4]
            if selected:
                bank.extend(selected)
                quotes_added_total += len(selected)
                books_processed += 1
                print(f"  ✓ Added {len(selected)} vetted quotes (total bank: {len(bank)})")

                # Save bank to disk
                with open(QB_PATH, "w", encoding="utf-8") as f:
                    json.dump(bank, f, indent=2, ensure_ascii=False)

                # Periodic sync and push every 10 books
                if books_processed % 10 == 0:
                    sync_and_commit(books_processed, len(bank))
            else:
                print(f"  No suitable candidates extracted.")

        except Exception as e:
            print(f"  Error processing {remote_fn}: {e}")
        finally:
            # Immediate scratch purge to honor disk discipline
            if epub_path and epub_path.exists():
                try:
                    epub_path.unlink()
                except Exception:
                    pass

    # Final sync at end
    sync_and_commit(books_processed, len(bank))
    print(f"\n============================================================")
    print(f"SWEEP COMPLETE! Processed {books_processed} books. Total bank: {len(bank)} quotes.")
    print(f"============================================================")

if __name__ == "__main__":
    run_continuous()
