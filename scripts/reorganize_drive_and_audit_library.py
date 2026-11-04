# scripts/reorganize_drive_and_audit_library.py — Strict title/author audit, bullshit filter, and Google Drive organizer
# Usage: python3 scripts/reorganize_drive_and_audit_library.py
# Requires: content/gdrive_books_catalog.json, content/quote-bank.json, rclone
#
# Gotchas:
# - Loose substring matching in quote bank was replacing titles (e.g. "Foundations of Screenwriting" -> "Foundation" by Asimov).
#   Strict normalized token comparison prevents title cross-contamination.
# - Moving files on Google Drive via rclone should use 'rclone moveto' with exact remote paths.
# - Whitepapers, cold email templates, and hustle bros (Hormozi, Belfort, Suby) must be purged from shelf/TBR.

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "content" / "gdrive_books_catalog.json"
QUOTE_BANK_PATH = ROOT / "content" / "quote-bank.json"

TBR_OUTPUT_PATH = ROOT / "content" / "tbr_clean_list.txt"
SHELF_JSON_PATH = ROOT / "content" / "books_curated_shelf.json"
SHELF_HTML_PROTO = ROOT / "prototype" / "shelf.html"
SHELF_HTML_DOCS = ROOT / "docs" / "shelf.html"
ARTIFACT_PATH = Path("/Users/apple/.gemini/antigravity/brain/81ccc3e6-122f-446d-b723-e563a56f7ea9/dynamic_bookshelf.html")
MOVE_SCRIPT_PATH = ROOT / "scripts" / "move_drive_files.sh"

# Exact keywords and filenames for Archive of bullshit
BULLSHIT_PATTERNS = [
    "100m offers", "way of the wolf", "sell like crazy", "cold email", "cold-email", 
    "linkedin", "viral linkedin", "posture mobility", "shoulder mobility",
    "product marketing glossary", "mr beast", "messaging strategy", "dawn creative",
    "mailmodo", "email subject line", "dave garehardt copywriting.pptx",
    "liz ellits", "search intent framework", "the 5 p approach", "copyblogger",
    "what the fortune 500 read", "worldclasspricing", "the abm cookbook",
    "secret sauce the ultimate growth hacking", "the 60 second sale", "scorecard marketing",
    "damianthefatass", "product strategy playbook by productplan"
]

# HBR files
HBR_PATTERNS = [
    "hbr on persuasive presentations", "hbr on communication", 
    "harvard innovation labs_ product-market fit", "hbr on strategic marketing"
]

EXACT_KNOWN_TITLES = {
    "heartburn_-_nora_ephron.epub": ("Heartburn", "Nora Ephron", "Fiction & Non-Fiction", 
        "A wickedly funny, autobiographical roman à clef about seven-months-pregnant food writer Rachel Samstat discovering her husband is in love with another woman.", 
        "Ephron's masterpiece of turning devastating domestic betrayal into razor-sharp, comedic survival prose."),
    "screenplay the foundations of screenwriting.epub": ("Screenplay: The Foundations of Screenwriting", "Syd Field", "Cinema & Film Craft",
        "The foundational Hollywood text codifying the universal three-act screenplay structure, plot points, and sequence pacing.",
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
        "Brilliant kinetic action married to biting socio-political class warfare."),
    "axiom’s end - lindsay ellis.epub": ("Axiom's End", "Lindsay Ellis", "Fiction & Non-Fiction",
        "In 2007 alternate history, the daughter of a fugitive leaker becomes the sole communication bridge to an enigmatic first-contact extraterrestrial organism.",
        "Cerebral, character-driven first contact exploring linguistics, xenobiology, and state secrecy."),
    "byung-chul han - absence on the culture and philosophy of the far east.pdf": ("Absence: On the Culture and Philosophy of the Far East", "Byung-Chul Han", "Philosophy, Essays & Misc",
        "Cultural philosopher Byung-Chul Han explores Eastern aesthetics of void, de-creation, and non-essence against Western fixation on substance and permanence.",
        "Short, luminous meditation unlocking the philosophical foundations of East Asian thought."),
    "qntm-there-is-no-antimemetics-di.epub": ("There Is No Antimemetics Division", "qntm (Sam Hughes)", "Fiction & Non-Fiction",
        "How do you contain an anomaly that erases all memory of its existence the second you look away? A cerebral psychological sci-fi thriller set in the SCP Foundation.",
        "One of the most terrifyingly original high-concept science fiction novels of the modern era."),
    "did-somebody-say-totalitarianism-[slavoj-zizek].epub": ("Did Somebody Say Totalitarianism? Five Interventions in the (Mis)Use of a Notion", "Slavoj Žižek", "Philosophy, Essays & Misc",
        "Žižek deconstructs how liberal political thought uses 'totalitarianism' as an intellectual bludgeon to forestall genuine economic critique.",
        "Provocative, energetic cultural philosophy challenging democratic complacency.")
}

def normalize_text(s: str) -> str:
    s = s.lower().replace("_", " ").replace("-", " ")
    return re.sub(r"[^a-z0-9 ]", "", s).strip()

