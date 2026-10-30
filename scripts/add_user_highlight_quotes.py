#!/usr/bin/env python3
# add_user_highlight_quotes.py — Adds curated passages from user Kindle highlights (Cixin Liu, Oliver Burkeman, Khushwant Singh)
# Usage: python3 scripts/add_user_highlight_quotes.py
# Requires: Python standard library, content/cards.json, content/quote-bank.json
#
# Gotchas:
# - Cards in cards.json require strict adherence to lint_cards.py: no em dashes, no banned adverbs/superlatives, strict word counts.
# - Shelf entries in quote-bank.json must have two clean paragraphs without markdown headings, bullet points, or dividers.
# - Quote sizes must be paced between 35-55 words to avoid font shrinkage on mobile widgets.

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARDS_FILE = ROOT / "content" / "cards.json"
QB_FILE = ROOT / "content" / "quote-bank.json"

NEW_CARD = {
    "id": "singh-train-to-pakistan-both-sides",
    "job": "How to strip an atrocity of its excuses",
    "quote": "Muslims said the Hindus had planned and started the killing. According to the Hindus, the Muslims were to blame. The fact is, both sides killed. Both shot and stabbed and speared and clubbed. Both tortured. Both raped.",
    "author": "Khushwant Singh",
    "work": "Train to Pakistan",
    "year": 1956,
    "translator": None,
    "highlights": [
        "The fact is, both sides killed",
        "Both shot and stabbed and speared and clubbed"
    ],
    "lookCloser": "Singh strips away political rationalizations by hammering the reader with monosyllabic verbs. He links four violent actions with the word and, refusing commas or pauses. The sentences grow shorter as the violence intensifies. By repeating the subject both across four consecutive declarations, he dissolves partisan blame into shared savagery.",
    "stealIt": "To describe collective violence without taking sides, eliminate explanatory adverbs. Chain physical verbs together with the conjunction and. Let the unadorned actions carry the horror.",
    "aroundIt": "Set during the 1947 Partition of British India, the novel depicts the fictional border village of Mano Majra. As ten million refugees crossed the new frontier and nearly a million died in communal massacres, Singh sought to record the human tragedy without historical abstraction.",
    "verification": "Chapter 1: Dacoity, opening pages."
}

