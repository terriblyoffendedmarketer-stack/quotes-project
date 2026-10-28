import json
from pathlib import Path

bank_file = Path("/Users/apple/Documents/Claude Code/quotes-project/content/quote-bank.json")
bank = json.loads(bank_file.read_text())

new_quotes = [
  # Albert Camus - The Myth of Sisyphus
  {
    "id": "camus-sisyphus-habit-living",
    "quote": "You continue making the gestures commanded by existence for many reasons, the first of which is habit.",
    "author": "Albert Camus",
    "work": "The Myth of Sisyphus",
    "year": 1942,
    "translator": "Justin O'Brien",
    "hook": "How to diagnose daily life as physical reflex",
    "whyItLands": "Demystifies human resilience: people do not endure existence out of heroic determination, but because muscles and routine repeat what conscious will would abandon.",
    "source": "Books/Fiction ／ non fiction/Myth of Sisyphus and Other Essays, The - Albert Camus.epub",
    "tags": ["habit", "routine", "existentialism"]
  },
  {
    "id": "camus-sisyphus-worm-in-heart",
    "quote": "The worm is in man’s heart. That is where it must be sought.",
    "author": "Albert Camus",
    "work": "The Myth of Sisyphus",
    "year": 1942,
    "translator": "Justin O'Brien",
    "hook": "How to locate the origin of despair in two short strokes",
    "whyItLands": "Refuses external scapegoats for human misery—placing the parasite of absurdity squarely inside the interior architecture of the self.",
    "source": "Books/Fiction ／ non fiction/Myth of Sisyphus and Other Essays, The - Albert Camus.epub",
    "tags": ["despair", "metaphor", "brevity"]
  },
  {
    "id": "camus-sisyphus-shoelace-brink",
    "quote": "It is, at the extreme limit of the condemned man’s last thought, that shoelace that despite everything he sees a few yards away, on the very brink of his dizzying fall.",
    "author": "Albert Camus",
    "work": "The Myth of Sisyphus",
    "year": 1942,
    "translator": "Justin O'Brien",
    "hook": "How to ground mortal terror in an absurd everyday object",
    "whyItLands": "When facing total annihilation, the human mind refuses sublime contemplation and fixes its entire gaze on the trivial geometry of an untied shoelace.",
    "source": "Books/Fiction ／ non fiction/Myth of Sisyphus and Other Essays, The - Albert Camus.epub",
    "tags": ["mortality", "detail", "absurdity"]
  },
  {
    "id": "camus-sisyphus-contemplation-action",
    "quote": "There always comes a time when one must choose between contemplation and action. This is called becoming a man.",
    "author": "Albert Camus",
    "work": "The Myth of Sisyphus",
    "year": 1942,
    "translator": "Justin O'Brien",
    "hook": "How to draw a line between thinking and living",
    "whyItLands": "Cuts through intellectual paralysis with a stark moral threshold, defining maturity as the surrender of theoretical detachment to real-world risk.",
    "source": "Books/Fiction ／ non fiction/Myth of Sisyphus and Other Essays, The - Albert Camus.epub",
    "tags": ["action", "maturity", "courage"]
  },

  # Mieko Kawakami - Heaven
  {
    "id": "kawakami-heaven-piece-of-furniture",
    "quote": "It was like being a piece of furniture in a room that nobody uses.",
    "author": "Mieko Kawakami",
    "work": "Heaven",
    "year": 2009,
    "translator": "Sam Bett & David Boyd",
    "hook": "How to describe total social invisibility",
    "whyItLands": "Captures adolescent alienation not with theatrical melodrama, but with the cold, dusty stillness of unvisited domestic wood.",
    "source": "Books/Fiction ／ non fiction/Heaven_-_Meiko_kawakami.epub",
    "tags": ["isolation", "domesticity", "alienation"]
  },
  {
    "id": "kawakami-heaven-right-versus-want",
    "quote": "Nobody does anything because they have the right. They do it because they want to.",
    "author": "Mieko Kawakami",
    "work": "Heaven",
    "year": 2009,
    "translator": "Sam Bett & David Boyd",
    "hook": "How to strip moral pretense from cruelty",
    "whyItLands": "The novel's defining revelation of power: bullies do not rationalize their actions through righteousness, but exercise raw, unadorned desire against the weak.",
    "source": "Books/Fiction ／ non fiction/Heaven_-_Meiko_kawakami.epub",
    "tags": ["power", "cruelty", "truth"]
  },
  {
    "id": "kawakami-heaven-crying-no-choice",
    "quote": "I wasn’t crying because I was sad. I guess I was crying because we had nowhere else to go, no choice but to go on living in this world.",
    "author": "Mieko Kawakami",
    "work": "Heaven",
    "year": 2009,
    "translator": "Sam Bett & David Boyd",
    "hook": "How to separate tears from ordinary sadness",
    "whyItLands": "Elevates weeping from personal sorrow into an involuntary reaction to the inescapable condition of staying alive.",
    "source": "Books/Fiction ／ non fiction/Heaven_-_Meiko_kawakami.epub",
    "tags": ["grief", "endurance", "resignation"]
  },

  # Sayaka Murata - Convenience Store Woman
  {
    "id": "murata-store-putting-on-trial",
    "quote": "People who are considered normal enjoy putting those who aren’t on trial, you know.",
    "author": "Sayaka Murata",
    "work": "Convenience Store Woman",
    "year": 2016,
    "translator": "Ginny Tapley Takemori",
    "hook": "How to expose society's secret courtroom",
    "whyItLands": "Lays bare the casual sadistic pleasure conventional society takes in diagnosing, cross-examining, and punishing anyone who deviates from the script.",
    "source": "Books/Fiction ／ non fiction/Sayaka Murata - Convenience Store Woman.epub",
    "tags": ["conformity", "society", "judgment"]
  },
  {
    "id": "murata-store-vague-answer",
    "quote": "You can just give a vague answer to a personal question, and they’ll come to their own conclusions.",
    "author": "Sayaka Murata",
    "work": "Convenience Store Woman",
    "year": 2016,
    "translator": "Ginny Tapley Takemori",
    "hook": "How to turn conversational ambiguity into an invisibility shield",
    "whyItLands": "A tactical lesson in surviving social surveillance: give people a blank canvas, and their own projections will do the work of keeping them satisfied.",
    "source": "Books/Fiction ／ non fiction/Sayaka Murata - Convenience Store Woman.epub",
    "tags": ["survival", "dialogue", "deflection"]
  },
  {
    "id": "murata-store-rattle-plastic-bottle",
    "quote": "I hear the faint rattle of a new plastic bottle rolling into place as a customer takes one out of the refrigerator, and look up instantly.",
    "author": "Sayaka Murata",
    "work": "Convenience Store Woman",
    "year": 2016,
    "translator": "Ginny Tapley Takemori",
    "hook": "How to show belonging through mechanical conditioning",
    "whyItLands": "Subverts the traditional idea of spiritual vocation: her peace does not come from nature or family, but from the synchronized, humming rhythm of modern retail.",
    "source": "Books/Fiction ／ non fiction/Sayaka Murata - Convenience Store Woman.epub",
    "tags": ["modernity", "vocation", "routine"]
  },

  # Franz Kafka - Letters to Milena
  {
    "id": "kafka-milena-hand-on-throat",
    "quote": "I do not know its inner laws, only its hand on my throat – and that really is the most terrible thing I have ever experienced or could experience.",
    "author": "Franz Kafka",
    "work": "Letters to Milena",
    "year": 1952,
    "translator": "Philip Boehm",
    "hook": "How to give psychological dread physical hands",
    "whyItLands": "Captures the terror of panic and neurotic dread without psychoanalytic terminology: fear is an unknowable sovereign whose only proof is the pressure on the windpipe.",
    "source": "Books/Fiction ／ non fiction/Letters to Milena Franz Kafka.epub",
    "tags": ["anxiety", "fear", "visceral"]
  },
  {
    "id": "kafka-milena-dirty-scream-purity",
    "quote": "I am dirty, Milena, infinitely dirty, this is why I scream so much about purity.",
    "author": "Franz Kafka",
    "work": "Letters to Milena",
    "year": 1952,
    "translator": "Philip Boehm",
    "hook": "How to confess hypocrisy with ruthless honesty",
    "whyItLands": "Unmasks moral sanctimony in a single sentence: the obsession with absolute purity is born directly from the conviction of one’s own incurable corruption.",
    "source": "Books/Fiction ／ non fiction/Letters to Milena Franz Kafka.epub",
    "tags": ["guilt", "purity", "confession"]
  },
  {
    "id": "kafka-milena-too-heavy-too-light",
    "quote": "I’m too heavy for myself and too light for you.",
    "author": "Franz Kafka",
    "work": "Letters to Milena",
    "year": 1952,
    "translator": "Philip Boehm",
    "hook": "How to measure love through incompatible scales",
    "whyItLands": "A nine-word balance beam that captures the tragedy of neurotic devotion: suffocated by his own self-consciousness yet incapable of offering solid grounding to the beloved.",
    "source": "Books/Fiction ／ non fiction/Letters to Milena Franz Kafka.epub",
    "tags": ["love", "balance", "neurosis"]
  },
  {
    "id": "kafka-milena-apartment-too-beautiful",
    "quote": "It seems to me I’ve never had such a beautiful apartment, I’m also sure I’ll soon lose it—it is too beautiful for me.",
    "author": "Franz Kafka",
    "work": "Letters to Milena",
    "year": 1952,
    "translator": "Philip Boehm",
    "hook": "How to poison joy with the certainty of punishment",
    "whyItLands": "The quintessential Kafka reflex: beauty is not welcomed as a gift, but suspected as an administrative error that will shortly be revoked.",
    "source": "Books/Fiction ／ non fiction/Letters to Milena Franz Kafka.epub",
    "tags": ["joy", "paranoia", "irony"]
  },

  # Leo Tolstoy - The Death of Ivan Ilych
  {
    "id": "tolstoy-ivan-he-dead-not-i",
    "quote": "It is he who is dead and not I.",
    "author": "Leo Tolstoy",
    "work": "The Death of Ivan Ilych",
    "year": 1886,
    "translator": "Louise and Aylmer Maude",
    "hook": "How to voice the secret relief of the survivor",
    "whyItLands": "Tolstoy skewers human sympathy: at the wake of a friend, every colleague's first instinctive, unspoken thought is selfish delight at still drawing breath.",
    "source": "Books/Fiction ／ non fiction/Leo Tolstoy - Death of Ivan Ilych.epub",
    "tags": ["death", "honesty", "selfishness"]
  },
  {
    "id": "tolstoy-ivan-gerasim-teeth",
    "quote": "‘It’s God’s will. We shall all come to it some day,’ said Gerasim, displaying his teeth—the even white teeth of a healthy peasant.",
    "author": "Leo Tolstoy",
    "work": "The Death of Ivan Ilych",
    "year": 1886,
    "translator": "Louise and Aylmer Maude",
    "hook": "How to contrast mortality against vital animal health",
    "whyItLands": "Juxtaposes the rotting decay of high-society bureaucracy against the shining, practical health of a peasant who touches death without squeamishness.",
    "source": "Books/Fiction ／ non fiction/Leo Tolstoy - Death of Ivan Ilych.epub",
    "tags": ["vitality", "death", "contrast"]
  },
  {
    "id": "tolstoy-ivan-semblance-propriety",
    "quote": "His aim was to free himself more and more from those unpleasantnesses and to give them a semblance of harmlessness and propriety.",
    "author": "Leo Tolstoy",
    "work": "The Death of Ivan Ilych",
    "year": 1886,
    "translator": "Louise and Aylmer Maude",
    "hook": "How to diagnose an entire bourgeois life as cowardice",
    "whyItLands": "Summarizes the central tragedy of middle-class respectability: sacrificing authenticity and truth to keep domestic reality comfortable and polite.",
    "source": "Books/Fiction ／ non fiction/Leo Tolstoy - Death of Ivan Ilych.epub",
    "tags": ["bourgeoisie", "facade", "avoidance"]
  }
]

bank.extend(new_quotes)
bank_file.write_text(json.dumps(bank, indent=2, ensure_ascii=False))
print(f"Updated quote-bank.json! Total quotes: {len(bank)}")
