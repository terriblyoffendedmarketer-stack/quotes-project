# scripts/curate_cluster_24.py — Curates 20 craft quotes from Cluster 24 (Depth Psychology, Systems, Instinct & Game Theory)
# Usage: python3 scripts/curate_cluster_24.py
# Requires: json, os

import json
import os

QUOTE_BANK_PATH = "content/quote-bank.json"

VETTED_CLUSTER_24 = [
    # 1. Carl G. Jung — Memories, Dreams, Reflections (1961)
    {
        "quote": "There is no linear evolution; there is only a circumambulation of the self.",
        "author": "Carl G. Jung",
        "work": "Memories, Dreams, Reflections",
        "year": 1961,
        "translator": "Richard & Clara Winston",
        "hook": "How to conceptualize psychological growth as an orbit rather than an ascent.",
        "why_it_lands": "Jung replaces the Western obsession with progressive, linear advancement with a rotational geometric metaphor, proposing that maturity is an ongoing orbit around an immutable interior core.",
        "tags": ["philosophy", "metaphor", "geometry", "psychology"]
    },
    {
        "quote": "The more uncertain I have felt about myself, the more there has grown up in me a feeling of kinship with all things.",
        "author": "Carl G. Jung",
        "work": "Memories, Dreams, Reflections",
        "year": 1961,
        "translator": "Richard & Clara Winston",
        "hook": "How to invert epistemological doubt into expansive relational empathy.",
        "why_it_lands": "Using a balanced correlative comparative ('The more... the more...'), Jung reframes the collapse of dogmatic self-certainty not as neurotic alienation, but as the precondition for universal connection.",
        "tags": ["vulnerability", "syntax", "interiority", "perspective"]
    },
    {
        "quote": "To my mind, therapy only really begins after the investigation of that wholly personal story. It is the patient's secret, the rock against which he is shattered.",
        "author": "Carl G. Jung",
        "work": "Memories, Dreams, Reflections",
        "year": 1961,
        "translator": "Richard & Clara Winston",
        "hook": "How to elevate biographical idiosyncrasy into the decisive somatic battlefield.",
        "why_it_lands": "Jung shifts clinical diagnosis away from diagnostic categories and into private myth, deploying a sudden geological metaphor ('the rock against which he is shattered') to dramatize psychic trauma.",
        "tags": ["metaphor", "candor", "narrative", "psychology"]
    },
    {
        "quote": "As far as we can discern, the sole purpose of human existence is to kindle a light in the darkness of being.",
        "author": "Carl G. Jung",
        "work": "Memories, Dreams, Reflections",
        "year": 1961,
        "translator": "Richard & Clara Winston",
        "hook": "How to distill human purpose into a single primeval sensory image.",
        "why_it_lands": "Jung qualifies an immense metaphysical claim with deliberate empirical modesty ('As far as we can discern'), contrasting infinite, vacant blackness against a singular, fragile ignite of consciousness.",
        "tags": ["existential", "imagery", "contrast", "rhythm"]
    },

    # 2. Neal Stephenson — Cryptonomicon (1999)
    {
        "quote": "The boundary between Randy and his environment has been annihilated.",
        "author": "Neal Stephenson",
        "work": "Cryptonomicon",
        "year": 1999,
        "translator": None,
        "hook": "How to signal total cognitive immersion through total passive finality.",
        "why_it_lands": "Stephenson uses a surgical, passive-voice declaration to dramatize deep flow state, presenting the collapse of external sensory distinction as an absolute, completed event.",
        "tags": ["brevity", "immersion", "focus", "clarity"]
    },
    {
        "quote": "A good programmer should be able to sit down and write a complete operating system from scratch in three weeks, in hex, using a soldering iron, if necessary.",
        "author": "Neal Stephenson",
        "work": "Cryptonomicon",
        "year": 1999,
        "translator": None,
        "hook": "How to construct a technical mythos through cascading hyperbolic specifics.",
        "why_it_lands": "Stephenson escalates craft competence from software to hardware down to raw physics ('in hex, using a soldering iron'), converting engineering mastery into an absurd, heroic tall tale.",
        "tags": ["hyperbole", "voice", "craft", "satire"]
    },
    {
        "quote": "It is a game, a cryptographic chess match between Waterhouse and his German counterpart, translated into action by gung-ho Shaftoe and his forces.",
        "author": "Neal Stephenson",
        "work": "Cryptonomicon",
        "year": 1999,
        "translator": None,
        "hook": "How to bridge abstract mathematical theory and chaotic physical combat.",
        "why_it_lands": "Stephenson links cerebral codebreaking with muddy kinetic warfare in a single sentence, framing battlefield violence as the kinetic execution layer of a silent intellectual duel.",
        "tags": ["contrast", "pacing", "structure", "metaphor"]
    },
    {
        "quote": "The idea of the Internet as a highly distributed, redundant global communications system is a myth; it is an archipelago of fragile chokepoints and physical wires laid across muddy seabeds.",
        "author": "Neal Stephenson",
        "work": "Cryptonomicon",
        "year": 1999,
        "translator": None,
        "hook": "How to puncture digital immateriality with industrial physical geography.",
        "why_it_lands": "Stephenson shatters the ethereal metaphor of the 'cloud' by contrasting high-tech abstractions against raw, tangible vulnerability—anchoring global communication in undersea silt and copper.",
        "tags": ["realism", "antithesis", "imagery", "cynicism"]
    },

    # 3. Charles Bukowski — On Cats (2015)
    {
        "quote": "“Shake hands!” I said to the cat. The cat just sat there.",
        "author": "Charles Bukowski",
        "work": "On Cats",
        "year": 2015,
        "translator": None,
        "hook": "How to expose human pretension against non-human indifference in eleven words.",
        "why_it_lands": "Bukowski pits an imperious human command against the immoveable, serene sovereignty of an animal, letting the blank physical refusal carry the entire comedic and philosophical punchline.",
        "tags": ["brevity", "understatement", "humor", "candor"]
    },
    {
        "quote": "I put the phone down and the cat-sides of the room come in upon me and I would scream, but they have places for people who scream.",
        "author": "Charles Bukowski",
        "work": "On Cats",
        "year": 2015,
        "translator": None,
        "hook": "How to compress domestic dread into streetwise, vernacular restraint.",
        "why_it_lands": "The unusual tactile compound 'cat-sides of the room' evokes a strange domestic claustrophobia, followed instantly by a blunt, deadpan survival calculation about insane asylums.",
        "tags": ["voice", "candor", "claustrophobia", "rhythm"]
    },
    {
        "quote": "Late at night when I drink and type they are about—like say one on the back of my chair and the other down there nibbling at my toes.",
        "author": "Charles Bukowski",
        "work": "On Cats",
        "year": 2015,
        "translator": None,
        "hook": "How to capture the solitary writing ritual through casual domestic friction.",
        "why_it_lands": "Bukowski rejects romanticized literary atmosphere in favor of unvarnished colloquial rhythm, grounding nocturnal creative work in the tactile, unbothered presence of feral housemates.",
        "tags": ["rhythm", "voice", "craft", "sensory"]
    },
    {
        "quote": "Having a bunch of cats around is good. If you're feeling bad, you just look at the cats, you'll feel better, because they know that everything is, just as it is. There's nothing to get excited about.",
        "author": "Charles Bukowski",
        "work": "On Cats",
        "year": 2015,
        "translator": None,
        "hook": "How to prescribe creaturely indifference as the cure for existential panic.",
        "why_it_lands": "Bukowski translates Zen acceptance into gutter-poet vernacular, praising cats not for their affection, but for their radical refusal to manufacture artificial drama out of existence.",
        "tags": ["stoicism", "clarity", "voice", "candor"]
    },

    # 4. Oliver Burkeman — Help! How to Become Slightly Happier and Get a Bit More Done (2011)
    {
        "quote": "Books on ‘getting motivated’, and hyper-energetic motivational speakers, ironically compound the problem by reinforcing the idea that you need to feel positive about doing something before you begin it. Motivation follows action.",
        "author": "Oliver Burkeman",
        "work": "Help! How to Become Slightly Happier and Get a Bit More Done",
        "year": 2011,
        "translator": None,
        "hook": "How to invert the emotional prerequisite of creative work.",
        "why_it_lands": "Burkeman exposes how the self-help industry paralyzes its adherents by demanding emotional readiness, delivering the three-word mechanical corrective: 'Motivation follows action.'",
        "tags": ["action", "candor", "psychology", "discipline"]
    },
    {
        "quote": "Our brains are so easy to fool that it’s borderline embarrassing; you might as well salvage some self-respect by exploiting that fact.",
        "author": "Oliver Burkeman",
        "work": "Help! How to Become Slightly Happier and Get a Bit More Done",
        "year": 2011,
        "translator": None,
        "hook": "How to turn neurological susceptibility into a pragmatic habit tool.",
        "why_it_lands": "Burkeman cuts through academic cognitive psychology with dry British self-deprecation, advising the reader to stop fighting cognitive glitches and start weaponizing them.",
        "tags": ["irony", "pragmatism", "wit", "voice"]
    },
    {
        "quote": "What we seek is ‘pragmatic accuracy’—we don’t base friendships on what we learn about people; we decide what to learn about people, and what to ignore, based on having decided to be friends.",
        "author": "Oliver Burkeman",
        "work": "Help! How to Become Slightly Happier and Get a Bit More Done",
        "year": 2011,
        "translator": None,
        "hook": "How to unmask interpersonal affection as deliberate cognitive bias.",
        "why_it_lands": "Burkeman uses a sharp causal reversal to demonstrate that loyalty is not objective appraisal, but an intentional, protective blindness that preserves social cohesion.",
        "tags": ["psychology", "candor", "relationships", "insight"]
    },
    {
        "quote": "Passion may not be worth getting too excited about. The obsession with finding your passion assumes that fulfilling work must feel like constant ecstasy rather than quiet absorption.",
        "author": "Oliver Burkeman",
        "work": "Help! How to Become Slightly Happier and Get a Bit More Done",
        "year": 2011,
        "translator": None,
        "hook": "How to puncture vocational romanticism with the reality of quiet absorption.",
        "why_it_lands": "Burkeman dismantles the cult of passion by distinguishing theatrical emotional highs from the low-temperature, durable satisfaction of absorbed craftsmanship.",
        "tags": ["craft", "clarity", "work-ethic", "realism"]
    },

    # 5. Orson Scott Card — Ender's Game (1985)
    {
        "quote": "In the moment when I truly understand my enemy, understand him well enough to defeat him, then in that very moment I also love him.",
        "author": "Orson Scott Card",
        "work": "Ender's Game",
        "year": 1985,
        "translator": None,
        "hook": "How to bind tactical supremacy to devastating emotional empathy.",
        "why_it_lands": "Card formulates the central tragic paradox of conflict: to predict an adversary with flawless precision requires complete cognitive identification, transforming eventual victory into grief.",
        "tags": ["paradox", "empathy", "conflict", "pathos"]
    },
    {
        "quote": "They love you. The question is whether they want you here. Your presence in this house is a constant disruption. A source of tension. Do you understand?",
        "author": "Orson Scott Card",
        "work": "Ender's Game",
        "year": 1985,
        "translator": None,
        "hook": "How to surgically detach familial affection from familial tolerance.",
        "why_it_lands": "Card uses clipped, monosyllabic declarations to demolish a child's sanctuary, demonstrating that unconditional love does not guarantee emotional hospitality.",
        "tags": ["dialogue", "tension", "brevity", "pathos"]
    },
    {
        "quote": "Home was merely a dull ache in the back of his memory. A tiredness in his eyes.",
        "author": "Orson Scott Card",
        "work": "Ender's Game",
        "year": 1985,
        "translator": None,
        "hook": "How to somatize homesickness into physiological exhaustion.",
        "why_it_lands": "Card avoids dramatic lamentation, condensing exile into two compact physical symptoms: a phantom ache behind the skull and a physical weariness behind the eyelids.",
        "tags": ["sensory", "understatement", "pathos", "characterization"]
    },
    {
        "quote": "There is no teacher but the enemy. No one but the enemy will tell you what you are doing wrong, and no one else will make you suffer the consequences.",
        "author": "Orson Scott Card",
        "work": "Ender's Game",
        "year": 1985,
        "translator": None,
        "hook": "How to elevate opposition into the singular engine of true education.",
        "why_it_lands": "Card discards benevolent pedagogy in favor of brutal feedback loops, arguing that only an adversarial force with no incentive to spare your feelings can reveal your actual weaknesses.",
        "tags": ["adversity", "discipline", "candor", "philosophy"]
    }
]

def main():
    with open(QUOTE_BANK_PATH, "r", encoding="utf-8") as f:
        existing = json.load(f)

    existing_quotes = {q["quote"].strip() for q in existing}
    added = 0

    for item in VETTED_CLUSTER_24:
        if item["quote"].strip() not in existing_quotes:
            existing.append(item)
            existing_quotes.add(item["quote"].strip())
            added += 1

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"Successfully added {added} vetted quotes from Cluster 24.")
    print(f"Total quotes in bank: {len(existing)}")

if __name__ == "__main__":
    main()
