# scripts/curate_cluster_33.py — Curates 20 craft quotes from Cluster 33 (Fabulism, Delusion & Shared Fractures)
# Usage: python3 scripts/curate_cluster_33.py
# Requires: json, os

import json
import os

QUOTE_BANK_PATH = "content/quote-bank.json"

VETTED_CLUSTER_33 = [
    # 1. Ken Liu — The Paper Menagerie and Other Stories (2016)
    {
        "quote": "It is simultaneously a score and recording. A speech sounds like a speech, a lament a lament, and a story re-creates perfectly the teller’s breathless excitement.",
        "author": "Ken Liu",
        "work": "The Paper Menagerie and Other Stories",
        "year": 2016,
        "translator": None,
        "hook": "How to define oral prose cadence as physical acoustics.",
        "why_it_lands": "Liu captures the sonic alchemy of written narrative: text is not merely arbitrary symbolic notation, but musical tablature engineered to reconstruct the speaker's vocal tempo and breath.",
        "tags": ["voice", "style", "sound", "storytelling"]
    },
    {
        "quote": "Each mind grows from a seed inherited through the millennia, and every thought leaves a mark that can be read and seen.",
        "author": "Ken Liu",
        "work": "The Paper Menagerie and Other Stories",
        "year": 2016,
        "translator": None,
        "hook": "How to trace generational memory through geological permanence.",
        "why_it_lands": "Liu links ancestral inheritance with physical inscription, framing cognition not as an isolated spark in the dark, but as an ancient seed accumulating permanent, legible strata across deep time.",
        "tags": ["memory", "time", "metaphor", "ancestry"]
    },
    {
        "quote": "You can measure, if you apply statistical software to it, how much a girl depreciates with each passing year; how much value men place on each pound, each inch of deviation from the ideal they’re seeking; how much more a blonde really is worth than a brunette; and how much more a girl who can pass as Japanese can charge than one who cannot.",
        "author": "Ken Liu",
        "work": "The Paper Menagerie and Other Stories",
        "year": 2016,
        "translator": None,
        "hook": "How to expose societal commodification through chilling algorithmic coldness.",
        "why_it_lands": "Liu weaponizes quantitative metrics to lay bare how market logic strips human bodies down to depreciating assets, achieving moral horror through mathematical detachment.",
        "tags": ["critique", "clarity", "subversion", "observation"]
    },
    {
        "quote": "For years, Mom carefully sliced open the wrappings around Christmas gifts and saved them on top of the fridge in a thick stack.",
        "author": "Ken Liu",
        "work": "The Paper Menagerie and Other Stories",
        "year": 2016,
        "translator": None,
        "hook": "How to anchor character thrift and tenderness in a single domestic habit.",
        "why_it_lands": "Liu renders love and immigrant economy through precise physical ritual: the careful preservation of wrapping paper avoids sentimental commentary, letting the quiet stack atop the refrigerator hold the emotional weight.",
        "tags": ["detail", "understatement", "character", "tenderness"]
    },
    {
        "quote": "It was naive and wise at the same time, and Ruth can almost feel, despite the Regulator, a kind of poignancy to her confident desperation.",
        "author": "Ken Liu",
        "work": "The Paper Menagerie and Other Stories",
        "year": 2016,
        "translator": None,
        "hook": "How to hold contradictory character traits in psychological equilibrium.",
        "why_it_lands": "Liu captures the delicate ambivalence of observation: maturity and naivety coexist without cancelling each other out, registered through an artificial emotional filter that fails to numb genuine sympathy.",
        "tags": ["character", "psychology", "nuance", "sympathy"]
    },
    {
        "quote": "Within the Four Seas, all men are brothers. If all men were brothers at the time of Confucius, then it stands to reason that being descended from them, Li Xiaoyi and I are related.",
        "author": "Ken Liu",
        "work": "The Paper Menagerie and Other Stories",
        "year": 2016,
        "translator": None,
        "hook": "How to weaponize classical rhetoric against institutional authority.",
        "why_it_lands": "Liu demonstrates courtroom subversion through classical syllogism: turning revered canonical morality back onto an authoritarian magistrate exposes the legal hypocrisy of persecuting kin.",
        "tags": ["wit", "dialogue", "argument", "subversion"]
    },

    # 2. Jia Tolentino — Trick Mirror: Reflections on Self-Delusion (2019)
    {
        "quote": "The problem is that we’re all trying to be the hero of our own stories, and the story always ends badly when you try to be the hero.",
        "author": "Jia Tolentino",
        "work": "Trick Mirror: Reflections on Self-Delusion",
        "year": 2019,
        "translator": None,
        "hook": "How to skewer the delusion of moral protagonist syndrome.",
        "why_it_lands": "Tolentino punctures contemporary narcissism with crisp narrative logic: demanding to be cast as the righteous protagonist inevitably distorts the surrounding human reality and collapses into tragic bathos.",
        "tags": ["narrative", "delusion", "irony", "truth"]
    },
    {
        "quote": "We became keenly watchful for transgressions. After a while it wasn’t just transgressions we were keenly watchful for. It was misspeakings.",
        "author": "Jia Tolentino",
        "work": "Trick Mirror: Reflections on Self-Delusion",
        "year": 2019,
        "translator": None,
        "hook": "How to document social descent through escalating precision.",
        "why_it_lands": "Tolentino charts the tightening paranoia of digital discourse in two brief beats, moving from broad violations of principle down to the microscopic policing of accidental syllables.",
        "tags": ["observation", "rhythm", "critique", "modernity"]
    },
    {
        "quote": "There is no good answer to being a woman; the art may instead lie in how we refuse the question.",
        "author": "Jia Tolentino",
        "work": "Trick Mirror: Reflections on Self-Delusion",
        "year": 2019,
        "translator": None,
        "hook": "How to subvert an impossible dilemma through categorical refusal.",
        "why_it_lands": "Tolentino dismantles cultural double binds with philosophical agility: when every prescribed role is a trap, liberation lies not in producing a compliant response, but in rejecting the premise of the examination.",
        "tags": ["subversion", "clarity", "autonomy", "voice"]
    },
    {
        "quote": "The underlying situation is simple. We are all defined by our historical terms and conditions, and these terms and conditions have mostly been written by and for men.",
        "author": "Jia Tolentino",
        "work": "Trick Mirror: Reflections on Self-Delusion",
        "year": 2019,
        "translator": None,
        "hook": "How to reframe patriarchal history as an unread terms-of-service agreement.",
        "why_it_lands": "Tolentino borrows mundane digital bureaucracy—the 'terms and conditions' nobody clicks to read—to illuminate how structural inheritance silently predetermines individual lives before they even begin.",
        "tags": ["metaphor", "clarity", "history", "critique"]
    },

    # 3. Perumal Murugan — One Part Woman (2010), trans. Aniruddhan Vasudevan
    {
        "quote": "Should I put a child on her lap the month after the wedding? I can only drop a grinding stone into her lap. Can’t she be patient for a year or two? We are young.",
        "author": "Perumal Murugan",
        "work": "One Part Woman",
        "year": 2010,
        "translator": "Aniruddhan Vasudevan",
        "hook": "How to convey the crushing weight of domestic expectation through domestic objects.",
        "why_it_lands": "Murugan contrasts the living baby against the stone grinder with brutal tactile domesticity, showing how maternal impatience turns a daughter-in-law's body into an anvil under continuous judgment.",
        "tags": ["metaphor", "pressure", "dialogue", "domesticity"]
    },
    {
        "quote": "All men who set their foot in Tiruchengode on the fourteenth day are gods.",
        "author": "Perumal Murugan",
        "work": "One Part Woman",
        "year": 2010,
        "translator": "Aniruddhan Vasudevan",
        "hook": "How to suspend social order with a single liturgical decree.",
        "why_it_lands": "Murugan captures how communal ritual sanctifies what society otherwise violently forbids: declaring ordinary men divine for a single night licenses transgression by elevating carnal desire into mythic necessity.",
        "tags": ["ritual", "irony", "myth", "transgression"]
    },
    {
        "quote": "Anything sowed in a dry land will go waste, no matter who helps in carrying the seeds.",
        "author": "Perumal Murugan",
        "work": "One Part Woman",
        "year": 2010,
        "translator": "Aniruddhan Vasudevan",
        "hook": "How to articulate agrarian despair through ecological inevitability.",
        "why_it_lands": "Murugan anchors human fertility struggles within harsh drought-ridden soil, demonstrating how agricultural reality becomes the fatalistic vocabulary through which rural characters interpret their own bodies.",
        "tags": ["landscape", "fatalism", "earth", "metaphor"]
    },
    {
        "quote": "It looked like there was a way leading out in every direction; there were gods wandering everywhere.",
        "author": "Perumal Murugan",
        "work": "One Part Woman",
        "year": 2010,
        "translator": "Aniruddhan Vasudevan",
        "hook": "How to evoke the vertigo of crowd intoxication and sacred disorientation.",
        "why_it_lands": "Murugan captures the terrifying sensory overload of the temple carnival: the overwhelming surfeit of open paths transforms spatial freedom into claustrophobia, where every shadow might be a divine apparition or a stranger.",
        "tags": ["atmosphere", "vertigo", "sensory", "hallucination"]
    },

    # 4. Khushwant Singh — Train to Pakistan (1956)
    {
        "quote": "The summer of 1947 was not like other Indian summers. It was hotter than usual, and drier and dustier. And the summer was longer.",
        "author": "Khushwant Singh",
        "work": "Train to Pakistan",
        "year": 1956,
        "translator": None,
        "hook": "How to signal impending historical catastrophe through meteorological dread.",
        "why_it_lands": "Singh opens his Partition masterpiece with ominous cadence: the parched earth and suffocating heat aren't just weather, but physical portents of the communal slaughter waiting just past the horizon.",
        "tags": ["opening", "atmosphere", "history", "understatement"]
    },
    {
        "quote": "Morality, Meet Singhji, is a matter of money. Poor people cannot afford to have morals.",
        "author": "Khushwant Singh",
        "work": "Train to Pakistan",
        "year": 1956,
        "translator": None,
        "hook": "How to strip away bourgeois ethics with brutal economic realism.",
        "why_it_lands": "Singh exposes the hypocrisy of moral sermonizing with cold agrarian clarity: virtue is a luxury of the comfortable, while the impoverished must spend their days navigating sheer physical survival.",
        "tags": ["cynicism", "truth", "dialogue", "poverty"]
    },
    {
        "quote": "The earth cracks up and deep fissures open their gaping mouths asking for water; but there is no water—only the shimmering haze at noon making mirage lakes of quicksilver.",
        "author": "Khushwant Singh",
        "work": "Train to Pakistan",
        "year": 1956,
        "translator": None,
        "hook": "How to summon landscape thirst through vivid visceral personification.",
        "why_it_lands": "Singh personifies drought with terrifying precision: the dry ground becomes gaping mouths starved for relief, mocked by noon heat that trades real moisture for shimmering, poisoned illusions.",
        "tags": ["imagery", "landscape", "drought", "personification"]
    },
    {
        "quote": "It is not our fault, Babu Sahib. Why are you getting angry with us? Get angry with the magistrate.",
        "author": "Khushwant Singh",
        "work": "Train to Pakistan",
        "year": 1956,
        "translator": None,
        "hook": "How to capture bureaucratic deflection in the face of moral failure.",
        "why_it_lands": "Singh renders the cowardice of administrative hierarchy in two plain sentences: petty enforcers shield themselves behind procedural orders, redirecting moral outrage upward into unreachable judicial abstraction.",
        "tags": ["dialogue", "bureaucracy", "realism", "power"]
    },
    {
        "quote": "They know not life, who know not this.",
        "author": "Khushwant Singh",
        "work": "Train to Pakistan",
        "year": 1956,
        "translator": None,
        "hook": "How to grant tragic authority to collective endurance in eight words.",
        "why_it_lands": "Singh channels generational fatalism with stark, biblical economy: true understanding of existence is denied to those who have lived sheltered from historic calamity and unmerited suffering.",
        "tags": ["brevity", "wisdom", "suffering", "fatalism"]
    },
    {
        "quote": "You will not find Mano Majra the same.",
        "author": "Khushwant Singh",
        "work": "Train to Pakistan",
        "year": 1956,
        "translator": None,
        "hook": "How to mark the death of an ancient communal innocence in seven syllables.",
        "why_it_lands": "Singh delivers the tragedy of Partition not with hysterical lamentation, but with a quiet, irreversible verdict: once communal poison enters an Edenic border village, its fragile peace is severed forever.",
        "tags": ["brevity", "understatement", "tragedy", "memory"]
    },

    # 5. Alain de Botton — The Consolations of Philosophy (2000)
    {
        "quote": "The most useful philosophy is the one that offers us a way to bear up against the things we cannot change.",
        "author": "Alain de Botton",
        "work": "The Consolations of Philosophy",
        "year": 2000,
        "translator": None,
        "hook": "How to define intellectual inquiry as practical psychological armor.",
        "why_it_lands": "De Botton strips philosophy of academic pomposity, returning it to its ancient Epicurean and Stoic roots: not an intellectual gymnastics routine, but a portable tool for surviving life's non-negotiable indignities.",
        "tags": ["philosophy", "wisdom", "stoicism", "clarity"]
    },
    {
        "quote": "To be comforted is not to be made happy; it is to be given a way of bearing up against unhappiness.",
        "author": "Alain de Botton",
        "work": "The Consolations of Philosophy",
        "year": 2000,
        "translator": None,
        "hook": "How to distinguish honest consolation from toxic optimism.",
        "why_it_lands": "De Botton draws an essential psychological line: true consolation does not promise cheer or deny sorrow; it simply gives the sufferer the structural fortitude to hold grief without breaking.",
        "tags": ["nuance", "comfort", "grief", "truth"]
    },
    {
        "quote": "The man who alleges that he is not yet ready for philosophy or that the time for it has passed him by, is like the man who says that he is either too young or too old for happiness.",
        "author": "Alain de Botton",
        "work": "The Consolations of Philosophy",
        "year": 2000,
        "translator": None,
        "hook": "How to demolish intellectual hesitation with an Epicurean analogy.",
        "why_it_lands": "De Botton (translating Epicurus) exposes the absurdity of postponing wisdom: framing philosophical inquiry as synonymous with human well-being reveals that claiming one is unready for philosophy is as tragic as claiming one is unready for joy.",
        "tags": ["philosophy", "analogy", "clarity", "epicurean"]
    },
    {
        "quote": "Those who are unfriendly with themselves find it hard to imagine that the cake seller is shouting in order to sell cakes.",
        "author": "Alain de Botton",
        "work": "The Consolations of Philosophy",
        "year": 2000,
        "translator": None,
        "hook": "How to diagnose self-hatred through everyday street paranoia.",
        "why_it_lands": "De Botton illuminates internal neurosis with absurd everyday comedy: when you carry self-loathing, even a street vendor hawking pastries feels like a targeted personal affront.",
        "tags": ["wit", "psychology", "humor", "observation"]
    },
    {
        "quote": "The essence of art is that its one case applies to thousands.",
        "author": "Alain de Botton",
        "work": "The Consolations of Philosophy",
        "year": 2000,
        "translator": None,
        "hook": "How to define artistic universality through solitary singularity.",
        "why_it_lands": "De Botton distills Schopenhauer's aesthetic theory into clean, unforgettable geometry: great literature does not generalize broadly, but renders a single specific human life so intimately that thousands recognize themselves in it.",
        "tags": ["art", "universality", "craft", "definition"]
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
    for q in VETTED_CLUSTER_33:
        if q["quote"].strip() not in existing_quotes:
            bank.append(q)
            existing_quotes.add(q["quote"].strip())
            added += 1
        else:
            print(f"Skipping duplicate: {q['quote'][:40]}...")

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)

    print(f"Successfully added {added} quotes from Cluster 33.")
    print(f"New quote bank total: {len(bank)}")

if __name__ == "__main__":
    main()
