# scripts/curate_cluster_43.py — Vets and integrates 20 quotes from Cluster 43 into quote-bank.json
# Usage: python3 scripts/curate_cluster_43.py

import json

new_quotes = [
    # Haruki Murakami — Blind Willow, Sleeping Woman (2006, trans. Philip Gabriel)
    {
        "quote": "It’s not like the total physical and mental commitment you have to make for the year or two it takes to compose a novel. You merely enter a room, finish your work, and exit. That’s it.",
        "author": "Haruki Murakami",
        "work": "Blind Willow, Sleeping Woman",
        "year": 2006,
        "translator": "Philip Gabriel",
        "hook": "How to contrast short fiction and the novel through spatial metaphor",
        "why_it_lands": "Murakami demystifies the craft of the short story by comparing it to walking in and out of a single room, contrasted with the exhausting, years-long architectural siege of a novel. The casual, flat rhythm ('That’s it') emphasizes the intense, contained focus of the form.",
        "tags": ["writing craft", "form", "voice"]
    },
    {
        "quote": "It wasn’t like there was some obvious change. Actually, the problem was more a lack of change.",
        "author": "Haruki Murakami",
        "work": "Blind Willow, Sleeping Woman",
        "year": 2006,
        "translator": "Philip Gabriel",
        "hook": "How to diagnose existential dread through the absence of momentum",
        "why_it_lands": "Murakami locates horror not in sudden catastrophe, but in suffocating stasis. The conversational hesitation ('It wasn't like... Actually...') mirrors the slow, creeping realization that absolute predictability is its own quiet trap.",
        "tags": ["understatement", "psychological truth", "internal monologue"]
    },
    {
        "quote": "Newspapers are all the same, no matter where you go. They never tell you what you really want to know.",
        "author": "Haruki Murakami",
        "work": "Blind Willow, Sleeping Woman",
        "year": 2006,
        "translator": "Philip Gabriel",
        "hook": "How to articulate narrative disillusionment with casual finality",
        "why_it_lands": "The sweeping, melancholy generality contrasts the noisy machinery of public reportage with the intimate, insoluble mysteries of private life. The plainspoken cadence delivers an instinctive emotional truth about information overload without human depth.",
        "tags": ["voice", "philosophy", "realism"]
    },
    {
        "quote": "I don’t know when it began, or when it ended, but before I knew it I was locked away, alone and numb in the endless winter of that world of ice.",
        "author": "Haruki Murakami",
        "work": "Blind Willow, Sleeping Woman",
        "year": 2006,
        "translator": "Philip Gabriel",
        "hook": "How to render psychological dissociation through sensory climate",
        "why_it_lands": "Murakami blurs temporal boundaries ('I don't know when it began, or when it ended') to mimic the disorienting drift of depression. The landscape of absolute ice physicalizes emotional numbness with haunting dreamscape clarity.",
        "tags": ["atmosphere", "sensory detail", "psychological truth"]
    },

    # Harishankar Parsai — Awara Bheed Ke Khatare (1998)
    {
        "quote": "क्लर्क को जुकाम है। उसे छींक आती है। साहब की चाँद निकली है। क्लर्क को भ्रम होता है कि उसकी छींक के छींटे साहब की चाँद पर गिर गए होंगे और साहब नाराज हो गया होगा।",
        "author": "Harishankar Parsai",
        "work": "Awara Bheed Ke Khatare",
        "year": 1998,
        "hook": "How to dramatize feudal office paranoia through microscopic somatic absurdity",
        "why_it_lands": "Parsai transposes Chekhov's tragicomic clerk into the brutal hierarchy of Indian bureaucracy. The staccato clauses escalate from an ordinary cold to the terrifying imagined offense of sneeze droplets landing on a supervisor's bald skull, laying bare the psychological terror of subjection.",
        "tags": ["satire", "bureaucracy", "humor"]
    },
    {
        "quote": "जो समाज कसमसाता नहीं, वह जड़ रह जाता है। इस कसमसाहट के कारण इक्का-दुक्का घटनाएँ होती हैं। ये प्रतीक हैं—व्यापक परिवर्तन और विकास की इच्छा की।",
        "author": "Harishankar Parsai",
        "work": "Awara Bheed Ke Khatare",
        "year": 1998,
        "hook": "How to interpret social unrest as an index of collective vitality",
        "why_it_lands": "Parsai distinguishes between paralyzed societal inertia and productive political agitation. By treating scattered dissent not as criminal disruptions but as vital physical spasms ('kasmasahat') of an awakening consciousness, he provides a profound sociological lens.",
        "tags": ["sociology", "political critique", "philosophy"]
    },
    {
        "quote": "जातियों के संगठन हैं खास राजनेता के पीछे। जातियों की सशस्त्र फौजें हैं। राजनेता जाति के नाम पर अपनी पार्टी के लिए समर्थन माँगते हैं। मत माँगते हैं।",
        "author": "Harishankar Parsai",
        "work": "Awara Bheed Ke Khatare",
        "year": 1998,
        "hook": "How to map electoral tribalism through unadorned structural cadence",
        "why_it_lands": "Parsai refuses polite euphemisms for caste politics, laying out the mechanism in blunt, declarative strokes. The final rhythmic division between seeking ideological support and merely harvesting votes ('समर्थन माँगते हैं। मत माँगते हैं।') captures the transactional cynicism of mob democracy.",
        "tags": ["satire", "clarity", "subcontinental realism"]
    },
    {
        "quote": "मैंने एक रसगुल्ला उठाया। मेजबान से कहा—आप भी तो खाइए। उन्होंने कहा—अरे साहब, आप खाइए। हम तो खाते ही रहते हैं।",
        "author": "Harishankar Parsai",
        "work": "Awara Bheed Ke Khatare",
        "year": 1998,
        "hook": "How to puncture performative hospitality through a single culinary exchange",
        "why_it_lands": "In five short lines of dialogue, Parsai skewers the hollow theatre of middle-class Indian etiquette. The host's haughty dismissal ('हम तो खाते ही रहते हैं') simultaneously feigns generosity while flexing casual domestic abundance.",
        "tags": ["satire", "dialogue", "cultural critique"]
    },

    # Umberto Eco — Six Walks in the Fictional Woods (1994)
    {
        "quote": "Every text, after all, is a lazy machine asking the reader to do some of its work.",
        "author": "Umberto Eco",
        "work": "Six Walks in the Fictional Woods",
        "year": 1994,
        "hook": "How to define narrative mechanism through collaborative cognitive labor",
        "why_it_lands": "Eco's mechanical metaphor dismantles the idea of the passive reader. A story is not a self-sufficient spectacle but an inert contraption that only comes alive when the audience invests its own memory, inference, and imaginative energy to crank the gears.",
        "tags": ["narrative theory", "aphorism", "writing craft"]
    },
    {
        "quote": "If something important or gripping is going to take place, we have to cultivate the art of lingering.",
        "author": "Umberto Eco",
        "work": "Six Walks in the Fictional Woods",
        "year": 1994,
        "hook": "How to build narrative tension by deliberately delaying arrival",
        "why_it_lands": "Eco articulates the secret architecture of suspense: speed dissolves anticipation, while deliberate retardation intensifies it. By reframing pacing not as efficiency but as the pleasurable stretching of narrative time, he instructs writers in structural control.",
        "tags": ["pacing", "suspense", "story structure"]
    },
    {
        "quote": "Texts are not always so wicked, and are usually inclined to allow the reader the pleasure of making a guess which will then be proved correct.",
        "author": "Umberto Eco",
        "work": "Six Walks in the Fictional Woods",
        "year": 1994,
        "hook": "How to reward reader anticipation without feeling predictable",
        "why_it_lands": "Eco reminds the writer that subverting expectations is not the only virtue; the human brain takes immense delight in validated deduction. The sly personification of the text as 'not always so wicked' balances trickery against reader satisfaction.",
        "tags": ["reader response", "mystery craft", "wit"]
    },
    {
        "quote": "I know that Rip Van Winkle has never existed; nevertheless, I not only believe but I assume to know that up the Hudson River one can really find the Catskill Mountains.",
        "author": "Umberto Eco",
        "work": "Six Walks in the Fictional Woods",
        "year": 1994,
        "hook": "How to anchor impossible fictional fables in concrete geography",
        "why_it_lands": "Eco illustrates the double-think required by literary belief: the mind simultaneously holds the falsity of the protagonist and the physical truth of the landscape. This hybrid trust is the foundation upon which all worldbuilding rests.",
        "tags": ["worldbuilding", "philosophy", "storytelling"]
    },

    # Chuck Palahniuk — Survivor (1999)
    {
        "quote": "The caseworker wouldn’t be dropping by for a breakfast gin and tonic if there hadn’t been another suicide last night.",
        "author": "Chuck Palahniuk",
        "work": "Survivor",
        "year": 1999,
        "hook": "How to establish dark institutional normalization through causal inversion",
        "why_it_lands": "Palahniuk pairs an early-morning cocktail with catastrophic death in a single sentence. The casual conjunction implies that horror has become routine administrative business, establishing the novel's satirical world with brutal speed.",
        "tags": ["opening", "dark humor", "voice"]
    },
    {
        "quote": "To get lipstick out of a collar, rub in a little white vinegar. For stubborn protein-based stains, like semen, try rinsing with cold salt water, then wash as usual.",
        "author": "Chuck Palahniuk",
        "work": "Survivor",
        "year": 1999,
        "hook": "How to collide domestic housekeeping manuals with transgressive violence",
        "why_it_lands": "Palahniuk's signature device: borrowing the clinical, reassuring tone of a 1950s housekeeping manual to solve the bodily crime scenes of modern life. The deadpan technical precision makes the underlying corruption feel intensely visceral.",
        "tags": ["voice", "juxtaposition", "satire"]
    },
    {
        "quote": "The big question people ask isn’t ‘What’s the nature of existence?’ The big question people ask is ‘What’s that from?’",
        "author": "Chuck Palahniuk",
        "work": "Survivor",
        "year": 1999,
        "hook": "How to diagnose cultural shallowness through competing interrogatives",
        "why_it_lands": "Palahniuk captures the shift from philosophical inquiry to pop-cultural citation. By contrasting an age-old metaphysical question with the reflex to identify a brand, movie, or song, he exposes a society that navigates reality entirely through secondhand references.",
        "tags": ["cultural critique", "aphorism", "dialogue"]
    },
    {
        "quote": "Long-term, we’re all going to die. Then our bodies will rot. No surprise there. Short-term, we’re going to live happily ever after.",
        "author": "Chuck Palahniuk",
        "work": "Survivor",
        "year": 1999,
        "hook": "How to dismantle commercial optimism with blunt biological certainty",
        "why_it_lands": "Palahniuk inverts the usual corporate framing of 'short-term vs. long-term'. By placing biological decomposition first as obvious and guaranteed, the promise of living 'happily ever after' is exposed as a childish, desperate delusion.",
        "tags": ["irony", "rhythm", "voice"]
    },

    # Bhagat Singh — Why I Am an Atheist (1930)
    {
        "quote": "Whether it is such an undue pride that has led me to atheism or whether it is after very careful study of the subject and after much consideration that I have come to disbelieve in God is a question that I intend to discuss here.",
        "author": "Bhagat Singh",
        "work": "Why I Am an Atheist",
        "year": 1930,
        "hook": "How to frame polemical self-defense with judicial objectivity",
        "why_it_lands": "Writing from the shadow of the gallows, Bhagat Singh refuses defensive rage or emotional pleas. The balanced syntactic structure ('Whether it is... or whether it is...') adopts the calm, dispassionate clarity of a philosophical treatise, disarming his critics before dismantling their arguments.",
        "tags": ["rhetoric", "opening", "moral courage"]
    },
    {
        "quote": "To the extent that you believe in an almighty, omnipresent, omniscient and omnipotent God—who created the earth or world, please let me know, why did he create it? This world of woes and miseries, a veritable, eternal combination of numberless tragedies: not a single soul being perfectly satisfied.",
        "author": "Bhagat Singh",
        "work": "Why I Am an Atheist",
        "year": 1930,
        "hook": "How to escalate rhetorical pressure on divine benevolence",
        "why_it_lands": "Singh begins with the heavy theological catalogue of traditional divine attributes ('almighty, omnipresent, omniscient and omnipotent') only to shatter them against observable human suffering. The cadence builds toward an unanswerable empirical indictment: 'not a single soul being perfectly satisfied.'",
        "tags": ["rhetoric", "polemic", "cadence"]
    },
    {
        "quote": "It takes a loud voice to make the deaf hear.",
        "author": "Bhagat Singh",
        "work": "Why I Am an Atheist",
        "year": 1930,
        "hook": "How to condense revolutionary justification into an iconic physical aphorism",
        "why_it_lands": "Singh distills the entire tactical rationale of militant agitation into eight monosyllabic words. The visceral sensory logic—that systemic political inertia requires acoustic shock—explains why pamphlets and polite petitions were abandoned for explosive action.",
        "tags": ["aphorism", "manifesto craft", "clarity"]
    },
    {
        "quote": "For us, compromise never means surrender, but a step forward and some rest. That is all and nothing else.",
        "author": "Bhagat Singh",
        "work": "Why I Am an Atheist",
        "year": 1930,
        "hook": "How to redefine political compromise without ideological surrender",
        "why_it_lands": "Singh defines political negotiation with soldierly pragmatism: a tactical pause to catch breath before the next offensive, not an abandonment of principle. The unyielding closure ('That is all and nothing else') rejects both naive absolutism and defeatist betrayal.",
        "tags": ["clarity", "voice", "political thought"]
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

    print(f"Added {added} vetted quotes from Cluster 43. Total in bank: {len(bank)}")

if __name__ == "__main__":
    main()
