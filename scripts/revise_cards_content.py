# revise_cards_content.py — Replaces all corporate/marketing/business language in cards.json with pure literary craft
# Usage: python3 scripts/revise_cards_content.py
# Requires: json, pathlib

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARDS_FILE = ROOT / "content" / "cards.json"

REVISIONS = {
    "morrison-beloved-thin-love": (
        "Let a character refute an accusation by taking the critic's own adjective and turning it inside out. "
        "When charged with an excess, answer with monosyllabic finality and define the opposite as total absence."
    ),
    "wallace-this-is-water-opening": (
        "Open a philosophical essay with a deadpan animal parable that embodies your central theme without declaring it. "
        "Use casual spoken phrasing and end on a punchy question, resisting the temptation to explain the moral immediately."
    ),
    "burkeman-four-thousand-weeks-attention": (
        "Take a worn everyday idiom like 'spending time' and strip away its figurative comfort. "
        "Reveal the cold economic transaction beneath the words, forcing the reader to weigh the physical life-hours they are trading away."
    ),
    "roy-god-of-small-things-opening": (
        "Fuse two tactile words into a new compound adjective, like 'dustgreen' or 'hot-brooding', to capture a physical atmosphere "
        "that English lacks a single name for. Anchor it beside living, hungry creatures."
    ),
    "didion-white-album-opening": (
        "Follow a bold declaration about human self-deception with immediate, visceral evidence. "
        "Show people seeking moral lessons in violent catastrophes, letting the examples prove the thesis."
    ),
    "sacks-my-own-life-gratitude": (
        "When writing about personal endings or irreversible transitions, acknowledge mortal dread in your opening clause. "
        "Then balance the terror with a clean cadence of monosyllabic past participles chained together with 'and'."
    ),
    "karr-liars-club-opening": (
        "Begin a memoir by distinguishing between two near-synonyms, like poor versus broke, to define your family's social reality. "
        "Then introduce a harsh regional survival skill that teaches the reader how to listen."
    ),
    "palahniuk-thought-verbs": (
        "Ban mental verbs like 'realized', 'felt', and 'remembered' from an entire scene. "
        "Force every internal reaction to register through physical actions and bodily tension."
    ),
    "wallace-supposedly-fun-thing-list": (
        "Build a comic catalogue of human strangeness by repeating the anaphoric phrase 'I have seen' across escalating, "
        "disparate sights. Pair absurd spectacle with clinical detachment."
    ),
    "hemingway-farewell-broken-places": (
        "Take a consoling sentiment about human resilience and follow it with its unforgiving corollary. "
        "Strip away sentimental optimism by showing that nature destroys the gentle as indifferently as the brave."
    ),
    "orwell-politics-english-rules": (
        "Formulate a sequence of spare negative prohibitions for prose, demonstrating the exact simplicity you demand. "
        "Then add a final escape clause that places common sense and musical ear above mechanical dogma."
    ),
    "didion-why-i-write": (
        "Before drafting an essay, write one private page to discover what your attention is truly snagging on. "
        "Let the list narrow from outer sights to inner dread. The real argument surfaces in what you uncover."
    ),
    "salinger-catcher-opening": (
        "Open a first-person narrative by declaring what you refuse to talk about. "
        "Dismiss the conventional biographical formulas of the genre in a running conversational syntax "
        "that lets your narrator's real voice take command."
    ),
    "chekhov-gooseberries-hammer": (
        "Embody an abstract ethical demand in a single tactile emblem, like a person tapping a hammer outside a closed door. "
        "An acoustic, physical reminder makes moral conscience impossible to ignore."
    ),
    "woolf-room-of-ones-own": (
        "Ground a radical philosophical argument in a plain material prerequisite of five hundred pounds a year and a room "
        "with a lock on the door. Dismiss high theoretical debate until the physical conditions for creation exist."
    ),
    "burkeman-four-thousand-weeks-results": (
        "Take a widely shared anxiety about personal productivity and invert the failure. "
        "Show that the true disaster is successfully clearing space for trivial obligations while leaving vital work untouched."
    ),
    "lamott-perfectionism": (
        "Take a praised virtue like perfectionism and redefine it in the language of totalitarian oppression. "
        "Name the raw, imperfect first attempt it prevents you from making."
    ),
    "dillard-spend-it-all": (
        "Place your strongest revelation in the immediate chapter rather than saving it for an imagined climax. "
        "Spending your best material immediately forces you to write into deeper, undiscovered ground."
    ),
    "mccarthy-blood-meridian-opening": (
        "Introduce a protagonist with a stark, three-word imperative: 'See the child.' "
        "Follow it with present-tense physical details and harsh landscape markers, withholding backstory "
        "so the reader confronts the figure cold."
    ),
    "leonard-sounds-like-writing": (
        "Read your dialogue and prose aloud. Whenever a sentence relies on artificial flourishes or bookish turns of phrase "
        "you would never utter to a companion, strip it back to spoken cadence."
    ),
    "oliver-summer-day-ending": (
        "Conclude a meditation on mortality by posing a direct, unanswerable question to the reader. "
        "Pair the terrifying brevity of life with two unexpected, vibrant adjectives."
    ),
    "white-charlottes-web-opening": (
        "Open a story with an overheard domestic question that contains an instrument of slaughter. "
        "Setting the threat against morning breakfast plates establishes immediate narrative dread."
    )
}

def apply_revisions():
    with open(CARDS_FILE, "r", encoding="utf-8") as f:
        cards = json.load(f)

    updated = 0
    for c in cards:
        cid = c.get("id")
        if cid in REVISIONS:
            c["stealIt"] = REVISIONS[cid]
            updated += 1

    with open(CARDS_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=2, ensure_ascii=False)

    print(f"Successfully revised {updated} cards in content/cards.json.")

if __name__ == "__main__":
    apply_revisions()
