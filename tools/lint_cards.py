"""Flag AI-sounding patterns in the explanation slides of content/cards.json.

This can't judge whether a card is good. It catches the mechanical tells so the
human and critic passes can spend their attention on taste.

Usage: python3 lint_cards.py [card-id ...]
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ("lookCloser", "aroundIt", "stealIt")
LIMITS = {"lookCloser": 80, "aroundIt": 100, "stealIt": 60}

BANNED_WORDS = [
    "genius", "masterful", "masterclass", "stunning", "haunting", "powerful",
    "quietly", "deceptively", "effortlessly", "testament", "tapestry", "delve",
    "nuanced", "profound", "poignant", "resonates", "evocative", "elevate",
    "captures the essence", "speaks volumes", "a must-read", "you should read",
    "worth reading", "pick up the book", "here's the thing", "the beauty of",
    "the magic of", "what makes this", "in other words", "ultimately",
    "at its core", "it's worth noting", "notice how", "the result is",
]

PATTERNS = {
    "not X, but/it's Y": r"\bnot (?:just |only |merely )?[^.;:]{1,50}[,;] (?:but|it's|it is|they're|he's|she's)\b",
    "isn't X. It's Y": r"\b(?:isn't|is not|wasn't|aren't|doesn't|don't|didn't|never)\b[^.]{1,70}\.\s+(?:It|He|She|They|This|That)(?:'s| is| was| does| did)?\b",
    "isn't about X": r"\bisn't (?:really )?about\b",
    "colon reveal": r"\w:\s+[a-z]",
    "em dash": r"—",
    "summing-up closer": r"(?:^|\.\s+)(?:That's|This is|And that's|That is) (?:how|why|what|the)\b[^.]*\.\s*$",
    "rhetorical question": r"\?",
    "possible triad": r"\b\w+, \w+(?: \w+)?,? and \w+\b",
    "and that's how/why": r"\band that's (?:how|why|where|what)\b",
    "teacherly aside": r"\b(?:Hold on to that|Keep that in mind|Remember that|Here's where)\b",
    "knowing nod": r"\b(?:Anyone who has|We've all|You know the feeling|knows the feeling)\b",
}

IMPERATIVE_OPENERS = {"read", "say", "listen", "watch", "look", "notice", "count", "check", "see", "take", "try"}


def strip_quotes(text):
    """Drop quoted material so we only judge our own sentences."""
    return re.sub(r"“[^”]*”|\"[^\"]*\"", "“…”", text)


def first_words(text, n=3):
    return " ".join(re.findall(r"[A-Za-z']+", text)[:n]).lower()


def lint(cards):
    problems = defaultdict(list)
    openers = defaultdict(Counter)
    grams = Counter()
    gram_cards = defaultdict(set)

    for card in cards:
        for field in FIELDS:
            raw = card.get(field) or ""
            own = strip_quotes(raw)
            words = len(raw.split())
            if words > LIMITS[field]:
                problems[card["id"]].append(f"{field}: {words} words (limit {LIMITS[field]})")
            low = own.lower()
            for w in BANNED_WORDS:
                if w in low:
                    problems[card["id"]].append(f"{field}: banned phrase “{w}”")
            for name, rx in PATTERNS.items():
                if name in card.get("lintAccepted", []):
                    continue
                for m in re.finditer(rx, own):
                    problems[card["id"]].append(f"{field}: {name} → “{m.group(0).strip()[:70]}”")
            openers[field][first_words(own)] += 1
            toks = re.findall(r"[a-z']+", low)
            for i in range(len(toks) - 3):
                g = " ".join(toks[i:i + 4])
                gram_cards[g].add(card["id"])

    corpus = []
    imperative = [c["id"] for c in cards if first_words(strip_quotes(c.get("lookCloser") or ""), 1) in IMPERATIVE_OPENERS]
    if len(cards) >= 4 and len(imperative) > len(cards) / 3:
        corpus.append(f"{len(imperative)} of {len(cards)} cards open lookCloser with an instruction (Read/Say/Listen/Watch…). Vary the way in.")
    for field, counts in openers.items():
        allowed = max(2, len(cards) // 20)
        for opener, n in counts.items():
            if n > allowed and opener:
                corpus.append(f"{n} cards open {field} with “{opener}…”")
    for g, ids in gram_cards.items():
        if len(ids) >= max(3, len(cards) // 15):
            corpus.append(f"phrase “{g}” appears in {len(ids)} cards")
    return problems, corpus


def main():
    cards = json.loads((ROOT / "content" / "cards.json").read_text())
    if len(sys.argv) > 1:
        cards = [c for c in cards if c["id"] in sys.argv[1:]]
    problems, corpus = lint(cards)
    total = 0
    for card in cards:
        items = problems.get(card["id"], [])
        total += len(items)
        print(f"{'✗' if items else '✓'} {card['id']}")
        for item in items:
            print(f"    {item}")
    if corpus:
        print("\nAcross the set:")
        for item in corpus:
            print(f"    {item}")
    print(f"\n{total} card-level flags, {len(corpus)} set-level flags")


if __name__ == "__main__":
    main()
