# clean_pdf_watermarks.py — Removes the OceanofPDF watermark from calibre-made PDFs (link + italic footer text)
# Usage: .cache/pdfenv/bin/python scripts/clean_pdf_watermarks.py <in.pdf> <out.pdf>     # clean + verify, no upload
#        then: rclone copyto <out.pdf> "gdrive:Books/<same path>"   (updates the same Drive file, keeps old version)
# Requires: pypdf in a throwaway uv venv:  uv venv .cache/pdfenv && uv pip install --python .cache/pdfenv/bin/python pypdf
#           Find affected PDFs first with scripts/scan_pdf_watermarks.py.
#
# How: on every page with a link to oceanofpdf.com, drop that link annotation and every text block (BT…ET)
# whose glyphs are ALL drawn inside the link's rectangle (positions computed from cm/Tm/Td, so it works
# whatever font the page used for the watermark), plus lines/boxes (the link underline) drawn entirely inside it.
# Verify (any failure = no output): same page count, each page's extracted words equal the original's minus
# the watermark words (nothing else lost, added or reordered), same images per page, no oceanofpdf left.
#
# Gotchas:
# - Don't pick the watermark by font: calibre drew it in Helvetica-Oblique on some pages and in the book's own
#   Palatino-Italic (same font as real italics) on others. The link rectangle is the reliable locator.
# - Text is drawn with Identity-H glyph codes, so "OceanofPDF" never appears as bytes in the content
#   stream; identify the block by its font (Helvetica-Oblique) and prove the result by text extraction.
# - Only 1 PDF had it on 2026-11-21 (A Cup of Zen): this handles calibre's layout, not arbitrary PDFs.

import difflib
import re
import sys

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, ContentStream, NameObject

JUNK = re.compile(r"^(?:oceanofpdf|\.|com|oceanofpdf\.com|www\.oceanofpdf\.com)$", re.I)


def words(page):
    return (page.extract_text() or "").split()


def mul(m, n):
    """PDF matrix product m x n ([a b c d e f])."""
    a, b, c, d, e, f = m
    A, B, C, D, E, F = n
    return [a * A + b * C, a * B + b * D, c * A + d * C, c * B + d * D, e * A + f * C + E, e * B + f * D + F]


def strip_page(page, reader):
    annots = page.get("/Annots")
    if not annots:
        return False
    rects, keep = [], []
    for a in annots:
        o = a.get_object()
        if "oceanofpdf" in str(o.get("/A", {}).get("/URI", "")).lower():
            x0, y0, x1, y1 = [float(v) for v in o["/Rect"]]
            rects.append((min(x0, x1) - 2, min(y0, y1) - 4, max(x0, x1) + 2, max(y0, y1) + 4))
        else:
            keep.append(a)
    if not rects:
        return False
    page[NameObject("/Annots")] = ArrayObject(keep)
    cs = ContentStream(page.get_contents(), reader)
    ops = cs.operations
    ctm, stack = [1, 0, 0, 1, 0, 0], []
    drop, block_start, block_pts = set(), None, []
    tm = tlm = [1, 0, 0, 1, 0, 0]
    leading = 0.0
    path_start, path_pts = None, []
    PATH_OPS = {b"m", b"l", b"c", b"v", b"y", b"re", b"h"}
    PAINT_OPS = {b"S", b"s", b"f", b"F", b"f*", b"B", b"B*", b"b", b"b*", b"n"}

    def pt(x, y):
        a_, b_, c_, d_, e_, f_ = ctm
        return (a_ * x + c_ * y + e_, b_ * x + d_ * y + f_)

    def inside_rect(p):
        return any(r[0] <= p[0] <= r[2] and r[1] <= p[1] <= r[3] for r in rects)

    for k, (o, op) in enumerate(ops):
        if block_start is None and op in PATH_OPS:          # underline drawn as a line/box under the link
            if path_start is None:
                path_start, path_pts = k, []
            nums = [float(v) for v in o]
            if op == b"re":
                x, y, w_, h_ = nums
                path_pts += [pt(x, y), pt(x + w_, y + h_)]
            else:
                path_pts += [pt(nums[i], nums[i + 1]) for i in range(0, len(nums) - 1, 2)]
        elif block_start is None and op in PAINT_OPS and path_start is not None:
            if path_pts and all(inside_rect(p) for p in path_pts):
                drop.update(range(path_start, k + 1))
            path_start = None
        if op == b"q":
            stack.append(ctm)
        elif op == b"Q" and stack:
            ctm = stack.pop()
        elif op == b"cm":
            ctm = mul([float(v) for v in o], ctm)
        elif op == b"BT":
            block_start, block_pts = k, []
            tm = tlm = [1, 0, 0, 1, 0, 0]
        elif op == b"Tm":
            tm = tlm = [float(v) for v in o]
        elif op in (b"Td", b"TD"):
            tm = tlm = mul([1, 0, 0, 1, float(o[0]), float(o[1])], tlm)
            if op == b"TD":
                leading = -float(o[1])
        elif op == b"TL":
            leading = float(o[0])
        elif op in (b"T*", b"'", b'"'):
            tm = tlm = mul([1, 0, 0, 1, 0, -leading], tlm)
        if op in (b"Tj", b"TJ", b"'", b'"') and block_start is not None:
            full = mul(tm, ctm)
            block_pts.append((full[4], full[5]))
        if op == b"ET" and block_start is not None:
            inside = lambda p: any(r[0] <= p[0] <= r[2] and r[1] <= p[1] <= r[3] for r in rects)
            if block_pts and all(inside(p) for p in block_pts):
                drop.update(range(block_start, k + 1))
            block_start = None
    out = [x for k, x in enumerate(ops) if k not in drop]
    cs.operations = out
    page.replace_contents(cs)
    return True


def main():
    src, dst = sys.argv[1], sys.argv[2]
    before = PdfReader(src)
    w = PdfWriter(clone_from=src)
    changed = sum(strip_page(p, w) for p in w.pages)
    w.compress_identical_objects(remove_duplicates=False, remove_unreferenced=True)   # drop the unlinked link objects
    w.write(dst)
    after = PdfReader(dst)
    problems = []
    if len(before.pages) != len(after.pages):
        problems.append("page count changed")
    for i, (a, b) in enumerate(zip(before.pages, after.pages)):
        wa, wb = words(a), words(b)
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, wa, wb, autojunk=False).get_opcodes():
            if op == "equal":
                continue
            if op != "delete" or not all(JUNK.match(x) for x in wa[i1:i2]):
                problems.append(f"page {i + 1}: text changed near {' '.join(wa[max(0, i1 - 5):i2 + 5])[:100]!r}")
        if len(a.images) != len(b.images):
            problems.append(f"page {i + 1}: images changed")
        if "oceanofpdf" in " ".join(wb).lower().replace(" ", "") or "oceanofpdf" in str(b.get("/Annots", "")).lower():
            problems.append(f"page {i + 1}: watermark left")
    raw = open(dst, "rb").read().lower().count(b"oceanofpdf")
    if raw:
        problems.append(f"{raw} oceanofpdf reference(s) still inside the file")
    if problems:
        import os
        os.remove(dst)
        print("NOT SAFE, no output written:\n  " + "\n  ".join(problems[:20]))
        sys.exit(1)
    print(f"OK: watermark removed from {changed} page(s); every page's text otherwise identical -> {dst}")


if __name__ == "__main__":
    main()
