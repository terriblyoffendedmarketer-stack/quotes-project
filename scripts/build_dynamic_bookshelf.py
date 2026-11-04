# scripts/build_dynamic_bookshelf.py — Normalizes, enriches, and compiles the dynamic Google Drive bookshelf and TBR list
# Usage: python3 scripts/build_dynamic_bookshelf.py
# Requires: content/gdrive_books_catalog.json, content/quote-bank.json, content/authors.md
#
# Gotchas:
# - Drives contain inverted filenames ("Author - Title" vs "Title - Author").
# - Multi-issue comics (Watchmen #1..#12, Oyasumi Punpun v1..v13) are grouped into complete series cards.
# - Screenplays have specific authors and directors mapped for clean attribution.
# - Output HTML includes full Tailwind UI, search, tag filters, TBR copy, editable rename modal, custom cover URLs, and quote corpus.

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "content" / "gdrive_books_catalog.json"
QUOTE_BANK_PATH = ROOT / "content" / "quote-bank.json"

TBR_OUTPUT_PATH = ROOT / "content" / "tbr_clean_list.txt"
SHELF_JSON_PATH = ROOT / "content" / "books_curated_shelf.json"
SHELF_HTML_PROTO = ROOT / "prototype" / "shelf.html"
SHELF_HTML_DOCS = ROOT / "docs" / "shelf.html"
ARTIFACT_PATH = Path("/Users/apple/.gemini/antigravity/brain/81ccc3e6-122f-446d-b723-e563a56f7ea9/dynamic_bookshelf.html")

KNOWN_AUTHORS = [
    "Haruki Murakami", "Kurt Vonnegut", "Kurt Vonnegut Jr.", "Charles Bukowski", "Alain De Botton",
    "James Baldwin", "Pierce Brown", "Virginia Woolf", "Robert Cialdini", "Matt Dinniman",
    "Meiko Kawakami", "Rahi Masoom Raza", "Perumal Murugan", "Jia Tolentino", "Ted Chiang",
    "Ken Liu", "Claudia Piñeiro", "E. M. Forster", "Chuck Palahniuk", "George Orwell",
    "Umberto Eco", "Harishankar Parsai", "Stephen King", "Franz Kafka", "Fyodor Dostoevsky",
    "Leo Tolstoy", "Albert Camus", "Jorge Luis Borges", "Italo Calvino", "Vladimir Nabokov",
    "Sylvia Plath", "Saadat Hasan Manto", "Truman Capote", "Raymond Carver", "E. B. White",
    "Kazuo Ishiguro", "Cormac McCarthy", "David Foster Wallace", "George Saunders", "Zadie Smith",
    "Arundhati Roy", "Vivek Shanbhag", "Jhumpa Lahiri", "Salman Rushdie", "Amitav Ghosh",
    "Geetanjali Shree", "Elena Ferrante", "Milan Kundera", "Hilary Mantel", "Donna Tartt",
    "Ocean Vuong", "Sally Rooney", "Ottessa Moshfegh", "Annie Ernaux", "Joan Didion",
    "Annie Dillard", "Anne Lamott", "Mary Karr", "Oliver Sacks", "Nora Ephron",
    "Hunter S. Thompson", "Tom Wolfe", "Oliver Burkeman", "Paul Kalanithi", "J. D. Salinger",
    "Shirley Jackson", "Ursula K. Le Guin", "Seneca", "Andrei Tarkovsky", "Walter Murch",
    "John Yorke", "Blake Snyder", "Neil Gaiman", "Alan Moore", "Katsuhiro Otomo",
    "Seth Godin", "Al Ries", "Laura Ries", "Alex Hormozi", "Tim Ferriss", "J. Kenji López-Alt",
    "Maangchi", "Amartya Sen", "John Gray", "Roland Barthes", "Nigel Benson", "David Orrell",
    "Rupert Woodfin", "Stuart Hood", "David Norris", "Anthony O'Hear", "Ziauddin Sardar",
    "Maggie Hyde", "Rius", "John Nagle", "Stephen Fox", "Adele Revella", "Eli Schwartz",
    "Jordan Belfort", "Sabri Suby", "Liu Cixin", "Cixin Liu", "H. P. Lovecraft", "Thomas S. Kuhn",
    "Patrick Radden Keefe", "Rebecca Skloot", "Cho Nam-Joo", "Bret Easton Ellis", "Seishi Yokomizo",
    "Benedict Jacka", "Ben Aaronovitch", "Jim Butcher", "Jann S. Wenner", "Irvine Welsh",
    "Nawal El Saadawi", "Amir Levine", "Lidia Zylowska", "Stuart Turton", "Sohn Won-pyung",
    "John Steinbeck", "Phil Knight", "Lori Gottlieb", "Julie Zhuo", "NISIOISIN", "Etgar Keret",
    "J. K. Rowling", "Inio Asano", "Ray Dalio", "David Allen", "Kevin Kelly", "Slavoj Žižek",
    "Thomas Frank", "Friedrich Engels", "G. W. F. Hegel", "Bertrand Russell", "Jostein Gaarder",
    "Lao Tzu", "Madeleine L'Engle", "Steven D. Levitt", "Nancy Duarte", "Cord Jefferson",
    "Rainer Maria Rilke", "Movement by David"
]

KNOWN_SCREENPLAYS = {
    "arrival": ("Arrival (Screenplay)", "Eric Heisserer (dir. Denis Villeneuve)", "2016", ["sci-fi", "linguistics", "nonlinear-time", "grief"]),
    "the-martian": ("The Martian (Screenplay)", "Drew Goddard (dir. Ridley Scott)", "2015", ["survival", "problem-solving", "optimism", "science"]),
    "groundhogday": ("Groundhog Day (Screenplay)", "Danny Rubin & Harold Ramis", "1993", ["existential-comedy", "time-loop", "redemption", "classic"]),
    "올드보이": ("Oldboy (Screenplay)", "Park Chan-wook & Hwang Jo-yun", "2003", ["revenge", "neo-noir", "tragedy", "visceral"]),
    "jojo-rabbit": ("Jojo Rabbit (Screenplay)", "Taika Waititi", "2019", ["satire", "wwii", "loss-of-innocence", "heartfelt"]),
    "500-days-of-summer": ("(500) Days of Summer (Screenplay)", "Scott Neustadter & Michael H. Weber", "2009", ["romance-deconstruction", "nonlinear", "memory", "humor"]),
    "get-out": ("Get Out (Screenplay)", "Jordan Peele", "2017", ["social-horror", "paranoia", "tight-pacing", "satire"]),
    "logan": ("Logan (Screenplay)", "Scott Frank, James Mangold & Michael Green", "2017", ["neo-western", "mortality", "redemption", "gritty"]),
    "everything-everywhere-all-at-once": ("Everything Everywhere All at Once (Screenplay)", "Daniel Kwan & Daniel Scheinert", "2022", ["multiverse", "absurdism", "existential-nihilism", "family"]),
    "american-fiction": ("American Fiction (Screenplay)", "Cord Jefferson", "2023", ["literary-satire", "identity", "family-grief", "wit"])
}

