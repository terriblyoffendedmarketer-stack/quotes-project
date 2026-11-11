# scripts/migrations/extract_bookshelf_template_2026_11.py — ONE-TIME: pulled the HTML out of the old
# generate_app_html() f-string into scripts/templates/bookshelf.html (plain HTML, single braces).
# Usage: python3 scripts/migrations/extract_bookshelf_template_2026_11.py  (run on 2026-11-11 against commit 7a20bce)
#
# Gotchas:
# - Don't unescape {{ }} with string replace: the f-string also contains backslash escapes ("\\n", "\\\\\\'")
#   that Python must evaluate. Instead swap the 5 interpolations for @@TOKENS@@ and exec the function.
import re, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
src = subprocess.run(["git", "show", "7a20bce:scripts/build_independent_bookshelf_app.py"], cwd=ROOT,
                     capture_output=True, text=True, check=True).stdout
fn = src[src.index("def generate_app_html"):src.index('if __name__ == "__main__":')]
for expr, tok in [("{shelf_json_str}", "@@SHELF_JSON@@"), ("{total_books}", "@@TOTAL_BOOKS@@"),
                  ("{covers_count}", "@@COVERS_COUNT@@"), ("{quote_count}", "@@QUOTE_COUNT@@"),
                  ("{len(tbr_lines)}", "@@TBR_COUNT@@")]:
    fn = fn.replace(expr, tok)
ns = {"json": __import__("json")}
exec(fn, ns)
html = ns["generate_app_html"]([], [], 0)
out = ROOT / "scripts" / "templates" / "bookshelf.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out} ({len(html)} chars), tokens:", sorted(set(re.findall(r"@@[A-Z_]+@@", html))))
