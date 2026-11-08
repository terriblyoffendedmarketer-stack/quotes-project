# scripts/audit_and_tag_categories.py — Audits and fixes inverted title/author metadata and tags curated categories
# Usage: python3 scripts/audit_and_tag_categories.py
# Requires: Python 3.8+ (standard library only)
#
# Gotchas:
# - In Google Drive, files formatted as 'Author - Title.epub' were naively parsed by older scripts as title=tokens[0], author=tokens[1].
# - Multi-category assignment allows books to be tagged with "Short Stories", "Essays", or "Literary Non-Fiction" while preserving their root category.
# - Always update both bookshelf/data.json and build_independent_bookshelf_app.py so builds are reproducible.

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "bookshelf" / "data.json"

# Complete verified dictionary of swapped title and author entries
SWAPPED_FIXES = {
    "neal-stephenson-snow-crash": {
        "title": "Snow Crash",
        "author": "Neal Stephenson"
    },
    "neal-stephenson-cryptonomicon": {
        "title": "Cryptonomicon",
        "author": "Neal Stephenson"
    },
    "neal-stephenson-seveneves": {
        "title": "Seveneves",
        "author": "Neal Stephenson"
    },
    "andy-weir-project-hail-mary": {
        "title": "Project Hail Mary",
        "author": "Andy Weir"
    },
    "blake-crouch-dark-matter": {
        "title": "Dark Matter",
        "author": "Blake Crouch"
    },
    "david-foster-wallace-infinite-jest": {
        "title": "Infinite Jest",
        "author": "David Foster Wallace"
    },
    "ernest-hemingway-short-stories": {
        "title": "The Short Stories of Ernest Hemingway",
        "author": "Ernest Hemingway"
    },
    "cixin-liu-the-wandering-earth": {
        "title": "The Wandering Earth",
        "author": "Cixin Liu"
    },
    "banana-yoshimoto-kitchen": {
        "title": "Kitchen",
        "author": "Banana Yoshimoto"
    },
    "arundhati-roy-the-god-of-small-things": {
        "title": "The God of Small Things",
        "author": "Arundhati Roy"
    },
    "brandon-sanderson-the-bands-of-mourning": {
        "title": "The Bands of Mourning",
        "author": "Brandon Sanderson"
    },
    "brandon-sanderson-shadows-of-self": {
        "title": "Shadows of Self",
        "author": "Brandon Sanderson"
    },
    "brandon-sanderson-the-alloy-of-law": {
        "title": "The Alloy of Law",
        "author": "Brandon Sanderson"
    },
    "brandon-sanderson-the-hero-of-ages": {
        "title": "The Hero of Ages",
        "author": "Brandon Sanderson"
    },
    "brandon-sanderson-the-well-of-ascension": {
        "title": "The Well of Ascension",
        "author": "Brandon Sanderson"
    },
    "brandon-sanderson-the-final-empire": {
        "title": "The Final Empire",
        "author": "Brandon Sanderson"
    },
    "brandon-sanderson-secret-history": {
        "title": "Mistborn: Secret History",
        "author": "Brandon Sanderson"
    },
    "carl-jung-the-development-of-personality": {
        "title": "The Development of Personality",
        "author": "Carl Jung"
    },
    "carl-jung-man-and-his-symbols": {
        "title": "Man and His Symbols",
        "author": "Carl Jung"
    },
    "carl-jung-memories-dreams-reflections": {
        "title": "Memories, Dreams, Reflections",
        "author": "Carl Jung"
    },
    "chris-voss-never-split-the-difference": {
        "title": "Never Split the Difference",
        "author": "Chris Voss"
    },
    "constance-hale-sin-and-syntax": {
        "title": "Sin and Syntax",
        "author": "Constance Hale"
    },
    "daryl-fielding-the-brand-book": {
        "title": "The Brand Book",
        "author": "Daryl Fielding"
    },
    "dean-koontz-intensity": {
        "title": "Intensity",
        "author": "Dean Koontz"
    },
    "dean-koontz-odd-thomas": {
        "title": "Odd Thomas",
        "author": "Dean Koontz"
    },
    "dean-r-koontz-watchers": {
        "title": "Watchers",
        "author": "Dean Koontz"
    },
    "derren-brown-confessions-of-a-conjuror": {
        "title": "Confessions of a Conjuror",
        "author": "Derren Brown"
    },
    "etgar-keret-the-bus-driver-who-wanted-to-be-god": {
        "title": "The Bus Driver Who Wanted to Be God",
        "author": "Etgar Keret"
    },
    "etgar-keret-the-seven-good-years": {
        "title": "The Seven Good Years",
        "author": "Etgar Keret"
    },
    "exurb1a-the-fifth-science": {
        "title": "The Fifth Science",
        "author": "Exurb1a"
    },
    "geoffrey-moore-crossing-the-chasm": {
        "title": "Crossing the Chasm",
        "author": "Geoffrey Moore"
    },
    "hannah-arendt-eichmann-in-jerusalem-a-report-on-the-banality-of-evil": {
        "title": "Eichmann in Jerusalem: A Report on the Banality of Evil",
        "author": "Hannah Arendt"
    },
    "herman-hesse-siddhartha": {
        "title": "Siddhartha",
        "author": "Hermann Hesse"
    },
    "isaac-asimov-asimov-s-mysteries": {
        "title": "Asimov's Mysteries",
        "author": "Isaac Asimov"
    },
    "issac-asimov-foundation": {
        "title": "Foundation",
        "author": "Isaac Asimov"
    },
    "james-gleick-chaos-making-a-new-science": {
        "title": "Chaos: Making a New Science",
        "author": "James Gleick"
    },
    "jared-diamond-guns-germs-and-steel": {
        "title": "Guns, Germs, and Steel",
        "author": "Jared Diamond"
    },
    "jay-heinrichs-thank-you-for-arguing": {
        "title": "Thank You for Arguing",
        "author": "Jay Heinrichs"
    },
    "jennifer-burns-goddess-of-the-market": {
        "title": "Goddess of the Market: Ayn Rand and the American Right",
        "author": "Jennifer Burns"
    },
    "joe-abercrombie-before-they-are-hanged": {
        "title": "Before They Are Hanged",
        "author": "Joe Abercrombie"
    },
    "joe-abercrombie-the-last-argument-of-kings": {
        "title": "The Last Argument of Kings",
        "author": "Joe Abercrombie"
    },
    "joe-abercrombie-the-blade-itself": {
        "title": "The Blade Itself",
        "author": "Joe Abercrombie"
    },
    "joe-hill-20th-century-ghosts": {
        "title": "20th Century Ghosts",
        "author": "Joe Hill"
    },
    "joe-hill-heart-shaped-box": {
        "title": "Heart-Shaped Box",
        "author": "Joe Hill"
    },
    "john-curran-agatha-christies-murder-in-the-making": {
        "title": "Agatha Christie's Murder in the Making",
        "author": "John Curran"
    },
    "john-gall-systemantics-how-systems-work": {
        "title": "Systemantics: How Systems Work and Especially How They Fail",
        "author": "John Gall"
    },
    "jonathan-sperber-a-nineteenth-century-life": {
        "title": "Karl Marx: A Nineteenth-Century Life",
        "author": "Jonathan Sperber"
    },
    "josh-kaufman-the-first-20-hours": {
        "title": "The First 20 Hours",
        "author": "Josh Kaufman"
    },
    "kara-kennedy-i-will-never-leave-you": {
        "title": "I Will Never Leave You",
        "author": "Kara Kennedy"
    },
    "kristen-perrin-how-to-solve-your-own-murder": {
        "title": "How to Solve Your Own Murder",
        "author": "Kristen Perrin"
    },
    "lg-ursula-k-the-left-hand-of-darkness": {
        "title": "The Left Hand of Darkness",
        "author": "Ursula K. Le Guin"
    },
    "leo-tolstoy-death-of-ivan-ilych": {
        "title": "The Death of Ivan Ilyich",
        "author": "Leo Tolstoy"
    },
    "malcolm-gladwell-david-and-goliath": {
        "title": "David and Goliath",
        "author": "Malcolm Gladwell"
    },
    "malcom-gladwell-blink": {
        "title": "Blink: The Power of Thinking Without Thinking",
        "author": "Malcolm Gladwell"
    },
    "marty-neumeier-the-brand-gap": {
        "title": "The Brand Gap",
        "author": "Marty Neumeier"
    },
    "marty-neumeier-the-brand-flip": {
        "title": "The Brand Flip",
        "author": "Marty Neumeier"
    },
    "matthew-walker-why-we-sleep": {
        "title": "Why We Sleep: Unlocking the Power of Sleep and Dreams",
        "author": "Matthew Walker"
    },
    "michael-crichton-airframe": {
        "title": "Airframe",
        "author": "Michael Crichton"
    },
    "michael-crichton-congo": {
        "title": "Congo",
        "author": "Michael Crichton"
    },
    "michael-crichton-sphere": {
        "title": "Sphere",
        "author": "Michael Crichton"
    },
    "mitch-albom-tuesdays-with-morrie": {
        "title": "Tuesdays with Morrie",
        "author": "Mitch Albom"
    },
    "mona-awad-bunny": {
        "title": "Bunny",
        "author": "Mona Awad"
    },
    "pat-conroy-the-prince-of-tides": {
        "title": "The Prince of Tides",
        "author": "Pat Conroy"
    },
    "percival-everett-the-trees": {
        "title": "The Trees",
        "author": "Percival Everett"
    },
    "peter-frankopan-the-silk-roads": {
        "title": "The Silk Roads: A New History of the World",
        "author": "Peter Frankopan"
    },
    "pranay-lal-indica-a-deep-natural-history-of-the-indian-subcontinent": {
        "title": "Indica: A Deep Natural History of the Indian Subcontinent",
        "author": "Pranay Lal"
    },
    "rand-fishkin-lost-and-founder": {
        "title": "Lost and Founder",
        "author": "Rand Fishkin"
    },
    "rick-rubin-the-creative-act-a-way-of-being": {
        "title": "The Creative Act: A Way of Being",
        "author": "Rick Rubin"
    },
    "robert-cialdini-pre-suasion": {
        "title": "Pre-Suasion: A Revolutionary Way to Influence and Persuade",
        "author": "Robert Cialdini"
    },
    "robert-houdin-memoirs-of-robert-houdin": {
        "title": "Memoirs of Robert-Houdin",
        "author": "Jean-Eugène Robert-Houdin"
    },
    "roland-barthes-image-music-text": {
        "title": "Image, Music, Text",
        "author": "Roland Barthes"
    },
    "rowan-williams-dostoevsky-language-faith-and-fiction": {
        "title": "Dostoevsky: Language, Faith and Fiction",
        "author": "Rowan Williams"
    },
    "ryan-holiday-the-obstacle-is-the-way": {
        "title": "The Obstacle Is the Way",
        "author": "Ryan Holiday"
    },
    "s-f-kosa-the-night-we-burned": {
        "title": "The Night We Burned",
        "author": "S. F. Kosa"
    },
    "salman-rushdie-the-satanic-verses": {
        "title": "The Satanic Verses",
        "author": "Salman Rushdie"
    },
    "salman-rushdie-haroun-and-the-sea-of-stories": {
        "title": "Haroun and the Sea of Stories",
        "author": "Salman Rushdie"
    },
    "sashi-tharoor-why-i-am-a-hindu": {
        "title": "Why I Am a Hindu",
        "author": "Shashi Tharoor"
    },
    "sasha-grey-the-juliette-society": {
        "title": "The Juliette Society",
        "author": "Sasha Grey"
    },
    "sayaka-murata-convenience-store-woman": {
        "title": "Convenience Store Woman",
        "author": "Sayaka Murata"
    },
    "susan-orlean-the-library-book": {
        "title": "The Library Book",
        "author": "Susan Orlean"
    },
    "susan-piver-the-wisdom-of-a-broken-heart": {
        "title": "The Wisdom of a Broken Heart",
        "author": "Susan Piver"
    },
    "t-m-scanlon-what-we-owe-to-each-other": {
        "title": "What We Owe to Each Other",
        "author": "T. M. Scanlon"
    },
    "tali-sharot-the-influential-mind": {
        "title": "The Influential Mind",
        "author": "Tali Sharot"
    },
    "ted-chiang-the-story-of-your-life": {
        "title": "Stories of Your Life and Others",
        "author": "Ted Chiang"
    },
    "the-agatha-christie-the-murder-of-roger-ackroyd": {
        "title": "The Murder of Roger Ackroyd",
        "author": "Agatha Christie"
    },
    "timothy-snyder-bloodlands-europe-btwn-hitler-stalin": {
        "title": "Bloodlands: Europe Between Hitler and Stalin",
        "author": "Timothy Snyder"
    },
    "walter-benjamin-the-work-of-art-in-the-age-of-mechanical-reproduction": {
        "title": "The Work of Art in the Age of Mechanical Reproduction",
        "author": "Walter Benjamin"
    },
    "walter-tevis-mockingbird": {
        "title": "Mockingbird",
        "author": "Walter Tevis"
    },
    "will-storr-the-status-game": {
        "title": "The Status Game: On Social Position and Why We Use It",
        "author": "Will Storr"
    },
    "william-faulkner-unknown": {
        "title": "The Sound and the Fury",
        "author": "William Faulkner"
    },
    "worringer-wilhelm-abstraction-and-empathy-psychology-of-style": {
        "title": "Abstraction and Empathy: A Contribution to the Psychology of Style",
        "author": "Wilhelm Worringer"
    },
    "yann-martel-the-facts-behind-the-helsinki-roccamatios": {
        "title": "The Facts Behind the Helsinki Roccamatios",
        "author": "Yann Martel"
    },
    "yuen-ren-chao-language-and-symbolic-systems": {
        "title": "Language and Symbolic Systems",
        "author": "Yuen Ren Chao"
    },
    "brad-frost-atomic-design": {
        "title": "Atomic Design",
        "author": "Brad Frost"
    },
    "david-kadavy-design-for-hackers": {
        "title": "Design for Hackers",
        "author": "David Kadavy"
    },
    "joe-pulizzi-epic-content-marketing": {
        "title": "Epic Content Marketing",
        "author": "Joe Pulizzi"
    },
    "steve-krug-don-t-make-me-think": {
        "title": "Don't Make Me Think",
        "author": "Steve Krug"
    },
    "daviant-ollam-practical-lock-picking": {
        "title": "Practical Lock Picking",
        "author": "Deviant Ollam"
    },
    "wes-bush-product-led-growth": {
        "title": "Product-Led Growth",
        "author": "Wes Bush"
    },
    "qntm-valuable-humans-in-transit-and-other-stories": {
        "title": "Valuable Humans in Transit and Other Stories",
        "author": "qntm"
    },
    "adolf-hitler-mein-kampf-ralph-manheim-translation": {
        "title": "Mein Kampf",
        "author": "Adolf Hitler"
    },
    "99-ways-to-tell-a-story-exercises-in-style": {
        "title": "99 Ways to Tell a Story: Exercises in Style",
        "author": "Matt Madden"
    },
    "barthes-the-death-of-the-author-unknown": {
        "title": "The Death of the Author",
        "author": "Roland Barthes"
    },
    "aristotle-nicomachean-ethics": {
        "title": "Nicomachean Ethics",
        "author": "Aristotle"
    },
    "maus-a-survivor-s-tale": {
        "title": "Maus: A Survivor's Tale",
        "author": "Art Spiegelman"
    },
    "logicomix-a-search-for-truth": {
        "title": "Logicomix: An Epic Search for Truth",
        "author": "Apostolos Doxiadis & Christos Papadimitriou"
    },
    "rilke-poems-from-the-book-of-hours": {
        "title": "Poems from the Book of Hours",
        "author": "Rainer Maria Rilke"
    },
    "ann-handley-everybody-writes": {
        "title": "Everybody Writes",
        "author": "Ann Handley"
    },
    "byung-chul-han-absence-on-the-culture-and-philosophy-of-the-far-east": {
        "title": "Absence: On the Culture and Philosophy of the Far East",
        "author": "Byung-Chul Han"
    },
    "david-guterson-snow-falling-on-cedars": {
        "title": "Snow Falling on Cedars",
        "author": "David Guterson"
    },
    "david-mcraney-you-are-not-so-smart-why-you-have-too-many-friends-on-facebook-why-your-memory-is-mostly-fiction-and-46-other-ways-you-re-deluding-yourself-penguin-group-us": {
        "title": "You Are Not So Smart",
        "author": "David McRaney"
    },
    "david-ogilvy-ogilvy-on-advertising": {
        "title": "Ogilvy on Advertising",
        "author": "David Ogilvy"
    },
    "dominic-o-brien-you-can-have-an-amazing-memory": {
        "title": "You Can Have an Amazing Memory",
        "author": "Dominic O'Brien"
    },
    "randall-munroe-what-if": {
        "title": "What If?: Serious Scientific Answers to Absurd Hypothetical Questions",
        "author": "Randall Munroe"
    }
}

