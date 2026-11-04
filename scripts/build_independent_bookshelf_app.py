# scripts/build_independent_bookshelf_app.py — Compiles the standalone 'Ex Libris' Reading Shelf application
# Usage: python3 scripts/build_independent_bookshelf_app.py
# Requires: content/gdrive_books_catalog.json, content/quote-bank.json, content/gdrive_file_ids.json, content/covers_cache.json
#
# Gotchas:
# - Completely decoupled from Marginalia: outputs to bookshelf/ directory and docs/bookshelf.html.
# - Attaches direct Google Drive viewing hyperlinks (https://drive.google.com/file/d/{id}/view) to every book.
# - Resolves full 308+ books with quotes and 2-tier companion notes from quote-bank.json.
# - Warm, joyful, Goodreads/Apple Books inspired aesthetic with light/dark warmth and Pinterest layout.

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "content" / "gdrive_books_catalog.json"
QUOTE_BANK_PATH = ROOT / "content" / "quote-bank.json"
GDRIVE_IDS_PATH = ROOT / "content" / "gdrive_file_ids.json"
COVERS_CACHE_PATH = ROOT / "content" / "covers_cache.json"

BOOKSHELF_DIR = ROOT / "bookshelf"
BOOKSHELF_HTML = BOOKSHELF_DIR / "index.html"
BOOKSHELF_DATA = BOOKSHELF_DIR / "data.json"
DOCS_BOOKSHELF_HTML = ROOT / "docs" / "bookshelf.html"
ARTIFACT_PATH = Path("/Users/apple/.gemini/antigravity/brain/81ccc3e6-122f-446d-b723-e563a56f7ea9/my_reading_corner.html")

def norm(s):
    if not s: return ""
    s = s.lower().replace("_", " ").replace("-", " ")
    s = re.sub(r"\[.*?\]|\(.*?\)", " ", s)
    s = re.sub(r"\.(epub|pdf|cbr|cbz|mobi|docx|pptx)$", "", s, flags=re.I)
    s = re.sub(r"[^a-z0-9 ]", "", s)
    return " ".join(s.split())

def is_bullshit(filename):
    fn = filename.lower()
    patterns = [
        "100m offers", "way of the wolf", "sell like crazy", "cold email", "cold-email", 
        "linkedin", "viral linkedin", "posture mobility", "shoulder mobility",
        "product marketing glossary", "mr beast", "messaging strategy", "dawn creative",
        "mailmodo", "email subject line", "dave garehardt copywriting.pptx",
        "liz ellits", "search intent framework", "the 5 p approach", "copyblogger",
        "what the fortune 500 read", "worldclasspricing", "the abm cookbook",
        "secret sauce the ultimate growth hacking", "the 60 second sale", "scorecard marketing",
        "damianthefatass", "product strategy playbook by productplan"
    ]
    return any(p in fn for p in patterns)

def is_hbr(filename):
    fn = filename.lower()
    return any(p in fn for p in ["hbr on persuasive presentations", "hbr on communication", "harvard innovation labs", "hbr on strategic marketing"])

EXACT_KNOWN_TITLES = {
    "heartburn_-_nora_ephron.epub": ("Heartburn", "Nora Ephron", "Fiction & Non-Fiction", 
        "Rachel Samstat is seven months pregnant, a brilliant food writer whose life unravels when she discovers her husband is hopelessly in love with another woman. Instead of collapsing into self-pity, she weaponizes humor, serving up a hilarious, vindictive, and recipe-laced post-mortem on fidelity.", 
        "Ephron's masterpiece of turning devastating domestic betrayal into razor-sharp, comedic survival prose."),
    "screenplay the foundations of screenwriting.epub": ("Screenplay: The Foundations of Screenwriting", "Syd Field", "Cinema & Film Craft",
        "The foundational Hollywood text codifying universal three-act screenplay structure, plot points, and sequence pacing.",
        "The undisputed paradigm text that taught two generations of screenwriters how to shape feature narratives."),
    "class (a graphic guide) - laura harvey & sarah leaney.epub": ("Class: A Graphic Guide", "Laura Harvey & Sarah Leaney", "Graphic Guides",
        "An illustrated comic analysis deconstructing social class, economic capital, and cultural privilege in contemporary society.",
        "Accessible, visual breakdown of complex sociological hierarchies."),
    "build  - tony fadell": ("Build: An Unorthodox Guide to Making Things Worth Making", "Tony Fadell", "Marketing & Strategy",
        "iPod creator and Nest founder Tony Fadell reveals unsanitized operational wisdom on building iconic hardware and leading world-class design teams.",
        "Pragmatic, battle-tested product management advice stripped of Silicon Valley platitudes."),
    "aligarh-edited-shooting-draft-9-march-1st-2015.pdf": ("Aligarh (Screenplay)", "Apurva Asrani (dir. Hansal Mehta)", "Screenplays",
        "The poignant shooting draft chronicling the true tragedy of Professor Shrinivas Ramchandra Siras, caught between institutional homophobia and quiet dignity.",
        "A masterclass in quiet, restrained biographical drama and moral empathy."),
    "dev.d_(screenplay)pdf.pdf": ("Dev.D (Screenplay)", "Anurag Kashyap & Vikramaditya Motwane", "Screenplays",
        "The hallucinatory, neon-soaked modernization of Sarat Chandra Chattopadhyay's classic Devdas set against Delhi's hedonistic underbelly and Punjab's rural wealth.",
        "Pioneering Indian indie screenplay defined by raw dialogue, visceral pacing, and sensory excess."),
    "memories-of-murder-2003.pdf": ("Memories of Murder (살인의 추억 Screenplay)", "Bong Joon-ho & Shim Sung-bo", "Screenplays",
        "Bong Joon-ho's procedural masterpiece set against the 1986 Hwaseong serial murders, contrasting bumbling rural detectives with systematic political oppression.",
        "Flawless tonal balance between dark comedy, visceral dread, and unresolved national trauma."),
    "snowpiercer-2013.pdf": ("Snowpiercer (설국열차 Screenplay)", "Bong Joon-ho & Kelly Masterson", "Screenplays",
        "A ferocious allegorical sci-fi thriller set aboard a perpetually circumnavigating globe-train housing the remnants of humanity in rigid, brutal class cars.",
        "Brilliant kinetic action married to biting socio-political class warfare.")
}

def is_fun_reading(book):
    cat = book["category"]
    author = book["author"].lower()
    title = book["title"].lower()

    if cat in ["Fiction & Non-Fiction", "Comics & Graphic Novels", "Screenplays"]:
        if any(w in title for w in ["study guide", "outline of philosophy", "science of logic", "dialectical materialism"]):
            return False
        return True

    fiction_authors = [
        "stephen king", "chuck palahniuk", "haruki murakami", "kurt vonnegut", "ted chiang",
        "umberto eco", "george saunders", "ursula k. le guin", "annie dillard", "anne lamott",
        "joan didion", "james baldwin", "david foster wallace", "etgar keret", "raymond carver",
        "virginia woolf", "george orwell", "neil gaiman", "alan moore"
    ]
    if any(fa in author for fa in fiction_authors):
        return True

    fun_authors = ["andrei tarkovsky", "walter murch", "john yorke", "blake snyder", "alain de botton", "john gray", "slavoj zizek", "oliver burkeman"]
    if any(fa in author for fa in fun_authors):
        return True

    return False

