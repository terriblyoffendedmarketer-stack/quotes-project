# scripts/curate_cluster_31.py — Curates 20 craft quotes from Cluster 31 (Underground Spite, Default Settings & Soul Transit)
# Usage: python3 scripts/curate_cluster_31.py
# Requires: json, os

import json
import os

QUOTE_BANK_PATH = "content/quote-bank.json"

VETTED_CLUSTER_31 = [
    # 1. Fyodor Dostoevsky — Notes from Underground (1864)
    {
        "quote": "Come on, gentlemen, why shouldn’t we get rid of all this calm reasonableness with one kick, just so as to send all these logarithms to the devil and be able to live our own lives at our own sweet will?",
        "author": "Fyodor Dostoevsky",
        "work": "Notes from Underground",
        "year": 1864,
        "translator": "Richard Pevear and Larissa Volokhonsky",
        "hook": "How to unleash irrational human will against utilitarian logic.",
        "why_it_lands": "Dostoevsky's narrator revolts against scientific determinism with visceral spite, arguing that human beings will deliberately smash perfection just to prove their freedom is more than mathematical formula.",
        "tags": ["rebellion", "philosophy", "freedom", "voice"]
    },
    {
        "quote": "To be overly conscious is a sickness, a real, thorough sickness. For human everyday life, ordinary human consciousness would be more than enough.",
        "author": "Fyodor Dostoevsky",
        "work": "Notes from Underground",
        "year": 1864,
        "translator": "Richard Pevear and Larissa Volokhonsky",
        "hook": "How to diagnose excessive self-awareness as a debilitating disease.",
        "why_it_lands": "Dostoevsky inverts the enlightenment ideal of self-knowledge, demonstrating that hyper-reflective analytical intelligence can paralyze moral action and trap the thinker in agonizing spite.",
        "tags": ["psychology", "consciousness", "existential", "paradox"]
    },
    {
        "quote": "Everything always ended happily, however, with a lazy and entrancing transition to art; that is, to beautiful ready-made images of life, forcibly wrenched from poets and novelists and adapted to every possible kind of service and requirement.",
        "author": "Fyodor Dostoevsky",
        "work": "Notes from Underground",
        "year": 1864,
        "translator": "Richard Pevear and Larissa Volokhonsky",
        "hook": "How to satirize romantic escapism as intellectual self-sedation.",
        "why_it_lands": "Dostoevsky mocks the literary daydreamer who retreats from humiliating reality by dressing petty vanity in second-hand poetic tropes borrowed from European melodrama.",
        "tags": ["satire", "irony", "literature", "vanity"]
    },
    {
        "quote": "You give yourself and your own will up completely. And afterwards, if you want to break those chains, it will be too late; the shackles will get stronger and stronger.",
        "author": "Fyodor Dostoevsky",
        "work": "Notes from Underground",
        "year": 1864,
        "translator": "Richard Pevear and Larissa Volokhonsky",
        "hook": "How to chart the silent compounding of voluntary servitude.",
        "why_it_lands": "Dostoevsky warns against small moral surrenders: giving away sovereignty seems convenient at first, but habits calcify into immovable psychic prisons.",
        "tags": ["will", "warning", "insight", "restraint"]
    },

    # 2. David Foster Wallace — This Is Water (2005)
    {
        "quote": "There are these two young fish swimming along and they happen to meet an older fish swimming the other way, who nods at them and says 'Morning, boys. How's the water?' And the two young fish swim on for a bit, and then eventually one of them looks over at the other and goes 'What the hell is water?'",
        "author": "David Foster Wallace",
        "work": "This Is Water",
        "year": 2005,
        "translator": None,
        "hook": "How to expose invisible default realities through a brief comic parable.",
        "why_it_lands": "Wallace uses an unassuming folk dialogue to introduce his central theme: the most obvious, ubiquitous, and crucial realities in adult life are often the ones hardest to see and talk about.",
        "tags": ["parable", "humor", "attention", "opening"]
    },
    {
        "quote": "The really significant education in thinking that we’re supposed to get in a place like this isn’t really about the capacity to think, but rather about the choice of what to think about.",
        "author": "David Foster Wallace",
        "work": "This Is Water",
        "year": 2005,
        "translator": None,
        "hook": "How to redefine intellectual maturity through attentional sovereignty.",
        "why_it_lands": "Wallace separates intellect from agency: intelligence is merely horsepower, but freedom lies in consciously choosing where to aim that horsepower instead of running on automatic default settings.",
        "tags": ["mind", "attention", "education", "clarity"]
    },
    {
        "quote": "The point is that petty, frustrating crap like this is exactly where the work of choosing comes in.",
        "author": "David Foster Wallace",
        "work": "This Is Water",
        "year": 2005,
        "translator": None,
        "hook": "How to locate existential labor within mundane domestic irritation.",
        "why_it_lands": "Wallace refuses lofty abstract philosophy, demonstrating that real spiritual work happens not on mountaintops, but in supermarket checkout lines and crowded evening traffic jams.",
        "tags": ["voice", "reality", "mind", "everyday"]
    },
    {
        "quote": "The really important kind of freedom involves attention, and awareness, and discipline, and effort, and being able truly to care about other people and to sacrifice for them, over and over, in myriad petty little unsexy ways, every day.",
        "author": "David Foster Wallace",
        "work": "This Is Water",
        "year": 2005,
        "translator": None,
        "hook": "How to build rhythmic accumulative cadence toward ordinary moral heroism.",
        "why_it_lands": "Wallace stacks polysyndetic conjunctions ('and awareness, and discipline, and effort') to strip freedom of Hollywood glamour, grounding genuine love in relentless, unglamorous daily devotion.",
        "tags": ["cadence", "rhythm", "love", "discipline"]
    },

    # 3. E.M. Forster — The Machine Stops (1909)
    {
        "quote": "Cannot you see, cannot all you lecturers see, that it is we that are dying, and that down here the only thing that really lives is the Machine?",
        "author": "E.M. Forster",
        "work": "The Machine Stops",
        "year": 1909,
        "translator": None,
        "hook": "How to confront institutional delusion with urgent rhetorical despair.",
        "why_it_lands": "Forster delivers a terrifying early 20th-century warning against technocratic complacency, exposing how an increasingly automated civilization slowly surrenders its vital biological spark to its apparatus.",
        "tags": ["dystopia", "dialogue", "technology", "voice"]
    },
    {
        "quote": "The Machine develops - but not on our lies. The Machine proceeds - but not to our goal.",
        "author": "E.M. Forster",
        "work": "The Machine Stops",
        "year": 1909,
        "translator": None,
        "hook": "How to articulate algorithmic divergence through antithetical parallelism.",
        "why_it_lands": "Forster captures technological drift in two balanced clauses, showing that systems built by human hands eventually evolve an autonomous momentum indifferent to human intention.",
        "tags": ["parallelism", "technology", "brevity", "systems"]
    },
    {
        "quote": "‘Beware of first-hand ideas!’ exclaimed one of the most advanced of them. ‘First-hand ideas do not really exist. They are but the physical impressions produced by love and fear, and on this gross foundation who could erect a philosophy?’",
        "author": "E.M. Forster",
        "work": "The Machine Stops",
        "year": 1909,
        "translator": None,
        "hook": "How to satirize intellectual detachment through inverted epistemic virtue.",
        "why_it_lands": "Forster skewers academic abstraction by having intellectuals celebrate second-hand commentary over raw lived experience, eerily predicting our digitized retreat from physical contact.",
        "tags": ["satire", "philosophy", "irony", "ideas"]
    },
    {
        "quote": "The Machine feeds us and clothes us and houses us; through it we speak to one another, through it we see one another, in it we have our being. The Machine is the friend of ideas and the enemy of superstition: the Machine is omnipotent, eternal; blessed is the Machine.",
        "author": "E.M. Forster",
        "work": "The Machine Stops",
        "year": 1909,
        "translator": None,
        "hook": "How to mimic liturgical rhythm to expose technological idolatry.",
        "why_it_lands": "Forster borrows biblical cadence and liturgical praise to show how algorithmic convenience inevitably becomes a religious cult that demands total spiritual submission.",
        "tags": ["rhythm", "satire", "technology", "dystopia"]
    },

    # 4. James Hollis — The Middle Passage: From Misery to Meaning in Midlife (1993)
    {
        "quote": "When we discover that we have been living what constitutes a false self, that we have been enacting a provisional adulthood, driven by unrealistic expectations, then we open the possibility for the second adulthood, our true personhood.",
        "author": "James Hollis",
        "work": "The Middle Passage: From Misery to Meaning in Midlife",
        "year": 1993,
        "translator": None,
        "hook": "How to reframe midlife crisis as an overdue birth of true personhood.",
        "why_it_lands": "Hollis strips midlife distress of pathetic cliché, reframing the collapse of early adult identity not as failure, but as the painful and necessary demolition of a provisional borrowed costume.",
        "tags": ["psychology", "growth", "identity", "insight"]
    },
    {
        "quote": "Few at the altar are conscious of the enormity of their expectations. No one would speak aloud the immense hopes: 'I am counting on you to make my life meaningful. I am counting on you to always be there for me. I am counting on you to read my mind and anticipate all my needs. I am counting on you to bind my wounds and fulfill the deficits of my life.'",
        "author": "James Hollis",
        "work": "The Middle Passage: From Misery to Meaning in Midlife",
        "year": 1993,
        "translator": None,
        "hook": "How to unmask romantic fantasy by voicing unconscious projections.",
        "why_it_lands": "Hollis articulates the hidden, impossible emotional contracts of modern marriage, demonstrating that demanding another person heal our existential voids inevitably crushes the bond.",
        "tags": ["relationships", "psychology", "honesty", "truth"]
    },
    {
        "quote": "By midlife the injury and neglect to the soul may be such that parts of the psyche strenuously resist further insult. This resistance manifests in symptoms.",
        "author": "James Hollis",
        "work": "The Middle Passage: From Misery to Meaning in Midlife",
        "year": 1993,
        "translator": None,
        "hook": "How to reinterpret psychological symptoms as self-protective psychic rebellions.",
        "why_it_lands": "Hollis reframes neurosis, depression, and anxiety: far from mere chemical malfunctions, they are the psyche's emergency immune response resisting continued self-betrayal.",
        "tags": ["healing", "psychology", "mind", "perspective"]
    },
    {
        "quote": "Our vocation is seldom a straight path, but a series of unfolding tackings and turnings.",
        "author": "James Hollis",
        "work": "The Middle Passage: From Misery to Meaning in Midlife",
        "year": 1993,
        "translator": None,
        "hook": "How to describe vocation through maritime nautical metaphor.",
        "why_it_lands": "Hollis uses the sailing concept of tacking against headwinds to normalize career wandering, showing that life directions reveal themselves only through zigzagging course corrections.",
        "tags": ["metaphor", "calling", "brevity", "reassurance"]
    },

    # 5. Elif Shafak — The Forty Rules of Love (2009)
    {
        "quote": "When a true lover of God goes into a tavern, the tavern becomes his chamber of prayer, but when a wine bibber goes into the same chamber, it becomes his tavern. In everything we do, it is our hearts that make the difference, not our outer appearances.",
        "author": "Elif Shafak",
        "work": "The Forty Rules of Love",
        "year": 2009,
        "translator": None,
        "hook": "How to demolish puritanical sanctimony through inverted sacred space.",
        "why_it_lands": "Shafak uses Shams of Tabriz's Sufi parable to show that sanctity resides neither in buildings nor in orthodox rituals, but in the inner intention and purity brought by the observer.",
        "tags": ["parable", "sufism", "insight", "spirituality"]
    },
    {
        "quote": "One man’s pain will hurt us all. One man’s joy will make everyone smile.",
        "author": "Elif Shafak",
        "work": "The Forty Rules of Love",
        "year": 2009,
        "translator": None,
        "hook": "How to affirm universal interconnection through balanced symmetrical phrasing.",
        "why_it_lands": "Shafak sets suffering and joy in perfect parallel symmetry, reminding the reader of the unbroken nervous system that binds human consciousness together.",
        "tags": ["compassion", "brevity", "parallelism", "wisdom"]
    },
    {
        "quote": "If you want to strengthen your faith, you will need to soften inside. For your faith to be rock solid, your heart needs to be as soft as a feather.",
        "author": "Elif Shafak",
        "work": "The Forty Rules of Love",
        "year": 2009,
        "translator": None,
        "hook": "How to reconcile spiritual strength with emotional softness.",
        "why_it_lands": "Shafak inverts rigid dogmatism through tactile contrast: enduring faith is not a brittle, armored fortress, but an elastic and vulnerable softness that bends without breaking.",
        "tags": ["paradox", "faith", "contrast", "softness"]
    },
    {
        "quote": "Whatever we received from the skies, we passed on to the earth, from God to people. Each and every one of us became a link connecting the Lover to the Beloved.",
        "author": "Elif Shafak",
        "work": "The Forty Rules of Love",
        "year": 2009,
        "translator": None,
        "hook": "How to evoke the devotional whirling dance as a conduit between heaven and earth.",
        "why_it_lands": "Shafak evokes the choreography of Rumi's whirling dervishes, transforming human existence into a dynamic conduit whose sole duty is to transmit grace downward without retaining it.",
        "tags": ["dance", "sufism", "rhythm", "transcendence"]
    }
]

def main():
    if not os.path.exists(QUOTE_BANK_PATH):
        print(f"Error: {QUOTE_BANK_PATH} not found.")
        return

    with open(QUOTE_BANK_PATH, "r", encoding="utf-8") as f:
        bank = json.load(f)

    existing_quotes = set(q["quote"].strip() for q in bank)
    added_count = 0

    for item in VETTED_CLUSTER_31:
        if item["quote"].strip() not in existing_quotes:
            bank.append(item)
            existing_quotes.add(item["quote"].strip())
            added_count += 1
        else:
            print(f"Duplicate found, skipping: {item['quote'][:40]}...")

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)

    print(f"Successfully added {added_count} vetted quotes from Cluster 31.")
    print(f"New total quote bank size: {len(bank)}")

if __name__ == "__main__":
    main()