def is_bullshit(filename: str) -> bool:
    fn = filename.lower()
    return any(p in fn for p in BULLSHIT_PATTERNS)

def is_hbr(filename: str) -> bool:
    fn = filename.lower()
    return any(p in fn for p in HBR_PATTERNS)

def main():
    print("Reading catalogs...")
    with open(CATALOG_PATH) as f:
        raw_books = json.load(f)
        
    qb_data = []
    if QUOTE_BANK_PATH.exists():
        with open(QUOTE_BANK_PATH) as f:
            qb_data = json.load(f)

    # Index quote bank strictly by (norm_work, norm_author)
    qb_strict = {}
    for q in qb_data:
        work = q.get("work", "").strip()
        auth = q.get("author", "").strip()
        if not work:
            continue
        key = (normalize_text(work), normalize_text(auth))
        if key not in qb_strict:
            qb_strict[key] = {
                "work": work,
                "author": auth,
                "quotes": [],
                "tags": set()
            }
        qb_strict[key]["quotes"].append({
            "quote": q.get("quote"),
            "explanation": q.get("explanation")
        })
        qb_strict[key]["tags"].update(q.get("tags", []))

    bs_moves = []
    hbr_moves = []
    shelf_items = []
    tbr_dict = {}

    for b in raw_books:
        fn = b["filename"]
        fn_lower = fn.lower()
        dp = b["drive_path"]
        cat = b["category"]
        fmt = b["format"].upper()

        # 1. Classify tactical bullshit
        if is_bullshit(fn):
            dest_path = f"Books/Archive of bullshit/{fn}"
            bs_moves.append((dp, dest_path))
            continue # HIDE from active shelf and TBR!

        # 2. Classify HBR
        if is_hbr(fn):
            dest_path = f"Books/HBR/{fn}"
            hbr_moves.append((dp, dest_path))
            cat = "Harvard Business Review"

        # 3. Handle multi-issue comic deduplication
        if "watchmen" in fn_lower and ("00" in fn_lower or "01" in fn_lower):
            if "watchmen_complete" in tbr_dict:
                continue
            shelf_items.append({
                "id": "watchmen-complete",
                "title": "Watchmen (Complete Series)",
                "author": "Alan Moore & Dave Gibbons",
                "category": "Comics & Graphic Novels",
                "format": "CBR",
                "cover_url": "https://covers.openlibrary.org/b/id/8231996-M.jpg",
                "pitch": "The monumental superhero deconstruction set against the ticking clock of nuclear armageddon. Rorschach investigates the murder of a former masked vigilante, uncovering a cosmic conspiracy.",
                "why_love": "Redefined what graphic storytelling could achieve; a dense nine-panel grid masterpiece of political dread and flawed human gods.",
                "tags": ["graphic-novel", "superhero-deconstruction", "cold-war", "classic", "dark"],
                "drive_path": dp,
                "filename": fn,
                "has_quote_bank": False,
                "quotes": []
            })
            tbr_dict["watchmen_complete"] = ("Watchmen (Complete Series)", "Alan Moore & Dave Gibbons")
            continue

        if "oyasumi punpun" in fn_lower:
            if "punpun_complete" in tbr_dict:
                continue
            shelf_items.append({
                "id": "goodnight-punpun-complete",
                "title": "Goodnight Punpun (Complete Series)",
                "author": "Inio Asano",
                "category": "Comics & Graphic Novels",
                "format": "PDF",
                "cover_url": "https://covers.openlibrary.org/b/id/10574169-M.jpg",
                "pitch": "A coming-of-age psychological masterpiece depicting Punpun Onodera, an innocent child drawn as a simple bird caricature navigating domestic abuse, depression, and turbulent young adulthood.",
                "why_love": "Universally acclaimed for its raw vulnerability, devastating emotional realism, and photorealistic backdrops.",
                "tags": ["manga", "coming-of-age", "psychological", "raw-honesty", "dark"],
                "drive_path": dp,
                "filename": fn,
                "has_quote_bank": False,
                "quotes": []
            })
            tbr_dict["punpun_complete"] = ("Goodnight Punpun (Complete Series)", "Inio Asano")
            continue

        # 4. Strict Title and Author Resolution
        title = b["title"]
        author = b["author"]
        pitch = ""
        why_love = ""

        # Check exact known titles
        matched_exact = False
        for ek, (etitle, eauth, ecat, epitch, ewhy) in EXACT_KNOWN_TITLES.items():
            if ek in fn_lower:
                title = etitle
                author = eauth
                cat = ecat
                pitch = epitch
                why_love = ewhy
                matched_exact = True
                break

        if not matched_exact:
            # Clean filename base
            base = re.sub(r'\.(epub|pdf|cbr|cbz|mobi|docx|pptx)$', '', fn, flags=re.I)
            base = re.sub(r'\[.*?\]|\(.*?\)', ' ', base).replace('_', ' ')
            base = re.sub(r'\s+', ' ', base).strip()

            if " - " in base:
                parts = [p.strip() for p in base.split(" - ") if p.strip()]
                if len(parts) == 2:
                    # Determine author vs title
                    p1, p2 = parts
                    # Check common inverted pattern "Author - Title"
                    if any(p1.lower() == a.lower() for a in ["chuck palahniuk", "george orwell", "umberto eco", "harishankar parsai", "andrei tarkovsky", "john yorke", "blake snyder", "tiago amaral", "eli schwartz", "seth godin", "dan nelken", "dave gerhardt", "justin welsh"]):
                        author = p1
                        title = p2
                    else:
                        title = p1
                        author = p2

        # 5. Strict Quote Bank Attachment (NO FALSE POSITIVES)
        norm_t = normalize_text(title)
        norm_a = normalize_text(author)
        qb_hit = None

        # Only match if normalized work matches and (author matches or author is unknown)
        for (qw, qa), qval in qb_strict.items():
            if qw == norm_t:
                if not norm_a or norm_a in qa or qa in norm_a or norm_a == "unknown":
                    qb_hit = qval
                    break

        quotes = []
        has_qb = False
        tags = [cat.lower().replace(" & ", "-").replace(" ", "-")]

        if qb_hit:
            has_qb = True
            quotes = qb_hit["quotes"][:3]
            tags.extend(list(qb_hit["tags"]))
            if not pitch:
                first_exp = quotes[0]["explanation"].split("\n\n")[0] if quotes else ""
                pitch = first_exp[:320] + "..." if len(first_exp) > 320 else first_exp
            if not why_love:
                why_love = "Celebrated for its striking prose rhythm, emotional clarity, and unforgettable cold-reader scenes."

        if not pitch:
            pitch = f"A notable work in {cat} by {author} exploring key human observations, ideas, and craft."
        if not why_love:
            why_love = "Admired for its distinct narrative voice, memorable perspective, and enduring resonance."

        # Unique book ID
        clean_key = f"{title.lower()}---{author.lower()}"
        if clean_key in tbr_dict:
            continue
        tbr_dict[clean_key] = (title, author)

        book_id = re.sub(r'[^a-z0-9]+', '-', f"{title}-{author}".lower()).strip('-')

        shelf_items.append({
            "id": book_id,
            "title": title,
            "author": author,
            "category": cat,
            "format": fmt,
            "cover_url": "",
            "pitch": pitch,
            "why_love": why_love,
            "tags": list(set(tags)),
            "drive_path": dp,
            "filename": fn,
            "has_quote_bank": has_qb,
            "quotes": quotes
        })

    # Sort shelf and TBR
    shelf_items.sort(key=lambda x: (x["category"], x["title"]))
    clean_tbr_lines = [f"{t} — {a}" for t, a in sorted(tbr_dict.values(), key=lambda x: x[0].lower())]

    print(f"\n==========================================")
    print(f"Total active curated shelf volumes: {len(shelf_items)}")
    print(f"Total clean TBR list items: {len(clean_tbr_lines)}")
    print(f"Identified tactical bullshit to archive: {len(bs_moves)}")
    print(f"Identified HBR documents for dedicated folder: {len(hbr_moves)}")
    print(f"==========================================\n")

    # Save shelf JSON
    SHELF_JSON_PATH.write_text(json.dumps(shelf_items, indent=2, ensure_ascii=False), encoding="utf-8")
    TBR_OUTPUT_PATH.write_text("\n".join(clean_tbr_lines), encoding="utf-8")
    print(f"Saved cleaned shelf: {SHELF_JSON_PATH}")
    print(f"Saved clean TBR list: {TBR_OUTPUT_PATH}")

    # Generate rclone move script
    generate_move_script(bs_moves, hbr_moves)