SPECIAL_CLEANUPS = {
    "damianthefatass": ("Cookbook of Gains", "Damian", "Cooking & Food", "High-protein, fitness-focused comfort recipes engineered for simple, consistent meal prep.", "Zero fluff, muscle-building fuel with actual taste."),
    "the book of ramen": ("The Book of Ramen", "Ramen Lords & Community", "Cooking & Food", "An exhaustive, obsessive guide to mastering authentic regional Japanese ramen broths, noodles, and tare at home.", "Unlocks the exact food chemistry behind legendary tonkotsu and shoyu bowls."),
    "the food lab better home cooking through science": ("The Food Lab: Better Home Cooking Through Science", "J. Kenji López-Alt", "Cooking & Food", "The culinary Bible breaking down every fundamental cooking technique using rigorous empirical food science.", "Turns cooking from superstitious guesswork into reproducible culinary perfection."),
    "maangchi's real korean cooking": ("Maangchi's Real Korean Cooking", "Maangchi (Emily Kim)", "Cooking & Food", "Authentic, vibrant homestyle Korean cuisine directly from the internet's most beloved Korean cooking mother.", "Foolproof recipes for kimchi, bulgogi, stews, and side dishes."),
    "the 4 hour chef": ("The 4-Hour Chef", "Tim Ferriss", "Cooking & Food", "A meta-learning blueprint disguised as a culinary journey, teaching rapid skill acquisition through cooking.", "Wildly entertaining masterclass on accelerated learning frameworks."),
    "akira": ("Akira (Complete)", "Katsuhiro Otomo", "Comics & Graphic Novels", "The monumental cyberpunk manga epic detailing psychic warfare, societal collapse, and motorcycle gangs in Neo-Tokyo.", "Pioneered modern cinematic manga storytelling and visceral kinetic action."),
    "the sandman complete": ("The Sandman (Complete Collection)", "Neil Gaiman", "Comics & Graphic Novels", "The legendary dark fantasy saga of Morpheus, the Lord of Dreams, weaving world mythology, history, and literature.", "Widely regarded as the single greatest literary comic book series ever written."),
    "the argumentative indian": ("The Argumentative Indian", "Amartya Sen", "Philosophy, Essays & Misc", "Nobel laureate Amartya Sen's classic essays on India's rich history of public debate, secularism, and pluralism.", "Demolishes narrow stereotypes with centuries of intellectual and philosophical tradition."),
    "influence": ("Influence: The Psychology of Persuasion", "Robert Cialdini", "Marketing & Strategy", "The seminal psychological study of the six universal principles of ethical and unyielding persuasion.", "The undisputed foundation stone of all modern marketing, sales, and behavioral economics."),
    "feline philosophy": ("Feline Philosophy: Cats and the Meaning of Life", "John Gray", "Philosophy, Essays & Misc", "A sharp philosophical critique of human anxiety and self-delusion through the quiet, contented nature of cats.", "Stripping away human hubris with witty, incisive philosophical clarity."),
    "letters to milena": ("Letters to Milena", "Franz Kafka", "Fiction & Non-Fiction", "Kafka's raw, agonizingly intimate epistolary relationship with the brilliant translator Milena Jesenská.", "One of literature's most vulnerable chronicles of nervous, obsessive romantic longing."),
    "style an anti textbook": ("Style: An Anti-Textbook", "Richard Lanham", "Cinema & Film Craft", "A playful, fierce rejection of stuffy bureaucratic prose in favor of vocal rhythm, drama, and rhetorical panache.", "Restores fun and muscular vitality to written English sentences."),
    "sculpting in time": ("Sculpting in Time", "Andrei Tarkovsky", "Cinema & Film Craft", "The master filmmaker's profound meditation on cinema as a direct imprint of lived human time.", "The ultimate sacred text for filmmakers seeking spiritual and artistic integrity."),
    "into the woods": ("Into the Woods: How Stories Work and Why We Tell Them", "John Yorke", "Cinema & Film Craft", "An architectural deep dive into universal five-act storytelling structure across theater, cinema, and literature.", "The single best structural breakdown of narrative psychology ever written."),
    "in the blink of an eye": ("In the Blink of an Eye: A Perspective on Film Editing", "Walter Murch", "Cinema & Film Craft", "Legendary editor/sound designer Walter Murch reveals how film editing reflects human consciousness.", "A timeless, poetic craft book on pacing, cuts, and the psychology of vision."),
    "save the cat": ("Save the Cat! The Last Book on Screenwriting", "Blake Snyder", "Cinema & Film Craft", "The legendary, punchy Hollywood screenwriting handbook with the famous 15-beat beat sheet.", "Essential blueprint for understanding commercial pacing and audience momentum."),
    "the death of the author": ("The Death of the Author", "Roland Barthes", "Philosophy, Essays & Misc", "The revolutionary post-structuralist essay severing a text's meaning from its creator's intent.", "The bedrock of modern literary criticism and open interpretation."),
    "the 22 immutable laws of branding": ("The 22 Immutable Laws of Branding", "Al Ries & Laura Ries", "Marketing & Strategy", "The battle-tested laws of category ownership, contraction, and singular focus.", "Brutally concise rules that prevent businesses from self-sabotaging their identity."),
    "permission marketing": ("Permission Marketing", "Seth Godin", "Marketing & Strategy", "The paradigm shift from interruptive spam to turning strangers into friends and friends into customers.", "The foundational doctrine of modern respect-based digital marketing."),
    "$100m offers": ("$100M Offers: How To Make Offers So Good People Feel Stupid Saying No", "Alex Hormozi", "Marketing & Strategy", "A ruthlessly practical, mathematically sound guide to creating irresistible value propositions.", "Zero-nonsense operational guide that simplifies pricing and pricing psychology."),
    "rilke": ("Poems from the Book of Hours", "Rainer Maria Rilke", "Fiction & Non-Fiction", "Rilke's transcendent, mystical prayers wrestling with darkness, divinity, and solitary creative awakening.", "Lyrical spiritual poetry that pierces ordinary perception."),
    "total shoulder mobility": ("Total Shoulder Mobility 2.0", "Movement by David", "Philosophy, Essays & Misc", "A functional movement routine designed to decompress stiff joints and build bulletproof overhead mobility.", "Direct, biomechanically sound drills for daily posture correction.")
}

