# curate_cluster_40.py — Curates 20 vetted quotes from Cluster 40 into quote-bank.json
# Usage: python3 scripts/curate_cluster_40.py
#
# Books:
# - Coin Locker Babies by Ryu Murakami (1980, trans. Ralph McCarthy)
# - Scene: 75 by Rahi Masoom Raza (1977, trans. Poonam Saxena)
# - Vikalang Shraddha Ka Daur by Harishankar Parsai (1980)
# - The Complete Adventures of Feluda by Satyajit Ray (1988, trans. Gopa Majumdar)
# - Indica: A Deep Natural History of the Indian Subcontinent by Pranay Lal (2016)

import json
from pathlib import Path

QUOTE_BANK = Path("content/quote-bank.json")

NEW_QUOTES = [
    # --- Ryu Murakami: Coin Locker Babies (1980) ---
    {
        "quote": "It was the heat. No one could have gone on sleeping in a damp, double-sealed box like that.",
        "author": "Ryu Murakami",
        "work": "Coin Locker Babies",
        "year": 1980,
        "translator": "Ralph McCarthy",
        "hook": "How to open trauma with physical thermodynamics",
        "why_it_lands": "Murakami doesn't open with psychological sentiment or tragic violin chords. The abandoned infant's awakening is framed with flat, suffocating physics: heat and humidity inside a sheet-metal locker.",
        "tags": ["sensory-detail", "realism", "brevity"]
    },
    {
        "quote": "It’s not that we’re unhappy with each other, not at all; it’s just that it’s not all that easy being a grown-up, all alone in the world.",
        "author": "Ryu Murakami",
        "work": "Coin Locker Babies",
        "year": 1980,
        "translator": "Ralph McCarthy",
        "hook": "How to diagnose adult loneliness without melodrama",
        "why_it_lands": "The double negative ('not that we're unhappy... not at all') sets up a calm, domestic defensive perimeter, only to deliver the unvarnished verdict: surviving adulthood without a net is terrifying.",
        "tags": ["candor", "understatement", "psychology"]
    },
    {
        "quote": "It was then that Kiku realized for the first time that he was fumbling around with a corpse.",
        "author": "Ryu Murakami",
        "work": "Coin Locker Babies",
        "year": 1980,
        "translator": "Ralph McCarthy",
        "hook": "How to land horror in a single retrospective realization",
        "why_it_lands": "The physical verb 'fumbling around' brings tactile banality to what should be an operatic shock. The delayed cognitive registration mirrors real psychological shock, where the senses comprehend reality seconds before the mind catches up.",
        "tags": ["understatement", "shock", "precision"]
    },
    {
        "quote": "You’re the one out of line. If you want to act all proud and uppity, if you’re so keen on exercising your inalienable rights, go do it in a hotel lobby or your own marble palace.",
        "author": "Ryu Murakami",
        "work": "Coin Locker Babies",
        "year": 1980,
        "translator": "Ralph McCarthy",
        "hook": "How to skewer bourgeois entitlement with street geography",
        "why_it_lands": "Constitutional abstractions ('inalienable rights') are shoved into physical real estate. Murakami shows that high-minded principles require marble floors and luxury lobbies; in the alley, they are merely comical posture.",
        "tags": ["dialogue", "cynicism", "class-critique"]
    },

    # --- Rahi Masoom Raza: Scene: 75 (1977) ---
    {
        "quote": "It is said that after Lalaji died, swarming circles of ants waited for him on those paths for months… Lalaji made a lot of money in the Second World War. He got many army tenders. And from an ordinary man, he turned into a Big Man.",
        "author": "Rahi Masoom Raza",
        "work": "Scene: 75",
        "year": 1977,
        "translator": "Poonam Saxena",
        "hook": "How to weave commercial war profiteering into mythic grotesque",
        "why_it_lands": "Raza contrasts the pious daily habit of feeding flour to ants with the blood-soaked profiteering of military contracts. The persistent ants waiting for sugar after the funeral become an eerie Greek chorus mocking religious hypocrisy.",
        "tags": ["irony", "satire", "social-anatomy"]
    },
    {
        "quote": "My question is, why, in this country of the unemployed, in Bharat that is India, does any girl’s mother have the right to name her daughter Rosy?",
        "author": "Rahi Masoom Raza",
        "work": "Scene: 75",
        "year": 1977,
        "translator": "Poonam Saxena",
        "hook": "How to weaponize a child's name against postcolonial pretension",
        "why_it_lands": "The satirical collision of constitutional gravity ('Bharat that is India') with an imported colonial moniker ('Rosy'). Raza exposes how Western glamour is grafted onto subcontinental destitution like cheap paint on mud.",
        "tags": ["satire", "cultural-critique", "irony"]
    },
    {
        "quote": "VD was a strange fellow. He was always grave, as if the revolution would seek him out and land up at his very doorstep, as if in all of India no one else was waiting for a revolution except him.",
        "author": "Rahi Masoom Raza",
        "work": "Scene: 75",
        "year": 1977,
        "translator": "Poonam Saxena",
        "hook": "How to caricature revolutionary vanity with domestic solitude",
        "why_it_lands": "Raza skewers the self-important radical who imagines history has his private street address. The comedy comes from the disproportion between the solitary solemn man on his charpoy and the vast, indifferent continent outside his window.",
        "tags": ["character-sketch", "irony", "voice"]
    },
    {
        "quote": "Writing a story isn’t difficult. Just pick up a pen and start writing.",
        "author": "Rahi Masoom Raza",
        "work": "Scene: 75",
        "year": 1977,
        "translator": "Poonam Saxena",
        "hook": "How to mock artistic mysticism with disarming simplicity",
        "why_it_lands": "Spoken by a hack Bombay film producer, the line strips literary creation of all romantic agony. It is both a hilarious sendup of Bollywood commercial cynicism and a strangely liberating craft challenge.",
        "tags": ["craft", "deadpan", "satire"]
    },

    # --- Harishankar Parsai: Vikalang Shraddha Ka Daur (1980) ---
    {
        "quote": "मैंने कतई ऐसा कुछ नहीं किया, जिससे ईमानदार माना जाऊँ। न जाने उन्हें कैसे यह भ्रम हो गया कि मैं ईमानदार हूँ।",
        "author": "Harishankar Parsai",
        "work": "Vikalang Shraddha Ka Daur",
        "year": 1980,
        "hook": "How to weaponize voluntary confession to mock public naivety",
        "why_it_lands": "Parsai upends the politician's desperate protestations of virtue. By actively repudiating his own reputation for integrity, he reveals that society's demand for heroes is so pathetic that even a crook gets misidentified as a saint.",
        "tags": ["satire", "paradox", "irony"]
    },
    {
        "quote": "मैं जानता हूँ कि तुम एक अरसे से मेरी मृत्यु का शुभ समाचार सुनने को लालायित हो, पर फिलहाल मैं तुम्हें निराश कर रहा हूँ। इंतज़ार करो। किसी दिन सचमुच मरकर तुम पर मेहरबानी करूँगा।",
        "author": "Harishankar Parsai",
        "work": "Vikalang Shraddha Ka Daur",
        "year": 1980,
        "hook": "How to turn a death wish into polite social sabotage",
        "why_it_lands": "Parsai takes unspoken familial malice and replies with extravagant, mocking courtliness. Calling his own demise a 'kind favor' he is eager to bestow strips the polite veneer off inheritance greed.",
        "tags": ["dark-humor", "candor", "epistolary-craft"]
    },
    {
        "quote": "वे आचार्य चाहे साहित्य के हों, इतिहास के, अर्थशास्त्र के... जिन्दगी की किसी चीज की परिभाषा नहीं बदलने देने के लिए दिमाग-तोड़ मेहनत करते हैं, पुरस्कार प्राप्त करने का कष्ट उठाते हैं, सम्मान में माला पहनने का त्रास भोगते हैं।",
        "author": "Harishankar Parsai",
        "work": "Vikalang Shraddha Ka Daur",
        "year": 1980,
        "hook": "How to frame academic self-preservation as heroic martyrdom",
        "why_it_lands": "Parsai satirizes institutional conservatism by treating public accolades as painful martyrdom. The scholars don't protect truth; they work tirelessly to freeze language so their own irrelevant tenure remains secure.",
        "tags": ["satire", "intellectual-craft", "irony"]
    },
    {
        "quote": "प्यार? हाँ, हर बुर्जुआ क्रान्तिकारिता को मारने के लिए प्यार करता है। यह प्यार षड्यंत्र है।",
        "author": "Harishankar Parsai",
        "work": "Vikalang Shraddha Ka Daur",
        "year": 1980,
        "hook": "How to parody political dogmatism by criminalizing tenderness",
        "why_it_lands": "Parsai skewers ideological fanaticism by turning romantic affection into a counter-revolutionary conspiracy. It captures the exact rhetorical paranoia of cadres who can't tolerate human warmth without smelling class treason.",
        "tags": ["satire", "parody", "brevity"]
    },

    # --- Satyajit Ray: The Complete Adventures of Feluda (1988) ---
    {
        "quote": "If Feluda needs information about any past event, he goes to Uncle Sidhu instead of the National Library. His work gets done far more quickly, and with good cheer.",
        "author": "Satyajit Ray",
        "work": "The Complete Adventures of Feluda",
        "year": 1988,
        "translator": "Gopa Majumdar",
        "hook": "How to establish character efficiency through living archives",
        "why_it_lands": "Ray replaces dusty bureaucratic institutions with eccentric human eccentricity. Uncle Sidhu represents the classic Kolkata adda intellectual: a living library powered by sweet tea and conversational delight rather than Dewey Decimal numbers.",
        "tags": ["character-detail", "observation", "charm"]
    },
    {
        "quote": "You made one false move in Calcutta, Mr Batra. In trying to establish that there were two Batras, you bought a kukri at the gift shop in your hotel and gave them a fake note.",
        "author": "Satyajit Ray",
        "work": "The Complete Adventures of Feluda",
        "year": 1988,
        "translator": "Gopa Majumdar",
        "hook": "How to unmask criminal cunning through tourist trivia",
        "why_it_lands": "Ray's detective does not rely on forensic science, but on sharp observation of petty habits. The grand conspiracy unravels because the villain couldn't resist buying an overpriced souvenir in his own hotel lobby.",
        "tags": ["deduction", "irony", "precision"]
    },
    {
        "quote": "It may only be an accident of geography, but can you think of any other state that has lush green farmland, dry and arid areas, a forest like the Sunderbans, huge rivers like the Ganga, Padma and Meghna, an ocean at its bottom and the Himalayas at its top?",
        "author": "Satyajit Ray",
        "work": "The Complete Adventures of Feluda",
        "year": 1988,
        "translator": "Gopa Majumdar",
        "hook": "How to sketch regional magnificence through geographic contrast",
        "why_it_lands": "A masterclass in landscape portraiture. Feluda frames Bengal's natural boundaries not as political borders, but as an impossible climatic stack: mangrove swamps at the base and glacial peaks at the summit.",
        "tags": ["landscape", "scale", "lyricism"]
    },
    {
        "quote": "It is probably only my vanity that made me want to open the chest and look at the necklace. I had just watched my mother wear it on the screen and it looked lovely on her. So I thought I’d put it round my own neck and see how I looked.",
        "author": "Satyajit Ray",
        "work": "The Complete Adventures of Feluda",
        "year": 1988,
        "translator": "Gopa Majumdar",
        "hook": "How to trace a crime back to fragile domestic imitation",
        "why_it_lands": "Ray strips mystery of monstrous melodrama and locates the impulse in childish vanity. The desire to try on a dead mother's cinema jewels reveals how deeply grief and glamour intertwine in ordinary households.",
        "tags": ["psychology", "candor", "vulnerability"]
    },

    # --- Pranay Lal: Indica: A Deep Natural History of the Indian Subcontinent (2016) ---
    {
        "quote": "Each piece of rock, every pinch of soil and every little fossil tells a story, and because the earth is so old, there are an infinite number of stories to tell.",
        "author": "Pranay Lal",
        "work": "Indica: A Deep Natural History of the Indian Subcontinent",
        "year": 2016,
        "hook": "How to turn geological strata into endless narrative craft",
        "why_it_lands": "Lal unites geology and storytelling. Rock isn't passive mineral weight; it is compressed narrative waiting for a literate reader to decode billions of years of forgotten drama.",
        "tags": ["metaphor", "deep-time", "craft"]
    },
    {
        "quote": "Of all known liquids water is probably the most studied and least understood.",
        "author": "Pranay Lal",
        "work": "Indica: A Deep Natural History of the Indian Subcontinent",
        "year": 2016,
        "hook": "How to establish mystery in the most ubiquitous element",
        "why_it_lands": "A clean, arresting paradox. By placing intense scientific scrutiny alongside persistent enigma, Lal reminds us that familiarity is not the same as comprehension.",
        "tags": ["paradox", "brevity", "scientific-wonder"]
    },
    {
        "quote": "The signature of the volcanic flow is its basalt rocks which, over 5 million years of volcanic activity, piled up to form a plateau more than 3350 metres high covering much of central and western India.",
        "author": "Pranay Lal",
        "work": "Indica: A Deep Natural History of the Indian Subcontinent",
        "year": 2016,
        "hook": "How to convey continental scale through basalt accumulation",
        "why_it_lands": "Lal helps the reader visualize the Deccan Traps not as an abstract plateau, but as five million years of molten lava cooling into a three-kilometer-high black fortress covering half a subcontinent.",
        "tags": ["deep-time", "scale", "precision"]
    },
    {
        "quote": "The transformation of the fierce wolf-like ancestors of sheep into giant whales and gentle dolphins is the Cinderella story of the animal world.",
        "author": "Pranay Lal",
        "work": "Indica: A Deep Natural History of the Indian Subcontinent",
        "year": 2016,
        "hook": "How to illuminate evolutionary drift through fairy tale subversion",
        "why_it_lands": "A startling, joyful analogy. Comparing predatory terrestrial ungulates swimming into the Tethys Ocean to become gentle leviathans turns dry paleontology into a miraculous mythic metamorphosis.",
        "tags": ["metaphor", "wonder", "evolutionary-craft"]
    }
]

def main():
    with open(QUOTE_BANK, "r", encoding="utf-8") as f:
        bank = json.load(f)

    existing_quotes = {q["quote"].strip().lower() for q in bank}
    added = 0
    for q in NEW_QUOTES:
        if q["quote"].strip().lower() not in existing_quotes:
            bank.append(q)
            existing_quotes.add(q["quote"].strip().lower())
            added += 1

    with open(QUOTE_BANK, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)

    print(f"Appended {added} new vetted quotes to {QUOTE_BANK}. Total bank size: {len(bank)}")

if __name__ == "__main__":
    main()
