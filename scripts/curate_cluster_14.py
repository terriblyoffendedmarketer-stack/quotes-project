#!/usr/bin/env python3
"""
curate_cluster_14.py — Curates 20 vetted quotes from Cluster 14 (Myth, Memory & The Shadow Self)
into content/quote-bank.json.
"""

import json
from pathlib import Path

QUOTE_BANK_PATH = Path("/Users/apple/Documents/Claude Code/quotes-project/content/quote-bank.json")

NEW_QUOTES = [
    # C. G. Jung — Memories, Dreams, Reflections
    {
        "quote": "Something within me has been touched. A gradient has formed, and I must write.",
        "author": "C. G. Jung",
        "work": "Memories, Dreams, Reflections",
        "year": 1961,
        "translator": "Richard & Clara Winston",
        "hook": "How to articulate creative compulsion through physical topography.",
        "why_it_lands": "Jung frames inspiration not as mystical muse, but as hydrological physics: an emotional slope ('a gradient') down which psychic energy must inevitably pour. The compulsion to write becomes a natural law rather than an act of vanity.",
        "tags": ["metaphor", "creativity", "interiority", "craft-rule"]
    },
    {
        "quote": "I felt positively relieved when I had actually done something wrong. Then at least I knew what my guilty conscience was for.",
        "author": "C. G. Jung",
        "work": "Memories, Dreams, Reflections",
        "year": 1961,
        "translator": "Richard & Clara Winston",
        "hook": "How to invert neurotic guilt with psychological relief.",
        "why_it_lands": "A brilliant psychological reversal: the child’s diffuse, free-floating anxiety is harder to bear than actual censure. Transgression is welcomed because it finally provides an external alibi for an internal torment.",
        "tags": ["paradox", "psychology", "inversion", "insight"]
    },
    {
        "quote": "‘Anyone who takes the sure road is as good as dead. Then nothing happens any longer at any rate, not the right things.’",
        "author": "C. G. Jung",
        "work": "Memories, Dreams, Reflections",
        "year": 1961,
        "translator": "Richard & Clara Winston",
        "hook": "How to warn against certainty as spiritual atrophy.",
        "why_it_lands": "Jung equates predictability with psychic death. The blunt colloquialism ('as good as dead') cuts through clinical neutrality, declaring that life only occurs where safe paths are abandoned.",
        "tags": ["aphorism", "urgency", "stoicism", "boldness"]
    },
    {
        "quote": "‘They say that they think with their heads,’ he replied. ‘Why of course. What do you think with?’ I asked him in surprise. ‘We think here,’ he said, indicating his heart.",
        "author": "C. G. Jung",
        "work": "Memories, Dreams, Reflections",
        "year": 1961,
        "translator": "Richard & Clara Winston",
        "hook": "How to dramatize epistemological divergence in dialogue.",
        "why_it_lands": "A Pueblo elder quietly overturns Western rationalism with a single physical gesture. The dialogue leaves the Western observer’s intellectual confidence stranded, exposing the cultural provincialism of head-centered intellect.",
        "tags": ["dialogue", "contrast", "mythology", "perspective"]
    },

    # Hermann Hesse — Demian
    {
        "quote": "I was glad when my father took me to task for my muddy boots. It diverted his attention by sidestepping the real issue and placed me in a position to endure reproaches that I could secretly transfer to the other, the more serious offense.",
        "author": "Hermann Hesse",
        "work": "Demian",
        "year": 1919,
        "translator": "Michael Roloff & Michael Lebeck",
        "hook": "How to endure minor domestic punishment as cover for deeper guilt.",
        "why_it_lands": "Hesse reveals the transactional economy of childhood guilt. Enduring an unjust scolding for muddy shoes is embraced as a bargain that conceals the unspeakable shadow transgression underneath.",
        "tags": ["psychology", "interiority", "childhood", "deception"]
    },
    {
        "quote": "‘If you want something from someone and you look him firmly in both eyes and he doesn’t become ill at ease, give up. You don’t have a chance, ever!’",
        "author": "Hermann Hesse",
        "work": "Demian",
        "year": 1919,
        "translator": "Michael Roloff & Michael Lebeck",
        "hook": "How to formulate an ironclad diagnostic of interpersonal resolve.",
        "why_it_lands": "Demian offers an operational rule of psychological combat. By linking eye contact directly to inner equilibrium, the line strips away social pleasantry to reveal raw sovereignty of will.",
        "tags": ["character-voice", "aphorism", "power", "directness"]
    },
    {
        "quote": "‘Fire worship was by no means the most foolish thing ever invented,’ he murmured to himself at one point.",
        "author": "Hermann Hesse",
        "work": "Demian",
        "year": 1919,
        "translator": "Michael Roloff & Michael Lebeck",
        "hook": "How to rehabilitate ancient primal rites through quiet musing.",
        "why_it_lands": "The litotes ('by no means the most foolish thing') rescues pagan elemental reverence from modern condescension. A muttered aside carries more philosophical gravity than an academic treatise.",
        "tags": ["understatement", "mythology", "philosophy", "voice"]
    },
    {
        "quote": "‘It is true of Moses and Buddha, of Napoleon and Bismarck. What particular movement one serves and what pole one is directed from are matters outside one's own choice.’",
        "author": "Hermann Hesse",
        "work": "Demian",
        "year": 1919,
        "translator": "Michael Roloff & Michael Lebeck",
        "hook": "How to decouple historical agency from individual intent.",
        "why_it_lands": "Hesse pairs religious founders with ruthless statesmen to demonstrate the indifference of destiny. Personal ambition is unmasked as merely the physical conduit for larger archetypal forces.",
        "tags": ["cadence", "fate", "history", "perspective"]
    },

    # Pat Conroy — The Prince of Tides
    {
        "quote": "My wound is geography. It is also my anchorage, my port of call.",
        "author": "Pat Conroy",
        "work": "The Prince of Tides",
        "year": 1986,
        "translator": None,
        "hook": "How to establish origin as both trauma and identity.",
        "why_it_lands": "Conroy opens with one of modern fiction’s greatest inversions: the place that injured the narrator is the identical port that keeps him anchored. Trauma and home are fused into a single maritime metaphor.",
        "tags": ["metaphor", "opening", "geography", "cadence"]
    },
    {
        "quote": "‘I pray to him to make you die,’ the priest explained. ‘Then I feel much shame. And I pray for you to live. A priest should only pray for life. It is a great sin.’",
        "author": "Pat Conroy",
        "work": "The Prince of Tides",
        "year": 1986,
        "translator": None,
        "hook": "How to dramatize spiritual conflict through forbidden confession.",
        "why_it_lands": "A priest confesses his murderous resentment without defensive rationalization. The rapid oscillation between wishing death and praying for life exposes the raw human frailty beneath clerical sanctity.",
        "tags": ["dialogue", "vulnerability", "confession", "contrast"]
    },
    {
        "quote": "He’s a greatly misunderstood man, Mom,” she said. “I think he’s very well understood, Mom,” I said.",
        "author": "Pat Conroy",
        "work": "The Prince of Tides",
        "year": 1986,
        "translator": None,
        "hook": "How to expose familial denial through symmetrical dialogue.",
        "why_it_lands": "Conroy achieves lethal comedic and dramatic contrast through a single repeated phrase. By echoing the sister's defense with a calm, inverted qualifier, the brother shatters a lifetime of excuse-making.",
        "tags": ["dialogue", "symmetry", "family", "subversion"]
    },
    {
        "quote": "In my family there were no clear lines between love and hate, cruelty and compassion.",
        "author": "Pat Conroy",
        "work": "The Prince of Tides",
        "year": 1986,
        "translator": None,
        "hook": "How to capture domestic ambivalence through paired opposites.",
        "why_it_lands": "Conroy diagnoses familial dysfunction by erasing the moral boundaries that separate tenderness from violence. The clean binary pairings convey decades of emotional entanglement in twelve words.",
        "tags": ["contrast", "family", "simplicity", "cadence"]
    },

    # Yann Martel — The Facts Behind the Helsinki Roccamatios
    {
        "quote": "‘The emotion in question is not the point; be it love, envy or apathy, so long as it is conveyed in a convincing manner, then the story will come alive.’",
        "author": "Yann Martel",
        "work": "The Facts Behind the Helsinki Roccamatios",
        "year": 1993,
        "translator": None,
        "hook": "How to locate narrative vitality in conviction rather than sentiment.",
        "why_it_lands": "Martel strips aesthetic power of moral purity. It is not noble sentiment that animates fiction, but the technical rigor of convincing delivery; even apathy, rendered with absolute fidelity, will catch fire.",
        "tags": ["craft-rule", "storytelling", "conviction", "insight"]
    },
    {
        "quote": "Time is on your side.” Fuck.",
        "author": "Yann Martel",
        "work": "The Facts Behind the Helsinki Roccamatios",
        "year": 1993,
        "translator": None,
        "hook": "How to puncture comforting platitudes with a single obscenity.",
        "why_it_lands": "Martel places the hollow optimism of a medical cliche against the abrupt, monosyllabic profanity of a dying friend. The jarring typographic contrast destroys false solace on contact.",
        "tags": ["contrast", "brevity", "grief", "defiance"]
    },
    {
        "quote": "It’s strangely moving. The earth yields to a great wedge on whose black marble walls the names of the war dead are inscribed.",
        "author": "Yann Martel",
        "work": "The Facts Behind the Helsinki Roccamatios",
        "year": 1993,
        "translator": None,
        "hook": "How to describe memorial architecture as an incision into the earth.",
        "why_it_lands": "Martel describes the Vietnam Veterans Memorial not as a monument built upward, but as a surgical wedge sliced into the ground. The earth 'yielding' gives stone the somatic vulnerability of wounded flesh.",
        "tags": ["imagery", "architecture", "memorial", "precision"]
    },
    {
        "quote": "‘It was about a young man who falls in love with a door. When a friend finds out, he destroys the door.’",
        "author": "Yann Martel",
        "work": "The Facts Behind the Helsinki Roccamatios",
        "year": 1993,
        "translator": None,
        "hook": "How to craft a surreal micro-parable on jealousy.",
        "why_it_lands": "Two sentences of fable-like simplicity. Martel replaces romantic rivals with an inanimate threshold, distilling erotic possessiveness and violent betrayal into an unforgettable surrealist snapshot.",
        "tags": ["micro-fiction", "parable", "surrealism", "brevity"]
    },

    # Ramdhari Singh Dinkar — Kurukshetra
    {
        "quote": "‘और यह मृतक शरीर जो बचा है शेष, चुप-चुप, मानो, पूछता है मुझसे पुकार- विजय का एक उपहार मैं बचा हूँ, बोलो, जीत किसकी है और किसकी हुई है हार?’\n\n('And this corpse that remains behind, silent yet crying out: I am what remains as the prize of victory—tell me, whose is the triumph, and who has been defeated?')",
        "author": "Ramdhari Singh Dinkar",
        "work": "Kurukshetra",
        "year": 1946,
        "translator": None,
        "hook": "How to question the legitimacy of victory through a silent corpse.",
        "why_it_lands": "Dinkar gives the slain soldier the ultimate moral interrogation. The silent dead body becomes the only surviving trophy of the epic war, reducing martial triumph to a ghastly category error.",
        "tags": ["poetry", "moral-weight", "war", "interrogation"]
    },
    {
        "quote": "‘पर शिराएँ जिस महीरुह की अतल में हैं गड़ी, वह नहीं भयभीत होता क्रूर झंझावात से।’\n\n('The tree whose roots are buried in the deep abyss does not tremble before the cruel tempest.')" ,
        "author": "Ramdhari Singh Dinkar",
        "work": "Kurukshetra",
        "year": 1946,
        "translator": None,
        "hook": "How to anchor internal resilience in deep roots.",
        "why_it_lands": "A timeless botanical metaphor for psychological and spiritual fortitude. Dinkar balances the violent agitation of the storm ('क्रूर झंझावात') against the profound stillness of roots embedded in the unshakeable deep ('अतल').",
        "tags": ["metaphor", "resilience", "poetry", "nature"]
    },
    {
        "quote": "‘बताना उसे दर्शन की भ्रान्ति है। शोषण की श्रृंखला के हेतु बनती जो शान्ति, युद्ध है, यथार्थ में वो भीषण अशान्ति है;’\n\n('To call it peace is a philosophical delusion. The peace that is forged merely to preserve the chains of exploitation is, in truth, an ongoing, terrible war.')",
        "author": "Ramdhari Singh Dinkar",
        "work": "Kurukshetra",
        "year": 1946,
        "translator": None,
        "hook": "How to unmask institutional peace as concealed violence.",
        "why_it_lands": "Dinkar shatters the sanctimonious defense of social order. A peace designed to protect the mechanisms of oppression is diagnosed not as harmony, but as the quietest and most devastating form of warfare.",
        "tags": ["political-satire", "philosophy", "justice", "polemic"]
    },
    {
        "quote": "‘अन्त नहीं नर-पंथ का, कुरुक्षेत्र की धूल, आँसू बरसें, तो यहीं खिले शान्ति का फूल।’\n\n('The dust of Kurukshetra is not the end of the human path; when tears rain down, it is right here that the flower of true peace will bloom.')",
        "author": "Ramdhari Singh Dinkar",
        "work": "Kurukshetra",
        "year": 1946,
        "translator": None,
        "hook": "How to transform a battlefield into ground for moral rebirth.",
        "why_it_lands": "Dinkar concludes the blood-soaked epic with redemption through grief. The battlefield's dust is not human finality, but soil where true peace can only sprout after being watered by tears of remorse.",
        "tags": ["poetry", "redemption", "hope", "metaphor"]
    }
]

def main():
    with open(QUOTE_BANK_PATH, "r", encoding="utf-8") as f:
        existing = json.load(f)

    existing_texts = {q["quote"].strip() for q in existing}
    added = 0
    for q in NEW_QUOTES:
        if q["quote"].strip() not in existing_texts:
            existing.append(q)
            existing_texts.add(q["quote"].strip())
            added += 1

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"Added {added} new quotes. Quote bank total: {len(existing)}")

if __name__ == "__main__":
    main()