def clean_title_author(raw_title, raw_author, filename):
    fn_lower = filename.lower()
    
    # Check exact cleanups
    for k, (t, a, c, p, w) in SPECIAL_CLEANUPS.items():
        if k in fn_lower:
            return t, a, c, p, w, [c.lower().replace(" & ", "-")]
            
    # Check screenplays
    for spk, (spt, spa, spyear, sptags) in KNOWN_SCREENPLAYS.items():
        if spk in fn_lower:
            return spt, spa, "Screenplays", f"Original master screenplay from {spyear}.", "Masterclass in scene geometry and dialogue.", sptags
            
    return raw_title, raw_author, None, None, None, None

def normalize_all():
    with open(CATALOG_PATH) as f:
        gbooks = json.load(f)
        
    qb_index = {}
    if QUOTE_BANK_PATH.exists():
        with open(QUOTE_BANK_PATH) as f:
            qb_data = json.load(f)
        for q in qb_data:
            work = (q.get("work") or "").strip().lower()
            if not work:
                continue
            if work not in qb_index:
                qb_index[work] = {
                    "author": q.get("author"),
                    "work": q.get("work"),
                    "tags": set(),
                    "quotes": []
                }
            qb_index[work]["tags"].update(q.get("tags", []))
            qb_index[work]["quotes"].append({
                "quote": q.get("quote"),
                "explanation": q.get("explanation")
            })

    shelf = []
    seen_keys = set()
    tbr_dict = {}

    for item in gbooks:
        fn = item["filename"]
        fn_lower = fn.lower()
        cat = item["category"]
        fmt = item["format"].upper()
        drive_path = item["drive_path"]
        
        # Collapse multi-issue series
        if "watchmen" in fn_lower and ("00" in fn_lower or "01" in fn_lower):
            if "watchmen_all" in seen_keys:
                continue
            seen_keys.add("watchmen_all")
            shelf.append({
                "id": "watchmen-complete",
                "title": "Watchmen (Complete Series)",
                "author": "Alan Moore & Dave Gibbons",
                "category": "Comics & Graphic Novels",
                "format": "CBR",
                "cover_url": "https://covers.openlibrary.org/b/id/8231996-M.jpg",
                "pitch": "The monumental superhero deconstruction set against the ticking clock of nuclear armageddon. Rorschach investigates the murder of a former masked vigilante, uncovering a cosmic conspiracy.",
                "why_love": "Redefined what comic art could achieve; a dense, nine-panel grid masterpiece of political dread and flawed human gods.",
                "tags": ["graphic-novel", "superhero-deconstruction", "cold-war", "classic", "dark"],
                "drive_path": drive_path,
                "filename": fn,
                "has_quote_bank": False,
                "quotes": []
            })
            tbr_dict["Watchmen (Complete Series)"] = "Alan Moore & Dave Gibbons"
            continue

        if "oyasumi punpun" in fn_lower:
            if "punpun_all" in seen_keys:
                continue
            seen_keys.add("punpun_all")
            shelf.append({
                "id": "goodnight-punpun-complete",
                "title": "Goodnight Punpun (Complete Series)",
                "author": "Inio Asano",
                "category": "Comics & Graphic Novels",
                "format": "PDF",
                "cover_url": "https://covers.openlibrary.org/b/id/10574169-M.jpg",
                "pitch": "A coming-of-age psychological masterpiece depicting Punpun Onodera, an innocent child drawn as a simple bird caricature navigating domestic abuse, depression, and turbulent young adulthood.",
                "why_love": "Universally acclaimed for its raw vulnerability, devastating emotional realism, and photorealistic backdrops.",
                "tags": ["manga", "coming-of-age", "psychological", "raw-honesty", "dark"],
                "drive_path": drive_path,
                "filename": fn,
                "has_quote_bank": False,
                "quotes": []
            })
            tbr_dict["Goodnight Punpun (Complete Series)"] = "Inio Asano"
            continue

        # Check clean title author mappings
        t, a, c, p, w, tg = clean_title_author(item["title"], item["author"], fn)
        if c:
            cat = c

        # Check graphic guides
        if "graphic guide" in cat.lower() or "introducing" in fn_lower:
            cat = "Graphic Guides"
            if not p:
                subject = t.replace("Introducing", "").strip()
                p = f"An accessible, illustrated comic-format primer deconstructing {subject} from fundamental origins to modern impact."
                w = "Visual mnemonic illustrations paired with high-density intellectual history."
                tg = ["graphic-guide", "illustrated", "primer"]

        # Check quote bank cross reference
        qb_match = None
        t_low = t.lower()
        for qwork, qdata in qb_index.items():
            if qwork == t_low or (len(qwork) > 4 and qwork in t_low) or (len(t_low) > 4 and t_low in qwork):
                qb_match = qdata
                break
                
        quotes = []
        has_qb = False
        if qb_match:
            has_qb = True
            t = qb_match["work"]
            a = qb_match["author"]
            quotes = qb_match["quotes"][:3]
            tags = list(qb_match["tags"])
            if not p:
                sample_exp = quotes[0]["explanation"] if quotes else ""
                first_p = sample_exp.split("\n\n")[0] if sample_exp else ""
                p = first_p[:320] + "..." if len(first_p) > 320 else first_p
            if not w:
                w = "Celebrated for its striking prose rhythm, emotional clarity, and unforgettable cold-reader scenes."
            tg = tags + [cat.lower().replace(" & ", "-")]

        if not p:
            p = f"A notable work in {cat} by {a} exploring key themes, human observation, and perspective."
        if not w:
            w = "Widely admired for its sharp insight, distinct narrative voice, and enduring ideas."
        if not tg:
            tg = [cat.lower().replace(" & ", "-")]

        # Deduplicate entry by (title, author)
        key = (t.lower().strip(), a.lower().strip())
        if key in seen_keys:
            continue
        seen_keys.add(key)
        
        # Build clean ID
        book_id = re.sub(r'[^a-z0-9]+', '-', f"{t}-{a}".lower()).strip('-')
        
        shelf.append({
            "id": book_id,
            "title": t,
            "author": a,
            "category": cat,
            "format": fmt,
            "cover_url": "", # Will fall back to dynamic jacket or user custom
            "pitch": p,
            "why_love": w,
            "tags": tg,
            "drive_path": drive_path,
            "filename": fn,
            "has_quote_bank": has_qb,
            "quotes": quotes
        })
        
        tbr_dict[t] = a

    shelf.sort(key=lambda x: (x["category"], x["title"]))
    tbr_clean_lines = [f"{t} — {a}" for t, a in sorted(tbr_dict.items(), key=lambda x: x[0].lower())]

    print(f"Processed {len(shelf)} unique books for shelf.")
    print(f"Generated {len(tbr_clean_lines)} unique clean TBR items.")

    SHELF_JSON_PATH.write_text(json.dumps(shelf, indent=2, ensure_ascii=False), encoding="utf-8")
    TBR_OUTPUT_PATH.write_text("\n".join(tbr_clean_lines), encoding="utf-8")

    build_html_app(shelf, tbr_clean_lines)

