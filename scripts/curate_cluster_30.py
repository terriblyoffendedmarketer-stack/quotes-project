# scripts/curate_cluster_30.py — Curates 20 craft quotes from Cluster 30 (Craft Mastery, Lyrical Grief & Flash Parable)
# Usage: python3 scripts/curate_cluster_30.py
# Requires: json, os

import json
import os

QUOTE_BANK_PATH = "content/quote-bank.json"

VETTED_CLUSTER_30 = [
    # 1. Kurt Vonnegut — Pity the Reader: On Writing with Style (2019)
    {
        "quote": "Our audience requires us to be sympathetic and patient teachers, ever willing to simplify and clarify.",
        "author": "Kurt Vonnegut",
        "work": "Pity the Reader: On Writing with Style",
        "year": 2019,
        "translator": None,
        "hook": "How to adopt the posture of a patient teacher toward the reader.",
        "why_it_lands": "Vonnegut strips authorship of pretension, framing writing not as self-expression to be deciphered, but as an act of service dedicated to clarity and sympathy.",
        "tags": ["craft", "writing", "clarity", "humility"]
    },
    {
        "quote": "The gift for narrative, for storytelling, is rarer than the gift for poetic prose or elegant language—it isn’t even close.",
        "author": "Kurt Vonnegut",
        "work": "Pity the Reader: On Writing with Style",
        "year": 2019,
        "translator": None,
        "hook": "How to prioritize narrative momentum over decorative prose.",
        "why_it_lands": "Vonnegut cuts through the literary hierarchy, observing that while anyone can learn to write lovely sentences, constructing a compelling sequence of events is a vastly rarer craft instinct.",
        "tags": ["storytelling", "craft", "truth", "critique"]
    },
    {
        "quote": "‘Your deadwood is my foliage,’ a private writing client once said to me. True, it can be hard to tell the difference, especially if it’s your own.",
        "author": "Kurt Vonnegut",
        "work": "Pity the Reader: On Writing with Style",
        "year": 2019,
        "translator": None,
        "hook": "How to acknowledge the blindness of authorial self-editing.",
        "why_it_lands": "Vonnegut uses a wry botanical metaphor to illustrate the tragedy of revising your own work: the flab you ought to prune always looks like lush artistic foliage to the person who wrote it.",
        "tags": ["metaphor", "editing", "wit", "craft"]
    },
    {
        "quote": "You do not have to take anyone’s suggestions. You are the final editor. If you adhere to every voice offering suggestions, pandering to one and then the other, you may find yourself so far off course that you’re out at sea.",
        "author": "Kurt Vonnegut",
        "work": "Pity the Reader: On Writing with Style",
        "year": 2019,
        "translator": None,
        "hook": "How to defend authorial instinct against committee consensus.",
        "why_it_lands": "Vonnegut warns against death by feedback, reminding writers that attempting to please every critic turns a sharp idiosyncratic voice into an unrecognizable compromise lost at sea.",
        "tags": ["autonomy", "voice", "courage", "writing"]
    },

    # 2. Constance Hale — Sin and Syntax: How to Craft Wicked Good Prose (1999)
    {
        "quote": "Choosing the right noun means exploring the layers of a word. First, it must be precise, conveying the exact image you are rendering: pick bungalow if you’re describing a one-story house with a low pitched roof.",
        "author": "Constance Hale",
        "work": "Sin and Syntax: How to Craft Wicked Good Prose",
        "year": 1999,
        "translator": None,
        "hook": "How to anchor sensory architecture in architectural precision.",
        "why_it_lands": "Hale shows how a single specific noun does the work of three sluggish adjectives, forcing the writer to see their subject clearly before demanding the reader see it.",
        "tags": ["nouns", "precision", "craft", "vocabulary"]
    },
    {
        "quote": "When I split an infinitive, God damn it, I split it so it stays split.",
        "author": "Constance Hale",
        "work": "Sin and Syntax: How to Craft Wicked Good Prose",
        "year": 1999,
        "translator": None,
        "hook": "How to violate grammatical orthodoxy for rhythmic emphasis.",
        "why_it_lands": "Quoting Raymond Chandler, Hale celebrates deliberate stylistic rebellion, arguing that artificial 19th-century Latin rules should never override the natural punch and swagger of spoken English.",
        "tags": ["grammar", "voice", "attitude", "rhythm"]
    },
    {
        "quote": "Remember… every audience is ready to tire; and the moment they begin to tire, all our eloquence goes for nothing. A loose and verbose manner never fails to create disgust… better to say too little, than too much.",
        "author": "Constance Hale",
        "work": "Sin and Syntax: How to Craft Wicked Good Prose",
        "year": 1999,
        "translator": None,
        "hook": "How to guard against reader fatigue through strategic economy.",
        "why_it_lands": "Hale quotes rhetorician Hugh Blair to warn that the reader's attention is a fragile, evaporating resource; once indulgence sets in, even the most poetic sentences are experienced as harassment.",
        "tags": ["brevity", "restraint", "rhetoric", "reader"]
    },
    {
        "quote": "You get paid by the period.",
        "author": "Constance Hale",
        "work": "Sin and Syntax: How to Craft Wicked Good Prose",
        "year": 1999,
        "translator": None,
        "hook": "How to enforce syntactic discipline in a five-word maxim.",
        "why_it_lands": "Hale quotes Gary Provost's memorable quip to remind verbose writers that ending sentences cleanly and frequently creates energy, rhythm, and forward velocity.",
        "tags": ["brevity", "syntax", "craft", "punch"]
    },

    # 3. Sylvia Plath — The Bell Jar (1963)
    {
        "quote": "It wasn't night and it wasn't day, but some lurid third interval that had suddenly slipped between them and would never end.",
        "author": "Sylvia Plath",
        "work": "The Bell Jar",
        "year": 1963,
        "translator": None,
        "hook": "How to invent an eerie liminal interval to dramatize insomnia.",
        "why_it_lands": "Plath slips past the binary of day and night to coin an uncanny 'third interval', capturing the terrifying hallucination of wakefulness where circadian time completely breaks down.",
        "tags": ["time", "psychology", "atmosphere", "imagery"]
    },
    {
        "quote": "The sickness rolled through me in great waves. After each wave it would fade away and leave me limp as a wet leaf and shivering all over.",
        "author": "Sylvia Plath",
        "work": "The Bell Jar",
        "year": 1963,
        "translator": None,
        "hook": "How to convey visceral nausea through organic botanical fragility.",
        "why_it_lands": "Plath moves from tidal momentum to dead calm, comparing a drained body to a sodden, lifeless leaf stuck to concrete to capture total physical surrender.",
        "tags": ["sensory", "simile", "body", "vulnerability"]
    },
    {
        "quote": "I laid my face to the smooth face of the marble and howled my loss into the cold salt rain.",
        "author": "Sylvia Plath",
        "work": "The Bell Jar",
        "year": 1963,
        "translator": None,
        "hook": "How to anchor acoustic agony against cold mineral texture.",
        "why_it_lands": "Plath pairs the unyielding smoothness of marble with the wild abandon of a vocal howl, creating an unforgettable sensory collision between permanent stone and temporary flesh.",
        "tags": ["grief", "imagery", "sound", "texture"]
    },
    {
        "quote": "The bottle slid from my fingers and I lay down. The silence drew off, baring the pebbles and shells and all the tatty wreckage of my life.",
        "author": "Sylvia Plath",
        "work": "The Bell Jar",
        "year": 1963,
        "translator": None,
        "hook": "How to reveal psychological ruin through an ebbing tidal landscape.",
        "why_it_lands": "Plath borrows the imagery of low tide to depict absolute desolation, baring the jagged, pathetic detritus of an identity when the noise of daily distraction recedes.",
        "tags": ["metaphor", "stillness", "desolation", "memoir"]
    },

    # 4. Markus Zusak — The Book Thief (2005)
    {
        "quote": "A small fact: You are going to die. I am in all truthfulness attempting to be cheerful about this whole topic, though most people find themselves hindered in believing me, no matter my protestations.",
        "author": "Markus Zusak",
        "work": "The Book Thief",
        "year": 2005,
        "translator": None,
        "hook": "How to disarm existential dread through conversational narrator frankness.",
        "why_it_lands": "Zusak gives Death the voice of an exasperated, polite civil servant who treats human mortality not as gothic terror, but as an inevitable administrative fact delivered with dark cheer.",
        "tags": ["voice", "irony", "perspective", "opening"]
    },
    {
        "quote": "I do not carry a sickle or scythe. I only wear a black-hooded robe if it's cold. And I don't have those skull-like facial features you seem to enjoy pinning on me from a distance.",
        "author": "Markus Zusak",
        "work": "The Book Thief",
        "year": 2005,
        "translator": None,
        "hook": "How to deconstruct mythic folklore with dry practical complaints.",
        "why_it_lands": "Zusak subverts centuries of gothic grim-reaper iconography, turning mythic terror into mundane wardrobe practicalities that puncture the reader's defense mechanisms.",
        "tags": ["humor", "deconstruction", "imagery", "character"]
    },
    {
        "quote": "Don’t forget your misery … It grew on them like a vine.",
        "author": "Markus Zusak",
        "work": "The Book Thief",
        "year": 2005,
        "translator": None,
        "hook": "How to depict chronic grief through parasitic botanical growth.",
        "why_it_lands": "Zusak uses a deceptively simple comparison to show that suffering in wartime doesn't remain an external trauma; it wraps itself around the ribs and becomes a living part of the host.",
        "tags": ["simile", "sorrow", "brevity", "imagery"]
    },
    {
        "quote": "‘You bastards, you lovely bastards. Don’t make me happy. Please, don’t fill me up and let me think that something good can come of any of this.’",
        "author": "Markus Zusak",
        "work": "The Book Thief",
        "year": 2005,
        "translator": None,
        "hook": "How to articulate the acute terror of hope during sustained tragedy.",
        "why_it_lands": "Zusak captures the defense mechanism of the traumatized: when suffering is all that is predictable, an unexpected gesture of kindness feels more dangerous than cruelty because it softens the armor.",
        "tags": ["dialogue", "emotion", "psychology", "contrast"]
    },

    # 5. Etgar Keret — The Bus Driver Who Wanted to Be God (2004)
    {
        "quote": "This was the story of a bus driver who didn't want to be an astronaut or a movie star. He wanted to be God.",
        "author": "Etgar Keret",
        "work": "The Bus Driver Who Wanted to Be God",
        "year": 2004,
        "translator": "Miriam Shlesinger",
        "hook": "How to open a contemporary parable with deadpan cosmic ambition.",
        "why_it_lands": "Keret bypasses normal childhood ambitions to place a mundane municipal worker in direct comparison with the Almighty, launching a surreal fable with poker-faced modern reality.",
        "tags": ["opening", "parable", "irony", "brevity"]
    },
    {
        "quote": "The first human being to use a club wasn’t the strongest person in his tribe or the smartest. It’s just that the others didn’t need a club, while he did.",
        "author": "Etgar Keret",
        "work": "The Bus Driver Who Wanted to Be God",
        "year": 2004,
        "translator": "Miriam Shlesinger",
        "hook": "How to subvert evolutionary mythology through human deficiency.",
        "why_it_lands": "Keret turns standard anthropology on its head, suggesting that technological tools arose not from genius or dominance, but from the acute weakness and inadequacy of the frail.",
        "tags": ["philosophy", "insight", "humor", "history"]
    },
    {
        "quote": "You know how they say suicides always happen in threes? Well, there’s something to it. People around you start dying, and you begin to ask yourself what the hell makes you different, and what’s keeping you alive anyway.",
        "author": "Etgar Keret",
        "work": "The Bus Driver Who Wanted to Be God",
        "year": 2004,
        "translator": "Miriam Shlesinger",
        "hook": "How to confront contagious despair with conversational bluntness.",
        "why_it_lands": "Keret uses colloquial cadence to cut straight through romanticized melancholy, capturing the terrifying rationalism of a mind wondering why it continues to breathe when peers give up.",
        "tags": ["voice", "existential", "psychology", "honesty"]
    },
    {
        "quote": "Kneller said it was a good sign, because Jan got lost last time too, and to celebrate, he took out this bong, and him and Jan each took four hits, till they were totally wasted.",
        "author": "Etgar Keret",
        "work": "The Bus Driver Who Wanted to Be God",
        "year": 2004,
        "translator": "Miriam Shlesinger",
        "hook": "How to defuse the solemnity of the afterlife with slacker nonchalance.",
        "why_it_lands": "Keret subverts Dante's inferno into an absurd, bureaucratic purgatory for suicides where losing the path is greeted not with dread, but with casual stoner indifference.",
        "tags": ["afterlife", "satire", "surrealism", "dialogue"]
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

    for item in VETTED_CLUSTER_30:
        if item["quote"].strip() not in existing_quotes:
            bank.append(item)
            existing_quotes.add(item["quote"].strip())
            added_count += 1
        else:
            print(f"Duplicate found, skipping: {item['quote'][:40]}...")

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)

    print(f"Successfully added {added_count} vetted quotes from Cluster 30.")
    print(f"New total quote bank size: {len(bank)}")

if __name__ == "__main__":
    main()
