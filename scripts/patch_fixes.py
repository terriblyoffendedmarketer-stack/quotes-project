# patch_fixes.py — Injects comprehensive manual book fixes and reader improvements into build script
import json, re
from pathlib import Path

BUILD_SCRIPT = Path('scripts/build_independent_bookshelf_app.py')
code = BUILD_SCRIPT.read_text(encoding='utf-8')

# 1. Update openBookInNook to handle PDF and reuse single tab
old_open_nook = """    function openBookInNook(event, bookId) {{
      if (event) {{
        event.stopPropagation();
        event.preventDefault();
      }}
      const b = SHELF_DATA.find(item => item.id === bookId);
      if (!b) return;

      // 1. Direct background download from Google Drive
      if (b.drive_id) {{
        const directDownloadUrl = `https://drive.usercontent.google.com/download?id=${{b.drive_id}}&export=download`;
        const a = document.createElement("a");
        a.href = directDownloadUrl;
        a.download = `${{b.title}}.epub`;
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        document.body.appendChild(a);
        a.click();
        setTimeout(() => a.remove(), 1000);
      }}

      // 2. Open reader in a new browser tab (keeps PWA intact, launches Chrome/Safari tab on mobile)
      const readerUrl = `./reader.html?id=${{encodeURIComponent(b.id)}}&title=${{encodeURIComponent(b.title)}}&author=${{encodeURIComponent(b.author)}}&drive_id=${{encodeURIComponent(b.drive_id || '')}}&drive=${{encodeURIComponent(b.drive_url || '')}}`;
      window.open(readerUrl, "_blank", "noopener,noreferrer");
    }}"""

new_open_nook = """    function openBookInNook(event, bookId) {{
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

      // 1. Direct background download from Google Drive
      if (b.drive_id) {{
        const directDownloadUrl = `https://drive.usercontent.google.com/download?id=${{b.drive_id}}&export=download`;
        const a = document.createElement("a");
        a.href = directDownloadUrl;
        a.download = `${{b.title}}.epub`;
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        document.body.appendChild(a);
        a.click();
        setTimeout(() => a.remove(), 1000);
      }}

      // 2. Open reader in a single named browser tab (reuses the exact same tab so it doesn't open multiple tabs)
      const readerUrl = `./reader.html?id=${{encodeURIComponent(b.id)}}&title=${{encodeURIComponent(b.title)}}&author=${{encodeURIComponent(b.author)}}&drive_id=${{encodeURIComponent(b.drive_id || '')}}&drive=${{encodeURIComponent(b.drive_url || '')}}`;
      window.open(readerUrl, "MyReadingNookTab");
    }}"""

if old_open_nook in code:
    code = code.replace(old_open_nook, new_open_nook)
    print("Replaced openBookInNook")
else:
    print("Warning: old_open_nook snippet not matched exactly")

# 2. Add comprehensive MANUAL_BOOK_FIXES dict
fixes_dict_str = '''MANUAL_BOOK_FIXES = {
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
        "title": "\'Salem\'s Lot",
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
}'''

# Replace MANUAL_BOOK_FIXES in code
start_idx = code.find('MANUAL_BOOK_FIXES = {')
end_idx = code.find('def build():', start_idx)
assert start_idx != -1 and end_idx != -1, "Could not find bounds of MANUAL_BOOK_FIXES"

code = code[:start_idx] + fixes_dict_str + '\n\n' + code[end_idx:]

# Ensure build() updates BOOKSHELF_DATA on disk too
persist_hook = '''        # Persist the cleaned in-memory fixes back to bookshelf/data.json
        BOOKSHELF_DATA.write_text(json.dumps(shelf_books, indent=2, ensure_ascii=False), encoding="utf-8")
'''
if "BOOKSHELF_DATA.write_text" not in code:
    code = code.replace('clean_tbr_lines = [f"{b[\'title\']} — {b[\'author\']}" for b in shelf_books]',
                        persist_hook + '        clean_tbr_lines = [f"{b[\'title\']} — {b[\'author\']}" for b in shelf_books]')

BUILD_SCRIPT.write_text(code, encoding='utf-8')
print("Successfully updated scripts/build_independent_bookshelf_app.py")

# 3. Dynamic button labels for PDF vs EPUB
code = BUILD_SCRIPT.read_text(encoding='utf-8')

code = code.replace(
    '<span>📖 Read ↗</span>',
    "<span>${{ (b.format && b.format.toLowerCase() === 'pdf') ? '📄 Open PDF ↗' : '📖 Read on Nooks ↗' }}</span>"
)

code = code.replace(
    """                <button onclick="openBookInNook(event, '${{b.id}}')" class="px-3.5 py-1.5 bg-[var(--terracotta)] hover:bg-[var(--terracotta-hover)] text-white text-xs font-bold rounded-lg shadow-xs transition flex items-center gap-1.5 shrink-0">
                  <span>📖</span>
                  <span>Read in Nook ↗</span>
                </button>""",
    """                <button onclick="openBookInNook(event, '${{b.id}}')" class="px-3.5 py-1.5 bg-[var(--terracotta)] hover:bg-[var(--terracotta-hover)] text-white text-xs font-bold rounded-lg shadow-xs transition flex items-center gap-1.5 shrink-0">
                  <span>${{ (b.format && b.format.toLowerCase() === 'pdf') ? '📄' : '📖' }}</span>
                  <span>${{ (b.format && b.format.toLowerCase() === 'pdf') ? 'Open PDF ↗' : 'Read on Nooks ↗' }}</span>
                </button>"""
)

code = code.replace(
    '<span>📖 Read in Nook ↗</span>',
    "<span>${{ (b.format && b.format.toLowerCase() === 'pdf') ? '📄 Open PDF ↗' : '📖 Read on Nooks ↗' }}</span>"
)

BUILD_SCRIPT.write_text(code, encoding='utf-8')
print("Successfully appended button label replacements")

# 4. Add Watchmen, Sandman, and Comic fixes
code = BUILD_SCRIPT.read_text(encoding='utf-8')

extra_fixes = '''    # Graphic Novels & Comics Verified (OpenLibrary & Amazon Edition Sources)
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
'''

if '"watchmen-complete":' not in code:
    code = code.replace('MANUAL_BOOK_FIXES = {', 'MANUAL_BOOK_FIXES = {\n' + extra_fixes)
    BUILD_SCRIPT.write_text(code, encoding='utf-8')
    print("Added Watchmen, Sandman Deluxe, and Graphic Novel fixes")
else:
    print("Watchmen already in MANUAL_BOOK_FIXES")
