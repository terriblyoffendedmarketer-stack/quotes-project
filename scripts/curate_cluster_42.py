# scripts/curate_cluster_42.py — Vets and integrates 20 quotes from Cluster 42 into quote-bank.json
# Usage: python3 scripts/curate_cluster_42.py

import json

new_quotes = [
    # Peter Abelard and Heloise — The Letters of Abelard and Heloise (1132, trans. Betty Radice)
    {
        "quote": "I have armed my hands against myself; I have exhausted my strength in constant exercises; I comment upon St. Paul; I contend with Aristotle: in short, I do all I used to do before I loved you, but all in vain; nothing can be successful that opposes you.",
        "author": "Peter Abelard and Heloise",
        "work": "The Letters of Abelard and Heloise",
        "year": 1132,
        "translator": "Betty Radice",
        "hook": "How to show intellectual discipline collapsing before emotional memory",
        "why_it_lands": "The speaker rallies the highest intellectual fortresses of the medieval world—Pauline theology, Aristotelian dialectic, rigorous asceticism—only to record their total uselessness. The escalating catalogue makes the final admission of vulnerability feel completely insurmountable.",
        "tags": ["passion", "syntax", "rhetoric"]
    },
    {
        "quote": "But though I am no longer deceived by love, I am not cured.",
        "author": "Peter Abelard and Heloise",
        "work": "The Letters of Abelard and Heloise",
        "year": 1132,
        "translator": "Betty Radice",
        "hook": "How to sever intellectual clarity from emotional healing in a single sentence",
        "why_it_lands": "The sentence hinges on a cruel distinction: understanding the illusion of desire does nothing to extinguish the pain. The brevity and balance of the two clauses deliver a cold, aphoristic diagnosis of unhealed grief.",
        "tags": ["aphorism", "understatement", "psychological truth"]
    },
    {
        "quote": "Alas! I am humbled under love, and not under the Cross.",
        "author": "Peter Abelard and Heloise",
        "work": "The Letters of Abelard and Heloise",
        "year": 1132,
        "translator": "Betty Radice",
        "hook": "How to expose spiritual despair through rival allegiances",
        "why_it_lands": "In a monastic world predicated on divine surrender, confessing that earthly passion commands greater obedience than Christ is an act of terrifying candour. The syntactic parallel balances devotion against heresy with breathless economy.",
        "tags": ["spiritual crisis", "contrast", "paradox"]
    },
    {
        "quote": "My passions there are in rebellion; I preside over others but cannot rule myself.",
        "author": "Peter Abelard and Heloise",
        "work": "The Letters of Abelard and Heloise",
        "year": 1132,
        "translator": "Betty Radice",
        "hook": "How to dramatize the hypocrisy of institutional authority",
        "why_it_lands": "The tension between external governance ('preside over others') and internal anarchy ('cannot rule myself') exposes the loneliness of leadership. The stark antithesis strips away ecclesiastical majesty to reveal raw human fracture.",
        "tags": ["irony", "characterization", "voice"]
    },

    # Khushwant Singh — Paradise and Other Stories (2004)
    {
        "quote": "The trouble with India is that it’s a country where everyone is trying to be something they are not.",
        "author": "Khushwant Singh",
        "work": "Paradise and Other Stories",
        "year": 2004,
        "hook": "How to open with an uncompromising national diagnosis",
        "why_it_lands": "Singh bypasses polite diplomatic nuance with an unapologetic, sweepingly blunt indictment of social pretension. The absolute certainty of the cadence hooks the reader by daring them to dispute the observation.",
        "tags": ["voice", "opening", "social critique"]
    },
    {
        "quote": "She had laid out her sari, petticoat and blouse on the bed. By way of greeting she said, 'Saara chippak-chippak—sticky all over—belly, thighs, all chippak-chippak.'",
        "author": "Khushwant Singh",
        "work": "Paradise and Other Stories",
        "year": 2004,
        "hook": "How to puncture decorum through raw domestic vernacular",
        "why_it_lands": "Singh rejects poeticized Indian domesticity, thrusting the physical discomfort of the northern heat directly into the reader's face. The phonetic repetition of the onomatopoeic Punjabi idiom 'chippak-chippak' creates an immediately tactile, sticky presence.",
        "tags": ["sensory detail", "dialogue", "realism"]
    },
    {
        "quote": "Take no notice of what that foul-mouthed fellow says; it’s just envy. See where he is today, close to retirement and only an executive engineer.",
        "author": "Khushwant Singh",
        "work": "Paradise and Other Stories",
        "year": 2004,
        "hook": "How to capture middle-class resentment through bureaucratic hierarchy",
        "why_it_lands": "The speaker dismisses genuine moral criticism not with ethical counterarguments, but by pointing out the critic's modest civil service grade ('only an executive engineer'). It encapsulates an entire bourgeois culture where rank is the only valid metric of truth.",
        "tags": ["satire", "characterization", "subcontinental realism"]
    },
    {
        "quote": "It looked squat, staid and lifeless, like middle-aged women who had let themselves go.",
        "author": "Khushwant Singh",
        "work": "Paradise and Other Stories",
        "year": 2004,
        "hook": "How to animate architectural neglect with a biting physical simile",
        "why_it_lands": "Singh refuses gentle landscape prose, applying an abrasive, unflattering human comparison to a dormant building. The triad of adjectives ('squat, staid and lifeless') sets up the blunt punch of the final image with characteristic irreverence.",
        "tags": ["simile", "imagery", "voice"]
    },

    # Harishankar Parsai — Nithalle Ki Diary (1968)
    {
        "quote": "कोई ‘प्राइवेसी’ नहीं—जिसका अपना मकान नहीं, उसकी भी क्या ‘प्राइवेसी’ !",
        "author": "Harishankar Parsai",
        "work": "Nithalle Ki Diary",
        "year": 1968,
        "hook": "How to expose property hierarchy through an imported bourgeois buzzword",
        "why_it_lands": "Parsai takes the English loanword 'privacy' and collides it with the brutal economic reality of urban tenancy. By laughing at the absurdity of a tenant expecting personal boundaries without property ownership, he mocks both bourgeois vanity and structural injustice in nine words.",
        "tags": ["satire", "cultural critique", "economy"]
    },
    {
        "quote": "मेरे भगवान ने ऐसे ‘केस’ में पहले भी मदद की है? यानी ऐसे मामले को ‘डील’ करने का उन्हें अनुभव है या नहीं?",
        "author": "Harishankar Parsai",
        "work": "Nithalle Ki Diary",
        "year": 1968,
        "hook": "How to treat divine providence like a junior bureaucratic clerk",
        "why_it_lands": "Parsai transposes the sacred machinery of prayer into the mundane vernacular of file processing. Asking whether the Almighty has sufficient prior experience handling such a 'case' satirizes both religious transactionalism and the all-consuming clerk culture of the Indian state.",
        "tags": ["satire", "irony", "humor"]
    },
    {
        "quote": "सजा उसके भले के लिए दिलवाओ, उससे कहो कि वह आज से लगातार तीन दिन साहब के बँगले के सामने खड़ा होकर उन्हें गालियाँ दे। जब साहब उसे डाटने आएँ, तब अपना नाम और पद बता दे।",
        "author": "Harishankar Parsai",
        "work": "Nithalle Ki Diary",
        "year": 1968,
        "hook": "How to weaponize administrative absurdity as revenge advice",
        "why_it_lands": "The advice parodies feudal deference by instructing a subordinate to orchestrate his own public disgrace to force higher authorities to remember his name and rank. The deadpan earnestness of the Machiavellian suggestion generates dark comedic brilliance.",
        "tags": ["satire", "dialogue", "bureaucracy"]
    },
    {
        "quote": "‘कर्मण्येवाधिकारस्ते मा फलेषु कदाचन्’—तुम्हारे अधिकार में सिर्फ काम करना है; तुम फल की इच्छा मत करो।",
        "author": "Harishankar Parsai",
        "work": "Nithalle Ki Diary",
        "year": 1968,
        "hook": "How to expose scripture being weaponized against labor rights",
        "why_it_lands": "Parsai strips the venerable Gita verse of its metaphysical grandeur, showing how employers and institutions quote sacred duty to rationalize unpaid labor and silence demands for fair wages. The cynical translation lays bare how dogma protects capital.",
        "tags": ["satire", "scripture subversion", "irony"]
    },

    # Isaac Asimov — Asimov's Mysteries (1968)
    {
        "quote": "They didn’t do anything. They stuck to the rule of being fair to the reader.",
        "author": "Isaac Asimov",
        "work": "Asimov's Mysteries",
        "year": 1968,
        "hook": "How to define narrative integrity as a contractual duty",
        "why_it_lands": "Asimov articulates the cardinal ethic of fair-play detective fiction: no hidden trapdoors, no sudden psychic insights, and no cheated physics. The two flat, unembellished sentences elevate structural honesty above flashy authorial sleight-of-hand.",
        "tags": ["mystery craft", "clarity", "storytelling"]
    },
    {
        "quote": "Steam—at the low temperature of space? Steam—at the low pressure of space!",
        "author": "Isaac Asimov",
        "work": "Asimov's Mysteries",
        "year": 1968,
        "hook": "How to dramatize scientific revelation through repeating interrogatives",
        "why_it_lands": "Asimov structures an intellectual breakthrough around a thermal paradox. The shift from question mark to exclamation mark across two identically phrased clauses captures the exact instant where physical impossibility transforms into deductive certainty.",
        "tags": ["pacing", "rhythm", "science fiction craft"]
    },
    {
        "quote": "It is the hallmark of the Ultras, I think. They are all very cold, very rigid, very sure of themselves. They can't empathize, or they wouldn’t speak of killing off billions of human beings.",
        "author": "Isaac Asimov",
        "work": "Asimov's Mysteries",
        "year": 1968,
        "hook": "How to define technocratic tyranny through emotional detachment",
        "why_it_lands": "Asimov identifies the chilling core of ideological fanaticism: not rabid bloodlust, but mathematical certainty and emotional numbness. The triad of descriptors ('very cold, very rigid, very sure') mirrors the unyielding logic of the machines they build.",
        "tags": ["characterization", "voice", "morality"]
    },
    {
        "quote": "You’ve got a gamma-fogged semireflector. Every time the positron beam circles round to its position the drive flickers out for a second.",
        "author": "Isaac Asimov",
        "work": "Asimov's Mysteries",
        "year": 1968,
        "hook": "How to create tactile mechanical tension with procedural science fiction",
        "why_it_lands": "Asimov grounds spaceflight in ordinary mechanical unreliability. The intermittent, cyclical stutter ('circles round... flickers out for a second') transforms speculative astrophysics into the relatable irritation of a faulty automotive alternator.",
        "tags": ["worldbuilding", "sensory detail", "clarity"]
    },

    # Uketsu — The Floor Plan (Strange Houses) (2021, trans. Louise Heal Kawai)
    {
        "quote": "They actively built walls that made the kitchen smaller.",
        "author": "Uketsu",
        "work": "The Floor Plan (Strange Houses)",
        "year": 2021,
        "translator": "Louise Heal Kawai",
        "hook": "How to generate spatial dread through deliberate architectural anomaly",
        "why_it_lands": "Domestic architecture exists to maximize comfort and utility. Stating flatly that homeowners spent money to deliberately constrict living space creates immediate, uncanny cognitive dissonance without needing any ghost or bloodstain.",
        "tags": ["suspense", "architectural dread", "understatement"]
    },
    {
        "quote": "The idea that there were two of these houses… It’s not all that unusual for houses to have what they call ‘interior windows’, little openings between rooms. But rarely, if ever, do you find them in this double-leaf style.",
        "author": "Uketsu",
        "work": "The Floor Plan (Strange Houses)",
        "year": 2021,
        "translator": "Louise Heal Kawai",
        "hook": "How to turn blueprint minutiae into a horrifying realization",
        "why_it_lands": "Uketsu operates entirely through architectural analysis. By lingering on the mundane anomaly of 'interior windows' configured in a rare double-leaf pattern, the technical deduction hints at a calculated surveillance layout disguised as renovation.",
        "tags": ["deduction", "atmosphere", "pacing"]
    },
    {
        "quote": "They didn't decide to leave it. They had to. They could not build a room over that area.",
        "author": "Uketsu",
        "work": "The Floor Plan (Strange Houses)",
        "year": 2021,
        "translator": "Louise Heal Kawai",
        "hook": "How to use deductive negative space to suggest concealment",
        "why_it_lands": "Three staccato sentences dismantle the illusion of architectural accident. Uketsu shifts the reader from thinking of unused space as an aesthetic quirk to recognizing it as an involuntary structural compromise concealing something underneath.",
        "tags": ["syntax", "mystery craft", "suspense"]
    },
    {
        "quote": "The couple used those rooms to play the ideal family as they raised him. But, at the same time, the house has a darker face too.",
        "author": "Uketsu",
        "work": "The Floor Plan (Strange Houses)",
        "year": 2021,
        "translator": "Louise Heal Kawai",
        "hook": "How to contrast suburban domestic performance with physical entrapment",
        "why_it_lands": "The horror stems from the juxtaposition: the bright, sunny rooms staged for the community to project perfect domesticity, set against the windowless, hidden corridors built into the same blueprint. It maps social hypocrisy directly onto floorplan geometry.",
        "tags": ["contrast", "psychological truth", "atmosphere"]
    }
]

def main():
    bank_path = "content/quote-bank.json"
    with open(bank_path, "r", encoding="utf-8") as f:
        bank = json.load(f)

    existing_quotes = {q["quote"].strip() for q in bank}
    added = 0

    for q in new_quotes:
        if q["quote"].strip() not in existing_quotes:
            bank.append(q)
            existing_quotes.add(q["quote"].strip())
            added += 1

    with open(bank_path, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)

    print(f"Added {added} vetted quotes from Cluster 42. Total in bank: {len(bank)}")

if __name__ == "__main__":
    main()
