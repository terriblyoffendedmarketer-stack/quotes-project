# scripts/curate_cluster_28.py — Curates 20 craft quotes from Cluster 28 (Systems, Dispossession & Ultimate Meaning)
# Usage: python3 scripts/curate_cluster_28.py
# Requires: json, os

import json
import os

QUOTE_BANK_PATH = "content/quote-bank.json"

VETTED_CLUSTER_28 = [
    # 1. Ursula K. Le Guin — The Dispossessed (1974)
    {
        "quote": "Nothing is yours. It is to use. It is to share. If you will not share it, you cannot use it.",
        "author": "Ursula K. Le Guin",
        "work": "The Dispossessed",
        "year": 1974,
        "translator": None,
        "hook": "How to deconstruct property relations through short declarative mandates.",
        "why_it_lands": "Le Guin pares political philosophy down to its barest syntactic bones, using four monosyllabic sentences to strip possession of moral legitimacy unless tethered to communal utility.",
        "tags": ["brevity", "philosophy", "politics", "clarity"]
    },
    {
        "quote": "In the end, the truth usually insists upon serving only the common good.",
        "author": "Ursula K. Le Guin",
        "work": "The Dispossessed",
        "year": 1974,
        "translator": None,
        "hook": "How to assert the objective moral weight of reality with quiet restraint.",
        "why_it_lands": "Le Guin personifies truth not as an aggressive weapon or ideological trophy, but as an inexorable gravitational current that ultimately bends toward collective survival.",
        "tags": ["philosophy", "insight", "truth", "clarity"]
    },
    {
        "quote": "Nothing he did was understood. In fact—it was not an uncommon phenomenon in his field—he had burnt out at twenty.",
        "author": "Ursula K. Le Guin",
        "work": "The Dispossessed",
        "year": 1974,
        "translator": None,
        "hook": "How to deflate intellectual prodigy with a dry parenthetical aside.",
        "why_it_lands": "Le Guin contrasts early intellectual genius against systemic indifference, using a flat, matter-of-fact parenthetical rupture to deflate the romantic myth of effortless brilliance.",
        "tags": ["irony", "pacing", "observation", "character"]
    },
    {
        "quote": "It was she who had withdrawn from him, and he had not tried to follow her. He had looked only at his own bitterness of heart, and never at her fear, or courage.",
        "author": "Ursula K. Le Guin",
        "work": "The Dispossessed",
        "year": 1974,
        "translator": None,
        "hook": "How to dissect emotional estrangement through reciprocal moral failure.",
        "why_it_lands": "Le Guin balances the anatomy of a severed bond across two clauses, exposing how self-pity and wounded ego blind an observer to the quiet bravery of the person walking away.",
        "tags": ["psychology", "relationship", "intimacy", "vulnerability"]
    },

    # 2. Mary Shelley — Frankenstein (1818)
    {
        "quote": "Leave them and you at peace; but if you refuse, I will glut the maw of death, until it be satiated with the blood of your remaining friends.",
        "author": "Mary Shelley",
        "work": "Frankenstein",
        "year": 1818,
        "translator": None,
        "hook": "How to weaponize gothic retribution through visceral personification.",
        "why_it_lands": "Shelley gives physical hunger to mortality itself ('glut the maw of death'), transforming vengeance from an abstract intention into a devouring physical appetite.",
        "tags": ["gothic", "imagery", "threat", "dialogue"]
    },
    {
        "quote": "Life, although it may only be an accumulation of anguish, is dear to me, and I will defend it.",
        "author": "Mary Shelley",
        "work": "Frankenstein",
        "year": 1818,
        "translator": None,
        "hook": "How to declare existential tenacity in the face of absolute despair.",
        "why_it_lands": "Shelley balances the catastrophic admission of suffering against primal survival instinct, asserting that life's intrinsic value survives even when all its circumstances are horrific.",
        "tags": ["existential", "resilience", "gothic", "perspective"]
    },
    {
        "quote": "I was hurried away by fury; revenge alone endowed me with strength and composure; it modelled my feelings, and allowed me to be calculating and calm, at periods when otherwise delirium or death would have been my portion.",
        "author": "Mary Shelley",
        "work": "Frankenstein",
        "year": 1818,
        "translator": None,
        "hook": "How to chart the stabilizing architecture of extreme obsession.",
        "why_it_lands": "Shelley reveals the perverse psychological paradox of vengeance: rather than producing madness, monomania can impose a cold, calculating discipline on a mind on the brink of collapse.",
        "tags": ["psychology", "obsession", "craft", "rhythm"]
    },
    {
        "quote": "I swear; and by thee, O Night, and by the spirits that preside over thee, I swear to pursue the dæmon, who caused this misery, until he or I shall perish in mortal conflict.",
        "author": "Mary Shelley",
        "work": "Frankenstein",
        "year": 1818,
        "translator": None,
        "hook": "How to elevate narrative climax into an invocational tragic oath.",
        "why_it_lands": "Shelley structures Victor's vow with archaic apostrophe and rhythmic repetitions of 'I swear', sealing the inexorable, fatalistic collision course between creator and creature.",
        "tags": ["tragedy", "voice", "gothic", "rhythm"]
    },

    # 3. Viktor E. Frankl — Man's Search for Meaning (1946)
    {
        "quote": "The privilege of actually smoking cigarettes was reserved for the Capo, who had his assured quota of weekly coupons; or possibly for a prisoner who worked as a foreman in a warehouse or workshop and received a few cigarettes in exchange for doing dangerous jobs. The only exceptions to this were those who had lost the will to live and wanted to 'enjoy' their last days.",
        "author": "Viktor E. Frankl",
        "work": "Man's Search for Meaning",
        "year": 1946,
        "translator": "Ilse Lasch",
        "hook": "How to decode symbolic objects into diagnostic markers of mortal surrender.",
        "why_it_lands": "Frankl transforms a trivial luxury—smoking a cigarette—into an unmistakable, terrifying behavioral indicator: the moment an inmate smoked their own cigarettes was the moment they had decided to die.",
        "tags": ["psychology", "symbolism", "observation", "historical"]
    },
    {
        "quote": "The engine's whistle had an uncanny sound, like a cry for help sent out in commiseration for the unhappy load which it was destined to lead into perdition.",
        "author": "Viktor E. Frankl",
        "work": "Man's Search for Meaning",
        "year": 1946,
        "translator": "Ilse Lasch",
        "hook": "How to infuse mechanical noise with ominous psychological dread.",
        "why_it_lands": "Frankl projects the collective terror of the doomed transport onto the machine itself, turning a shrill train whistle into a mourning wail across the tracks toward Auschwitz.",
        "tags": ["simile", "sound", "imagery", "dread"]
    },
    {
        "quote": "The corpse which had just been removed stared in at me with glazed eyes. If my lack of emotion had not surprised me from the standpoint of professional interest, I would not remember this incident now, because there was so little feeling involved in it.",
        "author": "Viktor E. Frankl",
        "work": "Man's Search for Meaning",
        "year": 1946,
        "translator": "Ilse Lasch",
        "hook": "How to clinically document psychic numbing during sustained atrocity.",
        "why_it_lands": "Frankl uses his training as a psychiatrist as a mirror to record his own desensitization, capturing how extreme horror eventually burns out the nervous system's capacity for shock.",
        "tags": ["psychology", "memoir", "restraint", "perspective"]
    },
    {
        "quote": "Love goes very far beyond the physical person of the beloved. It finds its deepest meaning in his spiritual being, his inner self.",
        "author": "Viktor E. Frankl",
        "work": "Man's Search for Meaning",
        "year": 1946,
        "translator": "Ilse Lasch",
        "hook": "How to transcend physical absence through interior communion.",
        "why_it_lands": "Frankl articulates how memory and love operate independent of physical proximity, offering an anchor of dignity that even total deprivation cannot dismantle.",
        "tags": ["philosophy", "love", "memory", "transcendence"]
    },

    # 4. Timothy Snyder — Bloodlands: Europe Between Hitler and Stalin (2010)
    {
        "quote": "‘Now we will live!’ This is what the hungry little boy liked to say, as he toddled along the quiet roadside, or through the empty fields. But the food that he saw was only in his imagination.",
        "author": "Timothy Snyder",
        "work": "Bloodlands: Europe Between Hitler and Stalin",
        "year": 2010,
        "translator": None,
        "hook": "How to convey famine's devastation through the heartbreaking optimism of a toddler.",
        "why_it_lands": "Snyder refrains from statistical rhetoric, letting the hallucinated feast of a dying child deliver the catastrophic human scale of the Ukrainian Holodomor.",
        "tags": ["pathos", "history", "restraint", "tragedy"]
    },
    {
        "quote": "‘They asked for my wedding ring, which I....’ The Polish officer broke off his diary just before he was executed by the Soviet secret police in 1940.",
        "author": "Timothy Snyder",
        "work": "Bloodlands: Europe Between Hitler and Stalin",
        "year": 2010,
        "translator": None,
        "hook": "How to let syntactic interruption mark the exact instant of slaughter.",
        "why_it_lands": "Snyder uses an unfinished archival sentence—trailing off at the demand for a wedding band—to let the sudden violent termination of a life speak louder than any narrative description.",
        "tags": ["history", "archive", "brevity", "tragedy"]
    },
    {
        "quote": "People were sentenced for the most apparently minor of offenses: ten years in the Gulag for owning a rosary, death for not producing enough sugar.",
        "author": "Timothy Snyder",
        "work": "Bloodlands: Europe Between Hitler and Stalin",
        "year": 2010,
        "translator": None,
        "hook": "How to expose totalitarian terror through disproportionate legal arithmetic.",
        "why_it_lands": "Snyder places sacred devotion and economic quotas side by side with their monstrous penal costs, exposing the grotesque mathematical arbitrariness of the Soviet purges.",
        "tags": ["irony", "history", "clarity", "contrast"]
    },
    {
        "quote": "Dina Pronicheva joined the perilous world of the few Jewish survivors in Kiev. The law required that Jews be turned in to the authorities. The Germans offered material incentives: money, and sometimes the keys to the Jew’s apartment.",
        "author": "Timothy Snyder",
        "work": "Bloodlands: Europe Between Hitler and Stalin",
        "year": 2010,
        "translator": None,
        "hook": "How to capture systemic complicity through casual transactional detail.",
        "why_it_lands": "Snyder exposes how genocidal machinery enlists ordinary neighbors not with grand ideology, but through the mundane, predatory allure of stolen domestic keys.",
        "tags": ["history", "chilling", "observation", "reality"]
    },

    # 5. Donella H. Meadows — Thinking in Systems: A Primer (2008)
    {
        "quote": "The development of the meanders in a river, the increasing complexity of the earth’s crust… are information-storing devices in the same manner that genetic systems are.",
        "author": "Donella H. Meadows",
        "work": "Thinking in Systems: A Primer",
        "year": 2008,
        "translator": None,
        "hook": "How to redefine physical terrain as dynamic information storage.",
        "why_it_lands": "Meadows collapses the boundary between geological landscape and biological data, demonstrating that bends in a river and tectonic strata encode procedural memory just like DNA.",
        "tags": ["metaphor", "science", "systems", "perspective"]
    },
    {
        "quote": "The information delivered by a feedback loop can only affect future behavior; it can’t deliver the information, and so can’t have an impact fast enough to correct behavior that drove the current feedback.",
        "author": "Donella H. Meadows",
        "work": "Thinking in Systems: A Primer",
        "year": 2008,
        "translator": None,
        "hook": "How to articulate systemic latency with rigorous structural logic.",
        "why_it_lands": "Meadows maps the inherent temporal tragedy of delayed feedback: by the time a system sounds the alarm, the momentum that caused the crisis is already irreversible history.",
        "tags": ["clarity", "systems", "time", "insight"]
    },
    {
        "quote": "The trouble is that the states created by interventions don’t last. The intoxication wears off. The subsidy is spent. The fertilizer is consumed or washed away.",
        "author": "Donella H. Meadows",
        "work": "Thinking in Systems: A Primer",
        "year": 2008,
        "translator": None,
        "hook": "How to demonstrate the fragility of artificial fixes through rhythmic staccato syntax.",
        "why_it_lands": "Meadows uses four terse, clipped sentences—moving from substance to money to soil—to illustrate how external subsidies vanish the moment active pumping stops.",
        "tags": ["rhythm", "brevity", "parallelism", "systems"]
    },
    {
        "quote": "Any new policy, especially if it’s effective, just pulls the system state farther from the goals of other actors and produces additional resistance, with a result that no one likes, but that everyone expends considerable effort in maintaining.",
        "author": "Donella H. Meadows",
        "work": "Thinking in Systems: A Primer",
        "year": 2008,
        "translator": None,
        "hook": "How to diagnose policy resistance and exhausted equilibria.",
        "why_it_lands": "Meadows lays bare the tragedy of institutional inertia: competing factions lock themselves into costly stalemates where tremendous energy is expended simply to preserve an outcome everyone hates.",
        "tags": ["systems", "society", "insight", "paradox"]
    }
]

def main():
    if not os.path.exists(QUOTE_BANK_PATH):
        print(f"Error: {QUOTE_BANK_PATH} not found.")
        return

    with open(QUOTE_BANK_PATH, "r", encoding="utf-8") as f:
        bank = json.load(f)

    existing_quotes = set(q["quote"].strip() for q in bank)
    added_count = 0

    for item in VETTED_CLUSTER_28:
        if item["quote"].strip() not in existing_quotes:
            bank.append(item)
            existing_quotes.add(item["quote"].strip())
            added_count += 1
        else:
            print(f"Duplicate found, skipping: {item['quote'][:40]}...")

    with open(QUOTE_BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)

    print(f"Successfully added {added_count} vetted quotes from Cluster 28.")
    print(f"New total quote bank size: {len(bank)}")

if __name__ == "__main__":
    main()
