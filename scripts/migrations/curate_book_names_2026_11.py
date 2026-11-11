# scripts/migrations/curate_book_names_2026_11.py — ONE-TIME migration that produced content/book_names.json
# Usage: python3 scripts/migrations/curate_book_names_2026_11.py <drive_id_to_filename.json>   (already run on 2026-11-11; kept for the record)
# Requires: bookshelf/data.json as it stood at commit 7a20bce (620 books, each with a drive_id)
#
# What it did: hand-reviewed every shelf title/author against its Google Drive filename and wrote the
# corrected names to content/book_names.json, keyed by Google Drive file ID. That file is now the single
# source of truth for names; the build script no longer guesses names for books listed there.
#
# Gotchas:
# - Corrections are keyed by the shelf book `id` (stable slug), not by list position.
# - Running it again against a newer data.json would overwrite later hand edits to book_names.json, so
#   it refuses to run when book_names.json already exists. Edit book_names.json directly instead.

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "bookshelf" / "data.json"
OUT = ROOT / "content" / "book_names.json"

# Author spellings normalised everywhere (wrong/variant -> canonical)
AUTHOR_CANON = {
    "George orwell": "George Orwell",
    "ToniMorrison": "Toni Morrison",
    "Kurt Vonnegut Jr": "Kurt Vonnegut",
    "Fyodor Dostoyevsky": "Fyodor Dostoevsky",
    "Herman Hesse": "Hermann Hesse",
    "Byung chul Han": "Byung-Chul Han",
    "Ursula K Le Guin": "Ursula K. Le Guin",
    "Hunter S Thompson": "Hunter S. Thompson",
    "Alain De Botton": "Alain de Botton",
    "Neil Stephenson": "Neal Stephenson",
    "Steven L Peck": "Steven L. Peck",
    "Thomas S Kuhn": "Thomas S. Kuhn",
    "E M Forster": "E. M. Forster",
    "HP Lovecraft": "H. P. Lovecraft",
    "Daniel H Pink": "Daniel H. Pink",
    "K David Harrison": "K. David Harrison",
    "William S Burroughs": "William S. Burroughs",
    "Arthur Conan Doyle.l": "Arthur Conan Doyle",
    "Victor Frankl": "Viktor E. Frankl",
    "Meiko kawakami": "Mieko Kawakami",
    "Rahi masoom raza": "Rahi Masoom Raza",
    "Jeffery Archer": "Jeffrey Archer",
    "Stanislaw Lem": "Stanisław Lem",
    "Claudia Pineiro": "Claudia Piñeiro",
    "Sheena Iyenga": "Sheena Iyengar",
    "Van der Kolk, Bessel A": "Bessel van der Kolk",
    "Alexander Dumas": "Alexandre Dumas",
    "Horowitz, Ben": "Ben Horowitz",
    "Palahniuk, Chuck": "Chuck Palahniuk",
    "Chandler, Robert": "Robert Chandler (ed.)",
    "Donald-Miller": "Donald Miller",
    "Erick Ries": "Eric Ries",
    "Mark Shaefer": "Mark Schaefer",
    "Al Ries Jack Trout": "Al Ries & Jack Trout",
    "Al Ries, Laura Ries": "Al Ries & Laura Ries",
    "Chip Heath, Dan Heath": "Chip Heath & Dan Heath",
    "Chip and Dan Heath": "Chip Heath & Dan Heath",
    "Gabriel Weinberg, Justin Mares": "Gabriel Weinberg & Justin Mares",
    "Tom Kelley, David Kelley": "Tom Kelley & David Kelley",
    "Lidia Zylowska, Daniel Siegel": "Lidia Zylowska & Daniel Siegel",
    "Daron Acemoglu, James Robinson": "Daron Acemoglu & James A. Robinson",
    "William Dowling, Robert Bell": "William Dowling & Robert Bell",
    "Al Ramadan, Dave Peterson, Christopher Lochhead": "Al Ramadan, Dave Peterson & Christopher Lochhead",
    "Jake Knapp John Zeratsky": "Jake Knapp & John Zeratsky",
    "Virginia Woolf and Vita Sackville West": "Virginia Woolf & Vita Sackville-West",
    "Friedrich Wilhelm Nietzsche": "Friedrich Nietzsche",
    "Swaroop Ch": "Swaroop C H",
    "Dinkar": "Ramdhari Singh Dinkar",
    "Frederick Brooks": "Frederick P. Brooks Jr.",
    "Dr. Robert A. Glover": "Robert A. Glover",
    "Jann S Wenner": "Jann S. Wenner",
    "Robert W Bly": "Robert W. Bly",
    "Gregory Hays translation": "Marcus Aurelius",
    "Unknown": "Anonymous",
}

