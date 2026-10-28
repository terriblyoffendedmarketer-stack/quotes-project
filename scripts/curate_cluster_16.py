#!/usr/bin/env python3
"""
curate_cluster_16.py — Curates 20 vetted quotes from Cluster 16 (Mythic Realism, Pastoral Irony & Classical Stoicism)
into content/quote-bank.json.
"""

import json
from pathlib import Path

QUOTE_BANK_PATH = Path("/Users/apple/Documents/Claude Code/quotes-project/content/quote-bank.json")

NEW_QUOTES = [
    # Neil Gaiman — American Gods
    {
        "quote": "One blow, is all it takes, one blow. That is the art.",
        "author": "Neil Gaiman",
        "work": "American Gods",
        "year": 2001,
        "translator": None,
        "hook": "How to distill slaughter into a craftsman's pride",
        "why_it_lands": "The repetition of the monosyllabic phrase 'one blow' frames ritual butchery not as frenzy, but as quiet, terrifying economy of motion.",
        "tags": ["repetition", "craft-rule", "brevity", "chilling-tone"]
    },
    {
        "quote": "Soon they will fall and the star people will meet the earth people. There will be heroes among them, and men who will slay monsters and bring knowledge, but none of them will be gods. This is a poor place for gods.",
        "author": "Neil Gaiman",
        "work": "American Gods",
        "year": 2001,
        "translator": None,
        "hook": "How to evoke mythological obsolescence through simple nouns",
        "why_it_lands": "Gaiman pairs epic cadence ('star people', 'slay monsters') with the quiet, devastating final verdict: America as an arid soil where divine beings starve.",
        "tags": ["mythology", "cadence", "understatement", "worldbuilding"]
    },
    {
        "quote": "The week before Christmas is often a quiet one in a funeral parlor.",
        "author": "Neil Gaiman",
        "work": "American Gods",
        "year": 2001,
        "translator": None,
        "hook": "How to open a scene through calendar irony",
        "why_it_lands": "Placing the seasonal flurry of Christmas against the stillness of a mortuary creates instant, dry narrative friction in twelve words.",
        "tags": ["juxtaposition", "opening", "tonal-contrast", "restraint"]
    },
    {
        "quote": "“It will be a mighty battle,” it told him, in a glutinous voice. “It’s not going to be a battle. All we’re facing here is a fucking paradigm shift. It’s a shakedown. Modalities like battle are so fucking Lao Tzu.”",
        "author": "Neil Gaiman",
        "work": "American Gods",
        "year": 2001,
        "translator": None,
        "hook": "How to pit corporate jargon against ancient epic register",
        "why_it_lands": "The vulgar corporate vocabulary—'paradigm shift', 'modalities'—subverts heroic fantasy, revealing that modern worship belongs to algorithmic commerce.",
        "tags": ["dialogue", "satire", "tonal-clash", "modernity"]
    },

    # Perumal Murugan — Poonachi, or the Story of a Black Goat
    {
        "quote": "“The unfortunate lesson that I’ve learnt from my experience of living all these years is that people are not that good or straight.”",
        "author": "Perumal Murugan",
        "work": "Poonachi, or the Story of a Black Goat",
        "year": 2016,
        "translator": "N. Kalyan Raman",
        "hook": "How to state a lifelong disillusionment without bitterness",
        "why_it_lands": "The pairing of 'good or straight' grounds moral disappointment in peasant pragmatism. The voice carries the calm fatigue of someone who stopped expecting virtue decades ago.",
        "tags": ["fable", "voice", "disillusionment", "peasant-wisdom"]
    },
    {
        "quote": "“Let him taste that pleasure at least once in this life. Just the memory will be enough for him,” the old man laughed.",
        "author": "Perumal Murugan",
        "work": "Poonachi, or the Story of a Black Goat",
        "year": 2016,
        "translator": "N. Kalyan Raman",
        "hook": "How to justify indulgence through the permanence of memory",
        "why_it_lands": "Murugan captures the tender, tragic generosity of the impoverished: when physical life promises only toil, a single memory of joy becomes wealth enough to survive on.",
        "tags": ["dialogue", "tenderness", "poverty", "memory"]
    },
    {
        "quote": "“No matter how much you give to this heart, it will never be enough.”",
        "author": "Perumal Murugan",
        "work": "Poonachi, or the Story of a Black Goat",
        "year": 2016,
        "translator": "N. Kalyan Raman",
        "hook": "How to state insatiable affection in one breath",
        "why_it_lands": "Twelve words diagnose the fundamental agony of attachment: the heart is an unfillable vessel where care only deepens the terror of loss.",
        "tags": ["aphorism", "emotion", "simplicity", "vulnerability"]
    },
    {
        "quote": "“Do you think a house will keep without people in it?”",
        "author": "Perumal Murugan",
        "work": "Poonachi, or the Story of a Black Goat",
        "year": 2016,
        "translator": "N. Kalyan Raman",
        "hook": "How to define domestic shelter through human presence",
        "why_it_lands": "A rhetorical question that exposes the vulnerability of dwellings: walls and roofs do not preserve a home; without daily human habitation, nature reclaims it within days.",
        "tags": ["domesticity", "interrogation", "brevity", "observation"]
    },

    # Kurt Vonnegut Jr. — Breakfast of Champions
    {
        "quote": "They lived in ugly places where there were only ugly things to do. They didn’t have a nickel to their names, so they couldn’t pretty up their surroundings. So they did their best to pretty up their insides instead.",
        "author": "Kurt Vonnegut Jr.",
        "work": "Breakfast of Champions",
        "year": 1973,
        "translator": None,
        "hook": "How to portray resilience against squalor without sentimental pity",
        "why_it_lands": "Vonnegut matches the blunt repetition of 'ugly' with the plainspoken folk cadence of 'pretty up their insides,' revealing how the poor cultivate secret interior gardens in dreary surroundings.",
        "tags": ["irony", "compassion", "cadence", "repetition"]
    },
    {
        "quote": "Your father was programmed to run out of the house and slam the door. That made your mother automatically into a crying machine.",
        "author": "Kurt Vonnegut Jr.",
        "work": "Breakfast of Champions",
        "year": 1973,
        "translator": None,
        "hook": "How to diagnose domestic trauma through industrial mechanics",
        "why_it_lands": "By reducing parental cruelty and grief to robotic clockwork ('programmed', 'machine'), Vonnegut strips emotional melodrama down to absurd, involuntary habit.",
        "tags": ["mechanistic-metaphor", "satire", "family-dynamics", "absurdism"]
    },
    {
        "quote": "She believed what so many Americans believed then: that the nation would be happy and just and rational when prosperity came.",
        "author": "Kurt Vonnegut Jr.",
        "work": "Breakfast of Champions",
        "year": 1973,
        "translator": None,
        "hook": "How to unmask national delusion with a chronological hinge",
        "why_it_lands": "The triad 'happy and just and rational' sits quietly against the historical illusion that moral virtue could simply be purchased with rising gross national product.",
        "tags": ["social-satire", "historical-irony", "triad", "understatement"]
    },
    {
        "quote": "“I hate this, Bill,” he said as he murdered mushrooms. “Mushrooms have as much right to live as I do. They know what they want, Bill. I’ll be damned if I know what I want anymore.”",
        "author": "Kurt Vonnegut Jr.",
        "work": "Breakfast of Champions",
        "year": 1973,
        "translator": None,
        "hook": "How to pivot from botanical absurdity to existential collapse",
        "why_it_lands": "The comic melodrama of 'murdering mushrooms' swerves sharply into the agonizing confession that fungi possess more directional purpose than the human chopping them.",
        "tags": ["dark-comedy", "existential-dread", "dialogue", "inversion"]
    },

    # Fyodor Dostoevsky — White Nights
    {
        "quote": "“Give me your hand,” I said to my unknown girl, “and he won’t dare bother us anymore.”",
        "author": "Fyodor Dostoevsky",
        "work": "White Nights",
        "year": 1848,
        "translator": "Constance Garnett",
        "hook": "How to claim intimacy through protective bravado",
        "why_it_lands": "The phrase 'my unknown girl' captures the dreamer's instant appropriation of a stranger, offering protection to conceal his own desperate hunger for connection.",
        "tags": ["dialogue", "romanticism", "delusion", "threshold"]
    },
    {
        "quote": "“It’s always the old days with Grandmother! She was younger in the old days, and the sun was warmer in the old days, and cream didn’t go sour so quickly in the old days—it’s always the old days!”",
        "author": "Fyodor Dostoevsky",
        "work": "White Nights",
        "year": 1848,
        "translator": "Constance Garnett",
        "hook": "How to mock nostalgia through escalating domestic grievances",
        "why_it_lands": "Dostoevsky strings together solar mythology with spoiled dairy, using obsessive repetition ('in the old days') to capture youth's exasperation with the golden past.",
        "tags": ["repetition", "comedy", "dialogue", "rhythm"]
    },
    {
        "quote": "“You see, now we’ll always be together, isn’t that so?”",
        "author": "Fyodor Dostoevsky",
        "work": "White Nights",
        "year": 1848,
        "translator": "Constance Garnett",
        "hook": "How to expose wishful thinking in a single fragile tag question",
        "why_it_lands": "The certainty of 'always' is immediately undercut by the desperate trailing plea ('isn’t that so?'), revealing the phantom architecture of loneliness.",
        "tags": ["vulnerability", "dialogue", "delusion", "brevity"]
    },
    {
        "quote": "“Oh, if only he were you!” flashed through my mind. I remembered your words, Nastenka!",
        "author": "Fyodor Dostoevsky",
        "work": "White Nights",
        "year": 1848,
        "translator": "Constance Garnett",
        "hook": "How to dramatize the cruelty of becoming a romantic surrogate",
        "why_it_lands": "A thought that wounds twice: the narrator is treasured not as an end in himself, but only as a flattering, temporary stand-in for the man she actually loves.",
        "tags": ["interiority", "heartbreak", "unrequited-love", "dramatic-irony"]
    },

    # Marcus Aurelius — Meditations
    {
        "quote": "Just that you do the right thing. The rest doesn’t matter.",
        "author": "Marcus Aurelius",
        "work": "Meditations",
        "year": 180,
        "translator": "Gregory Hays",
        "hook": "How to sever moral duty from external consequence",
        "why_it_lands": "Ten monosyllables eliminate all strategic calculation. Duty is stripped of outcome, reputation, and applause, leaving only the immediate ethical choice.",
        "tags": ["stoicism", "aphorism", "moral-clarity", "brevity"]
    },
    {
        "quote": "Disgust at what things are made of: Liquid, dust, bones, filth. Or marble as hardened dirt, gold and silver as residues, clothes as hair, purple dye as shellfish blood.",
        "author": "Marcus Aurelius",
        "work": "Meditations",
        "year": 180,
        "translator": "Gregory Hays",
        "hook": "How to cure vanity through material demystification",
        "why_it_lands": "Marcus Aurelius dismantles imperial luxury by naming their physical origins: imperial purple becomes fish blood, gold becomes mineral slag, and royal robes become animal hair.",
        "tags": ["cataloging", "sensory-detail", "demystification", "stoic-practice"]
    },
    {
        "quote": "It doesn’t matter how good a life you’ve led. There’ll still be people standing around the bed who will welcome the sad event.",
        "author": "Marcus Aurelius",
        "work": "Meditations",
        "year": 180,
        "translator": "Gregory Hays",
        "hook": "How to puncture the illusion of universal posthumous love",
        "why_it_lands": "The emperor looks straight into his own deathbed and refuses self-flattery: even the most righteous ruler leaves behind someone secretly relieved to see him gone.",
        "tags": ["realism", "candor", "mortality", "perspective"]
    },
    {
        "quote": "Death: something like birth, a natural mystery, elements that split and recombine. Not an embarrassing thing. Not an offense to reason, or our nature.",
        "author": "Marcus Aurelius",
        "work": "Meditations",
        "year": 180,
        "translator": "Gregory Hays",
        "hook": "How to domesticate mortality through biological symmetry",
        "why_it_lands": "Hays's modern translation strips death of religious terror, framing it as elemental physics—an ordinary dispersal of atoms no more scandalous than drawing breath.",
        "tags": ["stoicism", "cadence", "understatement", "philosophical-prose"]
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
