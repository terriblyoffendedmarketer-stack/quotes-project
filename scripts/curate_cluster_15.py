#!/usr/bin/env python3
"""
curate_cluster_15.py — Curates 20 vetted quotes from Cluster 15 (Epic Fiction, Groundbreaking Memoir & Creative Practice)
into content/quote-bank.json.
"""

import json
from pathlib import Path

QUOTE_BANK_PATH = Path("/Users/apple/Documents/Claude Code/quotes-project/content/quote-bank.json")

NEW_QUOTES = [
    # Michael Chabon — The Amazing Adventures of Kavalier & Clay
    {
        "quote": "“The Escapist.” It sounded magnificent to his unschooled ear—someone trustworthy and useful and strong.",
        "author": "Michael Chabon",
        "work": "The Amazing Adventures of Kavalier & Clay",
        "year": 2000,
        "translator": None,
        "hook": "How to name a persona through an uncorrupted ear",
        "why_it_lands": "The rhythm pivots on three simple coordinate adjectives—'trustworthy and useful and strong'—stripping away commercial cynicism to reveal how myth operates on pure longing.",
        "tags": ["naming", "characterization", "mythology", "adjective-triad"]
    },
    {
        "quote": "Without the witty, potent dialogue and the puzzling shape of the story, the movie would have been merely an American version of the kind of brooding, shadow-filled Ufa-style expressionist stuff that Joe had grown up watching in Prague. Without the brooding shadows and bold adventurings of the camera, without the theatrical lighting and queasy angles, it would have been merely a clever movie about a rich bastard.",
        "author": "Michael Chabon",
        "work": "The Amazing Adventures of Kavalier & Clay",
        "year": 2000,
        "translator": None,
        "hook": "How to dissect art through balanced negative clauses",
        "why_it_lands": "Parallel syntax ('Without X... it would have been merely Y') strips a masterpiece down to its twin counterweights: literary architecture on one side, visual delirium on the other.",
        "tags": ["sentence-architecture", "parallelism", "aesthetic-critique", "rhythm"]
    },
    {
        "quote": "The thought was banal, and yet somehow, as happened every now and then, it took him by surprise and profoundly disappointed him.",
        "author": "Michael Chabon",
        "work": "The Amazing Adventures of Kavalier & Clay",
        "year": 2000,
        "translator": None,
        "hook": "How to register the sting of a commonplace truth",
        "why_it_lands": "The subordinate parenthetical ('as happened every now and then') slows the tempo just enough for the emotional collision—between ordinary banality and sharp disappointment—to detonate quietly.",
        "tags": ["interiority", "subordination", "emotional-register", "restraint"]
    },
    {
        "quote": "“You have no right to any part of her. You boys came up with her as employees of Empire Comics, on our payroll. She’s ours.”",
        "author": "Michael Chabon",
        "work": "The Amazing Adventures of Kavalier & Clay",
        "year": 2000,
        "translator": None,
        "hook": "How to render corporate predation in three blunt strokes",
        "why_it_lands": "Three curt declarations strip away romance: legal non-existence ('no right'), labor contract ('on our payroll'), and absolute possession ('She’s ours'). The monosyllabic finality stuns.",
        "tags": ["dialogue", "cadence", "conflict", "power-dynamics"]
    },

    # Chanel Miller — Know My Name: A Memoir
    {
        "quote": "These were not pill-swallowing, bridge-jumping, arm-slicing suicides, for those at least carried a sliver of a chance you’d survive. These were certain deaths.",
        "author": "Chanel Miller",
        "work": "Know My Name: A Memoir",
        "year": 2019,
        "translator": None,
        "hook": "How to distinguish degrees of desperation through compound modifiers",
        "why_it_lands": "The compound participles create a grim catalog of conventional despair, only to dismiss them with the devastating monosyllabic counter-strike: 'These were certain deaths.'",
        "tags": ["memoir", "compound-modifiers", "cataloging", "contrast"]
    },
    {
        "quote": "I knew I would show up again at work the next morning, the same way tires bumped over the tracks, the same way that after learning about a death, you’d take out your textbook and carry on with the lesson.",
        "author": "Chanel Miller",
        "work": "Know My Name: A Memoir",
        "year": 2019,
        "translator": None,
        "hook": "How to depict dissociation through mechanical routine",
        "why_it_lands": "The repeated comparative clause ('the same way... the same way') anchors trauma in the numb, involuntary momentum of daily chores—tires over tracks, textbooks opened after grief.",
        "tags": ["dissociation", "metaphor", "parallelism", "grief"]
    },
    {
        "quote": "Women are raised to work with dexterity, to keep their nimble fingers ready, their minds alert. It is her job to know how to handle the stream of bombs, how to kindly decline giving her number, how to move a hand from the button of her jeans, to turn down a drink.",
        "author": "Chanel Miller",
        "work": "Know My Name: A Memoir",
        "year": 2019,
        "translator": None,
        "hook": "How to expose vigilance by cataloging mundane deflections",
        "why_it_lands": "Miller matches graceful domestic words ('dexterity', 'nimble fingers') with escalating physical violations, ending on an infinitive catalog that captures the exhausting labor of self-defense.",
        "tags": ["social-commentary", "infinitive-phrasing", "pacing", "visceral-detail"]
    },
    {
        "quote": "They looked and acted nothing alike; how were we expected to recognize one in the other? How do laced-up white sneakers become black heels snuffing out cigarette butts?",
        "author": "Chanel Miller",
        "work": "Know My Name: A Memoir",
        "year": 2019,
        "translator": None,
        "hook": "How to dramatize legal distortion through footwear",
        "why_it_lands": "The visual contrast between 'laced-up white sneakers' and 'black heels snuffing out cigarette butts' exposes how defense narratives manufacture a false persona out of clothing.",
        "tags": ["sensory-contrast", "interrogation", "imagery", "subtext"]
    },

    # Fyodor Dostoevsky — Crime and Punishment
    {
        "quote": "Trifles, trifles are what matter! Why, it’s just such trifles that always ruin everything.",
        "author": "Fyodor Dostoevsky",
        "work": "Crime and Punishment",
        "year": 1866,
        "translator": "Constance Garnett",
        "hook": "How to expose an obsessive mind through frantic repetition",
        "why_it_lands": "The double exclamation and opening repetition capture Raskolnikov's fevered rationalization—the delusion that a monumental crime hinges not on conscience, but on forgotten loose threads.",
        "tags": ["repetition", "psychological-monologue", "paranoia", "dramatization"]
    },
    {
        "quote": "“It all cuts both ways, now it all cuts both ways,” repeated Raskolnikov, and he went out more confident than ever.",
        "author": "Fyodor Dostoevsky",
        "work": "Crime and Punishment",
        "year": 1866,
        "translator": "Constance Garnett",
        "hook": "How to pair manic delusion with physical momentum",
        "why_it_lands": "The repetition of the idiom 'cuts both ways' becomes a nervous mantra; the sudden surge of false confidence right after panic exposes the split duality of the criminal ego.",
        "tags": ["interiority", "idiom", "psychological-realism", "pacing"]
    },
    {
        "quote": "“It’s simply a fantasy to amuse myself; a plaything!”",
        "author": "Fyodor Dostoevsky",
        "work": "Crime and Punishment",
        "year": 1866,
        "translator": "Constance Garnett",
        "hook": "How to show self-deception disguising murder as a game",
        "why_it_lands": "Dismissing a premeditated atrocity as a 'plaything' reveals the terrifying mechanism of intellectual detachment—reducing blood and butchery to an abstract intellectual puzzle.",
        "tags": ["denial", "psychology", "irony", "dialogue"]
    },
    {
        "quote": "“You don’t believe she used it? But do you know I managed the estate quite decently, they know me in the neighbourhood. I ordered books, too.”",
        "author": "Fyodor Dostoevsky",
        "work": "Crime and Punishment",
        "year": 1866,
        "translator": "Constance Garnett",
        "hook": "How to reveal moral rot through suburban respectability",
        "why_it_lands": "Svidrigaïlov casually offers the veneer of good civic standing—managing an estate, ordering books—as defense against cruelty, showing how monsters hide behind mundane decorum.",
        "tags": ["character-revelation", "dialogue", "deflection", "moral-irony"]
    },

    # Neal Stephenson — Snow Crash
    {
        "quote": "Condense fact from the vapor of nuance.",
        "author": "Neal Stephenson",
        "work": "Snow Crash",
        "year": 1992,
        "translator": None,
        "hook": "How to coin an intellectual imperative with physical metaphor",
        "why_it_lands": "Seven words contrast the gaseous, evasive realm of 'nuance' against the hard precipitation of 'fact,' creating an indelible law of digital investigation.",
        "tags": ["aphorism", "metaphor", "precision", "imperative"]
    },
    {
        "quote": "The edge is only a single molecule wide. Doctors use them for eye surgery—they can cut your cornea and not leave a scar.",
        "author": "Neal Stephenson",
        "work": "Snow Crash",
        "year": 1992,
        "translator": None,
        "hook": "How to describe lethality through clinical delicacy",
        "why_it_lands": "Stephenson weaponizes hyper-precision: an edge so microscopic it belongs in eye surgery becomes terrifying precisely because it wounds without leaving a mark.",
        "tags": ["hyper-detail", "sci-fi-craft", "clinical-tone", "contrast"]
    },
    {
        "quote": "“Hiro Protagonist,” the gargoyle says as Hiro finally tracks him down in the darkness beside a shanty. “CIC stringer for eleven months. Specializing in the Industry. Former hacker, security guard, pizza deliverer, concert promoter.”",
        "author": "Neal Stephenson",
        "work": "Snow Crash",
        "year": 1992,
        "translator": None,
        "hook": "How to build cyber-noir character resumes out of absurd fragments",
        "why_it_lands": "The staccato listing of fragmented freelance gigs—hacker, security guard, pizza deliverer—captures the manic gig-economy entropy of cyberpunk faster than any paragraph of exposition.",
        "tags": ["characterization", "listing", "worldbuilding", "staccato"]
    },
    {
        "quote": "“Your information, sir,” the Librarian says. “Are you smart enough to tie that information into YOU ARE HERE?”",
        "author": "Neal Stephenson",
        "work": "Snow Crash",
        "year": 1992,
        "translator": None,
        "hook": "How to challenge passive knowledge through algorithmic dialogue",
        "why_it_lands": "The AI librarian punctures the illusion of trivia: possessing raw facts means nothing without the spatial intelligence to locate oneself within the coordinates of reality.",
        "tags": ["dialogue", "epistemology", "cyberpunk", "philosophical-fiction"]
    },

    # Rick Rubin — The Creative Act: A Way of Being
    {
        "quote": "Creativity is not a rare ability. It is not difficult to access. Creativity is a fundamental aspect of being human. It’s our birthright. And it’s for all of us.",
        "author": "Rick Rubin",
        "work": "The Creative Act: A Way of Being",
        "year": 2023,
        "translator": None,
        "hook": "How to dismantle elitism through rhythmic short sentences",
        "why_it_lands": "Rubin stacks five declarative hammer blows, stripping away the mythology of the genius to restore creation to an ordinary, shared biological inheritance.",
        "tags": ["staccato", "craft-philosophy", "declarative", "rhythm"]
    },
    {
        "quote": "If you’re picking colors based on a Pantone book, you’re limited to a certain number of choices. If you step out in nature, the palette is infinite.",
        "author": "Rick Rubin",
        "work": "The Creative Act: A Way of Being",
        "year": 2023,
        "translator": None,
        "hook": "How to expose artificial limits through concrete contrast",
        "why_it_lands": "The contrast between a cataloged industrial index ('a Pantone book') and wild observation ('the palette is infinite') shows how systems of classification strangle perception.",
        "tags": ["analogy", "observation", "contrast", "artistic-vision"]
    },
    {
        "quote": "Collecting seeds typically doesn’t involve a tremendous amount of effort. It’s more a receiving of a transmission.",
        "author": "Rick Rubin",
        "work": "The Creative Act: A Way of Being",
        "year": 2023,
        "translator": None,
        "hook": "How to redefine ideation as quiet reception",
        "why_it_lands": "Rubin replaces muscular strain with open antennas: creative germination is not manufactured by force, but tuned into like a radio signal.",
        "tags": ["metaphor", "receptivity", "creative-process", "simplicity"]
    },
    {
        "quote": "We are interpretation machines, and this process of labeling and detaching is efficient but not accurate.",
        "author": "Rick Rubin",
        "work": "The Creative Act: A Way of Being",
        "year": 2023,
        "translator": None,
        "hook": "How to warn against premature intellectual categorization",
        "why_it_lands": "The phrase 'interpretation machines' exposes how our survival reflex—categorizing and discarding—hastens understanding while blinding us to genuine nuance.",
        "tags": ["perception", "aphorism", "critique", "craft-insight"]
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
