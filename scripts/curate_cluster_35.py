# scripts/curate_cluster_35.py — Curates 20 craft quotes from Cluster 35 (Partition Grief, Domestic Moralism & Feline Calm)
# Usage: python3 scripts/curate_cluster_35.py
# Requires: json, os

import json
import os

QUOTE_BANK_PATH = "content/quote-bank.json"

VETTED_CLUSTER_35 = [
    # 1. Rahi Masoom Raza — Topi Shukla (1969), trans. Meenakshi Shivram
    {
        "quote": "यह तो बिलकुल ही ग़लत ट्रान्स्लेशन हुआ। यह अनुवाद किसी प्रोफ़ेसर, या किसी महा उपाध्याय या किसी समसुलउलमा ने नहीं किया था। साधारण लोगों ने किया था।",
        "author": "Rahi Masoom Raza",
        "work": "Topi Shukla",
        "year": 1969,
        "translator": "Meenakshi Shivram",
        "hook": "How to locate linguistic revolution in common folk vernacular.",
        "why_it_lands": "Raza dismantles academic elitism with sly populist humor: living languages aren't forged in prestigious university seminars or liturgical courts, but shaped daily by ordinary people speaking on the street.",
        "tags": ["language", "vernacular", "satire", "translation"]
    },
    {
        "quote": "वह साहित्य का रसिया था। वामिक जौनपुरी, साहिर लुधियानवी, अली सरदार जाफ़री और दूसरे कवियों की कविताओं और कृश्नचन्दर, अब्बास और दूसरे कथाकारों की कहानियों ने उससे कहा कि इस आज़ादी में कोई घपला है।",
        "author": "Rahi Masoom Raza",
        "work": "Topi Shukla",
        "year": 1969,
        "translator": "Meenakshi Shivram",
        "hook": "How to use literary appetite as political awakening.",
        "why_it_lands": "Raza shows how revolutionary poetry alerts an adolescent mind to institutional deception: reading progressive poets pierces post-independence propaganda, revealing the fraudulent compromises hiding behind triumphant national rhetoric.",
        "tags": ["literature", "politics", "poetry", "awakening"]
    },
    {
        "quote": "अगर ये सारे मुसलमान पाकिस्तान भेज दिए जाएँ तो जो नौकरियाँ इन्हें मिलती हैं वह भी हिन्दुओं ही को मिल जाएँगी। नौकरी ! यह कैसा घिनौना शब्द है!",
        "author": "Rahi Masoom Raza",
        "work": "Topi Shukla",
        "year": 1969,
        "translator": "Meenakshi Shivram",
        "hook": "How to skewer sectarian hatred with economic disgust.",
        "why_it_lands": "Raza exposes the squalid commercial greed underlying communal bigotry: religious chauvinism is unmasked as petty bureaucratic envy over scarce government clerk positions.",
        "tags": ["critique", "irony", "prejudice", "economy"]
    },
    {
        "quote": "मैं पाकिस्तान कैसे जा सकता हूँ! मोहर्रम में इमाम हुसैन हिन्दुस्तान आते हैं। इस साल उनसे मुलाक़ात करके पूछूँगा कि सच बोलने की सज़ा आदमी को कब तक मिलती रहेगी।",
        "author": "Rahi Masoom Raza",
        "work": "Topi Shukla",
        "year": 1969,
        "translator": "Meenakshi Shivram",
        "hook": "How to blend tragic folklore with desperate childhood defiance.",
        "why_it_lands": "Raza captures the heart-rending absurdity of Partition through a child's sacred geography: faith belongs to the soil and grief of home, demanding an accounting for why truthfulness brings continuous persecution.",
        "tags": ["faith", "innocence", "tragedy", "dialogue"]
    },

    # 2. Dharamvir Bharati — Gunahon Ka Devta (1949), trans. Poonam Saxena
    {
        "quote": "ऐसा लगता है कि इस शहर की बनावट, गठन, जिंदगी और रहन-सहन में कोई बँधे-बँधाये नियम नहीं, कहीं कोई कसाव नहीं, हर जगह एक स्वच्छन्द खुलाव, एक बिखरी हुई-सी अनियमितता।",
        "author": "Dharamvir Bharati",
        "work": "Gunahon Ka Devta",
        "year": 1949,
        "translator": "Poonam Saxena",
        "hook": "How to sketch an ancient river city through deliberate structural looseness.",
        "why_it_lands": "Bharati captures Allahabad's architectural spirit through evocative rhythm: the holy confluence city resists rigid civic geometry, flourishing instead through chaotic, sprawling warmth and irregular freedom.",
        "tags": ["setting", "city", "atmosphere", "rhythm"]
    },
    {
        "quote": "देखो, ऐसी अरसौहीं अँगड़ाई न लिया करो, इससे लोग समझ जाते हैं कि अब बचपन करवट बदल रहा है।",
        "author": "Dharamvir Bharati",
        "work": "Gunahon Ka Devta",
        "year": 1949,
        "translator": "Poonam Saxena",
        "hook": "How to mark the arrival of adulthood in a single bodily stretch.",
        "why_it_lands": "Bharati captures the transition from girlhood to womanhood with delicate domestic observation: an unconscious stretch of the limbs becomes a threshold crossing that society immediately polices.",
        "tags": ["adolescence", "observation", "body", "innocence"]
    },
    {
        "quote": "जैसे-तैसे उसकी थोड़ी-सी आँख लगी... किसी ने सहसा जगा दिया। पलक बन्द करने में जितना दर्द हुआ था उतना ही पलकें खोलने में।",
        "author": "Dharamvir Bharati",
        "work": "Gunahon Ka Devta",
        "year": 1949,
        "translator": "Poonam Saxena",
        "hook": "How to render physical grief through symmetric muscular strain.",
        "why_it_lands": "Bharati mirrors heartbreak in bodily sensation: shutting exhausted eyelids burns with sorrow, and opening them to face waking consciousness hurts equally, trapping the sufferer in unbroken pain.",
        "tags": ["grief", "pain", "sensory", "symmetry"]
    },
    {
        "quote": "लेकिन वह नशा टूट चुका था, वह साँस धीमी पड़ गयी थी...अपनी हर कोशिश के बावजूद वह पम्मी को उदास होने से बचा न पाता था।",
        "author": "Dharamvir Bharati",
        "work": "Gunahon Ka Devta",
        "year": 1949,
        "translator": "Poonam Saxena",
        "hook": "How to evoke the irreversible fading of passionate illusion.",
        "why_it_lands": "Bharati charts the dissipation of romantic intoxication with quiet melancholy: once emotional intoxication fractures, no frantic act of will can prevent sadness from reclaiming the room.",
        "tags": ["melancholy", "passion", "loss", "realism"]
    },

    # 3. Satyajit Ray — The Best of Satyajit Ray (2001)
    {
        "quote": "Growing up amidst people from various parts of the country, she learnt to communicate with those who did not speak her language, and whose language she could not understand.",
        "author": "Satyajit Ray",
        "work": "The Best of Satyajit Ray",
        "year": 2001,
        "translator": None,
        "hook": "How to establish empathetic translation beyond verbal fluency.",
        "why_it_lands": "Ray captures the intuitive basis of human connection: genuine communication thrives in the non-verbal margins between distinct dialects, relying on observation, gesture, and patience rather than shared grammar.",
        "tags": ["language", "empathy", "communication", "observation"]
    },
    {
        "quote": "You’re pretty much on your own, like me, he had said.",
        "author": "Satyajit Ray",
        "work": "The Best of Satyajit Ray",
        "year": 2001,
        "translator": None,
        "hook": "How to forge a lonely kinship across nine words.",
        "why_it_lands": "Ray captures solitary companionship without sentimentality: two isolated characters bond instantly not through shared joy, but through mutual recognition of their stubborn, quiet estrangement from the crowd.",
        "tags": ["solitude", "dialogue", "brevity", "character"]
    },
    {
        "quote": "You have been to Ranchi, but due to some unknown reason, the entire episode has slipped out of your mind.",
        "author": "Satyajit Ray",
        "work": "The Best of Satyajit Ray",
        "year": 2001,
        "translator": None,
        "hook": "How to open a detective mystery by diagnosing amnesia.",
        "why_it_lands": "Ray creates immediate narrative suspense with clinical detachment: memory loss isn't treated as melodrama, but as an unsettling forensic discrepancy waiting for rational deduction.",
        "tags": ["mystery", "memory", "suspense", "clarity"]
    },
    {
        "quote": "This object is certainly worth keeping in my collection, but I cannot bear its effect on me. My temperature keeps shooting higher, and a most unpleasant scene rises before my eyes.",
        "author": "Satyajit Ray",
        "work": "The Best of Satyajit Ray",
        "year": 2001,
        "translator": None,
        "hook": "How to summon macabre obsession through physiological distress.",
        "why_it_lands": "Ray balances scholarly antiquarianism against psychological horror: the collector's acquisitive pride is overthrown by violent bodily panic whenever the cursed artifact is held in the hand.",
        "tags": ["horror", "objects", "suspense", "body"]
    },
    {
        "quote": "I will not have to chase ghosts again, Sitesh Babu. Never. I have finished with them.",
        "author": "Satyajit Ray",
        "work": "The Best of Satyajit Ray",
        "year": 2001,
        "translator": None,
        "hook": "How to deliver a definitive goodbye to the supernatural with cold finality.",
        "why_it_lands": "Ray delivers the closure of an eerie adventure not with grand spectacle, but with quiet, unshakeable resolution: the protagonist steps away from the borderlands of the dead and shuts the door permanently behind him.",
        "tags": ["ghosts", "resolution", "dialogue", "finality"]
    },

    # 4. Claudia Piñeiro — Elena Knows (2007), trans. Frances Riddle
    {
        "quote": "Are you your brain, which keeps sending out orders that won’t be followed? Or are you the thought itself, something that can’t be seen or touched beyond that furrowed organ guarded inside the cranium like a trove?",
        "author": "Claudia Piñeiro",
        "work": "Elena Knows",
        "year": 2007,
        "translator": "Frances Riddle",
        "hook": "How to question bodily consciousness through neurological rebellion.",
        "why_it_lands": "Piñeiro articulates the Cartesian horror of Parkinson's disease with philosophical terror: consciousness remains fully intact inside a skull whose motor signals are ignored by limbs that have formed their own mutinous will.",
        "tags": ["consciousness", "body", "illness", "philosophy"]
    },
    {
        "quote": "The plastic bottles, polystyrene cups, the chunks of concrete. Litter has accumulated below the platform opposite them, some of it will disintegrate with time, some of it will outlive her.",
        "author": "Claudia Piñeiro",
        "work": "Elena Knows",
        "year": 2007,
        "translator": "Frances Riddle",
        "hook": "How to contrast human mortality against industrial synthetic waste.",
        "why_it_lands": "Piñeiro measures bodily decline against urban decay with grim tactile realism: disposable polystyrene cups will outlast human bone and flesh, turning railway ballast into an immortal graveyard of trash.",
        "tags": ["mortality", "objects", "realism", "time"]
    },
    {
        "quote": "The problem isn’t how you look but who has to look at you.",
        "author": "Claudia Piñeiro",
        "work": "Elena Knows",
        "year": 2007,
        "translator": "Frances Riddle",
        "hook": "How to expose the cruelty of aesthetic shame in caretaking.",
        "why_it_lands": "Piñeiro cuts straight through superficial decorum: the true burden of physical disability in a judging society is not the sufferer's pain, but the discomfort and disgust it provokes in healthy bystanders.",
        "tags": ["disability", "truth", "society", "brevity"]
    },
    {
        "quote": "It’s not the smell of the perfume or deodorant the person wore or the laundry soap it was washed with when there was still someone to stain it. It’s the smell of the dead person when they were alive. The smell of Rita.",
        "author": "Claudia Piñeiro",
        "work": "Elena Knows",
        "year": 2007,
        "translator": "Frances Riddle",
        "hook": "How to anchor sensory haunting in biological odor.",
        "why_it_lands": "Piñeiro rejects clean sentimental eulogies: grief survives not in photographic memories or laundered cotton, but in the unrepeatable physical animal scent of a daughter who was once alive.",
        "tags": ["grief", "scent", "memory", "sensory"]
    },

    # 5. John Gray — Feline Philosophy: Cats and the Meaning of Life (2020)
    {
        "quote": "Thinking of happiness as a project, they look for fulfilment at some future time. The present slips by, and anxiety creeps in.",
        "author": "John Gray",
        "work": "Feline Philosophy: Cats and the Meaning of Life",
        "year": 2020,
        "translator": None,
        "hook": "How to diagnose modern neurosis as future-oriented teleology.",
        "why_it_lands": "Gray skewers self-help culture with philosophical razor: framing happiness as an executive goal defers contentment into an unreachable tomorrow while letting existential panic fill the empty present.",
        "tags": ["philosophy", "time", "anxiety", "critique"]
    },
    {
        "quote": "Cats decide to die. They creep into a cool place somewhere, because of the heat of their blood, crouch down, and wait to die.",
        "author": "John Gray",
        "work": "Feline Philosophy: Cats and the Meaning of Life",
        "year": 2020,
        "translator": None,
        "hook": "How to describe mortal acceptance through animal instinct.",
        "why_it_lands": "Gray (quoting Doris Lessing) contrasts human metaphysical panic against feline calm: death is approached not with bargaining or hysterical protest, but as a cool physical retreat into stillness.",
        "tags": ["death", "nature", "instinct", "calm"]
    },
    {
        "quote": "Knowing only life until they are on the brink of dying, cats are not ruled by death.",
        "author": "John Gray",
        "work": "Feline Philosophy: Cats and the Meaning of Life",
        "year": 2020,
        "translator": None,
        "hook": "How to liberate consciousness from the terror of non-existence.",
        "why_it_lands": "Gray delivers an Epicurean insight through animal psychology: human beings spend their whole lives dying in advance through anticipatory dread, while creatures without self-narratives inhabit pure life until the final breath.",
        "tags": ["mortality", "paradox", "clarity", "stoicism"]
    },
    {
        "quote": "Unlike dogs, cats have not become part-human.",
        "author": "John Gray",
        "work": "Feline Philosophy: Cats and the Meaning of Life",
        "year": 2020,
        "translator": None,
        "hook": "How to celebrate radical alterity in eight words.",
        "why_it_lands": "Gray notes why cats fascinate and frustrate human vanity: unlike domestic dogs who adopt human guilt and eagerness to please, the cat remains entirely sovereign and indifferent to our moral dramas.",
        "tags": ["brevity", "animals", "autonomy", "truth"]
    }
]

def main():
    if not os.path.exists(QUOTE_BANK_PATH):
        print(f"Error: {QUOTE_BANK_PATH} not found.")
        return

    with open(QUOTE_BANK_PATH, "r", encoding="utf-8") as f:
        bank = json.load(f)

    print(f"Current quote bank count: {len(bank)}")

    # Check for duplicates
    existing_quotes = {q["quote"].strip() for q in bank}
    added = 0
    for q in VETTED_CLUSTER_35:
        if q["quote"].strip() not in existing_quotes:
            bank.append(q)
            existing_quotes.add(q["quote"].strip())
            added += 1
        else:
            print(f"Skipping duplicate: {q['quote'][:40]}...")

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)

    print(f"Successfully added {added} quotes from Cluster 35.")
    print(f"New quote bank total: {len(bank)}")

if __name__ == "__main__":
    main()