# Books tagged for "Short Stories"
SHORT_STORIES_IDS = {
    "ted-chiang-the-story-of-your-life",
    "stories-of-your-life-and-others-ted-chiang",
    "ernest-hemingway-short-stories",
    "blind-willow-sleeping-woman-haruki-murakami",
    "men-without-women-haruki-murakami",
    "cixin-liu-the-wandering-earth",
    "the-paper-menagerie-and-other-stories-ken-liu",
    "qntm-valuable-humans-in-transit-and-other-stories",
    "exurb1a-the-fifth-science",
    "etgar-keret-the-bus-driver-who-wanted-to-be-god",
    "etgar-keret-the-seven-good-years",
    "joe-hill-20th-century-ghosts",
    "yann-martel-the-facts-behind-the-helsinki-roccamatios",
    "a-short-stay-in-hell-steven-l-peck",
    "best-of-satyajit-ray-satyajit-ray",
    "the-call-of-cthulhu-and-other-weird-stories-hp-lovecraft",
    "the-gambler-and-other-stories-fyodor-dostoyevsky",
    "white-nights-fyodor-dostoyevsky",
    "notes-from-underground-the-double-fyodor-dostoevsky",
    "leo-tolstoy-death-of-ivan-ilych",
    "isaac-asimov-asimov-s-mysteries",
    "russian-short-stories-from-pushkin-to-buida-chandler-robert",
    "paradise-and-other-stories-khushwant-singh",
    "short-storybaazi-divya-prakash-dubey",
    "the-reading-room-a-short-fiction-mag"
}

