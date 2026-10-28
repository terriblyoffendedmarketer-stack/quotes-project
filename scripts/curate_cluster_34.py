# scripts/curate_cluster_34.py — Curates 20 craft quotes from Cluster 34 (Physical Discipline, Doomsday Satire & Grief)
# Usage: python3 scripts/curate_cluster_34.py
# Requires: json, os

import json
import os

QUOTE_BANK_PATH = "content/quote-bank.json"

VETTED_CLUSTER_34 = [
    # 1. Haruki Murakami — What I Talk About When I Talk About Running (2007), trans. Philip Gabriel
    {
        "quote": "Muscles are like work animals that are quick on the uptake. If you carefully increase the load, step by step, they learn to take it.",
        "author": "Haruki Murakami",
        "work": "What I Talk About When I Talk About Running",
        "year": 2007,
        "translator": "Philip Gabriel",
        "hook": "How to conceptualize physical discipline as patient animal domestication.",
        "why_it_lands": "Murakami demystifies athletic endurance into gentle routine: physical capacity isn't forged through violent willpower, but through steady, incremental negotiation with obedient bodily tissue.",
        "tags": ["discipline", "body", "habit", "metaphor"]
    },
    {
        "quote": "Not enough training. Not enough training. And not enough training. That’s it in a word.",
        "author": "Haruki Murakami",
        "work": "What I Talk About When I Talk About Running",
        "year": 2007,
        "translator": "Philip Gabriel",
        "hook": "How to strip away rationalization through blunt rhythmic repetition.",
        "why_it_lands": "Murakami refuses self-pity after athletic failure, using staccato threefold repetition to reduce complex psychological excuses down to an unarguable physical deficit.",
        "tags": ["repetition", "rhythm", "honesty", "brevity"]
    },
    {
        "quote": "The surface of the water changes from day to day: the color, the shape of the waves, the speed of the current.",
        "author": "Haruki Murakami",
        "work": "What I Talk About When I Talk About Running",
        "year": 2007,
        "translator": "Philip Gabriel",
        "hook": "How to record environmental flux through quiet sensory cataloging.",
        "why_it_lands": "Murakami captures the runner's shifting backdrop through calm, steady cadence, noting how repetitive physical circuits attune the senses to microscopic natural variations.",
        "tags": ["observation", "nature", "cadence", "detail"]
    },
    {
        "quote": "They’re too busy eating grass to care about all these whimsical people and their nonsensical activities.",
        "author": "Haruki Murakami",
        "work": "What I Talk About When I Talk About Running",
        "year": 2007,
        "translator": "Philip Gabriel",
        "hook": "How to humble human vanity against pastoral indifference.",
        "why_it_lands": "Murakami undercuts the self-importance of marathon racing by contrasting puffed-up human ambition against cattle grazing peacefully on the roadside, completely unimpressed.",
        "tags": ["humor", "perspective", "nature", "irony"]
    },

    # 2. Kurt Vonnegut — Cat's Cradle (1963)
    {
        "quote": "The hand that stocks the drug stores rules the world.",
        "author": "Kurt Vonnegut",
        "work": "Cat's Cradle",
        "year": 1963,
        "translator": None,
        "hook": "How to summarize modern empire through commercial retail distribution.",
        "why_it_lands": "Vonnegut satirizes geopolitical dominance with deadpan domestic irony: sovereign power does not belong to ideological figureheads, but to whoever controls the logistical supply of aspirin and tranquilizers.",
        "tags": ["satire", "power", "irony", "brevity"]
    },
    {
        "quote": "I couldn’t think of anything to say that would interest anybody reading a book. I could have made up something about that day, but I didn’t think you’d want that.",
        "author": "Kurt Vonnegut",
        "work": "Cat's Cradle",
        "year": 1963,
        "translator": None,
        "hook": "How to build narrative intimacy through candid authorial embarrassment.",
        "why_it_lands": "Vonnegut punctures literary pretension by admitting dead air directly to the reader, gaining immediate trust through conversational modesty rather than synthetic drama.",
        "tags": ["metafiction", "voice", "candor", "irony"]
    },
    {
        "quote": "Mona has the simplicity of the all.",
        "author": "Kurt Vonnegut",
        "work": "Cat's Cradle",
        "year": 1963,
        "translator": None,
        "hook": "How to elevate character beauty into cosmic abstraction in seven words.",
        "why_it_lands": "Vonnegut achieves poetic weight through paradoxical economy: total innocence and absolute complexity collapse into an unforgettable single phrase.",
        "tags": ["brevity", "character", "paradox", "poetics"]
    },
    {
        "quote": "The luxurious pleasure craft was going down, and my meaningless life with it.",
        "author": "Kurt Vonnegut",
        "work": "Cat's Cradle",
        "year": 1963,
        "translator": None,
        "hook": "How to synchronize physical shipwreck with existential despair.",
        "why_it_lands": "Vonnegut balances dark comedy on the brink of disaster: coupling an opulent yacht with an empty personal trajectory yields bitter, laughing fatalism.",
        "tags": ["satire", "dark humor", "fate", "irony"]
    },

    # 3. Umberto Eco — Chronicles of a Liquid Society (2016), trans. Richard Dixon
    {
        "quote": "Such indignation knows what it doesn’t want, but not what it does.",
        "author": "Umberto Eco",
        "work": "Chronicles of a Liquid Society",
        "year": 2016,
        "translator": "Richard Dixon",
        "hook": "How to diagnose reactive political outrage through structural negation.",
        "why_it_lands": "Eco isolates the core pathology of modern populism in ten words: anger functions purely as explosive rejection without possessing the coherent architectural will to construct an alternative.",
        "tags": ["critique", "clarity", "politics", "truth"]
    },
    {
        "quote": "A book as object can tell a good story even when it’s been around for only fifty years.",
        "author": "Umberto Eco",
        "work": "Chronicles of a Liquid Society",
        "year": 2016,
        "translator": "Richard Dixon",
        "hook": "How to defend the material dignity of contemporary print.",
        "why_it_lands": "Eco reminds the bibliophile that book history doesn't require incunabula or vellum: twentieth-century paperbacks carry their own textured fingerprints, margin notes, and physical biographies.",
        "tags": ["books", "objects", "materiality", "reading"]
    },
    {
        "quote": "Seers see what they know.",
        "author": "Umberto Eco",
        "work": "Chronicles of a Liquid Society",
        "year": 2016,
        "translator": "Richard Dixon",
        "hook": "How to dismantle mystical prophecy into perceptual bias in five words.",
        "why_it_lands": "Eco compresses epistemological skepticism into an airtight aphorism: prophetic visions never reveal unmediated future truth, but simply project the visionary's pre-existing cultural library onto empty clouds.",
        "tags": ["epistemology", "brevity", "wit", "truth"]
    },
    {
        "quote": "Thrusting a cell phone into someone’s mouth is like a kick in the testicles: the cell phone is the most intimate and personal thing he possesses, the natural complement to his ear, his eye, and also of his penis.",
        "author": "Umberto Eco",
        "work": "Chronicles of a Liquid Society",
        "year": 2016,
        "translator": "Richard Dixon",
        "hook": "How to expose technological intimacy through grotesque sensory comparison.",
        "why_it_lands": "Eco shocks the reader into recognizing technological embodiment: the digital handset is no longer an external appliance, but an organ grafting directly onto human privacy and physical vulnerability.",
        "tags": ["satire", "modernity", "grotesque", "technology"]
    },

    # 4. Patrick Ness — A Monster Calls (2011)
    {
        "quote": "Stories are wild creatures, when you let them loose, who knows what havoc they might wreak?",
        "author": "Patrick Ness",
        "work": "A Monster Calls",
        "year": 2011,
        "translator": None,
        "hook": "How to define narrative as an untamed biological hazard.",
        "why_it_lands": "Ness strips fiction of cozy domestic safety, framing storytelling as an autonomous feral beast that mauls the teller's intentions the instant it escapes into the wild.",
        "tags": ["storytelling", "metaphor", "power", "danger"]
    },
    {
        "quote": "You be as angry as you need to be. Don’t let anyone tell you otherwise. Not your grandma, not your dad, no one. And if you need to break things, then by God, you break them good and hard.",
        "author": "Patrick Ness",
        "work": "A Monster Calls",
        "year": 2011,
        "translator": None,
        "hook": "How to grant unconditional permission for catastrophic grief.",
        "why_it_lands": "Ness shatters the polite domestic demands placed on grieving children, offering absolute validation for destructive sorrow with rhythmic, unapologetic cadence.",
        "tags": ["grief", "voice", "permission", "dialogue"]
    },
    {
        "quote": "It was like the time Conor and his mum had stayed in a bed and breakfast one summer in Cornwall. Except cleaner. And bossier.",
        "author": "Patrick Ness",
        "work": "A Monster Calls",
        "year": 2011,
        "translator": None,
        "hook": "How to sketch domestic tension through childhood vacation comparison.",
        "why_it_lands": "Ness grounds an alienated boy's discomfort in crisp sensory humor: two punchy comparative fragments capture the grandmother's suffocating, pristine sterility far better than an essay.",
        "tags": ["character", "humor", "childhood", "contrast"]
    },
    {
        "quote": "So come and get me then, he said.",
        "author": "Patrick Ness",
        "work": "A Monster Calls",
        "year": 2011,
        "translator": None,
        "hook": "How to deliver exhausted emotional defiance in seven monosyllables.",
        "why_it_lands": "Ness conveys the threshold where terror turns into cold calm: when an adolescent boy has suffered beyond capacity, monstrous confrontation ceases to terrify and becomes a form of relief.",
        "tags": ["brevity", "courage", "dialogue", "defiance"]
    },

    # 5. Frederick P. Brooks Jr. — The Mythical Man-Month (1975)
    {
        "quote": "Adding manpower to a late software project makes it later.",
        "author": "Frederick P. Brooks Jr.",
        "work": "The Mythical Man-Month",
        "year": 1975,
        "translator": None,
        "hook": "How to formulate an ironclad organizational paradox in nine words.",
        "why_it_lands": "Brooks's eponymous law endures because it strips managerial intuition bare: complex creative systems obey communication combinatorics, not assembly-line division of labor.",
        "tags": ["systems", "paradox", "brevity", "truth"]
    },
    {
        "quote": "Most documentation fails in giving too little overview. The trees are described, the bark and leaves are commented, but there is no map of the forest.",
        "author": "Frederick P. Brooks Jr.",
        "work": "The Mythical Man-Month",
        "year": 1975,
        "translator": None,
        "hook": "How to diagnose structural explanation failure through ecological scale.",
        "why_it_lands": "Brooks captures why technical writing so frequently confuses readers: authors obsessively dissect microscopic leaves and bark while completely forgetting to provide an aerial navigation chart.",
        "tags": ["craft", "clarity", "explanation", "metaphor"]
    },
    {
        "quote": "The hardest part of the software task is arriving at a complete and consistent specification, and much of the essence of building a program is in fact the debugging of the specification.",
        "author": "Frederick P. Brooks Jr.",
        "work": "The Mythical Man-Month",
        "year": 1975,
        "translator": None,
        "hook": "How to reframe engineering difficulty as linguistic articulation.",
        "why_it_lands": "Brooks elevates systems architecture to literary craft: the true battle is never keyboard syntax, but conceptual clarity—debugging human thoughts before a single line is executed.",
        "tags": ["clarity", "thinking", "specification", "architecture"]
    },
    {
        "quote": "The higher the level at which one thinks, the more numerous the primitive thought-elements one has to deal with.",
        "author": "Frederick P. Brooks Jr.",
        "work": "The Mythical Man-Month",
        "year": 1975,
        "translator": None,
        "hook": "How to identify the deceptive trap of high-level abstraction.",
        "why_it_lands": "Brooks dismantles the illusion of simplicity at high levels of abstraction: moving to higher conceptual summits doesn't eliminate messy details, but exponentially multiplies the underlying foundations that must remain sound.",
        "tags": ["abstraction", "philosophy", "systems", "intellect"]
    }
]

def main():
    if not os.path.exists(QUOTE_BANK_PATH):
        print(f"Error: {QUOTE_BANK_PATH} not found.")
        return

    with open(QUOTE_BANK_PATH, "r", encoding="utf-8") as f:
        bank = json.load(f)

    print(f"Current quote bank count: {len(bank)}")

    # Check for duplicates
    existing_quotes = {q["quote"].strip() for q in bank}
    added = 0
    for q in VETTED_CLUSTER_34:
        if q["quote"].strip() not in existing_quotes:
            bank.append(q)
            existing_quotes.add(q["quote"].strip())
            added += 1
        else:
            print(f"Skipping duplicate: {q['quote'][:40]}...")

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)

    print(f"Successfully added {added} quotes from Cluster 34.")
    print(f"New quote bank total: {len(bank)}")

if __name__ == "__main__":
    main()
