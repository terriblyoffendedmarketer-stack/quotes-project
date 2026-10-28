# mine_cluster.py — Downloads, mines, and cleans up a cluster of books using rclone and local Ollama (gemma3:4b)
# Usage: python3 scripts/mine_cluster.py <cluster_json_path>
# Requires: rclone configured with 'gdrive:', local Ollama with gemma3:4b
#
# Gotchas:
# - Always removes the downloaded EPUB immediately after mining to honor the ~12 GB disk ceiling.
# - Skips downloading if the file is already in scratch.
# - Output is saved as JSON for supervisor review.

import json
from pathlib import Path
import subprocess
import sys

# Ensure stdout flushes immediately for background tasks
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mine_quote_bank import mine_epub

SCRATCH = Path("/Users/apple/.gemini/antigravity/brain/6282abf0-33f0-44df-ac5d-1d65c90f0f65/scratch")
SCRATCH.mkdir(parents=True, exist_ok=True)
RCLONE = "/opt/homebrew/bin/rclone"

def download_from_gdrive(remote_filename: str) -> Path:
    target = SCRATCH / Path(remote_filename).name
    if target.exists() and target.stat().st_size > 0:
        return target
    
    remote_path = f"gdrive:Books/Fiction ／ non fiction/{remote_filename}"
    cmd = [RCLONE, "copyto", remote_path, str(target)]
    print(f"Downloading from Google Drive: {remote_filename}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error downloading {remote_filename}: {res.stderr}")
        return None
    return target

def process_cluster(cluster_file: Path):
    cluster = json.loads(cluster_file.read_text())
    cluster_name = cluster.get("name", "cluster")
    books = cluster.get("books", [])
    out_file = Path(__file__).resolve().parent.parent / "content" / f"{cluster_name}_raw.json"

    all_quotes = []
    for b in books:
        r_file = b["remote_file"]
        local_epub = download_from_gdrive(r_file)
        if not local_epub or not local_epub.exists():
            print(f"Failed to fetch {r_file}, skipping.")
            continue

        print(f"\n==========================================")
        print(f"Mining: {b['title']} by {b['author']}")
        print(f"==========================================")
        try:
            quotes = mine_epub(
                str(local_epub),
                b["author"],
                b["title"],
                b.get("year"),
                b.get("translator"),
                max_chunks=b.get("chunks", 8)
            )
            print(f"Mined {len(quotes)} candidate quotes from {b['title']}")
            for q in quotes:
                q["remote_file"] = r_file
            all_quotes.extend(quotes)
        except Exception as e:
            print(f"Error mining {b['title']}: {e}")
        finally:
            # Delete local EPUB immediately to preserve disk space
            if local_epub.exists():
                local_epub.unlink()
                print(f"Purged local scratch file: {local_epub.name}")

    out_file.write_text(json.dumps(all_quotes, indent=2, ensure_ascii=False))
    print(f"\nCompleted cluster {cluster_name}! Saved {len(all_quotes)} candidate quotes to {out_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/mine_cluster.py <cluster_json>")
        sys.exit(1)
    process_cluster(Path(sys.argv[1]))
