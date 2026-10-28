# scripts/curate_cluster_20.py — Curates 20 craft quotes from Cluster 20 (Craft Mechanics, Satirical Essay & Parable)
# Usage: python3 scripts/curate_cluster_20.py
# Requires: json, os

import json
import os

QUOTE_BANK_PATH = "content/quote-bank.json"

VETTED_CLUSTER_20 = [
    # 1. June Casagrande — It Was the Best of Sentences, It Was the Worst of Sentences (2010)
    {
        "quote": "It’s all good, clear, straightforward information that, unfortunately, has been shoved into the writer's mental Cuisinart.",
        "author": "June Casagrande",
        "work": "It Was the Best of Sentences, It Was the Worst of Sentences",
        "year": 2010,
        "translator": None,
        "hook": "How to diagnose sentence congestion before it reaches the page.",
        "why_it_lands": "The domestic appliance metaphor captures exactly what happens when writers treat a single sentence as a storage bin for unranked facts rather than an orderly delivery vehicle.",
        "tags": ["metaphor", "clarity", "editing", "syntax"]
    },
    {
        "quote": "Often, the simplest solution is to just drop all the conjunctions and fillers and parentheses and other connecting devices and make simple sentences out of what's left.",
        "author": "June Casagrande",
        "work": "It Was the Best of Sentences, It Was the Worst of Sentences",
        "year": 2010,
        "translator": None,
        "hook": "How to untangle complex syntax by stripping connective tissue.",
        "why_it_lands": "Casagrande advocates radical syntactic surgery: when a compound sentence stumbles under its own scaffolding, sever the joints and let the clauses stand alone.",
        "tags": ["syntax", "revision", "concision", "craft"]
    },
    {
        "quote": "It's the height of writer-serving writing and the root of my prejudice against semicolons.",
        "author": "June Casagrande",
        "work": "It Was the Best of Sentences, It Was the Worst of Sentences",
        "year": 2010,
        "translator": None,
        "hook": "How to distinguish reader-serving prose from writer-serving vanity.",
        "why_it_lands": "Casagrande names the cardinal sin of fussy prose—choosing punctuation to showcase syntactic pedigree rather than to ease the reader's comprehension.",
        "tags": ["punctuation", "candor", "reader-first", "craft"]
    },
    {
        "quote": "The Reader's needs should dictate which information you subordinate. If you subordinate the information about a ten-million-dollar gift, it should be a choice—a result of the power you wield over words.",
        "author": "June Casagrande",
        "work": "It Was the Best of Sentences, It Was the Worst of Sentences",
        "year": 2010,
        "translator": None,
        "hook": "How to use grammatical subordination as an instrument of deliberate emphasis.",
        "why_it_lands": "Subordination is reframed not as an abstract grammar rule, but as narrative triage—deciding what lives in the spotlight of the main clause and what waits in the wings.",
        "tags": ["subordination", "grammar", "emphasis", "syntax"]
    },

    # 2. Chuck Palahniuk — Consider This: Moments in My Writing Life (2020)
    {
        "quote": "That’s using what I call ‘cultural precedent’ and moving the reader from a common experience, through several intermediary, escalating examples, and ultimately arriving at an extreme the reader could’ve and would’ve never accepted if you’d presented it from the start.",
        "author": "Chuck Palahniuk",
        "work": "Consider This: Moments in My Writing Life",
        "year": 2020,
        "translator": None,
        "hook": "How to escort the reader into taboo territory through escalating cultural precedents.",
        "why_it_lands": "Palahniuk details the frog-in-boiling-water mechanics of transgressive fiction: anchor the reader in universal banality before incrementally ratcheting the stakes into absurdity.",
        "tags": ["transgressive", "escalation", "structure", "craft"]
    },
    {
        "quote": "Whether it was Channing Tatum or Jenna Jameson, you’d feel cheated. As readers or exotic dance enthusiasts, we want tension. We want a gradual discovery process.",
        "author": "Chuck Palahniuk",
        "work": "Consider This: Moments in My Writing Life",
        "year": 2020,
        "translator": None,
        "hook": "How to maintain reader appetite through disciplined withholding.",
        "why_it_lands": "Palahniuk equates storytelling to slow-burn performance, warning that instant gratification kills narrative tension faster than bad grammar.",
        "tags": ["tension", "pacing", "curiosity", "metaphor"]
    },
    {
        "quote": "The author photo is the ‘reality’ that underscores the magic of the fictional work. It’s as if an adult version of our annual school photos, this posed, stylized us, will convince readers that writing is a real job.",
        "author": "Chuck Palahniuk",
        "work": "Consider This: Moments in My Writing Life",
        "year": 2020,
        "translator": None,
        "hook": "How to expose authorial marketing as psychological theatre.",
        "why_it_lands": "Palahniuk punctures the solemn vanity of author headshots, unmasking the promotional portrait as an insecure adult pantomime designed to prove storytelling is honest labor.",
        "tags": ["satire", "metafiction", "author-persona", "candor"]
    },
    {
        "quote": "If you can identify the archetype your story depicts, you can more effectively fulfill the unconscious expectations of the reader.",
        "author": "Chuck Palahniuk",
        "work": "Consider This: Moments in My Writing Life",
        "year": 2020,
        "translator": None,
        "hook": "How to harness mythic archetypes to satisfy subliminal narrative appetite.",
        "why_it_lands": "Palahniuk frames archetype not as rigid formula, but as psychological shorthand—meeting the reader's deep subconscious expectations before destabilizing them.",
        "tags": ["archetype", "myth", "psychology", "craft"]
    },

    # 3. Harishankar Parsai — Awara Bheed Ke Khatare (1998)
    {
        "quote": "गांधीजी से सब डरते हैं, सबसे अधिक वे डरते हैं, जो उनके विरोधी हैं।",
        "author": "Harishankar Parsai",
        "work": "Awara Bheed Ke Khatare",
        "year": 1998,
        "translator": None,
        "hook": "How to invert an adversary's rhetoric into involuntary veneration.",
        "why_it_lands": "Parsai identifies the ultimate irony of Gandhi's political legacy: those who despise his philosophy are the very ones most haunted by its moral authority.",
        "tags": ["irony", "satire", "hindi-literature", "politics"]
    },
    {
        "quote": "जो करोड़ खर्च करेगा, वह पाँच करोड़ कहीं से निकालेगा ही। इस तरह जनसेवकों का व्यापार और लूट एक साथ होगी।",
        "author": "Harishankar Parsai",
        "work": "Awara Bheed Ke Khatare",
        "year": 1998,
        "translator": None,
        "hook": "How to expose democratic corruption with mathematical inevitability.",
        "why_it_lands": "Parsai strips electoral democracy down to a predatory ledger, demonstrating that when public office requires capital expenditure, governance becomes an extortionate business.",
        "tags": ["satire", "clarity", "hindi-literature", "corruption"]
    },
    {
        "quote": "तुम इन लोगों की परवाह मत करो. ये उस रूमाल को उठाने योग्य भी नहीं हैं, जो तुम्हारे हाथ से गिर गया हो।",
        "author": "Harishankar Parsai",
        "work": "Awara Bheed Ke Khatare",
        "year": 1998,
        "translator": None,
        "hook": "How to deliver a devastating dismissal through an aristocratic domestic prop.",
        "why_it_lands": "Parsai captures bourgeois contempt in a single devastating gesture, measuring social worth against the indignity of retrieving a fallen handkerchief.",
        "tags": ["dialogue", "satire", "hindi-literature", "class"]
    },
    {
        "quote": "जातियों के संगठन हैं खास राजनेता के पीछे। जातियों की सशस्त्र फौजें हैं। राजनेता जाति के नाम पर अपनी पार्टी के लिए समर्थन माँगते हैं। मत माँगते हैं।",
        "author": "Harishankar Parsai",
        "work": "Awara Bheed Ke Khatare",
        "year": 1998,
        "translator": None,
        "hook": "How to trace the militarization of identity politics in clipped, staccato clauses.",
        "why_it_lands": "Parsai moves from social organization to private militia in four unadorned declarative sentences, refusing to beautify the grim machinery of communal mobilization.",
        "tags": ["staccato", "political-thought", "hindi-literature", "candor"]
    },

    # 4. George Orwell — Selected Essays (1946)
    {
        "quote": "Writing a book is a horrible, exhausting struggle, like a long bout of some painful illness. One would never undertake such a thing if one were not driven on by some demon whom one can neither resist nor understand.",
        "author": "George Orwell",
        "work": "Selected Essays",
        "year": 1946,
        "translator": None,
        "hook": "How to depict the agonizing compulsion of authorship through a somatic simile.",
        "why_it_lands": "Orwell rejects the romantic posture of literary creation, comparing book-length composition to a chronic physical sickness driven by an irrational internal demon.",
        "tags": ["simile", "candor", "writing-process", "confession"]
    },
    {
        "quote": "A duke who has served a prison sentence is still a duke, whereas a mere man about town, if once disgraced, ceases to be ‘about town’ for evermore.",
        "author": "George Orwell",
        "work": "Selected Essays",
        "year": 1946,
        "translator": None,
        "hook": "How to expose class asymmetry in a balanced antithetical clause.",
        "why_it_lands": "Orwell illustrates the double standard of British caste: aristocratic pedigree survives felonious disgrace, while middle-class respectability dissolves at the first touch of scandal.",
        "tags": ["antithesis", "class", "social-commentary", "syntax"]
    },
    {
        "quote": "If a man cannot enjoy the return of spring, why should he be happy in a labour-saving Utopia?",
        "author": "George Orwell",
        "work": "Selected Essays",
        "year": 1946,
        "translator": None,
        "hook": "How to challenge technocratic utopianism with an elemental sensory test.",
        "why_it_lands": "Orwell pierces political engineering with biological simplicity, asking why engineers bother designing an automated paradise for human beings who have forgotten how to marvel at dirt.",
        "tags": ["rhetorical-question", "humanism", "clarity", "philosophy"]
    },
    {
        "quote": "All one can say is that, while civilization remains such that one needs distraction from time to time, ‘light’ literature has its appointed place; also that there is such a thing as sheer skill, or native grace, which may have more survival value than erudition or intellectual power.",
        "author": "George Orwell",
        "work": "Selected Essays",
        "year": 1946,
        "translator": None,
        "hook": "How to defend narrative craft against intellectual snobbery.",
        "why_it_lands": "Orwell defends readable popular storytelling with sober pragmatism, arguing that effortless prose grace will outlive heavy academic erudition.",
        "tags": ["craft", "readability", "criticism", "pragmatism"]
    },

    # 5. Patrick Ness — A Monster Calls (2011)
    {
        "quote": "The yew tree is the most important of all the healing trees, it said. It lives for thousands of years. Its berries, its bark, its leaves, its sap, its pulp, its wood, they all thrum and burn and twist with life.",
        "author": "Patrick Ness",
        "work": "A Monster Calls",
        "year": 2011,
        "translator": None,
        "hook": "How to animate an ancient botanical symbol with escalating polysyndetic verbs.",
        "why_it_lands": "Ness stacks the physical components of the tree before igniting them with active sensory verbs ('thrum and burn and twist'), turning an ordinary graveyard staple into a pulsating engine of myth.",
        "tags": ["sensory", "verbs", "symbolism", "mythic"]
    },
    {
        "quote": "‘There’s a lot of pain,’ she said. ‘More than there should be.’",
        "author": "Patrick Ness",
        "work": "A Monster Calls",
        "year": 2011,
        "translator": None,
        "hook": "How to convey terminal agony through quiet, unadorned dialogue.",
        "why_it_lands": "Rather than reaching for medical jargon or melodramatic shrieks, Ness uses eight monosyllables to let the maternal admission land with catastrophic, hollow weight.",
        "tags": ["dialogue", "understatement", "grief", "restraint"]
    },
    {
        "quote": "There are worse things than being invisible, it said.",
        "author": "Patrick Ness",
        "work": "A Monster Calls",
        "year": 2011,
        "translator": None,
        "hook": "How to pivot a childhood fear into an existential warning.",
        "why_it_lands": "The monster overturns the juvenile instinct to blend into the background, warning that total social erasure is a living death far more terrifying than punishment.",
        "tags": ["brevity", "dialogue", "parable", "truth"]
    },
    {
        "quote": "‘Things are going a little faster than I’d hoped, sweetheart,’ she said, and her voice was thick, thick in a way that made Conor’s stomach twist even harder.",
        "author": "Patrick Ness",
        "work": "A Monster Calls",
        "year": 2011,
        "translator": None,
        "hook": "How to anchor a devastating diagnosis in acoustic and somatic sensory detail.",
        "why_it_lands": "The repetition of 'thick' shifts the scene from verbal exchange into tactile dread, transmitting maternal decline through acoustic heaviness and an involuntary visceral reflex.",
        "tags": ["sensory", "repetition", "somatic", "pathos"]
    }
]

def main():
    with open(QUOTE_BANK_PATH, "r", encoding="utf-8") as f:
        quote_bank = json.load(f)

    print(f"Existing quote bank count: {len(quote_bank)}")

    # Check for duplicates by quote prefix
    existing_quotes = {q["quote"].strip()[:50].lower() for q in quote_bank}
    
    added_count = 0
    for entry in VETTED_CLUSTER_20:
        key = entry["quote"].strip()[:50].lower()
        if key in existing_quotes:
            print(f"Skipping duplicate: {entry['work']} - {entry['quote'][:40]}...")
            continue
        quote_bank.append(entry)
        existing_quotes.add(key)
        added_count += 1

    print(f"Added {added_count} new vetted quotes from Cluster 20.")
    print(f"New quote bank total: {len(quote_bank)}")

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(quote_bank, f, indent=2, ensure_ascii=False)
        f.write("\n")

if __name__ == "__main__":
    main()
