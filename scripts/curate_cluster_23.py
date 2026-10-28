# scripts/curate_cluster_23.py — Curates 20 craft quotes from Cluster 23 (Philosophical Rigor, Wit & Rural Friction)
# Usage: python3 scripts/curate_cluster_23.py
# Requires: json, os

import json
import os

QUOTE_BANK_PATH = "content/quote-bank.json"

VETTED_CLUSTER_23 = [
    # 1. Oliver Burkeman — The Antidote: Happiness for People Who Can't Stand Positive Thinking (2012)
    {
        "quote": "‘Inspiration is for amateurs,’ the artist Chuck Close once memorably observed. ‘The rest of us just show up and get to work.’",
        "author": "Oliver Burkeman",
        "work": "The Antidote",
        "year": 2012,
        "translator": None,
        "hook": "How to strip creative output of mystical romance through working-class pragmatism.",
        "why_it_lands": "Burkeman quotes painter Chuck Close to dismantle the myth of the muse, reframing creative mastery not as a divine lightning strike, but as the stubborn, daily habit of punching the clock.",
        "tags": ["work-ethic", "candor", "discipline", "craft"]
    },
    {
        "quote": "You’re never going to erase the groundlessness. You’re never going to have a neat, sweet little picture with no messiness.",
        "author": "Oliver Burkeman",
        "work": "The Antidote",
        "year": 2012,
        "translator": None,
        "hook": "How to puncture perfectionist control through parallel negative assertions.",
        "why_it_lands": "Burkeman confronts the underlying anxiety of self-improvement culture, arguing that the desire to solve life's fundamental messiness is itself the primary engine of distress.",
        "tags": ["candor", "stoicism", "acceptance", "clarity"]
    },
    {
        "quote": "‘Failure is the distinguishing feature of corporate life,’ writes the economist Paul Ormerod, at the start of his book Why Most Things Fail, but in this sense corporate life is merely a microcosm of the whole of life.",
        "author": "Oliver Burkeman",
        "work": "The Antidote",
        "year": 2012,
        "translator": None,
        "hook": "How to normalize systemic failure as the baseline condition of reality.",
        "why_it_lands": "Burkeman scales an economic observation into an existential law, transforming failure from a personal deficiency into the universal operating background of all human enterprise.",
        "tags": ["perspective", "stoicism", "realism", "philosophy"]
    },
    {
        "quote": "Death was in the air, and all was well.",
        "author": "Oliver Burkeman",
        "work": "The Antidote",
        "year": 2012,
        "translator": None,
        "hook": "How to reconcile mortality with serene equanimity in eight words.",
        "why_it_lands": "Burkeman captures the quiet catharsis of the memento mori tradition, demonstrating that confronting the absolute boundary of life dispels anxiety rather than causing it.",
        "tags": ["brevity", "mortality", "paradox", "equanimity"]
    },

    # 2. William Zinsser — On Writing Well (1976)
    {
        "quote": "Clutter is the disease of American writing. We are a society strangling in unnecessary words, circular constructions, pompous frills and meaningless jargon.",
        "author": "William Zinsser",
        "work": "On Writing Well",
        "year": 1976,
        "translator": None,
        "hook": "How to diagnose verbal excess as a cultural epidemic.",
        "why_it_lands": "Zinsser opens his assault on poor prose with clinical urgency, treating wordiness not as a harmless stylistic tic, but as a suffocating pathology choking clarity.",
        "tags": ["editing", "clarity", "jargon", "craft"]
    },
    {
        "quote": "Writing is hard work. A clear sentence is no accident. Very few sentences come out right the first time, or even the third time. Remember this in moments of despair. If you find that writing is hard, it’s because it is hard.",
        "author": "William Zinsser",
        "work": "On Writing Well",
        "year": 1976,
        "translator": None,
        "hook": "How to console the struggling writer with unvarnished candor.",
        "why_it_lands": "Zinsser dispels the beginner's shame of slow composition, providing reassurance not through false cheer, but by validating that friction is the inherent nature of the work.",
        "tags": ["encouragement", "revision", "candor", "craft"]
    },
    {
        "quote": "The secret of good writing is to strip every sentence to its cleanest components. Every word that serves no function, every long word that could be a short word, every adverb that carries the same meaning that’s already in the verb, every passive construction that leaves the reader uncertain of who is doing what—these are the thousand and one adulterants that weaken the strength of a sentence.",
        "author": "William Zinsser",
        "work": "On Writing Well",
        "year": 1976,
        "translator": None,
        "hook": "How to catalogue prose adulterants through relentless parallel clauses.",
        "why_it_lands": "Zinsser inventories the enemies of vitality in a single rolling sentence, demonstrating that strong style is not decorative addition, but rigorous subtraction.",
        "tags": ["subtraction", "revision", "syntax", "catalogue"]
    },
    {
        "quote": "Look for the lead in your writing. If it’s buried in the fourth paragraph, dig it out and put it where it belongs: right at the beginning.",
        "author": "William Zinsser",
        "work": "On Writing Well",
        "year": 1976,
        "translator": None,
        "hook": "How to rescue buried substance with excavation mechanics.",
        "why_it_lands": "Zinsser warns writers against the throat-clearing habits of essay drafts, ordering them to treat their best idea not as a delayed conclusion, but as the front door.",
        "tags": ["openings", "editing", "structure", "clarity"]
    },

    # 3. Albert Camus — The Myth of Sisyphus (1942)
    {
        "quote": "The absurd is born of this confrontation between the human need and the unreasonable silence of the world.",
        "author": "Albert Camus",
        "work": "The Myth of Sisyphus",
        "year": 1942,
        "translator": "Justin O'Brien",
        "hook": "How to define the absurd through a stark acoustic confrontation.",
        "why_it_lands": "Camus locates absurdity not in human consciousness alone nor in the physical cosmos, but in the irreconcilable friction between man's cry for meaning and the cosmos's unreasonable silence.",
        "tags": ["definition", "existentialism", "philosophy", "clarity"]
    },
    {
        "quote": "Living, naturally, is never easy. You continue making the gestures commanded by existence for many reasons, the first of which is habit.",
        "author": "Albert Camus",
        "work": "The Myth of Sisyphus",
        "year": 1942,
        "translator": "Justin O'Brien",
        "hook": "How to expose human survival as a series of mechanical physical reflexes.",
        "why_it_lands": "Camus strips biological continuation of romantic nobility, showing that we often persist in life simply because the daily momentum of physical habit precedes conscious philosophical consent.",
        "tags": ["candor", "habit", "understatement", "psychology"]
    },
    {
        "quote": "It is not to be built up, but to be burned up.",
        "author": "Albert Camus",
        "work": "The Myth of Sisyphus",
        "year": 1942,
        "translator": "Justin O'Brien",
        "hook": "How to contrast monumental accumulation with incandescent vitality in eleven words.",
        "why_it_lands": "Camus inverts the classical ideal of building an enduring legacy, arguing that life is not a monument to be assembled, but a finite fuel meant to be consumed with fierce intensity.",
        "tags": ["antithesis", "verbs", "vitality", "brevity"]
    },
    {
        "quote": "There is only one really serious philosophical problem, and that is suicide. Deciding whether or not life is worth living is to answer the fundamental question in philosophy. All other questions follow.",
        "author": "Albert Camus",
        "work": "The Myth of Sisyphus",
        "year": 1942,
        "translator": "Justin O'Brien",
        "hook": "How to open a philosophical treatise with maximum existential stakes.",
        "why_it_lands": "Camus dismisses centuries of metaphysical debate in two sentences, subordinating every intellectual enquiry to the urgent personal decision of whether to stay alive.",
        "tags": ["opening", "stakes", "clarity", "philosophy"]
    },

    # 4. Perumal Murugan — One Part Woman (2010)
    {
        "quote": "Kali’s hands are like large, rugged sieves. When they touch my cheek, my love pours forth despite the roughness of their touch.",
        "author": "Perumal Murugan",
        "work": "One Part Woman",
        "year": 2010,
        "translator": "Aniruddhan Vasudevan",
        "hook": "How to depict rural intimacy through agrarian tactile imagery.",
        "why_it_lands": "Murugan compares a husband's calloused hands to farming sieves, transforming manual roughness from an obstacle into the very vessel through which tender love is filtered.",
        "tags": ["simile", "sensory", "tenderness", "setting"]
    },
    {
        "quote": "Should I put a child on her lap the month after the wedding? I can only drop a grinding stone into her lap. Can’t she be patient for a year or two? We are young.",
        "author": "Perumal Murugan",
        "work": "One Part Woman",
        "year": 2010,
        "translator": "Aniruddhan Vasudevan",
        "hook": "How to dramatize societal fertility pressure with a crushing domestic weapon.",
        "why_it_lands": "The abrupt substitution of a heavy granite grinding stone for an unborn infant captures the brutal, unyielding pressure of village family expectations.",
        "tags": ["rhetorical-question", "domestic-imagery", "pressure", "dialogue"]
    },
    {
        "quote": "We don’t expect our children to take care of us when we are old. We only ask that there be someone to perform the last rites when we are gone.",
        "author": "Perumal Murugan",
        "work": "One Part Woman",
        "year": 2010,
        "translator": "Aniruddhan Vasudevan",
        "hook": "How to reveal the subterranean terror behind parental obsession.",
        "why_it_lands": "Murugan strips the desire for offspring of sentimental family romanticism, exposing the raw existential anxiety: not needing support during life, but fearing the lack of a ritual witness at the funeral pyre.",
        "tags": ["candor", "culture", "mortality", "lineage"]
    },
    {
        "quote": "‘Come to me with a new face, one I am not familiar with,’ she prayed.",
        "author": "Perumal Murugan",
        "work": "One Part Woman",
        "year": 2010,
        "translator": "Aniruddhan Vasudevan",
        "hook": "How to charge a religious prayer with terrifying psychological dread.",
        "why_it_lands": "The plea for the divine stranger at the Chariot Festival strips the ritual of festive romanticism, exposing the unbearable dread of submitting one's body to an anonymous deity to satisfy social convention.",
        "tags": ["prayer", "dread", "interiority", "brevity"]
    },

    # 5. Oscar Wilde — Only Dull People Are Brilliant at Breakfast (1894)
    {
        "quote": "All bad art is the result of good intentions.",
        "author": "Oscar Wilde",
        "work": "Only Dull People Are Brilliant at Breakfast",
        "year": 1894,
        "translator": None,
        "hook": "How to invert moral virtue into aesthetic malpractice in nine words.",
        "why_it_lands": "Wilde strikes at the core of didactic art, arguing that moral earnestness produces aesthetic failure because it subordinates creative instinct to ideological instruction.",
        "tags": ["aphorism", "inversion", "aestheticism", "craft"]
    },
    {
        "quote": "A sentimentalist is simply a man who desires to have the luxury of an emotion without paying for it.",
        "author": "Oscar Wilde",
        "work": "Only Dull People Are Brilliant at Breakfast",
        "year": 1894,
        "translator": None,
        "hook": "How to diagnose emotional sentimentality through a financial transaction metaphor.",
        "why_it_lands": "Wilde skewers emotional posturing, defining sentimentality not as tender feeling, but as unearned emotional tourism that refuses the costly moral consequences of actual love.",
        "tags": ["metaphor", "wit", "candor", "satire"]
    },
    {
        "quote": "Life is much too important a thing ever to talk seriously about it.",
        "author": "Oscar Wilde",
        "work": "Only Dull People Are Brilliant at Breakfast",
        "year": 1894,
        "translator": None,
        "hook": "How to deflect heavy moral earnestness with an elegant epigrammatic paradox.",
        "why_it_lands": "Wilde inverts conventional Victorian solemnity, suggesting that gravitas trivializes existence and that playful irony is the only dignified response to serious reality.",
        "tags": ["paradox", "wit", "epigram", "philosophy"]
    },
    {
        "quote": "Life imitates Art far more than Art imitates Life. Life holds the mirror up to Art, and either reproduces some strange type imagined by painter or sculptor, or realizes in fact what has been dreamed in fiction.",
        "author": "Oscar Wilde",
        "work": "Only Dull People Are Brilliant at Breakfast",
        "year": 1894,
        "translator": None,
        "hook": "How to overturn classical mimesis through rhetorical chiasmus.",
        "why_it_lands": "Wilde reverses Aristotle's ancient premise, asserting that human perception does not dictate artistic creation, but rather that art trains human eyes to notice fog, colors, and personalities.",
        "tags": ["chiasmus", "art-theory", "aestheticism", "vision"]
    }
]

def main():
    with open(QUOTE_BANK_PATH, "r", encoding="utf-8") as f:
        quote_bank = json.load(f)

    print(f"Existing quote bank count: {len(quote_bank)}")

    # Check for duplicates by quote prefix
    existing_quotes = {q["quote"].strip()[:50].lower() for q in quote_bank}
    
    added_count = 0
    for entry in VETTED_CLUSTER_23:
        key = entry["quote"].strip()[:50].lower()
        if key in existing_quotes:
            print(f"Skipping duplicate: {entry['work']} - {entry['quote'][:40]}...")
            continue
        quote_bank.append(entry)
        existing_quotes.add(key)
        added_count += 1

    print(f"Added {added_count} new vetted quotes from Cluster 23.")
    print(f"New quote bank total: {len(quote_bank)}")

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(quote_bank, f, indent=2, ensure_ascii=False)
        f.write("\n")

if __name__ == "__main__":
    main()
