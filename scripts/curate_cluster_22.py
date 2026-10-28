# scripts/curate_cluster_22.py — Curates 20 craft quotes from Cluster 22 (Epistolary Intimacy, Dread & Confession)
# Usage: python3 scripts/curate_cluster_22.py
# Requires: json, os

import json
import os

QUOTE_BANK_PATH = "content/quote-bank.json"

VETTED_CLUSTER_22 = [
    # 1. Franz Kafka — Letters to Milena (1952)
    {
        "quote": "The animal wrests the whip from the master and flails itself in order to become the master, unaware that this is only a fantasy created by a new knot in the master’s thong.",
        "author": "Franz Kafka",
        "work": "Letters to Milena",
        "year": 1952,
        "translator": "Philip Boehm",
        "hook": "How to map the illusion of self-liberation through a masochistic parable.",
        "why_it_lands": "Kafka exposes the trap of internalized oppression: when the subjugated ego seizes the whip to punish itself, it merely ties another knot in the master's apparatus while mistaking self-torment for autonomy.",
        "tags": ["parable", "psychology", "paradox", "power"]
    },
    {
        "quote": "And actually it’s not at all you I love, but rather the existence you have bestowed on me.",
        "author": "Franz Kafka",
        "work": "Letters to Milena",
        "year": 1952,
        "translator": "Philip Boehm",
        "hook": "How to dissect erotic devotion down to existential self-interest.",
        "why_it_lands": "Kafka strips romantic adoration of sentimental pretense, confessing that intense passion is often a desperate hunger for the borrowed vitality and validation that the other person's gaze bestows.",
        "tags": ["candor", "confession", "epistolary", "introspection"]
    },
    {
        "quote": "Just as there is no place in the deep sea which isn’t under the greatest pressure, so it is with you—but all other life is a disgrace and makes me sick.",
        "author": "Franz Kafka",
        "work": "Letters to Milena",
        "year": 1952,
        "translator": "Philip Boehm",
        "hook": "How to depict intimacy as oceanic, crushing barometric pressure.",
        "why_it_lands": "Kafka equates emotional devotion not to light or warmth, but to deep-sea atmospheric weight—a crushing, breathless intensity that renders ordinary human existence intolerable.",
        "tags": ["metaphor", "claustrophobia", "intensity", "epistolary"]
    },
    {
        "quote": "It’s not your illness which scares me, but the thought of what must have preceded this disturbance.",
        "author": "Franz Kafka",
        "work": "Letters to Milena",
        "year": 1952,
        "translator": "Philip Boehm",
        "hook": "How to locate horror not in the symptom, but in its hidden psychological prehistory.",
        "why_it_lands": "Kafka redirects concern from physical pathology to subterranean psychic stress, showing that the visible crisis is merely the final tremor of an unbearable, invisible collapse.",
        "tags": ["dread", "psychology", "forensic", "subtlety"]
    },

    # 2. Virginia Woolf & Vita Sackville-West — Love Letters: Vita and Virginia (2021)
    {
        "quote": "Observe perpetually. Observe the oncome of age. Observe greed. Observe my own despondency.",
        "author": "Virginia Woolf & Vita Sackville-West",
        "work": "Love Letters: Vita and Virginia",
        "year": 2021,
        "translator": None,
        "hook": "How to weaponize observational discipline against personal despair.",
        "why_it_lands": "Woolf uses repetitive imperative verbs ('Observe... Observe... Observe...') to transform aging, avarice, and mental depression from paralyzing afflictions into raw aesthetic specimens for authorial inspection.",
        "tags": ["imperative", "anaphora", "observation", "discipline"]
    },
    {
        "quote": "One has a sense of links fished up into the light which are usually submerged.",
        "author": "Virginia Woolf & Vita Sackville-West",
        "work": "Love Letters: Vita and Virginia",
        "year": 2021,
        "translator": None,
        "hook": "How to describe the retrieval of unconscious connection through an aquatic metaphor.",
        "why_it_lands": "Woolf captures the sudden surfacing of deep emotional affinity, comparing unspoken shared history to heavy marine cables hauled from the ocean floor into sunlight.",
        "tags": ["metaphor", "aquatic", "memory", "subconscious"]
    },
    {
        "quote": "You will be seeing those lavender and tawny slopes, I suppose: and all the wild spring flowers which I have never seen. How I envy you. How I envy the people who are with you.",
        "author": "Virginia Woolf & Vita Sackville-West",
        "work": "Love Letters: Vita and Virginia",
        "year": 2021,
        "translator": None,
        "hook": "How to channel acute romantic jealousy through pastoral landscape.",
        "why_it_lands": "Vita balances painterly landscape colors ('lavender and tawny slopes') against sharp personal longing, escalating from envying foreign terrain to envying the breathing strangers in Woolf's presence.",
        "tags": ["epistolary", "longing", "color", "repetition"]
    },
    {
        "quote": "‘It’s bloody,’ I can’t tell you how I hate leaving you.",
        "author": "Virginia Woolf & Vita Sackville-West",
        "work": "Love Letters: Vita and Virginia",
        "year": 2021,
        "translator": None,
        "hook": "How to puncture high literary decorum with a sudden colloquial curse.",
        "why_it_lands": "Vita breaks through aristocratic restraint with a raw vulgarity ('bloody'), abandoning polished phrasing to register the jagged ache of physical parting.",
        "tags": ["colloquial", "dialogue", "candor", "parting"]
    },

    # 3. Leo Tolstoy — The Death of Ivan Ilyich (1886)
    {
        "quote": "‘It is he who is dead and not I.’",
        "author": "Leo Tolstoy",
        "work": "The Death of Ivan Ilyich",
        "year": 1886,
        "translator": "Louise & Aylmer Maude",
        "hook": "How to capture the shameful relief of surviving another man's death.",
        "why_it_lands": "Tolstoy isolates the secret, shameful reflex of every mourner at a funeral: the involuntary rush of self-satisfaction that death has taken someone else and passed oneself by.",
        "tags": ["candor", "interiority", "brevity", "mortality"]
    },
    {
        "quote": "It was then that it became evident on the one hand that his salary was insufficient for them to live on, and on the other that he had been forgotten, and not only this, but that what was for him the greatest and most cruel injustice appeared to others a quite ordinary occurrence.",
        "author": "Leo Tolstoy",
        "work": "The Death of Ivan Ilyich",
        "year": 1886,
        "translator": "Louise & Aylmer Maude",
        "hook": "How to dramatize administrative oblivion through bureaucratic indifference.",
        "why_it_lands": "Tolstoy captures the bureaucratic nightmare: realizing that the catastrophe destroying your life is viewed by your colleagues and superiors as an unremarkable, routine administrative reshuffle.",
        "tags": ["irony", "bureaucracy", "alienation", "perspective"]
    },
    {
        "quote": "Everything she did for him was entirely for her own sake, and she told him she was doing for herself what she actually was doing for herself, as if that was so incredible that he must understand the opposite.",
        "author": "Leo Tolstoy",
        "work": "The Death of Ivan Ilyich",
        "year": 1886,
        "translator": "Louise & Aylmer Maude",
        "hook": "How to dissect performative martyrdom in an inverted domestic circle.",
        "why_it_lands": "Tolstoy unmasks the psychological cruelty of bourgeois marriage, showing how selfish motives are wrapped in transparent piety to force the dying invalid into apologizing for his own decay.",
        "tags": ["satire", "marriage", "psychology", "cruelty"]
    },
    {
        "quote": "Matrimony—at any rate with Praskovya Fedorovna—was not always conducive to the pleasures and amenities of life, but on contrary often infringed both comfort and propriety, and that he must therefore entrench himself against such infringement.",
        "author": "Leo Tolstoy",
        "work": "The Death of Ivan Ilyich",
        "year": 1886,
        "translator": "Louise & Aylmer Maude",
        "hook": "How to render marital estrangement as formal military entrenchment.",
        "why_it_lands": "Tolstoy reduces married life to siege warfare, showing how polite social conventions become sandbags and barricades constructed to defend personal convenience.",
        "tags": ["metaphor", "irony", "marriage", "propriety"]
    },

    # 4. George Orwell — 1984 (1949)
    {
        "quote": "To tell deliberate lies while genuinely believing in them, to forget any fact that has become inconvenient, and then, when it becomes necessary again, to draw it back from oblivion for just so long as it is needed, to deny the existence of objective reality and all the while to take account of the reality which one denies—all this is indispensably necessary.",
        "author": "George Orwell",
        "work": "1984",
        "year": 1949,
        "translator": None,
        "hook": "How to define doublethink through recursive periodic syntax.",
        "why_it_lands": "Orwell stacks infinitives ('To tell... to forget... to deny... to take account') in a tightening psychological loop, mimicking the mental acrobatics required to erase objective reality in real time.",
        "tags": ["syntax", "periodic-sentence", "propaganda", "psychology"]
    },
    {
        "quote": "With its grace and carelessness it seemed to annihilate a whole culture, a whole system of thought, as though Big Brother and the Party and the Thought Police could all be swept into nothingness by a single splendid movement of the arm.",
        "author": "George Orwell",
        "work": "1984",
        "year": 1949,
        "translator": None,
        "hook": "How to obliterate a totalitarian apparatus with an involuntary physical gesture.",
        "why_it_lands": "Orwell pits the immense tyranny of the surveillance state against a girl's spontaneous bodily grace, demonstrating how natural human movement instantly exposes authoritarian power as clumsy and hollow.",
        "tags": ["contrast", "sensory", "gesture", "defiance"]
    },
    {
        "quote": "To die hating them, that was freedom.",
        "author": "George Orwell",
        "work": "1984",
        "year": 1949,
        "translator": None,
        "hook": "How to locate the last refuge of sovereignty in private hatred.",
        "why_it_lands": "Winston reduces political freedom to its barest biological outpost: not public victory or physical escape, but keeping one's hatred inviolate inside the skull before execution.",
        "tags": ["brevity", "aphorism", "defiance", "liberty"]
    },
    {
        "quote": "WAR IS PEACE / FREEDOM IS SLAVERY / IGNORANCE IS STRENGTH.",
        "author": "George Orwell",
        "work": "1984",
        "year": 1949,
        "translator": None,
        "hook": "How to forge totalitarian doctrine from three monosyllabic contradictions.",
        "why_it_lands": "Orwell demonstrates the brutal acoustic efficiency of state sloganeering, balancing diametric opposites on equal terms until semantic meaning disintegrates.",
        "tags": ["motto", "antithesis", "propaganda", "rhythm"]
    },

    # 5. Woody Allen — Apropos of Nothing (2020)
    {
        "quote": "They were both geniuses in their chosen fields. Beethoven became deaf, the only thing a composer would dread, and Gordy, a cinematographer, started losing his eyesight. Nice deal, human existence.",
        "author": "Woody Allen",
        "work": "Apropos of Nothing",
        "year": 2020,
        "translator": None,
        "hook": "How to summarize cosmic malice in a deadpan four-word epitaph.",
        "why_it_lands": "Allen pairs two specific, cruel physiological ironies before concluding with sarcastic fatalism ('Nice deal, human existence'), capturing the grim comedy of biological design.",
        "tags": ["deadpan", "irony", "satire", "mortality"]
    },
    {
        "quote": "I was being a good sport and wanted to appear impressive but once out to sea, just when I was chug-a-lugging a beer and intoning a chorus of ‘Heave ho, blow the man down,’ I turned chartreuse and dropped to the deck, groaning and begging to be euthanized.",
        "author": "Woody Allen",
        "work": "Apropos of Nothing",
        "year": 2020,
        "translator": None,
        "hook": "How to puncture masculine bravado through escalating physical humiliation.",
        "why_it_lands": "Allen orchestrates a comedic trajectory from self-conscious swagger to green-faced seasickness in a single sentence, capping it with the melodramatic plea to be euthanized.",
        "tags": ["humor", "sensory", "self-deprecation", "cadence"]
    },
    {
        "quote": "So it is that my life is ruined, spoiled, by the knowledge that the alarm will be going off one day and I must go, and this knowledge kills my peace of mind and makes me toss and turn through all the days of my existence waiting for the hour to strike.",
        "author": "Woody Allen",
        "work": "Apropos of Nothing",
        "year": 2020,
        "translator": None,
        "hook": "How to depict existential dread as an inescapable morning alarm.",
        "why_it_lands": "Allen domesticates cosmic mortality down to the mundane horror of a ringing alarm clock, showing how obsessive foresight poisons the present hours with anticipation of the inevitable.",
        "tags": ["metaphor", "anxiety", "mortality", "voice"]
    },
    {
        "quote": "But I wasn’t any simpleton. I was a simpleton extraordinaire, in love with the apotheosis of my dreams and wading through the debris.",
        "author": "Woody Allen",
        "work": "Apropos of Nothing",
        "year": 2020,
        "translator": None,
        "hook": "How to elevate romantic delusion to grandiose mock-heroic stature.",
        "why_it_lands": "Allen pairs self-mockery ('simpleton extraordinaire') with elevated diction ('apotheosis') and grim physical comedy ('wading through the debris'), capturing youthful infatuation with clear-eyed irony.",
        "tags": ["irony", "self-deprecation", "voice", "diction"]
    }
]

def main():
    with open(QUOTE_BANK_PATH, "r", encoding="utf-8") as f:
        quote_bank = json.load(f)

    print(f"Existing quote bank count: {len(quote_bank)}")

    # Check for duplicates by quote prefix
    existing_quotes = {q["quote"].strip()[:50].lower() for q in quote_bank}
    
    added_count = 0
    for entry in VETTED_CLUSTER_22:
        key = entry["quote"].strip()[:50].lower()
        if key in existing_quotes:
            print(f"Skipping duplicate: {entry['work']} - {entry['quote'][:40]}...")
            continue
        quote_bank.append(entry)
        existing_quotes.add(key)
        added_count += 1

    print(f"Added {added_count} new vetted quotes from Cluster 22.")
    print(f"New quote bank total: {len(quote_bank)}")

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(quote_bank, f, indent=2, ensure_ascii=False)
        f.write("\n")

if __name__ == "__main__":
    main()
