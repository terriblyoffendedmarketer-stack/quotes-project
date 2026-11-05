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

MANUAL_BOOK_FIXES = {
    # Graphic Novels & Comics Verified (OpenLibrary & Amazon Edition Sources)
    "watchmen-complete": {
        "title": "Watchmen (The Complete Series)",
        "author": "Alan Moore & Dave Gibbons",
        "category": "Comics & Graphic Novels",
        "cover_url": "https://covers.openlibrary.org/b/id/7774899-L.jpg",
        "pitch": "Alan Moore and Dave Gibbons' groundbreaking masterpiece that deconstructed the superhero mythos, set against the ticking clock of Cold War nuclear apocalypse and vigilantism.",
        "tags": ["graphic-novel", "dc-comics", "superheroes", "cold-war", "masterpiece"]
    },
    "the-sandman-complete-unknown": {
        "title": "The Sandman (The Complete Deluxe Collection)",
        "author": "Neil Gaiman",
        "category": "Comics & Graphic Novels",
        "cover_url": "https://covers.openlibrary.org/b/id/10708688-L.jpg",
        "pitch": "Neil Gaiman's magnum opus following Morpheus, the Lord of Dreams, imprisoned by an occult ritual before breaking free to rebuild his ruined kingdom of the Dreaming.",
        "tags": ["mythology", "fantasy", "graphic-novel", "dark-fantasy"]
    },
    "understanding-comics-scott-mccloud-unknown": {
        "title": "Understanding Comics: The Invisible Art",
        "author": "Scott McCloud",
        "category": "Comics & Graphic Novels",
        "cover_url": "https://covers.openlibrary.org/b/id/10679940-L.jpg"
    },
    "aristotle-a-graphic-biography": {
        "title": "Aristotle: A Graphic Biography",
        "author": "Alexandre Le Mercier & Étienne Schréder",
        "category": "Graphic Guides",
        "cover_url": "https://covers.openlibrary.org/b/id/12593945-L.jpg"
    },

    # Ben Goldacre
    "ben-goldacre-bad-pharma": {
        "title": "Bad Pharma: How Drug Companies Mislead Doctors and Harm Patients",
        "author": "Ben Goldacre",
        "category": "Philosophy, Essays & Misc",
        "cover_url": "https://covers.openlibrary.org/b/id/7289568-L.jpg",
        "pitch": "We like to imagine that medicine is based on evidence and fair clinical trials. In reality, those tests are conducted by pharmaceutical companies who frequently bury negative trials, conduct flawed studies with tiny groups, and distort research to market ineffective and dangerous drugs.",
        "tags": ["medicine", "investigative", "science", "healthcare", "pharma"],
        "why_love": "Ben Goldacre is the scourge of medical quackery and institutional deceit. In Bad Pharma, he lays bare the systemic corruption of clinical drug trials: how negative results are buried, how regulatory agencies are captured, and how doctors are misled into prescribing expensive, ineffective treatments. A furious, meticulously footnoted exposé."
    },
    "ben-goldacre-bad-science": {
        "title": "Bad Science: Quacks, Hacks, and Big Pharma Flacks",
        "author": "Ben Goldacre",
        "category": "Philosophy, Essays & Misc",
        "cover_url": "https://covers.openlibrary.org/b/id/6680603-L.jpg",
        "pitch": "Full of spleen, this is a hilarious, invigorating and informative journey through the world of bad science. When Dr. Ben Goldacre saw someone on daytime TV dipping her feet in an 'Aqua Detox' footbath and releasing brown sludge, he tested it with a Barbie doll and salt water. An essential takedown of homeopaths and tabloid scaremongers.",
        "tags": ["pseudoscience", "critical-thinking", "media-literacy", "humor"],
        "why_love": "Ben Goldacre opened his book with a Barbie doll sitting in a tub of brown sludge, and I have never trusted a footbath since. Reading it feels like being taken by the collar by a friend who happens to be a doctor and refuses to let you swallow a claim without checking the numbers."
    },

    # User targeted specific fixes
    "the-riddler-year-one": {
        "title": "The Riddler: Year One",
        "author": "Paul Dano & Stevan Subić",
        "category": "Comics & Graphic Novels",
        "format": "CBR",
        "cover_url": "https://covers.openlibrary.org/b/id/14643238-L.jpg",
        "pitch": "A six-issue psychological crime thriller written by actor Paul Dano, exploring forensic accountant Edward Nashton's spiral into madness, systemic corruption, and the emergence of the Riddler persona in Gotham City.",
        "tags": ["batman", "dc-comics", "crime", "psychological", "noir"],
        "why_love": "Written by Paul Dano himself to explore the interior psychology of his character from Matt Reeves' The Batman, this is one of the most viscerally unsettling, gorgeously textured Gotham noir tales ever committed to paper."
    },
    "the-sandman-complete-unknown": {
        "title": "The Sandman: Preludes & Nocturnes",
        "author": "Neil Gaiman",
        "category": "Comics & Graphic Novels",
        "cover_url": "https://covers.openlibrary.org/b/id/7508162-L.jpg",
        "pitch": "Neil Gaiman's magnum opus following Morpheus, the Lord of Dreams, imprisoned for seven decades by an occult ritual before breaking free to rebuild his ruined kingdom of the Dreaming and reclaim his lost tools of power.",
        "tags": ["mythology", "fantasy", "graphic-novel", "dark-fantasy"],
        "why_love": "Neil Gaiman took comic books and turned them into modern mythic literature. Morpheus walking into the depths of Hell with a helm crafted from a demon's spine is one of the indelible sequences of 20th-century graphic storytelling."
    },
    "tim-feriss-the-4-hour-chef": {
        "title": "The 4-Hour Chef: The Simple Path to Cooking Like a Pro, Learning Anything, and Living the Good Life",
        "author": "Timothy Ferriss",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/7256387-L.jpg",
        "pitch": "Building on the Meta-Learning framework (DiSSS: Deconstruction, Selection, Sequencing, Stakes), Ferriss deconstructs culinary mastery as a blueprint to learn any skill in record time, from knife technique to sensory training.",
        "tags": ["learning", "cooking", "productivity", "meta-learning"],
        "why_love": "Don't let the cookbook format fool you: this is Ferriss's masterclass on accelerated skill acquisition masquerading as culinary instruction. If you want to understand how to dissect a complex domain into atomic drills, this is the manual."
    },
    "how-to-research-anything-unknown": {
        "title": "How to Research Anything",
        "author": "Curated Dossier / Research Heuristics",
        "category": "Philosophy, Essays & Misc",
        "cover_url": None,
        "no_cover": True,
        "pitch": "A curated compendium of advanced web intelligence, investigative research workflows, search heuristics, and OSINT methodologies gathered from investigative journalists and research practitioners across the web.",
        "tags": ["research", "osint", "investigation", "methodology", "web-intelligence"],
        "why_love": "This isn't a single corporate manual; it's a battle-tested compilation of heuristics and search tools gathered across the best research communities on the web. It renders cleanly as a bespoke clothbound research jacket."
    },
    "how-to-win-at-chess-1-levy-rozman": {
        "title": "How to Win at Chess: The Ultimate Guide for Beginners and Beyond",
        "author": "Levy Rozman (GothamChess)",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/14135096-L.jpg",
        "pitch": "YouTube's favorite chess educator demystifies the 64 squares with accessible, humorous, and ruthlessly practical lessons covering opening traps, positional control, and endgames.",
        "tags": ["chess", "strategy", "games", "tactics"],
        "why_love": "Levy Rozman made chess strategy kinetic, hilarious, and genuinely fun. Instead of burying beginners in dry algebraic notation, he breaks down the psychology of mistakes and fundamental habits that actually raise your rating."
    },
    "how-to-win-at-chess-2-next-level-levy-rozman": {
        "title": "How to Win at Chess 2: Next Level",
        "author": "Levy Rozman (GothamChess)",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/15243805-L.jpg",
        "pitch": "The follow-up masterclass expanding into intermediate opening repertoires, piece sacrifice evaluations, middlegame planning, and calculation techniques.",
        "tags": ["chess", "strategy", "games", "tactics", "intermediate"],
        "why_love": "Taking players beyond the beginner plateau, this second volume focuses on the murky middlegame where games are won and lost. Spot tactical patterns under pressure without getting paralyzed."
    },
    "intimacy-trusting-oneself-and-the-other-by-osho": {
        "title": "Intimacy: Trusting Oneself and the Other",
        "author": "Osho",
        "category": "Philosophy, Essays & Misc",
        "cover_url": "https://covers.openlibrary.org/b/id/177935-L.jpg",
        "pitch": "An uncompromising exploration of why human beings crave profound connection yet run in terror from genuine vulnerability, revealing how fear of exposure and self-rejection undermine our closest relationships.",
        "tags": ["philosophy", "intimacy", "psychology", "vulnerability"],
        "why_love": "Osho cuts through romantic sentimentalism to expose the fundamental paradox of modern relationships: we want to be loved deeply, yet we armor ourselves behind masks to keep from being seen."
    },
    "osho-freedom-the-courage-to-be-yourself-libgen-li": {
        "title": "Freedom: The Courage to Be Yourself",
        "author": "Osho",
        "category": "Philosophy, Essays & Misc",
        "cover_url": "https://covers.openlibrary.org/b/id/185078-L.jpg"
    },

    # Cinema & Film Craft Fixes
    "cinematography-theory-and-practice-unknown": {
        "title": "Cinematography: Theory and Practice",
        "author": "Blain Brown",
        "category": "Cinema & Film Craft",
        "cover_url": "https://covers.openlibrary.org/b/id/11163976-L.jpg"
    },
    "directing-actors-unknown": {
        "title": "Directing Actors: Creating Memorable Performances for Film & Television",
        "author": "Judith Weston",
        "category": "Cinema & Film Craft",
        "cover_url": "https://covers.openlibrary.org/b/id/718358-L.jpg"
    },
    "save-the-cat-the-last-book-on-screenwriting-you-ll-ever-need-by-blake-snyder-unknown": {
        "title": "Save the Cat! The Last Book on Screenwriting You’ll Ever Need",
        "author": "Blake Snyder",
        "category": "Cinema & Film Craft",
        "cover_url": "https://covers.openlibrary.org/b/id/960754-L.jpg"
    },
    "save-the-cat-writes-a-novel-by-jessica-brody-unknown": {
        "title": "Save the Cat! Writes a Novel",
        "author": "Jessica Brody",
        "category": "Cinema & Film Craft",
        "cover_url": "https://covers.openlibrary.org/b/id/10148215-L.jpg"
    },
    "john-truby-the-anatomy-of-story": {
        "title": "The Anatomy of Story: 22 Steps to Becoming a Master Storyteller",
        "author": "John Truby",
        "category": "Cinema & Film Craft",
        "cover_url": "https://covers.openlibrary.org/b/id/9698720-L.jpg"
    },
    "the-anatomy-of-story-22-steps-to-becoming-a-master-storyteller-unknown": {
        "title": "The Anatomy of Story: 22 Steps to Becoming a Master Storyteller",
        "author": "John Truby",
        "category": "Cinema & Film Craft",
        "cover_url": "https://covers.openlibrary.org/b/id/9698720-L.jpg"
    },
    "robert-mckee-story": {
        "title": "Story: Substance, Structure, Style and the Principles of Screenwriting",
        "author": "Robert McKee",
        "category": "Cinema & Film Craft",
        "cover_url": "https://covers.openlibrary.org/b/id/38437-L.jpg"
    },
    "story-robert-mckee": {
        "title": "Story: Substance, Structure, Style and the Principles of Screenwriting",
        "author": "Robert McKee",
        "category": "Cinema & Film Craft",
        "cover_url": "https://covers.openlibrary.org/b/id/38437-L.jpg"
    },
    "master-shots-100-advanced-camera-techniques-to-get-an-expensive-look-on-your-low-budget-movie-unknown": {
        "title": "Master Shots: 100 Advanced Camera Techniques",
        "author": "Christopher Kenworthy",
        "category": "Cinema & Film Craft",
        "cover_url": "https://covers.openlibrary.org/b/id/7104834-L.jpg"
    },

    # Stephen King & Neil Gaiman (Inverted Fixes)
    "neil-gaiman-american-gods": {
        "title": "American Gods",
        "author": "Neil Gaiman",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/8233777-L.jpg"
    },
    "stephen-king-the-stand": {
        "title": "The Stand",
        "author": "Stephen King",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/8235109-L.jpg"
    },
    "stephen-king-billy-summers": {
        "title": "Billy Summers",
        "author": "Stephen King",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/10864389-L.jpg"
    },
    "stephen-king-the-dark-tower-01-the-gunslinger": {
        "title": "The Dark Tower: The Gunslinger",
        "author": "Stephen King",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/8235122-L.jpg"
    },
    "stephen-king-the-mist": {
        "title": "The Mist",
        "author": "Stephen King",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/8235136-L.jpg"
    },
    "stephen-king-salem-s-lot": {
        "title": "'Salem's Lot",
        "author": "Stephen King",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/8235111-L.jpg"
    },
    "stephen-king-it": {
        "title": "IT",
        "author": "Stephen King",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/8235086-L.jpg"
    },
    "stephen-king-pet-sematary": {
        "title": "Pet Sematary",
        "author": "Stephen King",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/8235103-L.jpg"
    },
    "stephen-king-on-writing": {
        "title": "On Writing: A Memoir of the Craft",
        "author": "Stephen King",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/8235099-L.jpg"
    },

    # Oliver Burkeman & Will Storr & T. Kingfisher & Mary Kubica & Marcus Kliewer
    "oliver-burkeman-four-thousand-weeks-time-management-for-mortals-libgen-li": {
        "title": "Four Thousand Weeks: Time Management for Mortals",
        "author": "Oliver Burkeman",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/12519129-L.jpg"
    },
    "oliver-burkeman-the-antidote-happiness-for-people-who-can-t-stand-positive-thinking-libgen-li": {
        "title": "The Antidote: Happiness for People Who Can't Stand Positive Thinking",
        "author": "Oliver Burkeman",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/7318721-L.jpg"
    },
    "oliver-burkeman-help-libgen-li": {
        "title": "Help! How to Become Slightly Happier and Get a Bit More Done",
        "author": "Oliver Burkeman",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/6989481-L.jpg"
    },
    "will-storr-the-status-game-on-social-position-and-how-we-use-it-libgen-li": {
        "title": "The Status Game: On Social Position and How We Use It",
        "author": "Will Storr",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/12389923-L.jpg"
    },
    "t-kingfisher-what-moves-the-dead-libgen-li": {
        "title": "What Moves the Dead",
        "author": "T. Kingfisher",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/12854930-L.jpg"
    },
    "marcus-kliewer-we-used-to-live-here-a-novel-libgen-li": {
        "title": "We Used to Live Here: A Novel",
        "author": "Marcus Kliewer",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/14578135-L.jpg"
    },
    "mary-kubica-local-woman-missing-libgen-li": {
        "title": "Local Woman Missing",
        "author": "Mary Kubica",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/10899011-L.jpg"
    },
    "james-hollis-the-middle-passage-from-misery-to-meaning-in-midlife-libgen-li": {
        "title": "The Middle Passage: From Misery to Meaning in Midlife",
        "author": "James Hollis",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/1197996-L.jpg"
    },
    "geoff-mulgan-big-mind-how-collective-intelligence-can-change-our-world-libgen-li": {
        "title": "Big Mind: How Collective Intelligence Can Change Our World",
        "author": "Geoff Mulgan",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/8382431-L.jpg"
    },
    "phil-knight-shoe-dog-a-memoir-by-the-creator-of-nike": {
        "title": "Shoe Dog: A Memoir by the Creator of Nike",
        "author": "Phil Knight",
        "category": "Marketing & Strategy",
        "cover_url": "https://covers.openlibrary.org/b/id/8354784-L.jpg"
    },

    # Verified Classics & Key Reads
    "barabara-oakley-a-mind-for-numbers": {
        "title": "A Mind for Numbers: How to Excel at Math and Science",
        "author": "Barbara Oakley",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/8352403-L.jpg"
    },
    "david-allen-getting-things-done-unknown": {
        "title": "Getting Things Done: The Art of Stress-Free Productivity",
        "author": "David Allen",
        "category": "Marketing & Strategy",
        "cover_url": "https://covers.openlibrary.org/b/id/109288-L.jpg"
    },
    "ed-catmull-amy-wallace-creativity-inc-overcoming-the-unseen-forces-that-stand-in-the-way-of-true-inspiration-libgen-li": {
        "title": "Creativity, Inc.: Overcoming the Unseen Forces That Stand in the Way of True Inspiration",
        "author": "Ed Catmull & Amy Wallace",
        "category": "Marketing & Strategy",
        "cover_url": "https://covers.openlibrary.org/b/id/13124793-L.jpg"
    },
    "everybody-lies-seth-stephens-davidowitz": {
        "title": "Everybody Lies: Big Data, New Data, and What the Internet Can Tell Us About Who We Really Are",
        "author": "Seth Stephens-Davidowitz",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/8294628-L.jpg"
    },
    "40-rules-of-love-elif-shafak": {
        "title": "The Forty Rules of Love",
        "author": "Elif Shafak",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/9078986-L.jpg"
    },
    "alex-verus-1-fated-benedict-jacka": {
        "title": "Fated (Alex Verus #1)",
        "author": "Benedict Jacka",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/7367355-L.jpg"
    },
    "a-self-help-guide-for-copywriters-dan-nelken": {
        "title": "A Self-Help Guide for Copywriters",
        "author": "Dan Nelken",
        "category": "Marketing & Strategy",
        "cover_url": "https://covers.openlibrary.org/b/id/12838741-L.jpg"
    },
    "chess-for-zebras-jonathan-rowson": {
        "title": "Chess for Zebras: Thinking Differently About Black and White",
        "author": "Jonathan Rowson",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/2144888-L.jpg"
    },
    "mikhail-tal-the-life-and-games-of-mikhail-tal-libgen-li": {
        "title": "The Life and Games of Mikhail Tal",
        "author": "Mikhail Tal",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/7946850-L.jpg"
    },
    "the-silent-patient-by-alex-michaelides-pdfread-unknown": {
        "title": "The Silent Patient",
        "author": "Alex Michaelides",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/9407338-L.jpg"
    },
    "the-genealogy-of-morals-by-friedrich-nietzsche-unknown": {
        "title": "On the Genealogy of Morals",
        "author": "Friedrich Nietzsche",
        "category": "Philosophy, Essays & Misc",
        "cover_url": "https://covers.openlibrary.org/b/id/119371-L.jpg"
    },
    "the-food-lab-better-home-cooking-through-science-unknown": {
        "title": "The Food Lab: Better Home Cooking Through Science",
        "author": "J. Kenji López-Alt",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/8314250-L.jpg"
    },
    "a-wrinkle-in-time-unknown": {
        "title": "A Wrinkle in Time",
        "author": "Madeleine L'Engle",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/8709146-L.jpg"
    },
    "maangchi-s-real-korean-cooking-unknown": {
        "title": "Maangchi's Real Korean Cooking",
        "author": "Maangchi",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/13135332-L.jpg"
    },
    "akira-unknown": {
        "title": "Akira, Vol. 1",
        "author": "Katsuhiro Otomo",
        "category": "Comics & Graphic Novels",
        "cover_url": "https://covers.openlibrary.org/b/id/814967-L.jpg"
    },
    "understanding-comics-the-invisible-art-scott-mccloud": {
        "title": "Understanding Comics: The Invisible Art",
        "author": "Scott McCloud",
        "category": "Comics & Graphic Novels",
        "cover_url": "https://covers.openlibrary.org/b/id/10679940-L.jpg"
    },
    "the-picture-of-dorian-gray-oscar-wilde": {
        "title": "The Picture of Dorian Gray",
        "author": "Oscar Wilde",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/14314858-L.jpg"
    },
    "six-pillars-of-self-esteem-nathaniel-branden": {
        "title": "Six Pillars of Self-Esteem",
        "author": "Nathaniel Branden",
        "category": "Philosophy, Essays & Misc",
        "cover_url": "https://covers.openlibrary.org/b/id/8354780-L.jpg"
    },
    "the-communist-manifesto-karl-marx-friedrich-engels": {
        "title": "The Communist Manifesto",
        "author": "Karl Marx & Friedrich Engels",
        "category": "Philosophy, Essays & Misc",
        "cover_url": "https://covers.openlibrary.org/b/id/11048623-L.jpg"
    },
    "the-ones-who-walk-away-from-omelas-ursula-k-le-guin": {
        "title": "The Ones Who Walk Away from Omelas",
        "author": "Ursula K. Le Guin",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/3993167-L.jpg"
    },
    "the-argumentative-indian-amartya-sen": {
        "title": "The Argumentative Indian",
        "author": "Amartya Sen",
        "category": "Philosophy, Essays & Misc",
        "cover_url": "https://covers.openlibrary.org/b/id/7946950-L.jpg"
    },
    "freakonomics-steven-d-levitt-stephen-j-dubner": {
        "title": "Freakonomics: A Rogue Economist Explores the Hidden Side of Everything",
        "author": "Steven D. Levitt & Stephen J. Dubner",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/11172914-L.jpg"
    },
    "principles-life-and-work-ray-dalio": {
        "title": "Principles: Life and Work",
        "author": "Ray Dalio",
        "category": "Marketing & Strategy",
        "cover_url": "https://covers.openlibrary.org/b/id/8315355-L.jpg"
    },
    "sophie-s-world-jostein-gaarder": {
        "title": "Sophie's World: A Novel About the History of Philosophy",
        "author": "Jostein Gaarder",
        "category": "Philosophy, Essays & Misc",
        "cover_url": "https://covers.openlibrary.org/b/id/10563354-L.jpg"
    },
    "the-7-deaths-of-evelyn-hardcastle-stuart-turton": {
        "title": "The 7½ Deaths of Evelyn Hardcastle",
        "author": "Stuart Turton",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/8838910-L.jpg"
    },
    "what-every-body-is-saying-joe-navarro": {
        "title": "What Every BODY Is Saying: An Ex-FBI Agent's Guide to Speed-Reading People",
        "author": "Joe Navarro",
        "category": "Philosophy, Essays & Misc",
        "cover_url": "https://covers.openlibrary.org/b/id/8734461-L.jpg"
    },
    "the-1-page-marketing-plan-allan-dib": {
        "title": "The 1-Page Marketing Plan: Get New Customers, Make More Money, And Stand Out From The Crowd",
        "author": "Allan Dib",
        "category": "Marketing & Strategy",
        "cover_url": "https://covers.openlibrary.org/b/id/10390028-L.jpg"
    },
    "all-tomorrows-cm-kosemen-unknown": {
        "title": "All Tomorrows: A Billion Year Chronicle of the Myriad Species and Mixed Fortunes of Man",
        "author": "C.M. Kösemen",
        "category": "Fiction & Non-Fiction",
        "cover_url": "https://covers.openlibrary.org/b/id/15137394-L.jpg"
    },

    # Screenplays & Movie Scripts (Render cleanly using bespoke typographic clothbound template jackets)
    "500-days-of-summer-2009-unknown": {
        "title": "(500) Days of Summer (Screenplay)",
        "author": "Scott Neustadter & Michael H. Weber",
        "category": "Screenplays",
        "cover_url": None,
        "no_cover": True
    },
    "arrival-2016-unknown": {
        "title": "Arrival (Screenplay)",
        "author": "Eric Heisserer (based on Ted Chiang)",
        "category": "Screenplays",
        "cover_url": None,
        "no_cover": True
    },
    "bong-joon-ho-parasite-script": {
        "title": "Parasite (기생충 Screenplay)",
        "author": "Bong Joon-ho & Han Jin-won",
        "category": "Screenplays",
        "cover_url": None,
        "no_cover": True
    },
    "everything-everywhere-all-at-once-2022-unknown": {
        "title": "Everything Everywhere All at Once (Screenplay)",
        "author": "Daniel Kwan & Daniel Scheinert (Daniels)",
        "category": "Screenplays",
        "cover_url": None,
        "no_cover": True
    },
    "get-out-2017-unknown": {
        "title": "Get Out (Screenplay)",
        "author": "Jordan Peele",
        "category": "Screenplays",
        "cover_url": None,
        "no_cover": True
    },
    "groundhogday-unknown": {
        "title": "Groundhog Day (Screenplay)",
        "author": "Danny Rubin & Harold Ramis",
        "category": "Screenplays",
        "cover_url": None,
        "no_cover": True
    },
    "jojo-rabbit-2019-unknown": {
        "title": "Jojo Rabbit (Screenplay)",
        "author": "Taika Waititi",
        "category": "Screenplays",
        "cover_url": None,
        "no_cover": True
    },
    "logan-2017-unknown": {
        "title": "Logan (Screenplay)",
        "author": "James Mangold, Scott Frank & Michael Green",
        "category": "Screenplays",
        "cover_url": None,
        "no_cover": True
    },
    "the-martian-2015-unknown": {
        "title": "The Martian (Screenplay)",
        "author": "Drew Goddard (dir. Ridley Scott)",
        "category": "Screenplays",
        "cover_url": None,
        "no_cover": True
    },
    "hwp-unknown": {
        "title": "Oldboy (올드보이 Screenplay)",
        "author": "Park Chan-wook, Hwang Jo-yun & Lim Joon-hyung",
        "category": "Screenplays",
        "cover_url": None,
        "no_cover": True
    },
    "fight-club-script-palahniuk-chuck": {
        "title": "Fight Club (Screenplay)",
        "author": "Jim Uhls (dir. David Fincher)",
        "category": "Screenplays",
        "cover_url": None,
        "no_cover": True
    },
    "dangal-movie-script-film-companion-unknown": {
        "title": "Dangal (Screenplay)",
        "author": "Nitesh Tiwari, Piyush Gupta, Shreyas Jain & Nikhil Mehrotra",
        "category": "Screenplays",
        "cover_url": None,
        "no_cover": True
    },
    "gangs-of-wasseypur-part-1-movie-script-film-companion-unknown": {
        "title": "Gangs of Wasseypur: Part 1 (Screenplay)",
        "author": "Anurag Kashyap, Zeishan Quadri, Akhilesh Jaiswal & Sachin Ladia",
        "category": "Screenplays",
        "cover_url": None,
        "no_cover": True
    },
    "masaan-movie-script-film-companion-unknown": {
        "title": "Masaan (Screenplay)",
        "author": "Varun Grover (dir. Neeraj Ghaywan)",
        "category": "Screenplays",
        "cover_url": None,
        "no_cover": True
    },
    "the-lunchbox-screenplay-film-companion-unknown": {
        "title": "The Lunchbox (Screenplay)",
        "author": "Ritesh Batra",
        "category": "Screenplays",
        "cover_url": None,
        "no_cover": True
    },
    "mark-ko-dard-nahi-hota-1-unknown": {
        "title": "Mard Ko Dard Nahi Hota (Screenplay)",
        "author": "Vasan Bala",
        "category": "Screenplays",
        "cover_url": None,
        "no_cover": True
    }
}

