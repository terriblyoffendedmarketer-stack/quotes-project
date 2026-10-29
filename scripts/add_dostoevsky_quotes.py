#!/usr/bin/env python3
# add_dostoevsky_quotes.py — Updates the Crime & Punishment trifles quote and adds 3 iconic Dostoevsky shelf quotes
# Usage: python3 scripts/add_dostoevsky_quotes.py
# Requires: Python standard library

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QB_PATH = ROOT / "content" / "quote-bank.json"
ASSET_PATH = ROOT / "android" / "app" / "src" / "main" / "assets" / "quote-bank.json"

def main():
    print(f"Loading quote bank from {QB_PATH}...")
    with open(QB_PATH, "r", encoding="utf-8") as f:
        qb = json.load(f)

    # 1. Update the "Trifles" quote with Option B (including the Zimmerman hat)
    # and give the "trifles" kernel full philosophical weight in Tier 2
    updated_trifles = False
    for q in qb:
        if "Trifles, trifles are what matter" in q.get("quote", ""):
            q["quote"] = (
                "Nobody wears such a hat, it would be noticed a mile off, it would be remembered…. "
                "For this business one should be as little conspicuous as possible…. "
                "Trifles, trifles are what matter! Why, it’s just such trifles that always ruin everything…."
            )
            q["explanation"] = (
                "A destitute student in St. Petersburg has spent weeks constructing a grand theory that exceptional men are entitled to commit murder. "
                "Yet as he steps into the street to execute his plan, his confidence completely unravels over an absurd, oversized German hat that might catch a passerby’s eye.\n\n"
                "Dostoevsky homes in on the word ‘trifles’ because monumental human schemes are rarely defeated by grand moral epiphanies—they are undone by petty, humiliating minutiae. "
                "The criminal's true terror is not cosmic justice, but the uncontrollable trivia of the physical world: a creaking board, a stray thread, or a memorable hat."
            )
            q["tags"] = ["trifles", "paranoia", "irony", "vanity", "crime"]
            updated_trifles = True
            break

    print(f"Updated 'trifles' quote: {updated_trifles}")

    # 2. Add the 3 iconic Dostoevsky quotes
    new_quotes = [
        {
            "quote": "Pain and suffering are always inevitable for a large intelligence and a deep heart. The really great men must, I think, have great sadness on earth.",
            "author": "Fyodor Dostoevsky",
            "work": "Crime and Punishment",
            "year": 1866,
            "translator": "Constance Garnett",
            "explanation": (
                "In an essay on the psychology of law and transgression, Raskolnikov argues that extraordinary individuals—those who introduce new ideas to human civilization—inevitably endure profound inner torment.\n\n"
                "Dostoevsky strips intellectual brilliance of its romantic glamour. Deep consciousness is not a triumphant advantage; it expands your capacity to perceive suffering, binding mental acuity directly to melancholy."
            ),
            "tags": ["suffering", "intellect", "greatness", "melancholy", "dread"]
        },
        {
            "quote": "A whole moment of happiness! Is that too little, even for a whole human life?",
            "author": "Fyodor Dostoevsky",
            "work": "White Nights",
            "year": 1848,
            "translator": "Constance Garnett",
            "explanation": (
                "A lonely young dreamer wanders through the luminous midsummer twilight of St. Petersburg, experiencing four fleeting nights of deep connection with a young woman before she inevitably leaves him for another.\n\n"
                "Instead of succumbing to bitter resentment, the narrator chooses radical gratitude. Dostoevsky suggests that true joy is measured by its intensity rather than its duration: a single, unadulterated moment of communion can sustain a person across an entire lifetime of solitude."
            ),
            "tags": ["happiness", "solitude", "memory", "gratitude", "longing"]
        },
        {
            "quote": "The mystery of human existence lies not in just staying alive, but in finding something to live for.",
            "author": "Fyodor Dostoevsky",
            "work": "The Brothers Karamazov",
            "year": 1880,
            "translator": "Constance Garnett",
            "explanation": (
                "In the famous 'Grand Inquisitor' parable, an elderly church prelate confronts a silent Christ, arguing that ordinary humanity cannot bear the terrifying burden of moral freedom and would gladly trade it for bread.\n\n"
                "Dostoevsky cuts to the core of human restlessness: physical survival alone is never enough to satisfy the human soul. Without a devotion, a purpose, or a higher cause to anchor the conscience, people quickly find their own existence intolerable."
            ),
            "tags": ["purpose", "existentialism", "meaning", "human-nature", "stakes"]
        }
    ]

    added = 0
    for nq in new_quotes:
        if not any(nq["quote"].strip().lower() == q.get("quote", "").strip().lower() for q in qb):
            qb.append(nq)
            added += 1

    print(f"Added {added} new quotes. Total quote bank size: {len(qb)}")

    # Save to quote-bank.json
    with open(QB_PATH, "w", encoding="utf-8") as f:
        json.dump(qb, f, indent=2, ensure_ascii=False)

    # Sync to Android assets
    if ASSET_PATH.exists():
        with open(ASSET_PATH, "w", encoding="utf-8") as f:
            json.dump(qb, f, indent=2, ensure_ascii=False)
        print(f"Synced {QB_PATH.name} to {ASSET_PATH}")

    # Rebuild prototype/index.html
    proto_builder = ROOT / "tools" / "build_prototype.py"
    if proto_builder.exists():
        import subprocess
        subprocess.run(["python3", str(proto_builder)], check=True)

    print("Successfully completed Dostoevsky updates!")

if __name__ == "__main__":
    main()
