# scripts/fetch_covers_and_enhance_content.py — Fetches real book covers and injects voice-driven editorial pitches
# Usage: python3 scripts/fetch_covers_and_enhance_content.py
# Requires: content/books_curated_shelf.json, content/quote-bank.json, python3 standard library
#
# Gotchas:
# - OpenLibrary search API can time out on obscure titles; fall back gracefully to aesthetic SVG jackets.
# - Cache covers to disk in content/covers_cache.json so we never repeat network requests.
# - High-conviction 'fun' reading pool filters out dry academic texts for the 'Surprise Me' feature.

import json
import urllib.request
import urllib.parse
import concurrent.futures
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHELF_JSON = ROOT / "content" / "books_curated_shelf.json"
COVERS_CACHE_FILE = ROOT / "content" / "covers_cache.json"
QUOTE_BANK_FILE = ROOT / "content" / "quote-bank.json"

# Load existing cache if present
if COVERS_CACHE_FILE.exists():
    try:
        COVERS_CACHE = json.loads(COVERS_CACHE_FILE.read_text(encoding="utf-8"))
    except Exception:
        COVERS_CACHE = {}
else:
    COVERS_CACHE = {}

def get_cover_url(title, author):
    cache_key = f"{title.lower()}---{author.lower()}"
    if cache_key in COVERS_CACHE:
        return COVERS_CACHE[cache_key]

    if author and author.lower() != "unknown":
        q_params = {"title": title, "author": author, "limit": 1}
    else:
        q_params = {"title": title, "limit": 1}
        
    url = "https://openlibrary.org/search.json?" + urllib.parse.urlencode(q_params)
    req = urllib.request.Request(url, headers={"User-Agent": "MarginaliaPersonalShelf/2.0"})
    
    cover_url = None
    try:
        with urllib.request.urlopen(req, timeout=3.5) as res:
            data = json.loads(res.read().decode())
            if data.get("docs"):
                doc = data["docs"][0]
                cid = doc.get("cover_i")
                if cid:
                    cover_url = f"https://covers.openlibrary.org/b/id/{cid}-L.jpg"
                elif doc.get("isbn"):
                    isbns = doc["isbn"]
                    cover_url = f"https://covers.openlibrary.org/b/isbn/{isbns[0]}-L.jpg"
    except Exception:
        pass

    COVERS_CACHE[cache_key] = cover_url
    return cover_url

