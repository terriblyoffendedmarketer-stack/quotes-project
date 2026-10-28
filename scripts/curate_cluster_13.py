#!/usr/bin/env python3
"""
curate_cluster_13.py — Curates 20 vetted quotes from Cluster 13 (Time, Meaning & Polyphonic Fiction)
into content/quote-bank.json.
"""

import json
from pathlib import Path

QUOTE_BANK_PATH = Path("/Users/apple/Documents/Claude Code/quotes-project/content/quote-bank.json")

NEW_QUOTES = [
    # David Mitchell — Cloud Atlas
    {
        "quote": "A time is one’s own, Eva, when oneself and one’s peers take the same things for granted, without thinking about it. Likewise, a man is ruined when the times change but he does not.",
        "author": "David Mitchell",
        "work": "Cloud Atlas",
        "year": 2004,
        "translator": None,
        "hook": "How to define historical obsolescence as a failure of shared assumptions.",
        "why_it_lands": "Mitchell locates generational belonging not in fashion or technology, but in unexamined consensus. The paired structure ('A time is one’s own... Likewise, a man is ruined...') links private identity directly to cultural velocity.",
        "tags": ["time", "sociology", "syntax", "loss"]
    },
    {
        "quote": "‘You are welcome here, most welcome,’ she told me, ‘but you must understand that the world is not built for such things as kindness.’",
        "author": "David Mitchell",
        "work": "Cloud Atlas",
        "year": 2004,
        "translator": None,
        "hook": "How to strip benevolence of sentimental protection.",
        "why_it_lands": "The sentence begins with unconditional domestic hospitality, only to pivot instantly to a bleak cosmological reality. Kindness is acknowledged as genuine, yet structurally mismatched with the physics of the world.",
        "tags": ["dialogue", "contrast", "worldbuilding", "voice"]
    },
    {
        "quote": "‘I ain’t got no right to ask you for favors, I ain’t been a good host, nay I been a pisspoor bad un, but … I’d ran out o’ words.’",
        "author": "David Mitchell",
        "work": "Cloud Atlas",
        "year": 2004,
        "translator": None,
        "hook": "How to express rural vulnerability through verbal depletion.",
        "why_it_lands": "Mitchell crafts dialect that bypasses rustic caricature to expose raw emotional bankruptcy. Running out of words is rendered not as an intellectual failing, but as an existential drought.",
        "tags": ["vernacular", "vulnerability", "character-voice", "honesty"]
    },
    {
        "quote": "Houses like these secrete some dark sorcery that transforms their owners into fruitcakes.",
        "author": "David Mitchell",
        "work": "Cloud Atlas",
        "year": 2004,
        "translator": None,
        "hook": "How to personify gothic architecture as an active corrupting agent.",
        "why_it_lands": "The biological verb 'secrete' gives the architecture glandular, physical agency. Mitchell contrasts archaic gothic menace with the cheeky slang 'fruitcakes', deflating pretentious atmosphere into comic dread.",
        "tags": ["verb-choice", "humor", "personification", "setting"]
    },

    # Viktor E. Frankl — Man's Search for Meaning
    {
        "quote": "Freedom is only part of the story and half of the truth. Freedom is but the negative aspect of the whole phenomenon whose positive aspect is responsibleness.",
        "author": "Viktor E. Frankl",
        "work": "Man's Search for Meaning",
        "year": 1946,
        "translator": "Ilse Lasch",
        "hook": "How to counterbalance liberty with ethical weight.",
        "why_it_lands": "Frankl refuses the romantic glorification of liberty. By framing freedom as merely the removal of restraint (negative) and responsibility as the act of commitment (positive), the aphorism demands moral consequence.",
        "tags": ["philosophy", "balance", "moral-weight", "aphorism"]
    },
    {
        "quote": "The organism digested its own protein, and the muscles disappeared. Then the body had no powers of resistance left.",
        "author": "Viktor E. Frankl",
        "work": "Man's Search for Meaning",
        "year": 1946,
        "translator": "Ilse Lasch",
        "hook": "How to chronicle starvation through clinical biological detachment.",
        "why_it_lands": "Frankl describes physical annihilation not through emotional pleading, but through the calm, terrible autopsy of living tissue. The clinical verb 'digested its own protein' lands with horrifying precision.",
        "tags": ["restraint", "physicality", "precision", "understatement"]
    },
    {
        "quote": "Standing on tiptoe and looking past the others' heads through the bars of the window, I caught an eerie glimpse of my native town.",
        "author": "Viktor E. Frankl",
        "work": "Man's Search for Meaning",
        "year": 1946,
        "translator": "Ilse Lasch",
        "hook": "How to anchor profound dispossession in a physical posture.",
        "why_it_lands": "The physical strain of 'standing on tiptoe' to peer between prison bars contrasts sharply with the intimacy of 'native town'. The familiar home is turned ghostly ('eerie glimpse') precisely when it is closest yet unreachable.",
        "tags": ["sensory-detail", "posture", "exile", "interiority"]
    },
    {
        "quote": "‘He who has a why to live can bear with almost any how.’",
        "author": "Viktor E. Frankl",
        "work": "Man's Search for Meaning",
        "year": 1946,
        "translator": "Ilse Lasch",
        "hook": "How to anchor psychological endurance in teleological purpose.",
        "why_it_lands": "Borrowing Nietzsche's formulation, Frankl transforms abstract philosophy into survival mechanics. The sonic echo ('why' / 'how') binds existential intention directly to biological resilience.",
        "tags": ["aphorism", "endurance", "rhythm", "stoicism"]
    },

    # Seneca — Letters on Ethics (Letters to Lucilius)
    {
        "quote": "As we live, so do we speak.",
        "author": "Seneca",
        "work": "Letters on Ethics (Letters to Lucilius)",
        "year": 65,
        "translator": "Margaret Graver & A.A. Long",
        "hook": "How to diagnose ethical character through prose rhythm.",
        "why_it_lands": "Five words of monosyllabic Latinate balance. Seneca collapses the artificial divide between rhetorical style and moral integrity: syntactic decay is simply the acoustic signature of personal corruption.",
        "tags": ["aphorism", "concision", "craft-rule", "style"]
    },
    {
        "quote": "Decadence in language is a sure sign of widespread self-indulgence if it is not found in just one or two but meets with general approval.",
        "author": "Seneca",
        "work": "Letters on Ethics (Letters to Lucilius)",
        "year": 65,
        "translator": "Margaret Graver & A.A. Long",
        "hook": "How to treat linguistic corruption as a symptom of civic decay.",
        "why_it_lands": "Seneca treats grammar and vocabulary as public health metrics. When ornate, evasive phrasing becomes collective practice, stylistic degeneracy ceases to be personal taste and becomes cultural decay.",
        "tags": ["cultural-critique", "clarity", "style", "insight"]
    },
    {
        "quote": "Life, Lucilius, is a campaign. That is why those who endure the trials, march uphill and down through rough country, and put themselves into the most dangerous sorties are the heroes and leaders of the camp.",
        "author": "Seneca",
        "work": "Letters on Ethics (Letters to Lucilius)",
        "year": 65,
        "translator": "Margaret Graver & A.A. Long",
        "hook": "How to frame human endurance as military topography.",
        "why_it_lands": "The Roman martial metaphor ('march uphill and down through rough country') physicalizes moral struggle. Adversity is not an unexpected interruption of life; it is the terrain of the assignment.",
        "tags": ["metaphor", "stoicism", "cadence", "action"]
    },
    {
        "quote": "‘Prosperity is a restless thing; it drives itself to distraction.’",
        "author": "Seneca",
        "work": "Letters on Ethics (Letters to Lucilius)",
        "year": 65,
        "translator": "Margaret Graver & A.A. Long",
        "hook": "How to expose the kinetic agitation of worldly success.",
        "why_it_lands": "Seneca strips good fortune of its serene reputation. Wealth and advancement are diagnosed not as states of peace, but as perpetual motion machines of anxiety that consume their own possessor.",
        "tags": ["paradox", "psychology", "inversion", "ambition"]
    },

    # Percival Everett — The Trees
    {
        "quote": "I ain’t got no watch, but it was early. The ground was still dew wet. My boot toes was dark.",
        "author": "Percival Everett",
        "work": "The Trees",
        "year": 2021,
        "translator": None,
        "hook": "How to calibrate time through sensory ground contact.",
        "why_it_lands": "Everett rejects mechanical timepieces for physical indicators: moisture on grass, darkening leather. The staccato clauses give rural witness testimony an unshakeable, tactile reality.",
        "tags": ["sensory-detail", "time", "vernacular", "rhythm"]
    },
    {
        "quote": "That’s simple. It’s because we ain’t had us an election since I was elected.",
        "author": "Percival Everett",
        "work": "The Trees",
        "year": 2021,
        "translator": None,
        "hook": "How to deliver deadpan authoritarian satire in a single line.",
        "why_it_lands": "Everett exposes tyrannical entitlement not with indignant lecturing, but with folksy, matter-of-fact circularity. The corruption is admitted with such casual ease that the listener is shocked into laughter.",
        "tags": ["deadpan", "satire", "political-voice", "dialogue"]
    },
    {
        "quote": "There’s got to be some perk for everybody hating you.",
        "author": "Percival Everett",
        "work": "The Trees",
        "year": 2021,
        "translator": None,
        "hook": "How to balance isolation with grim operational humor.",
        "why_it_lands": "An investigator operating in hostile territory converts ostracism into tactical leverage. The line carries the dry, weary pragmatism of someone who has abandoned any expectation of goodwill.",
        "tags": ["irony", "character-voice", "humor", "resilience"]
    },
    {
        "quote": "They’s right, That Obamacare don’t work worth a hill of puppy shit. We done bought in, causin’ we had to, and I ain’t lost nary a pound.",
        "author": "Percival Everett",
        "work": "The Trees",
        "year": 2021,
        "translator": None,
        "hook": "How to reveal ideological absurdity through physical misunderstanding.",
        "why_it_lands": "Political resentment is skewered by reducing national healthcare reform to a failed diet plan. The earthy colloquialism ('hill of puppy shit') contrasts against the sheer category error with brutal comic timing.",
        "tags": ["satire", "colloquialism", "comic-timing", "dialogue"]
    },

    # James Gleick — Chaos: Making a New Science
    {
        "quote": "The behavior actually had an exquisite fine structure, yet any piece of it seemed indistinguishable from noise.",
        "author": "James Gleick",
        "work": "Chaos: Making a New Science",
        "year": 1987,
        "translator": None,
        "hook": "How to define hidden order within apparent turbulence.",
        "why_it_lands": "Gleick captures the philosophical paradox of nonlinear dynamics: chaos is not randomness; it is intricate architecture viewed through an inadequate lens. The contrast between 'exquisite fine structure' and 'noise' defines the paradigm shift.",
        "tags": ["paradox", "science-writing", "clarity", "contrast"]
    },
    {
        "quote": "The numbers were converging geometrically, the way a line of identical telephone poles converges toward the horizon in a perspective drawing.",
        "author": "James Gleick",
        "work": "Chaos: Making a New Science",
        "year": 1987,
        "translator": None,
        "hook": "How to translate abstract mathematical convergence into physical perspective.",
        "why_it_lands": "Gleick rescues quantitative scaling from abstraction by comparing Feigenbaum constants to telephone poles receding along a country road. The visual metaphor gives mathematical proof immediate optical depth.",
        "tags": ["metaphor", "visualization", "science-writing", "simplicity"]
    },
    {
        "quote": "Wherever two colors try to come together, the third always inserts itself, with a series of new, self-similar intrusions.",
        "author": "James Gleick",
        "work": "Chaos: Making a New Science",
        "year": 1987,
        "translator": None,
        "hook": "How to describe fractal geometry through persistent physical intrusion.",
        "why_it_lands": "Gleick describes dynamic boundary basins not with topology jargon, but as competitive agents jostling for space. The active verb 'inserts itself' makes mathematical recursion feel kinetic and alive.",
        "tags": ["animation", "imagery", "precision", "clarity"]
    },
    {
        "quote": "It was as if a marble, caught between the conflicting tugs of two nearby valleys, would end up in the third and most distant valley instead.",
        "author": "James Gleick",
        "work": "Chaos: Making a New Science",
        "year": 1987,
        "translator": None,
        "hook": "How to explain nonlinear dynamics through gravitational surprise.",
        "why_it_lands": "A simple domestic object (a rolling marble) illustrates counterintuitive sensitivity to initial conditions. Gleick leads the reader through physical expectation only to subvert it with the 'third and most distant valley'.",
        "tags": ["analogy", "didactic-craft", "surprise", "clarity"]
    }
]

def main():
    with open(QUOTE_BANK_PATH, "r", encoding="utf-8") as f:
        existing = json.load(f)

    existing_texts = {q["quote"].strip() for q in existing}
    added = 0
    for q in NEW_QUOTES:
        if q["quote"].strip() not in existing_texts:
            existing.append(q)
            existing_texts.add(q["quote"].strip())
            added += 1

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"Added {added} new quotes. Quote bank total: {len(existing)}")

if __name__ == "__main__":
    main()