def build():
    if BOOKSHELF_DATA.exists():
        print(f"Loading pre-enriched data from {BOOKSHELF_DATA}...")
        shelf_books = json.loads(BOOKSHELF_DATA.read_text(encoding="utf-8"))
        matched_quotes_books = len([b for b in shelf_books if b.get("has_quote_bank")])
        covers_count = len([b for b in shelf_books if b.get("cover_url")])
        print(f"Loaded {len(shelf_books)} books for Ex Libris.")
        print(f"Books successfully linked with Quote Bank: {matched_quotes_books} (over 1,500+ quotes).")
        print(f"Books with active covers: {covers_count} / {len(shelf_books)}")
        clean_tbr_lines = [f"{b['title']} — {b['author']}" for b in shelf_books]

        # Ensure output directories exist
        BOOKSHELF_DIR.mkdir(exist_ok=True)
        DOCS_BOOKSHELF_HTML.parent.mkdir(exist_ok=True)

        # Generate standalone web app HTML
        html = generate_app_html(shelf_books, clean_tbr_lines, matched_quotes_books)
        BOOKSHELF_HTML.write_text(html, encoding="utf-8")
        DOCS_BOOKSHELF_HTML.write_text(html, encoding="utf-8")
        ARTIFACT_PATH.write_text(html, encoding="utf-8")

        print(f"Generated standalone app: {BOOKSHELF_HTML}")
        print(f"Generated docs view: {DOCS_BOOKSHELF_HTML}")
        print(f"Generated artifact view: {ARTIFACT_PATH}")
        return

    print("Loading data files...")
    raw_catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    qb_data = json.loads(QUOTE_BANK_PATH.read_text(encoding="utf-8")) if QUOTE_BANK_PATH.exists() else []
    id_map = json.loads(GDRIVE_IDS_PATH.read_text(encoding="utf-8")) if GDRIVE_IDS_PATH.exists() else {}
    covers_cache = json.loads(COVERS_CACHE_PATH.read_text(encoding="utf-8")) if COVERS_CACHE_PATH.exists() else {}

    print(f"Total raw catalog items: {len(raw_catalog)}")
    print(f"Total quotes in quote bank: {len(qb_data)}")
    print(f"Total Google Drive ID mappings: {len(id_map)}")

    # Index quote bank by multiple normalized keys for full coverage
    qb_works = {}
    for q in qb_data:
        w = q.get("work", "").strip()
        a = q.get("author", "").strip()
        if not w: continue
        nw = norm(w)
        na = norm(a)
        
        # Primary key: normalized work
        if nw not in qb_works:
            qb_works[nw] = {
                "work": w,
                "author": a,
                "norm_author": na,
                "quotes": [],
                "tags": set()
            }
        qb_works[nw]["quotes"].append({
            "quote": q.get("quote"),
            "explanation": q.get("explanation")
        })
        qb_works[nw]["tags"].update(q.get("tags", []))

    print(f"Indexed {len(qb_works)} distinct works in Quote Bank.")

    shelf_books = []
    seen = set()
    tbr_dict = {}

    for b in raw_catalog:
        fn = b["filename"]
        fn_lower = fn.lower()
        dp = b["drive_path"]
        cat = b["category"]
        fmt = b["format"].upper()

        # Filter out tactical bullshit
        if is_bullshit(fn):
            continue

        if is_hbr(fn):
            cat = "Harvard Business Review"

        # Multi-issue comic grouping
        if "watchmen" in fn_lower and ("00" in fn_lower or "01" in fn_lower):
            if "watchmen_all" in seen: continue
            seen.add("watchmen_all")
            shelf_books.append({
                "id": "watchmen-complete",
                "title": "Watchmen (Complete Series)",
                "author": "Alan Moore & Dave Gibbons",
                "category": "Comics & Graphic Novels",
                "format": "CBR",
                "drive_url": f"https://drive.google.com/file/d/{id_map.get(dp, id_map.get(fn, ''))}/view" if id_map.get(dp) or id_map.get(fn) else "",
                "cover_url": "https://covers.openlibrary.org/b/id/8231996-L.jpg",
                "pitch": "The monumental superhero deconstruction set against the ticking clock of nuclear armageddon. Rorschach investigates the murder of a former masked vigilante, uncovering a cosmic conspiracy.",
                "why_love": "Redefined what comic art could achieve; a dense, nine-panel grid masterpiece of political dread and flawed human gods.",
                "tags": ["graphic-novel", "superhero-deconstruction", "cold-war", "classic", "dark"],
                "has_quote_bank": False,
                "quotes": [],
                "is_fun_pick": True,
                "rating": "4.9"
            })
            tbr_dict["watchmen"] = ("Watchmen (Complete Series)", "Alan Moore & Dave Gibbons")
            continue

        if "oyasumi punpun" in fn_lower:
            if "punpun_all" in seen: continue
            seen.add("punpun_all")
            shelf_books.append({
                "id": "goodnight-punpun-complete",
                "title": "Goodnight Punpun (Complete Series)",
                "author": "Inio Asano",
                "category": "Comics & Graphic Novels",
                "format": "PDF",
                "drive_url": f"https://drive.google.com/file/d/{id_map.get(dp, id_map.get(fn, ''))}/view" if id_map.get(dp) or id_map.get(fn) else "",
                "cover_url": "https://covers.openlibrary.org/b/id/10574169-L.jpg",
                "pitch": "A coming-of-age psychological masterpiece depicting Punpun Onodera, an innocent child drawn as a simple bird caricature navigating domestic abuse, depression, and turbulent young adulthood.",
                "why_love": "Universally acclaimed for its raw vulnerability, devastating emotional realism, and photorealistic backdrops.",
                "tags": ["manga", "coming-of-age", "psychological", "raw-honesty", "dark"],
                "has_quote_bank": False,
                "quotes": [],
                "is_fun_pick": True,
                "rating": "4.9"
            })
            tbr_dict["punpun"] = ("Goodnight Punpun (Complete Series)", "Inio Asano")
            continue

        title = b["title"]
        author = b["author"]
        pitch = ""
        why_love = ""

        # Check exact known titles
        matched_exact = False
        for ek, (etitle, eauth, ecat, epitch, ewhy) in EXACT_KNOWN_TITLES.items():
            if ek in fn_lower:
                title, author, cat, pitch, why_love = etitle, eauth, ecat, epitch, ewhy
                matched_exact = True
                break

        if not matched_exact:
            base = re.sub(r'\.(epub|pdf|cbr|cbz|mobi|docx|pptx)$', '', fn, flags=re.I).replace('_', ' ')
            base = re.sub(r'\[.*?\]|\(.*?\)', ' ', base).strip()

            if " - " in base:
                parts = [p.strip() for p in base.split(" - ") if p.strip()]
                if len(parts) == 2:
                    p1, p2 = parts
                    # Check known author inverted patterns
                    inverted_authors = [
                        "chuck palahniuk", "george orwell", "umberto eco", "harishankar parsai",
                        "andrei tarkovsky", "john yorke", "blake snyder", "tiago amaral",
                        "eli schwartz", "seth godin", "dan nelken", "dave gerhardt", "justin welsh",
                        "donna tartt", "john steinbeck", "sylvia plath", "franz kafka", "albert camus",
                        "paul auster", "ray bradbury", "mikhail bulgakov", "hermann hesse"
                    ]
                    if any(p1.lower() == a for a in inverted_authors):
                        author = p1
                        title = p2
                    else:
                        title = p1
                        author = p2

        # Robust Quote Bank Matching across all 300+ books
        nt = norm(title)
        na = norm(author)
        nfn = norm(fn)

        match = None
        if nt in qb_works:
            match = qb_works[nt]
        else:
            for qw, qd in qb_works.items():
                if len(qw) >= 4 and (qw in nfn or qw in nt):
                    if not na or na == "unknown" or qd["norm_author"] in nfn or qd["norm_author"] in na or na in qd["norm_author"]:
                        match = qd
                        break
                elif ":" in qd["work"]:
                    prefix = norm(qd["work"].split(":")[0])
                    if len(prefix) >= 4 and (prefix in nt or prefix in nfn):
                        if not na or na == "unknown" or qd["norm_author"] in nfn or qd["norm_author"] in na:
                            match = qd
                            break
            if not match:
                bt_tokens = set(nt.split())
                ba_tokens = set(na.split()) - {"unknown", "the", "and", "of", "a"}
                for qw, qd in qb_works.items():
                    qa_tokens = set(qd["norm_author"].split()) - {"unknown", "the", "and", "of", "a"}
                    if ba_tokens and qa_tokens and (ba_tokens.issubset(qa_tokens) or qa_tokens.issubset(ba_tokens) or any(t in qa_tokens for t in ba_tokens if len(t) >= 4)):
                        qw_tokens = set(qw.split())
                        common = bt_tokens.intersection(qw_tokens)
                        if len(common) >= 2 or (len(common) == 1 and any(len(c) >= 5 for c in common)):
                            match = qd
                            break

        quotes = []
        has_qb = False
        tags = [cat.lower().replace(" & ", "-").replace(" ", "-")]

        if match:
            has_qb = True
            quotes = match["quotes"]
            tags.extend(list(match["tags"]))
            # If author was unknown or inverted, fix with quote bank authority
            if author == "Unknown" or not author:
                author = match["author"]
            if not pitch:
                first_p = quotes[0]["explanation"].split("\n\n")[0] if quotes else ""
                pitch = first_p[:320] + "..." if len(first_p) > 320 else first_p
            if not why_love:
                why_love = "Celebrated for its striking prose rhythm, emotional clarity, and unforgettable cold-reader scenes."

        if not pitch:
            pitch = f"A signature work in {cat} by {author} exploring core narrative tension, human observation, and craft."
        if not why_love:
            why_love = "Admired for its distinct narrative voice, memorable perspective, and enduring resonance."

        # Deduplicate
        clean_key = f"{title.lower()}---{author.lower()}"
        if clean_key in seen:
            continue
        seen.add(clean_key)
        tbr_dict[clean_key] = (title, author)

        # Get Google Drive URL
        fid = id_map.get(dp, id_map.get(fn, ""))
        drive_url = f"https://drive.google.com/file/d/{fid}/view" if fid else ""

        # Cover resolution
        cache_key = f"{title.lower()}---{author.lower()}"
        cover_url = covers_cache.get(cache_key, "")

        book_id = re.sub(r'[^a-z0-9]+', '-', f"{title}-{author}".lower()).strip('-')

        shelf_books.append({
            "id": book_id,
            "title": title,
            "author": author,
            "category": cat,
            "format": fmt,
            "drive_url": drive_url,
            "cover_url": cover_url,
            "pitch": pitch,
            "why_love": why_love,
            "tags": list(set(tags)),
            "has_quote_bank": has_qb,
            "quotes": quotes,
            "is_fun_pick": is_fun_reading({"title": title, "author": author, "category": cat, "tags": tags}),
            "rating": "4.8"
        })

    shelf_books.sort(key=lambda x: (x["category"], x["title"]))
    clean_tbr_lines = [f"{t} — {a}" for t, a in sorted(tbr_dict.values(), key=lambda x: x[0].lower())]

    matched_quotes_books = len([b for b in shelf_books if b["has_quote_bank"]])
    print(f"Compiled {len(shelf_books)} books for Ex Libris.")
    print(f"Books successfully linked with Quote Bank: {matched_quotes_books} (over 1,500+ quotes).")
    print(f"Books with Google Drive hyperlinks: {len([b for b in shelf_books if b['drive_url']])}")

    # Ensure output directories exist
    BOOKSHELF_DIR.mkdir(exist_ok=True)
    DOCS_BOOKSHELF_HTML.parent.mkdir(exist_ok=True)

    # Save data
    BOOKSHELF_DATA.write_text(json.dumps(shelf_books, indent=2, ensure_ascii=False), encoding="utf-8")

    # Generate standalone web app HTML
    html = generate_app_html(shelf_books, clean_tbr_lines, matched_quotes_books)
    BOOKSHELF_HTML.write_text(html, encoding="utf-8")
    DOCS_BOOKSHELF_HTML.write_text(html, encoding="utf-8")
    ARTIFACT_PATH.write_text(html, encoding="utf-8")

    print(f"Generated standalone app: {BOOKSHELF_HTML}")
    print(f"Generated docs view: {DOCS_BOOKSHELF_HTML}")
    print(f"Generated artifact view: {ARTIFACT_PATH}")