def generate_move_script(bs_moves, hbr_moves):
    lines = [
        "#!/usr/bin/env bash",
        "# scripts/move_drive_files.sh — Server-side moves tactical lead magnets and HBR books on Google Drive",
        "# Usage: bash scripts/move_drive_files.sh",
        "# Requires: rclone configured with 'gdrive:'",
        "set -euo pipefail",
        "",
        "echo '=== Creating Target Folders on Google Drive ==='",
        'rclone mkdir "gdrive:Books/Archive of bullshit"',
        'rclone mkdir "gdrive:Books/HBR"',
        "",
        "echo '=== Moving Tactical Lead Magnets & Whitepapers to Archive of bullshit ==='"
    ]
    
    for src, dst in bs_moves:
        lines.append(f'rclone moveto "gdrive:Books/{src}" "gdrive:{dst}"')

    lines.append("")
    lines.append("echo '=== Moving Harvard Business Review Books to Books/HBR ==='")
    for src, dst in hbr_moves:
        lines.append(f'rclone moveto "gdrive:Books/{src}" "gdrive:{dst}"')

    lines.append("")
    lines.append("echo '=== All moves completed successfully! ==='")

    MOVE_SCRIPT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    MOVE_SCRIPT_PATH.chmod(0o755)
    print(f"Generated Google Drive organization script: {MOVE_SCRIPT_PATH}")

if __name__ == "__main__":
    main()
