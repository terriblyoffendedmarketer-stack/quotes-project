#!/usr/bin/env python3
"""
curate_cluster_17.py — Curates 20 vetted quotes from Cluster 17 (Solitude, Loss & Forensic Grief)
into content/quote-bank.json.
"""

import json
from pathlib import Path

QUOTE_BANK_PATH = Path("/Users/apple/Documents/Claude Code/quotes-project/content/quote-bank.json")

NEW_QUOTES = [
    # Donna Tartt — The Goldfinch
    {
        "quote": "It was my first time in Amsterdam; I’d seen almost nothing of the city and yet the room itself, in its bleak, drafty, sunscrubbed beauty, gave a keen sense of Northern Europe, a model of the Netherlands in miniature: whitewash and Protestant probity, co-mingled with deep-dyed luxury brought in merchant ships from the East.",
        "author": "Donna Tartt",
        "work": "The Goldfinch",
        "year": 2013,
        "translator": None,
        "hook": "How to evoke national character through room architecture",
        "why_it_lands": "Tartt balances ascetic austerity ('whitewash and Protestant probity') against opulent colonial commerce ('deep-dyed luxury'), distilling centuries of cultural tension into a single hotel interior.",
        "tags": ["atmosphere", "architecture", "sensory-detail", "cultural-contrast"]
    },
    {
        "quote": "It was as if I’d signed on as a cabin boy on the Marie Céleste.",
        "author": "Donna Tartt",
        "work": "The Goldfinch",
        "year": 2013,
        "translator": None,
        "hook": "How to establish vulnerability through maritime ghost-lore",
        "why_it_lands": "Combining youth ('cabin boy') with the legendary abandoned derelict ('Marie Céleste') creates an indelible metaphor for sudden, unmoored domestic abandonment.",
        "tags": ["metaphor", "allusion", "vulnerability", "brevity"]
    },
    {
        "quote": "“You’re a liar,” he said pleasantly. “You may think you can bluff your way out of this, but you can’t.”",
        "author": "Donna Tartt",
        "work": "The Goldfinch",
        "year": 2013,
        "translator": None,
        "hook": "How to deliver lethal confrontation with pleasant manners",
        "why_it_lands": "The adverb 'pleasantly' creates chilling tonal friction against the brutal accusation, showing how veteran manipulators dismantle defenses without raising their voice.",
        "tags": ["dialogue", "tonal-contrast", "conflict", "menace"]
    },
    {
        "quote": "Miami, Hamburg, even the place names made me burst into an incredulous huff of laughter.",
        "author": "Donna Tartt",
        "work": "The Goldfinch",
        "year": 2013,
        "translator": None,
        "hook": "How to render hysterics through foreign geography",
        "why_it_lands": "Disorientation turns the mundane index of travel into absurdity: under severe psychological shock, the solemn names of distant cities collapse into involuntary, hollow laughter.",
        "tags": ["shock", "absurdism", "laughter", "interiority"]
    },

    # David Guterson — Snow Falling on Cedars
    {
        "quote": "She sat across from him at the kitchen table at three o’clock in the morning, while he stared in silence or talked or wept, and she took when she could a piece of his sorrow and stored it for him in her own heart.",
        "author": "David Guterson",
        "work": "Snow Falling on Cedars",
        "year": 1994,
        "translator": None,
        "hook": "How to render emotional devotion through quiet nocturnal action",
        "why_it_lands": "The triad of reactions ('stared in silence or talked or wept') pairs with the physical metaphor of storing sorrow in another’s heart, capturing the silent, heroic labor of marital companionship.",
        "tags": ["intimacy", "rhythm", "grief", "tenderness"]
    },
    {
        "quote": "They walked barefoot; they kept their faces down. All of them wore woven straw pickers’ hats.",
        "author": "David Guterson",
        "work": "Snow Falling on Cedars",
        "year": 1994,
        "translator": None,
        "hook": "How to portray collective labor through three austere strokes",
        "why_it_lands": "Guterson uses simple coordinate clauses separated by semicolons to convey the exhausted posture, lowered gaze, and uniform poverty of agricultural migrant labor.",
        "tags": ["visual-craft", "understatement", "social-realism", "brevity"]
    },
    {
        "quote": "“War stinks,” he added. “But they started it. They bombed Hawaii on a Sunday morning. On a Sunday morning, of all things.”",
        "author": "David Guterson",
        "work": "Snow Falling on Cedars",
        "year": 1994,
        "translator": None,
        "hook": "How to reveal domestic outrage outraged by calendar transgression",
        "why_it_lands": "The visceral colloquialism 'war stinks' pivots into the repeated offense—not the carnage of war itself, but the unforgivable breach of Sabbath decorum.",
        "tags": ["dialogue", "vernacular", "repetition", "historical-voice"]
    },
    {
        "quote": "He did not like to explain or elaborate, and there was a part of him she couldn’t get to.",
        "author": "David Guterson",
        "work": "Snow Falling on Cedars",
        "year": 1994,
        "translator": None,
        "hook": "How to sketch emotional opacity in two coordinates",
        "why_it_lands": "Guterson diagnoses masculine reticence without judgment: the boundary between reticence and an unreachable inner wilderness is drawn in sixteen unadorned words.",
        "tags": ["characterization", "interiority", "relationships", "restraint"]
    },

    # Claudia Piñeiro — Elena Knows
    {
        "quote": "Litter has accumulated below the platform opposite them, some of it will disintegrate with time, some of it will outlive her.",
        "author": "Claudia Piñeiro",
        "work": "Elena Knows",
        "year": 2007,
        "translator": "Frances Riddle",
        "hook": "How to measure terminal illness against platform trash",
        "why_it_lands": "Piñeiro pairs the disposable indignity of station rubbish with human mortality: a Styrofoam cup possesses a greater life expectancy than the woman waiting on the bench.",
        "tags": ["mortality", "contrast", "imagery", "understatement"]
    },
    {
        "quote": "“She didn’t laugh much. When had she ever laughed much?”",
        "author": "Claudia Piñeiro",
        "work": "Elena Knows",
        "year": 2007,
        "translator": "Frances Riddle",
        "hook": "How to question a memory of joy in two steps",
        "why_it_lands": "The initial declarative observation is instantly turned inward as an interrogation, revealing how grief erodes the retrospective illusion of past happiness.",
        "tags": ["grief", "interiority", "interrogation", "brevity"]
    },
    {
        "quote": "That’s why she’s sitting on this train, so that this other body, the body of a woman she hasn’t seen for twenty years, may help her uncover the truth that her body refuses her.",
        "author": "Claudia Piñeiro",
        "work": "Elena Knows",
        "year": 2007,
        "translator": "Frances Riddle",
        "hook": "How to dramatize physical incapacity borrowing another’s limbs",
        "why_it_lands": "Parkinson's disease reduces investigation to mechanical physics: when one's own motor neurons fail, finding the truth requires borrowing the mobile flesh of a stranger.",
        "tags": ["somatic-detail", "cadence", "illness", "suspense"]
    },
    {
        "quote": "“People confuse thinking with knowing, they let themselves confuse the two.”",
        "author": "Claudia Piñeiro",
        "work": "Elena Knows",
        "year": 2007,
        "translator": "Frances Riddle",
        "hook": "How to distinguish speculation from visceral conviction",
        "why_it_lands": "Ten words draw a sharp epistemological boundary: intellectual consideration is often an evasive substitute for what the intuition already knows and dreads.",
        "tags": ["aphorism", "epistemology", "brevity", "voice"]
    },

    # Paul Auster — The Invention of Solitude
    {
        "quote": "My grandmother murdered my grandfather. On January 23, 1919, precisely sixty years before my father died, his mother shot and killed his father in the kitchen of their house on Fremont Avenue in Kenosha, Wisconsin.",
        "author": "Paul Auster",
        "work": "The Invention of Solitude",
        "year": 1982,
        "translator": None,
        "hook": "How to detonate a family secret with journalistic neutrality",
        "why_it_lands": "Auster refuses theatrical gasp or flourish. The shocking familial parricide is delivered with forensic precision—exact date, precise address, kitchen geography—making the horror indisputable.",
        "tags": ["opening", "forensic-precision", "family-trauma", "directness"]
    },
    {
        "quote": "The world ends at that barricaded door.",
        "author": "Paul Auster",
        "work": "The Invention of Solitude",
        "year": 1982,
        "translator": None,
        "hook": "How to draw the boundary of isolation in seven words",
        "why_it_lands": "A stark, unbending declaration that collapses reality into physical architecture: beyond the latch of a solitary room, the rest of the universe ceases to exist.",
        "tags": ["solitude", "aphorism", "spatial-metaphor", "brevity"]
    },
    {
        "quote": "Permanent solutions never interested him. He went on patching and patching, a little piece here, a little piece there, never allowing his boat to sink, but never giving it a chance to float either.",
        "author": "Paul Auster",
        "work": "The Invention of Solitude",
        "year": 1982,
        "translator": None,
        "hook": "How to portray chronic indecision through maritime maintenance",
        "why_it_lands": "The repetition of 'patching and patching' mirrors the weary futility of half-measures: a life suspended between survival and buoyancy, perpetually on the verge of ruin.",
        "tags": ["characterization", "metaphor", "repetition", "rhythm"]
    },
    {
        "quote": "It is almost like the drawing a child makes when he is troubled by some inexpressible fear: the most important thing is always the biggest thing.",
        "author": "Paul Auster",
        "work": "The Invention of Solitude",
        "year": 1982,
        "translator": None,
        "hook": "How to explain emotional distortion through naive proportions",
        "why_it_lands": "Auster uses the perspective of children's art—where scale reflects terror rather than optical geometry—to explain how trauma warps all adult proportions.",
        "tags": ["psychology", "analogy", "perspective", "craft-rule"]
    },

    # Steven L. Peck — A Short Stay in Hell
    {
        "quote": "I think I am in Hell, therefore I am.",
        "author": "Steven L. Peck",
        "work": "A Short Stay in Hell",
        "year": 2012,
        "translator": None,
        "hook": "How to adapt Descartes into an infernal axiom",
        "why_it_lands": "Peck replaces foundational skepticism with cosmic dread: the proof of conscious existence is no longer the purity of pure thought, but the undeniable ongoing sensation of damnation.",
        "tags": ["allusion", "aphorism", "dark-comedy", "epistemology"]
    },
    {
        "quote": "To murder a sinner in the morning is the start of a blessed day.",
        "author": "Steven L. Peck",
        "work": "A Short Stay in Hell",
        "year": 2012,
        "translator": None,
        "hook": "How to invert pious devotion into sanctified atrocity",
        "why_it_lands": "Peck pairs the liturgical cadence of morning prayers with ritual slaughter, exposing how religious fanaticism baptizes cruelty as holy duty.",
        "tags": ["satire", "fanaticism", "theology", "irony"]
    },
    {
        "quote": "“It’s two sentences that are grammatically correct! They make sense. This is the most amazing thing I’ve ever seen. It’s poetry.”",
        "author": "Steven L. Peck",
        "work": "A Short Stay in Hell",
        "year": 2012,
        "translator": None,
        "hook": "How to frame basic syntax as miraculous grace",
        "why_it_lands": "After trillions of pages of random typographical noise, simple grammatical coherence is elevated to sublime art—celebrating the miracle of human syntax itself.",
        "tags": ["dialogue", "meta-fiction", "reverence", "syntax"]
    },
    {
        "quote": "What I would have given even to see a cockroach in this place.",
        "author": "Steven L. Peck",
        "work": "A Short Stay in Hell",
        "year": 2012,
        "translator": None,
        "hook": "How to evoke barren sterility through repulsive vermin",
        "why_it_lands": "Peck reveals true damnation not through sulfur or torment, but through the absence of organic life: a reviled insect becomes a desperately yearned-for companion.",
        "tags": ["understatement", "isolation", "bathos", "sensory-longing"]
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