NEW_SHELF_QUOTES = [
    {
        "work": "The Three-Body Problem",
        "author": "Cixin Liu",
        "quote": "Her fifteen-year-old body was so soft that the bullet hardly slowed down as it passed through it and whistled in the air behind her. The young Red Guard tumbled down along with her flag, her light form descending even more slowly than the piece of red fabric, like a little bird unwilling to leave the sky.",
        "explanation": "Liu uses startlingly gentle verbs in the middle of a slaughter: the girl's form descends slowly, like a little bird unwilling to leave the sky. In this opening chapter, she appears as an anonymous casualty, an emblem of the madness and ideological fervor consuming the Cultural Revolution.\n\nOnly chapters later, when Ye Wenjie stands in the bitter cold of Inner Mongolia remembering her lost younger sister Wenxue, does Liu repeat the image of that same slender figure waving the flag. By attaching that exact physical marker to a person the protagonist loved, Liu collapses an anonymous historical spectacle into private, irreparable grief.",
        "tags": ["war", "loss", "devotion", "imagery"]
    },
    {
        "work": "The Three-Body Problem",
        "author": "Cixin Liu",
        "quote": "Half of her young head was blown away, and only a single, beautiful eye remained to stare at the blue sky of 1967. There was no pain in that gaze, only solidified devotion and yearning.",
        "explanation": "Liu captures the horror of ideological fanaticism not through grotesque revulsion, but through a chilling absence of suffering. The surviving eye reveals no agony or sense of betrayal, only an unshakeable faith frozen in the middle of crossfire.\n\nThe terror of the passage lies in its stillness. By fixing that final gaze on the clear summer sky, Liu exposes how easily youthful idealism can be hollowed out and turned into a sacrificial instrument, leaving devotion as the only thing that outlasts physical destruction.",
        "tags": ["fanaticism", "youth", "war", "tragedy"]
    },
    {
        "work": "The Three-Body Problem",
        "author": "Cixin Liu",
        "quote": "At the top of the building, a young girl waved a bright red banner. Her slender figure contrasted vividly with the breadth of the flag: It was her sister, Wenxue. She had only learned recently that Wenxue had died two years ago in one of the wars between Red Guard factions.",
        "explanation": "This memory completes the circular callback to the book's opening battle. When Wenjie envisions her sister on the rooftop, the recurring detail of the slender silhouette holding the oversized flag connects back to the anonymous casualty tumbling from the gates in the prologue.\n\nIn fiction, the most piercing emotional turns occur when public history reconnects with private loss. By withholding the sister's identity during the initial battle scene, Liu lets the historical tragedy strike twice: first as collective madness, and finally as an intimate family wound.",
        "tags": ["memory", "grief", "family", "history"]
    },
    {
        "work": "Four Thousand Weeks",
        "author": "Oliver Burkeman",
        "quote": "We treat our plans as though they are a lasso, thrown from the present around the future, in order to bring it under our command. But all a plan is—all it could ever possibly be—is a present-moment statement of intent. The future, of course, is under no obligation to comply.",
        "explanation": "Burkeman dismantles the modern obsession with time management with a single physical metaphor. We imagine planning as a mechanical grip that can rope tomorrow into submission, mistaking our anxious thoughts for actual sovereignty over what hasn't happened yet.\n\nThe sentence turns on that quiet, poetic closing cadence: the future is under no obligation to comply. Burkeman doesn't deliver this truth as a counsel of despair, but as a release valve. Acknowledging that our control is modest frees us from the exhausting burden of trying to dictate outcomes.",
        "tags": ["time", "planning", "anxiety", "philosophy"]
    },
    {
        "work": "Four Thousand Weeks",
        "author": "Oliver Burkeman",
        "quote": "“Because children grow up, we think a child’s purpose is to grow up,” Herzen says. “But a child’s purpose is to be a child. Nature doesn’t disdain what only lives for a day. It pours the whole of itself into each moment… Life’s bounty is in its flow. Later is too late.”",
        "explanation": "Drawing on the Russian thinker Alexander Herzen, Burkeman exposes the instrumental trap that infects modern life. We constantly evaluate our activities solely by where they lead, treating childhood merely as preparation for adulthood and today as a down payment on tomorrow.\n\nHerzen's formulation restores inherent dignity to fleeting experiences. A Mayfly that lives for a single afternoon is not an incomplete creature, and a quiet conversation is not a waste of time just because it produces no future asset. The value of life exists in its unfolding, not in an elusive destination.",
        "tags": ["presence", "childhood", "mortality", "living"]
    },
    {
        "work": "Four Thousand Weeks",
        "author": "Oliver Burkeman",
        "quote": "“In the process of trying to attain a few moments of bliss,” Rinaldi explains, “I experience something else: patience and humility, definitely, but also freedom. Freedom to pursue the futile. And the freedom to suck without caring is revelatory.” Results aren’t everything... because results always come later—and later is always too late.",
        "explanation": "Burkeman explores the quiet liberation of engaging in activities purely for their own sake. In an economy that demands every hobby be monetized or optimized for measurable growth, doing something clumsily and without ambition becomes a radical act of self-possession.\n\nThe freedom to suck without caring breaks the tyranny of future payoffs. When you surrender the requirement to be proficient, you step out of the productivity treadmill and reclaim the present moment as an end in itself.",
        "tags": ["hobbies", "play", "freedom", "atelic"]
    },
    {
        "work": "Four Thousand Weeks",
        "author": "Oliver Burkeman",
        "quote": "Kafka called off the engagement, but the letters continued. (Though Kafka was indecisive about those too: “It is quite right that we should stop this business of so many letters,” he wrote to Bauer on one occasion. “Yesterday I even started a letter on this subject, which I will send tomorrow.”)",
        "explanation": "Burkeman uses Kafka's tortuous romance with Felice Bauer to illustrate the paralysis of perfectionism. Kafka craved emotional connection yet panicked at the messy vulnerability of shared life, retreating into hundreds of neurotic letters while meeting in person only a handful of times.\n\nThe parenthetical note captures the tragicomic heart of avoidance. Kafka writes a letter to insist they must stop exchanging letters, and promises to mail it the following day. It is an unforgettable snapshot of how humans invent elaborate intellectual rituals to dodge the finality of a choice.",
        "tags": ["indecision", "romance", "letters", "kafka"]
    },
    {
        "work": "Train to Pakistan",
        "author": "Khushwant Singh",
        "quote": "Mano Majra is a tiny place. It has only three brick buildings, one of which is the home of the moneylender Lala Ram Lal. The other two are the Sikh temple and the mosque... But there is one object that all Mano Majrans—even Lala Ram Lal—venerate.",
        "explanation": "Singh builds the geographic and social fault lines of Mano Majra with razor-sharp economy. In a village of mud huts, brick signifies power, and the three brick buildings represent the fragile triad holding the community together: the Sikh gurdwara, the Muslim mosque, and the Hindu moneylender.\n\nNotice how Singh deliberately isolates Lala Ram Lal in the phrasing: even Lala Ram Lal venerates the sacred rock. By setting the moneylender apart not just from his neighbors but from the spiritual identity of the village, Singh foreshadows the quiet alienation that turns him into the first target when communal madness strikes.",
        "tags": ["community", "isolation", "society", "partition"]
    }
]

def main():
    # 1. Update cards.json
    with open(CARDS_FILE, "r", encoding="utf-8") as f:
        cards = json.load(f)

    existing_card_ids = {c["id"] for c in cards}
    if NEW_CARD["id"] not in existing_card_ids:
        cards.append(NEW_CARD)
        with open(CARDS_FILE, "w", encoding="utf-8") as f:
            json.dump(cards, f, indent=2, ensure_ascii=False)
        print(f"✓ Added card '{NEW_CARD['id']}' to cards.json (Total cards: {len(cards)})")
    else:
        print(f"Card '{NEW_CARD['id']}' already exists in cards.json.")

    # 2. Update quote-bank.json
    with open(QB_FILE, "r", encoding="utf-8") as f:
        qb = json.load(f)

    existing_quotes = {q.get("quote", "").strip() for q in qb}
    added_shelf = 0
    for nq in NEW_SHELF_QUOTES:
        if nq["quote"].strip() not in existing_quotes:
            qb.append(nq)
            added_shelf += 1
            print(f"✓ Added shelf quote: {nq['author']} — {nq['work']} ({len(nq['quote'].split())}w)")
        else:
            print(f"Shelf quote already exists: {nq['author']} — {nq['work']}")

    if added_shelf > 0:
        with open(QB_FILE, "w", encoding="utf-8") as f:
            json.dump(qb, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved {added_shelf} new quotes to quote-bank.json (Total shelf quotes: {len(qb)})")

if __name__ == "__main__":
    main()
