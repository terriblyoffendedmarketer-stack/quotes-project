# scripts/curate_cluster_36.py — Curates 20 craft quotes from Cluster 36 (Epistolary Intimacy, Surreal Satire & Fearless Will)
# Usage: python3 scripts/curate_cluster_36.py
# Requires: json, os

import json
import os

QUOTE_BANK_PATH = "content/quote-bank.json"

VETTED_CLUSTER_36 = [
    # 1. Perumal Murugan — Poonachi: Or the Story of a Black Goat (2016), trans. N. Kalyan Raman
    {
        "quote": "If he was in possession of a kid whose ears were not pierced, he might be an enemy of the regime.",
        "author": "Perumal Murugan",
        "work": "Poonachi: Or the Story of a Black Goat",
        "year": 2016,
        "translator": "N. Kalyan Raman",
        "hook": "How to reveal totalitarian paranoia through animal livestock regulation.",
        "why_it_lands": "Murugan satirizes authoritarian control through rural fable: the state's invasive surveillance extends even to ear-notches on newborn goat kids, where an unpierced ear becomes treason against the sovereign.",
        "tags": ["satire", "fable", "totalitarianism", "state"]
    },
    {
        "quote": "They had no other wish than to pass the remainder of their lives as serenely as they had done all these years.",
        "author": "Perumal Murugan",
        "work": "Poonachi: Or the Story of a Black Goat",
        "year": 2016,
        "translator": "N. Kalyan Raman",
        "hook": "How to sketch pastoral vulnerability through modest domestic desire.",
        "why_it_lands": "Murugan captures the fragile serenity of peasant existence: when characters ask for nothing more than undisturbed routine, the sentence reads as an ominous prelude to inevitable intrusion.",
        "tags": ["understatement", "vulnerability", "pastoral", "peace"]
    },
    {
        "quote": "It was beyond her understanding. Did the joy of mating amount to no more than this?",
        "author": "Perumal Murugan",
        "work": "Poonachi: Or the Story of a Black Goat",
        "year": 2016,
        "translator": "N. Kalyan Raman",
        "hook": "How to question biological instinct through innocent animal perspective.",
        "why_it_lands": "Murugan defamiliarizes animal reproduction through an innocent black goat: physical copulation is stripped of romantic mythology, leaving only brief, baffling bodily frenzy that leaves the animal unfulfilled.",
        "tags": ["fable", "disillusion", "innocence", "nature"]
    },
    {
        "quote": "There has been no rainfall anywhere in the world of the Asuras.",
        "author": "Perumal Murugan",
        "work": "Poonachi: Or the Story of a Black Goat",
        "year": 2016,
        "translator": "N. Kalyan Raman",
        "hook": "How to summon mythological drought in eleven words.",
        "why_it_lands": "Murugan merges peasant climate devastation with cosmic myth: drought is not merely local bad weather, but a mythological curse burning across an entire realm of demons and outcast mortals.",
        "tags": ["myth", "drought", "landscape", "brevity"]
    },

    # 2. Kurt Vonnegut — Breakfast of Champions (1973)
    {
        "quote": "Some people say there is no such thing as progress. The fact that human beings are now the only animals left in the world represents, I admit, a confusing sort of victory.",
        "author": "Kurt Vonnegut",
        "work": "Breakfast of Champions",
        "year": 1973,
        "translator": None,
        "hook": "How to dismantle ecological dominion through bitter ironical triumph.",
        "why_it_lands": "Vonnegut skewers human exceptionalism with deadpan comic despair: driving every competing species to extinction is technically an evolutionary win, but one that leaves humanity ruling a dead wasteland.",
        "tags": ["satire", "irony", "ecology", "humor"]
    },
    {
        "quote": "I shrank the universe down to a ball with a diameter of exactly one light year. I blew it up.",
        "author": "Kurt Vonnegut",
        "work": "Breakfast of Champions",
        "year": 1973,
        "translator": None,
        "hook": "How to execute a cosmic demolition in two sentences.",
        "why_it_lands": "Vonnegut flaunts authorial omnipotence with reckless, playful abandon: shrinking deep space down into a celestial toy and detonating it highlights the exhilarating absurdity of godlike fictional power.",
        "tags": ["metafiction", "voice", "cosmic", "absurdity"]
    },
    {
        "quote": "All molecules stopped functioning for a moment, and each of them sought to gain distance between itself and its neighbors.",
        "author": "Kurt Vonnegut",
        "work": "Breakfast of Champions",
        "year": 1973,
        "translator": None,
        "hook": "How to describe nervous breakdown at the atomic scale.",
        "why_it_lands": "Vonnegut dramatizes panic not through psychological interiority, but through physical chemistry: emotional collapse becomes a microscopic mutiny where every individual atom flees contact with its peers.",
        "tags": ["breakdown", "science", "metaphor", "wit"]
    },
    {
        "quote": "Life was an experiment by which the Creator of the Universe intended to test a new creature He planned to introduce into the universe. It was a creature that had the ability to make choices.",
        "author": "Kurt Vonnegut",
        "work": "Breakfast of Champions",
        "year": 1973,
        "translator": None,
        "hook": "How to frame human free will as an unpredictable cosmic field test.",
        "why_it_lands": "Vonnegut reframes moral responsibility as laboratory prototyping: autonomy isn't a holy gift, but a hazardous biological feature whose chaotic outcomes baffle the divine engineer himself.",
        "tags": ["free will", "parable", "philosophy", "cosmic"]
    },

    # 3. Malala Yousafzai — I Am Malala (2013)
    {
        "quote": "No Pashtun leaves his land of his own sweet will.",
        "author": "Malala Yousafzai",
        "work": "I Am Malala",
        "year": 2013,
        "translator": None,
        "hook": "How to convey ancestral displacement through cultural proverb.",
        "why_it_lands": "Yousafzai captures the agony of exile in nine words: migration isn't a search for cosmopolitan novelty, but a violent tearing away from ancestral mountain soil that only existential necessity can force.",
        "tags": ["exile", "homeland", "proverb", "brevity"]
    },
    {
        "quote": "They can stop us going to school but they can’t stop us learning.",
        "author": "Malala Yousafzai",
        "work": "I Am Malala",
        "year": 2013,
        "translator": None,
        "hook": "How to sever institutional education from autonomous intellectual will.",
        "why_it_lands": "Yousafzai draws an airtight philosophical distinction: physical military checkpoints can padlock schoolhouse gates, but no fascist regime can confiscate an individual's curiosity.",
        "tags": ["courage", "learning", "defiance", "truth"]
    },
    {
        "quote": "Education is neither Eastern nor Western, it is human.",
        "author": "Malala Yousafzai",
        "work": "I Am Malala",
        "year": 2013,
        "translator": None,
        "hook": "How to rescue universal knowledge from geopolitical tribalism.",
        "why_it_lands": "Yousafzai dismantles fundamentalist propaganda with crisp moral geometry: intellectual enlightenment carries no sectarian passport, belonging inherently to every living human mind.",
        "tags": ["clarity", "education", "humanism", "truth"]
    },
    {
        "quote": "If the men cannot win the battle, then the women will come forth and win you an honour.",
        "author": "Malala Yousafzai",
        "work": "I Am Malala",
        "year": 2013,
        "translator": None,
        "hook": "How to overthrow patriarchal martial vanity through ancient battle cry.",
        "why_it_lands": "Yousafzai invokes historical Pashtun folklore to rebuke male chauvinism: when warriors fail to defend the community, female courage steps onto the frontlines to salvage communal dignity.",
        "tags": ["defiance", "history", "voice", "courage"]
    },

    # 4. Kurt Vonnegut — The Sirens of Titan (1959)
    {
        "quote": "There is no reason why good cannot triumph as often as evil. The triumph of anything is a matter of organization.",
        "author": "Kurt Vonnegut",
        "work": "The Sirens of Titan",
        "year": 1959,
        "translator": None,
        "hook": "How to demystify moral triumph into bureaucratic logistics.",
        "why_it_lands": "Vonnegut strips ethical battles of Hollywood grandeur: righteousness loses to wickedness not through cosmic malice, but simply because villainy possesses better filing cabinets and organizational discipline.",
        "tags": ["morality", "satire", "organization", "cynicism"]
    },
    {
        "quote": "He doesn’t care what happens to you. He didn’t go to any trouble to get you here safe and sound, any more than He would go to the trouble to kill you.",
        "author": "Kurt Vonnegut",
        "work": "The Sirens of Titan",
        "year": 1959,
        "translator": None,
        "hook": "How to deliver cosmic indifference with chilling theological economy.",
        "why_it_lands": "Vonnegut replaces the vengeful deity with something far more terrifying: absolute, disinterested divine apathy that doesn't even bother to hold a grudge.",
        "tags": ["theology", "cosmic", "satire", "truth"]
    },
    {
        "quote": "Things fly this way and that, my boy, with or without messages. It’s chaos, and no mistake, for the Universe is just being born.",
        "author": "Kurt Vonnegut",
        "work": "The Sirens of Titan",
        "year": 1959,
        "translator": None,
        "hook": "How to comfort existential vertigo through cosmic infancy.",
        "why_it_lands": "Vonnegut dissolves panic over universal meaninglessness with warm paternal humor: erratic chaos isn't evidence of broken design, but the messy, bubbling nursery of a universe that hasn't finished hatching.",
        "tags": ["chaos", "cosmic", "humor", "wisdom"]
    },
    {
        "quote": "There is nowhere else for you to go, nothing else for you to do. By putting one foot in front of the other, while we watch in silence, you will make of yourself the most memorable, magnificent, and meaningful human being of modern times.",
        "author": "Kurt Vonnegut",
        "work": "The Sirens of Titan",
        "year": 1959,
        "translator": None,
        "hook": "How to craft a hollow heroic prophecy wrapped in fatalistic mockery.",
        "why_it_lands": "Vonnegut parodies epic grandeur with chilling fatalism: heroism is reduced to compulsory mechanical marching, cheered on by cosmic observers who find human struggle pathetic and amusing.",
        "tags": ["irony", "heroism", "satire", "fatalism"]
    },

    # 5. Virginia Woolf and Vita Sackville-West — Love Letters: Virginia Woolf and Vita Sackville-West (2021)
    {
        "quote": "There is a difference between being very sorry and sorry-to-matter.",
        "author": "Virginia Woolf and Vita Sackville-West",
        "work": "Love Letters: Virginia Woolf and Vita Sackville-West",
        "year": 2021,
        "translator": None,
        "hook": "How to dissect emotional sincerity across twelve syllables.",
        "why_it_lands": "Woolf isolates the boundary between polite social etiquette and genuine heartbreak: conventional condolences cost nothing, but genuine sorrow alters the emotional architecture of the sender.",
        "tags": ["nuance", "emotion", "truth", "brevity"]
    },
    {
        "quote": "I contrast my illiterate writing with your scholarly one, and am ashamed. So dull, I am; dull outwardly, at least; all oafish and muddy; but not dull inside.",
        "author": "Virginia Woolf and Vita Sackville-West",
        "work": "Love Letters: Virginia Woolf and Vita Sackville-West",
        "year": 2021,
        "translator": None,
        "hook": "How to defend inner incandescent vitality beneath self-deprecating mud.",
        "why_it_lands": "Vita Sackville-West captures epistolary vulnerability with disarming honesty: confessing outward awkwardness and muddy provincialism only sharpens the fierce, stubborn defense of her private inner brilliance.",
        "tags": ["epistolary", "vulnerability", "voice", "contrast"]
    },
    {
        "quote": "She is utterly unaffected: there is no outward adornments – she dresses quite atrociously.",
        "author": "Virginia Woolf and Vita Sackville-West",
        "work": "Love Letters: Virginia Woolf and Vita Sackville-West",
        "year": 2021,
        "translator": None,
        "hook": "How to sketch character charm through sartorial carelessness.",
        "why_it_lands": "Woolf captures Vita's unstudied aristocratic ease: genuine distinction requires no polished fashion armor, radiating instead through complete indifference to outward bourgeois dress.",
        "tags": ["character", "portrait", "wit", "fashion"]
    },
    {
        "quote": "I try to romanticise Berlin by thinking that Russia lies over there to the east. But the only tangible reminder of Russia is the piercing east wind which comes to us straight off the steppes.",
        "author": "Virginia Woolf and Vita Sackville-West",
        "work": "Love Letters: Virginia Woolf and Vita Sackville-West",
        "year": 2021,
        "translator": None,
        "hook": "How to replace poetic nostalgia with harsh physical meteorology.",
        "why_it_lands": "Vita punctures foreign romantic fantasy through icy geography: dreaming of mythic Slavic realms evaporates the instant the bitter, razor-sharp wind arrives from the barren eastern steppes.",
        "tags": ["geography", "weather", "atmosphere", "romanticism"]
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
    for q in VETTED_CLUSTER_36:
        if q["quote"].strip() not in existing_quotes:
            bank.append(q)
            existing_quotes.add(q["quote"].strip())
            added += 1
        else:
            print(f"Skipping duplicate: {q['quote'][:40]}...")

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)

    print(f"Successfully added {added} quotes from Cluster 36.")
    print(f"New quote bank total: {len(bank)}")

if __name__ == "__main__":
    main()