# Per-book corrections: id -> (title, author). None keeps the current value (after AUTHOR_CANON).
FIX = {
    "art-of-dramatic-writing-the-lajos-egri": ("The Art of Dramatic Writing", None),
    "akira-unknown": ("Akira (Complete Series)", None),
    "the-book-of-ramen-unknown": (None, "Mike Satinover (Ramen_Lord)"),
    "1984-george-orwell": (None, "George Orwell"),
    "a-cup-of-zen-kai-tsukimi-115919174-libgen-li-unknown": ("A Cup of Zen", "Kai Tsukimi"),
    "animal-farm-by-george-orwell-george-orwell": ("Animal Farm", None),
    "bhagat-singh-why-i-am-an-atheist-bhagat-singh": ("Why I Am an Atheist", None),
    "bird-by-bird-some-instructions-on-writing-and-life-anne-lamott": ("Bird by Bird: Some Instructions on Writing and Life", None),
    "boom-bubbles-and-the-end-of-stagnation-byrne-hobar": ("Boom: Bubbles and the End of Stagnation", "Byrne Hobart"),
    "burn-it-down-feminist-manifestos-breanne-fahs": ("Burn It Down! Feminist Manifestos for the Revolution", None),
    "cats-cradle-kurt-vonnegut-jr": ("Cat's Cradle", None),
    "chuck-palahniuk-rant-the-oral-biography-of-buster-casey-palahniuk-chuck": ("Rant: An Oral Biography of Buster Casey", "Chuck Palahniuk"),
    "contagious-why-things-catch-on-jonah-berger": ("Contagious: Why Things Catch On", None),
    "elements-of-style-strunk-and-white": ("The Elements of Style", "William Strunk Jr. & E. B. White"),
    "exurb1a-geometry-for-ocelots": ("Geometry for Ocelots", "Exurb1a"),
    "fear-and-loathing-on-the-campaign-trail-7-hunter-s-thompson": ("Fear and Loathing on the Campaign Trail '72", None),
    "feline-philosophy-john-gray-john-gray": ("Feline Philosophy: Cats and the Meaning of Life", None),
    "feluda-the-complete-adventures-of-feluda-satyajit-ray": ("The Complete Adventures of Feluda", None),
    "freakonomics-unknown": ("Freakonomics", "Steven D. Levitt & Stephen J. Dubner"),
    "gonzo-jann-s-wenner": ("Gonzo: The Life of Hunter S. Thompson", "Jann S. Wenner & Corey Seymour"),
    "good-stories-on-ai-and-future-ke-unknown": ("Good Stories (Future Science Fiction Digest)", "Ken Liu"),
    "harry-lorayne-super-power-memory": ("Super Power Memory", "Harry Lorayne"),
    "hells-angels-hunter-s-thompson": ("Hell's Angels", None),
    "hey-whipple-squeeze-this-the-classic-guide-to-creating-great-ads-luke-sullivan": ("Hey, Whipple, Squeeze This: The Classic Guide to Creating Great Ads", None),
    "hitlers-table-talk-1941-1944-norman-cameron": ("Hitler's Table Talk, 1941–1944", "Adolf Hitler (trans. Norman Cameron & R. H. Stevens)"),
    "how-to-research-anything-unknown": ("How to Research Anything: Smart Research Habits for Curious Adults", "Polymath Investor"),
    "how-to-travel-with-a-salmon-other-essays-umberto-eco": ("How to Travel with a Salmon & Other Essays", None),
    "ikigai-the-japanese-secret-to-a-long-and-happy-life-h-ctor-garc-a": ("Ikigai: The Japanese Secret to a Long and Happy Life", "Héctor García & Francesc Miralles"),
    "influence-the-psychology-of-persuasion-robert-b-cialdini": ("Influence: The Psychology of Persuasion", None),
    "japans-historical-arc-from-feuda-unknown": ("Japan's Historical Arc: From Feudalism to War to Rebirth", "Anonymous"),
    "joe-hill-king-sorrow": ("King Sorrow", "Joe Hill"),
    "jung-s-map-of-the-soul-an-introduction-murray-stein": ("Jung's Map of the Soul: An Introduction", None),
    "junkie-william-s-burroughs": ("Junky", None),
    "kavalier-and-clay-michael-chabon": ("The Amazing Adventures of Kavalier & Clay", None),
    "kim-jiyoung-born-1982-cho-nam-joo": ("Kim Jiyoung, Born 1982", None),
    "know-my-name-a-memoir-chanel-miller": ("Know My Name: A Memoir", None),
    "lessons-in-stoicism-john-sellers-john-sellars": ("Lessons in Stoicism", None),
    "letters-to-milena-franz-kafka-franz-kafka": ("Letters to Milena", None),
    "love-letters-virginia-woolf-and-vita-sackville-west": ("Love Letters: Vita and Virginia", None),
    "matthew-mcconaughey-greenlights": ("Greenlights", "Matthew McConaughey"),
    "meditations-marcus-aurelius-gregory-hays-translation": ("Meditations (trans. Gregory Hays)", "Marcus Aurelius"),
    "meditations-for-mortals-four-weeks-to-embrace-your-limitations-and-make-time-for-what-counts-oliver-burkeman-107217730-libgen-li-oliver-burkeman": ("Meditations for Mortals: Four Weeks to Embrace Your Limitations and Make Time for What Counts", None),
    "michael-crichton-rising-sun": ("Rising Sun", "Michael Crichton"),
    "monetizing-innovation-ramanujam-madhavan-tacke-georg": (None, "Madhavan Ramanujam & Georg Tacke"),
    "monkey-folk-tale-of-china-journey-to-the-west-abridged": ("Monkey: A Folk Novel of China (Journey to the West, abridged)", "Wu Cheng'en (trans. Arthur Waley)"),
    "moonwalking-with-einstein-the-art-and-science-of-remembering-everything-joshua-foer": ("Moonwalking with Einstein: The Art and Science of Remembering Everything", None),
    "myth-of-sisyphus-and-other-essays-the-albert-camus": ("The Myth of Sisyphus and Other Essays", None),
    "no-more-mr-nice-guy-robert-glove-dr-robert-a-glover": ("No More Mr. Nice Guy", None),
    "nothing-lasts-forever-jerry-roderick-thorp": ("Nothing Lasts Forever", None),
    "nuts-and-bolts-thought-verbs-litreactor-chuck-palahniuk": ("Nuts and Bolts: “Thought” Verbs", None),
    "on-writing-well-the-classic-guide-to-writing-nonfiction-william-zinsser": ("On Writing Well: The Classic Guide to Writing Nonfiction", None),
    "orson-scott-card-ender-s-game": ("Ender's Game", "Orson Scott Card"),
    "oscar-wilde-only-dull-people-are-brilliant-at-breakfast": ("Only Dull People Are Brilliant at Breakfast", "Oscar Wilde"),
    "owning-your-own-shadow-robert-a-johnson-robert-a-johnson": ("Owning Your Own Shadow", None),
    "paul-loomans-time-surfing": ("Time Surfing", "Paul Loomans"),
    "persuader-a-reacher-novel-lee-child": ("Persuader (Jack Reacher #7)", None),
    "picture-of-dorian-gray-unknown": ("The Picture of Dorian Gray", "Oscar Wilde"),
    "plato-five-dialogues": ("Five Dialogues", "Plato"),
    "positioning-al-ries-philip-kotler": ("Positioning: The Battle for Your Mind", "Al Ries & Jack Trout"),
    "ray-dalio-principles-unknown": ("Principles: Life and Work", "Ray Dalio"),
    "rest-alex-pang": ("Rest: Why You Get More Done When You Work Less", "Alex Soojung-Kim Pang"),
    "review-of-mein-kampf-by-adolf-hitler-george-orwell": ("Review of Mein Kampf", None),
    "richard-adams-watership-down": ("Watership Down", "Richard Adams"),
    "richard-bandler-frogs-into-princes": ("Frogs into Princes", "Richard Bandler & John Grinder"),
    "risk-savvy-how-to-make-good-decisions-gerd-gigerenzer": ("Risk Savvy: How to Make Good Decisions", None),
    "rivers-of-london-1-ben-aaronovitch": ("Rivers of London", None),
    "roadside-picnic-arkady-and-boris": (None, "Arkady & Boris Strugatsky"),
    "scene-75-rahi-masoom-raza": ("Scene 75", None),
    "second-look-issue-one": ("Second Look: A Magazine of Stories, Essays & Ideas (Issue One)", "Various Authors"),
    "seneca-letters-on-ethics": ("Letters on Ethics (Letters from a Stoic)", "Seneca"),
    "six-pillars-of-self-esteem-nathaniel-branden-unknown": ("The Six Pillars of Self-Esteem", "Nathaniel Branden"),
    "skeleton-creek-1-carman-patrick": ("Skeleton Creek", "Patrick Carman"),
    "sophies-world-a-novel-about-the-unknown": ("Sophie's World", "Jostein Gaarder"),
    "strange-pictures-uketsu-uketsu": ("Strange Pictures", None),
    "style-an-anti-textbook-richard-lanham-richard-a-lanham": ("Style: An Anti-Textbook", None),
    "susan-orlean-on-animals": ("On Animals", "Susan Orlean"),
    "talking-to-my-daughter-about-the-economy-how-capitalism-works-fails-yanis-varoufakis": ("Talking to My Daughter About the Economy: How Capitalism Works—and How It Fails", None),
    "tara-mohr-playing-big": ("Playing Big", "Tara Mohr"),
    "the-annotated-critical-laozi-unknown": ("The Annotated Critical Laozi (Tao Te Ching)", "Laozi"),
    "the-artists-way-julia-cameron": ("The Artist's Way", None),
    "the-communist-manifesto-unknown": (None, "Karl Marx & Friedrich Engels"),
    "the-darkest-hours-jim-butcher": ("The Darkest Hours (Spider-Man)", None),
    "the-diary-of-a-young-girl-anne-frank-anne-frank": ("The Diary of a Young Girl", None),
    "the-fifth-season-nk-jemisin-n-k-jemisin": ("The Fifth Season (The Broken Earth #1)", None),
    "the-freud-jung-letters-unknown": ("The Freud/Jung Letters", "Sigmund Freud & C. G. Jung"),
    "the-hard-thing-about-hard-things-horowitz-ben": ("The Hard Thing About Hard Things", None),
    "the-love-letters-of-abelard-and-heloise-virginia-woolf-vita-sackville-west": (None, "Peter Abelard & Héloïse"),
    "the-power-of-your-subconscious-mind-joseph-murphy": ("The Power of Your Subconscious Mind", None),
    "the-revolt-of-the-public-and-the-crisis-of-authority-in-the-new-millennium-martin-gurri": ("The Revolt of the Public and the Crisis of Authority in the New Millennium", None),
    "the-richest-man-in-babylon-george-s-clason": ("The Richest Man in Babylon", None),
    "the-seven-deaths-of-evelyn-hardcastle-unknown": (None, "Stuart Turton"),
    "the-stream-of-homer-on-story-heroism-and-the-river-that-runs-underneath-everything": ("The Stream of Homer: On Story, Heroism, and the River That Runs Underneath Everything", "Anonymous"),
    "the-thought-war-barak-kushner": ("The Thought War: Japanese Imperial Propaganda", None),
    "the-ones-who-walk-away-from-omelas-unknown": ("The Ones Who Walk Away from Omelas", "Ursula K. Le Guin"),
    "the-power-of-writing-it-down-allison-fallon": ("The Power of Writing It Down", None),
    "the-practicing-stoic-practising-stoic-a-philosophical-users-manual": ("The Practicing Stoic: A Philosophical User's Manual", "Ward Farnsworth"),
    "the-argumentative-indian-amartya-unknown": ("The Argumentative Indian", "Amartya Sen"),
    "the-great-business-reformation-h-unknown": ("The Great Business Reformation: How AI Agents Are Rewriting the Rules of Enterprise", "Anonymous"),
    "the-new-control-society-by-jon-a-unknown": ("The New Control Society", "Jon Askonas"),
    "the-paradox-of-self-knowledge-why-consciousness-must-forget-to-find-itself-unknown": ("The Paradox of Self-Knowledge: Why Consciousness Must Forget to Find Itself", "Anonymous"),
    "the-political-symphony-why-natio-unknown": ("The Political Symphony: Why Nations Choose Different Paths", "Anonymous"),
    "the-tao-te-ching-translated-by-g-unknown": ("Tao Te Ching (trans. Gia-Fu Feng)", "Lao Tzu"),
    "the-dream-of-a-ridiculous-man-fi-fyodor-dostoevsky": ("The Dream of a Ridiculous Man", None),
    "thinking-in-systems-a-primer-by-donella-h-meadows-donella-h-meadows": ("Thinking in Systems: A Primer", None),
    "train-to-pakistan-khushwant-singh": ("Train to Pakistan", None),
    "understanding-media-the-extensions-of-man-marshall-mcluhan": ("Understanding Media: The Extensions of Man", None),
    "verissimus-the-stoic-philosophy-of-marcus-aurelius-unknown": ("Verissimus: The Stoic Philosophy of Marcus Aurelius", "Donald J. Robertson & Zé Nuno Fraga"),
    "we-are-bob-we-are-legion": ("We Are Legion (We Are Bob)", "Dennis E. Taylor"),
    "what-every-body-is-saying-unknown": ("What Every BODY Is Saying", "Joe Navarro"),
    "white-nights-fyodor-dostoyevsky": ("White Nights", None),
    "won-pyung-sohn-almond-won-pyung-sohn": ("Almond", None),
    "world-war-z-brooks-max": ("World War Z", "Max Brooks"),
    "an-outline-of-philosophy-unknown": ("An Outline of Philosophy", "Ted Tripp"),
    "commodify-your-dissent-thomas-frank": ("Commodify Your Dissent", None),
    "did-somebody-say-totalitarianism-slavoj-zizek": ("Did Somebody Say Totalitarianism?", "Slavoj Žižek"),
    "qntm-there-is-no-antimemetics-di-unknown": ("There Is No Antimemetics Division", "qntm"),
    "socialism-utopian-and-scientific-frederick-engels": ("Socialism: Utopian and Scientific", "Friedrich Engels"),
    "the-reading-room-a-short-fiction-mag": ("The Reading Room: A Short Fiction Mag", "Various Authors"),
    "the-science-of-logic-unknown": ("The Science of Logic", "G. W. F. Hegel"),
    "thinking-fast-and-slow-daniel-kahneman": ("Thinking, Fast and Slow", None),
    "what-is-dialectical-materialism-a-study-guide-unknown": ("What Is Dialectical Materialism? A Study Guide", "Rob Sewell"),
    "zizek-s-jokes-slavoj-zizek": ("Žižek's Jokes", "Slavoj Žižek"),
    "unknown": ("The Little Prince (어린왕자, Korean edition)", "Antoine de Saint-Exupéry"),
    "introducing-semiotics-a-graphic-guide-paul-cobley-litza-jansz": ("Introducing Semiotics: A Graphic Guide", "Paul Cobley & Litza Jansz"),
    "hbr-on-strategic-marketing-unknown": ("HBR's 10 Must Reads on Strategic Marketing", "Harvard Business Review"),
    "hbr-on-persuasive-presentations-unknown": ("HBR on Persuasive Presentations", "Harvard Business Review"),
    "harvard-innovation-labs-product-market-fit-unknown": ("Product-Market Fit", "Harvard Innovation Labs"),
    "building-storybrand-donald-miller": ("Building a StoryBrand", None),
    "mirror-makers-stephen-fox": ("The Mirror Makers", None),
    "the-1-page-marketing-plan-unknown": ("The 1-Page Marketing Plan", "Allan Dib"),
    "the-22-immutable-laws-of-branding-al-ries-laura-ries": ("The 22 Immutable Laws of Branding", None),
    "the-art-of-seo-unknown": (None, "Eric Enge, Stephan Spencer & Jessie Stricchiola"),
    "the-choice-factory-25-behavioural-biases-that-influence-what-we-buy": ("The Choice Factory: 25 Behavioural Biases That Influence What We Buy", "Richard Shotton"),
    "unleashing-the-idea-virus-seth-godin": ("Unleashing the Ideavirus", None),
    "zero-to-one-notes-on-startups-peter-thiel": ("Zero to One: Notes on Startups, or How to Build the Future", None),
    "5-dead-copywriters-to-bring-your-copy-back-to-life-unknown": ("5 Dead Copywriters to Bring Your Copy Back to Life", "Anonymous"),
    "ann-handley-on-newsletter-unknown": ("Ann Handley on Newsletters", "Ann Handley"),
    "byte-of-python-swaroop-ch": ("A Byte of Python", None),
    "dave-gerhardt-ds-unknown": ("DS", "Dave Gerhardt"),
    "intercom-on-jobs-to-be-done-unknown": ("Intercom on Jobs-to-be-Done", "Intercom"),
    "neil-french-collection-unknown": ("The Neil French Collection", "Neil French"),
    "the-copywriter-s-handbook-robert-w-bly": ("The Copywriter's Handbook", None),
    "ultimate-guide-to-street-photography-unknown": ("Ultimate Guide to Street Photography", "Anonymous"),
    "t-u-m-b-b-a-d-unknown": ("Tumbbad (Screenplay)", "Mitesh Shah, Adesh Prasad, Rahi Anil Barve & Anand Gandhi"),
    "american-fiction-2023-unknown": ("American Fiction (Screenplay)", "Cord Jefferson"),
    "how-to-not-die-alone-logan-ury": ("How to Not Die Alone", None),
    "the-hogwarts-library-collection-j-k-rowling": ("The Hogwarts Library Collection", None),
    "mirror-maker-simplified-stephen-fox": ("Mirror Maker Simplified", None),
    "brandon-sanderson-the-final-empire": ("The Final Empire (Mistborn #1)", None),
    "brandon-sanderson-the-well-of-ascension": ("The Well of Ascension (Mistborn #2)", None),
    "brandon-sanderson-the-hero-of-ages": ("The Hero of Ages (Mistborn #3)", None),
    "brandon-sanderson-the-alloy-of-law": ("The Alloy of Law (Mistborn #4)", None),
    "brandon-sanderson-shadows-of-self": ("Shadows of Self (Mistborn #5)", None),
    "brandon-sanderson-the-bands-of-mourning": ("The Bands of Mourning (Mistborn #6)", None),
}

