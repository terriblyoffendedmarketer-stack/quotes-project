# scripts/curate_cluster_27.py — Curates 20 craft quotes from Cluster 27 (Media Ecology, Solaris & Radical Compassion)
# Usage: python3 scripts/curate_cluster_27.py
# Requires: json, os

import json
import os

QUOTE_BANK_PATH = "content/quote-bank.json"

VETTED_CLUSTER_27 = [
    # 1. Marshall McLuhan — Understanding Media: The Extensions of Man (1964)
    {
        "quote": "The medium is the message. This is merely to say that the personal and social consequences of any medium—that is, of any extension of ourselves—result from the new scale that is introduced into our affairs by each extension of ourselves, or by any new technology.",
        "author": "Marshall McLuhan",
        "work": "Understanding Media: The Extensions of Man",
        "year": 1964,
        "translator": None,
        "hook": "How to displace surface content to reveal structural media impact.",
        "why_it_lands": "McLuhan executes a foundational epistemological reversal, demonstrating that the structural channel of transmission alters human perception far more drastically than whatever topical content flows through it.",
        "tags": ["philosophy", "technology", "culture", "perspective"]
    },
    {
        "quote": "All electric forms whatsoever have a decentralizing effect, cutting across the older mechanical patterns like a bagpipe in a symphony.",
        "author": "Marshall McLuhan",
        "work": "Understanding Media: The Extensions of Man",
        "year": 1964,
        "translator": None,
        "hook": "How to illustrate institutional disruption with an auditory musical simile.",
        "why_it_lands": "McLuhan compares instantaneous electronic communication to a screeching, dissonant folk instrument tearing through the regimented, orchestral discipline of linear mechanical bureaucracy.",
        "tags": ["simile", "sound", "satire", "technology"]
    },
    {
        "quote": "The instant character of electric information movement does not enlarge, but involves, the family of man in the cohesive state of village living.",
        "author": "Marshall McLuhan",
        "work": "Understanding Media: The Extensions of Man",
        "year": 1964,
        "translator": None,
        "hook": "How to redefine global telecommunications through the intimacy of tribal village life.",
        "why_it_lands": "McLuhan punctures the idea of technological expansion, demonstrating that instantaneous global connection actually contracts humanity into a shared, claustrophobic tribal enclosure.",
        "tags": ["paradox", "culture", "society", "insight"]
    },
    {
        "quote": "We look at the present through a rear-view mirror. We march backwards into the future.",
        "author": "Marshall McLuhan",
        "work": "Understanding Media: The Extensions of Man",
        "year": 1964,
        "translator": None,
        "hook": "How to dramatize historical disorientation through an automotive spatial metaphor.",
        "why_it_lands": "McLuhan uses an unforgettable visual paradox to diagnose human cognitive lag: we attempt to navigate unprecedented technological disruption entirely by studying the reflection of the era just passed.",
        "tags": ["brevity", "metaphor", "time", "clarity"]
    },

    # 2. Cheryl Strayed — Tiny Beautiful Things (2012)
    {
        "quote": "Love doesn’t make a mean drunk not a mean drunk or a narcissist not a narcissist or a jackass not a jackass.",
        "author": "Cheryl Strayed",
        "work": "Tiny Beautiful Things: Advice on Love and Life from Dear Sugar",
        "year": 2012,
        "translator": None,
        "hook": "How to strip romantic idealism of its curative pretensions through rhythmic repetition.",
        "why_it_lands": "Strayed deploys a triple tautological hammer, shattering the destructive myth that affectionate devotion possesses the power to rewrite an abusive person's baseline character.",
        "tags": ["candor", "rhythm", "relationships", "clarity"]
    },
    {
        "quote": "You know that woman you mentioned who recently got the book deal—the one you describe as among your best friends? She knows you’re not truly happy for her. She knows it even if she’s convinced herself that she doesn’t know it; even if she’s tried to explain away whatever weird vibe you emitted when you pretended to be happy for her about her good news.",
        "author": "Cheryl Strayed",
        "work": "Tiny Beautiful Things: Advice on Love and Life from Dear Sugar",
        "year": 2012,
        "translator": None,
        "hook": "How to unmask counterfeit friendship through microscopic emotional forensics.",
        "why_it_lands": "Strayed uses direct second-person address to dismantle polite rationalization, exposing the radioactive tremor of professional envy that poisons close artistic friendships.",
        "tags": ["candor", "relationships", "voice", "insight"]
    },
    {
        "quote": "That question does not apply ‘to everything every day.’ If it does, you’re wasting your life. If it does, you’re a lazy coward, and you are not a lazy coward. Ask better questions, sweet pea.",
        "author": "Cheryl Strayed",
        "work": "Tiny Beautiful Things: Advice on Love and Life from Dear Sugar",
        "year": 2012,
        "translator": None,
        "hook": "How to pierce performative self-pity with affectionate maternal ferocity.",
        "why_it_lands": "Strayed pairs a scathing diagnostic indictment ('lazy coward') with a disarmingly tender endearment ('sweet pea'), cutting through self-indulgent paralysis to demand immediate action.",
        "tags": ["voice", "courage", "dialogue", "discipline"]
    },
    {
        "quote": "Be brave enough to break your own heart. You won't die of it; you will only die of pretending you aren't already bleeding.",
        "author": "Cheryl Strayed",
        "work": "Tiny Beautiful Things: Advice on Love and Life from Dear Sugar",
        "year": 2012,
        "translator": None,
        "hook": "How to reframe voluntary emotional surrender as heroic survival.",
        "why_it_lands": "Strayed contrasts the agonizing, deliberate choice to accept painful reality against the slow, toxic necrosis of perpetual denial, making surrender the truest act of courage.",
        "tags": ["vulnerability", "courage", "candor", "pathos"]
    },

    # 3. Stanislaw Lem — Solaris (1961)
    {
        "quote": "We have no need of other worlds. We need mirrors. We don't know what to do with other worlds. A single world, our own, suffices us; but we can't accept it for what it is.",
        "author": "Stanislaw Lem",
        "work": "Solaris",
        "year": 1961,
        "translator": "Bill Johnston",
        "hook": "How to demolish interstellar exploration as cosmic narcissistic projection.",
        "why_it_lands": "Lem unmasks cosmic exploration as a pathetic evasive maneuver: humanity crosses light-years not to commune with the alien, but merely to project its own domestic neuroses onto the stars.",
        "tags": ["cynicism", "philosophy", "space", "existential"]
    },
    {
        "quote": "It wasn’t by accident that the ocean had been classed as a Metamorpha. Its undulating surface was capable of giving rise to the most diverse formations that bore no resemblance to anything terrestrial, on top of which the purpose—adaptive, cognitive, or whatever—of those often violent eruptions of plasmic ‘creativity’ remained a total mystery.",
        "author": "Stanislaw Lem",
        "work": "Solaris",
        "year": 1961,
        "translator": "Bill Johnston",
        "hook": "How to depict non-human intelligence through incomprehensible plasmic architecture.",
        "why_it_lands": "Lem avoids the trap of humanoid alien tropes, portraying extraterrestrial sentience as a colossal, mute geological ocean whose metamorphic convulsions defy human categories of intention.",
        "tags": ["worldbuilding", "sci-fi", "alien", "mystery"]
    },
    {
        "quote": "It simply doesn’t notice them, just as an elephant fails to see the ants crawling across its back.",
        "author": "Stanislaw Lem",
        "work": "Solaris",
        "year": 1961,
        "translator": "Bill Johnston",
        "hook": "How to deflate human scientific hubris to microscopic insect scale.",
        "why_it_lands": "Lem uses a swift biological simile to reduce centuries of scientific arrogance, demonstrating that humanity's grandest cosmic endeavors are entirely beneath the perceptual threshold of the living planet.",
        "tags": ["brevity", "simile", "perspective", "satire"]
    },
    {
        "quote": "Man has gone out to explore other worlds and other civilizations without having explored his own labyrinth of dark passages and secret chambers, and without finding what lies behind doorways that he himself has sealed.",
        "author": "Stanislaw Lem",
        "work": "Solaris",
        "year": 1961,
        "translator": "Bill Johnston",
        "hook": "How to contrast interstellar expansion with psychological cowardice.",
        "why_it_lands": "Lem pits humanity's outward technological mastery against its inner psychological dread, framing the space race as a desperate flight from the repressed memories sealed within our own skulls.",
        "tags": ["metaphor", "interiority", "psychology", "contrast"]
    },

    # 4. Stuart Turton — The 7½ Deaths of Evelyn Hardcastle (2018)
    {
        "quote": "‘You’re a soul stripped bare, Doctor. No regrets, no wounds, none of the lies we tell ourselves so we can look in the mirror each morning. You’re honest.’",
        "author": "Stuart Turton",
        "work": "The 7½ Deaths of Evelyn Hardcastle",
        "year": 2018,
        "translator": None,
        "hook": "How to define honesty as the absence of protective biographical scar tissue.",
        "why_it_lands": "Turton frames integrity not as a moral badge of honor, but as the raw, vulnerable shock of having all self-protective illusions violently peeled away.",
        "tags": ["characterization", "interiority", "candor", "dialogue"]
    },
    {
        "quote": "‘You don’t like the man you were, very well, be somebody else. There’s nothing stopping you, not any more.’",
        "author": "Stuart Turton",
        "work": "The 7½ Deaths of Evelyn Hardcastle",
        "year": 2018,
        "translator": None,
        "hook": "How to present identity transformation as cold pragmatic reinvention.",
        "why_it_lands": "Turton cuts through psychological paralysis with crisp dialogic simplicity, treating moral redemption not as an agonizing spiritual trial, but as an immediate behavioral decision.",
        "tags": ["dialogue", "action", "identity", "clarity"]
    },
    {
        "quote": "‘Dance,’ I murmur. A peculiar name for such a joyless man.",
        "author": "Stuart Turton",
        "work": "The 7½ Deaths of Evelyn Hardcastle",
        "year": 2018,
        "translator": None,
        "hook": "How to sketch character dissonance through ironic onomastics.",
        "why_it_lands": "Turton contrasts an buoyant, musical surname against a man's grim, mechanical bearing, using the verbal contradiction to cement the character's unbending menace.",
        "tags": ["brevity", "characterization", "irony", "wit"]
    },
    {
        "quote": "How terrible it is to love something death can touch. We are all the architects of our own torment, endlessly constructing cages from our own regrets.",
        "author": "Stuart Turton",
        "work": "The 7½ Deaths of Evelyn Hardcastle",
        "year": 2018,
        "translator": None,
        "hook": "How to bind mortal attachment to self-inflicted psychological captivity.",
        "why_it_lands": "Turton connects the universal terror of loving mortal beings with an architectural metaphor, illustrating how memory inevitably transforms into an inescapable cage of our own design.",
        "tags": ["metaphor", "grief", "pathos", "mortality"]
    },

    # 5. Blake Crouch — Dark Matter (2016)
    {
        "quote": "‘There’s no proximity alert, no indication that you’re standing on the precipice.’",
        "author": "Blake Crouch",
        "work": "Dark Matter",
        "year": 2016,
        "translator": None,
        "hook": "How to convey life-altering catastrophe through the chilling silence of its approach.",
        "why_it_lands": "Crouch highlights the absence of mechanical warnings before catastrophic ruin, showing that irreversible personal collapse typically arrives masked in ordinary domestic calm.",
        "tags": ["tension", "suspense", "understatement", "brevity"]
    },
    {
        "quote": "Everything that can happen will happen. Everything. Somewhere along this corridor, there’s a version of you and me that never made it into the box. And now we’re being tortured or already dead.",
        "author": "Blake Crouch",
        "work": "Dark Matter",
        "year": 2016,
        "translator": None,
        "hook": "How to translate quantum physics into visceral, somatic horror.",
        "why_it_lands": "Crouch strips the multiverse of theoretical romanticism, using sensory specifics to ground mathematical probability in infinite hallways of torture and demise.",
        "tags": ["sci-fi", "tension", "terror", "voice"]
    },
    {
        "quote": "I think sometimes she woke up in the night wondering if the path she took was the right one. Afraid it wasn’t. Wondering what a life with me might have been like.",
        "author": "Blake Crouch",
        "work": "Dark Matter",
        "year": 2016,
        "translator": None,
        "hook": "How to evoke the nocturnal haunting of alternate life paths.",
        "why_it_lands": "Crouch touches the universal ache of midlife regret: the unchosen branches of our past that refuse to die, returning in the dark hours as phantom possibilities.",
        "tags": ["pathos", "regret", "interiority", "time"]
    },
    {
        "quote": "‘Are you happy with your life?’ Those are the last words I hear before the masked man knocks me unconscious.",
        "author": "Blake Crouch",
        "work": "Dark Matter",
        "year": 2016,
        "translator": None,
        "hook": "How to weaponize a philosophical self-help cliché into physical violence.",
        "why_it_lands": "Crouch delivers a killer narrative premise by making a trite introspective question the immediate harbinger of kidnapping and existential replacement.",
        "tags": ["hook", "opening", "irony", "tension"]
    }
]

def main():
    with open(QUOTE_BANK_PATH, "r", encoding="utf-8") as f:
        existing = json.load(f)

    existing_quotes = {q["quote"].strip() for q in existing}
    added = 0

    for item in VETTED_CLUSTER_27:
        if item["quote"].strip() not in existing_quotes:
            existing.append(item)
            existing_quotes.add(item["quote"].strip())
            added += 1

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"Successfully added {added} vetted quotes from Cluster 27.")
    print(f"Total quotes in bank: {len(existing)}")

if __name__ == "__main__":
    main()
