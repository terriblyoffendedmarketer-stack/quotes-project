# curate_cluster_46.py — Appends 20 curated quotes from Cluster 46 into quote-bank.json
# Usage: python3 scripts/curate_cluster_46.py
# Requires: content/quote-bank.json

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QB_PATH = ROOT / "content" / "quote-bank.json"

NEW_QUOTES = [
  # Paul Auster — The Invention of Solitude (1982)
  {
    "quote": "Things are inert: they have meaning only in function of the life that makes use of them. When that life ends, the things change, even though they remain the same.",
    "author": "Paul Auster",
    "work": "The Invention of Solitude",
    "year": 1982,
    "hook": "How to capture the sudden hollow weight of an inherited room",
    "why_it_lands": "Auster articulates the quiet uncanny horror of bereavement: objects outlive their owners without alteration, yet losing their animating human context renders them utterly alien.",
    "tags": ["grief", "objects", "philosophy"]
  },
  {
    "quote": "It was not blindness so much as a failure of imagination.",
    "author": "Paul Auster",
    "work": "The Invention of Solitude",
    "year": 1982,
    "hook": "How to redefine emotional distance with an unsparing noun",
    "why_it_lands": "Rather than diagnosing a lack of physical sight, Auster pinpoints the deliberate refusal to construct the inner life of another person.",
    "tags": ["characterization", "precision", "memoir"]
  },
  {
    "quote": "It would be impossible to say that we are not haunted.",
    "author": "Paul Auster",
    "work": "The Invention of Solitude",
    "year": 1982,
    "hook": "How to state an uncanny psychological truth with double negation",
    "why_it_lands": "Auster uses litotes to capture the pervasive, inescapable lingering of ancestral and personal memory without slipping into Gothic melodrama.",
    "tags": ["syntax", "memory", "understatement"]
  },
  {
    "quote": "Life is death, and death is a kind of life.",
    "author": "Paul Auster",
    "work": "The Invention of Solitude",
    "year": 1982,
    "hook": "How to distill an existential threshold into chiasmic balance",
    "why_it_lands": "A stark, mirrored balance that strips away decorative consolation to force the reader to contemplate mortality as an ongoing condition of consciousness.",
    "tags": ["chiasmus", "mortality", "paradox"]
  },

  # Peter Frankopan — The Silk Roads: A New History of the World (2015)
  {
    "quote": "It was, as one leading scholar has put it, a Versailles moment: too many towns, forts and important locations were handed over with too little thought about how they could be held.",
    "author": "Peter Frankopan",
    "work": "The Silk Roads: A New History of the World",
    "year": 2015,
    "hook": "How to compress geopolitical overreach into a historical shorthand",
    "why_it_lands": "Frankopan anchors military overextension in an evocative diplomatic archetype, showing how swift imperial conquests inevitably sow the seeds of logistical collapse.",
    "tags": ["history", "metaphor", "geopolitics"]
  },
  {
    "quote": "The hour of need in the east looked like it might deliver unity to the church.",
    "author": "Peter Frankopan",
    "work": "The Silk Roads: A New History of the World",
    "year": 2015,
    "hook": "How to reveal the predatory optimism behind religious diplomacy",
    "why_it_lands": "Frankopan shows how political leadership opportunistically reframes catastrophic foreign crises as instruments for domestic consolidation.",
    "tags": ["irony", "diplomacy", "power"]
  },
  {
    "quote": "He has a very large palace, entirely roofed with fine gold.",
    "author": "Peter Frankopan",
    "work": "The Silk Roads: A New History of the World",
    "year": 2015,
    "hook": "How to evoke mythic wealth through medieval unadorned scale",
    "why_it_lands": "The bare simplicity of Marco Polo’s report captures the hypnotic pull that Central Asian trade routes exerted on European imagination.",
    "tags": ["imagery", "scale", "simplicity"]
  },
  {
    "quote": "He is a miserly king, not a man from whom one might hope for a rich present.",
    "author": "Peter Frankopan",
    "work": "The Silk Roads: A New History of the World",
    "year": 2015,
    "hook": "How to puncture royal majesty with a travel chronicler's blunt disappointment",
    "why_it_lands": "Frankopan juxtaposes legendary imperial reputation against the pragmatic, transactional ledger of a traveler seeking immediate patronage.",
    "tags": ["voice", "irony", "portraiture"]
  },

  # Samin Nosrat — Salt, Fat, Acid, Heat (2017)
  {
    "quote": "Imagine that you’re cooking green beans in a pot of water. If the water is unseasoned or only lightly seasoned, then its salinity will be lower than that of the beans, and the salt from the beans will actually leach out into the cooking water, leaving the beans limp and dull.",
    "author": "Samin Nosrat",
    "work": "Salt, Fat, Acid, Heat",
    "year": 2017,
    "hook": "How to explain chemical osmosis through domestic sensory consequence",
    "why_it_lands": "Nosrat makes culinary science intuitive by tying an invisible molecular principle to a universally recognizable failure of texture and color.",
    "tags": ["sensory detail", "craft", "explanation"]
  },
  {
    "quote": "You might flinch upon seeing just how much salt this takes, but remember, most of the salt ends up going down the drain.",
    "author": "Samin Nosrat",
    "work": "Salt, Fat, Acid, Heat",
    "year": 2017,
    "hook": "How to disarm cook's anxiety with domestic reassurance",
    "why_it_lands": "Nosrat anticipates the reader's instinctual resistance, normalizing an apparently excessive physical quantity by explaining the mechanics of medium versus absorption.",
    "tags": ["voice", "reassurance", "process"]
  },
  {
    "quote": "Short doughs are the epitome of tenderness, crumbling and melting in your mouth.",
    "author": "Samin Nosrat",
    "work": "Salt, Fat, Acid, Heat",
    "year": 2017,
    "hook": "How to define textural mastery with twin sensory verbs",
    "why_it_lands": "Nosrat's pairing of 'crumbling' (structural yield under pressure) and 'melting' (thermal dissolution) paints an exact tactile target on the palate.",
    "tags": ["texture", "verbs", "food writing"]
  },
  {
    "quote": "Pat its skin dry before you stick it in the oven, so it can brown, instead of steam.",
    "author": "Samin Nosrat",
    "work": "Salt, Fat, Acid, Heat",
    "year": 2017,
    "hook": "How to isolate the culinary boundary between roasting and steaming",
    "why_it_lands": "A single crisp imperative that contrasts surface moisture against thermal caramelization, turning chemistry into practical kitchen discipline.",
    "tags": ["imperative", "contrast", "instruction"]
  },

  # T. Kingfisher — What Moves the Dead (2022)
  {
    "quote": "They watch, all the time. Not the way hares stare at you and bolt if you move. They’ll come up to you and watch.",
    "author": "T. Kingfisher",
    "work": "What Moves the Dead",
    "year": 2022,
    "hook": "How to invert animal instinct to manufacture uncanny dread",
    "why_it_lands": "Kingfisher transforms a skittish prey animal into an unnerving observer simply by subtracting its natural impulse to flee.",
    "tags": ["horror", "defamiliarization", "suspense"]
  },
  {
    "quote": "Saprophytic fungi—ah, that is to say, those that feed upon decaying organic matter—are exceedingly common. Unsightly, perhaps, but they pose no threat to living creatures.",
    "author": "T. Kingfisher",
    "work": "What Moves the Dead",
    "year": 2022,
    "hook": "How to weaponize scientific reassurance as dramatic irony",
    "why_it_lands": "A pedantic botanical definition delivered with serene confidence, set against creeping environmental horror the reader knows is already fatal.",
    "tags": ["irony", "science", "dialogue"]
  },
  {
    "quote": "Americans, so far as I know, have no sworn, but I am given to understand that they have very lurid periodicals.",
    "author": "T. Kingfisher",
    "work": "What Moves the Dead",
    "year": 2022,
    "hook": "How to reveal cultural estrangement through dry satirical assessment",
    "why_it_lands": "Kingfisher captures an outsider soldier's dry assessment of foreign mores by balancing martial honor against trashy tabloid print.",
    "tags": ["humor", "voice", "satire"]
  },
  {
    "quote": "She will be entirely herself one morning, and then by afternoon, I will find her speaking to the servants as if she is a small child. She points at things and asks for their names and seems astonished.",
    "author": "T. Kingfisher",
    "work": "What Moves the Dead",
    "year": 2022,
    "hook": "How to chart cognitive decay through lost vocabulary",
    "why_it_lands": "Rather than describing madness generically, Kingfisher tracks the eerie erasure of adulthood through a sudden regression to pointing and re-learning common nouns.",
    "tags": ["psychological horror", "pathos", "pacing"]
  },

  # Alexandre Dumas — The Count of Monte Cristo (1844)
  {
    "quote": "Gentlemen, when you grow tired of being actors and wish to become spectators again, you know that you have a place at my windows.",
    "author": "Alexandre Dumas",
    "work": "The Count of Monte Cristo",
    "year": 1844,
    "hook": "How to reduce human tragedy to theatrical entertainment",
    "why_it_lands": "The Count reframes public executions and worldly struggle as mere street drama, positioning himself above humanity in a private box.",
    "tags": ["dialogue", "metaphor", "power"]
  },
  {
    "quote": "Nothing is so rare as silence; nothing so precious as sound advice.",
    "author": "Alexandre Dumas",
    "work": "The Count of Monte Cristo",
    "year": 1844,
    "hook": "How to elevate verbal economy through parallel aphorisms",
    "why_it_lands": "Dumas pairs acoustic restraint with intellectual guidance, establishing patient silence as the prerequisite for power.",
    "tags": ["aphorism", "parallelism", "wisdom"]
  },
  {
    "quote": "It was time for him to go back among men and take up the rank, influence and power which great wealth gives in this world.",
    "author": "Alexandre Dumas",
    "work": "The Count of Monte Cristo",
    "year": 1844,
    "hook": "How to herald a character's return with monumental social clarity",
    "why_it_lands": "A sweeping, declarative transition that closes the chapter of monastic imprisonment and inaugurates calculated worldly vengeance.",
    "tags": ["transition", "revenge", "grandeur"]
  },
  {
    "quote": "I realize it would be useless for me to struggle against the vengeance of God which has just struck me. There’s no need for proof—everything this young man has brought against me is true.",
    "author": "Alexandre Dumas",
    "work": "The Count of Monte Cristo",
    "year": 1844,
    "hook": "How to stage the sudden collapse of legal arrogance",
    "why_it_lands": "The proud crown prosecutor abandons all procedural defense in a single stroke, recognizing moral retribution where legal arguments fail.",
    "tags": ["justice", "climax", "speech"]
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
