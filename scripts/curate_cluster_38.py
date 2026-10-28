# curate_cluster_38.py — Curates 20 vetted quotes from Cluster 38 into quote-bank.json
# Usage: python3 scripts/curate_cluster_38.py
#
# Books:
# - On Literature by Umberto Eco (2002, trans. Martin McLaughlin)
# - The Library Book by Susan Orlean (2018)
# - Style: An Anti-Textbook by Richard A. Lanham (1974)
# - Poems from the Book of Hours by Rainer Maria Rilke (1905, trans. Babette Deutsch)
# - Book of Rhymes: The Poetics of Hip Hop by Adam Bradley (2009)

import json
from pathlib import Path

QUOTE_BANK = Path("content/quote-bank.json")

NEW_QUOTES = [
    # --- Umberto Eco: On Literature (2002) ---
    {
        "quote": "You can die on Saint Helena without being Napoléon.",
        "author": "Umberto Eco",
        "work": "On Literature",
        "year": 2002,
        "translator": "Martin McLaughlin",
        "hook": "How to crush inflated ambition with dry geographic fatalism",
        "why_it_lands": "A magnificent ten-word deflation. Eco points out that exile, isolation, and ignominious death are easily attained by ordinary mediocrities; only the historic glory required the genius.",
        "tags": ["irony", "brevity", "aphorism"]
    },
    {
        "quote": "For in order to name everything in the universe men would need a dictionary made up entirely of things, and the size of this dictionary would match the extent of the entire cosmos.",
        "author": "Umberto Eco",
        "work": "On Literature",
        "year": 2002,
        "translator": "Martin McLaughlin",
        "hook": "How to dramatize the impossible frontier of taxonomy",
        "why_it_lands": "Eco pushes lexicography to Borges-like absurdity. The literal equation—one physical object per definition—turns language into a futile shadow of matter, exposing why literature must rely on abstraction and metaphor rather than catalogue.",
        "tags": ["metaphor", "scale", "craft"]
    },
    {
        "quote": "Whoever knows about chlorophyll and photosynthesis will for the rest of his life be insensitive to the beauty of a leaf, that whoever knows anything about the circulation of the blood will never be able to make his heart palpitate with love.",
        "author": "Umberto Eco",
        "work": "On Literature",
        "year": 2002,
        "translator": "Martin McLaughlin",
        "hook": "How to satirize reductionist pedantry through false causality",
        "why_it_lands": "Eco mocks the intellectual snobbery that claims analytical knowledge ruins romantic wonder. By taking the argument to its absurd anatomical extreme, he proves that true aesthetic comprehension easily survives scientific reality.",
        "tags": ["satire", "intellectual-craft", "irony"]
    },
    {
        "quote": "Every Poetics that proposes ideal structures, and chooses to ignore the particularities specific to individual works, is always in the end a theory of the works that the theorist judges to be best.",
        "author": "Umberto Eco",
        "work": "On Literature",
        "year": 2002,
        "translator": "Martin McLaughlin",
        "hook": "How to unmask aesthetic dogma as personal prejudice",
        "why_it_lands": "A devastating takedown of universal literary prescription. Eco exposes how every objective rulebook is just a disguised love letter to the critic's favorite writers, turning apparent objectivity into covert autobiography.",
        "tags": ["criticism", "candor", "craft"]
    },

    # --- Susan Orlean: The Library Book (2018) ---
    {
        "quote": "The architect of this building may have been a great architect, but he didn’t know his fanny from a hot rock when it came to fire protection.",
        "author": "Susan Orlean",
        "work": "The Library Book",
        "year": 2018,
        "hook": "How to puncture architectural majesty with vernacular contempt",
        "why_it_lands": "The grand aesthetic stature of a civic landmark is dismantled in twenty words by an unsparing working-class assessment. Orlean preserves the firefighter's earthy idiom to balance the library's cathedral-like romance.",
        "tags": ["vernacular", "voice", "candor"]
    },
    {
        "quote": "It’s the moment when a fire in a room is transformed into a room on fire.",
        "author": "Susan Orlean",
        "work": "The Library Book",
        "year": 2018,
        "hook": "How to define catastrophic tipping points with chiasmus",
        "why_it_lands": "A textbook inversion of syntax that makes physical disaster instantly legible. By simply swapping subject and predicate, Orlean marks the exact second control evaporates and containment becomes fatal.",
        "tags": ["chiasmus", "sentence-mechanics", "precision"]
    },
    {
        "quote": "The pages burned so fast they barely crackled; the sound was soft, like a sizzle, or like the crinkly light sound of water spraying out of a shower.",
        "author": "Susan Orlean",
        "work": "The Library Book",
        "year": 2018,
        "hook": "How to evoke physical destruction through paradoxical sensory comparison",
        "why_it_lands": "Instead of roaring flames and theatrical explosions, Orlean listens closely and hears the gentle, domestic whisper of incinerating paper. Comparing a devastating inferno to a bathroom shower is chilling because the auditory scale is so disarmingly benign.",
        "tags": ["sensory-detail", "metaphor", "understatement"]
    },
    {
        "quote": "Like all creative art, it is disturbing: it leaves an impression that is satisfying yet mystifying.",
        "author": "Susan Orlean",
        "work": "The Library Book",
        "year": 2018,
        "hook": "How to capture the uneasy aftermath of aesthetic encounter",
        "why_it_lands": "Orlean refuses the easy comfort of art as mere consolation. By binding satisfaction directly to mystification, she identifies the residue of great work: it leaves the reader settled and unsettled at the exact same moment.",
        "tags": ["craft", "paradox", "brevity"]
    },

    # --- Richard A. Lanham: Style: An Anti-Textbook (1974) ---
    {
        "quote": "I couldn’t do this job for the same reason I couldn’t sing the soprano lead in La Traviata: because I’m tone deaf.",
        "author": "Richard A. Lanham",
        "work": "Style: An Anti-Textbook",
        "year": 1974,
        "hook": "How to diagnose stylistic incompetence as a physical defect",
        "why_it_lands": "Lanham takes the polite fiction that 'anyone can write clearly with enough effort' and replaces it with sensory reality. Prose rhythm, like vocal pitch, requires an ear; without it, grammatical obedience is just noise.",
        "tags": ["analogy", "voice", "humor"]
    },
    {
        "quote": "What arcana they share! What bright chaps they must be to share them!",
        "author": "Richard A. Lanham",
        "work": "Style: An Anti-Textbook",
        "year": 1974,
        "hook": "How to dismantle academic jargon through sarcastic celebration",
        "why_it_lands": "Two gleeful exclamations that expose pedantic vocabulary as a schoolboy fraternity ritual. Lanham captures how dense prose often exists solely to reassure the writer and reader of their mutual intellectual pedigree.",
        "tags": ["satire", "irony", "voice"]
    },
    {
        "quote": "Students of meter often refer to the tension between natural word stress and the stress pattern that meter imposes. In prose rhythm an analogous tension waits there for the exploiting.",
        "author": "Richard A. Lanham",
        "work": "Style: An Anti-Textbook",
        "year": 1974,
        "hook": "How to locate the dynamic engine of prose rhythm",
        "why_it_lands": "Lanham bridges poetic meter and prose cadence. The energy of an extraordinary sentence comes not from floating freely or marching rigidly, but from the counterpoint between colloquial speech stress and formal syntactic shape.",
        "tags": ["prose-rhythm", "craft", "sentence-mechanics"]
    },
    {
        "quote": "No synonymity is ever exactly synonymous. Each new variation can be read not as an opaque variation on an already determined reality but as a transparent glimpse into a new reality.",
        "author": "Richard A. Lanham",
        "work": "Style: An Anti-Textbook",
        "year": 1974,
        "hook": "How to treat word choice as an act of world-building",
        "why_it_lands": "A definitive refutation of the 'thesaurus swap.' Changing a single noun doesn't simply decorate a thought; it bends the light and alters the moral reality of the sentence.",
        "tags": ["diction", "craft", "philosophical-depth"]
    },

    # --- Rainer Maria Rilke: Poems from the Book of Hours (1905) ---
    {
        "quote": "God is the child in the manger, the culprit on the gallows.",
        "author": "Rainer Maria Rilke",
        "work": "Poems from the Book of Hours",
        "year": 1905,
        "translator": "Babette Deutsch",
        "hook": "How to unite innocence and condemned agony in a single breath",
        "why_it_lands": "Ten words that dismantle centuries of gilded church majesty. By placing the cradle directly alongside the gallows, Rilke locates the sacred at the outer margins of helplessness and societal punishment.",
        "tags": ["antithesis", "brevity", "sacred-craft"]
    },
    {
        "quote": "They will say ‘mine’ as one will sometimes call the prince his friend in speech with villagers, this prince being very great — and far away.",
        "author": "Rainer Maria Rilke",
        "work": "Poems from the Book of Hours",
        "year": 1905,
        "translator": "Babette Deutsch",
        "hook": "How to expose human possessiveness as village boasting",
        "why_it_lands": "Rilke diagnoses property and attachment through a biting social metaphor. We claim ownership over life, land, and love with the pathetic bravado of a peasant pretending he has the ear of a distant monarch.",
        "tags": ["metaphor", "parable", "irony"]
    },
    {
        "quote": "God is the neighbor we hear breathing in the night. He is the gift, the lost or unfound wholeness of being.",
        "author": "Rainer Maria Rilke",
        "work": "Poems from the Book of Hours",
        "year": 1905,
        "translator": "Babette Deutsch",
        "hook": "How to bring the cosmic into acoustic proximity",
        "why_it_lands": "Instead of thunder on a mountain or celestial light, divinity becomes the sound of air moving through lungs on the other side of a bedroom wall. Intimacy replaces majesty.",
        "tags": ["sensory-detail", "intimacy", "metaphor"]
    },
    {
        "quote": "He must be wooed into being, refined into purity, he must ripen in deep peace and silence towards the future, like a wine that unperturbed, grows ever sweeter and all its own.",
        "author": "Rainer Maria Rilke",
        "work": "Poems from the Book of Hours",
        "year": 1905,
        "translator": "Babette Deutsch",
        "hook": "How to make spiritual emergence tangible through slow cellar craft",
        "why_it_lands": "The verb 'ripen' turns creation into an agricultural and artisanal process. Divine or artistic perfection cannot be rushed by decree; it requires the dark, undisturbed quiet of a barrel.",
        "tags": ["metaphor", "craft", "lyricism"]
    },

    # --- Adam Bradley: Book of Rhymes: The Poetics of Hip Hop (2009) ---
    {
        "quote": "What you find with a lot of rappers is they work out their flow—the rhythm to their words—and the better they get, the more tidy the flow becomes, until everything has to fit in, the same way it would with a poem.",
        "author": "Adam Bradley",
        "work": "Book of Rhymes: The Poetics of Hip Hop",
        "year": 2009,
        "hook": "How to diagnose when technical mastery threatens spontaneity",
        "why_it_lands": "Bradley identifies a crucial turning point in craft: the moment mechanical competence becomes a prison. When polish forces every syllable into pre-cast grooves, the unruly vitality that birthed the art form gets engineered away.",
        "tags": ["craft", "rhythm", "observation"]
    },
    {
        "quote": "Not surprisingly, the rhymes in these lines also shape the rhythm, with a pattern of stress carrying over from phrase to phrase.",
        "author": "Adam Bradley",
        "work": "Book of Rhymes: The Poetics of Hip Hop",
        "year": 2009,
        "hook": "How to let rhyme dictate metric momentum",
        "why_it_lands": "Bradley explains the internal mechanics of sonic storytelling: rhyme is not mere decorative chime at the end of a clause, but the engine that pushes the rhythmic stress across the bar line.",
        "tags": ["meter", "sound-craft", "sentence-mechanics"]
    },
    {
        "quote": "It may be of great interest to discover how accurately a poem reflects its author’s experience, attitudes, or beliefs; but this is a question that belongs to biography not to criticism.",
        "author": "Adam Bradley",
        "work": "Book of Rhymes: The Poetics of Hip Hop",
        "year": 2009,
        "hook": "How to separate literary form from personal confession",
        "why_it_lands": "A crucial demarcation line for craft criticism. Bradley protects the autonomy of the made object from the gossip of autobiographical assumption, insisting we evaluate the verse on its artistic terms rather than the artist's personal history.",
        "tags": ["criticism", "craft", "clarity"]
    },
    {
        "quote": "In hip hop—and inside the broken histories of black men in America—respect is the ultimate medium of exchange. And that is to say, in battling, the rapper is gambling with the most valuable commodity available: one’s rep and the respect that flows from it.",
        "author": "Adam Bradley",
        "work": "Book of Rhymes: The Poetics of Hip Hop",
        "year": 2009,
        "hook": "How to establish cultural currency as life-or-death stakes",
        "why_it_lands": "Bradley reframes the rap battle from adolescent braggadocio to high-stakes economic exchange. When disenfranchisement strips material assets away, personal respect becomes the only capital that cannot be devalued by outside institutions.",
        "tags": ["cultural-craft", "persuasive-prose", "scale"]
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
