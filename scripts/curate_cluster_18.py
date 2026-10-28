#!/usr/bin/env python3
"""
curate_cluster_18.py — Curates 20 vetted quotes from Cluster 18 (Satirical Fabulism & Cultural Dissection)
into content/quote-bank.json.
"""

import json
from pathlib import Path

QUOTE_BANK_PATH = Path("/Users/apple/Documents/Claude Code/quotes-project/content/quote-bank.json")

NEW_QUOTES = [
    # Nikolai Gogol — Dead Souls
    {
        "quote": "“See that? There’s a wheel for you! What do you say, would that wheel make it as far as Moscow, if it so happened, or wouldn’t it?”",
        "author": "Nikolai Gogol",
        "work": "Dead Souls",
        "year": 1842,
        "translator": "Richard Pevear & Larissa Volokhonsky",
        "hook": "How to anchor epic satire in provincial small-talk",
        "why_it_lands": "Gogol opens his epic with two peasants debating the geographical durability of a carriage wheel, immediately setting the tone of Russian realism—where grandiose destiny begins in roadside mud.",
        "tags": ["opening", "dialogue", "satire", "vernacular"]
    },
    {
        "quote": "“What is our life? A vale wherein grief dwells. What is this world? A crowd of people who do not feel.”",
        "author": "Nikolai Gogol",
        "work": "Dead Souls",
        "year": 1842,
        "translator": "Richard Pevear & Larissa Volokhonsky",
        "hook": "How to pair romantic lament with biting social contempt",
        "why_it_lands": "Two paired rhetorical questions move from traditional elegy to sociological diagnosis: the tragedy of the cosmos is not suffering itself, but the frozen indifference of human spectators.",
        "tags": ["rhetorical-question", "melancholy", "satire", "symmetry"]
    },
    {
        "quote": "“You’re both drunkards, you’re ruining the master, you bottomless barrels! You think the master doesn’t know it? There he is, and he can hear you.”",
        "author": "Nikolai Gogol",
        "work": "Dead Souls",
        "year": 1842,
        "translator": "Richard Pevear & Larissa Volokhonsky",
        "hook": "How to orchestrate domestic shouting with third-person menace",
        "why_it_lands": "The colorful vernacular insults ('bottomless barrels') accelerate until the sudden dramatic reveal: the master is sitting right there, listening to his own servants rob him blind.",
        "tags": ["comedy", "vernacular", "pacing", "dialogue"]
    },
    {
        "quote": "“You’ll obey that first good impulse and forget your accounting.”",
        "author": "Nikolai Gogol",
        "work": "Dead Souls",
        "year": 1842,
        "translator": "Richard Pevear & Larissa Volokhonsky",
        "hook": "How to treat generosity as a fatal financial defect",
        "why_it_lands": "Ten words dissect moral ruin through commercial arithmetic: the villain praises the victim's virtue only to diagnose it as an incurable vulnerability that guarantees bankruptcy.",
        "tags": ["cynicism", "moral-irony", "brevity", "character-voice"]
    },

    # Etgar Keret — The Seven Good Years
    {
        "quote": "“It’s not the emergencies,” the thin one insists. “I have no problem with accidents and things. It’s the terrorist attacks, I’m telling you. They put a damper on everything.”",
        "author": "Etgar Keret",
        "work": "The Seven Good Years",
        "year": 2015,
        "translator": "Sondra Silverston, Miriam Shlesinger & Arun Budman",
        "hook": "How to deploy bureaucratic understatement in wartime",
        "why_it_lands": "Keret captures the surreal domesticity of living under siege: a taxi driver treats bomb attacks not with existential terror, but as an annoying administrative inconvenience that ruins his day.",
        "tags": ["understatement", "satire", "absurdism", "dialogue"]
    },
    {
        "quote": "Destroying buildings and killing things. It’s so much fun.",
        "author": "Etgar Keret",
        "work": "The Seven Good Years",
        "year": 2015,
        "translator": "Sondra Silverston, Miriam Shlesinger & Arun Budman",
        "hook": "How to voice destructive impulse with childlike simplicity",
        "why_it_lands": "Two blunt coordinate clauses strip civilization of its polite veneer, exposing the raw, joyful catharsis of pure demolition.",
        "tags": ["candor", "dark-comedy", "brevity", "visceral-drive"]
    },
    {
        "quote": "“It’s actually an educational game that teaches you not to steal.”",
        "author": "Etgar Keret",
        "work": "The Seven Good Years",
        "year": 2015,
        "translator": "Sondra Silverston, Miriam Shlesinger & Arun Budman",
        "hook": "How to rebrand punitive discipline as moral pedagogy",
        "why_it_lands": "The earnest defense of a bizarre household ritual exposes the classic parental rationalization—disguising petty retaliation as character-building education.",
        "tags": ["satire", "pedagogy", "rationalization", "dialogue"]
    },
    {
        "quote": "“A lot of unlucky people are going to die in this damn war,” Avraham said, trying to calm the frightened woman, “but I won’t be one of them.”",
        "author": "Etgar Keret",
        "work": "The Seven Good Years",
        "year": 2015,
        "translator": "Sondra Silverston, Miriam Shlesinger & Arun Budman",
        "hook": "How to comfort someone through audacious personal arrogance",
        "why_it_lands": "The comically monstrous consolation: Avraham acknowledges the statistical certainty of slaughter, but offers absolute immunity based solely on the stubborn certainty of his own luck.",
        "tags": ["dialogue", "irony", "survival", "black-humor"]
    },

    # Walter M. Miller Jr. — A Canticle for Leibowitz
    {
        "quote": "Hellbound. Unblessed. Unshrived. Under our very noses.",
        "author": "Walter M. Miller Jr.",
        "work": "A Canticle for Leibowitz",
        "year": 1959,
        "translator": None,
        "hook": "How to stack theological condemnations into rhythmic staccato",
        "why_it_lands": "Three past participles with negative prefixes ('Hellbound. Unblessed. Unshrived.') fall like mallet strikes, concluding with the domestic proximity of damnation.",
        "tags": ["staccato", "theology", "rhythm", "brevity"]
    },
    {
        "quote": "“Holy Leibowitz! Did we labor for this?”",
        "author": "Walter M. Miller Jr.",
        "work": "A Canticle for Leibowitz",
        "year": 1959,
        "translator": None,
        "hook": "How to deflate centuries of sacred labor in five words",
        "why_it_lands": "An invocation of the monastery's founding patron saint collapses instantly into exasperated bathos: discovering that centuries of monastic preservation protected an ancient shopping list.",
        "tags": ["bathos", "dialogue", "irony", "brevity"]
    },
    {
        "quote": "“Pain’s the only evil I know about. It’s the only one I can fight.”",
        "author": "Walter M. Miller Jr.",
        "work": "A Canticle for Leibowitz",
        "year": 1959,
        "translator": None,
        "hook": "How to reduce secular ethics to somatic suffering",
        "why_it_lands": "A medical officer strips theology of sin and redemption: in a devastated post-nuclear world, abstract evil vanishes, leaving physical agony as the only enemy worthy of combat.",
        "tags": ["dialogue", "ethics", "pragmatism", "conflict"]
    },
    {
        "quote": "“Insult me,” he said in mocking tones, “rail at me, bait me, persecute me—but do you know what I’ll say?”",
        "author": "Walter M. Miller Jr.",
        "work": "A Canticle for Leibowitz",
        "year": 1959,
        "translator": None,
        "hook": "How to invite hostility to assert moral invulnerability",
        "why_it_lands": "A sequence of four imperative verbs ('Insult me... rail at me, bait me, persecute me') challenges the accuser to exhaust his wrath, turning martyrdom into theatrical defiance.",
        "tags": ["dialogue", "imperatives", "defiance", "rhythm"]
    },

    # Neil Postman — Amusing Ourselves to Death
    {
        "quote": "The value of telegraphy is undermined by applying the tests of permanence, continuity or coherence.",
        "author": "Neil Postman",
        "work": "Amusing Ourselves to Death",
        "year": 1985,
        "translator": None,
        "hook": "How to evaluate rapid communication against classical standards",
        "why_it_lands": "Postman subjects electronic instantaneity to three rigorous tests: permanence, continuity, and coherence. Evaluated by these standards, the information age is exposed as shallow novelty.",
        "tags": ["media-theory", "intellectual-standard", "critique", "triad"]
    },
    {
        "quote": "“Silence will be more acceptable to me in the discussion of these questions than applause.”",
        "author": "Neil Postman",
        "work": "Amusing Ourselves to Death",
        "year": 1985,
        "translator": None,
        "hook": "How to silence an audience to demand cognitive rigor",
        "why_it_lands": "A speaker rejects the flattering sugar of applause, demanding cold silence instead: when issues are genuinely grave, enthusiastic cheering is merely entertainment masquerading as consensus.",
        "tags": ["rhetoric", "candor", "seriousness", "dialogue"]
    },
    {
        "quote": "The men were less concerned with giving arguments than with “giving off” impressions, which is what television does best.",
        "author": "Neil Postman",
        "work": "Amusing Ourselves to Death",
        "year": 1985,
        "translator": None,
        "hook": "How to dissect modern politics with a single prepositional shift",
        "why_it_lands": "Postman shifts from 'giving' arguments to 'giving off' impressions, pinpointing the precise moment political philosophy was replaced by cosmetic aesthetics.",
        "tags": ["wordplay", "media-critique", "precision", "satire"]
    },
    {
        "quote": "“Sesame Street” encourages children to love television. Just as reading a book—any kind of book—promotes a particular orientation toward learning, watching a television show does the same.",
        "author": "Neil Postman",
        "work": "Amusing Ourselves to Death",
        "year": 1985,
        "translator": None,
        "hook": "How to challenge progressive consensus through medium analysis",
        "why_it_lands": "Postman attacks the sacred cow of educational television: the lesson of the show is never the alphabet or numbers, but the medium itself—teaching infants that learning must always entertain.",
        "tags": ["cultural-critique", "provocation", "pedagogy", "insight"]
    },

    # Satyajit Ray — The Best of Satyajit Ray
    {
        "quote": "Growing up amidst people from various parts of the country, she learnt to communicate with those who did not speak her language, and whose language she could not understand.",
        "author": "Satyajit Ray",
        "work": "The Best of Satyajit Ray",
        "year": 2001,
        "translator": "Gopa Majumdar",
        "hook": "How to define polyglot empathy beyond vocabulary",
        "why_it_lands": "Ray balances two clauses of incomprehension to reveal a deeper human truth: understanding does not require shared vocabulary, but the patient observation of human gesture.",
        "tags": ["observation", "empathy", "language", "cadence"]
    },
    {
        "quote": "“It is not clearly understood why human beings should laugh. Great philosophers have racked their brains to find out why; but have not succeeded.”",
        "author": "Satyajit Ray",
        "work": "The Best of Satyajit Ray",
        "year": 2001,
        "translator": "Gopa Majumdar",
        "hook": "How to introduce a surreal premise with mock philosophical gravity",
        "why_it_lands": "Ray uses the solemn failure of Western philosophy as a preamble to introduce an uncanny mystery: human laughter as an inexplicable, irrational biological convulsion.",
        "tags": ["philosophical-parody", "mystery", "fable", "voice"]
    },
    {
        "quote": "“Those fiendish mosquitoes are singing in my ears again. So that’s how the son of a mighty empire has to meet his end—at the hands of a tiny insect.”",
        "author": "Satyajit Ray",
        "work": "The Best of Satyajit Ray",
        "year": 2001,
        "translator": "Gopa Majumdar",
        "hook": "How to reduce imperial hubris to a mosquito bite",
        "why_it_lands": "The colonial conqueror dies not in a heroic duel, but in the swampy humiliation of insect song—exposing the fragility of empire before tropical biology.",
        "tags": ["colonial-satire", "bathos", "irony", "mortality"]
    },
    {
        "quote": "“Actually, it was an illness I used to suffer from. I mean, I am not really a thief. There is a medical term for it which escapes me at the moment.”",
        "author": "Satyajit Ray",
        "work": "The Best of Satyajit Ray",
        "year": 2001,
        "translator": "Gopa Majumdar",
        "hook": "How to disguise petty larceny in evasive clinical jargon",
        "why_it_lands": "The character reaches for the respectable shield of psychiatric diagnosis, but the punchline lands when he conveniently forgets the medical term, exposing his transparent excuse.",
        "tags": ["dialogue", "character-revelation", "irony", "comedy"]
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