def build():
    if BOOKSHELF_DATA.exists():
        print(f"Loading pre-enriched data from {BOOKSHELF_DATA}...")
        shelf_books = json.loads(BOOKSHELF_DATA.read_text(encoding="utf-8"))

        # Load covers cache to backfill any missing covers
        covers_cache = json.loads(COVERS_CACHE_PATH.read_text(encoding="utf-8")) if COVERS_CACHE_PATH.exists() else {}

        # Apply in-memory fixes to guarantee accurate titles, authors, and covers
        for b in shelf_books:
            bid = b.get("id")
            if bid in MANUAL_BOOK_FIXES:
                for k, v in MANUAL_BOOK_FIXES[bid].items():
                    b[k] = v

            # If explicitly marked as having no cover or set to None in manual fixes, respect that decision
            if b.get("no_cover") or (bid in MANUAL_BOOK_FIXES and MANUAL_BOOK_FIXES[bid].get("cover_url") is None):
                b["cover_url"] = None
                b["no_cover"] = True
            elif not b.get("cover_url"):
                clean_t = re.sub(r"libgen\.li|libgen|\(20\d\d.*?\)|\{.*?\}", "", b.get("title", ""), flags=re.I).strip()
                clean_a = re.sub(r"libgen\.li|libgen|\(dir\..*?\)|Unknown", "", b.get("author", ""), flags=re.I).strip()
                cache_key = f"{clean_t}|{clean_a}"
                if cache_key in covers_cache and covers_cache[cache_key]:
                    b["cover_url"] = covers_cache[cache_key]

            # Ensure drive_id and direct_download_url are present for 1-click download
            durl = b.get("drive_url", "")
            fid = b.get("drive_id", "")
            if not fid and durl:
                if "id=" in durl:
                    fid = durl.split("id=")[-1].split("&")[0]
                elif "/file/d/" in durl:
                    fid = durl.split("/file/d/")[-1].split("/")[0]
            b["drive_id"] = fid
            b["direct_download_url"] = f"https://drive.usercontent.google.com/download?id={fid}&export=download" if fid else ""

        matched_quotes_books = len([b for b in shelf_books if b.get("has_quote_bank")])
        covers_count = len([b for b in shelf_books if b.get("cover_url")])
        print(f"Loaded {len(shelf_books)} books for My Reading Corner.")
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
  <meta name="theme-color" content="#C85A32">
  <link rel="manifest" href="manifest.json">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <meta name="apple-mobile-web-app-title" content="Reading Corner">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
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

    /* Editorial Card & Responsive Synopsis Clamp */
    .editorial-synopsis {{
      display: -webkit-box;
      -webkit-box-orient: vertical;
      overflow: hidden;
      text-overflow: ellipsis;
      -webkit-line-clamp: 6; /* mobile default */
    }}
    @media (min-width: 640px) {{
      .editorial-synopsis {{
        -webkit-line-clamp: 7;
      }}
    }}
    @media (min-width: 768px) {{
      .editorial-synopsis {{
        -webkit-line-clamp: 7;
      }}
    }}
    @media (min-width: 1024px) {{
      .editorial-synopsis {{
        -webkit-line-clamp: 9;
      }}
    }}
    @media (min-width: 1280px) {{
      .editorial-synopsis {{
        -webkit-line-clamp: 11;
      }}
    }}
    .editorial-synopsis.expanded {{
      display: block !important;
      -webkit-line-clamp: unset !important;
      overflow: visible !important;
    }}
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
            title="Spacious 2-column cards with full synopsis and curator note">
            <span>📰</span>
            <span class="hidden md:inline">Editorial</span>
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
          title="Surprise me with a random book"
          class="shrink-0 px-2.5 sm:px-3 py-1.5 bg-[var(--amber-bg)] text-[var(--terracotta)] border border-[var(--terracotta)]/30 hover:bg-[var(--terracotta)] hover:text-white rounded-xl text-xs font-bold transition flex items-center gap-1.5 shadow-sm">
          <span>✨</span>
          <span class="hidden lg:inline">Surprise Me</span>
          <span class="hidden sm:inline lg:hidden">Surprise</span>
        </button>

        <!-- Copy TBR -->
        <button 
          onclick="copyAllTbr()" 
          title="Copy clean list for TBR trackers ({len(tbr_lines)} books)"
          class="shrink-0 px-2.5 sm:px-3 py-1.5 bg-[var(--card-bg)] hover:bg-[var(--card-hover)] border border-[var(--border)] text-[var(--text-heading)] rounded-xl text-xs font-semibold transition flex items-center gap-1.5 shadow-sm">
          <span>📋</span>
          <span class="hidden lg:inline">Copy TBR ({len(tbr_lines)})</span>
          <span class="hidden sm:inline lg:hidden">TBR ({len(tbr_lines)})</span>
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

    <!-- 2. Editorial View (Refined 2-column cards with authentic back-cover synopsis: 4 visible on screen) -->
    <div id="editorialView" class="hidden">
      <div id="editorialGrid" class="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-7 lg:gap-8">
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
          <div class="flex flex-wrap items-center justify-between gap-2 mt-2 pt-1 border-t border-[var(--border-subtle)] text-[11px]">
            <div class="flex items-center gap-2.5 text-[var(--terracotta)] font-medium">
              <button type="button" onclick="searchGoodreads()" class="hover:underline flex items-center gap-1">🔎 Goodreads</button>
              <span>•</span>
              <button type="button" onclick="searchGoogleImages()" class="hover:underline flex items-center gap-1">🖼️ Google Images</button>
            </div>
            <button type="button" onclick="removeCoverAction()" class="px-2.5 py-1 text-red-600 dark:text-red-400 bg-red-500/10 hover:bg-red-500/20 rounded font-semibold text-[11px] transition flex items-center gap-1">
              <span>🗑️</span>
              <span>Remove Cover (Use Template Jacket)</span>
            </button>
          </div>
          <p class="text-[10px] text-[var(--text-muted)] mt-1.5 leading-tight">
            ✦ Removing cover applies an authentic typographic clothbound jacket featuring the book title and author, and remembers not to regenerate it.
          </p>
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
        SHELF_DATA = SHELF_DATA.map(b => {{
          if (overrides[b.id]) {{
            const ov = overrides[b.id];
            b = Object.assign(b, ov);
            if (ov.no_cover) {{
              b.cover_url = null;
              b.no_cover = true;
            }}
          }}
          return b;
        }});
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

    function renderTypographicJacket(b, extraClasses = "") {{
      const jacketCls = getJacketStyle(b.category || "");
      const authorDisplay = (b.author && b.author.trim() && b.author.toLowerCase() !== "unknown") 
        ? b.author 
        : "Unknown Author";

      return `
        <div class="typographic-jacket w-full h-full ${{jacketCls}} p-3 sm:p-4 flex flex-col justify-between relative overflow-hidden select-none rounded-[6px] shadow-inner ${{extraClasses}}">
          <!-- Spine hinge shadow on left edge -->
          <div class="absolute left-0 top-0 bottom-0 w-2.5 bg-gradient-to-r from-black/40 via-black/15 to-transparent pointer-events-none z-10"></div>
          <!-- Fine cloth weave highlight -->
          <div class="absolute inset-0 bg-gradient-to-b from-white/10 via-transparent to-black/25 pointer-events-none"></div>

          <!-- Top Header: Format & Star Badge -->
          <div class="relative z-10 flex items-center justify-between text-[9px] text-white/80 font-mono tracking-wider uppercase">
            <span class="bg-black/35 backdrop-blur-xs px-1.5 py-0.5 rounded font-bold">${{b.format || 'EPUB'}}</span>
            <span class="text-amber-300 text-xs drop-shadow-xs">✦</span>
          </div>

          <!-- Center Typography Frame: Refined Inset Card -->
          <div class="relative z-10 my-auto py-2.5 px-3 rounded-lg border border-white/20 bg-black/25 backdrop-blur-xs text-center shadow-inner">
            <h4 class="font-serif font-bold text-xs sm:text-sm md:text-base text-white leading-snug drop-shadow-sm line-clamp-3 sm:line-clamp-4">
              ${{b.title}}
            </h4>
            <div class="w-8 h-[1px] bg-amber-300/60 mx-auto my-2"></div>
            <p class="font-serif italic text-white/90 text-[10px] sm:text-xs truncate">
              by ${{authorDisplay}}
            </p>
          </div>

          <!-- Bottom Publisher Ornament -->
          <div class="relative z-10 flex items-center justify-between text-[8px] font-mono text-white/60 uppercase tracking-widest pt-1.5 border-t border-white/10">
            <span class="truncate max-w-[100px]">${{b.category || 'Reading Corner'}}</span>
            <span>EX LIBRIS</span>
          </div>
        </div>
      `;
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
        const hasCover = !!b.cover_url && !b.no_cover;
        const hook = extractFirstWhyReadHook(b.why_love);

        return `
          <div class="book-card group cursor-pointer relative" onclick="openBookDetail('${{b.id}}')">
            <!-- Book Cover -->
            <div class="book-cover ${{jacketCls}} relative overflow-hidden rounded-[8px] shadow-md transition-all duration-200 group-hover:shadow-2xl group-hover:-translate-y-1.5 aspect-[2/3]">
              ${{hasCover ? `
                <img src="${{b.cover_url}}" alt="${{b.title}}" loading="lazy" class="w-full h-full object-cover z-0" onerror="this.onerror=null;this.style.display='none';this.parentElement.querySelector('.fallback-jacket').style.display='block';" />
                <div class="absolute top-2 left-2 z-10 flex items-center gap-1.5">
                  <span class="text-[9px] font-mono uppercase tracking-wider text-white bg-black/60 backdrop-blur-xs px-1.5 py-0.5 rounded shadow-sm">
                    ${{b.format || 'EPUB'}}
                  </span>
                  ${{b.has_quote_bank ? `<span class="text-[9px] font-bold text-amber-950 bg-amber-300/95 backdrop-blur-xs px-1.5 py-0.5 rounded shadow-sm">★ Quotes</span>` : ''}}
                </div>
                <div class="fallback-jacket hidden absolute inset-0 z-0 w-full h-full">
                  ${{renderTypographicJacket(b)}}
                </div>
              ` : `
                ${{renderTypographicJacket(b)}}
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
                  <button onclick="openBookInNook(event, '${{b.id}}')" class="text-amber-300 font-bold hover:underline flex items-center gap-1">
                    <span>${{ (b.format && b.format.toLowerCase() === 'pdf') ? '📄 Open PDF ↗' : '📖 Read on Nooks ↗' }}</span>
                  </button>
                  <span class="text-white/80 font-semibold">Dossier →</span>
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

    // Render Editorial View (Refined 2-column cards with back-cover synopsis, zero clipping)
    function renderEditorial(books) {{
      const grid = document.getElementById("editorialGrid");
      if (books.length === 0) {{
        grid.innerHTML = `<div class="col-span-full py-20 text-center text-sm text-[var(--text-muted)]">No matching books found.</div>`;
        return;
      }}

      grid.innerHTML = books.map(b => {{
        const jacketCls = getJacketStyle(b.category);
        const hasCover = !!b.cover_url && !b.no_cover;

        return `
          <div class="editorial-card bg-[var(--card-bg)] border border-[var(--border)] hover:border-[var(--terracotta)]/40 rounded-2xl p-4 sm:p-5 md:p-6 flex flex-row gap-4 sm:gap-6 hover:shadow-lg transition-all duration-200 cursor-pointer group items-stretch overflow-hidden" onclick="openBookDetail('${{b.id}}')">
            <!-- Cover (Left: substantial horizontal real estate, perfectly proportioned, 4 cards visible on screen) -->
            <div class="w-32 sm:w-40 md:w-48 lg:w-56 shrink-0 aspect-[2/3] book-cover ${{jacketCls}} relative rounded-xl overflow-hidden shadow-sm border border-black/10 flex items-center justify-center bg-[var(--border-subtle)]/40 p-1 self-start">
              ${{hasCover ? `
                <img src="${{b.cover_url}}" alt="${{b.title}}" loading="lazy" class="w-full h-full object-contain drop-shadow-xs rounded-lg" onerror="this.onerror=null;this.style.display='none';this.parentElement.querySelector('.fallback-ed').style.display='block';" />
                <div class="fallback-ed hidden absolute inset-0 w-full h-full">
                  ${{renderTypographicJacket(b)}}
                </div>
              ` : `
                <div class="w-full h-full">
                  ${{renderTypographicJacket(b)}}
                </div>
              `}}
              <div class="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-r from-black/15 to-transparent pointer-events-none"></div>
            </div>

            <!-- Content (Right: Clean back-cover synopsis & 1-click Read) -->
            <div class="flex-1 min-w-0 flex flex-col justify-between py-0.5">
              <div>
                <div class="flex items-center justify-between gap-2 mb-1.5">
                  <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--terracotta)] truncate">${{b.category}}</span>
                  ${{b.has_quote_bank ? `<span class="text-[9px] font-bold text-amber-950 bg-amber-300/90 px-1.5 py-0.5 rounded shrink-0">★ ${{b.quotes.length}} Quotes</span>` : ''}}
                </div>
                <h3 class="font-serif font-bold text-base sm:text-lg md:text-xl text-[var(--text-heading)] group-hover:text-[var(--terracotta)] transition leading-snug line-clamp-2">
                  ${{b.title}}
                </h3>
                <p class="text-xs sm:text-[13px] text-[var(--text-muted)] font-medium mt-0.5 line-clamp-1">by ${{b.author}}</p>

                <!-- Back of the Book Synopsis (Spacious, Elegant & Readable) -->
                <p id="pitch-${{b.id}}" class="editorial-synopsis font-serif text-xs sm:text-[13px] md:text-sm text-[var(--text-heading)]/85 mt-2.5 leading-relaxed transition-all">
                  ${{b.pitch}}
                </p>
                ${{b.pitch && b.pitch.length > 280 ? `
                  <button type="button" onclick="toggleExpandPitch(event, '${{b.id}}')" class="expand-btn-${{b.id}} text-[11px] font-bold text-[var(--terracotta)] hover:underline mt-1.5 inline-flex items-center gap-1 select-none">
                    <span>Read full synopsis ↓</span>
                  </button>
                ` : ''}}
              </div>

              <!-- Bottom Row Action -->
              <div class="mt-auto pt-2.5 border-t border-[var(--border-subtle)] flex items-center justify-between gap-2 text-xs">
                <button onclick="openBookInNook(event, '${{b.id}}')" class="px-3.5 py-1.5 bg-[var(--terracotta)] hover:bg-[var(--terracotta-hover)] text-white text-xs font-bold rounded-lg shadow-xs transition flex items-center gap-1.5 shrink-0">
                  <span>${{ (b.format && b.format.toLowerCase() === 'pdf') ? '📄' : '📖' }}</span>
                  <span>${{ (b.format && b.format.toLowerCase() === 'pdf') ? 'Open PDF ↗' : 'Read on Nooks ↗' }}</span>
                </button>
                <span class="text-[var(--terracotta)] font-semibold flex items-center gap-1 group-hover:translate-x-0.5 transition-transform text-xs ml-auto">
                  Notes & Quotes →
                </span>
              </div>
            </div>
          </div>
        `;
      }}).join("");
    }}

    // Render Bookshelf Split View
        function toggleExpandPitch(event, bookId) {{
      if (event) {{
        event.stopPropagation();
        event.preventDefault();
      }}
      const p = document.getElementById(`pitch-${{bookId}}`);
      const btn = document.querySelector(`.expand-btn-${{bookId}}`);
      if (!p) return;

      const isExpanded = p.classList.contains("expanded");
      if (isExpanded) {{
        p.classList.remove("expanded");
        if (btn) btn.innerHTML = '<span>Read full synopsis ↓</span>';
      }} else {{
        p.classList.add("expanded");
        if (btn) btn.innerHTML = '<span>Show less ↑</span>';
      }}
    }}

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
              ${{b.cover_url && !b.no_cover ? `<img src="${{b.cover_url}}" class="w-full h-full object-cover" onerror="this.style.display='none';this.parentElement.querySelector('.fallback-thumb').style.display='block';" /><div class="fallback-thumb hidden w-full h-full">${{renderTypographicJacket(b, 'text-[6px] p-1')}}</div>` : `<div class="w-full h-full">${{renderTypographicJacket(b, 'text-[6px] p-1')}}</div>`}}
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
          <div class="w-36 md:w-48 shrink-0 aspect-[2/3] book-cover ${{jacketCls}} shadow-xl relative overflow-hidden rounded-[8px] bg-[var(--border-subtle)]/40 p-1">
            ${{b.cover_url && !b.no_cover ? `
              <img src="${{b.cover_url}}" alt="${{b.title}}" class="w-full h-full object-contain drop-shadow-xs rounded-lg" onerror="this.onerror=null;this.style.display='none';this.parentElement.querySelector('.fallback-hero').style.display='block';" />
              <div class="fallback-hero hidden absolute inset-0 z-10 w-full h-full">
                ${{renderTypographicJacket(b)}}
              </div>
            ` : `
              <div class="w-full h-full">
                ${{renderTypographicJacket(b)}}
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
              <button onclick="openBookInNook(event, '${{b.id}}')" class="px-4 py-2 bg-[var(--terracotta)] hover:bg-[var(--terracotta-hover)] text-white text-xs font-bold rounded-xl shadow-sm transition flex items-center gap-1.5 cursor-pointer">
                <span>📖</span>
                <span>Read in Nook ↗</span>
              </button>
              ${{b.drive_url ? `
                <a href="${{b.drive_url}}" target="_blank" rel="noopener noreferrer" class="px-3.5 py-2 bg-[var(--canvas)] border border-[var(--border)] hover:border-[var(--terracotta)] text-xs font-semibold text-[var(--text-heading)] rounded-xl transition flex items-center gap-1.5">
                  <span>📁</span>
                  <span>Drive File ↗</span>
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
              <button onclick="quickRemoveCover('${{b.id}}')" class="px-3.5 py-2 bg-[var(--canvas)] border border-[var(--border)] hover:border-red-400 text-xs font-semibold text-[var(--text-muted)] hover:text-red-500 rounded-xl transition flex items-center gap-1.5" title="Remove cover and use classic typographic template">
                <span>🗑️</span>
                <span>${{b.cover_url && !b.no_cover ? 'Remove Cover' : 'Jacket Active'}}</span>
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

    function openBookInNook(event, bookId) {{
      if (event) {{
        event.stopPropagation();
        event.preventDefault();
      }}
      const b = SHELF_DATA.find(item => item.id === bookId);
      if (!b) return;

      // If PDF, open directly or trigger direct download
      const isPdf = (b.format && b.format.toLowerCase() === 'pdf') || (b.title && b.title.toLowerCase().endsWith('.pdf'));
      if (isPdf) {{
        if (b.direct_download_url) {{
          window.open(b.direct_download_url, '_blank');
          showToast(`Opening PDF download for "${{b.title}}"...`);
        }} else if (b.drive_url) {{
          window.open(b.drive_url, '_blank');
        }}
        return;
      }}

      // Open Nooks reader directly without unexpected auto-downloading
      const readerUrl = `./reader.html?id=${{encodeURIComponent(b.id)}}&title=${{encodeURIComponent(b.title)}}&author=${{encodeURIComponent(b.author)}}&drive_id=${{encodeURIComponent(b.drive_id || '')}}&drive=${{encodeURIComponent(b.drive_url || '')}}`;
      window.open(readerUrl, "_blank");
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
          <div class="w-28 shrink-0 aspect-[2/3] book-cover ${{jacketCls}} shadow-md relative overflow-hidden rounded-[8px] bg-[var(--border-subtle)]/40 p-1">
            ${{b.cover_url && !b.no_cover ? `
              <img src="${{b.cover_url}}" alt="${{b.title}}" class="w-full h-full object-contain drop-shadow-xs rounded-lg" onerror="this.onerror=null;this.style.display='none';this.parentElement.querySelector('.fallback-drawer').style.display='block';" />
              <div class="fallback-drawer hidden absolute inset-0 z-10 w-full h-full">
                ${{renderTypographicJacket(b)}}
              </div>
            ` : `
              <div class="w-full h-full">
                ${{renderTypographicJacket(b)}}
              </div>
            `}}
          </div>
          <div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--terracotta)]">${{b.category}}</span>
            <h3 class="font-serif font-bold text-lg text-[var(--text-heading)] mt-0.5 leading-snug">${{b.title}}</h3>
            <p class="text-xs text-[var(--text-muted)] font-medium">by ${{b.author}}</p>
            <div class="flex flex-wrap items-center gap-2 mt-3">
              <button onclick="openBookInNook(event, '${{b.id}}')" class="px-3 py-1.5 bg-[var(--terracotta)] hover:bg-[var(--terracotta-hover)] text-white text-xs font-bold rounded-lg shadow-sm transition flex items-center gap-1.5 cursor-pointer">
                <span>📖</span>
                <span>Read in Nook ↗</span>
              </button>
              ${{b.drive_url ? `
                <a href="${{b.drive_url}}" target="_blank" rel="noopener noreferrer" class="px-3 py-1.5 bg-[var(--canvas)] border border-[var(--border)] text-xs font-semibold rounded-lg">
                  Drive File ↗
                </a>
              ` : ''}}
              <button onclick="copySingleTbr('${{b.title.replace(/'/g, "\\\\\\'")}}', '${{b.author.replace(/'/g, "\\\\\\'")}}')" class="px-3 py-1.5 bg-[var(--canvas)] border border-[var(--border)] text-xs font-semibold rounded-lg">Copy TBR</button>
              <button onclick="openEditModal('${{b.id}}')" class="px-3 py-1.5 bg-[var(--canvas)] border border-[var(--border)] text-xs font-semibold text-[var(--text-muted)] hover:text-[var(--text-heading)] rounded-lg">Edit</button>
              <button onclick="quickRemoveCover('${{b.id}}')" class="px-3 py-1.5 bg-[var(--canvas)] border border-[var(--border)] hover:border-red-400 text-xs font-semibold text-[var(--text-muted)] hover:text-red-500 rounded-lg">
                ${{b.cover_url && !b.no_cover ? 'Remove Cover' : 'Jacket Active'}}
              </button>
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
          <div class="w-28 md:w-32 shrink-0 aspect-[2/3] book-cover ${{jacketCls}} shadow-md relative overflow-hidden rounded-[8px] bg-[var(--border-subtle)]/40 p-1">
            ${{chosen.cover_url && !chosen.no_cover ? `<img src="${{chosen.cover_url}}" class="w-full h-full object-contain drop-shadow-xs rounded-lg" onerror="this.onerror=null;this.style.display='none';this.parentElement.querySelector('.fallback-surprise').style.display='block';" /><div class="fallback-surprise hidden absolute inset-0 z-10 w-full h-full">${{renderTypographicJacket(chosen)}}</div>` : `<div class="w-full h-full">${{renderTypographicJacket(chosen)}}</div>`}}
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
      document.getElementById("editAuthor").value = b.author || "";
      document.getElementById("editCoverUrl").value = b.no_cover ? "" : (b.cover_url || "");
      document.getElementById("editPitch").value = b.pitch || "";
      document.getElementById("editWhyLove").value = b.why_love || "";

      document.getElementById("editModal").classList.remove("hidden");
    }}

    function closeEditModal() {{
      document.getElementById("editModal").classList.add("hidden");
    }}

    function removeCoverAction() {{
      document.getElementById("editCoverUrl").value = "";
      showToast("Cover cleared. Tap 'Save Changes' to apply the typographic template jacket!");
    }}

    function quickRemoveCover(bookId) {{
      const b = SHELF_DATA.find(item => item.id === bookId);
      if (!b) return;

      if (!b.no_cover && b.cover_url) {{
        b.cover_url = null;
        b.no_cover = true;
        showToast(`Cover removed for "${{b.title}}"! Applied typographic template jacket.`);
      }} else {{
        b.no_cover = false;
        showToast(`Template jacket active for "${{b.title}}". Use Edit to paste a cover URL if desired.`);
      }}

      // Persist to localStorage
      let saved = {{}};
      try {{ saved = JSON.parse(localStorage.getItem("exlibris_shelf_edits") || "{{}}"); }} catch (e) {{}}
      saved[b.id] = Object.assign(saved[b.id] || {{}}, {{
        title: b.title,
        author: b.author,
        cover_url: b.cover_url,
        no_cover: b.no_cover
      }});
      localStorage.setItem("exlibris_shelf_edits", JSON.stringify(saved));

      renderCurrentView();
      if (activeView === "split" && selectedBookId === b.id) {{
        selectBookForSplit(b.id);
      }}
    }}

    function saveEdit() {{
      const bookId = document.getElementById("editBookId").value;
      const b = SHELF_DATA.find(item => item.id === bookId);
      if (!b) return;

      b.title = document.getElementById("editTitle").value.trim() || b.title;
      b.author = document.getElementById("editAuthor").value.trim() || "Unknown Author";
      const newCover = document.getElementById("editCoverUrl").value.trim();

      if (!newCover) {{
        b.cover_url = null;
        b.no_cover = true;
      }} else {{
        b.cover_url = newCover;
        b.no_cover = false;
      }}

      b.pitch = document.getElementById("editPitch").value.trim();
      b.why_love = document.getElementById("editWhyLove").value.trim();

      // Persist to localStorage
      let saved = {{}};
      try {{ saved = JSON.parse(localStorage.getItem("exlibris_shelf_edits") || "{{}}"); }} catch (e) {{}}
      saved[b.id] = {{
        title: b.title,
        author: b.author,
        cover_url: b.cover_url,
        no_cover: b.no_cover,
        pitch: b.pitch,
        why_love: b.why_love
      }};
      localStorage.setItem("exlibris_shelf_edits", JSON.stringify(saved));

      closeEditModal();
      renderCurrentView();
      if (activeView === "split" && selectedBookId === b.id) {{
        selectBookForSplit(b.id);
      }}
      showToast(b.cover_url ? `Updated "${{b.title}}" and saved changes!` : `Saved "${{b.title}}" with typographic template jacket!`);
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

    // Register Service Worker for PWA
    if ('serviceWorker' in navigator) {{
      window.addEventListener('load', () => {{
        navigator.serviceWorker.register('./sw.js').catch(() => {{}});
      }});
    }}
  </script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
