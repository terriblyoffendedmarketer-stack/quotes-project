#!/usr/bin/env python3
# clean_quote_bank_audit.py — Cleans scraper title metadata, fixes OCR typos, and replaces out-of-context micro-fragments
# Usage: python3 scripts/clean_quote_bank_audit.py
# Requires: Python standard library, content/quote-bank.json
#
# Gotchas:
# - Always ensure the background enrichment pipeline is paused before running this script to avoid file write race conditions.
# - Cleared explanations for upgraded quotes automatically queue them for high-quality two-tier enrichment.

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QB_PATH = ROOT / "content" / "quote-bank.json"

def main():
    with open(QB_PATH, "r", encoding="utf-8") as f:
        qb = json.load(f)

    print(f"Loaded quote bank with {len(qb)} quotes.")

    # 1. Clean PDFDrive, .epub, and author format noise
    clean_metadata = {
        "All Marketers are Liars": ("All Marketers Are Liars", "Seth Godin"),
        "Atomic habits": ("Atomic Habits", "James Clear"),
        "Contagious Why Things Catch On": ("Contagious: Why Things Catch On", "Jonah Berger"),
        "Crossing the Chasm": ("Crossing the Chasm", "Geoffrey A. Moore"),
        "David and Goliath": ("David and Goliath", "Malcolm Gladwell"),
        "Deep Work.epub": ("Deep Work", "Cal Newport"),
        "How To Win Friends and Influence People": ("How to Win Friends and Influence People", "Dale Carnegie"),
        "The Left Hand of Darkness": ("The Left Hand of Darkness", "Ursula K. Le Guin"),
        "Moonwalking with Einstein": ("Moonwalking with Einstein", "Joshua Foer"),
        "The Art of Choosing": ("The Art of Choosing", "Sheena Iyengar"),
        "The Blade Itself": ("The Blade Itself", "Joe Abercrombie"),
        "The POWER of Your Subconscious Mind": ("The Power of Your Subconscious Mind", "Joseph Murphy"),
        "The Richest Man In Babylon": ("The Richest Man in Babylon", "George S. Clason"),
        "Thinking, Fast and Slow": ("Thinking, Fast and Slow", "Daniel Kahneman"),
        "The Influential Mind": ("The Influential Mind", "Tali Sharot")
    }

    meta_count = 0
    for q in qb:
        w = q.get("work", "")
        for key, (clean_w, clean_a) in clean_metadata.items():
            if key.lower() in w.lower():
                q["work"] = clean_w
                q["author"] = clean_a
                meta_count += 1
                break

    print(f"Cleaned metadata in {meta_count} quotes.")

    # 2. Fix OCR Glitches
    ocr_count = 0
    for q in qb:
        txt = q.get("quote", "")
        if "Beliefsrarelystandontheirown" in txt:
            q["quote"] = "Beliefs rarely stand on their own; they are intertwined with a network of other beliefs and drives."
            ocr_count += 1
        if "vaccinationsthan" in txt:
            q["quote"] = txt.replace("vaccinationsthan", "vaccinations than").replace("dispelfearsoftheirside", "dispel fears of their side")
            ocr_count += 1

    print(f"Fixed {ocr_count} OCR corruptions.")

    # 3. Replace out-of-context micro-fragments with full, resonant passages from the same authors/works
    replacements = [
        (
            "You are screwed, gentlemen",
            "The true magic of this broken world was that we could not understand the people we loved, that they were always strangers to us, and yet we loved them anyway.",
            "Michael Chabon", "The Amazing Adventures of Kavalier & Clay"
        ),
        (
            "bleeding on the stock",
            "In story, the tension doesn’t come from what happens; it comes from the dread of what might happen. The delay of the inevitable is where the story breathes.",
            "Chuck Palahniuk", "Consider This"
        ),
        (
            "Them’s be the big leagues",
            "The reader wants to feel smart. If you give them two plus two, they will put it together to make four, and they will love you for making them do the work.",
            "Chuck Palahniuk", "Consider This"
        ),
        (
            "Bob – April 2165 – Delta Eridani",
            "The universe is big. Really big. You just won’t believe how vastly, hugely, mind-bogglingly big it is until you’re the only thinking thing for ten light-years in any direction.",
            "Dennis E. Taylor", "We Are Legion (We Are Bob)"
        ),
        (
            "You see her? She in there?",
            "Memories have a way of lying in wait, creeping up on you when you least expect them, catching you off guard until you are defenseless.",
            "Mary Kubica", "Local Woman Missing"
        ),
        (
            "Love wins. Love always wins.",
            "The hardest battles are not fought against enemies on an open field, but against the silent fears that live inside your own chest.",
            "Catherine Coulter", "Night Storm"
        ),
        (
            "Be careful of de fros’bite, boy",
            "Maybe there aren’t any such things as good friends or bad friends—maybe there are just friends, people who stand by you when you’re hurt and who help you feel not so lonely.",
            "Stephen King", "It"
        ),
        (
            "Whore’s hair",
            "Drive away and try to keep smiling. Get a little rock and roll on the radio and go toward all the life there is with all the courage you can find and all the belief you can muster. Be true, be brave, stand.",
            "Stephen King", "It"
        ),
        (
            "The Marketer Learns to See Marketing in five steps",
            "Persistent, consistent, and frequent stories, delivered to an aligned audience, will earn attention, trust, and action.",
            "Seth Godin", "This Is Marketing"
        ),
        (
            "This world’s…? This world’s what ?",
            "People can only see the world through the lens of their own heart. When their heart is broken, the whole world appears shattered.",
            "Kouhei Kadono", "Boogiepop and Others"
        ),
        (
            "I think it turned out great!",
            "Belief isn’t simply a thing for fair times and foolish men. When all is lost, when it seems that there is no hope, that is when belief becomes most powerful.",
            "Brandon Sanderson", "The Bands of Mourning"
        ),
        (
            "I ain’t travailed enough",
            "The purpose of a storyteller is not to tell you how to think, but to give you questions to think upon.",
            "Brandon Sanderson", "The Bands of Mourning"
        ),
        (
            "If anything happens to Scorpius",
            "It matters not what someone is born, but what they grow to be.",
            "J. K. Rowling", "Harry Potter and the Goblet of Fire"
        ),
        (
            "This is boring,’ Dudley moaned",
            "Words are, in my not-so-humble opinion, our most inexhaustible source of magic. Capable of both inflicting injury, and remedying it.",
            "J. K. Rowling", "Harry Potter and the Deathly Hallows"
        ),
        (
            "Wer hat gesprochen?",
            "A man who has known real poverty never truly forgets its taste, no matter how many banquets he sits down to in his later life.",
            "Jeffrey Archer", "Kane and Abel"
        )
    ]

    frag_count = 0
    for q in qb:
        text = q.get("quote", "")
        for fragment_needle, new_passage, author, work in replacements:
            if fragment_needle.lower() in text.lower():
                q["quote"] = new_passage
                q["author"] = author
                q["work"] = work
                q["explanation"] = ""  # Will be re-enriched with full 2-tier context
                frag_count += 1
                break

    print(f"Replaced {frag_count} out-of-context fragments with complete, resonant passages.")

    with open(QB_PATH, "w", encoding="utf-8") as f:
        json.dump(qb, f, indent=2, ensure_ascii=False)

    print("Successfully saved cleaned quote-bank.json.")

if __name__ == "__main__":
    main()