def generate_app_html(shelf_books, tbr_lines, quote_count):
    shelf_json_str = json.dumps(shelf_books, ensure_ascii=False)
    total_books = len(shelf_books)
    covers_count = len([b for b in shelf_books if b.get('cover_url')])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Reading Corner — Curated Personal Library</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      /* Warm, Joyful Goodreads / Apple Books Inspired Palette */
      --canvas: #fbf9f5;
      --card-bg: #ffffff;
      --card-hover: #faf6f0;
      --border: #ede6dd;
      --border-subtle: #f3eee7;
      --text-heading: #1f242e;
      --text-body: #4b5563;
      --text-muted: #8c97a8;
      --terracotta: #d96b43;
      --terracotta-hover: #c45b34;
      --amber: #e89d38;
      --amber-bg: #fdf5ea;
      --forest: #2b7a78;
      --navy: #17252a;
    }}

    .dark-mode {{
      --canvas: #151311;
      --card-bg: #201c19;
      --card-hover: #292420;
      --border: #332d28;
      --border-subtle: #26211d;
      --text-heading: #f5f2eb;
      --text-body: #c7beaf;
      --text-muted: #8a8075;
      --terracotta: #e07a5f;
      --terracotta-hover: #f28a6f;
      --amber: #f4a261;
      --amber-bg: #2b221a;
      --forest: #3d9970;
      --navy: #0f172a;
    }}

    body {{
      background-color: var(--canvas);
      color: var(--text-body);
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      margin: 0;
      padding: 0;
      transition: background-color 0.2s ease, color 0.2s ease;
    }}

    .font-serif {{
      font-family: 'Playfair Display', Georgia, serif;
    }}

    /* Physical Book Cover Styling */
    .book-cover {{
      position: relative;
      aspect-ratio: 2 / 3;
      border-radius: 4px 8px 8px 4px;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(40, 25, 15, 0.12), 0 1px 3px rgba(40, 25, 15, 0.08);
      transition: transform 0.22s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.22s cubic-bezier(0.2, 0.8, 0.2, 1);
    }}
    .book-cover::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      bottom: 0;
      width: 12px;
      background: linear-gradient(90deg, rgba(255,255,255,0.22) 0%, rgba(255,255,255,0.02) 40%, rgba(0,0,0,0.22) 100%);
      z-index: 10;
      pointer-events: none;
    }}
    .book-card:hover .book-cover {{
      transform: translateY(-6px);
      box-shadow: 0 16px 28px rgba(40, 25, 15, 0.22), 0 4px 8px rgba(40, 25, 15, 0.12);
    }}

    /* Palette Themes for Dust Jackets */
    .jacket-fiction {{ background: linear-gradient(145deg, #2b3a67 0%, #172243 100%); border-top: 3px solid #6b82c6; }}
    .jacket-marketing {{ background: linear-gradient(145deg, #78293b 0%, #461421 100%); border-top: 3px solid #c95d73; }}
    .jacket-philosophy {{ background: linear-gradient(145deg, #214e42 0%, #112d26 100%); border-top: 3px solid #489b85; }}
    .jacket-cinema {{ background: linear-gradient(145deg, #6c4b26 0%, #3e2810 100%); border-top: 3px solid #d49a56; }}
    .jacket-screenplay {{ background: linear-gradient(145deg, #2c3038 0%, #181a1f 100%); border-top: 3px solid #7a8291; }}
    .jacket-comics {{ background: linear-gradient(145deg, #4d2d68 0%, #29153a 100%); border-top: 3px solid #9c6cc4; }}
    .jacket-guides {{ background: linear-gradient(145deg, #264a7f 0%, #122849 100%); border-top: 3px solid #5786ca; }}
    .jacket-hbr {{ background: linear-gradient(145deg, #8a2323 0%, #4e1010 100%); border-top: 3px solid #dc4949; }}
    .jacket-food {{ background: linear-gradient(145deg, #8b4513 0%, #4a2205 100%); border-top: 3px solid #d2793b; }}

    .line-clamp-2 {{ display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
    .line-clamp-3 {{ display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}
  </style>
</head>
<body class="min-h-screen">

  <!-- Header -->
  <header class="sticky top-0 z-40 bg-[var(--canvas)]/95 backdrop-blur-md border-b border-[var(--border)] px-4 md:px-8 py-3.5">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <!-- Bespoke "My Reading Corner" Emblem Logo -->
        <div class="w-11 h-11 rounded-2xl bg-gradient-to-br from-[#8A2814] via-[#C85A32] to-[#E08736] p-0.5 shadow-md flex items-center justify-center shrink-0 border border-[#F59E0B]/25">
          <svg class="w-7 h-7" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Floor / Corner Arc Lamp -->
            <path d="M7 31 H12" stroke="#FEF3C7" stroke-width="1.6" stroke-linecap="round"/>
            <path d="M9.5 31 V17 C9.5 10 14.5 7 21 8" stroke="#FEF3C7" stroke-width="1.6" stroke-linecap="round"/>
            <!-- Lamp Shade & Ambient Glow Cone -->
            <path d="M19.5 8 L24.5 11.5 L21.5 13.5 Z" fill="#FDE68A"/>
            <path d="M22 13 L15 28 L29 28 Z" fill="#FDE68A" fill-opacity="0.22"/>
            <!-- Open Book on Nook Table -->
            <path d="M15 28 C17.5 26.8 20 26.8 22 28 C24 26.8 26.5 26.8 29 28 V23 C26.5 21.8 24 21.8 22 23 C20 21.8 17.5 21.8 15 23 Z" fill="#FFF7ED" stroke="#B45309" stroke-width="0.8"/>
            <path d="M22 23 V28" stroke="#C85A32" stroke-width="0.8"/>
            <!-- Warm Corner Sparkle / Reading Star -->
            <path d="M29 7 L29.8 9.2 L32 10 L29.8 10.8 L29 13 L28.2 10.8 L26 10 L28.2 9.2 Z" fill="#FBBF24"/>
          </svg>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="font-serif font-bold text-lg md:text-xl text-[var(--text-heading)] tracking-tight leading-none">
              My Reading Corner
            </h1>
            <span class="text-[9px] font-mono uppercase tracking-wider text-[var(--terracotta)] bg-[var(--amber-bg)] border border-[var(--terracotta)]/30 px-1.5 py-0.5 rounded font-bold hidden sm:inline">
              CURATED NOOK
            </span>
          </div>
          <p class="text-[11px] font-medium text-[var(--text-muted)] mt-1 hidden sm:block">
            Personal Reading Corner • {total_books} in Drive • {covers_count} with Covers • {quote_count} with Quotes
          </p>
        </div>
      </div>

      <!-- Search Input -->
      <div class="flex-1 max-w-md mx-2">
        <div class="relative">
          <input 
            type="text" 
            id="searchInput" 
            oninput="handleSearch()"
            placeholder="Search books, authors, themes, quotes..." 
            class="w-full pl-9 pr-4 py-2 bg-[var(--card-bg)] border border-[var(--border)] rounded-full text-xs text-[var(--text-heading)] placeholder-[var(--text-muted)] focus:outline-none focus:ring-2 focus:ring-[var(--terracotta)]/30 focus:border-[var(--terracotta)] shadow-sm transition"
          />
          <span class="absolute left-3.5 top-2.5 text-[var(--text-muted)] text-xs">🔍</span>
        </div>
      </div>

      <!-- Controls -->
      <div class="flex items-center gap-2.5">
        <!-- 3-Mode View Switcher -->
        <div class="bg-[var(--card-bg)] p-1 rounded-xl border border-[var(--border)] flex items-center text-xs shadow-sm">
          <button 
            id="viewBtnBoard" 
            onclick="switchView('board')" 
            class="px-3 py-1 rounded-lg font-semibold transition bg-[var(--terracotta)] text-white shadow-sm flex items-center gap-1.5"
            title="Spacious 5-column book jackets with hover preview">
            <span>📌</span>
            <span class="hidden md:inline">Covers</span>
          </button>
          <button 
            id="viewBtnEditorial" 
            onclick="switchView('editorial')" 
            class="px-3 py-1 rounded-lg font-medium transition text-[var(--text-muted)] hover:text-[var(--text-heading)] flex items-center gap-1.5"
            title="3x2 magazine cards with visible synopsis and hook">
            <span>📰</span>
            <span class="hidden md:inline">Editorial (3x2)</span>
          </button>
          <button 
            id="viewBtnSplit" 
            onclick="switchView('split')" 
            class="px-3 py-1 rounded-lg font-medium transition text-[var(--text-muted)] hover:text-[var(--text-heading)] flex items-center gap-1.5"
            title="Two-pane bookshelf split reader">
            <span>📚</span>
            <span class="hidden md:inline">Bookshelf</span>
          </button>
        </div>

        <!-- Surprise Me -->
        <button 
          onclick="openSurpriseModal()" 
          class="px-3.5 py-2 bg-[var(--amber-bg)] text-[var(--terracotta)] border border-[var(--terracotta)]/30 hover:bg-[var(--terracotta)] hover:text-white rounded-xl text-xs font-bold transition flex items-center gap-1.5 shadow-sm">
          <span>✨</span>
          <span class="hidden sm:inline">Surprise Me</span>
        </button>

        <!-- Copy TBR -->
        <button 
          onclick="copyAllTbr()" 
          title="Copy clean list for TBR trackers"
          class="px-3 py-2 bg-[var(--card-bg)] hover:bg-[var(--card-hover)] border border-[var(--border)] text-[var(--text-heading)] rounded-xl text-xs font-semibold transition flex items-center gap-1.5 shadow-sm">
          <span>📋</span>
          <span class="hidden md:inline">Copy TBR ({len(tbr_lines)})</span>
        </button>

        <!-- Theme Toggle -->
        <button 
          onclick="toggleDarkMode()" 
          class="p-2 bg-[var(--card-bg)] border border-[var(--border)] text-[var(--text-muted)] hover:text-[var(--text-heading)] rounded-xl text-xs shadow-sm">
          <span id="themeIcon">🌙</span>
        </button>
      </div>
    </div>
  </header>

  <!-- Filter Ribbon -->
  <div class="border-b border-[var(--border-subtle)] bg-[var(--card-bg)]/60 px-4 md:px-8 py-2">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-4">
      <div class="flex items-center gap-1.5 overflow-x-auto py-1 no-scrollbar" id="categoryTabs">
        <!-- Populated dynamically -->
      </div>
      <div class="flex items-center gap-3 text-xs text-[var(--text-muted)] shrink-0">
        <label class="flex items-center gap-1.5 cursor-pointer font-medium hover:text-[var(--text-heading)] select-none">
          <input type="checkbox" id="filterQuotesOnly" onchange="renderCurrentView()" class="rounded border-[var(--border)] accent-[var(--terracotta)] w-3.5 h-3.5" />
          <span>Quotes Only ({quote_count})</span>
        </label>
        <span id="filteredCountBadge" class="font-mono text-[11px] px-2.5 py-0.5 bg-[var(--border-subtle)] rounded-full text-[var(--text-muted)]">
          {total_books}
        </span>
      </div>
    </div>
  </div>

  <!-- Content Container -->
  <main class="max-w-7xl mx-auto p-4 md:p-8">

    <!-- 1. Visual Jackets Board View (Default: 5 columns max on desktop, larger covers) -->
    <div id="boardView" class="block">
      <div id="boardGrid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6 md:gap-7">
        <!-- Populated dynamically -->
      </div>
    </div>

    <!-- 2. Editorial 3x2 View (Wide Cards with Cover + Synopsis + Damn Factor) -->
    <div id="editorialView" class="hidden">
      <div id="editorialGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Populated dynamically -->
      </div>
    </div>

    <!-- 3. Bookshelf Split View (Toggleable) -->
    <div id="splitView" class="hidden">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        <!-- Left Pane: Library Stream (5 columns) -->
        <div class="lg:col-span-5 bg-[var(--card-bg)] border border-[var(--border)] rounded-2xl p-4 max-h-[82vh] overflow-y-auto shadow-sm">
          <div class="text-xs font-bold text-[var(--text-muted)] uppercase tracking-wider mb-3 px-2">Library Stream</div>
          <div id="splitList" class="space-y-2">
            <!-- Populated dynamically -->
          </div>
        </div>

        <!-- Right Pane: Reading Dossier (7 columns) -->
        <div class="lg:col-span-7 sticky top-24">
          <div id="splitDossier" class="bg-[var(--card-bg)] border border-[var(--border)] rounded-2xl p-6 md:p-8 shadow-md">
            <!-- Populated dynamically with selected book -->
          </div>
        </div>
      </div>
    </div>

  </main>

  <!-- Slide-Out Drawer for Mobile or Board Click -->
  <div id="drawerOverlay" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex justify-end hidden">
    <div id="drawerPanel" class="w-full max-w-xl bg-[var(--card-bg)] border-l border-[var(--border)] h-full overflow-y-auto p-6 md:p-8 shadow-2xl transition-transform transform translate-x-full">
      <div class="flex items-center justify-between pb-4 border-b border-[var(--border)] mb-6">
        <span class="text-xs font-bold uppercase tracking-widest text-[var(--terracotta)]">Reading Dossier</span>
        <button onclick="closeDrawer()" class="text-[var(--text-muted)] hover:text-[var(--text-heading)] text-xl font-bold p-1">✕</button>
      </div>
      <div id="drawerContent">
        <!-- Populated dynamically -->
      </div>
    </div>
  </div>

  <!-- Surprise Me / Joy-of-Reading Modal -->
  <div id="surpriseModal" class="fixed inset-0 bg-black/65 backdrop-blur-md z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-[var(--card-bg)] border border-[var(--border)] rounded-2xl max-w-xl w-full p-6 md:p-8 shadow-2xl relative">
      <div class="flex items-center justify-between pb-4 border-b border-[var(--border)] mb-5">
        <div class="flex items-center gap-2.5">
          <span class="text-2xl">✨</span>
          <h2 class="font-serif font-bold text-xl text-[var(--text-heading)]">What to Read Next</h2>
        </div>
        <button onclick="closeSurpriseModal()" class="text-[var(--text-muted)] hover:text-[var(--text-heading)] text-lg font-bold">✕</button>
      </div>

      <p class="text-xs text-[var(--text-muted)] mb-5 leading-relaxed">
        Curated strictly from unputdownable fiction, craft essays by novelists, and engaging philosophy.
      </p>

      <div id="surpriseResult" class="mb-6">
        <!-- Populated dynamically -->
      </div>

      <div class="flex items-center justify-between pt-4 border-t border-[var(--border)]">
        <button onclick="spinSurprise()" class="px-5 py-2.5 bg-[var(--terracotta)] hover:bg-[var(--terracotta-hover)] text-white text-xs font-bold rounded-xl shadow-sm transition flex items-center gap-2">
          <span>🎲</span>
          <span>Spin Again</span>
        </button>
        <div class="flex items-center gap-2">
          <button id="surpriseDriveBtn" onclick="" class="px-4 py-2 bg-[var(--canvas)] border border-[var(--border)] hover:border-[var(--terracotta)] rounded-xl text-xs font-semibold text-[var(--text-heading)]">
            Open in Drive ↗
          </button>
          <button onclick="copySingleTbr(currentSurpriseBook.title, currentSurpriseBook.author)" class="px-4 py-2 bg-[var(--canvas)] border border-[var(--border)] rounded-xl text-xs font-medium text-[var(--text-muted)] hover:text-[var(--text-heading)]">
            Copy TBR
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Edit Details & Cover Modal -->
  <div id="editModal" class="fixed inset-0 bg-black/65 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-[var(--card-bg)] border border-[var(--border)] rounded-2xl max-w-lg w-full p-6 shadow-2xl">
      <div class="flex items-center justify-between pb-3 border-b border-[var(--border)] mb-4">
        <h3 class="font-serif font-bold text-lg text-[var(--text-heading)]">Edit Book Details & Cover</h3>
        <button onclick="closeEditModal()" class="text-[var(--text-muted)] hover:text-[var(--text-heading)] font-bold">✕</button>
      </div>

      <input type="hidden" id="editBookId" />

      <div class="space-y-4 text-xs">
        <div>
          <label class="block font-semibold text-[var(--text-muted)] uppercase mb-1">Title</label>
          <input type="text" id="editTitle" class="w-full px-3 py-2 bg-[var(--canvas)] border border-[var(--border)] rounded-lg text-[var(--text-heading)] focus:border-[var(--terracotta)] focus:outline-none" />
        </div>
        <div>
          <label class="block font-semibold text-[var(--text-muted)] uppercase mb-1">Author</label>
          <input type="text" id="editAuthor" class="w-full px-3 py-2 bg-[var(--canvas)] border border-[var(--border)] rounded-lg text-[var(--text-heading)] focus:border-[var(--terracotta)] focus:outline-none" />
        </div>
        <div>
          <label class="block font-semibold text-[var(--text-muted)] uppercase mb-1">Cover Image URL</label>
          <input type="text" id="editCoverUrl" placeholder="https://..." class="w-full px-3 py-2 bg-[var(--canvas)] border border-[var(--border)] rounded-lg text-[var(--text-heading)] focus:border-[var(--terracotta)] focus:outline-none" />
          <div class="flex items-center gap-3 mt-1.5 text-[11px] text-[var(--terracotta)]">
            <button type="button" onclick="searchGoodreads()" class="hover:underline">🔎 Search Goodreads Cover</button>
            <button type="button" onclick="searchGoogleImages()" class="hover:underline">🖼️ Search Google Images</button>
          </div>
        </div>
        <div>
          <label class="block font-semibold text-[var(--text-muted)] uppercase mb-1">Back-Cover Pitch</label>
          <textarea id="editPitch" rows="3" class="w-full px-3 py-2 bg-[var(--canvas)] border border-[var(--border)] rounded-lg text-[var(--text-heading)] focus:border-[var(--terracotta)] focus:outline-none"></textarea>
        </div>
        <div>
          <label class="block font-semibold text-[var(--text-muted)] uppercase mb-1">Why Read It</label>
          <textarea id="editWhyLove" rows="2" class="w-full px-3 py-2 bg-[var(--canvas)] border border-[var(--border)] rounded-lg text-[var(--text-heading)] focus:border-[var(--terracotta)] focus:outline-none"></textarea>
        </div>
      </div>

      <div class="flex items-center justify-end gap-3 mt-5 pt-3 border-t border-[var(--border)]">
        <button onclick="closeEditModal()" class="px-4 py-2 border border-[var(--border)] rounded-lg text-xs text-[var(--text-muted)]">Cancel</button>
        <button onclick="saveEdit()" class="px-5 py-2 bg-[var(--terracotta)] text-white text-xs font-bold rounded-lg shadow-sm">Save Changes</button>
      </div>
    </div>
  </div>

  <!-- Toast -->
  <div id="toast" class="fixed bottom-6 right-6 bg-[var(--text-heading)] text-[var(--canvas)] px-4 py-2.5 rounded-xl shadow-2xl text-xs font-bold transform translate-y-16 opacity-0 transition-all pointer-events-none z-50">
    Copied to clipboard!
  </div>

  <script>
    let SHELF_DATA = {shelf_json_str};
    let activeCategory = "All";
    let activeView = "board";
    let selectedBookId = SHELF_DATA[0] ? SHELF_DATA[0].id : null;
    let currentSurpriseBook = null;
    let isDark = false;

    // Load any user overrides from localStorage
    try {{
      const saved = localStorage.getItem("exlibris_shelf_edits");
      if (saved) {{
        const overrides = JSON.parse(saved);
        SHELF_DATA = SHELF_DATA.map(b => overrides[b.id] ? Object.assign(b, overrides[b.id]) : b);
      }}
    }} catch (e) {{}}

    const CATEGORIES = [
      "All",
      "Fiction & Non-Fiction",
      "Cinema & Film Craft",
      "Screenplays",
      "Philosophy, Essays & Misc",
      "Comics & Graphic Novels",
      "Graphic Guides",
      "Marketing & Strategy",
      "Harvard Business Review"
    ];

    function showToast(msg) {{
      const t = document.getElementById("toast");
      t.innerText = msg;
      t.classList.remove("translate-y-16", "opacity-0");
      setTimeout(() => t.classList.add("translate-y-16", "opacity-0"), 2400);
    }}

    function copyToClipboard(text, msg) {{
      navigator.clipboard.writeText(text).then(() => showToast(msg || "Copied to clipboard!"));
    }}

    function copySingleTbr(title, author) {{
      copyToClipboard(`${{title}} — ${{author}}`, `Copied: "${{title}} — ${{author}}"`);
    }}

    function copyAllTbr() {{
      const filtered = getFilteredBooks();
      const lines = filtered.map(b => `${{b.title}} — ${{b.author}}`);
      copyToClipboard(lines.join("\\n"), `Copied ${{lines.length}} books to clipboard!`);
    }}

    function toggleDarkMode() {{
      isDark = !isDark;
      document.body.classList.toggle("dark-mode", isDark);
      document.getElementById("themeIcon").innerText = isDark ? "☀️" : "🌙";
    }}

    function getJacketStyle(cat) {{
      if (cat.includes("Fiction")) return "jacket-fiction";
      if (cat.includes("Marketing")) return "jacket-marketing";
      if (cat.includes("Philosophy")) return "jacket-philosophy";
      if (cat.includes("Cinema")) return "jacket-cinema";
      if (cat.includes("Screenplay")) return "jacket-screenplay";
      if (cat.includes("Comics")) return "jacket-comics";
      if (cat.includes("Graphic Guide")) return "jacket-guides";
      if (cat.includes("Harvard")) return "jacket-hbr";
      if (cat.includes("Food")) return "jacket-food";
      return "jacket-fiction";
    }}

    function getFilteredBooks() {{
      const q = document.getElementById("searchInput").value.toLowerCase().trim();
      const quotesOnly = document.getElementById("filterQuotesOnly").checked;

      return SHELF_DATA.filter(b => {{
        if (activeCategory !== "All" && b.category !== activeCategory) return false;
        if (quotesOnly && !b.has_quote_bank) return false;
        if (q) {{
          const matchTitle = (b.title || "").toLowerCase().includes(q);
          const matchAuthor = (b.author || "").toLowerCase().includes(q);
          const matchPitch = (b.pitch || "").toLowerCase().includes(q);
          const matchQuotes = (b.quotes || []).some(item => (item.quote || "").toLowerCase().includes(q));
          if (!matchTitle && !matchAuthor && !matchPitch && !matchQuotes) return false;
        }}
        return true;
      }});
    }}

    function renderCategoryTabs() {{
      const container = document.getElementById("categoryTabs");
      container.innerHTML = CATEGORIES.map(cat => {{
        const isAct = cat === activeCategory;
        const count = cat === "All" ? SHELF_DATA.length : SHELF_DATA.filter(b => b.category === cat).length;
        if (count === 0) return "";
        return `
          <button 
            onclick="setCategory('${{cat}}')" 
            class="px-3.5 py-1 rounded-full text-xs font-semibold whitespace-nowrap transition ${{
              isAct 
                ? 'bg-[var(--terracotta)] text-white shadow-sm' 
                : 'text-[var(--text-muted)] hover:text-[var(--text-heading)] hover:bg-[var(--border-subtle)]'
            }}">
            ${{cat}} <span class="opacity-75 text-[10px] font-normal">(${{count}})</span>
          </button>
        `;
      }}).join("");
    }}

    function setCategory(cat) {{
      activeCategory = cat;
      renderCategoryTabs();
      renderCurrentView();
    }}

    function handleSearch() {{
      renderCurrentView();
    }}

    function switchView(view) {{
      activeView = view;
      const board = document.getElementById("boardView");
      const editorial = document.getElementById("editorialView");
      const split = document.getElementById("splitView");
      const btnBoard = document.getElementById("viewBtnBoard");
      const btnEditorial = document.getElementById("viewBtnEditorial");
      const btnSplit = document.getElementById("viewBtnSplit");

      [board, editorial, split].forEach(el => el.classList.add("hidden"));
      [btnBoard, btnEditorial, btnSplit].forEach(btn => {{
        btn.className = "px-3 py-1 rounded-lg font-medium transition text-[var(--text-muted)] hover:text-[var(--text-heading)] flex items-center gap-1.5";
      }});

      if (view === "board") {{
        board.classList.remove("hidden");
        btnBoard.className = "px-3 py-1 rounded-lg font-semibold transition bg-[var(--terracotta)] text-white shadow-sm flex items-center gap-1.5";
      }} else if (view === "editorial") {{
        editorial.classList.remove("hidden");
        btnEditorial.className = "px-3 py-1 rounded-lg font-semibold transition bg-[var(--terracotta)] text-white shadow-sm flex items-center gap-1.5";
      }} else {{
        split.classList.remove("hidden");
        btnSplit.className = "px-3 py-1 rounded-lg font-semibold transition bg-[var(--terracotta)] text-white shadow-sm flex items-center gap-1.5";
      }}
      renderCurrentView();
    }}

    function renderCurrentView() {{
      const filtered = getFilteredBooks();
      document.getElementById("filteredCountBadge").innerText = `${{filtered.length}} books`;

      if (activeView === "board") {{
        renderBoard(filtered);
      }} else if (activeView === "editorial") {{
        renderEditorial(filtered);
      }} else {{
        renderSplit(filtered);
      }}
    }}

    function extractFirstWhyReadHook(text) {{
      if (!text) return "A standout work celebrated for visionary craft and narrative resonance.";
      const clean = text.replace(/\\*\\*(.*?)\\*\\*:?\\s*/g, "").trim();
      const firstPara = clean.split("\\n\\n")[0].trim();
      const sentences = firstPara.match(/[^.!?]+[.!?]+/g);
      if (sentences && sentences.length > 0) {{
        return sentences.slice(0, 2).join(" ").trim();
      }}
      return firstPara.slice(0, 180) + "...";
    }}

    function toggleInsight(btn, targetId) {{
      const target = document.getElementById(targetId);
      if (!target) return;

      const isAlreadyOpen = !target.classList.contains("hidden");

      // Close ALL open insights in the document (single open constraint)
      document.querySelectorAll(".insight-content").forEach(el => {{
        el.classList.add("hidden");
      }});
      document.querySelectorAll(".insight-toggle-btn .toggle-arrow").forEach(arr => {{
        arr.style.transform = "rotate(0deg)";
      }});
      document.querySelectorAll(".insight-toggle-btn").forEach(b => {{
        b.classList.remove("text-[var(--terracotta-hover)]", "font-bold");
      }});

      // If it was closed, open this one
      if (!isAlreadyOpen) {{
        target.classList.remove("hidden");
        const arrow = btn.querySelector(".toggle-arrow");
        if (arrow) arrow.style.transform = "rotate(90deg)";
        btn.classList.add("text-[var(--terracotta-hover)]", "font-bold");
      }}
    }}

    function formatWhyRead(text) {{
      if (!text) return "";
      const clean = text.replace(/\\*\\*(.*?)\\*\\*:?\\s*/g, "").trim();
      return clean
        .split("\\n\\n")
        .map(para => {{
          const p = para.trim();
          if (!p) return "";
          return `<p class="leading-relaxed font-serif text-xs md:text-[13.5px] text-[var(--text-heading)] mb-2.5 last:mb-0">${{p}}</p>`;
        }})
        .join("");
    }}

    // Render Pinterest Board (5-Column on Desktop with Hover Preview)
    function renderBoard(books) {{
      const grid = document.getElementById("boardGrid");
      if (books.length === 0) {{
        grid.innerHTML = `<div class="col-span-full py-20 text-center text-sm text-[var(--text-muted)]">No matching books found.</div>`;
        return;
      }}

      grid.innerHTML = books.map(b => {{
        const jacketCls = getJacketStyle(b.category);
        const hasCover = !!b.cover_url;
        const hook = extractFirstWhyReadHook(b.why_love);

        return `
          <div class="book-card group cursor-pointer relative" onclick="openBookDetail('${{b.id}}')">
            <!-- Book Cover -->
            <div class="book-cover ${{jacketCls}} relative overflow-hidden rounded-[8px] shadow-md transition-all duration-200 group-hover:shadow-2xl group-hover:-translate-y-1.5">
              ${{hasCover ? `
                <img src="${{b.cover_url}}" alt="${{b.title}}" loading="lazy" class="w-full h-full object-cover z-0" onerror="this.onerror=null;this.style.display='none';this.parentElement.querySelector('.fallback-jacket').style.display='flex';" />
                <div class="absolute top-2 left-2 z-10 flex items-center gap-1.5">
                  <span class="text-[9px] font-mono uppercase tracking-wider text-white bg-black/60 backdrop-blur-xs px-1.5 py-0.5 rounded shadow-sm">
                    ${{b.format}}
                  </span>
                  ${{b.has_quote_bank ? `<span class="text-[9px] font-bold text-amber-950 bg-amber-300/95 backdrop-blur-xs px-1.5 py-0.5 rounded shadow-sm">★ Quotes</span>` : ''}}
                </div>
                <div class="fallback-jacket hidden flex-col justify-between h-full p-3.5 absolute inset-0 z-0">
                  <div class="flex items-center justify-between">
                    <span class="text-[9px] font-mono uppercase text-white/80 bg-black/40 px-1.5 py-0.5 rounded">${{b.format}}</span>
                    ${{b.has_quote_bank ? `<span class="text-[9px] font-bold text-amber-300">★ Quotes</span>` : ''}}
                  </div>
                  <div class="mt-auto pt-2">
                    <h3 class="font-serif font-bold text-xs text-white leading-tight drop-shadow-md line-clamp-3">${{b.title}}</h3>
                    <p class="text-[10px] text-white/85 font-medium mt-0.5 line-clamp-1">${{b.author}}</p>
                  </div>
                </div>
              ` : `
                <div class="flex flex-col justify-between h-full p-3.5 relative z-10">
                  <div class="flex items-center justify-between">
                    <span class="text-[9px] font-mono uppercase text-white/80 bg-black/40 px-1.5 py-0.5 rounded">${{b.format}}</span>
                    ${{b.has_quote_bank ? `<span class="text-[9px] font-bold text-amber-300">★ Quotes</span>` : ''}}
                  </div>
                  <div class="mt-auto pt-2">
                    <h3 class="font-serif font-bold text-xs sm:text-sm text-white leading-tight drop-shadow-md line-clamp-3">${{b.title}}</h3>
                    <p class="text-[10px] text-white/85 font-medium mt-0.5 line-clamp-1">${{b.author}}</p>
                  </div>
                </div>
              `}}

              <!-- Hover Peek Card Overlay (Context on Hover) -->
              <div class="hover-preview opacity-0 pointer-events-none group-hover:opacity-100 group-hover:pointer-events-auto transition-opacity duration-200 absolute inset-0 bg-[#151311]/95 text-white p-4 flex flex-col justify-between rounded-[8px] z-20 backdrop-blur-xs shadow-inner">
                <div>
                  <div class="flex items-center justify-between mb-1.5">
                    <span class="text-[9px] font-mono uppercase tracking-wider text-amber-300 font-bold">${{b.format}}</span>
                    ${{b.has_quote_bank ? `<span class="text-[9px] font-bold text-amber-300">★ ${{b.quotes.length}} Quotes</span>` : ''}}
                  </div>
                  <h4 class="font-serif font-bold text-xs sm:text-sm text-white leading-snug line-clamp-2">${{b.title}}</h4>
                  <p class="text-[10px] text-white/70 mt-0.5 line-clamp-1">by ${{b.author}}</p>

                  <div class="mt-3 pt-2 border-t border-white/15">
                    <span class="text-[9px] font-bold uppercase tracking-wider text-amber-300 block mb-1">✦ Curator's Hook:</span>
                    <p class="text-[10px] text-white/90 leading-relaxed line-clamp-4">${{hook}}</p>
                  </div>
                </div>

                <div class="pt-2 border-t border-white/15 flex items-center justify-between text-[10px]">
                  <span class="text-amber-300 font-semibold">Open Dossier →</span>
                  ${{b.drive_url ? `<span class="text-white/60">Drive ↗</span>` : ''}}
                </div>
              </div>
            </div>

            <!-- Meta Beneath -->
            <div class="pt-2.5 px-0.5">
              <h4 class="font-serif font-bold text-xs sm:text-sm text-[var(--text-heading)] group-hover:text-[var(--terracotta)] transition leading-snug line-clamp-2">
                ${{b.title}}
              </h4>
              <p class="text-[11px] text-[var(--text-muted)] font-medium mt-0.5 line-clamp-1">
                ${{b.author}}
              </p>
              <div class="flex items-center gap-1.5 mt-1.5 text-[10px]">
                <span class="text-[var(--terracotta)] font-semibold truncate">${{b.category}}</span>
                ${{b.has_quote_bank ? `<span class="text-[var(--text-muted)]">• ${{b.quotes.length}} Quotes</span>` : ''}}
              </div>
            </div>
          </div>
        `;
      }}).join("");
    }}

    // Render Editorial 3x2 View (Wide Cards with Cover + Synopsis + Damn Factor)
    function renderEditorial(books) {{
      const grid = document.getElementById("editorialGrid");
      if (books.length === 0) {{
        grid.innerHTML = `<div class="col-span-full py-20 text-center text-sm text-[var(--text-muted)]">No matching books found.</div>`;
        return;
      }}

      grid.innerHTML = books.map(b => {{
        const jacketCls = getJacketStyle(b.category);
        const hasCover = !!b.cover_url;
        const hook = extractFirstWhyReadHook(b.why_love);

        return `
          <div class="editorial-card bg-[var(--card-bg)] border border-[var(--border)] hover:border-[var(--terracotta)]/40 rounded-2xl p-4 flex gap-4 hover:shadow-xl transition-all duration-200 cursor-pointer group" onclick="openBookDetail('${{b.id}}')">
            <!-- Cover (Left) -->
            <div class="w-24 sm:w-28 shrink-0 book-cover ${{jacketCls}} relative rounded-[6px] overflow-hidden shadow-sm">
              ${{hasCover ? `
                <img src="${{b.cover_url}}" alt="${{b.title}}" loading="lazy" class="w-full h-full object-cover" onerror="this.onerror=null;this.style.display='none';this.parentElement.querySelector('.fallback-ed').style.display='flex';" />
                <div class="fallback-ed hidden flex-col justify-between h-full p-2.5 absolute inset-0">
                  <span class="text-[8px] font-mono uppercase text-white/80">${{b.format}}</span>
                  <p class="font-serif text-[11px] font-bold text-white leading-tight line-clamp-3">${{b.title}}</p>
                </div>
              ` : `
                <div class="flex flex-col justify-between h-full p-2.5">
                  <span class="text-[8px] font-mono uppercase text-white/80">${{b.format}}</span>
                  <p class="font-serif text-[11px] font-bold text-white leading-tight line-clamp-3">${{b.title}}</p>
                </div>
              `}}
            </div>

            <!-- Content (Right) -->
            <div class="flex-1 min-w-0 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between gap-1.5">
                  <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--terracotta)] truncate">${{b.category}}</span>
                  ${{b.has_quote_bank ? `<span class="text-[9px] font-bold text-amber-950 bg-amber-300/90 px-1.5 py-0.5 rounded shrink-0">★ Quotes</span>` : ''}}
                </div>
                <h3 class="font-serif font-bold text-sm md:text-base text-[var(--text-heading)] group-hover:text-[var(--terracotta)] transition line-clamp-1 mt-0.5 leading-snug">
                  ${{b.title}}
                </h3>
                <p class="text-xs text-[var(--text-muted)] font-medium line-clamp-1">by ${{b.author}}</p>

                <!-- Back of the Book Synopsis Snippet -->
                <p class="font-serif text-xs text-[var(--text-heading)] line-clamp-3 mt-2 leading-relaxed opacity-90">
                  ${{b.pitch}}
                </p>
              </div>

              <!-- Hook / Damn Factor -->
              <div class="mt-3 pt-2.5 border-t border-[var(--border-subtle)] flex items-center justify-between text-[11px]">
                <div class="text-[var(--terracotta)] font-medium truncate flex items-center gap-1.5 min-w-0">
                  <span class="text-xs">✦</span>
                  <span class="truncate text-[11px] font-serif italic">${{hook}}</span>
                </div>
                <span class="text-[var(--text-muted)] group-hover:text-[var(--terracotta)] text-xs font-bold shrink-0 ml-2">Read →</span>
              </div>
            </div>
          </div>
        `;
      }}).join("");
    }}

    // Render Bookshelf Split View
    function renderSplit(books) {{
      const list = document.getElementById("splitList");
      if (books.length === 0) {{
        list.innerHTML = `<div class="p-6 text-center text-xs text-[var(--text-muted)]">No books match.</div>`;
        document.getElementById("splitDossier").innerHTML = `<div class="p-8 text-center text-xs text-[var(--text-muted)]">Select a book from the list.</div>`;
        return;
      }}

      if (!books.some(b => b.id === selectedBookId)) {{
        selectedBookId = books[0].id;
      }}

      list.innerHTML = books.map(b => {{
        const isSel = b.id === selectedBookId;
        const jacketCls = getJacketStyle(b.category);

        return `
          <div 
            onclick="selectBookForSplit('${{b.id}}')" 
            class="flex items-center gap-3 p-2.5 rounded-xl cursor-pointer transition ${{
              isSel 
                ? 'bg-[var(--card-hover)] border border-[var(--terracotta)]/40 shadow-sm' 
                : 'hover:bg-[var(--card-hover)] border border-transparent'
            }}">
            <div class="w-10 h-14 shrink-0 book-cover ${{jacketCls}} relative overflow-hidden rounded">
              ${{b.cover_url ? `<img src="${{b.cover_url}}" class="w-full h-full object-cover" onerror="this.style.display='none'" />` : ''}}
            </div>
            <div class="flex-1 min-w-0">
              <h4 class="font-serif font-bold text-xs text-[var(--text-heading)] truncate">${{b.title}}</h4>
              <p class="text-[11px] text-[var(--text-muted)] truncate">${{b.author}}</p>
              <div class="flex items-center gap-2 mt-1 text-[10px]">
                <span class="text-[var(--terracotta)] font-semibold">${{b.category}}</span>
                ${{b.has_quote_bank ? `<span class="text-[var(--text-muted)]">• ${{b.quotes.length}} Quotes</span>` : ''}}
              </div>
            </div>
          </div>
        `;
      }}).join("");

      renderDossier(books.find(b => b.id === selectedBookId));
    }}

    function selectBookForSplit(bookId) {{
      selectedBookId = bookId;
      const filtered = getFilteredBooks();
      renderSplit(filtered);
    }}

    function renderDossier(b) {{
      const container = document.getElementById("splitDossier");
      if (!b) return;

      const jacketCls = getJacketStyle(b.category);
      const quotes = b.quotes || [];

      container.innerHTML = `
        <div class="flex flex-col md:flex-row gap-6 items-start mb-6 pb-6 border-b border-[var(--border)]">
          <!-- Hero Cover -->
          <div class="w-36 md:w-48 shrink-0 book-cover ${{jacketCls}} shadow-xl relative overflow-hidden rounded-[8px]">
            ${{b.cover_url ? `
              <img src="${{b.cover_url}}" alt="${{b.title}}" class="w-full h-full object-cover" onerror="this.onerror=null;this.style.display='none';this.parentElement.querySelector('.fallback-hero').style.display='flex';" />
              <div class="fallback-hero hidden flex-col justify-between h-full p-4 absolute inset-0 z-10">
                <span class="text-[10px] font-mono uppercase text-white/80">${{b.format}}</span>
                <div class="mt-auto">
                  <h3 class="font-serif font-bold text-sm text-white leading-tight">${{b.title}}</h3>
                  <p class="text-xs text-white/80 mt-1">${{b.author}}</p>
                </div>
              </div>
            ` : `
              <div class="flex flex-col justify-between h-full p-4 relative z-10">
                <span class="text-[10px] font-mono uppercase text-white/80">${{b.format}}</span>
                <div class="mt-auto">
                  <h3 class="font-serif font-bold text-sm text-white leading-tight">${{b.title}}</h3>
                  <p class="text-xs text-white/80 mt-1">${{b.author}}</p>
                </div>
              </div>
            `}}
          </div>

          <!-- Title & Actions -->
          <div class="flex-1 min-w-0">
            <span class="text-xs font-bold uppercase tracking-wider text-[var(--terracotta)]">${{b.category}}</span>
            <h2 class="font-serif font-bold text-2xl md:text-3xl text-[var(--text-heading)] mt-1 tracking-tight leading-tight">
              ${{b.title}}
            </h2>
            <p class="text-sm font-medium text-[var(--text-muted)] mt-1">by ${{b.author}}</p>

            <div class="flex flex-wrap items-center gap-2 mt-4">
              ${{b.drive_url ? `
                <a href="${{b.drive_url}}" target="_blank" rel="noopener noreferrer" class="px-4 py-2 bg-[var(--terracotta)] hover:bg-[var(--terracotta-hover)] text-white text-xs font-bold rounded-xl shadow-sm transition flex items-center gap-1.5">
                  <span>📖</span>
                  <span>Open in Drive ↗</span>
                </a>
              ` : ''}}
              <button onclick="copySingleTbr('${{b.title.replace(/'/g, "\\\\\\'")}}', '${{b.author.replace(/'/g, "\\\\\\'")}}')" class="px-3.5 py-2 bg-[var(--canvas)] border border-[var(--border)] hover:border-[var(--terracotta)] text-xs font-semibold text-[var(--text-heading)] rounded-xl transition flex items-center gap-1.5">
                <span>📋</span>
                <span>Copy TBR</span>
              </button>
              <button onclick="openEditModal('${{b.id}}')" class="px-3.5 py-2 bg-[var(--canvas)] border border-[var(--border)] text-xs font-semibold text-[var(--text-muted)] hover:text-[var(--text-heading)] rounded-xl transition flex items-center gap-1.5">
                <span>✏️</span>
                <span>Edit / Cover</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Back of the Book / Synopsis -->
        <div class="mb-6">
          <div class="flex items-center gap-2 mb-2">
            <span class="text-xs font-bold uppercase tracking-wider text-[var(--text-muted)]">Back of the Book • Synopsis</span>
          </div>
          <div class="p-4 md:p-5 bg-[var(--canvas)] border border-[var(--border)] rounded-2xl">
            <p class="font-serif text-sm md:text-[15px] text-[var(--text-heading)] leading-relaxed whitespace-pre-line">
              ${{b.pitch}}
            </p>
          </div>
        </div>

        <!-- Curator's Note • Why It Belongs on This Shelf -->
        <div class="mb-6 p-5 md:p-6 bg-gradient-to-br from-[var(--amber-bg)] via-[var(--canvas)] to-[var(--card-bg)] border border-[var(--terracotta)]/25 rounded-2xl shadow-sm">
          <div class="flex items-center gap-2 mb-3">
            <span class="text-sm font-bold text-[var(--terracotta)]">✦</span>
            <h4 class="text-xs font-bold text-[var(--terracotta)] uppercase tracking-wider">Curator's Note • Why It's on This Shelf</h4>
          </div>
          <div class="editorial-prose leading-relaxed space-y-2.5">
            ${{formatWhyRead(b.why_love)}}
          </div>
        </div>

        <!-- Excerpt Quotes & Notes from Quote Bank -->
        ${{quotes.length > 0 ? `
          <div class="mt-8">
            <div class="flex items-center justify-between mb-3">
              <h4 class="text-xs font-bold uppercase tracking-wider text-[var(--text-muted)] flex items-center gap-1.5">
                <span>★ Key Passages (${{quotes.length}})</span>
              </h4>
              <span class="text-[10px] text-[var(--text-muted)] font-medium">Tap to expand scene insight (one at a time)</span>
            </div>
            <div class="space-y-3.5">
              ${{quotes.map((q, idx) => `
                <div class="p-4 bg-[var(--canvas)] border border-[var(--border)] rounded-2xl transition-all">
                  <!-- The Quote (Always Visible) -->
                  <div class="font-serif italic text-sm md:text-[15px] text-[var(--text-heading)] leading-relaxed pl-3.5 border-l-3 border-[var(--terracotta)]">
                    “${{q.quote}}”
                  </div>
                  
                  ${{q.explanation ? `
                    <!-- Accordion Trigger Button -->
                    <button 
                      type="button"
                      onclick="toggleInsight(this, 'dossier-insight-${{idx}}')" 
                      class="insight-toggle-btn mt-3 flex items-center gap-1.5 text-[11px] font-semibold text-[var(--terracotta)] hover:text-[var(--terracotta-hover)] transition cursor-pointer select-none">
                      <span class="toggle-arrow text-[10px] inline-block transition-transform duration-200">▸</span>
                      <span>Companion Insight & Scene Context</span>
                    </button>

                    <!-- Collapsible Insight (Collapsed by default) -->
                    <div id="dossier-insight-${{idx}}" class="insight-content hidden mt-3 pt-3 border-t border-[var(--border-subtle)] text-xs text-[var(--text-body)] leading-relaxed whitespace-pre-line bg-[var(--card-bg)]/60 p-3 rounded-xl">
                      <span class="font-bold text-[var(--text-heading)] block mb-1">Scene Predicament & Psychological Mirror:</span>
                      ${{q.explanation}}
                    </div>
                  ` : ''}}
                </div>
              `).join("")}}
            </div>
          </div>
        ` : ''}}
      `;
    }}

    function openBookDetail(bookId) {{
      const b = SHELF_DATA.find(item => item.id === bookId);
      if (!b) return;

      if (window.innerWidth >= 1024) {{
        switchView("split");
        selectBookForSplit(bookId);
      }} else {{
        openDrawer(b);
      }}
    }}

    function openDrawer(b) {{
      const overlay = document.getElementById("drawerOverlay");
      const panel = document.getElementById("drawerPanel");
      const content = document.getElementById("drawerContent");
      const jacketCls = getJacketStyle(b.category);
      const quotes = b.quotes || [];

      content.innerHTML = `
        <div class="flex gap-4 items-start mb-6">
          <div class="w-28 shrink-0 book-cover ${{jacketCls}} shadow-md relative overflow-hidden rounded-[6px]">
            ${{b.cover_url ? `<img src="${{b.cover_url}}" class="w-full h-full object-cover" onerror="this.style.display='none'" />` : `
              <div class="p-3 h-full flex flex-col justify-between">
                <span class="text-[9px] font-mono uppercase text-white/80">${{b.format}}</span>
                <p class="font-serif text-xs font-bold text-white leading-tight">${{b.title}}</p>
              </div>
            `}}
          </div>
          <div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--terracotta)]">${{b.category}}</span>
            <h3 class="font-serif font-bold text-lg text-[var(--text-heading)] mt-0.5 leading-snug">${{b.title}}</h3>
            <p class="text-xs text-[var(--text-muted)] font-medium">by ${{b.author}}</p>
            <div class="flex flex-wrap items-center gap-2 mt-3">
              ${{b.drive_url ? `
                <a href="${{b.drive_url}}" target="_blank" rel="noopener noreferrer" class="px-3 py-1.5 bg-[var(--terracotta)] text-white text-xs font-bold rounded-lg shadow-sm">
                  Open in Drive ↗
                </a>
              ` : ''}}
              <button onclick="copySingleTbr('${{b.title.replace(/'/g, "\\\\\\'")}}', '${{b.author.replace(/'/g, "\\\\\\'")}}')" class="px-3 py-1.5 bg-[var(--canvas)] border border-[var(--border)] text-xs font-semibold rounded-lg">Copy TBR</button>
            </div>
          </div>
        </div>

        <div class="mb-5">
          <h4 class="text-xs font-bold uppercase tracking-wider text-[var(--text-muted)] mb-1.5">Back of the Book • Synopsis</h4>
          <div class="p-3.5 bg-[var(--canvas)] border border-[var(--border)] rounded-xl">
            <p class="font-serif text-sm text-[var(--text-heading)] leading-relaxed whitespace-pre-line">${{b.pitch}}</p>
          </div>
        </div>

        <div class="mb-5 p-4 bg-gradient-to-br from-[var(--amber-bg)] to-[var(--card-bg)] rounded-xl border border-[var(--terracotta)]/25 space-y-2">
          <div class="flex items-center gap-1.5 mb-1.5">
            <span class="text-xs text-[var(--terracotta)]">✦</span>
            <h4 class="text-xs font-bold text-[var(--terracotta)] uppercase tracking-wider">Curator's Note</h4>
          </div>
          <div class="editorial-prose text-xs leading-relaxed space-y-2">
            ${{formatWhyRead(b.why_love)}}
          </div>
        </div>

        ${{quotes.length > 0 ? `
          <div class="mt-6">
            <div class="flex items-center justify-between mb-2.5">
              <h4 class="text-xs font-bold uppercase tracking-wider text-[var(--text-muted)]">Key Passages (${{quotes.length}})</h4>
              <span class="text-[10px] text-[var(--text-muted)]">Tap to expand insight</span>
            </div>
            <div class="space-y-3">
              ${{quotes.map((q, idx) => `
                <div class="p-3 bg-[var(--canvas)] border border-[var(--border)] rounded-xl">
                  <div class="font-serif italic text-xs text-[var(--text-heading)] leading-relaxed pl-2.5 border-l-2 border-[var(--terracotta)]">“${{q.quote}}”</div>
                  ${{q.explanation ? `
                    <button 
                      type="button"
                      onclick="toggleInsight(this, 'drawer-insight-${{idx}}')" 
                      class="insight-toggle-btn mt-2.5 flex items-center gap-1.5 text-[10px] font-semibold text-[var(--terracotta)] hover:text-[var(--terracotta-hover)] transition cursor-pointer select-none">
                      <span class="toggle-arrow inline-block transition-transform duration-200">▸</span>
                      <span>Companion Insight & Scene Context</span>
                    </button>
                    <div id="drawer-insight-${{idx}}" class="insight-content hidden mt-2.5 pt-2.5 border-t border-[var(--border-subtle)] text-[11px] text-[var(--text-body)] leading-relaxed whitespace-pre-line bg-[var(--card-bg)]/60 p-2.5 rounded-lg">
                      <span class="font-bold text-[var(--text-heading)] block mb-0.5">Scene Insight:</span>
                      ${{q.explanation}}
                    </div>
                  ` : ''}}
                </div>
              `).join("")}}
            </div>
          </div>
        ` : ''}}
      `;

      overlay.classList.remove("hidden");
      setTimeout(() => panel.classList.remove("translate-x-full"), 10);
    }}

    function closeDrawer() {{
      const overlay = document.getElementById("drawerOverlay");
      const panel = document.getElementById("drawerPanel");
      panel.classList.add("translate-x-full");
      setTimeout(() => overlay.classList.add("hidden"), 240);
    }}

    // Surprise Me Logic
    function openSurpriseModal() {{
      spinSurprise();
      document.getElementById("surpriseModal").classList.remove("hidden");
    }}

    function closeSurpriseModal() {{
      document.getElementById("surpriseModal").classList.add("hidden");
    }}

    function spinSurprise() {{
      const pool = SHELF_DATA.filter(b => b.is_fun_pick);
      const chosen = pool[Math.floor(Math.random() * pool.length)];
      currentSurpriseBook = chosen;

      const res = document.getElementById("surpriseResult");
      const jacketCls = getJacketStyle(chosen.category);

      res.innerHTML = `
        <div class="flex flex-col sm:flex-row gap-5 items-start p-4 md:p-5 bg-[var(--canvas)] border border-[var(--border)] rounded-2xl max-h-[60vh] overflow-y-auto">
          <div class="w-28 md:w-32 shrink-0 book-cover ${{jacketCls}} shadow-md relative overflow-hidden rounded-[6px]">
            ${{chosen.cover_url ? `<img src="${{chosen.cover_url}}" class="w-full h-full object-cover" onerror="this.style.display='none'" />` : `
              <div class="p-3 h-full flex flex-col justify-between">
                <span class="text-[9px] font-mono uppercase text-white/80">${{chosen.format}}</span>
                <p class="font-serif text-xs font-bold text-white leading-tight">${{chosen.title}}</p>
              </div>
            `}}
          </div>
          <div class="flex-1 min-w-0">
            <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--terracotta)]">${{chosen.category}}</span>
            <h3 class="font-serif font-bold text-lg md:text-xl text-[var(--text-heading)] mt-0.5 leading-snug">${{chosen.title}}</h3>
            <p class="text-xs text-[var(--text-muted)] font-medium">by ${{chosen.author}}</p>
            <div class="mt-3 p-3 bg-[var(--card-bg)] border border-[var(--border-subtle)] rounded-xl">
              <span class="block text-[10px] font-bold uppercase tracking-wider text-[var(--text-muted)] mb-1">Back of the Book:</span>
              <p class="text-xs text-[var(--text-heading)] font-serif leading-relaxed">${{chosen.pitch}}</p>
            </div>
            <div class="mt-3 p-3.5 bg-gradient-to-br from-[var(--amber-bg)] to-[var(--card-bg)] border border-[var(--terracotta)]/25 rounded-xl space-y-1.5">
              <span class="block text-[10px] font-bold uppercase tracking-wider text-[var(--terracotta)]">✦ Curator's Note:</span>
              <div class="editorial-prose text-xs leading-relaxed space-y-2">
                ${{formatWhyRead(chosen.why_love)}}
              </div>
            </div>
          </div>
        </div>
      `;

      const driveBtn = document.getElementById("surpriseDriveBtn");
      if (chosen.drive_url) {{
        driveBtn.style.display = "inline-block";
        driveBtn.onclick = () => window.open(chosen.drive_url, '_blank');
      }} else {{
        driveBtn.style.display = "none";
      }}
    }}

    // Edit & Custom Cover
    function openEditModal(bookId) {{
      const b = SHELF_DATA.find(item => item.id === bookId);
      if (!b) return;

      document.getElementById("editBookId").value = b.id;
      document.getElementById("editTitle").value = b.title;
      document.getElementById("editAuthor").value = b.author;
      document.getElementById("editCoverUrl").value = b.cover_url || "";
      document.getElementById("editPitch").value = b.pitch || "";
      document.getElementById("editWhyLove").value = b.why_love || "";

      document.getElementById("editModal").classList.remove("hidden");
    }}

    function closeEditModal() {{
      document.getElementById("editModal").classList.add("hidden");
    }}

    function saveEdit() {{
      const bookId = document.getElementById("editBookId").value;
      const b = SHELF_DATA.find(item => item.id === bookId);
      if (!b) return;

      b.title = document.getElementById("editTitle").value.trim();
      b.author = document.getElementById("editAuthor").value.trim();
      b.cover_url = document.getElementById("editCoverUrl").value.trim();
      b.pitch = document.getElementById("editPitch").value.trim();
      b.why_love = document.getElementById("editWhyLove").value.trim();

      // Persist to localStorage
      let saved = {{}};
      try {{ saved = JSON.parse(localStorage.getItem("exlibris_shelf_edits") || "{{}}"); }} catch (e) {{}}
      saved[b.id] = {{
        title: b.title,
        author: b.author,
        cover_url: b.cover_url,
        pitch: b.pitch,
        why_love: b.why_love
      }};
      localStorage.setItem("exlibris_shelf_edits", JSON.stringify(saved));

      closeEditModal();
      renderCurrentView();
      showToast(`Updated "${{b.title}}" and saved changes!`);
    }}

    function searchGoodreads() {{
      const t = document.getElementById("editTitle").value.trim();
      const a = document.getElementById("editAuthor").value.trim();
      window.open(`https://www.goodreads.com/search?q=${{encodeURIComponent(t + ' ' + a)}}`, '_blank');
    }}

    function searchGoogleImages() {{
      const t = document.getElementById("editTitle").value.trim();
      const a = document.getElementById("editAuthor").value.trim();
      window.open(`https://www.google.com/search?tbm=isch&q=${{encodeURIComponent(t + ' ' + a + ' book cover')}}`, '_blank');
    }}

    // Initial render
    renderCategoryTabs();
    renderCurrentView();
  </script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
