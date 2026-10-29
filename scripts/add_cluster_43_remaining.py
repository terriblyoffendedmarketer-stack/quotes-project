# scripts/add_cluster_43_remaining.py — Adds 5 fresh unique quotes to complete Cluster 43 (20 total)

import json

fresh_quotes = [
    {
        "quote": "It’s like being in an elevator when it breaks down and you’re trapped inside with strangers.",
        "author": "Haruki Murakami",
        "work": "Blind Willow, Sleeping Woman",
        "year": 2006,
        "translator": "Philip Gabriel",
        "hook": "How to compress urban social dread into a broken elevator",
        "why_it_lands": "Murakami captures modern isolation through forced physical proximity in a mechanical breakdown. The casual simile turns a familiar metropolitan inconvenience into an emblem of psychic claustrophobia.",
        "tags": ["simile", "claustrophobia", "voice"]
    },
    {
        "quote": "It wasn’t bad, it was just missing that extra element that sends us flying to another world.",
        "author": "Haruki Murakami",
        "work": "Blind Willow, Sleeping Woman",
        "year": 2006,
        "translator": "Philip Gabriel",
        "hook": "How to describe aesthetic disappointment through understated longing",
        "why_it_lands": "Murakami avoids academic critical jargon to evaluate music through visceral transport. The simple admission of 'missing that extra element' captures the quiet heartbreak of encountering competent but uninspired art.",
        "tags": ["understatement", "artistic craft", "reflection"]
    },
    {
        "quote": "'मार्केट इकॉनमी’... कंट्रोल लाइसेंस सब गए। स्वतंत्र पूँजीवाद और बाजार की शोषक व्यवस्था आ गई।",
        "author": "Harishankar Parsai",
        "work": "Awara Bheed Ke Khatare",
        "year": 1998,
        "hook": "How to satirize economic liberalization through predatory clarity",
        "why_it_lands": "Parsai punctures neoliberal rhetoric by peeling away modern economic buzzwords to reveal raw commercial predation. The dry cadence captures the transition from sluggish state bureaucracy to unbridled market exploitation.",
        "tags": ["satire", "economic critique", "subcontinental realism"]
    },
    {
        "quote": "We will die a martyr’s death while fighting, as a real revolutionary, for the sake of our motherland, but we shall not surrender our weapons.",
        "author": "Bhagat Singh",
        "work": "Why I Am an Atheist",
        "year": 1930,
        "hook": "How to voice unconditional resolve before the gallows",
        "why_it_lands": "Written with unblinking moral clarity from Lahore Central Jail, Singh matches the biological finality of death with an absolute refusal of ideological surrender. The rhythmic balance between mortality and armed dignity creates an unforgettable manifesto cadence.",
        "tags": ["defiance", "manifesto craft", "moral courage"]
    },
    {
        "quote": "Neither you nor I, rather none of us, have suffered any pain so far. That part of our life has started only now.",
        "author": "Bhagat Singh",
        "work": "Why I Am an Atheist",
        "year": 1930,
        "hook": "How to define the threshold of true ordeal through ascending negation",
        "why_it_lands": "Bhagat Singh reframes past imprisonment as mere preamble, calmly preparing his comrades for execution. The ascending negation ('Neither you nor I, rather none of us') creates an intimate, unbreakable solidarity in the face of state violence.",
        "tags": ["stoicism", "voice", "solidarity"]
    }
]

def main():
    bank_path = "content/quote-bank.json"
    with open(bank_path, "r", encoding="utf-8") as f:
        bank = json.load(f)

    existing_quotes = {q["quote"].strip() for q in bank}
    added = 0

    for q in fresh_quotes:
        if q["quote"].strip() not in existing_quotes:
            bank.append(q)
            existing_quotes.add(q["quote"].strip())
            added += 1

    with open(bank_path, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)

    print(f"Added {added} fresh quotes to complete Cluster 43. Total in bank: {len(bank)}")

if __name__ == "__main__":
    main()