# Known editorial pitches for prominent works (vivid, voice-driven, craft-focused)
RICH_EDITORIAL_PITCHES = {
    "heartburn": (
        "Rachel Samstat is seven months pregnant, a brilliant food writer whose life unravels when she discovers her husband is hopelessly in love with another woman. Instead of collapsing into self-pity, she weaponizes humor, serving up a hilarious, vindictive, and recipe-laced post-mortem on fidelity.",
        "Ephron's ultimate craft lesson: turning gut-wrenching personal betrayal into comedic gold. You will laugh out loud while marveling at how sentences can turn agony into survival."
    ),
    "slaughterhouse-five": (
        "Billy Pilgrim has become unstuck in time. He travels between the horrific firebombing of Dresden in 1945, his suburban optometrist practice in Ilium, New York, and a geodesic dome in a zoo on the distant planet Tralfamadore, where time exists all at once.",
        "Vonnegut's anti-war masterpiece that treats unimaginable historical trauma with shrugs of grim fatalism ('So it goes') and tender, tragic irony. Effortlessly readable and impossible to forget."
    ),
    "norwegian-wood": (
        "Toru Watanabe hears the Beatles' 'Norwegian Wood' while landing at Hamburg airport, triggering a flood of bittersweet memory: his Tokyo college days in the late 1960s, caught between the quiet, grief-haunted Naoko and the impulsive, life-hungry Midori.",
        "Murakami stripped of his signature magical cats and wells—pure, aching intimacy about youth, suicide, and the quiet horror of surviving people you love."
    ),
    "on-writing": (
        "Part visceral childhood memoir, part unapologetic masterclass. King strips away literary pretension to show the raw nuts and bolts of narrative: clearing out adverbs, building a toolbox, and writing with the door shut.",
        "The single most practical, non-academic book on storytelling ever written. King treats writing not as high art, but as honest, muscular carpentry."
    ),
    "consider-this": (
        "Palahniuk shares thirty years of storytelling wisdom picked up in workshops with Tom Spanbauer and Ken Kesey. He breaks down chorus refrains, unpacking visceral physical textures, and killing 'thought' verbs (thinks, knows, realizes) to force readers directly into the bone and muscle of a scene.",
        "Electrifying, punchy, and wildly unconventional. You'll never write or read a sentence the same way again."
    ),
    "stories-of-your-life-and-others": (
        "A linguist tasked with communicating with seven-limbed extraterrestrials begins perceiving time non-linearly, experiencing her unborn daughter's birth and future death simultaneously. Eight stories of peerless intellectual wonder.",
        "Ted Chiang doesn't write sci-fi for spaceship dogfights; he explores what happens when a mind-bending mathematical or philosophical premise collides with devastating human grief."
    ),
    "the-stranger": (
        "In colonial Algiers, Meursault buries his mother without weeping, swims with a lover, and shoots an Arab on a blinding, sun-drenched beach for reasons he can barely articulate. Put on trial, society judges him not for murder, but for his refusal to feign acceptable emotional grief.",
        "Camus's flat, unforgettable prose style delivers the ultimate existential cold-shower: life has no inherent meaning, which is precisely why freedom feels so terrifying."
    ),
    "the-metamorphosis": (
        "One morning, waking from troubled dreams, traveling salesman Gregor Samsa finds himself transformed into a monstrous vermin. His immediate, catastrophic panic? Not the alien carapace or twitching legs, but the horrifying realization that he is going to be late for the 7 o'clock train to work.",
        "The impossible stated with bureaucratic flat-footedness. Kafka turns modern workplace dread, familial resentment, and alienating guilt into the definitive myth of the 20th century."
    ),
    "dungeon-crawler-carl": (
        "When Earth's surface is abruptly collapsed by galactic corporations into an 18-level underground reality TV dungeon crawl, Carl (caught wearing only boxers and pink crocs) and his ex-girlfriend's pampered Persian cat Princess Donut must fight for survival in front of a universe of paying subscribers.",
        "Pure, unadulterated narrative cocaine. Deceptively absurd on the surface, beneath the explosive chaos lies genuine emotional stakes, razor-sharp satire of late-stage capitalism, and unbelievable pacing."
    ),
    "dark-matter": (
        "Jason Dessen is walking home to his wife and teenage son in Chicago when he is abducted at gunpoint, knocked unconscious, and wakes up in a laboratory surrounded by strangers applauding his breakthrough. In this world, his wife is not his wife, his son was never born, and he chose solitary quantum research over family.",
        "A pulse-pounding, high-concept quantum thriller that moves at breakneck speed while asking an agonizing question: which life would you kill to return to?"
    ),
    "project-hail-mary": (
        "Ryland Grace wakes up on an interstellar vessel with zero memory of his name, surrounded by dead crewmates, with only computer monitors and rudimentary lab equipment to piece together why he is here: an extinction-level microbe is eating the Sun.",
        "An irresistible celebration of human ingenuity, optimistic problem-solving, and the single greatest interspecies friendship in contemporary science fiction."
    ),
    "sculpting-in-time": (
        "The visionary Soviet director of Stalker and Solaris meditates on the sacred essence of cinema. He rejects montage-as-ideology, arguing that filmmaking is uniquely the direct mechanical imprint of lived, spiritual time.",
        "Deeply poetic and aesthetically uncompromising. A sacred text for anyone who cares about visual atmosphere, pacing, and human mystery."
    ),
    "in-the-blink-of-an-eye": (
        "The Oscar-winning editor of Apocalypse Now and The Godfather reveals how the mechanics of film editing mirror human cognitive blinks and emotional rhythm.",
        "Short, poetic, and utterly eye-opening. Murch makes you realize that every cut is an emotional dialogue between the storyteller and the viewer's subconscious."
    ),
    "into-the-woods": (
        "John Yorke deconstructs five-act storytelling structure across fairy tales, Shakespeare, cinema, and box-set television, revealing why the human brain naturally arranges conflict into an archetypal journey into the dark forest.",
        "The structural blueprint of narrative psychology. Demolishes formulaic beat-sheet dogmas and reveals why stories work on a neural level."
    ),
    "feline-philosophy": (
        "Humans spend centuries inventing tortured philosophical systems, religious anxieties, and political doctrines to distract themselves from mortality. Cats, by contrast, possess an effortless, contented tranquility without ever needing a purpose.",
        "John Gray at his wittiest and most incisive. A delightful, razor-sharp antidote to modern human anxiety and existential posturing."
    ),
    "four-thousand-weeks": (
        "Assuming you live to be eighty, you have roughly four thousand weeks on Earth. Burkeman exposes the tragic delusion of modern time-management: clearing your inbox and maximizing productivity only invites more demands, trapping you in an infinite conveyor belt of busyness.",
        "A liberating, comforting philosophical punch in the gut. Instead of cheering you on to do more, it teaches you how to surrender the impossible and embrace the finite beauty of being human."
    ),
    "the-sandman-complete": (
        "Morpheus, the Lord of Dreams and one of the seven Endless, is captured in an occult ritual and imprisoned for seventy years. Upon escaping into the 20th century, he must rebuild his crumbling kingdom and confront the tragic rigidity of his own ancient nature.",
        "The crown jewel of literary graphic storytelling. Gaiman weaves Shakespeare, world mythologies, historical grief, and human sorrow into an unforgettable epic."
    ),
    "watchmen": (
        "In an alternate 1985 America where Nixon is in his third term and nuclear tensions are minutes from midnight, the murder of a government-sanctioned vigilante draws a fractured group of retired, deeply broken masked heroes into a staggering conspiracy.",
        "The definitive masterpiece that exploded superhero myth into Cold War dread, moral nihilism, and architectural narrative perfection."
    )
}

