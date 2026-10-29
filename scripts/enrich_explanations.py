#!/usr/bin/env python3
# enrich_explanations.py — Enriches quote bank scene explanations with narrative meat
# Usage: python3 scripts/enrich_explanations.py [--batch-size N] [--max-quotes N]
# Requires: Python 3 standard library, local Ollama (optional)

import json
import urllib.request
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QB_PATH = ROOT / "content" / "quote-bank.json"
ASSET_PATH = ROOT / "android" / "app" / "src" / "main" / "assets" / "quote-bank.json"

# High-priority curated scene contexts with rich narrative meat
CURATED_EXPLANATIONS = {
    # Foundation — Isaac Asimov
    "A nuclear blaster is a good weapon, but it can point both ways.": (
        "In Foundation, Mayor Salvor Hardin faces down an aggressive warlord from Anacreon who threatens "
        "to annex the nascent Foundation by brute force. Hardin possesses neither armies nor starships, but he "
        "understands that weapons cannot run a civilization, and those who rule by intimidation inevitably invite "
        "their own downfall. The line cuts through martial posturing by asserting that true power lies in foresight and diplomacy."
    ),
    # The Invention of Solitude — Paul Auster
    "Things are inert: they have meaning only in function of the life that makes use of them.": (
        "While cleaning out his late father's empty house in New Jersey, Auster sifts through drawers of unworn clothes, "
        "unopened mail, and abandoned furniture. The objects remain completely intact and physically unchanged, yet the death "
        "of the person who used them empties them of purpose, leaving behind a quiet and uncanny absence. It captures how grief "
        "transforms ordinary domestic surroundings into monuments of loss."
    ),
    "It would be impossible to say that we are not haunted.": (
        "Confronting his father's sudden and silent demise, Auster reflects on how the dead linger in the minds of the living. "
        "The haunting is not supernatural or gothic; it is the stubborn, physical residue of memory and unasked questions. "
        "The line acknowledges that grief is not a phase you finish, but an ongoing dialogue with people who left before we truly knew them."
    ),
    "Life is death, and death is a kind of life.": (
        "Auster stares at old photographs of his father as a young man, realizing that mortality is not a distant event that "
        "happens at the end of life, but a shadow present from the very beginning. By refusing to soften the boundary between "
        "living and dying, the passage forces us to look squarely at human finitude without sentimental comfort."
    ),
    # Men Without Women — Haruki Murakami
    "Suddenly one day you become Men Without Women. That day comes to you completely out of the blue": (
        "In the title story, the narrator is woken in the middle of the night by a phone call delivering news of a former lover's "
        "suicide. The phrase 'Men Without Women' is not an intellectual classification, but an irreversible emotional continent "
        "you wake up stranded upon without warning. Murakami captures how true heartbreak does not arrive gradually, but splits "
        "your life into a before and an after in a single second."
    ),
    "There’s something inside her, something important, that I must have missed.": (
        "Looking back on years of shared intimacy, the narrator confronts the terrifying limitation of human understanding. "
        "Even when two people sleep in the same bed and exchange thousands of quiet words, the essential core of another human "
        "being remains hidden behind an invisible door. The passage exposes how familiarity can become a seductive substitute for actual perception."
    ),
    "Pain is inevitable. Suffering is optional.": (
        "Writing while training along the sweltering coastal roads of Lake Saroma, Murakami reflects on the physical breakdown "
        "that strikes every marathon runner past mile twenty. The body's exhaustion and the burning in the legs are stubborn facts "
        "of physics, but whether that fatigue turns into psychological defeat is a sovereign choice. It serves as a quiet manifesto "
        "for enduring long, unglamorous creative labor."
    ),
    # The Bell Jar — Sylvia Plath
    "I saw my life branching out before me like the green fig tree": (
        "Sitting in the fork of a fig tree, Esther Greenwood is paralyzed by the competing demands placed on young women: "
        "marriage, motherhood, poetry, scholarship, and travel. Choosing one branch means watching every other ripe fig wither "
        "and drop to the soil at her feet. Plath crystallizes the agonizing paralysis of youth, where every ambition demands "
        "the murder of another possibility."
    ),
    # Four Thousand Weeks — Oliver Burkeman
    "The problem with trying to make time for everything that matters": (
        "Burkeman attacks the central myth of the productivity industry: that with enough discipline and life-hacks, you will "
        "finally get on top of everything. Because our time on earth is brutally finite—roughly four thousand weeks—every meaningful "
        "commitment requires actively disappointing other possibilities. The line liberates the reader by turning defeat into peace: "
        "you will never do it all, and accepting that limit is where real life begins."
    ),
    # The Silk Roads — Peter Frankopan
    "It was, as one leading scholar has put it, a Versailles moment: too many ambitions, too few resources": (
        "Frankopan details how grand empires repeatedly overextend themselves during periods of rapid geographic conquest. "
        "Military victory often blinds rulers to the catastrophic logistical and economic costs required to maintain dominion. "
        "The passage demonstrates how imperial hubris consistently mistakes initial battlefield success for permanent stability."
    ),
    # Salt, Fat, Acid, Heat — Samin Nosrat
    "Imagine that you’re cooking green beans in a pot of water. If the water isn't salty enough": (
        "Nosrat demystifies culinary technique by shifting the focus from rigid recipe measurements to sensory physics. "
        "When vegetables are submerged in properly seasoned water, salt penetrates the cell walls and preserves both crisp texture "
        "and vibrant chlorophyll. It turns kitchen anxiety into intuitive confidence by explaining why food behaves the way it does."
    )
}

