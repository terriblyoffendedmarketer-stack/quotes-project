# audit_and_rewrite.py — Rewrites marketing/SaaS-biased explanation slides to focus purely on prose craft
# Usage: python3 scripts/audit_and_rewrite.py
#
# Gotchas:
# - lint_cards.py enforces word count limit of 60 for stealIt and 80 for lookCloser.
# - lint_cards.py forbids em dashes (—), rhetorical questions (?), colon reveals (w: a), triads, and banned words.
# - Openers must be varied to prevent set-level repetitive opener flags.

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARDS_PATH = ROOT / "content" / "cards.json"

UPDATES = {
    "kafka-metamorphosis-opening": {
        "stealIt": "State the most unbelievable event in your story with the flattest grammar you have. Skip the exclamation mark. Place your sensory details on something small beside it, like an itchy blanket or a cold cup."
    },
    "didion-magical-thinking-opening": {
        "stealIt": "Describe a moment of loss without naming a single emotion. Cut words like 'grief' or 'heartbroken'. Record only what the hands were doing right before the news arrived, like slicing an apple or tying a shoe."
    },
    "plath-bell-jar-opening": {
        "stealIt": "Anchor a personal essay by tying your opening line to a public event. Name the weather and the headline everyone talked about that month, then drop your narrator into the middle of the noise."
    },
    "garcia-marquez-solitude-opening": {
        "stealIt": "Fold three distinct moments of time into a single sentence. Look forward from the past, stand in the present threat, and remember a distant afternoon. The contrast between danger and discovery pulls the reader forward."
    },
    "shanbhag-ghachar-ghochar-money": {
        "stealIt": "Personify an abstract presence like ambition, fear, or debt. Describe how it behaves when modest, then show the strange personality it takes on once it expands. Give it physical gestures instead of clinical definitions."
    },
    "palahniuk-fight-club-opening": {
        "stealIt": "Begin a scene at the crisis, skipping the gradual buildup entirely. Join two unequal events with a flat phrase like 'after that'. Let the reader scramble to imagine the missing bridge."
    },
    "king-on-writing-adverbs": {
        "stealIt": "Deliver your craft advice by rewriting a familiar proverb. Take a moral warning everyone knows and substitute the technical habit you want to ban. Concrete proverbs outlive abstract rules."
    },
    "burkeman-four-thousand-weeks-opening": {
        "stealIt": "Take a familiar span of time and reframe it in a unit that shocks the senses. Count a lifetime in weeks or a career in summers. Shrink the horizon until the reader feels the edge."
    },
    "burkeman-four-thousand-weeks-defeat": {
        "stealIt": "Catalog the secret fantasy your narrator chases, naming every unrealistic condition with a run of 'when' clauses. Then declare defeat in a five-word sentence. Giving up the impossible struggle brings instant relief to the reader."
    },
    "tolstoy-anna-karenina-opening": {
        "stealIt": "Frame your opening as an unbending law about human nature, balancing two clauses on either side of a semicolon. Then step straight from that grand thesis into one specific, messy household."
    },
    "woolf-mrs-dalloway-opening": {
        "stealIt": "Enter a character's thoughts without using tags like 'she thought' or 'he remembered'. State their private rationalizations directly through the narrator's voice, treating an excuse as an established fact."
    },
    "austen-pride-and-prejudice-opening": {
        "stealIt": "Adopt the pompous voice of conventional wisdom in your opening clause. State an assumption as universal truth, then frame it so the real appetite belongs to the people claiming neutrality."
    },
    "dickens-bleak-house-fog": {
        "stealIt": "Choose a single physical element, like oppressive heat, and open your scene without a verb. Repeat the word like an echo, tracking it across rooftops and low alleys until it smothers the entire setting."
    },
    "orwell-shooting-an-elephant-opening": {
        "stealIt": "Confess an unflattering fact about yourself in the first clause, then add a dry observation puncturing your own importance. Readers trust an essayist who delivers the sharpest blow against himself."
    },
    "hemingway-farewell-to-arms-opening": {
        "stealIt": "Describe an impending crisis entirely through its quiet surroundings. Avoid ominous words like 'danger' or 'war'. Track dust rising on the road and troop movements glimpsed between trees in late summer heat."
    },
    "fitzgerald-gatsby-voice": {
        "stealIt": "Capture a complex personality through one physical trait, like a laugh or a walk. Let your narrator stumble for the description, then have another character name the essence in a startling, worldly noun."
    },
    "baldwin-notes-of-a-native-son-opening": {
        "stealIt": "Set two immense, opposing events side by side using bare dates and minimal punctuation. Give equal weight to dying and birth in consecutive sentences. Let the plain calendar carry the weight."
    },
    "oconnor-good-man-misfit": {
        "stealIt": "Assign the sharpest moral judgment of your story to an outsider or an antagonist. Preserve their colloquial speech and rough grammar. A raw phrasing can cut deeper than an essayist's refined reflection."
    },
    "dostoevsky-notes-from-underground-opening": {
        "stealIt": "Open an essay with four short confessions, each stripping away another layer of vanity. Move from moral flaws down to a petty physical ache. When you volunteer your worst traits early, the reader cannot accuse you."
    },
    "tolstoy-ivan-ilych-ordinary": {
        "stealIt": "Build a gentle rhythm with reassuring words like 'simple' and 'ordinary', then insert 'therefore' before an unsettling conclusion. Show that the horror lies in conformity itself."
    },
    "proust-swanns-way-madeleine": {
        "stealIt": "Describe an unexpected physical sensation before explaining the memory it unlocks. Trace the taste or scent across the body, pause the narrative, and observe the slow emergence of forgotten childhood scenes."
    },
    "joyce-the-dead-ending": {
        "stealIt": "Broaden the lens of your final paragraph from a quiet room to the entire horizon. Soften the consonants and repeat key participles in inverted order. Let the sentence drift until it encompasses both the living and the absent."
    },
    "camus-stranger-opening": {
        "stealIt": "Announce a life-altering tragedy in four monosyllabic words. Follow it immediately with a minor uncertainty about the date. That small factual hesitation reveals your narrator's emotional numbness faster than pages of explanation."
    },
    "kafka-diary-war-swimming": {
        "stealIt": "Place monumental world news right beside a tiny personal errand, with no connective explanation. Set an empire falling next to an afternoon swim. The stark collision reflects how humans actually live through catastrophe."
    },
    "garcia-marquez-chronicle-opening": {
        "stealIt": "Reveal the eventual tragedy in your very first subordinate clause, then describe your subject waking up and dressing for an ordinary errand. Knowing the end infuses every breakfast detail with agonizing dramatic weight."
    },
    "ishiguro-remains-heart-breaking": {
        "stealIt": "Hide your narrator's most painful revelation behind a formal, polite hesitation. Frame the admission as a reluctant question to oneself. The stiff etiquette heightens the grief beneath the restraint."
    },
    "ishiguro-never-let-me-go-opening": {
        "stealIt": "Present an unsettling arrangement in the neutral voice of an administrative form. State an unusual profession plainly, as if every listener already accepts its routine requirements."
    },
    "mccarthy-the-road-opening": {
        "stealIt": "Strip your opening sentence of ornamental adjectives. Use plain Anglo-Saxon nouns and monosyllables to evoke cold and darkness. Center the line on one protective, physical gesture."
    },
    "rushdie-midnights-children-opening": {
        "stealIt": "Open with a mythical flourish, then visibly stop and correct yourself on the page. Replace the fable with an exact address, a doctor's name, and a calendar date. The friction between myth and record grabs attention."
    },
    "tartt-secret-history-opening": {
        "stealIt": "Slip a horrifying event into the middle of a sentence, flanked by tranquil observations about seasonal weather. The casual placement forces the reader to double-back in disbelief."
    },
    "mantel-wolf-hall-opening": {
        "stealIt": "Open directly with an aggressive line of spoken dialogue, followed by an immediate physical impact. Omit backstory, character names, and setting. Thrust the reader into sensory defense."
    },
    "vuong-briefly-gorgeous-opening": {
        "stealIt": "Address your essay or letter to someone who will never be able to read it. Acknowledge that the page is an impossible bridge. The futility intensifies the honesty of every word you write."
    },
    "saunders-failures-of-kindness": {
        "stealIt": "Summon a lifetime of errors and dismiss the dramatic failures of ambition or fortune. Name a quiet, moral omission instead. The shift in perspective catches readers who expect grand drama."
    },
    "didion-goodbye-to-all-that-opening": {
        "stealIt": "Structure an opening thesis around two mirrored clauses, contrasting what is easy with what is elusive. Keep the syllables balanced. A clean geometric statement sets up a sprawling personal reflection."
    },
    "lamott-bird-by-bird": {
        "stealIt": "Anchor an abstract philosophy of work in a vivid childhood scene. Recreate the kitchen table, the panic of the deadline, and the father's exact spoken phrase. Concrete memories make advice unforgettable."
    },
    "dillard-writing-life-days": {
        "stealIt": "Insert a calm 'of course' into the center of a startling equation. Act as though the terrifying equivalence between a single afternoon and an entire lifetime is common sense."
    },
    "orwell-1984-opening": {
        "stealIt": "Establish a familiar seasonal scene, then twist a single mechanical fact just beyond reality. A clock striking thirteen alerts the reader that the laws of nature and society have slipped."
    },
    "kafka-the-trial-opening": {
        "stealIt": "Deduce the cause of an unjust catastrophe with detached, orderly logic. Use phrases like 'someone must have' to simulate rationality in the face of an absurd, inexplicable accusation."
    },
    "austen-persuasion-letter": {
        "stealIt": "Cut away the polite social preambles and open a critical letter with an admission that silence has become unbearable. Declare your internal division in stark, balanced opposites."
    },
    "capote-in-cold-blood-opening": {
        "stealIt": "Frame the setting of a true catastrophe through the local phrase neighbors use to set it apart. Quoting an insider nickname establishes isolation before the characters appear."
    },
    "carver-cathedral-opening": {
        "stealIt": "Open a story with the conversational syntax of an irritated person talking to a friend. Use casual phrasing like 'this blind man, he was' to signal resentment without formal exposition."
    },
    "calvino-winters-night-opening": {
        "stealIt": "Address the reader directly in the second person, guiding their physical posture before the story begins. Instruct them to adjust the light, shut the door, and set aside daily distractions."
    },
    "borges-library-of-babel-opening": {
        "stealIt": "Translate an abstract philosophical realm into concrete architectural geometry. Specify the exact shape of rooms and spiral staircases. Precise physical measurements ground an infinite concept."
    },
    "angelou-caged-bird-razor": {
        "stealIt": "Take a lingering emotional ache and compare it to a jagged household instrument. Add a second sensory layer like rust on steel to turn discomfort into sharp peril."
    },
    "murakami-running-pain": {
        "stealIt": "Take a burdensome experience like exhaustion or grief, and divide it into two clean categories. One is physical fact; the other is mental interpretation. Defining the boundary restores agency."
    },
    "jackson-hill-house-opening": {
        "stealIt": "Formulate a clinical, biological principle about the limits of the human mind. Mention insects or birds dreaming to establish scientific breadth before turning the lens on a haunted house."
    },
    "ernaux-the-years-opening": {
        "stealIt": "Begin a personal history with a sweeping, five-word prophecy of total erasure. List the fleeting private images that will vanish when you die, reminding the reader why memory must be written down."
    },
    "davis-the-outing": {
        "stealIt": "Isolate a minor involuntary bodily twitch, like a fluttering eyelid. Give it two divergent interpretations in adjacent clauses, spanning mortal terror and everyday fatigue. The contrast creates immediate psychological comedy."
    },
    "smith-white-teeth-opening": {
        "stealIt": "Pair two contrasting time scales in your opening line, matching the hour of day with the span of a century. Let the rhyming syllables create musical momentum before introducing an unfortunate protagonist."
    },
    "ferrante-brilliant-friend-childhood": {
        "stealIt": "Depict extreme hardship or violence without moral indignation. Describe bruises, wounds, and feuds through a child's matter-of-fact observation, showing how quickly horror becomes routine background noise."
    },
    "moshfegh-eileen-opening": {
        "stealIt": "Open an autobiographical account with an uncompromising comparative insult directed at your younger self. Admitting you were once even more unpleasant establishes immediate intimacy through harsh honesty."
    },
    "lahiri-third-and-final-continent-ending": {
        "stealIt": "Close a reflective memoir by repeating 'each' across expanding categories, moving from physical distance to daily meals to human bonds. The steady cadence turns personal biography into quiet wonder."
    },
    "vonnegut-slaughterhouse-five-opening": {
        "stealIt": "Introduce a traumatic historical narrative with an informal shrug about accuracy. Qualify your claims with 'more or less' and 'pretty much true'. The conversational hedge disarms skepticism better than a solemn guarantee."
    },
    "plath-bell-jar-fig-tree": {
        "stealIt": "Represent paralyzing life choices as ripe figs on a spreading tree. Give each branch a distinct path, and describe the agony of starving while watching the fruit turn black and fall."
    },
    "hemingway-iceberg": {
        "stealIt": "Draft a scene with deep emotional resonance, then delete the explanatory lines describing how the characters feel. If the physical dialogue is accurate, the unspoken tension will register with double intensity."
    },
    "king-gunslinger-opening": {
        "stealIt": "Establish an entire saga in eleven words by balancing two anonymous figures across a desolate expanse. One flees, the other follows. Two strong verbs create an immediate engine of pursuit."
    },
    "kafka-letter-axe": {
        "stealIt": "Define the purpose of your essay or story with an uncompromising physical instrument. Compare the reader's complacency to a frozen sea, and let your words serve as the blunt axe that cracks it."
    },
    "austen-emma-opening": {
        "stealIt": "Shower your protagonist with enviable gifts in your opening sentence, then slip a single doubtful word like 'seemed' into the catalog. The faint doubt hints at the inevitable downfall."
    },
    "camus-sisyphus-ending": {
        "stealIt": "Close an argument with a startling imperative that defies common sense. State it in five simple words without defensive explanations. Let the reader contemplate the paradoxical triumph."
    },
    "burkeman-four-thousand-weeks-capacities": {
        "stealIt": "Frame a core dilemma as a cruel disproportion between mind and body. Use 'yet' to pivot from infinite mental ambition to the severe physical limits of time and endurance."
    },
    "burkeman-four-thousand-weeks-trap": {
        "stealIt": "Attack a universally praised virtue, like efficiency or discipline, in a four-word opening verdict. Show how optimizing the habit merely accelerates the treadmill, leaving the practitioner more overwhelmed than before."
    },
    "orwell-why-i-write-windowpane": {
        "stealIt": "Review a drafted passage and circle every phrase where the author's performance obscures the subject matter. Polish the sentences until the ego disappears, leaving only clear glass between reader and world."
    },
    "palahniuk-fight-club-timeline": {
        "stealIt": "Express an existential truth about human mortality in the cold, mathematical language of risk assessment. The clinical terminology makes the inevitability hit harder than poetic lament."
    },
    "didion-on-self-respect": {
        "stealIt": "Reclaim a sentimentalized virtue like self-respect, loyalty, or patience. Strip away its pious associations and define it through rigorous personal accountability. Anchor the concept in concrete sacrifices rather than good intentions."
    },
    "ogilvy-rolls-royce-clock": {
        "job": "How to prove a grand claim with one quiet fact",
        "stealIt": "Replace an abstract claim like 'peaceful' or 'engineered perfection' with one measurable condition and one quiet, specific fact. Let the understated detail prove the case."
    },
    "chandler-farewell-my-lovely-blonde": {
        "stealIt": "Illustrate a character's staggering impact by depicting the most solemn authority figure you can imagine committing a reckless act of vandalism. Keep it to one sentence."
    },
    "le-guin-candle-shadow": {
        "stealIt": "Express an inescapable trade-off in an eight-syllable equation using the formula 'To [action] is to [consequence]'. Pair light with shadow to show that every creative exertion bears an inevitable cost."
    },
    "seneca-shortness-of-life": {
        "stealIt": "Take a grievance people constantly lodge against nature or circumstance, like a shortage of time. Reframe the premise to show that abundance is squandered through careless neglect."
    },
    "dickens-tale-of-two-cities-opening": {
        "stealIt": "Capture a chaotic historical era through a rhythmic succession of extreme contradictions. Pair light with darkness, then conclude with a dry comment on the authorities who claimed everything was settled."
    }
}


def main():
    with open(CARDS_PATH, "r", encoding="utf-8") as f:
        cards = json.load(f)

    updated_count = 0
    for card in cards:
        cid = card["id"]
        if cid in UPDATES:
            for k, v in UPDATES[cid].items():
                card[k] = v
            updated_count += 1

    with open(CARDS_PATH, "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Successfully updated {updated_count} cards in {CARDS_PATH}")


if __name__ == "__main__":
    main()
