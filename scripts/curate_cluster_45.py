# curate_cluster_45.py — Appends 20 curated quotes from Cluster 45 into quote-bank.json
# Usage: python3 scripts/curate_cluster_45.py
# Requires: content/quote-bank.json

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QB_PATH = ROOT / "content" / "quote-bank.json"

NEW_QUOTES = [
  # Joe Abercrombie — Before They Are Hanged (2007)
  {
    "quote": "‘That’s what the hillmen call him. Death, that is. He levels all differences. Named Men and nobodies, south or north. He catches everyone in the end, and he treats each man the same.’",
    "author": "Joe Abercrombie",
    "work": "Before They Are Hanged",
    "year": 2007,
    "hook": "How to level all social hierarchy with a single impartial noun",
    "why_it_lands": "Abercrombie gives mortality a northern fatalistic cadence, using repetitive symmetry ('Named Men and nobodies, south or north') to reduce martial glory to common dust.",
    "tags": ["dialogue", "fatalism", "rhythm"]
  },
  {
    "quote": "A choice between killing and dying is no choice at all. You have to be realistic about these things.",
    "author": "Joe Abercrombie",
    "work": "Before They Are Hanged",
    "year": 2007,
    "hook": "How to expose false dilemmas with brutal pragmatic cadence",
    "why_it_lands": "Abercrombie strips away romantic heroic posturing by pairing a stark logical impossibility with a flat, conversational colloquialism.",
    "tags": ["voice", "pragmatism", "irony"]
  },
  {
    "quote": "Battles are like men. No two are ever quite the same.",
    "author": "Joe Abercrombie",
    "work": "Before They Are Hanged",
    "year": 2007,
    "hook": "How to introduce martial complexity through home-spun simile",
    "why_it_lands": "A concise, deceptive comparison that reframes vast military chaos as individual human temperament, grounded in experience rather than theory.",
    "tags": ["simile", "understatement", "war"]
  },
  {
    "quote": "Here we still cling to the ways of our forefathers. The city is yet governed by an Imperial Legate, as it was in the Old Time, not ruled by some brigand, some petty chieftain, some false Emperor.",
    "author": "Joe Abercrombie",
    "work": "Before They Are Hanged",
    "year": 2007,
    "hook": "How to dramatize political decay through stubborn adherence to ritual",
    "why_it_lands": "Abercrombie reveals the hollow inertia of a dying empire whose officials substitute ancient ceremonial titles for actual power.",
    "tags": ["worldbuilding", "irony", "politics"]
  },

  # Joe Hill — 20th Century Ghosts (2005)
  {
    "quote": "Some silences seem to resonate with feeling. You can almost sense them trying to articulate an idea, like someone leaning toward you to whisper in your ear.",
    "author": "Joe Hill",
    "work": "20th Century Ghosts",
    "year": 2005,
    "hook": "How to give atmospheric silence the tactile weight of a human whisper",
    "why_it_lands": "Hill personifies empty acoustic space by transitioning from an abstract feeling to an uncomfortably close physical gesture.",
    "tags": ["sensory detail", "atmosphere", "horror"]
  },
  {
    "quote": "It was about young people, young healthy bodies, punched full of holes and the life pouring out in arterial gouts, not a single dream realized, not a single ambition achieved.",
    "author": "Joe Hill",
    "work": "20th Century Ghosts",
    "year": 2005,
    "hook": "How to balance visceral horror against the tragedy of unlived time",
    "why_it_lands": "The visceral violence of 'arterial gouts' is immediately counterbalanced by the sorrowful, rhythmic cadence of wasted potential.",
    "tags": ["contrast", "visceral detail", "mortality"]
  },
  {
    "quote": "When the typewriter jumped to life and began to write, Elena’s mother threw her hands up and shrieked and her legs wobbled under her, and Elena had to grab her by the arm to keep her from going down.",
    "author": "Joe Hill",
    "work": "20th Century Ghosts",
    "year": 2005,
    "hook": "How to register supernatural shock through immediate physical collapse",
    "why_it_lands": "Hill anchors the eerie impossibility of an automated typewriter in the awkward, heavy mechanics of human balance giving way.",
    "tags": ["pacing", "physicality", "supernatural"]
  },
  {
    "quote": "‘He dropped it,’ she said. ‘His hands were bloody and he got it stuck in Baxter. When he tried to pull it out, it slipped out of his hands. It fell on the floor and I picked it up. That’s why he didn’t kill me. Because I had the knife.’",
    "author": "Joe Hill",
    "work": "20th Century Ghosts",
    "year": 2005,
    "hook": "How to narrate traumatic survival through staccato physical causality",
    "why_it_lands": "The blunt, factual progression of short declarative clauses mirrors shock, stripping narrative distance until the final sentence reveals the decisive inversion of power.",
    "tags": ["suspense", "staccato", "syntax"]
  },

  # David Wong — John Dies at the End (2007)
  {
    "quote": "Imagine fifty thousand men trapped on a desert island, deprived of food and water and sex but somehow kept alive for fifty thousand years. Then, after they’ve been tormented a hundred steps beyond insanity, tortured past self-mutilation and cannibalism, somebody drops off a sculpture of a naked woman made from T-bone steaks.",
    "author": "David Wong",
    "work": "John Dies at the End",
    "year": 2007,
    "hook": "How to escalate a cosmic nightmare through grotesque comedic hyperbole",
    "why_it_lands": "Wong builds an absurdly horrifying thought experiment where mathematical extremes of suffering collide with a ludicrous, greasy pop-culture punchline.",
    "tags": ["hyperbole", "grotesque", "dark comedy"]
  },
  {
    "quote": "It was madness and desperation and deprivation and torment gone supernova, screeches and howls and, sprinkled in here and there, my own name.",
    "author": "David Wong",
    "work": "John Dies at the End",
    "year": 2007,
    "hook": "How to punctuate an abstract onslaught of noise with a personal terror",
    "why_it_lands": "After escalating sensory abstractions to astronomical proportions ('gone supernova'), Wong lands on a quiet, intimate shock that pulls the terror directly into the narrator's chest.",
    "tags": ["sound", "escalation", "psychological horror"]
  },
  {
    "quote": "It takes so much energy to keep myself on top, on the surface, at the wheel. As soon as I relax, he’ll take over. It will take over. And I’ll just be a spectator. Helpless.",
    "author": "David Wong",
    "work": "John Dies at the End",
    "year": 2007,
    "hook": "How to dramatize the psychic fatigue of fighting off possession",
    "why_it_lands": "The progression from vehicular metaphor ('at the wheel') to pronoun slippage ('he' to 'it') captures the exhausting slippage of personal autonomy.",
    "tags": ["metaphor", "internal conflict", "voice"]
  },
  {
    "quote": "The thing was as tall as the truck and walked on six legs that looked horned and armored like something seen at a seafood buffet.",
    "author": "David Wong",
    "work": "John Dies at the End",
    "year": 2007,
    "hook": "How to ground eldritch menace in suburban culinary banality",
    "why_it_lands": "Wong prevents monster description from becoming generic fantasy by comparing terrifying alien chitin to the familiar clutter of an all-you-can-eat buffet.",
    "tags": ["simile", "bizarre", "defamiliarization"]
  },

  # Michael Crichton — Congo (1980)
  {
    "quote": "It takes too long for a man to push the button—at least 1.8 seconds, which is an eternity in modern warfare.",
    "author": "Michael Crichton",
    "work": "Congo",
    "year": 1980,
    "hook": "How to dramatize human obsolescence with a biological fraction of a second",
    "why_it_lands": "Crichton grounds modern technological dread in human neurological delay, turning a tiny decimal measurement into an uncrossable gulf of vulnerability.",
    "tags": ["precision", "suspense", "techno-thriller"]
  },
  {
    "quote": "We’ve been doing it for centuries. What’s a domesticated animal—or a pocket calculator—except an attempt to give up control?",
    "author": "Michael Crichton",
    "work": "Congo",
    "year": 1980,
    "hook": "How to link prehistoric domestication to computational surrender",
    "why_it_lands": "Crichton uses casual rhetorical framing to draw an unexpected lineage from agrarian husbandry to electronic automation, exposing mankind's ongoing desire to delegate survival.",
    "tags": ["juxtaposition", "philosophy", "dialogue"]
  },
  {
    "quote": "Like Stanley, the Americans lost two-thirds of their party, and emerged from the jungle as desperately as Stanley’s men a century before.",
    "author": "Michael Crichton",
    "work": "Congo",
    "year": 1980,
    "hook": "How to haunt modern technological hubris with historical repetition",
    "why_it_lands": "Crichton deflates high-tech corporate hubris by measuring modern disaster against Victorian colonial catastrophe in identical fractional terms.",
    "tags": ["irony", "history", "understatement"]
  },
  {
    "quote": "The hair is definitely not human. Cross section doesn’t match. Some kind of animal hair, close to human.",
    "author": "Michael Crichton",
    "work": "Congo",
    "year": 1980,
    "hook": "How to evoke biological horror through forensic laboratory staccato",
    "why_it_lands": "Terse laboratory sentences deliver a creeping taxonomic anomaly without relying on melodrama, letting clinical disconfirmation generate dread.",
    "tags": ["dialogue", "suspense", "science"]
  },

  # Isaac Asimov — Foundation (1951)
  {
    "quote": "Violence is the last refuge of the incompetent.",
    "author": "Isaac Asimov",
    "work": "Foundation",
    "year": 1951,
    "hook": "How to turn pacifism into an intellectual weapon with an uncompromising noun",
    "why_it_lands": "Asimov inverts the conventional romanticization of brute force, defining physical aggression not as strength but as an admission of failed imagination.",
    "tags": ["aphorism", "intellect", "theme"]
  },
  {
    "quote": "It pays to be obvious, especially if you have a reputation for subtlety.",
    "author": "Isaac Asimov",
    "work": "Foundation",
    "year": 1951,
    "hook": "How to weaponize transparency against suspicious rivals",
    "why_it_lands": "A razor-sharp tactical paradox that exploits the opponent’s tendency to over-interpret simplicity, turning plain honesty into an impenetrable disguise.",
    "tags": ["paradox", "cynicism", "strategy"]
  },
  {
    "quote": "To succeed, planning alone is insufficient. One must improvise as well.",
    "author": "Isaac Asimov",
    "work": "Foundation",
    "year": 1951,
    "hook": "How to puncture deterministic confidence with tactical necessity",
    "why_it_lands": "In a novel premised on mathematical prediction of galactic history, Asimov succinctly balances long-range statistical determinism against agile individual agency.",
    "tags": ["balance", "philosophy", "action"]
  },
  {
    "quote": "A nuclear blaster is a good weapon, but it can point both ways.",
    "author": "Isaac Asimov",
    "work": "Foundation",
    "year": 1951,
    "hook": "How to warn against technological hubris through symmetrical leverage",
    "why_it_lands": "A folk idiom applied to advanced galactic weaponry that exposes how martial superiority inherently breeds equal and opposite vulnerability.",
    "tags": ["idiom", "technology", "leverage"]
  }
]

def main():
    with open(QB_PATH, "r", encoding="utf-8") as f:
        bank = json.load(f)

    existing_quotes = set(q["quote"].strip() for q in bank)
    added = 0
    for q in NEW_QUOTES:
        if q["quote"].strip() not in existing_quotes:
            bank.append(q)
            existing_quotes.add(q["quote"].strip())
            added += 1

    with open(QB_PATH, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)

    print(f"Added {added} new quotes. Total bank size now: {len(bank)}")

if __name__ == "__main__":
    main()
