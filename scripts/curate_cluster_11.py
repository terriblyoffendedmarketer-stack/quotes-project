#!/usr/bin/env python3
"""
curate_cluster_11.py — Curates 20 vetted quotes from Cluster 11 (Modern Classics & Philosophical Allegory)
into content/quote-bank.json.
"""

import json
from pathlib import Path

QUOTE_BANK_PATH = Path("/Users/apple/Documents/Claude Code/quotes-project/content/quote-bank.json")

NEW_QUOTES = [
    # Markus Zusak — The Book Thief
    {
        "quote": "With a smile like that, you don’t need eyes.",
        "author": "Markus Zusak",
        "work": "The Book Thief",
        "year": 2005,
        "translator": None,
        "hook": "How to displace sight with an overpowering domestic expression.",
        "why_it_lands": "Zusak renders visual warmth not by detailing facial geometry, but by rendering the observer's eyes completely redundant. It is a sudden, tender inversion that bypasses sentimental clutter.",
        "tags": ["imagery", "subversion", "tenderness", "character-voice"]
    },
    {
        "quote": "She said it out loud, the words distributed into a room that was full of cold air and books.",
        "author": "Markus Zusak",
        "work": "The Book Thief",
        "year": 2005,
        "translator": None,
        "hook": "How to give spoken breath physical volume in a room.",
        "why_it_lands": "Words aren't merely uttered; they are 'distributed' like physical ballast into an atmosphere already thick with cold air and paper. The sentence binds speech directly to the architectural texture of the sanctuary.",
        "tags": ["sensory-detail", "setting", "verb-choice", "interiority"]
    },
    {
        "quote": "Better that we leave the paint behind, than ever forget the music.",
        "author": "Markus Zusak",
        "work": "The Book Thief",
        "year": 2005,
        "translator": None,
        "hook": "How to weigh disposable materials against enduring sensory truth.",
        "why_it_lands": "A crisp ethical choice drawn between the utility of paint and the preservation of melody. The clean comparative balance ('Better that... than ever...') turns practical triage into a statement on human survival.",
        "tags": ["cadence", "contrast", "moral-weight", "simplicity"]
    },
    {
        "quote": "Suffering had most definitely come, and if they could blame the Jews as a warning or prologue, they should have blamed the Führer and his quest for Russia as the actual cause.",
        "author": "Markus Zusak",
        "work": "The Book Thief",
        "year": 2005,
        "translator": None,
        "hook": "How to strip away collective scapegoating with syntactic lucidity.",
        "why_it_lands": "Zusak contrasts the superstitious scapegoating of a vulnerable minority with the cold arithmetic of imperial disaster. The rhythm of the conditional clause exposes the cowardice of ideological displacement.",
        "tags": ["syntax", "clarity", "moral-weight", "indictment"]
    },

    # Richard Adams — Watership Down
    {
        "quote": "Like trees in November, they were standing still, but they were not dead.",
        "author": "Richard Adams",
        "work": "Watership Down",
        "year": 1972,
        "translator": None,
        "hook": "How to capture stunned survival through autumnal stillness.",
        "why_it_lands": "Adams doesn't rely on frantic melodrama to depict trauma. He compares the surviving rabbits to bare November trees—unmoving, stripped of foliage, yet stubbornly retaining life beneath the bark.",
        "tags": ["simile", "pacing", "setting", "understatement"]
    },
    {
        "quote": "You can’t call your life your own: and in return you have safety—if it’s worth having at the price you pay.",
        "author": "Richard Adams",
        "work": "Watership Down",
        "year": 1972,
        "translator": None,
        "hook": "How to expose the Faustian bargain of totalitarian security.",
        "why_it_lands": "In one balanced sentence, Adams cuts right to the heart of Cowslip's warren. The colon splits autonomy from survival, and the trailing conditional ('if it’s worth having...') leaves the reader with the chill of comfortable enslavement.",
        "tags": ["syntax", "moral-weight", "philosophy", "freedom"]
    },
    {
        "quote": "“A jury of animals you shall have,” said Prince Rainbow. “A jury of elil, El-ahrairah. For a jury of rabbits would refuse to convict you, in spite of the evidence.”",
        "author": "Richard Adams",
        "work": "Watership Down",
        "year": 1972,
        "translator": None,
        "hook": "How to construct mythological law through tribal solidarity.",
        "why_it_lands": "The dialogue establishes lapine solidarity with dry inevitability. A jury of his own kind cannot convict the folk hero because cunning against predators is their supreme evolutionary virtue, evidence be damned.",
        "tags": ["mythology", "dialogue-craft", "worldbuilding", "voice"]
    },
    {
        "quote": "The ground became soft and damp. They could smell sedge and water.",
        "author": "Richard Adams",
        "work": "Watership Down",
        "year": 1972,
        "translator": None,
        "hook": "How to signal sanctuary through immediate tactile shifts.",
        "why_it_lands": "Two concise sentences that abandon abstraction for direct sensory evidence. The dampness underfoot and the sudden sharp scent of sedge and river water announce refuge faster than any narrative exposition could.",
        "tags": ["sensory-detail", "economy", "pacing", "setting"]
    },

    # Ursula K. Le Guin — The Dispossessed
    {
        "quote": "To break a promise is to deny the reality of the past; therefore it is to deny the hope of a real future.",
        "author": "Ursula K. Le Guin",
        "work": "The Dispossessed",
        "year": 1974,
        "translator": None,
        "hook": "How to tie ethical integrity to the mechanics of time.",
        "why_it_lands": "Le Guin anchors morality not in religious dogma, but in temporal physics. If the past was real, a vow made in it binds; breaking it collapses the temporal bridge required to construct any coherent tomorrow.",
        "tags": ["philosophy", "ethics", "time", "aphorism"]
    },
    {
        "quote": "Death was in him, under him; the earth itself was uncertain, unreliable. The enduring, the reliable, is a promise made by the human mind.",
        "author": "Ursula K. Le Guin",
        "work": "The Dispossessed",
        "year": 1974,
        "translator": None,
        "hook": "How to ground human permanence against geophysical indifference.",
        "why_it_lands": "The sentence begins with mortal instability beneath the boots and resolves with a quiet triumph of consciousness: endurance isn't an innate property of rocks or dirt, but a discipline authored entirely by human commitment.",
        "tags": ["contrast", "cadence", "philosophy", "existentialism"]
    },
    {
        "quote": "Grain grows best in shit, as we say in Northsetting.",
        "author": "Ursula K. Le Guin",
        "work": "The Dispossessed",
        "year": 1974,
        "translator": None,
        "hook": "How to cut intellectual pretension with agrarian earthiness.",
        "why_it_lands": "A sharp proverb from an anarchist mining colony. By insisting that flourishing depends upon rotting waste, the voice grounds lofty political debates in the inescapable soil of biological reality.",
        "tags": ["proverb", "voice", "vernacular", "candor"]
    },
    {
        "quote": "He lived about two hours. He couldn’t have been saved; there was no reason for him to live that long, no justification for those two hours.",
        "author": "Ursula K. Le Guin",
        "work": "The Dispossessed",
        "year": 1974,
        "translator": None,
        "hook": "How to stare at meaningless biological suffering without consolation.",
        "why_it_lands": "The sentence refuses to sanitize death with tragic nobility. Repeating the total lack of 'reason' and 'justification' forces the reader to confront the brute, unredeemed absurdity of physical agony.",
        "tags": ["understatement", "grief", "staccato", "candor"]
    },

    # Mary Shelley — Frankenstein
    {
        "quote": "Alas! why does man boast of sensibilities superior to those apparent in the brute; it only renders them more necessary beings.",
        "author": "Mary Shelley",
        "work": "Frankenstein",
        "year": 1818,
        "translator": None,
        "hook": "How to turn intellectual superiority into an instrument of torment.",
        "why_it_lands": "Shelley inverts the Enlightenment conceit of human reason. Rather than elevating humanity, refined sensibility merely multiplies our avenues for grief, leaving humankind far more fragile than instinctual beasts.",
        "tags": ["reversal", "philosophy", "irony", "Enlightenment"]
    },
    {
        "quote": "He appeared at one time a mere scion of the evil principle, and at another as all that can be conceived of noble and godlike.",
        "author": "Mary Shelley",
        "work": "Frankenstein",
        "year": 1818,
        "translator": None,
        "hook": "How to balance dual extremes across a single rhythmic sentence.",
        "why_it_lands": "The balanced clauses hold the creature's monstrosity and angelic nobility in simultaneous suspension. The classical cadence forces the reader to acknowledge both realities without collapsing one into the other.",
        "tags": ["antithesis", "syntax", "character-voice", "dualism"]
    },
    {
        "quote": "It is well. I go; but remember, I shall be with you on your wedding-night.",
        "author": "Mary Shelley",
        "work": "Frankenstein",
        "year": 1818,
        "translator": None,
        "hook": "How to deliver lethal menace in ten monosyllabic beats.",
        "why_it_lands": "A terrifying threat delivered with icy formal calm. The phrase 'I shall be with you' borrows the language of marital intimacy and perverts it into an inescapable sentence of execution.",
        "tags": ["dialogue-craft", "understatement", "foreshadowing", "chilling"]
    },
    {
        "quote": "Life is obstinate, and clings closest where it is most hated.",
        "author": "Mary Shelley",
        "work": "Frankenstein",
        "year": 1818,
        "translator": None,
        "hook": "How to personify vitality as an unwelcome parasite.",
        "why_it_lands": "Shelley subverts the natural instinct to celebrate survival. Describing life as an obstinate, clinging presence where existence itself has become abhorrent captures the profound agony of prolonged grief.",
        "tags": ["personification", "aphorism", "grief", "irony"]
    },

    # Oscar Wilde — The Picture of Dorian Gray
    {
        "quote": "Books are well written, or badly written. That is all.",
        "author": "Oscar Wilde",
        "work": "The Picture of Dorian Gray",
        "year": 1890,
        "translator": None,
        "hook": "How to demolish moral censorship with an eight-word verdict.",
        "why_it_lands": "The supreme manifesto of Aestheticism. By reducing all literary criticism to craft execution alone, Wilde strips moralistic scolds of their authority with devastating, icy brevity.",
        "tags": ["craft-of-writing", "aphorism", "economy", "clarity"]
    },
    {
        "quote": "Nothing can cure the soul but the senses, just as nothing can cure the senses but the soul.",
        "author": "Oscar Wilde",
        "work": "The Picture of Dorian Gray",
        "year": 1890,
        "translator": None,
        "hook": "How to craft a chiasmus that locks two opposites in mutual dependency.",
        "why_it_lands": "A textbook chiasmus where soul and sense mirror and heal each other. The symmetrical syntactic turn gives the radical hedonism an air of inevitable spiritual balance.",
        "tags": ["chiasmus", "syntax", "aphorism", "sensory-detail"]
    },
    {
        "quote": "When one is in love, one always begins by deceiving one’s self, and one always ends by deceiving others. That is what the world calls a romance.",
        "author": "Oscar Wilde",
        "work": "The Picture of Dorian Gray",
        "year": 1890,
        "translator": None,
        "hook": "How to trace the trajectory of romantic deceit with cynical precision.",
        "why_it_lands": "Lord Henry structures romance as a two-act farce: self-delusion followed by public fraud. The deadpan punchline ('That is what the world calls a romance') treats societal sentimentality as mass delusion.",
        "tags": ["wit", "cynicism", "syntax", "satire"]
    },
    {
        "quote": "A cigarette is the perfect type of a perfect pleasure. It is exquisite, and it leaves one unsatisfied. What more can one want?",
        "author": "Oscar Wilde",
        "work": "The Picture of Dorian Gray",
        "year": 1890,
        "translator": None,
        "hook": "How to redefine desire around intentional insufficiency.",
        "why_it_lands": "Wilde identifies the genius of addictive aesthetics: true luxury doesn't satiate; it whets the appetite while remaining incomplete. The concluding rhetorical question elevates frustration into an art form.",
        "tags": ["paradox", "wit", "hedonism", "voice"]
    }
]

def main():
    with open(QUOTE_BANK_PATH, "r", encoding="utf-8") as f:
        quote_bank = json.load(f)

    existing_quotes = {q["quote"].strip() for q in quote_bank}
    added = 0
    for nq in NEW_QUOTES:
        if nq["quote"].strip() not in existing_quotes:
            quote_bank.append(nq)
            existing_quotes.add(nq["quote"].strip())
            added += 1

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(quote_bank, f, indent=2, ensure_ascii=False)

    print(f"Added {added} new quotes. Total in quote-bank.json: {len(quote_bank)}")

if __name__ == "__main__":
    main()
