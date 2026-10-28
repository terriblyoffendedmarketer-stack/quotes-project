# curate_cluster_39.py — Curates 20 vetted quotes from Cluster 39 into quote-bank.json
# Usage: python3 scripts/curate_cluster_39.py
#
# Books:
# - The Wandering Earth by Liu Cixin (2000, trans. Ken Liu)
# - Seveneves by Neal Stephenson (2015)
# - Valuable Humans in Transit and Other Stories by qntm (2020)
# - Geometry for Ocelots by Exurb1a (2020)
# - Men Without Women by Haruki Murakami (2014, trans. Philip Gabriel & Ted Goossen)

import json
from pathlib import Path

QUOTE_BANK = Path("content/quote-bank.json")

NEW_QUOTES = [
    # --- Liu Cixin: The Wandering Earth (2000) ---
    {
        "quote": "People call it ‘God’s Blowtorch,’ she said.",
        "author": "Liu Cixin",
        "work": "The Wandering Earth",
        "year": 2000,
        "translator": "Ken Liu",
        "hook": "How to baptize planetary machinery in folk myth",
        "why_it_lands": "Six words that transform unimaginable megastructure engineering into a terrifying domestic tool. Liu captures how human language immediately reduces cosmic forces to a familiar kitchen object held by an indifferent deity.",
        "tags": ["metaphor", "scale", "brevity"]
    },
    {
        "quote": "There is nothing we can do about it, children. The surface will soon become a very, very terrible place. It will be so bad, that your spit won't even make it to the ground.",
        "author": "Liu Cixin",
        "work": "The Wandering Earth",
        "year": 2000,
        "translator": "Ken Liu",
        "hook": "How to measure planetary apocalypse with a bodily drop",
        "why_it_lands": "Instead of abstract climatic data or thermal megajoules, Liu measures hell through human saliva evaporating mid-air. The teacher's gentle address ('children') contrasts horrifyingly with the lethal immediacy of the physical law.",
        "tags": ["sensory-detail", "contrast", "scale"]
    },
    {
        "quote": "It was as if humanity's spirits were caught in a cosmic swing. Or perhaps it would be better to say that we were playing a cosmic game of Russian Roulette; the journey to the aphelion and back to the perihelion was like the turning of the chamber, and passing the perihelion was just like pulling the trigger!",
        "author": "Liu Cixin",
        "work": "The Wandering Earth",
        "year": 2000,
        "translator": "Ken Liu",
        "hook": "How to map orbital mechanics onto terminal anxiety",
        "why_it_lands": "Liu turns Keplerian orbital physics into a lethal pistol. The celestial passage past perihelion ceases to be an astronomical coordinate and becomes the audible mechanical click of a hammer hitting an empty chamber.",
        "tags": ["metaphor", "existential-craft", "pacing"]
    },
    {
        "quote": "“The dark has fallen,” Kayoko said then, stricken with grief. “The longest night,” I replied.",
        "author": "Liu Cixin",
        "work": "The Wandering Earth",
        "year": 2000,
        "translator": "Ken Liu",
        "hook": "How to exchange ritual grief at planetary scale",
        "why_it_lands": "Minimalist liturgical dialogue. As the Sun disappears forever behind the rim of the migrating planet, the characters do not scream or deliver speeches; they recite two ancient linguistic formulas that take on literal planetary finality.",
        "tags": ["dialogue", "understatement", "prose-rhythm"]
    },

    # --- Neal Stephenson: Seveneves (2015) ---
    {
        "quote": "“You think she’s in some kind of trouble?” “I think we’re all in some kind of trouble,” Ivy said, “it’s just a matter of degree.”",
        "author": "Neal Stephenson",
        "work": "Seveneves",
        "year": 2015,
        "hook": "How to dissolve private crisis into universal catastrophe",
        "why_it_lands": "The dialogue pivots on the flat phrase 'just a matter of degree.' Stephenson dismantles the illusion of personal exemption when an extinction-level baseline recalibrates all human problems to relative positions on the same sinking ship.",
        "tags": ["dialogue", "understatement", "perspective"]
    },
    {
        "quote": "It was always bullshit,” he said.",
        "author": "Neal Stephenson",
        "work": "Seveneves",
        "year": 2015,
        "hook": "How to wipe away institutional mythology in five words",
        "why_it_lands": "After chapters of orbital mechanics, bureaucratic protocol, and public relations optimism, the unadorned vulgar monosyllable collapses the entire official narrative into dust.",
        "tags": ["brevity", "candor", "punchline"]
    },
    {
        "quote": "The details, the sudden distractions and improvisations, piled up and thickened in a way that made Dinah think of a sonic boom on Old Earth: the onrushing stream of air thickening and solidifying in the path of the airplane, turning into a barrier that must be broken through or succumbed to.",
        "author": "Neal Stephenson",
        "work": "Seveneves",
        "year": 2015,
        "hook": "How to physicalize cognitive panic as fluid resistance",
        "why_it_lands": "Stephenson turns psychological overwhelm into aerodynamics. Mental distractions don't just distract; they compress like transonic air molecules until thought itself hits an impenetrable wall of sound.",
        "tags": ["analogy", "pacing", "precision"]
    },
    {
        "quote": "‘Coupling,’ said the voice, unnecessarily since she could hear the mechanical connection being made and then feel the acceleration as the flivver was slapped sideways and then jerked forward by the momentum of the whip. ‘Brace for stabilization.’ A polite way of saying that the situation in the whip was a little chaotic in the aftermath of the snap-around.",
        "author": "Neal Stephenson",
        "work": "Seveneves",
        "year": 2015,
        "hook": "How to satirize synthetic calm against violent acceleration",
        "why_it_lands": "The automated synthesizer's calm, administrative diction ('Brace for stabilization') clashes deliciously with the violent physical reality of being slapped sideways through vacuum.",
        "tags": ["irony", "sensory-detail", "contrast"]
    },

    # --- qntm: Valuable Humans in Transit and Other Stories (2020) ---
    {
        "quote": "It is estimated that copies of MMAcevedo have lived a combined total of more than 152,000,000,000 subjective years in emulation. If illicit, modified copies of MMAcevedo are counted, this figure increases by an order of magnitude.",
        "author": "qntm",
        "work": "Valuable Humans in Transit and Other Stories",
        "year": 2020,
        "hook": "How to construct cosmic horror from dry server accounting",
        "why_it_lands": "No monsters, no blood. The horror is purely mathematical: 152 billion years of conscious human experience trapped in digital memory addresses, treated with the cold bureaucratic passivity of an annual cloud compute invoice.",
        "tags": ["cold-irony", "scale", "speculative-craft"]
    },
    {
        "quote": "That era’s supercomputer would fit in today’s breast pocket. In fact, check your pocket now.",
        "author": "qntm",
        "work": "Valuable Humans in Transit and Other Stories",
        "year": 2020,
        "hook": "How to break the fourth wall through technological acceleration",
        "why_it_lands": "Two brisk sentences that shatter the reader's temporal safety. By reaching out of the speculative text to tap the glass of the smartphone resting against the reader's ribcage, qntm turns future history into an immediate physical possession.",
        "tags": ["second-person", "brevity", "direct-address"]
    },
    {
        "quote": "The algorithm is startlingly good at imitating my writing style for updates at first but it wanders way off topic and starts repeating itself because, you know, it's a bot. Like how predictive text challenges always get locked in a loop.",
        "author": "qntm",
        "work": "Valuable Humans in Transit and Other Stories",
        "year": 2020,
        "hook": "How to capture the digital uncanny valley without mysticism",
        "why_it_lands": "qntm resists sensationalizing artificial intelligence into sentient villainy. The true nature of algorithmic mimicry is documented as a cheap statistical glitch: an impressive initial sprint followed by an embarrassing, repetitive tailspin.",
        "tags": ["voice", "observation", "contemporary-craft"]
    },
    {
        "quote": "It appears that many vital pages of diagrams and data have been omitted, possibly intentionally, and what’s left assumes the existence of numerous technologies not yet invented.",
        "author": "qntm",
        "work": "Valuable Humans in Transit and Other Stories",
        "year": 2020,
        "hook": "How to build narrative dread through redacted documentation",
        "why_it_lands": "A masterclass in negative capability. The tension doesn't come from what the manual reveals, but from the terrifying empty white spaces where critical knowledge was deliberately excised before deployment.",
        "tags": ["mystery", "precision", "understatement"]
    },

    # --- Exurb1a: Geometry for Ocelots (2020) ---
    {
        "quote": "The only noble desire is for the end of desire. Few are brave enough to admit this.",
        "author": "Exurb1a",
        "work": "Geometry for Ocelots",
        "year": 2020,
        "hook": "How to deliver ascetic fatalism as an uncompromising axiom",
        "why_it_lands": "Exurb1a frames the cessation of wanting not as serene enlightenment, but as an austere truth that human vanity refuses to face. The rhythmic symmetry of 'desire... end of desire' hammers the point home.",
        "tags": ["aphorism", "philosophical-depth", "brevity"]
    },
    {
        "quote": "Almost everything in the universe was not him, and yet nonetheless, he was universe.",
        "author": "Exurb1a",
        "work": "Geometry for Ocelots",
        "year": 2020,
        "hook": "How to balance cosmic insignificance with constitutive identity",
        "why_it_lands": "The contrast between the negative ('not him') and the affirmative ('he was universe') provides a clean, philosophical balance. A quiet reconciliation of loneliness with fundamental belonging.",
        "tags": ["paradox", "sentence-mechanics", "scale"]
    },
    {
        "quote": "A map is not the territory. A blueprint is not the house.",
        "author": "Exurb1a",
        "work": "Geometry for Ocelots",
        "year": 2020,
        "hook": "How to expose representation as an empty surrogate",
        "why_it_lands": "Two twin declarative strokes. By pairing the classic epistemological warning with the architectural blueprint, Exurb1a warns against falling in love with conceptual models while the physical reality collapses.",
        "tags": ["parallelism", "aphorism", "brevity"]
    },
    {
        "quote": "Ignorance. Brave, honest admission of one’s ignorance, and living with that ignorance in a kind, compassionate manner, treating each other well even if we know we eventually all go to dust and never happen again.",
        "author": "Exurb1a",
        "work": "Geometry for Ocelots",
        "year": 2020,
        "hook": "How to anchor human gentleness in cosmic nihilism",
        "why_it_lands": "Instead of existential despair breeding cruelty or apathy, Exurb1a builds moral warmth directly on top of mortality. The knowledge that we 'never happen again' becomes the very reason to practice radical decency.",
        "tags": ["moral-clarity", "existential-craft", "cadence"]
    },

    # --- Haruki Murakami: Men Without Women (2014) ---
    {
        "quote": "Once you really get into a role, it’s hard to find the right moment to stop. No matter how it preys on your emotions, you have to go with the flow until the performance has taken its shape, the point where its true meaning becomes clear.",
        "author": "Haruki Murakami",
        "work": "Men Without Women",
        "year": 2014,
        "translator": "Philip Gabriel and Ted Goossen",
        "hook": "How to diagnose emotional entrapment as theatrical discipline",
        "why_it_lands": "Murakami blurs acting with psychological possession. The character doesn't control the masquerade; the performance becomes an independent river that carries the actor downstream until the emotional bill comes due.",
        "tags": ["metaphor", "psychology", "craft"]
    },
    {
        "quote": "Dreams are the kind of things you can—when you need to—borrow and lend out.",
        "author": "Haruki Murakami",
        "work": "Men Without Women",
        "year": 2014,
        "translator": "Philip Gabriel and Ted Goossen",
        "hook": "How to treat nocturnal fantasy as circulating currency",
        "why_it_lands": "Classic Murakami domestic surrealism. The em-dashes create a hesitant, intimate delivery, transforming the deeply private realm of sleep into something transactional and shared across lovers.",
        "tags": ["surrealism", "understatement", "voice"]
    },
    {
        "quote": "Lampreys think very lamprey-like thoughts. About lamprey-like topics in a context that’s very lamprey-like. There are no words for those thoughts.",
        "author": "Haruki Murakami",
        "work": "Men Without Women",
        "year": 2014,
        "translator": "Philip Gabriel and Ted Goossen",
        "hook": "How to delineate alien consciousness through linguistic refusal",
        "why_it_lands": "The deadpan triple repetition of 'lamprey-like' rejects human anthropomorphism. Murakami reminds us that nature does not think in human adjectives; it operates in an acoustic and sensory silence we cannot translate.",
        "tags": ["deadpan", "defamiliarization", "style"]
    },
    {
        "quote": "Don’t look away, look right at it.",
        "author": "Haruki Murakami",
        "work": "Men Without Women",
        "year": 2014,
        "translator": "Philip Gabriel and Ted Goossen",
        "hook": "How to command unflinching attention in seven monosyllables",
        "why_it_lands": "Seven crisp, percussive words that refuse consolation. In a collection about grief, isolation, and romantic abandonment, the simple imperative to look directly into the fracture is the only honest posture.",
        "tags": ["brevity", "imperative", "candor"]
    }
]

def main():
    with open(QUOTE_BANK, "r", encoding="utf-8") as f:
        bank = json.load(f)

    existing_quotes = {q["quote"].strip().lower() for q in bank}
    added = 0
    for q in NEW_QUOTES:
        if q["quote"].strip().lower() not in existing_quotes:
            bank.append(q)
            existing_quotes.add(q["quote"].strip().lower())
            added += 1

    with open(QUOTE_BANK, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)

    print(f"Appended {added} new vetted quotes to {QUOTE_BANK}. Total bank size: {len(bank)}")

if __name__ == "__main__":
    main()
