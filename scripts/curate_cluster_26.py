# scripts/curate_cluster_26.py — Curates 20 craft quotes from Cluster 26 (Mythic Individuation, Emotion & Broken Earths)
# Usage: python3 scripts/curate_cluster_26.py
# Requires: json, os

import json
import os

QUOTE_BANK_PATH = "content/quote-bank.json"

VETTED_CLUSTER_26 = [
    # 1. Sohn Won-pyung — Almond (2017)
    {
        "quote": "‘He could die,’ I said, fiddling with one of the chewy caramel packs neatly lined up on the display stand.",
        "author": "Sohn Won-pyung",
        "work": "Almond",
        "year": 2017,
        "translator": "Sandy Joosun Lee",
        "hook": "How to depict cognitive detachment by juxtaposing mortality with banal candy packaging.",
        "why_it_lands": "Sohn captures clinical alexithymia through tactile dissonance: the narrator states a lethal reality with zero vocal inflection while idly straightening rows of caramel in a convenience store.",
        "tags": ["understatement", "sensory", "characterization", "interiority"]
    },
    {
        "quote": "Books don't get angry. They don't shout or change their minds depending on their mood. They just wait quietly for you to open them.",
        "author": "Sohn Won-pyung",
        "work": "Almond",
        "year": 2017,
        "translator": "Sandy Joosun Lee",
        "hook": "How to contrast interpersonal volatility against the serene constancy of print.",
        "why_it_lands": "Sohn contrasts the unpredictable, threatening weather of human mood swings against the patient, loyal silence of bound paper, turning reading into a sensory sanctuary.",
        "tags": ["books", "solitude", "contrast", "sensory"]
    },
    {
        "quote": "They had been my whole universe. But now that they were gone, I began to learn that there were others in this world.",
        "author": "Sohn Won-pyung",
        "work": "Almond",
        "year": 2017,
        "translator": "Sandy Joosun Lee",
        "hook": "How to measure the painful expansion of consciousness after catastrophic loss.",
        "why_it_lands": "Sohn moves with devastating quietness from the intimate sanctuary of a two-person family into the blinding, indifferent light of a wider society that must now be endured.",
        "tags": ["grief", "perspective", "growth", "understatement"]
    },
    {
        "quote": "My grandmother called me a monster. But she said it while holding me so tightly my ribs hurt.",
        "author": "Sohn Won-pyung",
        "work": "Almond",
        "year": 2017,
        "translator": "Sandy Joosun Lee",
        "hook": "How to juxtapose linguistic severity against protective physical devotion.",
        "why_it_lands": "Sohn creates a sharp somatic contradiction: the verbal insult is utterly demolished by the bone-crushing pressure of an embrace, revealing how love often disguises itself in defensive barbs.",
        "tags": ["contradiction", "sensory", "dialogue", "pathos"]
    },

    # 2. Richard Adams — Watership Down (1972)
    {
        "quote": "‘Like trees in November,’ he said, ‘they were standing still, but they weren’t dead.’",
        "author": "Richard Adams",
        "work": "Watership Down",
        "year": 1972,
        "translator": None,
        "hook": "How to convey trauma-induced paralysis through autumnal landscape imagery.",
        "why_it_lands": "Adams uses an evocative seasonal simile to distinguish between dormant emotional shock and literal death, capturing how living creatures freeze when overwhelmed by terror.",
        "tags": ["imagery", "simile", "trauma", "nature"]
    },
    {
        "quote": "All the world will be your enemy, Prince with a Thousand Enemies, and whenever they catch you, they will kill you. But first they must catch you.",
        "author": "Richard Adams",
        "work": "Watership Down",
        "year": 1972,
        "translator": None,
        "hook": "How to forge mythic defiance from total physical vulnerability.",
        "why_it_lands": "Adams builds an epic mythic cadence by conceding absolute physical vulnerability, only to flip the entire balance of power with a legendary, six-word conditional punchline.",
        "tags": ["myth", "courage", "rhythm", "resilience"]
    },
    {
        "quote": "‘Risk is risk. Don’t you want to get out and come and live on the high downs with us? Think of it!’",
        "author": "Richard Adams",
        "work": "Watership Down",
        "year": 1972,
        "translator": None,
        "hook": "How to strip subterranean safety of its moral virtue through the appeal of wind and sky.",
        "why_it_lands": "Adams uses a bare tautological shrug ('Risk is risk') to sweep aside institutional anxiety, trading the stale safety of the burrow for the perilous exhilaration of open horizon.",
        "tags": ["freedom", "voice", "courage", "dialogue"]
    },
    {
        "quote": "Animals don't behave like men. If they have to fight, they fight; and if they have to kill, they kill. But they don't sit down and set their wits to work to invent ways of ruining other creatures' lives.",
        "author": "Richard Adams",
        "work": "Watership Down",
        "year": 1972,
        "translator": None,
        "hook": "How to indict human malice by contrasting it with instinctive creaturely survival.",
        "why_it_lands": "Adams separates clean, necessary biological violence from the sadistic intellectual ingenuity of humans, who alone weaponize leisure to manufacture torment.",
        "tags": ["candor", "satire", "instinct", "philosophy"]
    },

    # 3. Hermann Hesse — Demian (1919)
    {
        "quote": "Nothing in the world is more distasteful to a man than to take the path that leads to himself.",
        "author": "Hermann Hesse",
        "work": "Demian",
        "year": 1919,
        "translator": "Michael Roloff & Michael Lebeck",
        "hook": "How to expose the universal terror of genuine psychological individuation.",
        "why_it_lands": "Hesse inverts the romantic cliché of self-discovery, defining the honest descent into one's own shadow as the single most repulsive and avoided chore in human existence.",
        "tags": ["psychology", "candor", "individuation", "clarity"]
    },
    {
        "quote": "Clever talk is absolutely worthless. All you do in the process is lose yourself. And to lose yourself is a sin.",
        "author": "Hermann Hesse",
        "work": "Demian",
        "year": 1919,
        "translator": "Michael Roloff & Michael Lebeck",
        "hook": "How to strip verbal cleverness of its social prestige in three short strokes.",
        "why_it_lands": "Hesse cuts through intellectual posturing with monastic bluntness, declaring that articulate exhibitionism is not intelligence, but a cowardly flight from inner presence.",
        "tags": ["brevity", "candor", "discipline", "authenticity"]
    },
    {
        "quote": "They know exactly how many ounces of powder it takes to kill a man, but they don't know how to pray to God, they don't even know how to be happy for a single contented hour.",
        "author": "Hermann Hesse",
        "work": "Demian",
        "year": 1919,
        "translator": "Michael Roloff & Michael Lebeck",
        "hook": "How to contrast ballistic industrial precision with spiritual bankruptcy.",
        "why_it_lands": "Hesse balances exact mechanical measurement ('how many ounces of powder') against spiritual helplessness, demonstrating that technological mastery often masks emotional destitution.",
        "tags": ["antithesis", "critique", "rhythm", "morality"]
    },
    {
        "quote": "The bird fights its way out of the egg. The egg is the world. Who would be born must first destroy a world.",
        "author": "Hermann Hesse",
        "work": "Demian",
        "year": 1919,
        "translator": "Michael Roloff & Michael Lebeck",
        "hook": "How to dramatize spiritual emergence as a cosmic catastrophe.",
        "why_it_lands": "Hesse crafts an unyielding mythological syllogism: genuine transformation is not peaceful accretion, but the violent demolition of the inherited shelter that previously kept you safe.",
        "tags": ["metaphor", "myth", "rebirth", "transformation"]
    },

    # 4. N. K. Jemisin — The Fifth Season (2015)
    {
        "quote": "You are lightning, dangerous unless captured in wires.",
        "author": "N. K. Jemisin",
        "work": "The Fifth Season",
        "year": 2015,
        "translator": None,
        "hook": "How to dehumanize marginalized power as an elemental industrial utility.",
        "why_it_lands": "Jemisin reduces an autonomous person to raw electrical wattage, demonstrating how an imperial culture justifies enslaving gifted bodies under the guise of public safety.",
        "tags": ["brevity", "metaphor", "power", "oppression"]
    },
    {
        "quote": "‘You think that matters?’ He jerks his head toward the body of the abused, murdered child. ‘The only reason they don’t do this to all of us is because we’re more versatile, more useful, if we control ourselves.’",
        "author": "N. K. Jemisin",
        "work": "The Fifth Season",
        "year": 2015,
        "translator": None,
        "hook": "How to strip an oppressive truce of its humanitarian illusions.",
        "why_it_lands": "Jemisin articulates the brutal economic arithmetic of oppression: safety for the subjugated is never a moral right, only a temporary concession granted for self-policed labor.",
        "tags": ["candor", "dialogue", "power", "cynicism"]
    },
    {
        "quote": "‘It’s safe to love you. You won’t fail me. You won’t die. And I know the price up front.’",
        "author": "N. K. Jemisin",
        "work": "The Fifth Season",
        "year": 2015,
        "translator": None,
        "hook": "How to negotiate emotional safety through transactional defense mechanisms.",
        "why_it_lands": "Jemisin shows how intergenerational trauma converts love into an actuarial insurance policy, demanding guaranteed survival and upfront costs before allowing attachment.",
        "tags": ["dialogue", "trauma", "vulnerability", "pathos"]
    },
    {
        "quote": "Let's start with the end of the world, why don't we? Get it over with and move on to more interesting things.",
        "author": "N. K. Jemisin",
        "work": "The Fifth Season",
        "year": 2015,
        "translator": None,
        "hook": "How to bypass apocalyptic spectacle with weary, second-person flippancy.",
        "why_it_lands": "Jemisin shatters standard epic opening conventions by treating planetary destruction not as a climactic fireworks show, but as an administrative hurdle to brush past.",
        "tags": ["voice", "opening", "subversion", "irony"]
    },

    # 5. Joseph Campbell — The Power of Myth (1988)
    {
        "quote": "If your private myth, your dream, happens to coincide with that of the society, you are in good accord with your group. If it isn't, you've got an adventure in the dark forest ahead of you.",
        "author": "Joseph Campbell",
        "work": "The Power of Myth",
        "year": 1988,
        "translator": None,
        "hook": "How to reframe social estrangement as an archetypal heroic journey.",
        "why_it_lands": "Campbell uses parallel conditional clauses to reclassify psychological alienation away from clinical pathology, elevating loneliness into the classic heroic descent into the dark wood.",
        "tags": ["myth", "individuation", "solitude", "perspective"]
    },
    {
        "quote": "Love thine enemies because they are the instruments of your destiny.",
        "author": "Joseph Campbell",
        "work": "The Power of Myth",
        "year": 1988,
        "translator": None,
        "hook": "How to elevate adversaries into the unwitting architects of character.",
        "why_it_lands": "Campbell offers a metaphysical twist on the Christian commandment, arguing that our bitterest opponents are not evils to defeat, but the exact abrasive friction required to forge identity.",
        "tags": ["philosophy", "adversity", "insight", "brevity"]
    },
    {
        "quote": "Religion is a defense against the experience of God.",
        "author": "Joseph Campbell",
        "work": "The Power of Myth",
        "year": 1988,
        "translator": None,
        "hook": "How to indict clerical dogma as a shield against authentic revelation.",
        "why_it_lands": "Campbell quotes Jung to deliver an eight-word paradox, arguing that codified ritual and institutional doctrine exist primarily to protect worshippers from the unmediated, terrifying sacred.",
        "tags": ["paradox", "brevity", "religion", "candor"]
    },
    {
        "quote": "Desire is the bait, death is the hook. Adam and Eve were moved; the Buddha was not.",
        "author": "Joseph Campbell",
        "work": "The Power of Myth",
        "year": 1988,
        "translator": None,
        "hook": "How to compress the entire mythological history of temptation into two parallel clauses.",
        "why_it_lands": "Campbell pairs a visceral fishing metaphor with a swift comparative contrast, juxtaposing the tragedy of Western fallenness against the serene immobility of Eastern enlightenment.",
        "tags": ["metaphor", "contrast", "rhythm", "myth"]
    }
]

def main():
    with open(QUOTE_BANK_PATH, "r", encoding="utf-8") as f:
        existing = json.load(f)

    existing_quotes = {q["quote"].strip() for q in existing}
    added = 0

    for item in VETTED_CLUSTER_26:
        if item["quote"].strip() not in existing_quotes:
            existing.append(item)
            existing_quotes.add(item["quote"].strip())
            added += 1

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"Successfully added {added} vetted quotes from Cluster 26.")
    print(f"Total quotes in bank: {len(existing)}")

if __name__ == "__main__":
    main()
