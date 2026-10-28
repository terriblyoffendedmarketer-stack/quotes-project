# scripts/curate_cluster_21.py — Curates 20 craft quotes from Cluster 21 (Twentieth-Century Titans & Uncompromising Visions)
# Usage: python3 scripts/curate_cluster_21.py
# Requires: json, os

import json
import os

QUOTE_BANK_PATH = "content/quote-bank.json"

VETTED_CLUSTER_21 = [
    # 1. John Steinbeck — East of Eden (1952)
    {
        "quote": "He was regarded as thick-skinned and insensitive—even cruel. But this was only his skin. Underneath he was more vulnerable than most.",
        "author": "John Steinbeck",
        "work": "East of Eden",
        "year": 1952,
        "translator": None,
        "hook": "How to invert an exterior character appraisal through somatic antithesis.",
        "why_it_lands": "Steinbeck dismantles community gossip by distinguishing protective dermal armor from internal vulnerability, reminding the reader that apparent callousness is often a shield against excessive sensitivity.",
        "tags": ["characterization", "interiority", "contrast", "vulnerability"]
    },
    {
        "quote": "‘You take most kids,’ he said, ‘if they know the answer, why, they’re tickled to death to tell it. But Cal doesn’t say anything until you make him.’",
        "author": "John Steinbeck",
        "work": "East of Eden",
        "year": 1952,
        "translator": None,
        "hook": "How to reveal character reserve through childhood contrast.",
        "why_it_lands": "The contrast between ordinary juvenile eagerness and Cal's guarded silence marks his isolation without clinical jargon.",
        "tags": ["dialogue", "contrast", "characterization", "voice"]
    },
    {
        "quote": "He fought the quiet hateful brain down and it slipped aside and went about its work.",
        "author": "John Steinbeck",
        "work": "East of Eden",
        "year": 1952,
        "translator": None,
        "hook": "How to personify self-destructive impulse as an autonomous domestic operative.",
        "why_it_lands": "Steinbeck splits Cal from his own malice, depicting the brain not as an abstract faculty, but as an unruly, quietly hateful roommate that eludes suppression and continues its sabotage.",
        "tags": ["psychology", "verbs", "characterization", "interiority"]
    },
    {
        "quote": "My father always told it at the last: No child ever had such care as I. The whole camp became my mother.",
        "author": "John Steinbeck",
        "work": "East of Eden",
        "year": 1952,
        "translator": None,
        "hook": "How to invert collective desolation into maternal sanctuary.",
        "why_it_lands": "The speaker reframes an army encampment into an improvised cradle, replacing individual maternal absence with the gruff, collective vigilance of soldiers.",
        "tags": ["pathos", "voice", "memory", "paradox"]
    },

    # 2. Mikhail Bulgakov — The Master and Margarita (1967)
    {
        "quote": "Gods, my gods! How sad the evening earth! How mysterious the mists over the bogs! He who has wandered in these mists, he who has suffered much before death, he who has flown over this earth bearing a burden beyond his strength knows it.",
        "author": "Mikhail Bulgakov",
        "work": "The Master and Margarita",
        "year": 1967,
        "translator": "Richard Pevear & Larissa Volokhonsky",
        "hook": "How to open a narrative departure with sweeping liturgical sorrow.",
        "why_it_lands": "Bulgakov shifts from biting Moscow satire to mythic lamentation, addressing the ancient gods with lyrical gravity as twilight settles across human futility.",
        "tags": ["lyricism", "lament", "atmosphere", "voice"]
    },
    {
        "quote": "‘Excuse me, but I don’t believe you,’ Woland replied. ‘That cannot be: manuscripts don’t burn.’",
        "author": "Mikhail Bulgakov",
        "work": "The Master and Margarita",
        "year": 1967,
        "translator": "Richard Pevear & Larissa Volokhonsky",
        "hook": "How to deliver an indestructible artistic creed in three words.",
        "why_it_lands": "Woland's calm refutation to the Master elevates literary creation above state censorship and physical destruction, turning creative integrity into an immortal law of nature.",
        "tags": ["aphorism", "theme", "defiance", "immortality"]
    },
    {
        "quote": "And at night, by moonlight, I have no peace... Why am I being tormented? Surely I did everything to save him?",
        "author": "Mikhail Bulgakov",
        "work": "The Master and Margarita",
        "year": 1967,
        "translator": "Richard Pevear & Larissa Volokhonsky",
        "hook": "How to render bureaucratic guilt as lunar insomnia.",
        "why_it_lands": "Bulgakov strips the Roman procurator of imperial dignity, leaving him wandering in perpetual moonlight, unable to quiet the ghost of his moral failure.",
        "tags": ["guilt", "interiority", "theme", "history"]
    },
    {
        "quote": "‘Oh, for pity’s sake,’ replied Azazello, ‘is it you I hear talking? Your friend calls you a master, you can think, so how can you be dead?’",
        "author": "Mikhail Bulgakov",
        "work": "The Master and Margarita",
        "year": 1967,
        "translator": "Richard Pevear & Larissa Volokhonsky",
        "hook": "How to dismantle defeatism with sharp demonic pragmatism.",
        "why_it_lands": "Azazello rebukes authorial despair by reducing death to an impossibility for anyone whose intellect and imaginative craft remain intact.",
        "tags": ["dialogue", "satire", "irony", "defiance"]
    },

    # 3. Ursula K. Le Guin — The Left Hand of Darkness (1969)
    {
        "quote": "It’s words that make the trouble and confusion.",
        "author": "Ursula K. Le Guin",
        "work": "The Left Hand of Darkness",
        "year": 1969,
        "translator": None,
        "hook": "How to challenge semantic confidence with an alien aphorism.",
        "why_it_lands": "Le Guin isolates language not as a transparent bridge between minds, but as the very fog that creates diplomatic misunderstanding and interpersonal alienation.",
        "tags": ["aphorism", "language", "theme", "clarity"]
    },
    {
        "quote": "‘Praise then darkness and Creation unfinished,’ he said, and there was darkness.",
        "author": "Ursula K. Le Guin",
        "work": "The Left Hand of Darkness",
        "year": 1969,
        "translator": None,
        "hook": "How to sanctify incompletion through a liturgical inversion of Genesis.",
        "why_it_lands": "Le Guin inverts traditional Western creation myth, offering praise not for light and finished design, but for darkness, shadow, and ongoing cosmic flux.",
        "tags": ["inversion", "mythic", "shadow", "philosophy"]
    },
    {
        "quote": "‘Sometimes you must go against the wheel’s turn,’ he said. He was as steady as ever, but in his walk, his voice, his bearing, vigor had been replaced by patience, and certainty by stubborn resolve.",
        "author": "Ursula K. Le Guin",
        "work": "The Left Hand of Darkness",
        "year": 1969,
        "translator": None,
        "hook": "How to register character maturation through physical and tonal substitution.",
        "why_it_lands": "Le Guin measures internal fortitude through physical transformation—showing how experience replaces fiery confidence with quiet, unshakeable endurance.",
        "tags": ["characterization", "subtlety", "endurance", "rhythm"]
    },
    {
        "quote": "‘We none of us choose,’ he said.",
        "author": "Ursula K. Le Guin",
        "work": "The Left Hand of Darkness",
        "year": 1969,
        "translator": None,
        "hook": "How to distill existential determinism into six monosyllabic words.",
        "why_it_lands": "Estraven cuts through human vanity with quiet resignation, reminding the envoy that circumstance, climate, and biology constrain individual intention far more than pride admits.",
        "tags": ["brevity", "fatalism", "dialogue", "candor"]
    },

    # 4. William S. Burroughs — Junkie (1953)
    {
        "quote": "I was afraid some day the dream would still be there when I woke up.",
        "author": "William S. Burroughs",
        "work": "Junkie",
        "year": 1953,
        "translator": None,
        "hook": "How to articulate chronic paranoia in a plain declarative sentence.",
        "why_it_lands": "Burroughs captures the terrifying erosion of boundaries between delirium and daylight, fearing not the nightmare itself, but its refusal to dissolve upon waking.",
        "tags": ["paranoia", "interiority", "brevity", "understatement"]
    },
    {
        "quote": "‘No time for finesse,’ he remarked. The wallet was empty.",
        "author": "William S. Burroughs",
        "work": "Junkie",
        "year": 1953,
        "translator": None,
        "hook": "How to puncture criminal calculation with a deadpan anti-climax.",
        "why_it_lands": "Burroughs delivers the street-level hustle with dry forensic brevity—showing how criminal bravado collapses into petty failure in eight words.",
        "tags": ["dialogue", "deadpan", "understatement", "anti-climax"]
    },
    {
        "quote": "Well, I guess he’ll die soon.",
        "author": "William S. Burroughs",
        "work": "Junkie",
        "year": 1953,
        "translator": None,
        "hook": "How to register terminal decline with clinical, street-level detachment.",
        "why_it_lands": "Burroughs strips mortality of tragedy, rendering an acquaintance's imminent death with the flat, unfeeling shorthand of the narcotic economy.",
        "tags": ["candor", "fatalism", "brevity", "voice"]
    },
    {
        "quote": "Always build a John up. If he has any sort of body at all say, ‘Oh, don’t ever hurt me.’ A John is different from a sucker. When you’re with a sucker you’re on the alert all the time. You give him nothing. A sucker is just to be taken.",
        "author": "William S. Burroughs",
        "work": "Junkie",
        "year": 1953,
        "translator": None,
        "hook": "How to codify transactional psychology into field-guide rules.",
        "why_it_lands": "Burroughs outlines the taxonomy of the underworld with detached anthropological rigor, demonstrating how calculated flattery and manufactured vulnerability are weaponized.",
        "tags": ["taxonomy", "cynicism", "dialogue", "psychology"]
    },

    # 5. Charles Bukowski — Love Is a Dog from Hell (1977)
    {
        "quote": "we know God is dead, they’ve told us, but listening to you I wasn’t sure.",
        "author": "Charles Bukowski",
        "work": "Love Is a Dog from Hell",
        "year": 1977,
        "translator": None,
        "hook": "How to challenge philosophical dogma with an offhand personal aside.",
        "why_it_lands": "Bukowski punctures high Nietzschean theory with street-level observation, measuring grand metaphysical proclamations against the gritty reality of a single human voice.",
        "tags": ["candor", "voice", "satire", "philosophy"]
    },
    {
        "quote": "hey, my God, here’s a TWENTY! God, here’s a TWENTY I never knew I had! I’m RICH!",
        "author": "Charles Bukowski",
        "work": "Love Is a Dog from Hell",
        "year": 1977,
        "translator": None,
        "hook": "How to capture instant destitution relief through frantic repetition.",
        "why_it_lands": "Bukowski renders poverty's sudden windfall with raw, unvarnished ecstasy, showing how twenty crumpled dollars in an empty pocket feels like infinite wealth.",
        "tags": ["dialogue", "repetition", "poverty", "humor"]
    },
    {
        "quote": "he said, ‘I’m just going to read 3 more poems and then I’m going to step down and let Bukowski read.’",
        "author": "Charles Bukowski",
        "work": "Love Is a Dog from Hell",
        "year": 1977,
        "translator": None,
        "hook": "How to build anticipation by highlighting the dread of an impending performance.",
        "why_it_lands": "Bukowski captures the awkward comedy of poetry readings, where an earnest academic delays his own exit while the audience waits for the chaotic main event.",
        "tags": ["dialogue", "deadpan", "understatement", "metafiction"]
    },
    {
        "quote": "I use acrylics, paint right out of the tube. I do the left side of the painting first with my left hand and then finish the right side with my right hand.",
        "author": "Charles Bukowski",
        "work": "Love Is a Dog from Hell",
        "year": 1977,
        "translator": None,
        "hook": "How to demystify creative technique through deadpan manual procedure.",
        "why_it_lands": "Bukowski strips artistic process of spiritual pretension, describing painting as purely physical, ambidextrous labor squeezed straight from the tube.",
        "tags": ["process", "deadpan", "candor", "simplicity"]
    }
]

def main():
    with open(QUOTE_BANK_PATH, "r", encoding="utf-8") as f:
        quote_bank = json.load(f)

    print(f"Existing quote bank count: {len(quote_bank)}")

    # Check for duplicates by quote prefix
    existing_quotes = {q["quote"].strip()[:50].lower() for q in quote_bank}
    
    added_count = 0
    for entry in VETTED_CLUSTER_21:
        key = entry["quote"].strip()[:50].lower()
        if key in existing_quotes:
            print(f"Skipping duplicate: {entry['work']} - {entry['quote'][:40]}...")
            continue
        quote_bank.append(entry)
        existing_quotes.add(key)
        added_count += 1

    print(f"Added {added_count} new vetted quotes from Cluster 21.")
    print(f"New quote bank total: {len(quote_bank)}")

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(quote_bank, f, indent=2, ensure_ascii=False)
        f.write("\n")

if __name__ == "__main__":
    main()
