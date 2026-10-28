# curate_cluster_37.py — Curates 20 vetted quotes from Cluster 37 into quote-bank.json
# Usage: python3 scripts/curate_cluster_37.py
#
# Books:
# - Love Is a Dog from Hell by Charles Bukowski (1977)
# - Timequake by Kurt Vonnegut (1997)
# - The School of Life: An Emotional Education by Alain de Botton (2019)
# - Welcome to the Monkey House by Kurt Vonnegut (1968)
# - Red Rising by Pierce Brown (2014)

import json
from pathlib import Path

QUOTE_BANK = Path("content/quote-bank.json")

NEW_QUOTES = [
    # --- Charles Bukowski: Love Is a Dog from Hell (1977) ---
    {
        "quote": "It was still 103 degrees. When I opened my mail I found my auto insurance company wanted $76 more.",
        "author": "Charles Bukowski",
        "work": "Love Is a Dog from Hell",
        "year": 1977,
        "hook": "How to anchor existential dread in petty arithmetic",
        "why_it_lands": "The sweltering physical oppression of triple-digit heat collides directly with the small, persistent sting of a postal bill. Bukowski knows psychological ruin rarely arrives as grand tragedy; it arrives as eighty dollars you do not have on an unbearable Tuesday afternoon.",
        "tags": ["prose-rhythm", "sensory-detail", "candor"]
    },
    {
        "quote": "people are not good to each other. the rich are not good to the rich the poor are not good to the poor.",
        "author": "Charles Bukowski",
        "work": "Love Is a Dog from Hell",
        "year": 1977,
        "hook": "How to strip human solidarity down to cold observation",
        "why_it_lands": "No grand moral excuse, no sociological rescue. By repeating the exact same syntactic clause across classes, Bukowski strips away romantic illusions of shared solidarity and leaves behind a flat, unblinking verdict on human friction.",
        "tags": ["candor", "sentence-mechanics", "understatement"]
    },
    {
        "quote": "“it’s good to hear your voice,” she’d say. “it’s good to hear your voice too,” I’d say.",
        "author": "Charles Bukowski",
        "work": "Love Is a Dog from Hell",
        "year": 1977,
        "hook": "How to expose emotional weariness through mechanical repetition",
        "why_it_lands": "The symmetrical dialogue functions like an automatic handshake across a phone line. By mirroring the two phrases without a single descriptive adverb, Bukowski makes intimacy sound like an echo in an empty hallway.",
        "tags": ["dialogue", "understatement", "prose-rhythm"]
    },
    {
        "quote": "Hank, nobody loves you if you don’t have money.",
        "author": "Charles Bukowski",
        "work": "Love Is a Dog from Hell",
        "year": 1977,
        "hook": "How to cut straight to the transactional bone",
        "why_it_lands": "Spoken by a lover or a creditor, the sentence strips romantic pretension down to zero. The direct vocative address paired with an unsparing economic absolute delivers the flat slap of street reality.",
        "tags": ["candor", "dialogue", "brevity"]
    },

    # --- Kurt Vonnegut: Timequake (1997) ---
    {
        "quote": "Only when free will kicked in again could they stop running obstacle courses of their own construction.",
        "author": "Kurt Vonnegut",
        "work": "Timequake",
        "year": 1997,
        "hook": "How to diagnose self-inflicted ritual",
        "why_it_lands": "Vonnegut turns autonomy into an exhausting physical trial. The term 'obstacle courses of their own construction' captures human habit as voluntary imprisonment, rescued only by the terrifying return of actual choice.",
        "tags": ["irony", "philosophical-depth", "observation"]
    },
    {
        "quote": "It’s true. Actors know everything they are going to say and do, and how everything is going to come out in the end, for good or ill, when the curtain goes up on Act One, Scene One.",
        "author": "Kurt Vonnegut",
        "work": "Timequake",
        "year": 1997,
        "hook": "How to render determinism through theatrical craft",
        "why_it_lands": "Vonnegut equates the dread of cosmic fate with the professional burden of an actor. The foreknowledge of disaster does not stop the lines from being spoken; it turns performance into a prolonged, inevitable sentence.",
        "tags": ["metaphor", "existential-craft", "irony"]
    },
    {
        "quote": "Listen, if it isn't a timequake dragging us through knothole after knothole, it’s something else just as mean and powerful.",
        "author": "Kurt Vonnegut",
        "work": "Timequake",
        "year": 1997,
        "hook": "How to establish folksy fatalism",
        "why_it_lands": "The term 'knothole' grounds cosmic catastrophe in midwestern carpentry. It gives existential pressure physical splinters and friction, making abstract doom feel like an abrasive fence post.",
        "tags": ["vernacular", "voice", "metaphor"]
    },
    {
        "quote": "“I only regret that I have but one life to lose for my country,” said the American patriot Nathan Hale. “Fuck the bums!” said the American patriot Kilgore Trout.",
        "author": "Kurt Vonnegut",
        "work": "Timequake",
        "year": 1997,
        "hook": "How to puncture monumentality with vulgar counterpoint",
        "why_it_lands": "The parallel structure sets textbook high-school nobility directly against the gutter philosopher's unfiltered screech. The symmetry of the attributions ('said the American patriot...') makes the second blow land with twice the satirical velocity.",
        "tags": ["satire", "juxtaposition", "sentence-mechanics"]
    },

    # --- Alain de Botton: The School of Life: An Emotional Education (2019) ---
    {
        "quote": "We have the technology of an advanced civilization balancing precariously on an emotional base that has not developed much since we dwelt in caves.",
        "author": "Alain de Botton",
        "work": "The School of Life: An Emotional Education",
        "year": 2019,
        "hook": "How to dramatize civilizational asymmetry",
        "why_it_lands": "The architecture of the sentence—balancing titanium satellites on primeval bedrock—gives psychological fragility the scale of a planetary engineering flaw.",
        "tags": ["metaphor", "observation", "perspective"]
    },
    {
        "quote": "If a parent shouts at us, the foundations of the earth tremble.",
        "author": "Alain de Botton",
        "work": "The School of Life: An Emotional Education",
        "year": 2019,
        "hook": "How to capture a child's psychological scale",
        "why_it_lands": "To an adult, a raised voice is an irritation; to a small child, it is tectonic plate collapse. De Botton uses planetary hyperbole not for drama, but to measure the literal cognitive reality of dependent childhood.",
        "tags": ["perspective", "psychological-truth", "brevity"]
    },
    {
        "quote": "It is easy to imagine we know what we think, what we feel, and what’s going on in our heads. But we rarely do entirely.",
        "author": "Alain de Botton",
        "work": "The School of Life: An Emotional Education",
        "year": 2019,
        "hook": "How to puncture cognitive complacency",
        "why_it_lands": "A tranquil two-stroke demolition. The first sentence flatters our illusion of internal transparency; the second pulls the rug with the quiet restraint of 'rarely do entirely.'",
        "tags": ["understatement", "psychological-truth", "candor"]
    },
    {
        "quote": "It is always better to touch the ur-argument than for a relationship to die by a thousand squabbles.",
        "author": "Alain de Botton",
        "work": "The School of Life: An Emotional Education",
        "year": 2019,
        "hook": "How to name the root cause of friction",
        "why_it_lands": "By contrasting the single foundational injury ('the ur-argument') with the slow, death-by-attrition erosion of domestic sniping, de Botton offers both an anatomy of intimacy and an urgent plea for courageous confrontation.",
        "tags": ["intimacy", "observation", "clarity"]
    },

    # --- Kurt Vonnegut: Welcome to the Monkey House (1968) ---
    {
        "quote": "It’s a good way to grow up fast. Took me about six months to find out I was killing myself for peanuts, that a little guy couldn't even save a village three blocks long, and that the world wasn't worth saving anyway. So I started looking out for Number One.",
        "author": "Kurt Vonnegut",
        "work": "Welcome to the Monkey House",
        "year": 1968,
        "hook": "How to chart the arithmetic of disillusionment",
        "why_it_lands": "Three rapid clauses map the trajectory from adolescent altruism to survivalist cynicism. Vonnegut doesn't mourn the lost idealism; he documents its deflation like a tire losing air on a highway.",
        "tags": ["voice", "pacing", "candor"]
    },
    {
        "quote": "The deer is not on the payroll—he isn't going to wait for you.",
        "author": "Kurt Vonnegut",
        "work": "Welcome to the Monkey House",
        "year": 1968,
        "hook": "How to humble human vanity through wildlife economy",
        "why_it_lands": "A brilliant collision between the logic of office employment and the indifferent rhythm of the forest. The humor lies in the deadpan assumption that nature might observe corporate punctuality.",
        "tags": ["deadpan", "metaphor", "irony"]
    },
    {
        "quote": "He looked like a machine, but he was a whole lot less like a machine than plenty of people I could name.",
        "author": "Kurt Vonnegut",
        "work": "Welcome to the Monkey House",
        "year": 1968,
        "hook": "How to turn mechanical comparison into moral verdict",
        "why_it_lands": "An elegant inversion of the classic sci-fi trope. By redirecting the accusation of mechanization from the metal object back onto polite society, Vonnegut delivers a sharp appraisal of everyday human numbness.",
        "tags": ["irony", "satire", "observation"]
    },
    {
        "quote": "Just because you have talent, it doesn’t mean that you have to do something with it.",
        "author": "Kurt Vonnegut",
        "work": "Welcome to the Monkey House",
        "year": 1968,
        "hook": "How to emancipate art from obligation",
        "why_it_lands": "A startling heresy in an achievement-obsessed culture. Vonnegut separates gift from utility, suggesting that the societal pressure to exploit a capability often destroys the joy of simply possessing it.",
        "tags": ["paradox", "craft", "brevity"]
    },

    # --- Pierce Brown: Red Rising (2014) ---
    {
        "quote": "Patience is the better part of valor. And obedience the better part of humanity.",
        "author": "Pierce Brown",
        "work": "Red Rising",
        "year": 2014,
        "hook": "How to invert classic maxims into ideological poison",
        "why_it_lands": "The first sentence borrows familiar Shakespearean wisdom; the second attaches a horrifying addendum that turns survival virtue into a tool of enslavement. The syntactic symmetry disguises tyranny as philosophy.",
        "tags": ["subversion", "sentence-mechanics", "irony"]
    },
    {
        "quote": "They’ll preach caution. As if caution has ever helped them. We haven’t won a Laurel in ages.",
        "author": "Pierce Brown",
        "work": "Red Rising",
        "year": 2014,
        "hook": "How to capture youthful defiance in clipped cadence",
        "why_it_lands": "Short, percussive sentences mirror an impatient heartbeat. The transition from defensive elders to practical defeat ('We haven’t won...') grounds generational rebellion in humiliating history.",
        "tags": ["cadence", "voice", "pacing"]
    },
    {
        "quote": "The toughest ant is yet but an ant.",
        "author": "Pierce Brown",
        "work": "Red Rising",
        "year": 2014,
        "hook": "How to crush individual distinction with scale",
        "why_it_lands": "Seven monosyllables that reduce exceptional effort to irrelevance. The proverb illustrates how totalitarian hierarchies view the most capable underdog: not as a threat, but as an easily stepped-on specimen.",
        "tags": ["brevity", "metaphor", "candor"]
    },
    {
        "quote": "We have to leave the castle to get it, Sir Numbnuts. A real siege? We’d last five days without replenishing our water. Seven if we drank the animals’ blood before the salt jacks us up.",
        "author": "Pierce Brown",
        "work": "Red Rising",
        "year": 2014,
        "hook": "How to puncture military romanticism with grim logistics",
        "why_it_lands": "The insolent insult ('Sir Numbnuts') pairs with brutal siege arithmetic. Brown sweeps away heroic martial fantasy with the literal gallon count of drinking water and animal blood.",
        "tags": ["dialogue", "realism", "candor"]
    }
]

def main():
    with open(QUOTE_BANK, "r", encoding="utf-8") as f:
        bank = json.load(f)

    existing_quotes = {q["quote"].strip().lower() for q in bank}
    added = 0
    for q in NEW_QUOTES:
        if q["quote"].strip().lower() not in existing_quotes:
            bank.append(q)
            existing_quotes.add(q["quote"].strip().lower())
            added += 1

    with open(QUOTE_BANK, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)

    print(f"Appended {added} new vetted quotes to {QUOTE_BANK}. Total bank size: {len(bank)}")

if __name__ == "__main__":
    main()
