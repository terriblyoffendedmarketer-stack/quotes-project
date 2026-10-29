# scripts/curate_cluster_44.py — Vets and integrates 20 quotes from Cluster 44 into quote-bank.json
# Usage: python3 scripts/curate_cluster_44.py

import json

new_quotes = [
    # Joe Abercrombie — The Blade Itself (2006)
    {
        "quote": "Once you’ve got a task to do, it’s better to do it than to live with the fear of it.",
        "author": "Joe Abercrombie",
        "work": "The Blade Itself",
        "year": 2006,
        "hook": "How to anchor a warrior's mindset in unsentimental pragmatic stoicism",
        "why_it_lands": "Abercrombie gives Logen Ninefingers a plainspoken, rhythmic proverb that cuts through romantic heroism. The blunt utilitarian cadence turns visceral dread into an immediate physical chore that must be completed simply to clear the mental ledger.",
        "tags": ["voice", "stoicism", "characterization"]
    },
    {
        "quote": "Things had taken a turn for the worse alright. A moment ago that had hardly seemed possible, but fate had found a way.",
        "author": "Joe Abercrombie",
        "work": "The Blade Itself",
        "year": 2006,
        "hook": "How to undercut high-stakes tension with dry fatalistic irony",
        "why_it_lands": "Abercrombie punctures dramatic gravity by treating catastrophe as a minor bureaucratic inevitability. The colloquial phrasing ('fate had found a way') personifies misfortune not as a grand tragic fury, but as a stubborn, petty nuisance.",
        "tags": ["irony", "voice", "understatement"]
    },
    {
        "quote": "Damn, he was bored. It was a fact, he was only now beginning to realise, that the conversation of the drunk is only interesting to the drunk.",
        "author": "Joe Abercrombie",
        "work": "The Blade Itself",
        "year": 2006,
        "hook": "How to dismantle high-society camaraderie through solitary sober irritation",
        "why_it_lands": "The prose cuts through aristocratic revelry with devastating internal clarity. The repetition of 'drunk' at both ends of the clause balances the observation like a mathematical theorem, delivering an immediately recognizable social diagnosis.",
        "tags": ["internal monologue", "wit", "social critique"]
    },
    {
        "quote": "They will catch you, and they will break your legs with hammers in the city square, so you can never run again.",
        "author": "Joe Abercrombie",
        "work": "The Blade Itself",
        "year": 2006,
        "hook": "How to convey state intimidation through unadorned anatomical violence",
        "why_it_lands": "Abercrombie avoids gothic atmosphere or psychological threats, choosing instead the flat, mechanical reality of blunt tools on bone. The causal finality ('so you can never run again') makes the physical consequence far more terrifying than any rhetorical flourish.",
        "tags": ["visceral voice", "understatement", "tension"]
    },

    # Chuck Palahniuk — Invisible Monsters (1999)
    {
        "quote": "You can live a completely normal, regular life. You just can’t let anybody get close enough to you to learn the truth.",
        "author": "Chuck Palahniuk",
        "work": "Invisible Monsters",
        "year": 1999,
        "hook": "How to define social survival as total emotional quarantine",
        "why_it_lands": "Palahniuk hinges the sentence on a devastating trade-off: external normalcy is possible only if human intimacy is permanently outlawed. The flat conversational delivery turns profound alienation into practical lifestyle advice.",
        "tags": ["voice", "psychological truth", "aphorism"]
    },
    {
        "quote": "The word love tastes like earwax when I think about Manus and Evie.",
        "author": "Chuck Palahniuk",
        "work": "Invisible Monsters",
        "year": 1999,
        "hook": "How to destroy romantic sentiment through abrasive sensory synesthesia",
        "why_it_lands": "Palahniuk pairs an abstract, sacred emotional term ('love') with a revolting somatic sensation ('earwax'). The sensory shock short-circuits cliché, instantly conveying the narrator's bitter physical revulsion.",
        "tags": ["sensory detail", "metaphor", "voice"]
    },
    {
        "quote": "That’s what I love about fire, how it would kill me as quick as anybody else. How it can’t know I’m its mother.",
        "author": "Chuck Palahniuk",
        "work": "Invisible Monsters",
        "year": 1999,
        "hook": "How to find radical solace in non-discriminating physical destruction",
        "why_it_lands": "The arsonist's affection for the flame stems from its total refusal of human narcissism. By celebrating that fire cannot recognize kinship or authorial origin, Palahniuk articulates an intimate longing for absolute, unsparing equality.",
        "tags": ["paradox", "psychological truth", "visceral voice"]
    },
    {
        "quote": "The point is whoever cuts your ears off is the one you’ll hate for the rest of your life.",
        "author": "Chuck Palahniuk",
        "work": "Invisible Monsters",
        "year": 1999,
        "hook": "How to deliver an abrasive moral lesson through brutal physical mutilation",
        "why_it_lands": "Palahniuk strips away psychological nuance to anchor long-term trauma in a single irreversible bodily act. The casual cadence of 'The point is' clashes with the horror of the deed, creating an unsettling moral certainty.",
        "tags": ["understatement", "morality", "voice"]
    },

    # Michael Crichton — Sphere (1987)
    {
        "quote": "Every conception of extraterrestrial life… has been basically human.",
        "author": "Michael Crichton",
        "work": "Sphere",
        "year": 1987,
        "hook": "How to expose anthropocentric bias in speculative investigation",
        "why_it_lands": "Crichton diagnosis the intellectual failing at the heart of first-contact science: even humanity's wildest fictional monsters are merely distorted mirrors of human anatomy and psychology. The economy of the observation prepares the reader for genuine, incomprehensible alterity.",
        "tags": ["science fiction craft", "clarity", "philosophy"]
    },
    {
        "quote": "God, it’s big. You know, we’re the first people in human history to see a free-swimming giant squid. This should be a great moment.",
        "author": "Michael Crichton",
        "work": "Sphere",
        "year": 1987,
        "hook": "How to collide historical scientific triumph with impending physical dread",
        "why_it_lands": "Crichton sets up the majestic language of intellectual discovery ('first people in human history') only to deflate it with the hollow conditional of 'This should be a great moment.' The psychological rift between abstract achievement and deep-sea panic lands with chilling restraint.",
        "tags": ["irony", "suspense", "sensory detail"]
    },
    {
        "quote": "That’s a psychologist’s trick, isn’t it? To repeat the last word in a sentence. It’s a way to keep the person talking.",
        "author": "Michael Crichton",
        "work": "Sphere",
        "year": 1987,
        "hook": "How to create claustrophobic paranoia by exposing clinical dialogue tactics",
        "why_it_lands": "Inside a deep-sea habitat where air and sanity are dwindling, the protagonist dismantles his own conversational mechanics. Laying bare the clinician's conversational mirror weaponizes ordinary dialogue into a symptom of escalating suspicion.",
        "tags": ["dialogue", "paranoia", "psychological realism"]
    },
    {
        "quote": "Nothing else. It is not your ape-nature, not your tool-using nature, not language or your violence or your caring for young or your social groupings. Your greatness lies in imagination.",
        "author": "Michael Crichton",
        "work": "Sphere",
        "year": 1987,
        "hook": "How to strip away anthropological categories to isolate a species' defining trait",
        "why_it_lands": "The sentence works by methodical negative elimination: biology, technology, linguistics, violence, and social altruism are all systematically dismissed. The rhythmic crescendo lands on 'imagination' as both humanity's supreme power and its lethal curse.",
        "tags": ["syntax", "rhetoric", "thematic payoff"]
    },

    # Exurb1a — The Fifth Science (2018)
    {
        "quote": "Void workers are often told that decompression is painless, that one passes out immediately. This is a lie to maintain the steady stream of colonisation volunteers.",
        "author": "Exurb1a",
        "work": "The Fifth Science",
        "year": 2018,
        "hook": "How to expose institutional recruitment propaganda through physiological reality",
        "why_it_lands": "Exurb1a pairs the serene clinical myth of instantaneous death with the cold, administrative calculation of imperial expansion. The blunt, declarative sentence ('This is a lie...') strips all romantic grandeur from space colonization, leaving only cheap labour and bodily ruin.",
        "tags": ["worldbuilding", "clarity", "political critique"]
    },
    {
        "quote": "They fired anger. They dispatched hope. Yes, with all these hurdles dead, Dr. Ek would know true contentment soon.",
        "author": "Exurb1a",
        "work": "The Fifth Science",
        "year": 2018,
        "hook": "How to treat human emotional faculties as corporate obstacles to be liquidated",
        "why_it_lands": "By applying the vocabulary of corporate layoffs ('fired', 'dispatched') to fundamental human emotions, Exurb1a turns psychological excision into a horrific parody of efficiency. The bitter irony of 'contentment' achieved through emotional death lands with surgical chill.",
        "tags": ["satire", "dark humor", "science fiction craft"]
    },
    {
        "quote": "In even asking a question one affects the world.",
        "author": "Exurb1a",
        "work": "The Fifth Science",
        "year": 2018,
        "hook": "How to compress quantum epistemology into an unadorned aphorism",
        "why_it_lands": "Exurb1a translates the observer effect from quantum physics into moral philosophy in eight simple words. The syntax carries an ancient, meditative weight, asserting that passive neutrality is an illusion.",
        "tags": ["aphorism", "philosophy", "economy"]
    },
    {
        "quote": "I don't think taking photos of crumpled tissues is very clever. I don't think taking photos of yourself with minor celebrities makes you an interesting person... But something has gone awful, awful wrong.",
        "author": "Exurb1a",
        "work": "The Fifth Science",
        "year": 2018,
        "hook": "How to capture civilizational exhaustion through ordinary cultural irritation",
        "why_it_lands": "The voice of an interstellar working engineer grounds grandiose science fiction in everyday annoyance. The progression from petty social media vanity to the repetition of 'awful, awful wrong' diagnoses an entire empire's moral rot through its frivolous art.",
        "tags": ["voice", "social critique", "rhythm"]
    },

    # George Orwell — Animal Farm (1945)
    {
        "quote": "No animal in England is free. The life of an animal is misery and slavery: that is the plain truth.",
        "author": "George Orwell",
        "work": "Animal Farm",
        "year": 1945,
        "hook": "How to establish revolutionary premise through unadorned declarative prose",
        "why_it_lands": "Orwell's mastery of political prose lies in his refusal of decorative rhetoric. Old Major's opening premise uses short, uncompromising Anglo-Saxon words that present revolutionary diagnosis not as theoretical debate, but as self-evident physical reality.",
        "tags": ["clarity", "opening", "political prose"]
    },
    {
        "quote": "‘Comrade,’ said Snowball, ‘can you not understand that liberty is worth more than ribbons?’",
        "author": "George Orwell",
        "work": "Animal Farm",
        "year": 1945,
        "hook": "How to contrast political emancipation with superficial vanity",
        "why_it_lands": "The dialogue crystallizes the ideological gulf between collective liberation and bourgeois triviality in a single question. By opposing the vast abstract concept of 'liberty' with the petty domestic ornament of 'ribbons', Orwell exposes the difficulty of awakening political consciousness.",
        "tags": ["dialogue", "contrast", "parable craft"]
    },
    {
        "quote": "‘Donkeys live a long time. None of you has ever seen a dead donkey.’",
        "author": "George Orwell",
        "work": "Animal Farm",
        "year": 1945,
        "hook": "How to embody historical skepticism through cryptic folk wisdom",
        "why_it_lands": "Benjamin the donkey refuses both revolutionary euphoria and counter-revolutionary panic. His refusal to elaborate forces the listener to confront deep time, suggesting that regimes rise and fall while systemic misery outlives them all.",
        "tags": ["characterization", "voice", "understatement"]
    },
    {
        "quote": "But if there were hardships to be borne, they were partly offset by the fact that life nowadays had a greater dignity than it had had before. There were more songs, more speeches, more processions.",
        "author": "George Orwell",
        "work": "Animal Farm",
        "year": 1945,
        "hook": "How to expose authoritarian substitution of spectacle for substance",
        "why_it_lands": "Orwell documents the psychological sleight of hand by which totalitarian regimes compensate for physical deprivation. The rhythmic catalogue ('more songs, more speeches, more processions') exposes how empty ceremonial noise is manufactured to drown out the sounds of empty bellies.",
        "tags": ["irony", "political critique", "syntax"]
    }
]

def main():
    bank_path = "content/quote-bank.json"
    with open(bank_path, "r", encoding="utf-8") as f:
        bank = json.load(f)

    existing_quotes = {q["quote"].strip() for q in bank}
    added = 0

    for q in new_quotes:
        if q["quote"].strip() not in existing_quotes:
            bank.append(q)
            existing_quotes.add(q["quote"].strip())
            added += 1

    with open(bank_path, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)

    print(f"Added {added} vetted quotes from Cluster 44. Total in bank: {len(bank)}")

if __name__ == "__main__":
    main()