# Books tagged for "Essays"
ESSAYS_IDS = {
    "selected-essays-george-orwell",
    "all-art-is-propaganda-george-orwell",
    "review-of-mein-kampf-by-adolf-hitler-george-orwell",
    "myth-of-sisyphus-and-other-essays-the-albert-camus",
    "how-to-travel-with-a-salmon-other-essays-umberto-eco",
    "chronicles-of-a-liquid-society-umberto-eco",
    "this-is-water-david-foster-wallace",
    "writing-craft-essays-chuck-palahniuk",
    "chuck-palahniuk-nuts-and-bolts-thought-verbs-litreactor",
    "stranger-than-fiction-chuck-palahniuk",
    "roland-barthes-image-music-text",
    "barthes-the-death-of-the-author-unknown",
    "walter-benjamin-the-work-of-art-in-the-age-of-mechanical-reproduction",
    "the-fire-next-time-james-baldwin",
    "trick-mirror-jia-tolentino",
    "the-anthropocene-reviewed-john-green",
    "seneca-letters-on-ethics",
    "rilke-letters-to-a-young-poet",
    "letters-to-milena-franz-kafka-franz-kafka",
    "love-letters-virginia-woolf-and-vita-sackville-west",
    "the-love-letters-of-abelard-and-heloise-virginia-woolf-vita-sackville-west",
    "bhagat-singh-why-i-am-an-atheist-bhagat-singh",
    "awara-bheed-ke-khatare-harishankar-parsai",
    "vaishnav-ki-phislan-harishankar-parsai",
    "byung-chul-han-absence-on-the-culture-and-philosophy-of-the-far-east",
    "burn-it-down-feminist-manifestos-breanne-fahs",
    "scum-manifesto-valerie-solanas",
    "the-communist-manifesto-unknown",
    "the-stream-of-homer-on-story-heroism-and-the-river-that-runs-underneath-everything",
    "zen-in-the-art-of-writing-ray-bradbury",
    "pity-the-reader-kurt-vonnegut",
    "t-m-scanlon-what-we-owe-to-each-other",
    "socialism-utopian-and-scientific-frederick-engels",
    "commodify-your-dissent-thomas-frank"
}

