#!/usr/bin/env python3
# scripts/serve_bookshelf.py — Local helper server for My Reading Corner, with the in-app "Tidy Drive names" button
# Usage: python3 scripts/serve_bookshelf.py [port] [--no-browser]     (default port 8899, http://localhost:8899)
#        Runs permanently via ~/Library/LaunchAgents/com.local.reading-corner-server.plist (see scripts/launchd/).
# Requires: Python 3 standard library; for the tidy job also rclone (`gdrive:`) and git — same as refresh_bookshelf.sh
#
# API (only reachable from this Mac — bound to 127.0.0.1):
#   GET  /api/status -> {"available": true, "running": bool, "log": "<last lines>", "last_exit": int|null}
#   POST /api/tidy   -> starts `refresh_bookshelf.sh --tidy --publish` (sync Drive, add new books, verify + rename
#                       Drive files, rebuild, publish). The page shows the button only when /api/status answers,
#                       so the public GitHub Pages copy never shows it.
#   POST /api/archive {"id": "<shelf id>", "archived": true|false}
#                    -> records the choice in content/book_overrides.json so it applies on every device after the
#                       next build + publish (the page also keeps it in localStorage immediately).
#
# Gotchas:
# - POST is refused unless the Origin header is this server itself: otherwise any website you visit could
#   trigger the job by posting to localhost.
# - Only one job at a time; a second click while running just returns the current status.
# - No-cache headers so a rebuilt index.html shows up on refresh.

import json
import subprocess
import sys
import threading
import webbrowser
from collections import deque
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKSHELF_DIR = ROOT / "bookshelf"
REFRESH = ROOT / "scripts" / "refresh_bookshelf.sh"

JOB = {"running": False, "log": deque(maxlen=400), "last_exit": None}
LOCK = threading.Lock()


def run_tidy():
    JOB["log"].clear()
    proc = subprocess.Popen(["/bin/bash", str(REFRESH), "--tidy", "--publish"], cwd=ROOT,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        JOB["log"].append(line.rstrip())
    JOB["last_exit"] = proc.wait()
    JOB["running"] = False


class BookshelfHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BOOKSHELF_DIR), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def _json(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _status(self):
        return {"available": True, "running": JOB["running"], "log": "\n".join(list(JOB["log"])[-60:]),
                "last_exit": JOB["last_exit"]}

    def do_GET(self):
        if self.path.startswith("/api/status"):
            return self._json(200, self._status())
        return super().do_GET()

    def do_POST(self):
        origin = self.headers.get("Origin", "")
        host = self.headers.get("Host", "")
        if origin not in (f"http://{host}", f"http://localhost:{self.server.server_port}",
                          f"http://127.0.0.1:{self.server.server_port}"):
            return self._json(403, {"error": "cross-origin request refused"})
        if self.path.startswith("/api/archive"):
            return self._archive()
        if not self.path.startswith("/api/tidy"):
            return self._json(404, {"error": "not found"})
        with LOCK:
            if not JOB["running"]:
                JOB["running"] = True
                JOB["last_exit"] = None
                threading.Thread(target=run_tidy, daemon=True).start()
        return self._json(202, self._status())

    def _archive(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0) or 0)) or b"{}")
            book_id, flag = str(body["id"]), bool(body["archived"])
        except Exception:
            return self._json(400, {"error": "expected {id, archived}"})
        path = ROOT / "content" / "book_overrides.json"
        with LOCK:
            data = json.loads(path.read_text(encoding="utf-8"))
            entry = data["books"].setdefault(book_id, {})
            if flag:
                entry["archived"] = True
            else:
                entry.pop("archived", None)
                if not entry:
                    data["books"].pop(book_id)
            path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        return self._json(200, {"ok": True, "id": book_id, "archived": flag})

    def log_message(self, fmt, *args):
        if "/api/status" not in (args[0] if args else ""):
            super().log_message(fmt, *args)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    port = int(args[0]) if args else 8899
    if not (BOOKSHELF_DIR / "index.html").exists():
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build_independent_bookshelf_app.py")], check=False)
    httpd = ThreadingHTTPServer(("127.0.0.1", port), BookshelfHandler)
    url = f"http://localhost:{port}"
    print(f"My Reading Corner helper running at {url}  (Ctrl+C to stop)", flush=True)
    if "--no-browser" not in sys.argv:
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
