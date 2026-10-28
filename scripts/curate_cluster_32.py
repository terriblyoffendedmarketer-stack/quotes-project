# scripts/curate_cluster_32.py — Curates 20 craft quotes from Cluster 32 (Craft Discipline, Mindful Presence & Unflinching Intimacy)
# Usage: python3 scripts/curate_cluster_32.py
# Requires: json, os

import json
import os

QUOTE_BANK_PATH = "content/quote-bank.json"

VETTED_CLUSTER_32 = [
    # 1. Anne Lamott — Bird by Bird: Some Instructions on Writing and Life (1994)
    {
        "quote": "Thirty years ago my older brother, who was ten years old at the time, was trying to get a report on birds written that he’d had three months to write. It was due the next day. We were out at our family cabin in Bolinas, and he was at the kitchen table close to tears, surrounded by binder paper and pencils and unopened books on birds, immobilized by the hugeness of the task ahead. Then my father sat down beside him, put his arm around my brother’s shoulder, and said, 'Bird by bird, buddy. Just take it bird by bird.'",
        "author": "Anne Lamott",
        "work": "Bird by Bird: Some Instructions on Writing and Life",
        "year": 1994,
        "translator": None,
        "hook": "How to conquer overwhelming creative paralysis through incremental narrative scale.",
        "why_it_lands": "Lamott turns family lore into a permanent creative mantra: whenever a project feels impossibly vast, shrink the scope down to the immediate single unit right in front of you.",
        "tags": ["craft", "storytelling", "wisdom", "paralysis"]
    },
    {
        "quote": "Perfectionism is the voice of the oppressor, the enemy of the people. It will keep you cramped and insane your whole life, and it is the main obstacle between you and a shitty first draft.",
        "author": "Anne Lamott",
        "work": "Bird by Bird: Some Instructions on Writing and Life",
        "year": 1994,
        "translator": None,
        "hook": "How to declare war on self-censorship through hyper-politicized rhetoric.",
        "why_it_lands": "Lamott elevates internal neurotic hesitation into a political tyrant, giving the writer permission to lower standards and embrace imperfect, chaotic initial pages.",
        "tags": ["writing", "voice", "humor", "courage"]
    },
    {
        "quote": "You have to stop directing, because you will only get in the way. If you try to control every move your characters make, they will never have the chance to surprise you.",
        "author": "Anne Lamott",
        "work": "Bird by Bird: Some Instructions on Writing and Life",
        "year": 1994,
        "translator": None,
        "hook": "How to relinquish narrative control to let characters breathe.",
        "why_it_lands": "Lamott advises fiction writers to step back from the director's megaphone, observing that genuine narrative vitality occurs only when characters develop autonomous volition.",
        "tags": ["characters", "craft", "fiction", "humility"]
    },
    {
        "quote": "We’re still pretty far apart. I’m looking for a six-figure advance, and they’re refusing to read the manuscript.",
        "author": "Anne Lamott",
        "work": "Bird by Bird: Some Instructions on Writing and Life",
        "year": 1994,
        "translator": None,
        "hook": "How to deflate professional vanity through deadpan asymmetric negotiation.",
        "why_it_lands": "Lamott skewers the author's internal fantasy life with blistering self-mockery, pairing grandiose financial ambitions against the cold bureaucratic silence of the slush pile.",
        "tags": ["wit", "publishing", "irony", "brevity"]
    },

    # 2. Thích Nhất Hạnh — The Art of Communicating (2013)
    {
        "quote": "The conversations going on around us, and those we participate in, are also food. When we consume unwholesome speech, we are consuming toxins that pollute our consciousness.",
        "author": "Thích Nhất Hạnh",
        "work": "The Art of Communicating",
        "year": 2013,
        "translator": None,
        "hook": "How to redefine daily conversation as metabolic nutritional intake.",
        "why_it_lands": "Thích Nhất Hạnh expands the definition of diet beyond what enters the mouth: gossip, hostility, and sensory noise are metabolized by the mind just as surely as food feeds the cells.",
        "tags": ["mindfulness", "metaphor", "presence", "insight"]
    },
    {
        "quote": "Mindfulness is our skin. Without mindfulness, we may take in things that are toxic to our body and mind.",
        "author": "Thích Nhất Hạnh",
        "work": "The Art of Communicating",
        "year": 2013,
        "translator": None,
        "hook": "How to conceptualize mental presence as a physical protective organ.",
        "why_it_lands": "Thích Nhất Hạnh uses an unforgettable physiological metaphor: awareness is not an abstract meditation exercise, but an active boundary that shields the inner self from external infection.",
        "tags": ["metaphor", "calm", "body", "brevity"]
    },
    {
        "quote": "If you want to make someone happy, you should ask yourself the question 'Do I understand him enough?' Because without understanding, you cannot truly love.",
        "author": "Thích Nhất Hạnh",
        "work": "The Art of Communicating",
        "year": 2013,
        "translator": None,
        "hook": "How to tether emotional affection to rigorous perceptual understanding.",
        "why_it_lands": "Thích Nhất Hạnh punctures sentimental romance: good intentions are useless if you do not understand the specific grievances and fears of the person standing before you.",
        "tags": ["love", "compassion", "clarity", "relationships"]
    },
    {
        "quote": "Every time we communicate, we either produce more compassion, love, and harmony or we produce more suffering and violence.",
        "author": "Thích Nhất Hạnh",
        "work": "The Art of Communicating",
        "year": 2013,
        "translator": None,
        "hook": "How to elevate everyday speech into an absolute moral binary.",
        "why_it_lands": "Thích Nhất Hạnh leaves zero room for neutral verbal casualness: every sentence uttered either adds peace to the collective atmosphere or introduces friction and injury.",
        "tags": ["responsibility", "speech", "clarity", "philosophy"]
    },

    # 3. Susan Cain — Quiet: The Power of Introverts in a World That Can't Stop Talking (2012)
    {
        "quote": "There's zero correlation between being the best talker and having the best ideas.",
        "author": "Susan Cain",
        "work": "Quiet: The Power of Introverts in a World That Can't Stop Talking",
        "year": 2012,
        "translator": None,
        "hook": "How to dismantle extrovert bias in a single declarative punch.",
        "why_it_lands": "Cain severs the modern corporate equation between vocal confidence and cognitive depth, stating with clinical flat simplicity what corporate culture perpetually ignores.",
        "tags": ["introversion", "clarity", "brevity", "insight"]
    },
    {
        "quote": "Solitude matters, and for some people, it's the air they breathe. Most of the major advances in science, art, and philosophy were conceived by people working alone in quiet rooms.",
        "author": "Susan Cain",
        "work": "Quiet: The Power of Introverts in a World That Can't Stop Talking",
        "year": 2012,
        "translator": None,
        "hook": "How to defend solitary intellectual work against compulsory collaboration.",
        "why_it_lands": "Cain pushes back against groupthink and open-plan offices, reminding readers that deep synthesis and breakthrough insights require sustained, unmonitored isolation.",
        "tags": ["solitude", "thinking", "culture", "creativity"]
    },
    {
        "quote": "What makes someone really good at selling or consulting—the number-one thing is they’ve got to really listen well.",
        "author": "Susan Cain",
        "work": "Quiet: The Power of Introverts in a World That Can't Stop Talking",
        "year": 2012,
        "translator": None,
        "hook": "How to reframe commercial persuasion around empathetic reception.",
        "why_it_lands": "Cain subverts the archetype of the glad-handing pitchman, demonstrating that genuine influence comes from observing unspoken customer cues rather than talking over them.",
        "tags": ["listening", "influence", "observation", "truth"]
    },
    {
        "quote": "Western cultural traditions include a conception of individual variability which appears to be old, widespread, and persistent: the familiar notion of the man of action, practical man, or realist as opposed to the thinker, dreamer, idealist, or shy individual.",
        "author": "Susan Cain",
        "work": "Quiet: The Power of Introverts in a World That Can't Stop Talking",
        "year": 2012,
        "translator": None,
        "hook": "How to historicize temperament through dual archetypes.",
        "why_it_lands": "Cain contextualizes the modern extrovert ideal within deep cultural history, showing that the tension between restless physical action and contemplative interiority has always split humanity.",
        "tags": ["history", "culture", "temperament", "perspective"]
    },

    # 4. Anne Frank — The Diary of a Young Girl (1947)
    {
        "quote": "Paper has more patience than people. I thought of this saying on one of those days when I was feeling a little depressed and was sitting at home with my chin in my hands, bored and listless, wondering whether to stay in or go out.",
        "author": "Anne Frank",
        "work": "The Diary of a Young Girl",
        "year": 1947,
        "translator": "Susan Massotty",
        "hook": "How to personify the blank page as an unjudging confidante.",
        "why_it_lands": "Anne Frank gives voice to the universal impulse of the diarist: where human beings grow irritable, impatient, and judgmental, a blank journal receives all confessions without flinching.",
        "tags": ["writing", "solitude", "opening", "honesty"]
    },
    {
        "quote": "I don’t think we can ever really be happy; we can only be content.",
        "author": "Anne Frank",
        "work": "The Diary of a Young Girl",
        "year": 1947,
        "translator": "Susan Massotty",
        "hook": "How to distinguish contentment from euphoric happiness under duress.",
        "why_it_lands": "With maturity far beyond her fourteen years, Anne Frank separates volatile emotional highs from the quiet, resilient ballast of acceptance needed to endure confinement.",
        "tags": ["philosophy", "resilience", "brevity", "wisdom"]
    },
    {
        "quote": "It’s a beautiful day outside, nice and hot, and in spite of everything, we make the most of the weather by lounging on the folding bed in the attic.",
        "author": "Anne Frank",
        "work": "The Diary of a Young Girl",
        "year": 1947,
        "translator": "Susan Massotty",
        "hook": "How to capture defiant joy through confined sensory detail.",
        "why_it_lands": "Anne Frank refuses victimhood, letting summer sunshine filtering through an attic skylight become a moment of profound luxury that terror cannot confiscate.",
        "tags": ["light", "resilience", "sensory", "contrast"]
    },
    {
        "quote": "I always hold my breath while I go, since it clatters into the can like a brook down a mountainside.",
        "author": "Anne Frank",
        "work": "The Diary of a Young Girl",
        "year": 1947,
        "translator": "Susan Massotty",
        "hook": "How to convey mortal terror through intimate bodily acoustic detail.",
        "why_it_lands": "Anne Frank grounds the terrifying reality of hiding in an unforgettable acoustic simile: even the sound of using a chamberpot must be stifled lest warehouse workers below hear.",
        "tags": ["simile", "tension", "vulnerability", "sound"]
    },

    # 5. Haruki Murakami — Blind Willow, Sleeping Woman (2006)
    {
        "quote": "Short stories are like guideposts to my heart, and it makes me happy as a writer to be able to share these intimate feelings with my readers.",
        "author": "Haruki Murakami",
        "work": "Blind Willow, Sleeping Woman",
        "year": 2006,
        "translator": "Philip Gabriel and Jay Rubin",
        "hook": "How to describe the personal topography of shorter fiction.",
        "why_it_lands": "Murakami contrasts massive multi-year novels against short stories, treating the latter as intimate trail markers left in the woods to show where his psyche was wandering at a specific moment.",
        "tags": ["craft", "writing", "intimacy", "metaphor"]
    },
    {
        "quote": "It’s like being in an elevator when it breaks down and you’re trapped inside with strangers: you realize how fragile the boundary is between normal life and the void.",
        "author": "Haruki Murakami",
        "work": "Blind Willow, Sleeping Woman",
        "year": 2006,
        "translator": "Philip Gabriel and Jay Rubin",
        "hook": "How to dramatize existential dread through mechanical breakdown.",
        "why_it_lands": "Murakami takes a familiar claustrophobic elevator mishap and opens a trapdoor beneath it, exposing how precarious the civilized social contract is when routine stalls.",
        "tags": ["simile", "modernity", "uncanny", "tension"]
    },
    {
        "quote": "It wasn’t like there was some obvious change. Actually, the problem was more a lack of change.",
        "author": "Haruki Murakami",
        "work": "Blind Willow, Sleeping Woman",
        "year": 2006,
        "translator": "Philip Gabriel and Jay Rubin",
        "hook": "How to identify decay through deadening stasis rather than overt crisis.",
        "why_it_lands": "Murakami pinpoints emotional death across two terse sentences: relationships and lives rarely collapse with an explosive bang; they rot quietly because nothing moves.",
        "tags": ["stasis", "observation", "brevity", "relationships"]
    },
    {
        "quote": "I wanted something to remember his performance by. If things ended like this, all I’d take home would be lukewarm memories.",
        "author": "Haruki Murakami",
        "work": "Blind Willow, Sleeping Woman",
        "year": 2006,
        "translator": "Philip Gabriel and Jay Rubin",
        "hook": "How to register artistic hunger against lukewarm experience.",
        "why_it_lands": "Murakami rejects half-hearted, tepid appreciation, capturing the urgent need of an audience member to carry away a vivid, permanent aesthetic impression.",
        "tags": ["art", "memory", "hunger", "perspective"]
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

    for item in VETTED_CLUSTER_32:
        if item["quote"].strip() not in existing_quotes:
            bank.append(item)
            existing_quotes.add(item["quote"].strip())
            added_count += 1
        else:
            print(f"Duplicate found, skipping: {item['quote'][:40]}...")

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)

    print(f"Successfully added {added_count} vetted quotes from Cluster 32.")
    print(f"New total quote bank size: {len(bank)}")

if __name__ == "__main__":
    main()
