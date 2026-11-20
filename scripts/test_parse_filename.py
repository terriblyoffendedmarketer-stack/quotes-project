# test_parse_filename.py — Checks that messy download filenames parse into the right (title, author)
# Usage: python3 scripts/test_parse_filename.py          # offline cases only
#        python3 scripts/test_parse_filename.py --net    # also the Open Library whole-name lookup cases
# Requires: Python 3 stdlib (+ network for --net). Add a case here whenever a new kind of junk name shows up.
#
# Gotchas:
# - Watermark stripping is a generic "word.tld" regex (oceanofpdf.com, z-library.sk, dokumen.pub...). Titles
#   with real domains in them would lose that word; none on the shelf so far.
# - Names with no separator ("the_midnight_library_matt_haig") can't be split offline; enrich_new_books.py's
#   whole_name_match() asks Open Library and only accepts a hit whose title AND author surname are in the name.

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shelf_common import parse_filename  # noqa: E402

OFFLINE = [
    ("OceanofPDF.com_Project_Hail_Mary_-_Andy_Weir.epub", ("Project Hail Mary", "Andy Weir")),
    ("_OceanofPDF.com_Piranesi_-_Susanna_Clarke.epub", ("Piranesi", "Susanna Clarke")),
    ("Klara and the Sun (Kazuo Ishiguro) (z-library.sk, 1lib.sk, z-lib.sk).epub", ("Klara and the Sun", "Kazuo Ishiguro")),
    ("Normal People - Sally Rooney [Anna’s Archive].epub", ("Normal People", "Sally Rooney")),
    ("Snow Crash - Neal Stephenson.epub", ("Snow Crash", "Neal Stephenson")),
    ("Second Look – A Magazine of Stories, Essays & Ideas (Issue One).epub",
     ("Second Look – A Magazine of Stories, Essays & Ideas", "Unknown")),
    ("Dev.D_(screenplay)pdf.pdf", ("Dev.D", "Unknown")),
]
ONLINE = [
    ("oceanofpdf.com_The_Midnight_Library_Matt_Haig.pdf", ("The Midnight Library", "Matt Haig")),
    ("dokumen.pub_atomic-habits-james-clear.pdf", ("Atomic Habits", "James Clear")),
]


def run(cases, net):
    bad = 0
    for fn, want in cases:
        got = parse_filename(fn, set())
        if net and got[1] == "Unknown":
            from enrich_new_books import whole_name_match
            d, t, a = whole_name_match(got[0])
            got = (t, a) if d else got
        ok = got == want
        bad += not ok
        print(("ok   " if ok else "FAIL ") + f"{fn}\n       -> {got}" + ("" if ok else f"   wanted {want}"))
    return bad


if __name__ == "__main__":
    fails = run(OFFLINE, False) + (run(ONLINE, True) if "--net" in sys.argv else 0)
    print("all passed" if not fails else f"{fails} failed")
    sys.exit(1 if fails else 0)