# Series volumes: id prefix -> formatter(volume_label, subtitle)
SERIES_AUTHOR = {"boogiepop-series": "Kouhei Kadono", "monogatari-series": "NisiOisin", "zaregoto": "NisiOisin"}

SMALL = {"a", "an", "the", "and", "but", "or", "nor", "for", "so", "yet", "at", "by", "in", "of", "on", "to",
         "up", "as", "is", "vs", "via", "with", "from", "into", "than"}


def smart_title(t: str) -> str:
    """Capitalise all-lowercase words (keeps acronyms, mixed case like 'unMind', and non-Latin text)."""
    words = t.split(" ")
    out = []
    for i, w in enumerate(words):
        core = w.strip("(\"'“")
        if core and core.islower() and core.isascii() and (i == 0 or core not in SMALL or out[-1].endswith(":")):
            lead = w[: len(w) - len(w.lstrip("(\"'“"))]
            w = lead + core[0].upper() + core[1:]
        out.append(w)
    return " ".join(out)


def series_name(b, fn):
    """Boogiepop / Monogatari / Zaregoto volumes from their consistent filenames."""
    m = re.match(r"(Boogiepop Series|Monogatari Series|Zaregoto) - Volume (\S+) - (.+?)\s*\[", fn)
    if not m:
        return None
    series, vol, sub = m.groups()
    sub = sub.replace(" - ", ": ").replace(" vs ", " VS ")
    short = series.replace(" Series", "")
    vol = vol.lstrip("0") or "0"
    return f"{sub} ({short}, Vol. {vol})", SERIES_AUTHOR[re.sub(r'[^a-z]+', '-', series.lower()).strip('-')]


def main():
    if OUT.exists() and "--force" not in sys.argv:
        sys.exit(f"{OUT} already exists — edit it directly (pass --force to regenerate from data.json).")
    books = json.loads(DATA.read_text(encoding="utf-8"))
    # {drive_id: filename} snapshot of the Drive listing, passed as the first positional argument
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    filenames = json.loads(Path(args[0]).read_text()) if args else {}
    names = {}
    for b in books:
        title, author = b["title"].strip(), b["author"].strip()
        sn = series_name(b, filenames.get(b["drive_id"], ""))
        if sn:
            title, author = sn
        if b["id"] in FIX:
            t, a = FIX[b["id"]]
            title = t or title
            author = a or author
        author = AUTHOR_CANON.get(author, author)
        if not re.search(r"[^\x00-\x7f]", title[:3]):
            title = smart_title(title)
        names[b["drive_id"]] = {"title": title, "author": author}
    OUT.write_text(json.dumps(names, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {len(names)} curated names to {OUT}")


if __name__ == "__main__":
    main()
