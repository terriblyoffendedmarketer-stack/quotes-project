import json
from pathlib import Path

bank_file = Path("/Users/apple/Documents/Claude Code/quotes-project/content/quote-bank.json")
bank = json.loads(bank_file.read_text())

new_quotes = [
  # Ursula K. Le Guin - The Left Hand of Darkness
  {
    "id": "leguin-darkness-truth-logically-a-lie",
    "quote": "The only truth I can understand or express is, logically defined, a lie.",
    "author": "Ursula K. Le Guin",
    "work": "The Left Hand of Darkness",
    "year": 1969,
    "translator": None,
    "hook": "How to begin with the paradox of storytelling",
    "whyItLands": "The novel's foundational confession: factual reportage cannot capture lived experience, so narrative artifice must serve as the only reliable vessel for truth.",
    "source": "Books/Fiction ／ non fiction/LG Ursula K - The Left Hand of Darkness.epub",
    "tags": ["truth", "paradox", "storytelling"]
  },
  {
    "id": "leguin-darkness-passive-murder",
    "quote": "They do not kill people on their Farms: they let hunger and winter and despair do their murders for them.",
    "author": "Ursula K. Le Guin",
    "work": "The Left Hand of Darkness",
    "year": 1969,
    "translator": None,
    "hook": "How to unmask institutional cruelty without raising your voice",
    "whyItLands": "Replaces active violence with the bureaucratic outsourcing of death to the climate, indicting passive systems through chilling grammatical calm.",
    "source": "Books/Fiction ／ non fiction/LG Ursula K - The Left Hand of Darkness.epub",
    "tags": ["power", "injustice", "understatement"]
  },
  {
    "id": "leguin-darkness-traitor-name-sticks",
    "quote": "It is hard, I found, to be called traitor. Strange how hard it is, for it’s an easy name to call another man; a name that sticks, that fits, that convinces.",
    "author": "Ursula K. Le Guin",
    "work": "The Left Hand of Darkness",
    "year": 1969,
    "translator": None,
    "hook": "How to weigh the asymmetrical weight of an accusation",
    "whyItLands": "Contrasts the trivial effort required to slander someone with the crushing, permanent gravity the accused must carry.",
    "source": "Books/Fiction ／ non fiction/LG Ursula K - The Left Hand of Darkness.epub",
    "tags": ["language", "betrayal", "reputation"]
  },
  {
    "id": "leguin-darkness-existed-named",
    "quote": "I was named, known, recognized; I existed. It was an intense relief.",
    "author": "Ursula K. Le Guin",
    "work": "The Left Hand of Darkness",
    "year": 1969,
    "translator": None,
    "hook": "How to build a climax out of simple recognition",
    "whyItLands": "Reduces the deepest human hunger not to triumph or dominance, but to the basic confirmation that another consciousness sees you.",
    "source": "Books/Fiction ／ non fiction/LG Ursula K - The Left Hand of Darkness.epub",
    "tags": ["identity", "relief", "connection"]
  },

  # Ted Chiang - Stories of Your Life and Others
  {
    "id": "chiang-stories-sequential-consciousness",
    "quote": "Freedom isn’t an illusion; it’s perfectly real in the context of sequential consciousness.",
    "author": "Ted Chiang",
    "work": "Stories of Your Life and Others",
    "year": 2002,
    "translator": None,
    "hook": "How to reconcile free will with fatalism",
    "whyItLands": "Resolves the age-old philosophical contradiction of determinism by defining free will as a phenomenon of experiencing time in a forward direction.",
    "source": "Books/Fiction ／ non fiction/Stories_of_Your_Life_and_Others_-_Ted_Chiang.epub",
    "tags": ["time", "free-will", "philosophy"]
  },
  {
    "id": "chiang-stories-for-sake-of-a-word",
    "quote": "He altered the selling patterns of the stock of five unrelated corporations, for the sake of a word.",
    "author": "Ted Chiang",
    "work": "Stories of Your Life and Others",
    "year": 2002,
    "translator": None,
    "hook": "How to demonstrate terrifying power through trivial motive",
    "whyItLands": "Scales global corporate machinations against a motive so minute it reveals godlike intellect through absurd detachment.",
    "source": "Books/Fiction ／ non fiction/Stories_of_Your_Life_and_Others_-_Ted_Chiang.epub",
    "tags": ["power", "scale", "irony"]
  },
  {
    "id": "chiang-stories-touch-the-ceiling",
    "quote": "The water rose, and bore them up, until Hillalum could reach up with his hands and touch the ceiling.",
    "author": "Ted Chiang",
    "work": "Stories of Your Life and Others",
    "year": 2002,
    "translator": None,
    "hook": "How to invert the universe through physical touch",
    "whyItLands": "From Tower of Babylon: the biblical vertical ascent reaches a literal stone vault of heaven, making cosmological dogma tangible with a fingertip.",
    "source": "Books/Fiction ／ non fiction/Stories_of_Your_Life_and_Others_-_Ted_Chiang.epub",
    "tags": ["wonder", "cosmology", "physical-detail"]
  },
  {
    "id": "chiang-stories-universe-indifferent",
    "quote": "The problem with the universe is that it is not only vast but also indifferent. It does not care whether you live or die, whether you are happy or sad, whether you succeed or fail.",
    "author": "Ted Chiang",
    "work": "Stories of Your Life and Others",
    "year": 2002,
    "translator": None,
    "hook": "How to state existential neutrality without despair",
    "whyItLands": "A clean, unadorned declaration of cosmological indifference that frees the individual from reading moral meaning into random fortune.",
    "source": "Books/Fiction ／ non fiction/Stories_of_Your_Life_and_Others_-_Ted_Chiang.epub",
    "tags": ["cosmos", "indifference", "clarity"]
  },

  # Susanna Clarke - Piranesi
  {
    "id": "clarke-piranesi-rain-pixelated",
    "quote": "The afternoon had been stormy, and the lights of the cars were pixelated by rain; the pavements collaged with wet black leaves.",
    "author": "Susanna Clarke",
    "work": "Piranesi",
    "year": 2020,
    "translator": None,
    "hook": "How to describe our modern world through the innocent eyes of an exile",
    "whyItLands": "Uses the sensory vocabulary of an ancient house-dweller to make everyday city traffic look like a dazzling, impressionistic mosaic.",
    "source": "Books/Fiction ／ non fiction/Piranesi  - Susanna Clarke.epub",
    "tags": ["observation", "sensory", "wonder"]
  },
  {
    "id": "clarke-piranesi-sea-sweeps-through-house",
    "quote": "The sea sweeps through the house. Sometimes it swept over me, but always I was saved.",
    "author": "Susanna Clarke",
    "work": "Piranesi",
    "year": 2020,
    "translator": None,
    "hook": "How to establish mythic innocence in two plain sentences",
    "whyItLands": "Combines the violent grandeur of oceanic tides inside grand halls with an unshakeable, childlike trust in the benevolence of the World.",
    "source": "Books/Fiction ／ non fiction/Piranesi  - Susanna Clarke.epub",
    "tags": ["trust", "myth", "atmosphere"]
  },
  {
    "id": "clarke-piranesi-mad-already",
    "quote": "Worse still, at the very point at which the Other has declared he will kill me if I become mad, I have discovered that I am mad already!",
    "author": "Susanna Clarke",
    "work": "Piranesi",
    "year": 2020,
    "translator": None,
    "hook": "How to turn existential terror into sudden dark comedy",
    "whyItLands": "Subverts the terrifying ultimatum of a captor by realizing the dreaded condition has already arrived, converting suspense into uncanny irony.",
    "source": "Books/Fiction ／ non fiction/Piranesi  - Susanna Clarke.epub",
    "tags": ["madness", "irony", "suspense"]
  },
  {
    "id": "clarke-piranesi-message-urge",
    "quote": "What should I do? I knew that as long as the message existed I would experience a strong urge to read it.",
    "author": "Susanna Clarke",
    "work": "Piranesi",
    "year": 2020,
    "translator": None,
    "hook": "How to pin down the irresistible gravity of written words",
    "whyItLands": "Pinpoints the psychological torment of forbidden knowledge: text does not just sit in physical space, it radiates a continuous pull on curiosity.",
    "source": "Books/Fiction ／ non fiction/Piranesi  - Susanna Clarke.epub",
    "tags": ["curiosity", "reading", "temptation"]
  },

  # Arkady and Boris Strugatsky - Roadside Picnic
  {
    "id": "strugatsky-picnic-crumbly-grass",
    "quote": "It was no longer stiff and bristly, but soft and crumbly—it was falling apart under their shoes, like flakes of soot.",
    "author": "Arkady and Boris Strugatsky",
    "work": "Roadside Picnic",
    "year": 1972,
    "translator": "Olena Bormashenko",
    "hook": "How to describe alien contamination through decaying texture",
    "whyItLands": "Instead of monsters or glowing lights, the eerie horror of the Zone is communicated through familiar grass that has lost its cellular memory and collapses like ash.",
    "source": "Books/Fiction ／ non fiction/Roadside Picnic - Arkady and Boris.epub",
    "tags": ["horror", "texture", "uncanny"]
  },
  {
    "id": "strugatsky-picnic-phone-lines-tonight",
    "quote": "They haven’t laid the phone lines to where he is tonight. Let’s go.",
    "author": "Arkady and Boris Strugatsky",
    "work": "Roadside Picnic",
    "year": 1972,
    "translator": "Olena Bormashenko",
    "hook": "How to euphemize death with technological understatement",
    "whyItLands": "Announces a friend's demise in the Zone not with tragic lamentation, but with a stalker's rough, practical metaphor of interrupted telecom.",
    "source": "Books/Fiction ／ non fiction/Roadside Picnic - Arkady and Boris.epub",
    "tags": ["death", "dialogue", "understatement"]
  },
  {
    "id": "strugatsky-picnic-as-though-nothing-happened",
    "quote": "It was as though nothing had happened here.",
    "author": "Arkady and Boris Strugatsky",
    "work": "Roadside Picnic",
    "year": 1972,
    "translator": "Olena Bormashenko",
    "hook": "How to make normalcy the most terrifying detail",
    "whyItLands": "The most disturbing consequence of cosmic visitation is how quickly the surrounding landscape forgets it, leaving human survivors stranded in false calm.",
    "source": "Books/Fiction ／ non fiction/Roadside Picnic - Arkady and Boris.epub",
    "tags": ["calm", "dread", "memory"]
  },

  # Stanislaw Lem - Solaris
  {
    "id": "lem-solaris-library-colors-of-spines",
    "quote": "They’re wandering around in a library of books written in an unknown language, and just looking at the colors of the spines.",
    "author": "Stanislaw Lem",
    "work": "Solaris",
    "year": 1961,
    "translator": "Bill Johnston",
    "hook": "How to indict scientific arrogance with an architectural metaphor",
    "whyItLands": "A devastating critique of humanity's attempt to decipher the cosmic alien ocean: classifying surface features while remaining utterly illiterate to the text.",
    "source": "Books/Fiction ／ non fiction/Solaris - Stanislaw Lem.epub",
    "tags": ["science", "knowledge", "metaphor"]
  },
  {
    "id": "lem-solaris-not-worth-it",
    "quote": "It wasn’t worth it. It really wasn’t.",
    "author": "Stanislaw Lem",
    "work": "Solaris",
    "year": 1961,
    "translator": "Bill Johnston",
    "hook": "How to end cosmic ambition on four flat words",
    "whyItLands": "Strips all heroic sci-fi grandeur from space exploration, delivering the quiet, exhausted reality of psychological breakdown.",
    "source": "Books/Fiction ／ non fiction/Solaris - Stanislaw Lem.epub",
    "tags": ["disillusion", "brevity", "exhaustion"]
  },
  {
    "id": "lem-solaris-recognize-my-voice",
    "quote": "It doesn’t matter. I mean, you do recognize my voice?",
    "author": "Stanislaw Lem",
    "work": "Solaris",
    "year": 1961,
    "translator": "Bill Johnston",
    "hook": "How to dismantle certainty through a desperate check on sanity",
    "whyItLands": "Reduces an astronaut confronting a material manifestation of his dead wife to the fragile question of acoustic recognition.",
    "source": "Books/Fiction ／ non fiction/Solaris - Stanislaw Lem.epub",
    "tags": ["haunting", "identity", "grief"]
  }
]

bank.extend(new_quotes)
bank_file.write_text(json.dumps(bank, indent=2, ensure_ascii=False))
print(f"Updated quote-bank.json! Total quotes: {len(bank)}")