def build_html_app(shelf, tbr_lines):
    shelf_json = json.dumps(shelf, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Personal Library & Dynamic Reading Shelf</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    :root {{
      --background: #0f141c;
      --card: #181f2c;
      --card-hover: #1f2838;
      --border: #2a3447;
      --foreground: #f1f5f9;
      --muted-foreground: #94a3b8;
      --accent: #38bdf8;
      --accent-hover: #0ea5e9;
      --pill-bg: #222d3f;
    }}
    .light {{
      --background: #f8fafc;
      --card: #ffffff;
      --card-hover: #f1f5f9;
      --border: #e2e8f0;
      --foreground: #0f172a;
      --muted-foreground: #64748b;
      --accent: #0284c7;
      --accent-hover: #0369a1;
      --pill-bg: #e2e8f0;
    }}
    body {{
      background-color: var(--background);
      color: var(--foreground);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    .line-clamp-3 {{
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    .line-clamp-2 {{
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    /* Physical Book Cover Jacket Aesthetic */
    .book-jacket {{
      position: relative;
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
      box-shadow: 2px 4px 12px rgba(0, 0, 0, 0.4), inset -2px 0 6px rgba(0, 0, 0, 0.3);
      border-radius: 4px 8px 8px 4px;
      border-left: 6px solid rgba(255, 255, 255, 0.12);
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .book-jacket:hover {{
      transform: translateY(-2px);
      box-shadow: 4px 8px 20px rgba(0, 0, 0, 0.5), inset -2px 0 6px rgba(0, 0, 0, 0.3);
    }}
    .jacket-fiction {{
      background: linear-gradient(145deg, #312e81 0%, #1e1b4b 100%);
      border-left-color: #818cf8;
    }}
    .jacket-marketing {{
      background: linear-gradient(145deg, #831843 0%, #500724 100%);
      border-left-color: #f472b6;
    }}
    .jacket-philosophy {{
      background: linear-gradient(145deg, #064e3b 0%, #022c22 100%);
      border-left-color: #34d399;
    }}
    .jacket-cinema {{
      background: linear-gradient(145deg, #78350f 0%, #451a03 100%);
      border-left-color: #fbbf24;
    }}
    .jacket-screenplay {{
      background: linear-gradient(145deg, #1c1917 0%, #0c0a09 100%);
      border-left-color: #a8a29e;
    }}
    .jacket-comics {{
      background: linear-gradient(145deg, #701a75 0%, #4a044e 100%);
      border-left-color: #e879f9;
    }}
    .jacket-guides {{
      background: linear-gradient(145deg, #1e3a8a 0%, #172554 100%);
      border-left-color: #60a5fa;
    }}
    .jacket-food {{
      background: linear-gradient(145deg, #7c2d12 0%, #431407 100%);
      border-left-color: #fb923c;
    }}
  </style>
</head>
<body class="min-h-screen p-4 md:p-8">
  <div class="max-w-7xl mx-auto">
    <!-- Header -->
    <header class="flex flex-col md:flex-row md:items-center justify-between pb-6 mb-8 border-b border-[var(--border)] gap-4">
      <div>
        <div class="flex items-center gap-3">
          <span class="text-3xl">📚</span>
          <h1 class="text-2xl md:text-3xl font-bold tracking-tight text-[var(--foreground)]">My Drive Library & Dynamic Shelf</h1>
        </div>
        <p class="text-[var(--muted-foreground)] text-sm mt-1">
          {len(shelf)} volumes & screenplays • Visual Book Jackets • Quotes & Companion Notes • Live Rename & Cover Editor • TBR Exporter
        </p>
      </div>
      <div class="flex flex-wrap items-center gap-2">
        <button onclick="openRecommender()" class="px-4 py-2 bg-[var(--accent)] hover:bg-[var(--accent-hover)] text-white text-sm font-semibold rounded-lg shadow transition flex items-center gap-2">
          <span>✨</span>
          <span>What to Read Next?</span>
        </button>
        <button onclick="copyAllTbr()" class="px-4 py-2 bg-[var(--card)] hover:bg-[var(--border)] border border-[var(--border)] text-[var(--foreground)] text-sm font-medium rounded-lg transition flex items-center gap-2">
          <span>📋</span>
          <span id="copyAllBtnText">Copy TBR ({len(tbr_lines)})</span>
        </button>
      </div>
    </header>

    <!-- Controls / Filters -->
    <div class="bg-[var(--card)] border border-[var(--border)] rounded-xl p-4 md:p-5 mb-8 shadow-sm">
      <div class="flex flex-col md:flex-row gap-4 items-center justify-between mb-4">
        <!-- Search Input -->
        <div class="relative w-full md:w-96">
          <input 
            type="text" 
            id="searchInput" 
            oninput="renderShelf()"
            placeholder="Search title, author, keyword, or quote..." 
            class="w-full pl-10 pr-4 py-2 bg-[var(--background)] border border-[var(--border)] rounded-lg text-sm text-[var(--foreground)] placeholder-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
          />
          <span class="absolute left-3 top-2.5 text-[var(--muted-foreground)] text-sm">🔍</span>
        </div>

        <!-- Quick filter toggle -->
        <div class="flex items-center gap-4 w-full md:w-auto justify-between md:justify-end">
          <label class="flex items-center gap-2 text-sm text-[var(--muted-foreground)] cursor-pointer select-none">
            <input type="checkbox" id="quoteBankOnly" onchange="renderShelf()" class="rounded border-[var(--border)] accent-[var(--accent)] w-4 h-4" />
            <span>Has Quotes ({len([b for b in shelf if b['has_quote_bank']])})</span>
          </label>
          <span id="itemCount" class="text-xs font-semibold px-2.5 py-1 bg-[var(--pill-bg)] rounded-full text-[var(--muted-foreground)]">
            Showing {len(shelf)}
          </span>
        </div>
      </div>

      <!-- Category Filter Pills -->
      <div class="flex flex-wrap gap-2 pt-2 border-t border-[var(--border)]" id="categoryPills">
        <!-- dynamically populated -->
      </div>
    </div>

    <!-- Book Grid -->
    <div id="booksGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- dynamically populated -->
    </div>
  </div>

  <!-- Recommender Modal -->
  <div id="recommenderModal" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl max-w-2xl w-full p-6 shadow-2xl overflow-y-auto max-h-[90vh]">
      <div class="flex items-center justify-between pb-4 border-b border-[var(--border)] mb-5">
        <div class="flex items-center gap-2">
          <span class="text-2xl">✨</span>
          <h2 class="text-xl font-bold text-[var(--foreground)]">What Should I Read Next?</h2>
        </div>
        <button onclick="closeRecommender()" class="text-[var(--muted-foreground)] hover:text-[var(--foreground)] text-xl font-bold px-2">✕</button>
      </div>

      <p class="text-sm text-[var(--muted-foreground)] mb-4">
        Pick what kind of experience you are in the mood for, or spin the wheel for a high-conviction book from your drive:
      </p>

      <!-- Mood selection buttons -->
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5 mb-6">
        <button onclick="recommendByMood('fast-paced')" class="p-3 text-left border border-[var(--border)] rounded-xl hover:bg-[var(--border)] transition">
          <div class="font-semibold text-sm text-[var(--foreground)]">⚡ Unputdownable</div>
          <div class="text-xs text-[var(--muted-foreground)]">High momentum, page-turner</div>
        </button>
        <button onclick="recommendByMood('sci-fi')" class="p-3 text-left border border-[var(--border)] rounded-xl hover:bg-[var(--border)] transition">
          <div class="font-semibold text-sm text-[var(--foreground)]">🌌 Mind-Bending Sci-Fi</div>
          <div class="text-xs text-[var(--muted-foreground)]">Cosmic scope & concepts</div>
        </button>
        <button onclick="recommendByMood('existential')" class="p-3 text-left border border-[var(--border)] rounded-xl hover:bg-[var(--border)] transition">
          <div class="font-semibold text-sm text-[var(--foreground)]">🧠 Existential & Absurd</div>
          <div class="text-xs text-[var(--muted-foreground)]">Quiet depth & dark humor</div>
        </button>
        <button onclick="recommendByMood('craft')" class="p-3 text-left border border-[var(--border)] rounded-xl hover:bg-[var(--border)] transition">
          <div class="font-semibold text-sm text-[var(--foreground)]">✍️ Masterful Prose</div>
          <div class="text-xs text-[var(--muted-foreground)]">Didion, Dillard, Baldwin</div>
        </button>
        <button onclick="recommendByMood('screenplay')" class="p-3 text-left border border-[var(--border)] rounded-xl hover:bg-[var(--border)] transition">
          <div class="font-semibold text-sm text-[var(--foreground)]">🎬 Cinema & Story</div>
          <div class="text-xs text-[var(--muted-foreground)]">Scripts & narrative craft</div>
        </button>
        <button onclick="recommendByMood('marketing')" class="p-3 text-left border border-[var(--border)] rounded-xl hover:bg-[var(--border)] transition">
          <div class="font-semibold text-sm text-[var(--foreground)]">🎯 Persuasion & Strategy</div>
          <div class="text-xs text-[var(--muted-foreground)]">Influence, branding, offers</div>
        </button>
      </div>

      <div class="flex items-center gap-3 mb-6">
        <div class="h-px bg-[var(--border)] flex-1"></div>
        <button onclick="surpriseMe()" class="px-5 py-2.5 bg-[var(--accent)] hover:bg-[var(--accent-hover)] text-white text-sm font-semibold rounded-xl shadow transition flex items-center gap-2">
          <span>🎲</span>
          <span>Surprise Me / Spin Shelf</span>
        </button>
        <div class="h-px bg-[var(--border)] flex-1"></div>
      </div>

      <!-- Recommendation Result Card -->
      <div id="recommendationResult" class="p-5 bg-[var(--background)] border border-[var(--border)] rounded-xl hidden">
        <div class="flex items-start justify-between gap-4 mb-2">
          <div>
            <div id="recCategory" class="text-xs font-semibold text-[var(--accent)] uppercase tracking-wider"></div>
            <h3 id="recTitle" class="text-lg font-bold text-[var(--foreground)] mt-0.5"></h3>
            <p id="recAuthor" class="text-sm font-medium text-[var(--muted-foreground)]"></p>
          </div>
          <button onclick="copySingleTbr(document.getElementById('recTitle').innerText, document.getElementById('recAuthor').innerText)" class="px-3 py-1 bg-[var(--card)] hover:bg-[var(--border)] border border-[var(--border)] text-xs font-medium rounded-lg">
            Copy
          </button>
        </div>
        <div class="mt-3 text-sm text-[var(--foreground)] leading-relaxed">
          <div class="font-semibold text-xs text-[var(--muted-foreground)] uppercase tracking-wider mb-1">The Pitch</div>
          <p id="recPitch"></p>
        </div>
        <div class="mt-3 p-3 bg-[var(--card)] rounded-lg text-xs text-[var(--muted-foreground)] border border-[var(--border)]">
          <span class="font-semibold text-[var(--foreground)]">Why read it:</span> <span id="recWhyLove"></span>
        </div>
      </div>
    </div>
  </div>

  <!-- Rename & Edit Modal -->
  <div id="editModal" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl max-w-lg w-full p-6 shadow-2xl overflow-y-auto max-h-[90vh]">
      <div class="flex items-center justify-between pb-3 border-b border-[var(--border)] mb-4">
        <h3 class="text-lg font-bold text-[var(--foreground)] flex items-center gap-2">
          <span>✏️</span>
          <span>Rename & Edit Book</span>
        </h3>
        <button onclick="closeEditModal()" class="text-[var(--muted-foreground)] hover:text-[var(--foreground)] font-bold text-lg px-2">✕</button>
      </div>

      <input type="hidden" id="editBookId" />

      <div class="space-y-4 text-sm">
        <div>
          <label class="block text-xs font-semibold text-[var(--muted-foreground)] uppercase mb-1">Book Title</label>
          <input type="text" id="editTitle" class="w-full px-3 py-2 bg-[var(--background)] border border-[var(--border)] rounded-lg text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]" />
        </div>

        <div>
          <label class="block text-xs font-semibold text-[var(--muted-foreground)] uppercase mb-1">Author</label>
          <input type="text" id="editAuthor" class="w-full px-3 py-2 bg-[var(--background)] border border-[var(--border)] rounded-lg text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]" />
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-semibold text-[var(--muted-foreground)] uppercase mb-1">Category</label>
            <select id="editCategory" class="w-full px-3 py-2 bg-[var(--background)] border border-[var(--border)] rounded-lg text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]">
              <option value="Fiction & Non-Fiction">Fiction & Non-Fiction</option>
              <option value="Cinema & Film Craft">Cinema & Film Craft</option>
              <option value="Screenplays">Screenplays</option>
              <option value="Marketing & Strategy">Marketing & Strategy</option>
              <option value="Philosophy, Essays & Misc">Philosophy, Essays & Misc</option>
              <option value="Graphic Guides">Graphic Guides</option>
              <option value="Comics & Graphic Novels">Comics & Graphic Novels</option>
              <option value="Cooking & Food">Cooking & Food</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-semibold text-[var(--muted-foreground)] uppercase mb-1">Custom Cover Image URL</label>
            <input type="text" id="editCoverUrl" placeholder="https://..." class="w-full px-3 py-2 bg-[var(--background)] border border-[var(--border)] rounded-lg text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]" />
          </div>
        </div>

        <div class="flex items-center justify-between text-xs text-[var(--accent)] pt-1">
          <button type="button" onclick="openGoodreadsSearch()" class="hover:underline flex items-center gap-1">
            <span>🔎</span>
            <span>Search cover on Goodreads</span>
          </button>
          <button type="button" onclick="openGoogleImagesSearch()" class="hover:underline flex items-center gap-1">
            <span>🖼️</span>
            <span>Search Google Images</span>
          </button>
        </div>

        <div>
          <label class="block text-xs font-semibold text-[var(--muted-foreground)] uppercase mb-1">Back-Cover Pitch</label>
          <textarea id="editPitch" rows="3" class="w-full px-3 py-2 bg-[var(--background)] border border-[var(--border)] rounded-lg text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"></textarea>
        </div>

        <div>
          <label class="block text-xs font-semibold text-[var(--muted-foreground)] uppercase mb-1">Why Read It / Notes</label>
          <textarea id="editWhyLove" rows="2" class="w-full px-3 py-2 bg-[var(--background)] border border-[var(--border)] rounded-lg text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"></textarea>
        </div>

        <div class="flex items-center justify-end gap-3 pt-3 border-t border-[var(--border)]">
          <button onclick="closeEditModal()" class="px-4 py-2 border border-[var(--border)] rounded-lg text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Cancel</button>
          <button onclick="saveEdit()" class="px-5 py-2 bg-[var(--accent)] hover:bg-[var(--accent-hover)] text-white text-sm font-semibold rounded-lg shadow">Save Changes</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Quote Notes Modal -->
  <div id="quotesModal" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl max-w-2xl w-full p-6 shadow-2xl overflow-y-auto max-h-[90vh]">
      <div class="flex items-center justify-between pb-3 border-b border-[var(--border)] mb-4">
        <div>
          <h3 id="modalBookTitle" class="text-lg font-bold text-[var(--foreground)]"></h3>
          <p id="modalBookAuthor" class="text-xs font-semibold text-[var(--muted-foreground)]"></p>
        </div>
        <button onclick="closeQuotesModal()" class="text-[var(--muted-foreground)] hover:text-[var(--foreground)] font-bold text-lg px-2">✕</button>
      </div>
      <div id="modalQuotesList" class="space-y-4">
        <!-- populated dynamically -->
      </div>
    </div>
  </div>

  <!-- Toast Notification -->
  <div id="toast" class="fixed bottom-6 right-6 bg-[var(--foreground)] text-[var(--background)] px-4 py-2.5 rounded-lg shadow-xl text-sm font-medium transition-all transform translate-y-16 opacity-0 pointer-events-none z-50">
    Copied to clipboard!
  </div>

  <script>
    let SHELF_DATA = {shelf_json};
    let activeCategory = "All";

    // Load any user overrides from localStorage
    const savedOverrides = localStorage.getItem("marginalia_shelf_edits");
    if (savedOverrides) {{
      try {{
        const overrides = JSON.parse(savedOverrides);
        SHELF_DATA = SHELF_DATA.map(b => overrides[b.id] ? Object.assign(b, overrides[b.id]) : b);
      }} catch (e) {{
        console.error("Failed to parse saved overrides", e);
      }}
    }}

    const CATEGORIES = [
      "All",
      "Fiction & Non-Fiction",
      "Cinema & Film Craft",
      "Screenplays",
      "Marketing & Strategy",
      "Philosophy, Essays & Misc",
      "Graphic Guides",
      "Comics & Graphic Novels",
      "Cooking & Food"
    ];

    function showToast(msg) {{
      const t = document.getElementById("toast");
      t.innerText = msg;
      t.classList.remove("translate-y-16", "opacity-0");
      setTimeout(() => {{
        t.classList.add("translate-y-16", "opacity-0");
      }}, 2500);
    }}

    function copyToClipboard(text, msg) {{
      navigator.clipboard.writeText(text).then(() => {{
        showToast(msg || "Copied to clipboard!");
      }});
    }}

    function copySingleTbr(title, author) {{
      copyToClipboard(`${{title}} — ${{author}}`, `Copied: "${{title}} — ${{author}}"`);
    }}

    function copyAllTbr() {{
      const q = document.getElementById("searchInput").value.toLowerCase().trim();
      const quoteOnly = document.getElementById("quoteBankOnly").checked;

      const filtered = SHELF_DATA.filter(b => {{
        if (activeCategory !== "All" && b.category !== activeCategory) return false;
        if (quoteOnly && !b.has_quote_bank) return false;
        if (q) {{
          const matchTitle = b.title.toLowerCase().includes(q);
          const matchAuthor = b.author.toLowerCase().includes(q);
          const matchPitch = (b.pitch || "").toLowerCase().includes(q);
          const matchTags = (b.tags || []).some(t => t.toLowerCase().includes(q));
          if (!matchTitle && !matchAuthor && !matchPitch && !matchTags) return false;
        }}
        return true;
      }});

      const lines = filtered.map(b => `${{b.title}} — ${{b.author}}`);
      copyToClipboard(lines.join("\\n"), `Copied ${{lines.length}} books to clipboard!`);
    }}

    function renderCategoryPills() {{
      const container = document.getElementById("categoryPills");
      container.innerHTML = CATEGORIES.map(cat => {{
        const isAct = cat === activeCategory;
        const count = cat === "All" ? SHELF_DATA.length : SHELF_DATA.filter(b => b.category === cat).length;
        if (count === 0) return "";
        return `
          <button 
            onclick="setCategory('${{cat}}')" 
            class="px-3 py-1.5 rounded-full text-xs font-medium transition ${{
              isAct 
                ? 'bg-[var(--accent)] text-white shadow-sm' 
                : 'bg-[var(--pill-bg)] text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--border)]'
            }}">
            ${{cat}} (${{count}})
          </button>
        `;
      }}).join("");
    }}

    function setCategory(cat) {{
      activeCategory = cat;
      renderCategoryPills();
      renderShelf();
    }}

    function getJacketClass(cat) {{
      if (cat.includes("Fiction")) return "jacket-fiction";
      if (cat.includes("Marketing")) return "jacket-marketing";
      if (cat.includes("Philosophy")) return "jacket-philosophy";
      if (cat.includes("Cinema")) return "jacket-cinema";
      if (cat.includes("Screenplay")) return "jacket-screenplay";
      if (cat.includes("Comics")) return "jacket-comics";
      if (cat.includes("Graphic Guide")) return "jacket-guides";
      if (cat.includes("Cooking")) return "jacket-food";
      return "";
    }}

    function renderShelf() {{
      const q = document.getElementById("searchInput").value.toLowerCase().trim();
      const quoteOnly = document.getElementById("quoteBankOnly").checked;
      const grid = document.getElementById("booksGrid");

      const filtered = SHELF_DATA.filter(b => {{
        if (activeCategory !== "All" && b.category !== activeCategory) return false;
        if (quoteOnly && !b.has_quote_bank) return false;
        if (q) {{
          const matchTitle = b.title.toLowerCase().includes(q);
          const matchAuthor = b.author.toLowerCase().includes(q);
          const matchPitch = (b.pitch || "").toLowerCase().includes(q);
          const matchTags = (b.tags || []).some(t => t.toLowerCase().includes(q));
          const matchQuotes = (b.quotes || []).some(item => (item.quote || "").toLowerCase().includes(q));
          if (!matchTitle && !matchAuthor && !matchPitch && !matchTags && !matchQuotes) return false;
        }}
        return true;
      }});

      document.getElementById("itemCount").innerText = `Showing ${{filtered.length}} of ${{SHELF_DATA.length}}`;

      if (filtered.length === 0) {{
        grid.innerHTML = `
          <div class="col-span-full py-16 text-center text-[var(--muted-foreground)]">
            <span class="text-4xl block mb-2">🔍</span>
            <p class="font-medium">No matching books found for "${{q}}"</p>
            <p class="text-xs mt-1">Try clearing your search query or switching categories.</p>
          </div>
        `;
        return;
      }}

      grid.innerHTML = filtered.map((b) => {{
        const hasQuote = b.quotes && b.quotes.length > 0;
        const quoteSnippet = hasQuote ? b.quotes[0].quote : "";
        const jacketCls = getJacketClass(b.category);

        return `
          <div class="bg-[var(--card)] hover:bg-[var(--card-hover)] border border-[var(--border)] rounded-xl p-5 shadow-sm transition flex flex-col justify-between group relative">
            <div>
              <!-- Visual Book Jacket Banner -->
              <div class="book-jacket ${{jacketCls}} p-4 mb-4 text-white rounded-lg flex flex-col justify-between min-h-[140px] relative overflow-hidden">
                ${{b.cover_url ? `
                  <img src="${{b.cover_url}}" alt="${{b.title}}" class="absolute inset-0 w-full h-full object-cover rounded-lg" onerror="this.style.display='none'" />
                  <div class="absolute inset-0 bg-gradient-to-t from-black/85 via-black/40 to-transparent"></div>
                ` : ''}}
                
                <div class="relative z-10 flex items-center justify-between">
                  <span class="text-[10px] font-bold tracking-widest uppercase opacity-85">${{b.category}}</span>
                  <span class="text-[9px] font-mono px-1.5 py-0.5 bg-black/40 rounded border border-white/20 text-white/90">
                    ${{b.format}}
                  </span>
                </div>

                <div class="relative z-10 my-2">
                  <h4 class="font-serif font-bold text-base md:text-lg leading-tight tracking-wide drop-shadow-sm text-white">
                    ${{b.title}}
                  </h4>
                  <p class="text-xs text-white/80 font-medium mt-0.5">${{b.author}}</p>
                </div>

                <div class="relative z-10 flex items-center justify-between pt-1 border-t border-white/15 text-[10px] text-white/70">
                  <span>${{hasQuote ? '★ Mined Passages' : 'Drive Library'}}</span>
                  <button onclick="openEditModal('${{b.id}}')" class="text-white hover:text-[var(--accent)] hover:underline flex items-center gap-1">
                    <span>✏️ Edit / Cover</span>
                  </button>
                </div>
              </div>

              <!-- Pitch / Back-cover synopsis -->
              <div class="text-xs text-[var(--foreground)] leading-relaxed mb-3 line-clamp-3">
                ${{b.pitch}}
              </div>

              <!-- Why people love it -->
              <div class="p-2.5 bg-[var(--background)] rounded-lg text-[11px] text-[var(--muted-foreground)] border border-[var(--border)] mb-3">
                <span class="font-semibold text-[var(--foreground)]">Why read it:</span> ${{b.why_love}}
              </div>

              <!-- Excerpt Quote (if available) -->
              ${{quoteSnippet ? `
                <div class="p-3 bg-blue-500/5 border border-blue-500/20 rounded-lg mb-3">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-[10px] font-semibold text-blue-400 uppercase tracking-wider">Notable Excerpt</span>
                    <button onclick="openQuotesModal('${{b.id}}')" class="text-[10px] text-blue-400 hover:underline font-medium">
                      View all notes (${{b.quotes.length}}) →
                    </button>
                  </div>
                  <p class="text-xs italic text-[var(--foreground)] line-clamp-3">
                    “${{quoteSnippet}}”
                  </p>
                </div>
              ` : ''}}
            </div>

            <!-- Footer / Copy button -->
            <div class="pt-3 border-t border-[var(--border)] flex items-center justify-between text-xs">
              <span class="text-[10px] text-[var(--muted-foreground)]">
                ${{hasQuote ? `★ ${{b.quotes.length}} Quotes` : ''}}
              </span>
              <div class="flex items-center gap-2">
                <button 
                  onclick="openEditModal('${{b.id}}')" 
                  class="px-2 py-1 bg-[var(--background)] hover:bg-[var(--border)] border border-[var(--border)] rounded text-[11px] font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition">
                  Rename
                </button>
                <button 
                  onclick="copySingleTbr('${{b.title.replace(/'/g, "\\\\\\'")}}', '${{b.author.replace(/'/g, "\\\\\\'")}}')" 
                  class="px-2.5 py-1 bg-[var(--accent)] hover:bg-[var(--accent-hover)] text-white rounded text-[11px] font-medium transition flex items-center gap-1 shadow-sm">
                  <span>📋</span>
                  <span>Copy</span>
                </button>
              </div>
            </div>
          </div>
        `;
      }}).join("");
    }}

    function openQuotesModal(bookId) {{
      const book = SHELF_DATA.find(b => b.id === bookId);
      if (!book) return;
      document.getElementById("modalBookTitle").innerText = book.title;
      document.getElementById("modalBookAuthor").innerText = book.author;
      const list = document.getElementById("modalQuotesList");

      list.innerHTML = (book.quotes || []).map((q, idx) => `
        <div class="p-4 bg-[var(--background)] border border-[var(--border)] rounded-xl">
          <div class="text-sm italic font-serif text-[var(--foreground)] mb-3 leading-relaxed border-l-2 border-[var(--accent)] pl-3">
            “${{q.quote}}”
          </div>
          ${{q.explanation ? `
            <div class="text-xs text-[var(--muted-foreground)] leading-relaxed pt-2 border-t border-[var(--border)]">
              <span class="font-semibold text-[var(--foreground)] block mb-1">Companion Insight & Context:</span>
              <p class="whitespace-pre-line">${{q.explanation}}</p>
            </div>
          ` : ''}}
        </div>
      `).join("");

      document.getElementById("quotesModal").classList.remove("hidden");
    }}

    function closeQuotesModal() {{
      document.getElementById("quotesModal").classList.add("hidden");
    }}

    function openEditModal(bookId) {{
      const b = SHELF_DATA.find(item => item.id === bookId);
      if (!b) return;

      document.getElementById("editBookId").value = b.id;
      document.getElementById("editTitle").value = b.title;
      document.getElementById("editAuthor").value = b.author;
      document.getElementById("editCategory").value = b.category;
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
      b.category = document.getElementById("editCategory").value;
      b.cover_url = document.getElementById("editCoverUrl").value.trim();
      b.pitch = document.getElementById("editPitch").value.trim();
      b.why_love = document.getElementById("editWhyLove").value.trim();

      // Save to localStorage
      let saved = {{}};
      try {{
        saved = JSON.parse(localStorage.getItem("marginalia_shelf_edits") || "{{}}");
      }} catch (e) {{}}
      saved[b.id] = {{
        title: b.title,
        author: b.author,
        category: b.category,
        cover_url: b.cover_url,
        pitch: b.pitch,
        why_love: b.why_love
      }};
      localStorage.setItem("marginalia_shelf_edits", JSON.stringify(saved));

      closeEditModal();
      renderCategoryPills();
      renderShelf();
      showToast(`Updated "${{b.title}}" and saved changes!`);
    }}

    function openGoodreadsSearch() {{
      const title = document.getElementById("editTitle").value.trim();
      const author = document.getElementById("editAuthor").value.trim();
      const q = encodeURIComponent(`${{title}} ${{author}}`);
      window.open(`https://www.goodreads.com/search?q=${{q}}`, '_blank');
    }}

    function openGoogleImagesSearch() {{
      const title = document.getElementById("editTitle").value.trim();
      const author = document.getElementById("editAuthor").value.trim();
      const q = encodeURIComponent(`${{title}} ${{author}} book cover`);
      window.open(`https://www.google.com/search?tbm=isch&q=${{q}}`, '_blank');
    }}

    function openRecommender() {{
      document.getElementById("recommenderModal").classList.remove("hidden");
    }}

    function closeRecommender() {{
      document.getElementById("recommenderModal").classList.add("hidden");
    }}

    function displayRecommendation(b) {{
      const res = document.getElementById("recommendationResult");
      document.getElementById("recCategory").innerText = b.category;
      document.getElementById("recTitle").innerText = b.title;
      document.getElementById("recAuthor").innerText = b.author;
      document.getElementById("recPitch").innerText = b.pitch;
      document.getElementById("recWhyLove").innerText = b.why_love;
      res.classList.remove("hidden");
    }}

    function surpriseMe() {{
      const randomBook = SHELF_DATA[Math.floor(Math.random() * SHELF_DATA.length)];
      displayRecommendation(randomBook);
    }}

    function recommendByMood(mood) {{
      let pool = [];
      if (mood === 'fast-paced') {{
        pool = SHELF_DATA.filter(b => (b.tags || []).some(t => t.includes('fast-paced') || t.includes('unputdownable') || t.includes('thriller') || t.includes('pacing')));
        if (pool.length === 0) pool = SHELF_DATA.filter(b => b.category === "Fiction & Non-Fiction");
      }} else if (mood === 'sci-fi') {{
        pool = SHELF_DATA.filter(b => (b.tags || []).some(t => t.includes('sci-fi') || t.includes('speculative') || t.includes('cosmic')));
      }} else if (mood === 'existential') {{
        pool = SHELF_DATA.filter(b => (b.tags || []).some(t => t.includes('existential') || t.includes('absurd') || t.includes('satire') || t.includes('philosophy')));
      }} else if (mood === 'craft') {{
        pool = SHELF_DATA.filter(b => (b.tags || []).some(t => t.includes('craft') || t.includes('writing') || t.includes('memoir') || t.includes('observation')));
      }} else if (mood === 'screenplay') {{
        pool = SHELF_DATA.filter(b => b.category === "Screenplays" || b.category === "Cinema & Film Craft");
      }} else if (mood === 'marketing') {{
        pool = SHELF_DATA.filter(b => b.category === "Marketing & Strategy");
      }}

      if (pool.length === 0) pool = SHELF_DATA;
      const pick = pool[Math.floor(Math.random() * pool.length)];
      displayRecommendation(pick);
    }}

    // Initial render
    renderCategoryPills();
    renderShelf();
  </script>
</body>
</html>
"""
    SHELF_HTML_PROTO.parent.mkdir(exist_ok=True)
    SHELF_HTML_PROTO.write_text(html, encoding="utf-8")
    SHELF_HTML_DOCS.parent.mkdir(exist_ok=True)
    SHELF_HTML_DOCS.write_text(html, encoding="utf-8")
    ARTIFACT_PATH.parent.mkdir(exist_ok=True)
    ARTIFACT_PATH.write_text(html, encoding="utf-8")
    print(f"Generated prototype page: {SHELF_HTML_PROTO}")
    print(f"Generated docs page: {SHELF_HTML_DOCS}")
    print(f"Generated artifact page: {ARTIFACT_PATH}")

if __name__ == "__main__":
    normalize_all()