def clean_sentence_count(text):
    s = [x for x in re.split(r'[.!?]+', text) if x.strip()]
    return len(s)

def call_ollama_batch(batch):
    """Enrich a batch of quotes via local Ollama."""
    items_desc = []
    for i, q in enumerate(batch, 1):
        items_desc.append(
            f"{i}. Book: {q['work']} | Author: {q['author']}\n"
            f"Quote: '{q['quote']}'\n"
            f"Current explanation: '{q['explanation']}'"
        )
    
    prompt = f"""You are a thoughtful literary reading companion. Enrich the scene explanation for each of the following quotes.
For each quote:
- Write 2 to 3 sentences (50 to 80 words).
- Set the narrative scene/circumstance (who is speaking or what circumstance in the book prompted this).
- Explain the human/emotional/philosophical tension.
- Explain why the moment lands so effectively.
- Strictly NO preachy self-help or life advice, NO academic jargon ('litotes', 'chiasmus', 'synecdoche').
- Strictly NO formulaic openings like 'Captures the...' or 'Takes an abstract...'.

Quotes to enrich:
{chr(10).join(items_desc)}

Respond ONLY with valid JSON in this exact structure:
{{
""" + ",\n".join([f'  "{i}": "enriched text"' for i in range(1, len(batch) + 1)]) + "\n}"

    data = json.dumps({
        "model": "gemma3:4b",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }).encode("utf-8")

    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    
    with urllib.request.urlopen(req, timeout=60) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        raw = res.get("response", "{}")
        parsed = json.loads(raw)
        return parsed

def main():
    print(f"Loading quote bank from {QB_PATH}...")
    with open(QB_PATH, "r", encoding="utf-8") as f:
        bank = json.load(f)

    print(f"Loaded {len(bank)} quotes.")
    updated_count = 0

    # 1. Apply high-priority curated expansions
    for q in bank:
        q_text = q.get("quote", "")
        for target, enriched in CURATED_EXPLANATIONS.items():
            if target.lower() in q_text.lower():
                q["explanation"] = enriched
                updated_count += 1
                break

    print(f"Applied {updated_count} curated high-priority scene contexts.")

    # 2. Check for local Ollama and enrich rotating shelf quotes if requested
    use_ollama = "--with-ollama" in sys.argv
    if use_ollama:
        # Target the top 20 upcoming shelf quotes that have only 1 sentence
        candidates = []
        for i, q in enumerate(bank[:100]):
            exp = q.get("explanation", "").strip()
            word_count = len(exp.split())
            if word_count < 35 or clean_sentence_count(exp) <= 1:
                candidates.append((i, q))

        print(f"Found {len(candidates)} shelf candidates needing narrative enrichment.")
        batch_size = 3
        for b_idx in range(0, min(len(candidates), 15), batch_size):
            chunk = candidates[b_idx:b_idx+batch_size]
            print(f"Enriching batch {b_idx//batch_size + 1} with Ollama...")
            try:
                enriched_map = call_ollama_batch([item[1] for item in chunk])
                for idx_str, new_exp in enriched_map.items():
                    c_idx = int(idx_str) - 1
                    if 0 <= c_idx < len(chunk):
                        orig_idx = chunk[c_idx][0]
                        bank[orig_idx]["explanation"] = new_exp.strip()
                        updated_count += 1
            except Exception as e:
                print(f"Batch failed: {e}")

    # Save to quote-bank.json
    with open(QB_PATH, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)

    # Sync to Android assets
    if ASSET_PATH.exists():
        with open(ASSET_PATH, "w", encoding="utf-8") as f:
            json.dump(bank, f, indent=2, ensure_ascii=False)
        print(f"Synced {QB_PATH.name} to {ASSET_PATH}")

    # Rebuild prototype/index.html
    proto_builder = ROOT / "tools" / "build_prototype.py"
    if proto_builder.exists():
        import subprocess
        subprocess.run([sys.executable, str(proto_builder)], check=True)

    print(f"Successfully enriched quote bank! Total updates: {updated_count}")

if __name__ == "__main__":
    main()
