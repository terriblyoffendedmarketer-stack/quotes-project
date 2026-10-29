# curate_cluster_47.py — Appends 20 curated quotes from Cluster 47 into quote-bank.json
# Usage: python3 scripts/curate_cluster_47.py
# Requires: content/quote-bank.json

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QB_PATH = ROOT / "content" / "quote-bank.json"

NEW_QUOTES = [
  # Patrick Rothfuss — The Name of the Wind (2007)
  {
    "quote": "The world is a map, and we are the ink.",
    "author": "Patrick Rothfuss",
    "work": "The Name of the Wind",
    "year": 2007,
    "hook": "How to condense narrative metaphysics into an intimate cartographic metaphor",
    "why_it_lands": "Rothfuss fuses human agency with physical geography, establishing that lives do not merely traverse the terrain but actively author its substance.",
    "tags": ["metaphor", "worldbuilding", "poetics"]
  },
  {
    "quote": "Etiquette is a set of rules people use so they can be rude to each other in public.",
    "author": "Patrick Rothfuss",
    "work": "The Name of the Wind",
    "year": 2007,
    "hook": "How to dismantle polite society with a cynical social aphorism",
    "why_it_lands": "Rothfuss exposes high-born manners not as kindness, but as an elaborate ceremonial armor devised to inflict cruelty without physical contact.",
    "tags": ["aphorism", "cynicism", "dialogue"]
  },
  {
    "quote": "Man wants his daughter to have a fine house with a view, that’s all to the good. But when you’re diggin the foundation and you find bones and such, and you don’t stop…that’s a whole new type of stupid.",
    "author": "Patrick Rothfuss",
    "work": "The Name of the Wind",
    "year": 2007,
    "hook": "How to ground supernatural dread in working-class construction common sense",
    "why_it_lands": "Rothfuss undercuts epic Gothic tropes by viewing terrifying portents through the unromantic, weary pragmatism of a laborer who knows when to drop his shovel.",
    "tags": ["voice", "folklore", "humor"]
  },
  {
    "quote": "It is always, always, expressly forbidden to cause harm with sympathy, especially to a master.",
    "author": "Patrick Rothfuss",
    "work": "The Name of the Wind",
    "year": 2007,
    "hook": "How to formulate an institutional prohibition with an ominous hierarchy",
    "why_it_lands": "The chilling repetition of 'always' paired with the specialized magic terminology establishes strict institutional danger and the constant temptation to break it.",
    "tags": ["rules", "worldbuilding", "suspense"]
  },

  # Leo Tolstoy — War and Peace (1869)
  {
    "quote": "‘The Prussians are our faithful allies who have only betrayed us three times in three years.’",
    "author": "Leo Tolstoy",
    "work": "War and Peace",
    "year": 1869,
    "translator": "Louise and Aylmer Maude",
    "hook": "How to skewer military alliances through deadpan arithmetic irony",
    "why_it_lands": "Tolstoy delivers a scathing geopolitical indictment with the polite, unblinking courtesy of ballroom diplomacy.",
    "tags": ["irony", "politics", "understatement"]
  },
  {
    "quote": "After all, you must understand that besides your pleasure there is such a thing as other people’s happiness and peace, and that you are ruining a whole life for the sake of amusing yourself!",
    "author": "Leo Tolstoy",
    "work": "War and Peace",
    "year": 1869,
    "translator": "Louise and Aylmer Maude",
    "hook": "How to confront selfish hedonism with moral fury",
    "why_it_lands": "A searing moral rebuke that contrasts momentary private amusement against the total structural collapse of another human being’s existence.",
    "tags": ["morality", "dialogue", "conflict"]
  },
  {
    "quote": "‘It is not in the eye of the beholder that truth resides, but in the world itself,’ he said to himself.",
    "author": "Leo Tolstoy",
    "work": "War and Peace",
    "year": 1869,
    "translator": "Louise and Aylmer Maude",
    "hook": "How to rescue objective truth from solipsism with a quiet conviction",
    "why_it_lands": "Tolstoy inverts the fashionable relativistic cliché, grounding moral sanity in the external reality of the universe rather than the shifting moods of the observer.",
    "tags": ["philosophy", "truth", "interiority"]
  },
  {
    "quote": "‘You may go and kill whom you please, but I don’t want to do so any more!’",
    "author": "Leo Tolstoy",
    "work": "War and Peace",
    "year": 1869,
    "translator": "Louise and Aylmer Maude",
    "hook": "How to record the abrupt exhaustion of a soldier's obedience",
    "why_it_lands": "A stark, unadorned declaration that strips military heroism of its collective glory, isolating individual conscience against the mechanized slaughter of war.",
    "tags": ["war", "clarity", "conscience"]
  },

  # Umberto Eco — How to Travel with a Salmon & Other Essays (1992)
  {
    "quote": "For such is the fate of parody: it must never fear exaggerating. If it strikes home, it will only prefigure something that others will then do without a smile—and without a blush—in steadfast, virile seriousness.",
    "author": "Umberto Eco",
    "work": "How to Travel with a Salmon & Other Essays",
    "year": 1992,
    "translator": "William Weaver",
    "hook": "How to define the predictive destiny of literary parody",
    "why_it_lands": "Eco identifies the cruel law of satire: mock an absurdity loud enough and society will adopt it as official policy within a decade.",
    "tags": ["satire", "philosophy", "prophecy"]
  },
  {
    "quote": "The peas have only two alternatives: either they roll down your shirtfront or they fall on your fly.",
    "author": "Umberto Eco",
    "work": "How to Travel with a Salmon & Other Essays",
    "year": 1992,
    "translator": "William Weaver",
    "hook": "How to reduce airline dining to binary gravitational humiliation",
    "why_it_lands": "Eco formulates a mock-scientific binary law of motion that punctures the glamorous illusion of modern air travel.",
    "tags": ["humor", "observation", "hyperbole"]
  },
  {
    "quote": "When revolutionary inventions become widely accessible, they cease to be accessible.",
    "author": "Umberto Eco",
    "work": "How to Travel with a Salmon & Other Essays",
    "year": 1992,
    "translator": "William Weaver",
    "hook": "How to formulate the paradox of democratized infrastructure",
    "why_it_lands": "A razor-sharp aphorism on congestion: once a breakthrough is available to all, its universal adoption inevitably recreates the exact paralysis it was designed to solve.",
    "tags": ["aphorism", "paradox", "technology"]
  },
  {
    "quote": "Posterity, as we know, is voracious and easily pleased. In order to have something to write about, any writing by others will do.",
    "author": "Umberto Eco",
    "work": "How to Travel with a Salmon & Other Essays",
    "year": 1992,
    "translator": "William Weaver",
    "hook": "How to deflate academic legacy through voracious indifference",
    "why_it_lands": "Eco mocks the solemn industry of literary preservation, revealing that future scholars do not sift for genius but simply scavenge whatever paper survived the fire.",
    "tags": ["cynicism", "academia", "legacy"]
  },

  # Max Brooks — World War Z (2006)
  {
    "quote": "‘It was all too intimate,’ the chairperson said during one of our many ‘animated’ discussions. ‘Too many opinions, too much feeling. That’s not what this report is about. We need clear facts and figures, unclouded by the human factor.’",
    "author": "Max Brooks",
    "work": "World War Z",
    "year": 2006,
    "hook": "How to dramatize bureaucratic erasure of human suffering",
    "why_it_lands": "Brooks captures the clinical horror of post-war administrative commissions, which purge the messiness of grief to produce sanitized statistical reports.",
    "tags": ["dialogue", "bureaucracy", "satire"]
  },
  {
    "quote": "‘And in the end, isn’t the human factor the only true difference between us and the enemy we now refer to as ‘the living dead’?’",
    "author": "Max Brooks",
    "work": "World War Z",
    "year": 2006,
    "hook": "How to invert an institutional dismissal into an existential defense",
    "why_it_lands": "Brooks reframes the bureaucrat's liability ('the human factor') as the sole moral boundary separating civilization from cannibalistic oblivion.",
    "tags": ["rhetorical question", "humanity", "theme"]
  },
  {
    "quote": "The dead were coming. Slow and deliberate, and just as tightly packed as the refugees they were devouring.",
    "author": "Max Brooks",
    "work": "World War Z",
    "year": 2006,
    "hook": "How to mirror civilian panic against relentless mechanical momentum",
    "why_it_lands": "Brooks links the fleeing crowds and the pursuing horde through identical density ('just as tightly packed'), highlighting the terrible symmetry of mass panic.",
    "tags": ["pacing", "visceral detail", "horror"]
  },
  {
    "quote": "Cities were dying, whole countries. We listened to the last report from Buenos Aires, the evacuation of the Japanese home islands, too.",
    "author": "Max Brooks",
    "work": "World War Z",
    "year": 2006,
    "hook": "How to register planetary collapse through radio silence",
    "why_it_lands": "A chilling, telescopic compression of continental catastrophe into clipped, ambient broadcasts heard from an isolated perch.",
    "tags": ["scale", "apocalypse", "understatement"]
  },

  # Virginia Feito — Victorian Psycho (2024)
  {
    "quote": "‘It sounded like a woman screaming in the night.’ ‘That’s Yorkshire for you.’",
    "author": "Virginia Feito",
    "work": "Victorian Psycho",
    "year": 2024,
    "hook": "How to deflate nocturnal terror with provincial dismissal",
    "why_it_lands": "Feito pairs a terrifying auditory omen with deadpan regional stoicism, transforming Gothic horror into a dry comedic punchline.",
    "tags": ["dialogue", "dark comedy", "gothic"]
  },
  {
    "quote": "I have never tasted swan before and so do not know if it is always like this or if it has been overcooked, which tends to occur nowadays because undercooking is thought to exacerbate women’s weak nervous conditions.",
    "author": "Virginia Feito",
    "work": "Victorian Psycho",
    "year": 2024,
    "hook": "How to satirize medical misogyny through dinner party critique",
    "why_it_lands": "Feito weaves Victorian pseudoscientific anxieties about female fragility directly into the fussy, decadent mechanics of eating game birds.",
    "tags": ["satire", "voice", "historical irony"]
  },
  {
    "quote": "‘Nothing a good rest devoid of intellectual strain can’t cure,’ Mr Pounds says brightly.",
    "author": "Virginia Feito",
    "work": "Victorian Psycho",
    "year": 2024,
    "hook": "How to capture Victorian patriarchal condescension in a cheerful diagnosis",
    "why_it_lands": "Feito skewers the historical medical habit of prescribing enforced domestic stupidity as the ultimate remedy for female intelligence.",
    "tags": ["irony", "patriarchy", "dialogue"]
  },
  {
    "quote": "The ghosts of the servants are reflected on the silver. They wait at the sideboard to serve the food and drinks, looking upon the scene through a veil of their superiors’ indifference.",
    "author": "Virginia Feito",
    "work": "Victorian Psycho",
    "year": 2024,
    "hook": "How to reveal class invisibility through polished dining silver",
    "why_it_lands": "Feito captures the eerie phantom existence of Victorian domestic servants, present only as distorted metallic reflections ignored by the diners they sustain.",
    "tags": ["imagery", "class", "atmosphere"]
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
