#!/usr/bin/env python3
"""
curate_cluster_10.py — Curates 20 vetted quotes from Cluster 10 (Contemporary East Asian Voices)
into content/quote-bank.json.
"""

import json
from pathlib import Path

QUOTE_BANK_PATH = Path("/Users/apple/Documents/Claude Code/quotes-project/content/quote-bank.json")

NEW_QUOTES = [
    # Won-pyung Sohn — Almond
    {
        "quote": "“He could die,” I said, fiddling with one of the chewy caramel packs neatly lined up on the display stand.",
        "author": "Won-pyung Sohn",
        "work": "Almond",
        "year": 2017,
        "translator": "Sandy Joosun Lee",
        "hook": "How to anchor indifference through a sensory domestic detail.",
        "why_it_lands": "The physical act of straightening confectionery while calmly discussing another human being's mortality creates an immediate chill; the sentence refuses sentimentality by letting the trivial object carry the narrator's neurological inability to fear.",
        "tags": ["tone", "juxtaposition", "understatement", "character-voice"]
    },
    {
        "quote": "Darkness in winter settled quickly. One moment you noticed it gathering, the next moment everything turned inky black.",
        "author": "Won-pyung Sohn",
        "work": "Almond",
        "year": 2017,
        "translator": "Sandy Joosun Lee",
        "hook": "How to capture sudden threshold changes in two clean beats.",
        "why_it_lands": "Sohn doesn't describe twilight as a slow gradient; she splits time into two stark states—noticing the gathering, then total blackness. The cadence mirrors how abrupt sensory shifts register in an observant mind.",
        "tags": ["pacing", "setting", "observation", "rhythm"]
    },
    {
        "quote": "There is no such person who can’t be saved. There are only people who give up on trying to save others.",
        "author": "Won-pyung Sohn",
        "work": "Almond",
        "year": 2017,
        "translator": "Sandy Joosun Lee",
        "hook": "How to reverse moral agency through a balanced syntactic shift.",
        "why_it_lands": "The sentence flips the burden from the unsaveable subject to the weary witness. By balancing the negative assertion against an ethical accusation, it turns a platitude into an indictment of collective exhaustion.",
        "tags": ["moral-weight", "syntax", "reversal", "philosophy"]
    },
    {
        "quote": "Every little thing around you might feel like sharp weapons. A subtle expression or a few words could sting you.",
        "author": "Won-pyung Sohn",
        "work": "Almond",
        "year": 2017,
        "translator": "Sandy Joosun Lee",
        "hook": "How to turn social nuance into physical peril.",
        "why_it_lands": "For someone navigating alexithymia, an ambiguous facial expression isn't social friction—it is a blade. The metaphor works because it scales emotional vulnerability down to tactile lacerations.",
        "tags": ["metaphor", "interiority", "vulnerability"]
    },

    # Ken Liu — The Paper Menagerie and Other Stories
    {
        "quote": "It is simultaneously a score and recording. A speech sounds like a speech, a lament a lament, and a story re-creates perfectly the teller’s breathless excitement.",
        "author": "Ken Liu",
        "work": "The Paper Menagerie and Other Stories",
        "year": 2016,
        "translator": None,
        "hook": "How to define an impossible art form through cadence and tripartite rhythm.",
        "why_it_lands": "Liu moves from technical classification into a three-part rhythmic cadence where speech, lament, and story match their own sonic definitions. The language enacts the phenomenon it describes.",
        "tags": ["rhythm", "definition", "worldbuilding", "voice"]
    },
    {
        "quote": "Each mind grows from a seed inherited through the millennia, and every thought leaves a mark that can be read and seen.",
        "author": "Ken Liu",
        "work": "The Paper Menagerie and Other Stories",
        "year": 2016,
        "translator": None,
        "hook": "How to materialize memory across deep time.",
        "why_it_lands": "The sentence joins biological ancestry ('seed inherited') with physical inscription ('read and seen'). Thought is stripped of vapor and given the weight of sedimentary rock.",
        "tags": ["memory", "imagery", "metaphor", "philosophy"]
    },
    {
        "quote": "It is also a trace, something directly stenciled off the real; it is also a footprint or a death mask.",
        "author": "Ken Liu",
        "work": "The Paper Menagerie and Other Stories",
        "year": 2016,
        "translator": None,
        "hook": "How to escalate a definition toward physical finality.",
        "why_it_lands": "The parallel clauses begin with an architectural image ('stenciled off the real') and tighten rapidly into mortality: a transient footprint, then the cold bronze of a death mask. Each noun raises the existential stakes.",
        "tags": ["syntax", "escalation", "imagery", "mortality"]
    },
    {
        "quote": "“We are all now exploiters of the dead,” he said, as if explaining a fundamental law of physics.",
        "author": "Ken Liu",
        "work": "The Paper Menagerie and Other Stories",
        "year": 2016,
        "translator": None,
        "hook": "How to deliver moral horror with thermodynamic calm.",
        "why_it_lands": "The dialogue tag does the heavy lifting. Delivering an ethical atrocity ('exploiters of the dead') with the dry neutrality reserved for entropy or gravity strips the speaker of hysteria, making the indictment inescapable.",
        "tags": ["dialogue-craft", "tone", "understatement", "cynicism"]
    },

    # Hiromi Kawakami — The Ten Loves of Nishino
    {
        "quote": "People have the right to fall in love, but not the right to be loved.",
        "author": "Hiromi Kawakami",
        "work": "The Ten Loves of Nishino",
        "year": 2003,
        "translator": "Allison Markin Powell",
        "hook": "How to split an emotional entitlement down its asymmetric seam.",
        "why_it_lands": "The aphorism cuts clean through romantic mythology. By granting emotional liberty to the lover while denying any reciprocal claim on the beloved, Kawakami restores the true, terrifying risk of desire.",
        "tags": ["aphorism", "syntax", "desire", "clarity"]
    },
    {
        "quote": "Young ladies like me, we tend to think of things in abstraction, much more than most people realize. Inside the shop, there were tanks of tropical fish and goldfish lined up.",
        "author": "Hiromi Kawakami",
        "work": "The Ten Loves of Nishino",
        "year": 2003,
        "translator": "Allison Markin Powell",
        "hook": "How to ground intellectual pretension against a mundane physical backdrop.",
        "why_it_lands": "The narrator begins with self-conscious psychological distance ('think of things in abstraction'), and Kawakami immediately pulls the lens wide to reveal neon tetras and cloudy pet shop glass. The concrete world refuses the abstraction.",
        "tags": ["juxtaposition", "interiority", "irony", "setting"]
    },
    {
        "quote": "There may not have been much advantage in loving Nishino, but there were good times to be had, weren’t there. It was hard work, worth doing.",
        "author": "Hiromi Kawakami",
        "work": "The Ten Loves of Nishino",
        "year": 2003,
        "translator": "Allison Markin Powell",
        "hook": "How to evaluate passion with the plain vocabulary of labor.",
        "why_it_lands": "Kawakami avoids tragic melodrama. Describing romance as an unprofitable task that was nonetheless 'hard work, worth doing' reframes heartbreak as craft—something survived, shaped, and evaluated without self-pity.",
        "tags": ["understatement", "tone", "craft-of-living", "voice"]
    },
    {
        "quote": "“If only I could want all of Nishino,” I murmured.",
        "author": "Hiromi Kawakami",
        "work": "The Ten Loves of Nishino",
        "year": 2003,
        "translator": "Allison Markin Powell",
        "hook": "How to isolate the tragic insufficiency of partial affection.",
        "why_it_lands": "The horror here isn't unrequited love, but incomplete wanting. The small, quiet verb 'murmured' frames the confession as an admission of personal defect—loving someone enough to see them, but not enough to consume them whole.",
        "tags": ["interiority", "longing", "understatement"]
    },

    # Haruki Murakami — Blind Willow, Sleeping Woman
    {
        "quote": "It’s not like the total physical and mental commitment you have to make for the year or two it takes to compose a novel. You merely enter a room, finish your work, and exit. That’s it.",
        "author": "Haruki Murakami",
        "work": "Blind Willow, Sleeping Woman",
        "year": 2006,
        "translator": "Philip Gabriel & Jay Rubin",
        "hook": "How to strip artistic practice of romantic mystique.",
        "why_it_lands": "Murakami treats short fiction not as a sacred trance, but as entering a room, executing the task with surgical economy, and stepping outside. The plain sequence of monosyllabic verbs ('enter... finish... exit') demystifies creation.",
        "tags": ["craft-of-writing", "simplicity", "pacing", "understatement"]
    },
    {
        "quote": "It’s like we fell off a high fence, on the outside. Painlessly, without a sound.",
        "author": "Haruki Murakami",
        "work": "Blind Willow, Sleeping Woman",
        "year": 2006,
        "translator": "Philip Gabriel & Jay Rubin",
        "hook": "How to render profound estrangement through weightless kinetic imagery.",
        "why_it_lands": "Trauma usually comes with shock and noise. Murakami strips out both: the fall is from a high fence, yet lands painlessly and silently on the 'outside.' The lack of friction makes the dislocation all the more eerie.",
        "tags": ["metaphor", "estrangement", "sensory-detail", "mood"]
    },
    {
        "quote": "Everything was out of order, and would never get back to the way it was.",
        "author": "Haruki Murakami",
        "work": "Blind Willow, Sleeping Woman",
        "year": 2006,
        "translator": "Philip Gabriel & Jay Rubin",
        "hook": "How to state irreversible catastrophe with flat monosyllables.",
        "why_it_lands": "There are no ornate adjectives to dress up the devastation. The rhythm moves from a factual diagnosis ('out of order') to a quiet, permanent closure ('never get back to the way it was'). It accepts collapse without pleading.",
        "tags": ["cadence", "grief", "finality", "simplicity"]
    },
    {
        "quote": "“Your work should be an act of love, not a marriage of convenience.”",
        "author": "Haruki Murakami",
        "work": "Blind Willow, Sleeping Woman",
        "year": 2006,
        "translator": "Philip Gabriel & Jay Rubin",
        "hook": "How to set an uncompromised standard for creative labor.",
        "why_it_lands": "A sharp comparison that pits genuine devotion against transactional settlement. By borrowing marital legalism ('marriage of convenience'), the sentence reveals the quiet tragedy of creative compromise.",
        "tags": ["aphorism", "craft", "conviction", "metaphor"]
    },

    # Choi Jin-young — Hunger
    {
        "quote": "Human beings are up for sale. They kill and eat anything. They lie and cheat. They have the power to ruin or save a life.",
        "author": "Choi Jin-young",
        "work": "Hunger",
        "year": 2014,
        "translator": "Soje",
        "hook": "How to open with a staccato litany of human brutality.",
        "why_it_lands": "Four rapid, unembellished sentences that refuse transitions. The rapid-fire inventory moves from commodification to cannibalism to moral deceit, ending on the terrifying arbitrariness of mercy.",
        "tags": ["staccato", "rhythm", "cynicism", "pacing"]
    },
    {
        "quote": "Turns out even dying’s expensive. But you’ll have to keep it on the down-low, or else the fuckers will sell off my corpse.",
        "author": "Choi Jin-young",
        "work": "Hunger",
        "year": 2014,
        "translator": "Soje",
        "hook": "How to lace fatal vulnerability with street-corner insolence.",
        "why_it_lands": "The narrator refuses tragic nobility. By treating death as an overpriced bureaucratic headache and a predatory black market risk, the voice maintains its biting edge even at the threshold of extinction.",
        "tags": ["voice", "black-humor", "survival", "vernacular"]
    },
    {
        "quote": "I wanted to be the only person who knew everything there was to know about Gu. The idea of him feeling something I couldn’t understand, of not occupying his thoughts for a single second, was unbearable and simply unacceptable.",
        "author": "Choi Jin-young",
        "work": "Hunger",
        "year": 2014,
        "translator": "Soje",
        "hook": "How to articulate the claustrophobia of absolute romantic possession.",
        "why_it_lands": "It doesn't soften possessiveness into poetic romance. The insistence on total cognitive monopoly ('not occupying his thoughts for a single second') admits the tyrannical, devouring nature of desperate intimacy.",
        "tags": ["interiority", "obsession", "candor", "psychology"]
    },
    {
        "quote": "You and I will be together until the day we die. And even when we’re not, we’ll be together.",
        "author": "Choi Jin-young",
        "work": "Hunger",
        "year": 2014,
        "translator": "Soje",
        "hook": "How to bend temporal logic to affirm impossible permanence.",
        "why_it_lands": "The second sentence directly contradicts the linear boundary of the first. By asserting presence even in the physical void of absence, the phrasing captures the irrational stubbornness of devotion.",
        "tags": ["paradox", "devotion", "syntax", "lyricism"]
    }
]

def main():
    with open(QUOTE_BANK_PATH, "r", encoding="utf-8") as f:
        quote_bank = json.load(f)

    existing_quotes = {q["quote"].strip() for q in quote_bank}
    added = 0
    for nq in NEW_QUOTES:
        if nq["quote"].strip() not in existing_quotes:
            quote_bank.append(nq)
            existing_quotes.add(nq["quote"].strip())
            added += 1

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(quote_bank, f, indent=2, ensure_ascii=False)

    print(f"Added {added} new quotes. Total in quote-bank.json: {len(quote_bank)}")

if __name__ == "__main__":
    main()
