# scripts/curate_cluster_29.py — Curates 20 craft quotes from Cluster 29 (Linguistic Determinism, Burnout & Incandescent Will)
# Usage: python3 scripts/curate_cluster_29.py
# Requires: json, os

import json
import os

QUOTE_BANK_PATH = "content/quote-bank.json"

VETTED_CLUSTER_29 = [
    # 1. Ted Chiang — Story of Your Life (1998)
    {
        "quote": "It was strange trying to learn a language that had no spoken form. Instead of practicing my pronunciation, I had taken to squeezing my eyes shut and trying to paint semagrams on the insides of my eyelids.",
        "author": "Ted Chiang",
        "work": "Story of Your Life",
        "year": 1998,
        "translator": None,
        "hook": "How to ground alien semiotics in intimate physical effort.",
        "why_it_lands": "Chiang transforms abstract linguistic theory into a visceral physical ritual, replacing vocal cord muscle memory with eyelids acting as a private, closed canvas for visual glyphs.",
        "tags": ["language", "sensory", "imagination", "craft"]
    },
    {
        "quote": "We can’t simply cut their sentences into individual words and recombine them; we’ll have to learn the rules of their script before we can write anything legible.",
        "author": "Ted Chiang",
        "work": "Story of Your Life",
        "year": 1998,
        "translator": None,
        "hook": "How to expose linear narrative bias through non-linear syntax.",
        "why_it_lands": "Chiang illustrates the challenge of holistic thought: language that cannot be atomized into modular words requires grasping the complete arc of meaning before laying down a single mark.",
        "tags": ["writing", "mind", "language", "structure"]
    },
    {
        "quote": "The physical universe was a language with a perfectly ambiguous grammar. Every physical event was an utterance that could be parsed in two entirely different ways, one causal and the other teleological, both valid, neither disqualifying the other.",
        "author": "Ted Chiang",
        "work": "Story of Your Life",
        "year": 1998,
        "translator": None,
        "hook": "How to harmonize scientific determinism and human agency through linguistic ambiguity.",
        "why_it_lands": "Chiang uses grammatical parsing as a metaphysical metaphor, demonstrating that human cause-and-effect and cosmic teleological purpose can coexist simultaneously without contradiction.",
        "tags": ["philosophy", "physics", "perspective", "metaphor"]
    },
    {
        "quote": "From the beginning I knew my destination, and I chose my route accordingly. But am I working toward an extreme of joy, or of pain? Will I achieve a minimum, or a maximum?",
        "author": "Ted Chiang",
        "work": "Story of Your Life",
        "year": 1998,
        "translator": None,
        "hook": "How to infuse variational physics with emotional resonance.",
        "why_it_lands": "Chiang adapts Fermat's principle of least time into an aching existential inquiry, asking whether embracing a predetermined future measures out minimum sorrow or maximum love.",
        "tags": ["physics", "emotion", "time", "reflection"]
    },

    # 2. Byung-Chul Han — The Burnout Society (2010)
    {
        "quote": "Harm does not come from negativity alone, but also from positivity—not just from the Other or the foreign, but also from the Same.",
        "author": "Byung-Chul Han",
        "work": "The Burnout Society",
        "year": 2010,
        "translator": "Erik Butler",
        "hook": "How to overturn immunological assumptions through structural paradox.",
        "why_it_lands": "Han diagnoses the modern condition by subverting conventional sociology: violence in late capitalism no longer attacks from external hostility, but suffocates from excessive sameness and self-generated conformity.",
        "tags": ["philosophy", "culture", "insight", "paradox"]
    },
    {
        "quote": "The violence of positivity does not presume or require hostility. It unfolds specifically in a permissive and pacified society.",
        "author": "Byung-Chul Han",
        "work": "The Burnout Society",
        "year": 2010,
        "translator": "Erik Butler",
        "hook": "How to identify predatory coercion beneath institutional gentleness.",
        "why_it_lands": "Han warns that systemic exhaustion operates best not under totalitarian oppression, but within voluntary, celebratory environments where individuals exploit themselves willingly.",
        "tags": ["society", "clarity", "politics", "modernity"]
    },
    {
        "quote": "Boredom is a warm gray fabric on the inside, with the most lustrous and colorful silks; in this fabric we wrap ourselves when we dream.",
        "author": "Byung-Chul Han",
        "work": "The Burnout Society",
        "year": 2010,
        "translator": "Erik Butler",
        "hook": "How to elevate boredom into a rich sensory sanctuary.",
        "why_it_lands": "Quoting Walter Benjamin, Han contrasts the hyperactive twitching of digital attention against the quiet, luxurious texture of unoccupied time where imagination actually takes root.",
        "tags": ["imagery", "stillness", "metaphor", "rest"]
    },
    {
        "quote": "Already the two were irresistibly recoiling, each into a private tiredness, not ours, but mine over here and yours over there.",
        "author": "Byung-Chul Han",
        "work": "The Burnout Society",
        "year": 2010,
        "translator": "Erik Butler",
        "hook": "How to capture the alienating, divisive nature of modern fatigue.",
        "why_it_lands": "Han borrows Handke's spatial phrasing to reveal how capitalist exhaustion isolates human beings into separate solitudes, destroying the communal solidarity of shared rest.",
        "tags": ["isolation", "psychology", "rhythm", "society"]
    },

    # 3. Oscar Wilde — The Picture of Dorian Gray (1890)
    {
        "quote": "It was a poisonous book. The heavy odour of incense seemed to cling about its pages and to trouble the brain.",
        "author": "Oscar Wilde",
        "work": "The Picture of Dorian Gray",
        "year": 1890,
        "translator": None,
        "hook": "How to dramatize intellectual seduction as atmospheric intoxication.",
        "why_it_lands": "Wilde renders literary influence not as cognitive persuasion, but as a fragrant, physical contagion that infiltrates the senses and intoxicates the nervous system.",
        "tags": ["sensory", "gothic", "imagery", "reading"]
    },
    {
        "quote": "Things that he had dimly dreamed of were suddenly made real to him. Things of which he had never dreamed were gradually revealed.",
        "author": "Oscar Wilde",
        "work": "The Picture of Dorian Gray",
        "year": 1890,
        "translator": None,
        "hook": "How to structure psychological awakening across parallel antithetical clauses.",
        "why_it_lands": "Wilde balances the progression of temptation through mirrored cadence: moving from the validation of secret desires to the dangerous revelation of sins hitherto unimagined.",
        "tags": ["parallelism", "craft", "rhythm", "psychology"]
    },
    {
        "quote": "‘You ask me why Berwick leaves a room when I enter it. It is because I know everything about his life, not because he knows anything about mine.’",
        "author": "Oscar Wilde",
        "work": "The Picture of Dorian Gray",
        "year": 1890,
        "translator": None,
        "hook": "How to expose asymmetric social power through conversational retort.",
        "why_it_lands": "Wilde demonstrates how silence and private knowledge intimidate far more ruthlessly than open gossip: total exposure on one side creates panic in the presence of an opaque observer.",
        "tags": ["dialogue", "power", "wit", "irony"]
    },
    {
        "quote": "To get back one’s youth, one has merely to repeat one’s follies.",
        "author": "Oscar Wilde",
        "work": "The Picture of Dorian Gray",
        "year": 1890,
        "translator": None,
        "hook": "How to deliver biting social satire in a single paradoxical maxim.",
        "why_it_lands": "Wilde subverts moral earnestness with characteristic effrontery, suggesting that vitality belongs not to hard-won wisdom, but to the reckless surrender to past mistakes.",
        "tags": ["epigram", "wit", "paradox", "brevity"]
    },

    # 4. Friedrich Nietzsche — On the Genealogy of Morals (1887)
    {
        "quote": "We are unknown, we knowers, ourselves to ourselves: this has its own good reason.",
        "author": "Friedrich Nietzsche",
        "work": "On the Genealogy of Morals",
        "year": 1887,
        "translator": "Walter Kaufmann",
        "hook": "How to open philosophical inquiry with an ironic epistemological paradox.",
        "why_it_lands": "Nietzsche begins with unforgettable chiasmic dissonance ('unknown, we knowers'), dismantling intellectual hubris by suggesting our compulsive quest to analyze the world is an elaborate evasion of self-examination.",
        "tags": ["opening", "philosophy", "insight", "epistemology"]
    },
    {
        "quote": "The artist is after all merely the presupposition of his work, the womb, the soil, in certain cases the dung and manure, on which and out of which it grows—and consequently, in most cases, something that must be forgotten if the work itself is to be enjoyed.",
        "author": "Friedrich Nietzsche",
        "work": "On the Genealogy of Morals",
        "year": 1887,
        "translator": "Walter Kaufmann",
        "hook": "How to separate artistic majesty from human vanity through agricultural metaphor.",
        "why_it_lands": "Nietzsche demystifies creative genius, reducing the author to mere biological compost whose personal flaws must be buried so that the fruit of the art can be tasted clean.",
        "tags": ["metaphor", "art", "craft", "truth"]
    },
    {
        "quote": "The man who is truthful in that daring and extreme fashion, which is the presupposition of the faith in science, asserts thereby a different world from that of life, nature, and history; and in so far as he asserts the existence of that different world, come, must he not similarly repudiate its counterpart, this world, our world?",
        "author": "Friedrich Nietzsche",
        "work": "On the Genealogy of Morals",
        "year": 1887,
        "translator": "Walter Kaufmann",
        "hook": "How to interrogate scientific objectivity as a covert metaphysical longing.",
        "why_it_lands": "Nietzsche unmasks absolute empiricism, arguing that an unbending demand for objective truth carries an ascetic hostility toward the chaotic, imperfect flux of biological life.",
        "tags": ["philosophy", "science", "argument", "depth"]
    },
    {
        "quote": "What if this belief becomes more and more incredible, what if nothing proves itself to be divine, unless it be error, blindness, lies—what if God Himself proved Himself to be our oldest lie?",
        "author": "Friedrich Nietzsche",
        "work": "On the Genealogy of Morals",
        "year": 1887,
        "translator": "Walter Kaufmann",
        "hook": "How to escalate existential stakes through relentless hypothetical questioning.",
        "why_it_lands": "Nietzsche stacks three escalating conditional clauses, daring the reader to confront the radical possibility that civilization's sacred sanctities were sustained solely by useful falsehoods.",
        "tags": ["voice", "intensity", "philosophy", "rhetoric"]
    },

    # 5. James Gleick — Chaos: Making a New Science (1987)
    {
        "quote": "It is hard to break the habit of thinking of things in terms of how big they are and how long they last.",
        "author": "James Gleick",
        "work": "Chaos: Making a New Science",
        "year": 1987,
        "translator": None,
        "hook": "How to challenge spatial and temporal scale with direct colloquial simplicity.",
        "why_it_lands": "Gleick diagnoses humanity's fundamental perceptual rut: our sensory intuition is enslaved to Euclidean dimensions and linear clocks, blinding us to recursive structures that repeat identically at every magnification.",
        "tags": ["perspective", "science", "brevity", "clarity"]
    },
    {
        "quote": "By the time 1,000 orbits have been drawn, the attractor has become an impenetrably tangled skein.",
        "author": "James Gleick",
        "work": "Chaos: Making a New Science",
        "year": 1987,
        "translator": None,
        "hook": "How to visualize complex mathematics through textile imagery.",
        "why_it_lands": "Gleick translates differential equations and phase space trajectories into the tactile familiarity of tangled yarn, allowing readers to 'see' deterministic chaos as a physical thread weaving its own envelope.",
        "tags": ["metaphor", "visualization", "craft", "science"]
    },
    {
        "quote": "The more random a data stream, the more information would be conveyed by each new bit.",
        "author": "James Gleick",
        "work": "Chaos: Making a New Science",
        "year": 1987,
        "translator": None,
        "hook": "How to distill information theory into an arresting scientific paradox.",
        "why_it_lands": "Gleick turns common sense on its head: predictable communication carries almost zero news, whereas total unpredictability demands maximum cognitive bandwidth and delivers pure information.",
        "tags": ["information", "paradox", "brevity", "clarity"]
    },
    {
        "quote": "‘When you reach an equilibrium in biology you’re dead,’ he said.",
        "author": "James Gleick",
        "work": "Chaos: Making a New Science",
        "year": 1987,
        "translator": None,
        "hook": "How to deflate scientific reverence for equilibrium through mortal finality.",
        "why_it_lands": "Gleick quotes a dynamicist to dismantle the romantic myth of biological harmony: living organisms maintain life precisely by staying far from static equilibrium; true equilibrium is the stillness of a grave.",
        "tags": ["biology", "aphorism", "truth", "science"]
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

    for item in VETTED_CLUSTER_29:
        if item["quote"].strip() not in existing_quotes:
            bank.append(item)
            existing_quotes.add(item["quote"].strip())
            added_count += 1
        else:
            print(f"Duplicate found, skipping: {item['quote'][:40]}...")

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)

    print(f"Successfully added {added_count} vetted quotes from Cluster 29.")
    print(f"New total quote bank size: {len(bank)}")

if __name__ == "__main__":
    main()