# Books tagged for "Literary Non-Fiction"
LITERARY_NON_FICTION_IDS = {
    "stephen-king-on-writing",
    "mitch-albom-tuesdays-with-morrie",
    "shoe-dog-phil-knight",
    "know-my-name-chanel-miller",
    "susan-orlean-the-library-book",
    "peter-frankopan-the-silk-roads",
    "pranay-lal-indica-a-deep-natural-history-of-the-indian-subcontinent",
    "carl-jung-memories-dreams-reflections",
    "carl-jung-man-and-his-symbols",
    "carl-jung-the-development-of-personality",
    "derren-brown-confessions-of-a-conjuror",
    "robert-houdin-memoirs-of-robert-houdin",
    "hannah-arendt-eichmann-in-jerusalem-a-report-on-the-banality-of-evil",
    "timothy-snyder-bloodlands-europe-btwn-hitler-stalin",
    "jared-diamond-guns-germs-and-steel",
    "oliver-burkeman-four-thousand-weeks-time-management-for-mortals-libgen-li",
    "meditations-for-mortals-oliver-burkeman",
    "the-fire-next-time-james-baldwin",
    "homage-to-catalonia-george-orwell",
    "apropos-of-nothing-woody-allen",
    "bahut-door-kitni-door-hota-hai-manav-kaul",
    "sashi-tharoor-why-i-am-a-hindu",
    "the-great-indian-novel-shashi-tharoor",
    "no-nation-for-women-priyanka-dubey",
    "bird-by-bird-some-instructions-on-writing-and-life-anne-lamott",
    "tiny-beautiful-things-cheryl-strayed",
    "what-i-talk-about-when-i-talk-about-running-haruki-murakami",
    "james-gleick-chaos-making-a-new-science",
    "sculpting-in-time-andrei-tarkovsky",
    "in-the-blink-of-an-eye-walter-murch",
    "rick-rubin-the-creative-act-a-way-of-being",
    "into-the-woods-john-yorke",
    "john-curran-agatha-christies-murder-in-the-making",
    "jonathan-sperber-a-nineteenth-century-life",
    "the-meaning-of-hitler-sebastian-haffner",
    "amusing-ourselves-to-death-neil-postman",
    "matthew-walker-why-we-sleep",
    "will-storr-the-status-game",
    "the-science-of-storytelling-will-storr",
    "malcolm-gladwell-david-and-goliath",
    "malcom-gladwell-blink",
    "the-anthropocene-reviewed-john-green",
    "trick-mirror-jia-tolentino",
    "jennifer-burns-goddess-of-the-market",
    "rowan-williams-dostoevsky-language-faith-and-fiction",
    "david-mcraney-you-are-not-so-smart-why-you-have-too-many-friends-on-facebook-why-your-memory-is-mostly-fiction-and-46-other-ways-you-re-deluding-yourself-penguin-group-us",
    "tali-sharot-the-influential-mind",
    "susan-piver-the-wisdom-of-a-broken-heart",
    "pat-conroy-the-prince-of-tides",
    "yuen-ren-chao-language-and-symbolic-systems",
    "worringer-wilhelm-abstraction-and-empathy-psychology-of-style"
}

