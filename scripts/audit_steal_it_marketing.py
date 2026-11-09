# audit_steal_it_marketing.py — Audits stealIt and lookCloser sections in content/cards.json for marketing, business, or SaaS jargon
# Usage: python3 scripts/audit_steal_it_marketing.py
# Requires: json, pathlib

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARDS_FILE = ROOT / "content" / "cards.json"

# Expanded list of business, marketing, corporate, and SaaS terms
CORP_TERMS = [
    r"\bstrategy\b", r"\bstrategy doc\b", r"\bproduct\b", r"\bfeature\b", r"\blaunch\b",
    r"\blead\b", r"\bleads\b", r"\bfunnel\b", r"\bfunnels\b", r"\bcustomer\b", r"\bcustomers\b",
    r"\bclient\b", r"\bclients\b", r"\buser\b", r"\busers\b", r"\bchurn\b", r"\bonboarding\b",
    r"\blanding page\b", r"\bslack\b", r"\bpitch\b", r"\bdeck\b", r"\bpitch deck\b",
    r"\bmemo\b", r"\bexecutive\b", r"\bcorporate\b", r"\bbusiness\b", r"\bmarketing\b",
    r"\bbrand\b", r"\bbranding\b", r"\bsales\b", r"\bconversion\b", r"\bmetric\b", r"\bmetrics\b",
    r"\bpresentation\b", r"\bmeeting\b", r"\bemail\b", r"\bnewsletter\b", r"\bcta\b",
    r"\bcall to action\b", r"\bvalue prop\b", r"\bvalue proposition\b", r"\baudience\b",
    r"\bstakeholder\b", r"\bstakeholders\b", r"\broi\b", r"\bkpi\b", r"\bdeliverable\b",
    r"\breport\b", r"\bproposal\b", r"\bproject\b", r"\bcompany\b", r"\bstartup\b"
]

def audit():
    with open(CARDS_FILE, "r", encoding="utf-8") as f:
        cards = json.load(f)

    flagged = []
    print(f"Total cards audited: {len(cards)}\n")

    for i, card in enumerate(cards):
        cid = card.get("id", f"index-{i}")
        author = card.get("author", "Unknown")
        work = card.get("work", "Unknown")
        job = card.get("job", "")
        steal = card.get("stealIt", "")
        look = card.get("lookCloser", "")

        hits = []
        for term in CORP_TERMS:
            m_steal = re.findall(term, steal, re.IGNORECASE)
            m_look = re.findall(term, look, re.IGNORECASE)
            m_job = re.findall(term, job, re.IGNORECASE)
            if m_steal:
                hits.append(f"stealIt: '{m_steal[0]}'")
            if m_look:
                hits.append(f"lookCloser: '{m_look[0]}'")
            if m_job:
                hits.append(f"job: '{m_job[0]}'")

        if hits:
            flagged.append((cid, author, work, hits, job, steal))

    print(f"--- Flagged {len(flagged)} cards with corporate / marketing / business language ---\n")
    for cid, author, work, hits, job, steal in flagged:
        print(f"[{cid}] {author} — {work}")
        print(f"  Job: {job}")
        print(f"  Hits: {', '.join(hits)}")
        print(f"  Steal It: {steal}\n")

if __name__ == "__main__":
    audit()
