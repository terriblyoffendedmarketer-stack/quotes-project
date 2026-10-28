#!/usr/bin/env python3
"""
curate_cluster_12.py — Curates 20 vetted quotes from Cluster 12 (Satire & Philosophical Subversion)
into content/quote-bank.json.
"""

import json
from pathlib import Path

QUOTE_BANK_PATH = Path("/Users/apple/Documents/Claude Code/quotes-project/content/quote-bank.json")

NEW_QUOTES = [
    # Harishankar Parsai — Nithalle Ki Diary
    {
        "quote": "‘अरे यार, जब जिन्दगी बरबाद ही होनी है, तो उसे प्रमोशन पर बरबाद क्यों न किया जाए।’\n\n('My friend, when life has to be wasted anyway, why not waste it on a promotion?')",
        "author": "Harishankar Parsai",
        "work": "Nithalle Ki Diary",
        "year": 1968,
        "translator": None,
        "hook": "How to capture existential resignation through bureaucratic irony.",
        "why_it_lands": "Parsai captures middle-class despair not with tragic lamentation, but with casual fatalism. The dark pivot to ambition—ruining life deliberately in exchange for a higher post—turns institutional vanity into grim comedy.",
        "tags": ["satire", "irony", "existentialism", "bureaucracy"]
    },
    {
        "quote": "‘चमचा ज्यों-ज्यों परिपक्व होता जाता है, त्यों-त्यों नेता बनता जाता है।’\n\n('As a sycophant ripens, he turns into a leader.')",
        "author": "Harishankar Parsai",
        "work": "Nithalle Ki Diary",
        "year": 1968,
        "translator": None,
        "hook": "How to craft a biological aphorism on institutional sycophancy.",
        "why_it_lands": "Parsai borrows the vocabulary of natural ripening ('परिपक्व') to describe political corruption. The sycophant does not undergo moral transformation; leadership is merely the inevitable adult stage of the parasite.",
        "tags": ["aphorism", "political-satire", "subversion", "cynicism"]
    },
    {
        "quote": "देखो, हुआ ऐसा कि उसके पड़ोसी ने सुबह अखबार में उसकी तारीफ पढ़ी। वह शिवशंकर के पास गया और बोला— शिवशंकर बाबू, आज अखबार में आपके बारे में छपा है। यह सुनते ही शिवशंकर घबराकर चिल्लाया, 'अरे बाप रे! छप गया!' और वहीं गिर पड़ा।\n\n('His neighbor read praise of him in the morning paper. He rushed to Shivshankar and said, \"Shivshankar Babu, something about you is printed in today\\'s paper!\" Hearing this, Shivshankar panicked and screamed, \"Oh my god! It got printed!\" and collapsed right on the spot.')",
        "author": "Harishankar Parsai",
        "work": "Nithalle Ki Diary",
        "year": 1968,
        "translator": None,
        "hook": "How to expose civic terror through an innocent celebration.",
        "why_it_lands": "In an authoritarian or paranoid bureaucracy, public visibility is equated with catastrophe, even when framed as praise. The comedy springs from the instantaneous physical collapse provoked by a single headline.",
        "tags": ["comic-timing", "absurdism", "character-voice", "irony"]
    },
    {
        "quote": "‘बात यह है कि सरकारी दल बहुत चतुर है। वह कुछ ऐसे सदस्य ले आया है जिन्हें यहाँ पैर रखते ही नींद आने लगती है। वे दस्तखत करके सो जाते हैं, तो शाम को ही उठते हैं।’\n\n('The fact is, the ruling party is exceedingly clever. It brought in members who start feeling drowsy the moment they step into the chamber. They sign the roll, fall asleep, and wake up only in the evening.')",
        "author": "Harishankar Parsai",
        "work": "Nithalle Ki Diary",
        "year": 1968,
        "translator": None,
        "hook": "How to satirize legislative complicity as deliberate slumber.",
        "why_it_lands": "Parliamentary corruption is stripped of rhetorical theatrics and reduced to physiological lethargy. Compliance is weaponized as a scheduled afternoon nap.",
        "tags": ["satire", "political-voice", "understatement", "humor"]
    },

    # Harishankar Parsai — Vaishnav Ki Phislan
    {
        "quote": "शव-यात्रा का तौलिया तैयार रखते हैं। किसी के मरने की खबर मिली नहीं कि इतने प्रसन्न होते हैं, जैसे किसी की शादी हो रही है।\n\n('They keep a funeral towel folded and ready. The moment news of a death arrives, they are overjoyed, as though someone is getting married.')",
        "author": "Harishankar Parsai",
        "work": "Vaishnav Ki Phislan",
        "year": 1972,
        "translator": None,
        "hook": "How to expose morbid opportunism through a single domestic prop.",
        "why_it_lands": "The domestic specificity of the 'funeral towel' immediately indicts the social climber who uses mourning as networking. Parsai inverts societal grief into festive eagerness with devastating economy.",
        "tags": ["social-satire", "contrast", "prop", "hypocrisy"]
    },
    {
        "quote": "‘हनुमानभक्त’ मेरा एक मित्र कहता है, “अब आदमी पर भरोसा नहीं रहा। कुछ निश्चित नहीं है। अब तो हनुमानजी से प्रार्थना करते हैं कि अब के जब राम के काम से गन्धमादन जाओ तो हमारे लिए भी पेचिश की दवा लेते आना।”\n\n('A devotee friend of mine says: \"I no longer trust mankind. Nothing is certain anymore. Now I only pray to Lord Hanuman: next time you fly across Mount Gandhamadana on Ram\\'s errand, pick up some dysentery medicine for us as well.\"')",
        "author": "Harishankar Parsai",
        "work": "Vaishnav Ki Phislan",
        "year": 1972,
        "translator": None,
        "hook": "How to deflate epic mythology with mundane bodily affliction.",
        "why_it_lands": "Parsai collapses mythological grandiosity against the gritty reality of chronic illness. Placing an order for dysentery medicine on an epic celestial voyage deflates religious piety with sharp colloquial irreverence.",
        "tags": ["deflation", "satire", "contrast", "mythology"]
    },
    {
        "quote": "‘सरकारें खुद चाहती हैं कि कुछ लेखक उनका विरोध करें। वे उन्हें पहचान लें और जो चाहिए, दे-दिवा दें।’\n\n('Governments themselves want some writers to oppose them, so they can identify them and give them whatever payoffs they need.')",
        "author": "Harishankar Parsai",
        "work": "Vaishnav Ki Phislan",
        "year": 1972,
        "translator": None,
        "hook": "How to expose co-opted political dissent.",
        "why_it_lands": "Dissent is revealed not as a threat to authority, but as a recognized cataloging mechanism for co-optation. The power dynamic is inverted: protest becomes an application for an institutional handout.",
        "tags": ["cynicism", "political-satire", "power", "insight"]
    },
    {
        "quote": "इतना बड़ा भक्त, उतनी ही मैली चादर। शायद कबीरदास की तरह ‘जतन’ से ओढ़कर चदरिया को ‘जस की तस’ धर देते हैं।\n\n('The greater the devotee, the filthier the shroud. Perhaps, like Kabir, they drape the sheet with careful devotion only to return it untransformed.')",
        "author": "Harishankar Parsai",
        "work": "Vaishnav Ki Phislan",
        "year": 1972,
        "translator": None,
        "hook": "How to invert mystical verse to indict moral decay.",
        "why_it_lands": "Parsai takes Kabir's celebrated metaphor of the untainted spiritual garment ('चादर') and subverts it: the modern pietist wears their filth proudly as an ostentatious badge of sanctity.",
        "tags": ["allusion", "subversion", "irony", "spiritual-hypocrisy"]
    },

    # Umberto Eco — Six Walks in the Fictional Woods
    {
        "quote": "Every text, after all (as I have already written), is a lazy machine asking the reader to do some of its work.",
        "author": "Umberto Eco",
        "work": "Six Walks in the Fictional Woods",
        "year": 1994,
        "translator": None,
        "hook": "How to define literary mechanics through mechanical metaphor.",
        "why_it_lands": "Eco de-sacralizes narrative theory by treating the text as an incomplete contraption. A story is not an ornamental monument; it is a mechanism whose engine only turns over when fueled by the reader's inferences.",
        "tags": ["metaphor", "literary-craft", "metafiction", "aphorism"]
    },
    {
        "quote": "When trying to assess a film that contains sexually explicit scenes, you should check to see whether, when a character gets into an elevator or a car, the discourse time coincides with the story time.",
        "author": "Umberto Eco",
        "work": "Six Walks in the Fictional Woods",
        "year": 1994,
        "translator": None,
        "hook": "How to expose narrative stalling through chronological pacing.",
        "why_it_lands": "Eco provides an infallible diagnostic for artistic laziness: when discourse time mirrors physical transit without thematic weight, the storyteller is simply killing time between spectacles.",
        "tags": ["pacing", "craft-rule", "wit", "observation"]
    },
    {
        "quote": "It is true that in Sylvie we know without a doubt that Adrienne died in 1832 (whereas we are not equally sure that Napoleon died in 1821—since he could have been secretly rescued from Saint Helena by Julien Sorel, leaving a double there in his place, and may subsequently have lived under the name of Père Dodu in Loisy, where he encountered the narrator in 1830).",
        "author": "Umberto Eco",
        "work": "Six Walks in the Fictional Woods",
        "year": 1994,
        "translator": None,
        "hook": "How to prove that fictional certainty outlasts historical fact.",
        "why_it_lands": "Eco demonstrates the ontological supremacy of fiction: historical accounts are perpetually vulnerable to conspiracy and revision, whereas an author's created death remains eternally immutable.",
        "tags": ["paradox", "metafiction", "narrative-theory", "wit"]
    },
    {
        "quote": "It is the quantity of pages devoted to the effort of recollecting these hours, without actually reconstructing their actual sequence, it is the disproportion between the time of recollection and the time recollected...",
        "author": "Umberto Eco",
        "work": "Six Walks in the Fictional Woods",
        "year": 1994,
        "translator": None,
        "hook": "How to stretch subjective memory against chronological story time.",
        "why_it_lands": "Eco articulates the precise machinery of psychological realism: emotional truth is never measured by minutes lived, but by the disproportionate narrative space required to dredge them up.",
        "tags": ["time", "narrative-structure", "craft-analysis", "memory"]
    },

    # John Gray — Feline Philosophy: Cats and the Meaning of Life
    {
        "quote": "A good life is one they have felt and smelt, not a dim sighting of something far away.",
        "author": "John Gray",
        "work": "Feline Philosophy: Cats and the Meaning of Life",
        "year": 2020,
        "translator": None,
        "hook": "How to ground existential contentment in sensory immediacy.",
        "why_it_lands": "Gray strips away philosophical abstraction with tactile monosyllables ('felt and smelt'). Fulfillment is returned to animal immediacy, rebuking the human tendency to trade living presence for distant, deferred ideals.",
        "tags": ["sensory-detail", "philosophy", "simplicity", "contrast"]
    },
    {
        "quote": "Sleep for the joy of sleeping. Sleeping so that you can work harder when you wake up is a miserable way to live. Sleep for pleasure, not profit.",
        "author": "John Gray",
        "work": "Feline Philosophy: Cats and the Meaning of Life",
        "year": 2020,
        "translator": None,
        "hook": "How to liberate restorative rest from utilitarian productivity.",
        "why_it_lands": "Gray attacks the Protestant work ethic at its root. By contrasting 'pleasure' against 'profit', the sentence rescues the biological necessity of sleep from being monetized as instrumental maintenance.",
        "tags": ["cadence", "counter-intuitive", "polemic", "aphorism"]
    },
    {
        "quote": "Reasoning makes the modern neurosis worse: the characteristics the modern mind prides itself on are precisely those of madness.",
        "author": "John Gray",
        "work": "Feline Philosophy: Cats and the Meaning of Life",
        "year": 2020,
        "translator": None,
        "hook": "How to indict instrumental rationality as an anxiety amplifier.",
        "why_it_lands": "A clean, shocking reversal: human intellect is diagnosed not as the cure for psychic distress, but as its primary accelerant. Our proudest analytical faculties become indistinguishable from delirium.",
        "tags": ["paradox", "inversion", "cultural-critique", "intellect"]
    },
    {
        "quote": "The myth-ritual complex is a social form for the channelling of obsessions … It automatically engineers safety and banishes despair by keeping people focussed on the noses in front of their faces.",
        "author": "John Gray",
        "work": "Feline Philosophy: Cats and the Meaning of Life",
        "year": 2020,
        "translator": None,
        "hook": "How to diagnose human ritual as an insulation against existential dread.",
        "why_it_lands": "Gray dissects human social architecture with anthropological detachment. Ceremonies and daily customs are not searches for transcendental truth, but mechanical blinders constructed to keep cosmic terror at bay.",
        "tags": ["sociology", "detachment", "existentialism", "insight"]
    },

    # David Foster Wallace — Infinite Jest
    {
        "quote": "It’s a kind of emotional novocaine, this form of depression, and while it’s not overtly painful its deadness is disconcerting and . .. well, depressing.",
        "author": "David Foster Wallace",
        "work": "Infinite Jest",
        "year": 1996,
        "translator": None,
        "hook": "How to register clinical anhedonia through chemical numbness.",
        "why_it_lands": "Wallace bypasses gothic metaphors of sadness to identify depression's true horror: not active agony, but the eerie absence of feeling. The trailing conversational hesitation mimics psychic exhaustion.",
        "tags": ["interiority", "vernacular-rhythm", "psychology", "honesty"]
    },
    {
        "quote": "The needle makes a kind of thud and squeak when it goes in the cloth. It’s not much like the soundless pop and slide of a real cook-and-shoot.",
        "author": "David Foster Wallace",
        "work": "Infinite Jest",
        "year": 1996,
        "translator": None,
        "hook": "How to use micro-acoustic detail to establish somatic addiction.",
        "why_it_lands": "Wallace renders habit through sensory comparison: the friction of cotton versus the frictionless glide of flesh. The tactile onomatopoeia ('thud and squeak' vs. 'pop and slide') conveys visceral expertise without didactic explanation.",
        "tags": ["sound-design", "sensory-detail", "realism", "contrast"]
    },
    {
        "quote": "And so a series of personal interviews with the spiritually necrotic brother took place, Barry having to station himself on the other side of the playing-cards’ wastebasket so as even to get the older brother’s attention, trying to talk the brother down from the misanthropic spiritual ledge he was on.",
        "author": "David Foster Wallace",
        "work": "Infinite Jest",
        "year": 1996,
        "translator": None,
        "hook": "How to capture existential intervention through bureaucratic absurdity.",
        "why_it_lands": "The clinical inflation ('spiritually necrotic brother', 'misanthropic spiritual ledge') clashes against the bathetic obstacle of a novelty wastebasket. Wallace balances high clinical tragedy with physical farce.",
        "tags": ["maximalism", "contrast", "irony", "syntax"]
    },
    {
        "quote": "the A.C.D.C. campaign, brilliantly orchestrated by Boston MA's Viney and Veals Advertising, was pummelling the Big Four in the fiscal thorax with its ubiquitous anti-passivity slogan 'Don't Sit Still for Anything Less'",
        "author": "David Foster Wallace",
        "work": "Infinite Jest",
        "year": 1996,
        "translator": None,
        "hook": "How to parody commercial aggression through hyper-technical anatomical metaphor.",
        "why_it_lands": "Wallace renders corporate marketing through violent biological warfare. 'Pummelling the Big Four in the fiscal thorax' combines pugilism and corporate jargon into a delirious parody of late-capitalist velocity.",
        "tags": ["satire", "maximalism", "metaphor", "dissonance"]
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
