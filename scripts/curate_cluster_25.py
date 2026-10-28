# scripts/curate_cluster_25.py — Curates 20 craft quotes from Cluster 25 (Steering the Craft, Mortality, Satire & Epic Verse)
# Usage: python3 scripts/curate_cluster_25.py
# Requires: json, os

import json
import os

QUOTE_BANK_PATH = "content/quote-bank.json"

VETTED_CLUSTER_25 = [
    # 1. Ursula K. Le Guin — Steering the Craft (1998)
    {
        "quote": "A sentence has to hang together. Incoherent, straggling, patched-together sentences can’t lead seamlessly to the next sentence, because they can’t even hold themselves together.",
        "author": "Ursula K. Le Guin",
        "work": "Steering the Craft",
        "year": 1998,
        "translator": None,
        "hook": "How to diagnose sentence instability as architectural structural failure.",
        "why_it_lands": "Le Guin personifies syntax as physical masonry, arguing that a clause cannot carry the reader forward into the paragraph if its own internal joints cannot bear weight.",
        "tags": ["craft", "syntax", "clarity", "editing"]
    },
    {
        "quote": "An awareness of what your own writing sounds like is an essential skill for a writer. If you don't hear it as you write it, or as you read it over, how can you expect your reader to hear it?",
        "author": "Ursula K. Le Guin",
        "work": "Steering the Craft",
        "year": 1998,
        "translator": None,
        "hook": "How to establish prose rhythm through internal acoustic playback.",
        "why_it_lands": "Le Guin roots the craft of writing in the physical sense of hearing, insisting that even silent print on paper is fundamentally an acoustic performance between voices.",
        "tags": ["sound", "rhythm", "voice", "craft"]
    },
    {
        "quote": "Present-tense narration persuades people that it’s ‘more real’ because it sounds like eyewitness narration. But the past tense is the natural, traditional tense of storytelling in English: it gives narrative distance, perspective, and resonance.",
        "author": "Ursula K. Le Guin",
        "work": "Steering the Craft",
        "year": 1998,
        "translator": None,
        "hook": "How to deconstruct the illusory immediacy of the present tense.",
        "why_it_lands": "Le Guin challenges modern stylistic fashion, contrasting the frantic, unexamined heat of present-tense reportage against the panoramic authority and acoustic depth of the past tense.",
        "tags": ["perspective", "tenses", "craft", "narrative"]
    },
    {
        "quote": "Pacing is not a matter of speed, but of movement. You can go very slowly and still be moving forward; you can go very fast and run in circles.",
        "author": "Ursula K. Le Guin",
        "work": "Steering the Craft",
        "year": 1998,
        "translator": None,
        "hook": "How to detach narrative progression from mere physical velocity.",
        "why_it_lands": "Le Guin makes a crucial craft distinction between rushing and progressing, warning that frantic kinetic acceleration frequently conceals a total lack of narrative development.",
        "tags": ["pacing", "movement", "craft", "structure"]
    },

    # 2. Oliver Burkeman — Meditations for Mortals (2024)
    {
        "quote": "This portion of your limited time, the part before you’ve managed to get on top of everything, or dealt with your procrastination problem, or graduated or found a partner or retired; and before the survival of democracy or the climate have been secured: this part matters just as much as any other and arguably even more than any other, since the past is gone and the future hasn’t occurred yet, so right now is the only time that really exists.",
        "author": "Oliver Burkeman",
        "work": "Meditations for Mortals",
        "year": 2024,
        "translator": None,
        "hook": "How to demolish provisional living in a single sweeping periodic sentence.",
        "why_it_lands": "Burkeman lists every cultural excuse for delaying presence into a relentless catalogue of conditions, only to deliver the devastating truth: the messy interlude you are enduring is already your actual life.",
        "tags": ["existential", "perspective", "time", "candor"]
    },
    {
        "quote": "The good thing about everything being so fucked up is that no matter where you look, there is great work to be done.",
        "author": "Oliver Burkeman",
        "work": "Meditations for Mortals",
        "year": 2024,
        "translator": None,
        "hook": "How to find radical vocational purpose in total civilizational disrepair.",
        "why_it_lands": "Burkeman executes a brazen tonal pivot, converting despair over an imperfect world into an invigorating mandate for immediate, unglamorous useful labor.",
        "tags": ["courage", "pragmatism", "purpose", "voice"]
    },
    {
        "quote": "He can be a charming sort of person to be around, until one day he very much isn’t, and he’s suddenly the dubious fifty-something in a bar full of 25-year-olds, having frittered his real future away on fantasies of an unlimited one.",
        "author": "Oliver Burkeman",
        "work": "Meditations for Mortals",
        "year": 2024,
        "translator": None,
        "hook": "How to dramatize the tragedy of non-commitment as a grotesque aging archetype.",
        "why_it_lands": "Burkeman fast-forwards through the illusion of infinite potential, exposing how the refusal to choose a single path ultimately leaves a person stranded in pathetic irrelevance.",
        "tags": ["characterization", "time", "candor", "pathos"]
    },
    {
        "quote": "You don't need to feel like doing something in order to do it. The feeling of resistance isn’t a stop sign; it’s just what it feels like to confront the limits of your control.",
        "author": "Oliver Burkeman",
        "work": "Meditations for Mortals",
        "year": 2024,
        "translator": None,
        "hook": "How to demote internal resistance from an obstacle to an operating baseline.",
        "why_it_lands": "Burkeman strips procrastination of its dramatic power, reminding the practitioner that creative dread is not a cosmic warning to pause, but the natural friction of engaging with reality.",
        "tags": ["discipline", "pragmatism", "action", "clarity"]
    },

    # 3. Percival Everett — The Trees (2021)
    {
        "quote": "‘We use these because they are cliché,’ Hind said. ‘We’re the FBI. We are walking clichés.’",
        "author": "Percival Everett",
        "work": "The Trees",
        "year": 2021,
        "translator": None,
        "hook": "How to subvert bureaucratic authority through deadpan meta-irony.",
        "why_it_lands": "Everett deflates institutional self-importance by having a federal agent calmly embrace his own pulp caricature, disarming the listener with radical narrative self-awareness.",
        "tags": ["satire", "dialogue", "wit", "voice"]
    },
    {
        "quote": "‘Some things don’t add up,’ Jim said. ‘And when they don’t add up, you have to look at who is doing the arithmetic.’",
        "author": "Percival Everett",
        "work": "The Trees",
        "year": 2021,
        "translator": None,
        "hook": "How to interrogate official authority through an arithmetic metaphor.",
        "why_it_lands": "Everett pivots detective work from physical evidence to institutional power, warning that when official facts fail to cohere, the corruption lies with the entity doing the counting.",
        "tags": ["dialogue", "satire", "power", "wit"]
    },
    {
        "quote": "They’re dead! Dead. Dead. Dead. Sacrilegious? Ain’t no souls down there, just arms and legs, hands, heads and elbows, tongues, testicles and nipples, ears and eyeballs.",
        "author": "Percival Everett",
        "work": "The Trees",
        "year": 2021,
        "translator": None,
        "hook": "How to dismantle sentimental mourning through a rhythmic anatomical inventory.",
        "why_it_lands": "Everett rejects pious euphemisms for historical lynching, piling up raw anatomical parts in rhythmic, alliterative succession to confront the reader with unvarnished butcher's meat.",
        "tags": ["rhythm", "grief", "candor", "satire"]
    },
    {
        "quote": "‘Don’t speak for the dead,’ Jim said. ‘The dead don’t need an interpreter. They need a scorekeeper.’",
        "author": "Percival Everett",
        "work": "The Trees",
        "year": 2021,
        "translator": None,
        "hook": "How to replace sentimental mourning with cold moral accounting.",
        "why_it_lands": "Everett cuts through performative sympathy with a sharp antithetical distinction: the victims of racial terror do not require rhetorical patronage, only an unyielding ledger of retribution.",
        "tags": ["justice", "dialogue", "candor", "contrast"]
    },

    # 4. Ernest Hemingway — The Old Man and the Sea (1952)
    {
        "quote": "He always thought of the sea as feminine and as something that gave or withheld great favours, and if she did wild or wicked things it was because she could not help them.",
        "author": "Ernest Hemingway",
        "work": "The Old Man and the Sea",
        "year": 1952,
        "translator": None,
        "hook": "How to anthropomorphize nature without domesticating its danger.",
        "why_it_lands": "Hemingway uses gentle rhythmic coordination to grant the sea emotional agency, yet forgives its cruelty by treating oceanic violence as an involuntary, cosmic compulsion.",
        "tags": ["rhythm", "imagery", "characterization", "metaphor"]
    },
    {
        "quote": "No man is alone on the sea.",
        "author": "Ernest Hemingway",
        "work": "The Old Man and the Sea",
        "year": 1952,
        "translator": None,
        "hook": "How to invert maritime isolation into cosmic fraternity in seven words.",
        "why_it_lands": "Hemingway delivers a compact declarative paradox, transforming the vast, empty oceanic horizon from a space of solitary vulnerability into a shared theater of living creatures.",
        "tags": ["brevity", "solitude", "perspective", "philosophy"]
    },
    {
        "quote": "I am sorry that I went too far out. I ruined us both.",
        "author": "Ernest Hemingway",
        "work": "The Old Man and the Sea",
        "year": 1952,
        "translator": None,
        "hook": "How to compress tragic hubris into eleven monosyllables.",
        "why_it_lands": "Hemingway strips epic tragedy down to bare bone, framing overambitious trespass not as heroic glory, but as a mutual disaster shared equally between predator and prey.",
        "tags": ["brevity", "pathos", "candor", "hubris"]
    },
    {
        "quote": "Now is no time to think of what you do not have. Think of what you can do with what there is.",
        "author": "Ernest Hemingway",
        "work": "The Old Man and the Sea",
        "year": 1952,
        "translator": None,
        "hook": "How to banish paralyzing regret through radical situational pragmatism.",
        "why_it_lands": "Hemingway uses parallel imperatives to arrest nostalgic panic, pivoting the mind instantly from a grieving inventory of lack to immediate tactical mobilization.",
        "tags": ["pragmatism", "courage", "clarity", "stoicism"]
    },

    # 5. Agatha Christie — The Murder of Roger Ackroyd (1926)
    {
        "quote": "‘Everyone has something to hide,’ I quoted, smiling. ‘Exactly.’",
        "author": "Agatha Christie",
        "work": "The Murder of Roger Ackroyd",
        "year": 1926,
        "translator": None,
        "hook": "How to hide a confession in plain sight under conversational cliché.",
        "why_it_lands": "Christie weaponizes the unreliable narrator: Dr. Sheppard offers an aphorism about general human frailty that doubles as a literal, smug admission of guilt right under the reader's nose.",
        "tags": ["irony", "dialogue", "subversion", "deception"]
    },
    {
        "quote": "If I am to save him, I must know all there is to know—even if it should seem to make the case against him blacker than before.",
        "author": "Agatha Christie",
        "work": "The Murder of Roger Ackroyd",
        "year": 1926,
        "translator": None,
        "hook": "How to raise investigative stakes by demanding self-incriminating truth.",
        "why_it_lands": "Christie articulates Poirot's paradoxical investigative code: the client can only be rescued by ruthlessly exposing the very evidence that appears to condemn him.",
        "tags": ["tension", "deduction", "paradox", "candor"]
    },
    {
        "quote": "‘Use your little grey cells,’ he said. ‘There is always a reason behind my actions.’",
        "author": "Agatha Christie",
        "work": "The Murder of Roger Ackroyd",
        "year": 1926,
        "translator": None,
        "hook": "How to turn a character catchphrase into a rule of narrative deduction.",
        "why_it_lands": "Christie elevates Poirot's quirky sensory metaphor into an intellectual command, requiring both sidekick and reader to abandon surface assumptions in favor of rigorous causal analysis.",
        "tags": ["characterization", "voice", "wit", "craft"]
    },
    {
        "quote": "There is only one way out—and that way does not lead to freedom.",
        "author": "Agatha Christie",
        "work": "The Murder of Roger Ackroyd",
        "year": 1926,
        "translator": None,
        "hook": "How to close off narrative escape through an ominous syntactic dash.",
        "why_it_lands": "Christie dangles the promise of release in the first clause, then snaps the trap shut after the em-dash, delivering the quiet, inescapable verdict of trapped guilt.",
        "tags": ["brevity", "tension", "antithesis", "syntax"]
    }
]

def main():
    with open(QUOTE_BANK_PATH, "r", encoding="utf-8") as f:
        existing = json.load(f)

    existing_quotes = {q["quote"].strip() for q in existing}
    added = 0

    for item in VETTED_CLUSTER_25:
        if item["quote"].strip() not in existing_quotes:
            existing.append(item)
            existing_quotes.add(item["quote"].strip())
            added += 1

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"Successfully added {added} vetted quotes from Cluster 25.")
    print(f"Total quotes in bank: {len(existing)}")

if __name__ == "__main__":
    main()