def audit_and_tag():
    books = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    print(f"Loaded {len(books)} books from {DATA_PATH}")

    swapped_applied = 0
    short_stories_tagged = 0
    essays_tagged = 0
    lit_nonfiction_tagged = 0

    for b in books:
        bid = b.get("id")
        
        # 1. Apply Swapped metadata fixes
        if bid in SWAPPED_FIXES:
            fix = SWAPPED_FIXES[bid]
            b["title"] = fix["title"]
            b["author"] = fix["author"]
            swapped_applied += 1

        # 2. Manage multi-category tagging
        # Start with primary category
        primary_cat = b.get("category", "Fiction & Non-Fiction")
        cats = [primary_cat]

        if bid in SHORT_STORIES_IDS and "Short Stories" not in cats:
            cats.append("Short Stories")
            short_stories_tagged += 1

        if bid in ESSAYS_IDS and "Essays" not in cats:
            cats.append("Essays")
            essays_tagged += 1

        if bid in LITERARY_NON_FICTION_IDS and "Literary Non-Fiction" not in cats:
            cats.append("Literary Non-Fiction")
            lit_nonfiction_tagged += 1

        b["categories"] = cats

    # Check Snow Crash
    snow_crash = next((b for b in books if "snow-crash" in b.get("id", "")), None)
    if snow_crash:
        print(f"Snow Crash verification: Title='{snow_crash['title']}', Author='{snow_crash['author']}'")

    print(f"Successfully applied {swapped_applied} swapped metadata fixes.")
    print(f"Tagged {short_stories_tagged} books as 'Short Stories'.")
    print(f"Tagged {essays_tagged} books as 'Essays'.")
    print(f"Tagged {lit_nonfiction_tagged} books as 'Literary Non-Fiction'.")

    # Save to data.json
    DATA_PATH.write_text(json.dumps(books, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated {DATA_PATH} successfully.")

if __name__ == "__main__":
    audit_and_tag()
