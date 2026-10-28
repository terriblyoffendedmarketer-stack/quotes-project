# scripts/curate_cluster_19.py — Curates 20 craft quotes from Cluster 19 (Moral Clarity, Banality & Existential Longing)
# Usage: python3 scripts/curate_cluster_19.py
# Requires: json, os

import json
import os

QUOTE_BANK_PATH = "content/quote-bank.json"

VETTED_CLUSTER_19 = [
    # 1. Hannah Arendt — Eichmann in Jerusalem: A Report on the Banality of Evil (1963)
    {
        "quote": "They are so obviously three good and honest men that one is not surprised that none of them yields to the greatest temptation to playact in this setting – that of pretending that they, all three born and educated in Germany, must wait for the Hebrew translation.",
        "author": "Hannah Arendt",
        "work": "Eichmann in Jerusalem: A Report on the Banality of Evil",
        "year": 1963,
        "translator": None,
        "hook": "How to capture bureaucratic absurdity and judicial decorum in a single observational stroke.",
        "why_it_lands": "Arendt exposes the courtroom's polite theatricality not with indignation, but with a dry, forensic appraisal of how educated men perform formal justice while ignoring the shared language of the accused.",
        "tags": ["irony", "forensic", "bureaucracy", "observation"]
    },
    {
        "quote": "I could not; I had to disappear.",
        "author": "Hannah Arendt",
        "work": "Eichmann in Jerusalem: A Report on the Banality of Evil",
        "year": 1963,
        "translator": None,
        "hook": "How to distill absolute moral cowardice into seven monosyllabic words.",
        "why_it_lands": "Stripped of bureaucratic euphemisms, Eichmann's excuse reveals the core mechanism of administrative evil: the instinctive retreat of the ego into total erasure to evade complicity.",
        "tags": ["voice", "understatement", "confession", "brevity"]
    },
    {
        "quote": "The question was whether Eichmann had lied when he said: ‘I never killed a Jew or, for that matter, I never killed a non-Jew… . I never gave an order to kill a Jew nor an order to kill a non-Jew.’",
        "author": "Hannah Arendt",
        "work": "Eichmann in Jerusalem: A Report on the Banality of Evil",
        "year": 1963,
        "translator": None,
        "hook": "How to isolate administrative detachment in its barest legal syntax.",
        "why_it_lands": "Arendt isolates how bureaucratic syntax severs individual agency from industrialized slaughter, exposing how procedural innocence becomes the ultimate mask for systemic murder.",
        "tags": ["syntax", "forensic", "denial", "responsibility"]
    },
    {
        "quote": "He began by stating emphatically that he was a Gottgläubiger, to express in common Nazi fashion that he was no Christian and did not believe in life after death. He then proceeded: ‘After a short while, gentlemen, we shall all meet again. Such is the fate of all men.’",
        "author": "Hannah Arendt",
        "work": "Eichmann in Jerusalem: A Report on the Banality of Evil",
        "year": 1963,
        "translator": None,
        "hook": "How to expose totalitarian absurdity through an immediate ideological contradiction.",
        "why_it_lands": "The immediate contradiction between stated ideological atheism and a theatrical, clichéd farewell demonstrates how unexamined slogans substitute for genuine thought in the totalitarian mind.",
        "tags": ["irony", "cliche", "characterization", "absurdity"]
    },

    # 2. Dharamvir Bharati — Gunahon Ka Devta (1949)
    {
        "quote": "ऐसा लगता है कि इस शहर की बनावट, गठन, जिंदगी और रहन-सहन में कोई बँधे-बँधाये नियम नहीं, कहीं कोई कसाव नहीं, हर जगह एक स्वच्छन्द खुलाव, एक बिखरी हुई-सी अनियमितता।",
        "author": "Dharamvir Bharati",
        "work": "Gunahon Ka Devta",
        "year": 1949,
        "translator": None,
        "hook": "How to establish a city's psychological freedom through expansive, rhythmic prose.",
        "why_it_lands": "Bharati sketches Allahabad not merely as architecture or geography, but as an unruly state of consciousness—uncorseted, generous, and defined by a scattered, effortless vitality.",
        "tags": ["setting", "rhythm", "hindi-literature", "atmosphere"]
    },
    {
        "quote": "बड़ी फीकी, बड़ी बेजार, बड़ी बनावटी लगती हैं ये कविताएँ, मन के दर्द के आगे सभी फीकी हैं।",
        "author": "Dharamvir Bharati",
        "work": "Gunahon Ka Devta",
        "year": 1949,
        "translator": None,
        "hook": "How to strip aesthetic sentimentality bare in the face of actual suffering.",
        "why_it_lands": "The rhythmic cadence of the adjectives ('फीकी... बेजार... बनावटी') strips romantic poetry to the bone, establishing an unbridgeable gulf between aesthetic decoration and raw human grief.",
        "tags": ["repetition", "disillusionment", "hindi-literature", "candor"]
    },
    {
        "quote": "जैसे-तैसे उसकी थोड़ी-सी आँख लगी... किसी ने सहसा जगा दिया। पलक बन्द करने में जितना दर्द हुआ था उतना ही पलकें खोलने में।",
        "author": "Dharamvir Bharati",
        "work": "Gunahon Ka Devta",
        "year": 1949,
        "translator": None,
        "hook": "How to render acute psychological exhaustion as a physical, somatic reflex.",
        "why_it_lands": "Bharati balances the exact physical symmetry of opening and closing the eyelids, turning an involuntary biological movement into a precise gauge of unbearable sorrow.",
        "tags": ["sensory", "symmetry", "hindi-literature", "grief"]
    },
    {
        "quote": "यह देवत्व की मूर्ति-सी पथरीली सुधा! यह चन्दर की सुधा तो नहीं!",
        "author": "Dharamvir Bharati",
        "work": "Gunahon Ka Devta",
        "year": 1949,
        "translator": None,
        "hook": "How to capture the tragic estrangement of idealization in two abrupt exclamations.",
        "why_it_lands": "The abrupt contrast between a petrified, sanctified goddess and the living intimacy of a beloved woman reveals the tragedy of elevating someone onto a pedestal where they can no longer be loved.",
        "tags": ["contrast", "tragedy", "hindi-literature", "idealization"]
    },

    # 3. Mieko Kawakami — Heaven (2009)
    {
        "quote": "“We should be friends.” That’s all it said.",
        "author": "Mieko Kawakami",
        "work": "Heaven",
        "year": 2009,
        "translator": "Sam Bett & David Boyd",
        "hook": "How to charge a mundane elementary overture with quiet, suffocating suspense.",
        "why_it_lands": "Kawakami isolates the blunt four-word note against the brutal reality of schoolyard torment, where sudden solidarity feels just as dangerous and destabilizing as violence.",
        "tags": ["brevity", "tension", "understatement", "dialogue"]
    },
    {
        "quote": "It was like being a piece of furniture in a room that nobody uses.",
        "author": "Mieko Kawakami",
        "work": "Heaven",
        "year": 2009,
        "translator": "Sam Bett & David Boyd",
        "hook": "How to convey total social non-existence through a domestic object simile.",
        "why_it_lands": "Rather than dramatizing emotional woundedness, Kawakami reduces the human self to forgotten upholstery—occupying physical space while completely erased from collective consciousness.",
        "tags": ["simile", "isolation", "domestic-imagery", "alienation"]
    },
    {
        "quote": "Maybe it looks like they’re doing everything while we sit there doing nothing, but that’s not true. What we’re doing has meaning.",
        "author": "Mieko Kawakami",
        "work": "Heaven",
        "year": 2009,
        "translator": "Sam Bett & David Boyd",
        "hook": "How to formulate an ethics of passive endurance against overwhelming cruelty.",
        "why_it_lands": "Kojima's quiet assertion inverts conventional power dynamics, transforming forced physical immobility and silence from a sign of surrender into an intentional, stubborn defiance.",
        "tags": ["voice", "endurance", "defiance", "philosophy"]
    },
    {
        "quote": "Nobody does anything because they have the right. They do it because they want to.",
        "author": "Mieko Kawakami",
        "work": "Heaven",
        "year": 2009,
        "translator": "Sam Bett & David Boyd",
        "hook": "How to articulate ruthless amoral power with casual conversational simplicity.",
        "why_it_lands": "Momose strips away every moral rationalization of cruelty in two clipped sentences, presenting raw desire and capacity as the only operative laws of the playground.",
        "tags": ["candor", "dialogue", "power", "nihilism"]
    },

    # 4. Hermann Hesse — Siddhartha (1922)
    {
        "quote": "Walking the rosy paths of the fig tree garden, sitting in the bluish shade of the grove of contemplation, washing his limbs daily in the bath of repentance, sacrificing in the dim shade of the mango forest, his gestures of perfect decency, everyone’s love and joy, he still lacked all joy in his heart.",
        "author": "Hermann Hesse",
        "work": "Siddhartha",
        "year": 1922,
        "translator": "Hilda Rosner",
        "hook": "How to build an elaborate catalogue of piety only to collapse it with a single final clause.",
        "why_it_lands": "Hesse layers rhythmic participial phrases filled with sensory color and ritual perfection, creating a lush facade of spiritual accomplishment that makes the stark concluding vacancy hit with double force.",
        "tags": ["rhythm", "catalogue", "sensory", "contrast"]
    },
    {
        "quote": "It was the self, the purpose and essence of which I sought to learn. It was the self, I wanted to free myself from, which I sought to overcome. But I was not able to overcome it, could only deceive it, could only flee from it, only hide from it.",
        "author": "Hermann Hesse",
        "work": "Siddhartha",
        "year": 1922,
        "translator": "Hilda Rosner",
        "hook": "How to map the recursive trap of ego through parallel clauses and escalating verbs.",
        "why_it_lands": "The triadic structure ('deceive it... flee from it... hide from it') captures the psychological cul-de-sac of ascetic striving, showing that the harder one fights the ego, the more entangled one becomes.",
        "tags": ["syntax", "parallelism", "paradox", "introspection"]
    },
    {
        "quote": "Never before, it had become so strangely clear to Siddhartha, how closely lust was akin to death.",
        "author": "Hermann Hesse",
        "work": "Siddhartha",
        "year": 1922,
        "translator": "Hilda Rosner",
        "hook": "How to link sensual intoxication to mortality in an unadorned declarative cadence.",
        "why_it_lands": "Hesse connects two primal human currents with quiet, unhurried certainty, making the profound existential realization feel ancient and inevitable rather than dramatic.",
        "tags": ["theme", "clarity", "mortality", "desire"]
    },
    {
        "quote": "Wisdom cannot be passed on. Wisdom which a wise man tries to pass on to someone always sounds like foolishness.",
        "author": "Hermann Hesse",
        "work": "Siddhartha",
        "year": 1922,
        "translator": "Hilda Rosner",
        "hook": "How to state the fundamental limitation of language and instruction in two plain strokes.",
        "why_it_lands": "The aphorism cuts cleanly through millennia of didactic tradition, highlighting the inevitable decay that occurs whenever lived understanding is compressed into pedagogical speech.",
        "tags": ["aphorism", "paradox", "philosophy", "simplicity"]
    },

    # 5. Bhagat Singh — Why I Am An Atheist (1930)
    {
        "quote": "Whether it is such an undue pride that has led me to atheism or whether it is after very careful study of the subject and after much consideration that I have come to disbelieve in God is a question that I intend to discuss here.",
        "author": "Bhagat Singh",
        "work": "Why I Am An Atheist",
        "year": 1930,
        "translator": None,
        "hook": "How to disarm an opponent's psychological accusation by accepting it as an open inquiry.",
        "why_it_lands": "Writing from a colonial condemned cell, Singh rejects emotional defensiveness, opening his essay with judicial detachment and converting a personal smear into a calm intellectual examination.",
        "tags": ["rhetoric", "candor", "inquiry", "opening"]
    },
    {
        "quote": "British rule is here not because God wills it but because they possess power and we do not dare to oppose them.",
        "author": "Bhagat Singh",
        "work": "Why I Am An Atheist",
        "year": 1930,
        "translator": None,
        "hook": "How to puncture theological justification with cold material reality.",
        "why_it_lands": "Singh collapses divine providence into raw violence and collective hesitation in twenty-one words, refusing the consolation of fatalism in exchange for clear political accountability.",
        "tags": ["political-thought", "clarity", "antithesis", "power"]
    },
    {
        "quote": "It takes a loud voice to make the deaf hear.",
        "author": "Bhagat Singh",
        "work": "Why I Am An Atheist",
        "year": 1930,
        "translator": None,
        "hook": "How to justify extreme action through a razor-sharp acoustic metaphor.",
        "why_it_lands": "Quoting the French anarchist martyr Auguste Vaillant, Singh re-frames political provocation not as arbitrary violence, but as a severe acoustical necessity demanded by institutional indifference.",
        "tags": ["metaphor", "motto", "sensory", "rhetoric"]
    },
    {
        "quote": "It was perhaps Upton Sinclair that wrote at some place that just make a man a believer in immortality and then rob him of all his riches and possessions. He shall help you even in that ungrudgingly.",
        "author": "Bhagat Singh",
        "work": "Why I Am An Atheist",
        "year": 1930,
        "translator": None,
        "hook": "How to expose religious exploitation through a biting, transactional scenario.",
        "why_it_lands": "Singh illustrates how otherworldly promises serve as ideological sedation, allowing earthly exploitation to unfold with the smiling cooperation of the victim.",
        "tags": ["satire", "argument", "materialism", "irony"]
    }
]

def main():
    with open(QUOTE_BANK_PATH, "r", encoding="utf-8") as f:
        quote_bank = json.load(f)

    print(f"Existing quote bank count: {len(quote_bank)}")

    # Check for duplicates by quote prefix
    existing_quotes = {q["quote"].strip()[:50].lower() for q in quote_bank}
    
    added_count = 0
    for entry in VETTED_CLUSTER_19:
        key = entry["quote"].strip()[:50].lower()
        if key in existing_quotes:
            print(f"Skipping duplicate: {entry['work']} - {entry['quote'][:40]}...")
            continue
        quote_bank.append(entry)
        existing_quotes.add(key)
        added_count += 1

    print(f"Added {added_count} new vetted quotes from Cluster 19.")
    print(f"New quote bank total: {len(quote_bank)}")

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(quote_bank, f, indent=2, ensure_ascii=False)
        f.write("\n")

if __name__ == "__main__":
    main()
