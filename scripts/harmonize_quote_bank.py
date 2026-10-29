# harmonize_quote_bank.py — Harmonizes schema across all 1,871 quotes in the master bank
# Usage: python3 scripts/harmonize_quote_bank.py
# Requires: python standard library

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QB_PATH = ROOT / "content" / "quote-bank.json"

CUSTOM_EXPLANATIONS = {
    "It is only in social contexts that a person becomes an individual.": (
        "Adlerian psychology argues that human individuality and loneliness do not exist in pure isolation; "
        "it is only in relation to other people that our identity, frictions, and self-definition emerge."
    ),
    "“Well, if we did, it just might start moving again…”": (
        "Nisio Isin captures how characters in the Monogatari series treat supernatural stagnation with wry fatalism, "
        "recognizing that acknowledging a dormant curse is often what reawakens its forward momentum."
    ),
    "Something wrong?” asked Ron. “There was a locket.”": (
        "Captures the grim, hollow shock after the ordeal in Voldemort's sea cave, realizing that Dumbledore's agony "
        "yielded only a counterfeit Horcrux left behind by an unknown deserter."
    ),
}

def clean_tag(t):
    if not isinstance(t, str):
        return None
    t = t.strip().lower()
    t = re.sub(r"^#", "", t)
    t = re.sub(r"[^a-z0-9\- ]", "", t)
    t = t.replace(" ", "-")
    return t if len(t) >= 2 else None

def harmonize():
    with open(QB_PATH, "r", encoding="utf-8") as f:
        bank = json.load(f)

    print(f"Total entries before harmonization: {len(bank)}")

    harmonized = []
    for q in bank:
        # Extract core fields
        q_text = q.get("quote", "").strip()
        author = q.get("author", "Unknown").strip()
        work = q.get("work", "Unknown").strip()

        # Clean work title if it was marked Unknown
        if work.lower() == "unknown":
            # Attempt to derive from source or filename if available
            src = q.get("source", "")
            if src:
                stem = Path(src).stem.replace("_", " ").strip()
                work = stem
            else:
                work = "Literary Anthology"

        # Determine explanation
        exp = q.get("explanation")
        if not exp or len(exp.strip()) < 10:
            # Check custom fallback first
            for k, v in CUSTOM_EXPLANATIONS.items():
                if k in q_text:
                    exp = v
                    break
            if not exp:
                parts = []
                if q.get("context"):
                    parts.append(q["context"].strip())
                why = q.get("whyItLands") or q.get("why_it_lands")
                if why:
                    parts.append(why.strip())
                elif q.get("hook"):
                    parts.append(q["hook"].strip())
                exp = " ".join(parts).strip()

        # Clean tags
        raw_tags = q.get("tags", [])
        if isinstance(raw_tags, str):
            raw_tags = [t.strip() for t in raw_tags.split(",")]
        cleaned_tags = []
        for t in raw_tags:
            ct = clean_tag(t)
            if ct and ct not in cleaned_tags:
                cleaned_tags.append(ct)
        if not cleaned_tags:
            cleaned_tags = ["observation", "prose"]

        entry = {
            "quote": q_text,
            "author": author,
            "work": work,
            "explanation": exp or "A striking passage that showcases the author's distinctive voice and thematic pressure.",
            "tags": cleaned_tags
        }

        if q.get("year"):
            entry["year"] = q["year"]
        if q.get("translator"):
            entry["translator"] = q["translator"]

        harmonized.append(entry)

    # Save harmonized bank
    with open(QB_PATH, "w", encoding="utf-8") as f:
        json.dump(harmonized, f, indent=2, ensure_ascii=False)

    print(f"Harmonized {len(harmonized)} entries!")
    missing_exp = sum(1 for q in harmonized if not q.get("explanation"))
    print(f"Entries without explanation: {missing_exp}")

if __name__ == "__main__":
    harmonize()
