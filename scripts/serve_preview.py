#!/usr/bin/env python3
# serve_preview.py — Lightweight local HTTP server for Marginalia Visual Studio
# Usage: python3 scripts/serve_preview.py [port]
# Requires: Python 3 standard library only

import sys
import os
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTOTYPE_DIR = ROOT / "prototype"

class PrototypeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PROTOTYPE_DIR), **kwargs)

    def end_headers(self):
        # Disable browser caching for live editing
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    server_address = ("0.0.0.0", port)
    
    # Ensure index.html exists
    index_file = PROTOTYPE_DIR / "index.html"
    if not index_file.exists():
        print("prototype/index.html not found. Building now...")
        os.system(f"python3 '{ROOT / 'tools' / 'build_prototype.py'}'")

    httpd = ThreadingHTTPServer(server_address, PrototypeHandler)
    url = f"http://localhost:{port}"
    print(f"\n=======================================================")
    print(f"  Marginalia Visual Studio Live on Computer")
    print(f"  URL: {url}")
    print(f"  - App Reader & ViewPager Simulator")
    print(f"  - Home Screen Widget Simulator (Cards & Shelf Spark)")
    print(f"  - Light & Dark Mode Instant Toggle")
    print(f"  - Thematic Horizons Categorized Catalog")
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