def is_fun_reading_pick(book):
    cat = book["category"]
    tags = [t.lower() for t in book.get("tags", [])]
    author = book["author"].lower()
    title = book["title"].lower()

    # Fiction and literary fiction are always fun
    if cat in ["Fiction & Non-Fiction", "Comics & Graphic Novels", "Screenplays"]:
        # Exclude dry political tracts or study guides
        if any(w in title for w in ["study guide", "outline of philosophy", "science of logic", "dialectical materialism"]):
            return False
        return True

    # Non-fiction by fiction authors
    fiction_authors = [
        "stephen king", "chuck palahniuk", "haruki murakami", "kurt vonnegut", "ted chiang",
        "umberto eco", "george saunders", "ursula k. le guin", "annie dillard", "anne lamott",
        "joan didion", "james baldwin", "david foster wallace", "etgar keret", "raymond carver",
        "virginia woolf", "george orwell", "neil gaiman", "alan moore"
    ]
    if any(fa in author for fa in fiction_authors):
        return True

    # Engaging art, cinema, and accessible philosophy
    fun_authors = ["andrei tarkovsky", "walter murch", "john yorke", "blake snyder", "alain de botton", "john gray", "slavoj zizek", "oliver burkeman"]
    if any(fa in author for fa in fun_authors):
        return True

    return False

def enhance_shelf():
    print("Loading books shelf...")
    with open(SHELF_JSON) as f:
        shelf = json.load(f)

    # 1. Fetch covers with high concurrency
    print(f"Resolving cover images for {len(shelf)} books...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        future_to_book = {executor.submit(get_cover_url, b["title"], b["author"]): b for b in shelf}
        for future in concurrent.futures.as_completed(future_to_book):
            b = future_to_book[future]
            try:
                cov = future.result()
                if cov:
                    b["cover_url"] = cov
            except Exception:
                pass

    # Save covers cache
    COVERS_CACHE_FILE.write_text(json.dumps(COVERS_CACHE, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated covers cache ({len(COVERS_CACHE)} entries cached).")

    # 2. Inject rich editorial pitches and fun reading flags
    fun_count = 0
    for b in shelf:
        t_slug = b["title"].lower().replace(" ", "-").replace(":", "").replace("'", "")
        # Check custom rich editorial pitches
        for rk, (rpitch, rwhy) in RICH_EDITORIAL_PITCHES.items():
            if rk in t_slug:
                b["pitch"] = rpitch
                b["why_love"] = rwhy
                break

        # If book has quotes from Marginalia quote bank, ensure the synopsis is substantive
        if b.get("has_quote_bank") and b.get("quotes"):
            sample_exp = b["quotes"][0].get("explanation", "")
            if sample_exp and (not b.get("pitch") or len(b.get("pitch", "")) < 80):
                paras = sample_exp.split("\n\n")
                b["pitch"] = paras[0]
                if len(paras) > 1 and (not b.get("why_love") or len(b.get("why_love", "")) < 50):
                    b["why_love"] = paras[1][:240] + "..."

        # Tag if eligible for 'Surprise Me'
        b["is_fun_pick"] = is_fun_reading_pick(b)
        if b["is_fun_pick"]:
            fun_count += 1

    print(f"Flagged {fun_count} high-conviction fun/literary reading picks for Surprise Me.")

    # Save enhanced shelf JSON
    SHELF_JSON.write_text(json.dumps(shelf, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Enhanced books curated shelf written.")

if __name__ == "__main__":
    enhance_shelf()
