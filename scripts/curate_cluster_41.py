# scripts/curate_cluster_41.py — Vets and integrates 20 quotes from Cluster 41 into quote-bank.json
# Usage: python3 scripts/curate_cluster_41.py

import json

new_quotes = [
    # Susan Orlean — On Animals (2021)
    {
        "quote": "He was cheerful, affectionate, eager to please—the sort of killer whale who, if you were in the water with him, might decide to give you a hug, which would break every bone in your body.",
        "author": "Susan Orlean",
        "work": "On Animals",
        "year": 2021,
        "hook": "How to contrast domestic affection with lethal physical reality",
        "why_it_lands": "Orlean opens with a catalogue of golden-retriever descriptors ('cheerful, affectionate, eager to please') only to pivot abruptly to blunt skeletal physics. The tonal shock forces the reader to confront the terrifying ambivalence of an apex predator treated like a household pet.",
        "tags": ["irony", "sensory detail", "characterization"]
    },
    {
        "quote": "I just took two black bears and bleached one of them. I think I used Clairol Basic bleach, left it on for two hours. It smelled awful, like someone's bad hair appointment, but it came out looking pretty good.",
        "author": "Susan Orlean",
        "work": "On Animals",
        "year": 2021,
        "hook": "How to anchor bizarre subcultures in mundane commercial details",
        "why_it_lands": "The taxidermist's surreal act of bleaching a wild bear is rendered hilariously concrete through brand-name domestic dye ('Clairol Basic') and the sensory banality of a bad salon appointment. The comedy springs entirely from the collision of wilderness and drugstore cosmetology.",
        "tags": ["humor", "sensory detail", "subculture"]
    },
    {
        "quote": "The virus’s ability to survive and spread is uncanny. It can persist on dry cloth with no organic material for more than three months; it survives freezing, and it can withstand temperatures of up to a hundred and twenty degrees for an hour.",
        "author": "Susan Orlean",
        "work": "On Animals",
        "year": 2021,
        "hook": "How to build dread through unadorned physical endurance",
        "why_it_lands": "Orlean avoids apocalyptic hyperbole, choosing instead a clinical catalogue of thermal and temporal thresholds. The quiet listing of dry cloth, freezing, and 120-degree heat makes microscopic persistence feel far more monstrous than any dramatic adjective could.",
        "tags": ["pacing", "clarity", "nonfiction craft"]
    },
    {
        "quote": "It is a sign of some special and strange quality of my life that the first question people ask me when I return from an assignment is usually, 'Did you get to pet it?'",
        "author": "Susan Orlean",
        "work": "On Animals",
        "year": 2021,
        "hook": "How to establish authorial premise through a recurring dialogue hook",
        "why_it_lands": "Rather than announcing a high-minded thematic statement about human-animal coexistence, Orlean captures the entire thesis in a single childlike question. It disarms the reader while immediately diagnosing the universal human impulse toward tactile possession of the wild.",
        "tags": ["voice", "understatement", "opening"]
    },

    # Ryu Murakami — Audition (1997, trans. Ralph McCarthy)
    {
        "quote": "Her fingertips were like ice, and then again like molten lava.",
        "author": "Ryu Murakami",
        "work": "Audition",
        "year": 1997,
        "translator": "Ralph McCarthy",
        "hook": "How to convey sensory dread through violent tactile contradiction",
        "why_it_lands": "Murakami strips away narrative cushioning to present an impossible thermal paradox. By snapping between freezing numbness and scalding intensity in nine words, the tactile shock signals psychic instability before any overt violence occurs.",
        "tags": ["sensory detail", "psychological truth", "foreshadowing"]
    },
    {
        "quote": "Every little sound was amplified, and when Yamasaki Asami peered into his face and said 'Aoyama-san?' in a whisper that was almost a hiss, the blood rushed through his temples with a roar.",
        "author": "Ryu Murakami",
        "work": "Audition",
        "year": 1997,
        "translator": "Ralph McCarthy",
        "hook": "How to escalate claustrophobia through acoustic amplification",
        "why_it_lands": "The prose mirrors physiological panic by contrasting a sibilant, barely audible whisper with internal hemodynamic violence ('blood rushed through his temples with a roar'). The acoustic contrast locks the reader directly inside the protagonist's paralyzed sensorium.",
        "tags": ["suspense", "sensory detail", "internal monologue"]
    },
    {
        "quote": "It wasn’t quite like anything he’d ever known before – a sense of having done something that could never be undone, of having crossed an invisible line into a dark territory where ordinary laws no longer applied.",
        "author": "Ryu Murakami",
        "work": "Audition",
        "year": 1997,
        "translator": "Ralph McCarthy",
        "hook": "How to render the irreversible vertigo of moral transgression",
        "why_it_lands": "Murakami defines the psychological threshold of no return through negative space: it is not dramatic guilt, but an eerie stillness where familiar rules simply cease to register. The cadence conveys absolute, quiet isolation.",
        "tags": ["dread", "psychological truth", "suspense"]
    },
    {
        "quote": "The faces of the ladies in their gaudy clothing and the boys with their thick make-up and dyed hair seemed to float above the crowd like paper lanterns on a murky canal.",
        "author": "Ryu Murakami",
        "work": "Audition",
        "year": 1997,
        "translator": "Ralph McCarthy",
        "hook": "How to turn a nocturnal crowd into an eerie floating panorama",
        "why_it_lands": "The comparison of neon-lit Shibuya faces to festive paper lanterns on polluted water creates an unsettling dissonance between decorative beauty and underlying grime. It grounds urban alienation in lingering visual poetry.",
        "tags": ["metaphor", "imagery", "atmosphere"]
    },

    # Harishankar Parsai — Vaishnav Ki Phislan (1976)
    {
        "quote": "नाक उनकी काफी लम्बी थी। मेरा खयाल है, नाक की हिफाजत सबसे ज्यादा इसी देश में होती है। और या तो नाक बहुत नर्म होती है या छुरा तेज, जिससे छोटी-सी बात से भी नाक कट जाती है।",
        "author": "Harishankar Parsai",
        "work": "Vaishnav Ki Phislan",
        "year": 1976,
        "hook": "How to literalize a cultural idiom to dismantle fragile social pride",
        "why_it_lands": "Parsai takes the sacred subcontinental idiom of 'honour' ('naak katna') and treats it with razor-sharp surgical literalism. By debating whether human noses are unusually fragile or societal knives are extraordinarily sharp, he renders feudal insecurity utterly ridiculous.",
        "tags": ["satire", "cultural critique", "irony"]
    },
    {
        "quote": "मेरी इच्छा है, आप खूब खुशी के साथ अकाल-उत्सव मनाएँ। हम घोर संकट में भी प्रसन्न रहते हैं।",
        "author": "Harishankar Parsai",
        "work": "Vaishnav Ki Phislan",
        "year": 1976,
        "hook": "How to expose political callousness through grotesque festive inversion",
        "why_it_lands": "The compounding of 'akaal' (famine) with 'utsav' (carnival/festival) exposes the obscene complacency of the privileged classes. Parsai's mock blessing weaponizes formal courtesy to lay bare how societal tragedy is converted into moral self-congratulation.",
        "tags": ["satire", "paradox", "irony"]
    },
    {
        "quote": "पचपन करोड़ के हाथों में एक-एक रूमाल दे दिया गया है कि लो, एक दूसरे के स्वराज्य के आँसू पोंछो।",
        "author": "Harishankar Parsai",
        "work": "Vaishnav Ki Phislan",
        "year": 1976,
        "hook": "How to reduce bureaucratic democracy to an absurd physical gesture",
        "why_it_lands": "Distributing 550 million handkerchiefs so citizens can take turns wiping each other's disillusionment transforms vast national grief into a pathetic assembly line. The visual economy crystallizes the empty tokenism of post-colonial statecraft.",
        "tags": ["metaphor", "political critique", "imagery"]
    },
    {
        "quote": "शव-यात्रा का तौलिया तैयार रखते हैं। किसी के मरने की खबर मिली नहीं कि इतने प्रसन्न होते हैं, जैसे किसी की शादी हो रही है।",
        "author": "Harishankar Parsai",
        "work": "Vaishnav Ki Phislan",
        "year": 1976,
        "hook": "How to satirize performative grief through grotesque enthusiasm",
        "why_it_lands": "The professional mourner who keeps his funeral towel laundered and ready treats tragedy as social recreation. By equating the announcement of death with the joy of a wedding feast, Parsai captures the predatory socialite for whom others' grief is merely a stage.",
        "tags": ["satire", "characterization", "humor"]
    },

    # Chuck Palahniuk — Stranger Than Fiction: True Stories (2004)
    {
        "quote": "When the problem looks too big, when we’re shown too much reality, we tend to shut down. We become resigned. We fail to take any action because disaster seems so inevitable. We're trapped.",
        "author": "Chuck Palahniuk",
        "work": "Stranger Than Fiction: True Stories",
        "year": 2004,
        "hook": "How to map the psychological paralysis induced by monolithic scale",
        "why_it_lands": "Palahniuk constructs a descending ladder of short, declarative clauses ('shut down', 'become resigned', 'fail to take action') ending with the monosyllabic finality of 'trapped'. The rhythm enacts the exact cognitive claustrophobia it describes.",
        "tags": ["rhythm", "psychological truth", "syntax"]
    },
    {
        "quote": "After we’re miserable enough—like the narrator in his Fight Club condo, or the narrator isolated by her own beautiful face in Invisible Monsters—we destroy our lovely nest and force ourselves back into the larger world.",
        "author": "Chuck Palahniuk",
        "work": "Stranger Than Fiction: True Stories",
        "year": 2004,
        "hook": "How to articulate self-destruction as a desperate bid for re-entry into life",
        "why_it_lands": "Palahniuk demystifies his own trademark narrative arc: vandalism is not nihilism, but an abrasive cure for numbness. By framing comfortable isolation as a trap that only catastrophic arson can break, he reveals the emotional engine behind transgressive fiction.",
        "tags": ["voice", "philosophy", "story structure"]
    },
    {
        "quote": "It would hurt, chopping off my fat, purple finger, but it would be better than the weeks of letting it rot.",
        "author": "Chuck Palahniuk",
        "work": "Stranger Than Fiction: True Stories",
        "year": 2004,
        "hook": "How to choose acute violent shock over prolonged decay",
        "why_it_lands": "The visceral bluntness of 'fat, purple finger' forces an instinctive physical reaction. Palahniuk uses childhood bodily trauma as an absolute moral calculus: agonizing immediate severing is always preferred to the creeping stench of compromise.",
        "tags": ["sensory detail", "visceral voice", "understatement"]
    },
    {
        "quote": "You become so close with a workout partner that they're like your own blood, and if they go out and lose a match, lose a big match, then you’ve just had your heart torn out.",
        "author": "Chuck Palahniuk",
        "work": "Stranger Than Fiction: True Stories",
        "year": 2004,
        "hook": "How to capture athletic intimacy through vicarious devastation",
        "why_it_lands": "Palahniuk cuts past sports clichés by focusing on the shared nervous system of training partners. The repetition of 'lose a match, lose a big match' mimics the numb stutter of disbelief before the brutal somatic finish.",
        "tags": ["dialogue", "emotion", "rhythm"]
    },

    # Marryam H. Reshii — The Flavour of Spice (2017)
    {
        "quote": "Only thing, it doesn’t have any spices. Because we are in mourning.",
        "author": "Marryam H. Reshii",
        "work": "The Flavour of Spice",
        "year": 2017,
        "hook": "How to convey immense grief through sensory deprivation",
        "why_it_lands": "In a culture where food is defined by intricate aroma and heat, the complete withdrawal of spice is a radical somatic gesture. The starkness of the two short sentences mirrors the sudden flatness of a world drained of joy.",
        "tags": ["understatement", "sensory detail", "cultural critique"]
    },
    {
        "quote": "It is pounded in our mortar and pestle along with black cardamom, shallots and fennel over which the minced meat is added and whole lot is hammered till the mince becomes silky and the spices are amalgamated into its very fibre.",
        "author": "Marryam H. Reshii",
        "work": "The Flavour of Spice",
        "year": 2017,
        "hook": "How to build physical kinetic momentum in culinary prose",
        "why_it_lands": "The sentence relies on strong transitive verbs ('pounded', 'hammered', 'amalgamated') to evoke the sheer physical labor of Kashmiri waza cooking. The tactile transformation from raw muscle to 'silky' emulsification grounds gastronomy in authentic craft.",
        "tags": ["sensory detail", "kinetic prose", "rhythm"]
    },
    {
        "quote": "Every single dish, from main courses like the Dogri khatta meat to desserts like payasam and halwa, is bathed in a medley of spice, to the extent that it is the spice that defines a dish rather than the main ingredient.",
        "author": "Marryam H. Reshii",
        "work": "The Flavour of Spice",
        "year": 2017,
        "hook": "How to invert culinary hierarchy through sensory primacy",
        "why_it_lands": "Reshii challenges Western protein-centric dining taxonomy with an authoritative catalogue spanning savoury meat to dairy desserts. The prose establishes that spices are not decorative seasoning, but the foundational architecture of the meal.",
        "tags": ["clarity", "nonfiction craft", "voice"]
    },
    {
        "quote": "It’s another matter entirely that today, you could claim to have never heard of Tidore or Run and not elicit gasps of astonishment but try telling your colleagues you’ve not heard of Manhattan!",
        "author": "Marryam H. Reshii",
        "work": "The Flavour of Spice",
        "year": 2017,
        "hook": "How to expose historical amnesia through geographical juxtaposition",
        "why_it_lands": "By pairing tiny nutmeg atolls with the capital of global capitalism—which was traded away by the Dutch in exchange for the island of Run—Reshii delivers a punchy history lesson on how perishable spices once dictated the map of modern empire.",
        "tags": ["irony", "history", "voice"]
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

    print(f"Added {added} vetted quotes from Cluster 41. Total in bank: {len(bank)}")

if __name__ == "__main__":
    main()
