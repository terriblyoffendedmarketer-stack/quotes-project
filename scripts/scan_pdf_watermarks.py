# scan_pdf_watermarks.py — Finds PDFs that carry the OceanofPDF watermark and HOW it is stored (read-only)
# Usage: python3 scripts/scan_pdf_watermarks.py .cache/pdfs     # needs a local mirror:
#        rclone copy gdrive:Books .cache/pdfs --filter "- Archive of bullshit/**" --filter "+ *.pdf" --filter "- *"
# Requires: Python 3 stdlib only. Writes content/pdf_watermark_scan.md.
#
# Per PDF it counts: link annotations to oceanofpdf (uncompressed /URI), page-text hits (decompressed
# FlateDecode content streams), and whether the page text is searchable at all (scans = images only).
#
# Gotchas:
# - Text in content streams is often drawn with font-specific codes, so "OceanofPDF" may not appear as
#   plain bytes even when visible; the /URI link annotation is the reliable marker for this site.

import re
import sys
import time
import zlib
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

MARK = re.compile(rb"oceanofpdf", re.I)
STREAM = re.compile(rb"stream\r?\n(.*?)\r?\nendstream", re.S)


def scan(path):
    data = Path(path).read_bytes()
    raw_hits = len(MARK.findall(data))
    uri_hits = len(re.findall(rb"/URI\s*\(\s*https?://(?:www\.)?oceanofpdf", data, re.I))
    text_hits = streams = text_streams = 0
    for m in STREAM.finditer(data):
        streams += 1
        try:
            d = zlib.decompress(m.group(1))
        except Exception:
            continue
        if re.search(rb"\b(?:Tj|TJ)\b", d):
            text_streams += 1
        text_hits += len(MARK.findall(d))
    pages = len(re.findall(rb"/Type\s*/Page\b", data))
    return {"path": str(path), "pages": pages, "uri": uri_hits, "text": text_hits, "raw": raw_hits,
            "has_text": text_streams > 0, "mb": round(len(data) / 1e6, 1)}


def main():
    root = Path(sys.argv[1])
    files = sorted(root.rglob("*.pdf"))
    with ProcessPoolExecutor() as ex:
        rows = list(ex.map(scan, files, chunksize=4))
    hit = [r for r in rows if r["uri"] or r["text"] or r["raw"]]
    lines = [f"# PDF watermark scan — {time.strftime('%Y-%m-%d')}", "",
             f"{len(rows)} PDFs: {len(hit)} carry OceanofPDF. "
             f"{sum(1 for r in rows if not r['has_text'])} have no searchable text (scans).", "",
             "| PDF | pages | link marks | text marks | other raw |", "|---|---|---|---|---|"]
    for r in sorted(hit, key=lambda r: -max(r["uri"], r["text"])):
        lines.append(f"| {Path(r['path']).relative_to(root)} | {r['pages']} | {r['uri']} | {r['text']} | {r['raw']} |")
    Path(__file__).resolve().parent.parent.joinpath("content", "pdf_watermark_scan.md").write_text("\n".join(lines) + "\n")
    print(lines[2])


if __name__ == "__main__":
    main()
