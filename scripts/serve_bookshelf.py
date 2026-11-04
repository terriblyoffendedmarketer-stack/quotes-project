#!/usr/bin/env python3
# scripts/serve_bookshelf.py — Lightweight local HTTP server for 'Anything That Doesn't Suck'
# Usage: python3 scripts/serve_bookshelf.py [port]
# Requires: Python 3 standard library only

import sys
import os
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKSHELF_DIR = ROOT / "bookshelf"

class BookshelfHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BOOKSHELF_DIR), **kwargs)

    def end_headers(self):
        # Disable browser caching for live viewing
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8899
    server_address = ("127.0.0.1", port)
    
    index_file = BOOKSHELF_DIR / "index.html"
    if not index_file.exists():
        print("bookshelf/index.html not found. Building now...")
        os.system(f"python3 '{ROOT / 'scripts' / 'build_independent_bookshelf_app.py'}'")

    httpd = ThreadingHTTPServer(server_address, BookshelfHandler)
    url = f"http://localhost:{port}"
    print(f"\n=======================================================")
    print(f"  Anything That Doesn't Suck — Live on Browser")
    print(f"  URL: {url}")
    print(f"  - 3-Mode View Switcher (📌 Covers | 📰 Editorial 3x2 | 📚 Bookshelf)")
    print(f"  - 498 Verified Covers with Clean Artwork")
    print(f"  - Single-Open Collapsible Companion Insights")
    print(f"  - Real Back-of-the-Book Synopses & 'Damn Factor' Accolades")
    print(f"=======================================================\n")
    print("Press Ctrl+C to stop the server.\n")

    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main()
