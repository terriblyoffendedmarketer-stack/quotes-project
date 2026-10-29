# curate_cluster_48.py — Appends 20 curated quotes from Cluster 48 into quote-bank.json with context and takeaway
# Usage: python3 scripts/curate_cluster_48.py
# Requires: content/quote-bank.json

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QB_PATH = ROOT / "content" / "quote-bank.json"

NEW_QUOTES = [
  # Stephen King — Pet Sematary (1983)
  {
    "quote": "‘There were better than a hundred graves up in the Pet Sematary, I’d say.’",
    "author": "Stephen King",
    "work": "Pet Sematary",
    "year": 1983,
    "hook": "How to introduce a cursed threshold through countrified arithmetic",
    "why_it_lands": "King introduces an ancient, terrifying landscape through the folksy, casual estimating of an elderly neighbor, deflecting supernatural horror into mundane rural upkeep.",
    "context": "Louis Creed is guided up into the dense Maine woods behind his new house by his neighbor Jud Crandall, who walks him past generations of crude grave markers built by children.",
    "takeaway": "Communities often normalize their oldest tragedies into quaint local folklore; pay attention to what taboos a culture teaches you to view as harmless scenery.",
    "tags": ["dialogue", "folklore", "understatement"]
  },
  {
    "quote": "Your destruction and the destruction of all you love is very near, Doctor.",
    "author": "Stephen King",
    "work": "Pet Sematary",
    "year": 1983,
    "hook": "How to deliver an apocalyptic prophecy through clinical detachment",
    "why_it_lands": "The chilling power comes from the total absence of dramatic theatricality; delivered by a dying stranger with medical calm, the sentence feels like an immutable diagnosis.",
    "context": "A student jogger brought into the university infirmary after a horrific hit-and-run speaks directly to Dr. Louis Creed in his dying moments, addressing him by name before brain death occurs.",
    "takeaway": "The most consequential warnings in life rarely arrive with sirens and theatrics; they often sound quiet, direct, and unnervingly matter-of-fact.",
    "tags": ["prophecy", "horror", "brevity"]
  },
  {
    "quote": "‘There’s a lot of funny things down this way, Louis. The air’s heavier . . . more electrical . . . or somethin.’",
    "author": "Stephen King",
    "work": "Pet Sematary",
    "year": 1983,
    "hook": "How to register atmospheric wrongness through colloquial imprecision",
    "why_it_lands": "King captures how ordinary rural speech struggles to articulate the supernatural, using domestic descriptors ('heavier', 'electrical') to evoke an alien electromagnetic pressure.",
    "context": "Jud Crandall attempts to explain the magnetic, corrupting pull of the ancient Micmac burial ground beyond the deadfall without admitting to the madness it provokes.",
    "takeaway": "When your gut senses that an environment is toxic, the body registers discomfort through vague physiological tension long before the intellect can explain why.",
    "tags": ["atmosphere", "voice", "uncanny"]
  },
  {
    "quote": "‘It was like washing a piece of meat.’",
    "author": "Stephen King",
    "work": "Pet Sematary",
    "year": 1983,
    "hook": "How to evoke the uncanny through domestic tactile revulsion",
    "why_it_lands": "A shockingly flat, butcher-shop simile that strips resurrection of all religious wonder, reducing an undead pet to inert, animate flesh devoid of soul.",
    "context": "Jud recounts what it felt like bathing a dog that had returned from the burial ground—moving and breathing, but fundamentally dead inside.",
    "takeaway": "Visceral revulsion is nature's alarm system when an imitation mimics the surface of life while lacking the fundamental spirit that made it precious.",
    "tags": ["simile", "grotesque", "visceral detail"]
  },

  # Stephen King — The Mist (1980)
  {
    "quote": "The telephone gave out a startled ting! and I turned to see my wife and son standing directly in front of the big picture window... That was the last call that came into the house.",
    "author": "Stephen King",
    "work": "The Mist",
    "year": 1980,
    "hook": "How to mark the severance of civilization with a domestic sound effect",
    "why_it_lands": "King punctuates the end of ordinary technological security with a single, fragile acoustic onomatopoeia ('a startled ting!'), immediately following it with permanent severance.",
    "context": "As an unnatural bank of fog begins rolling across Long Lake after a violent summer storm, the family telephone gives one abbreviated chime before going permanently dead.",
    "takeaway": "Modern civilization’s safety nets don't collapse with an explosion; they vanish silently when ordinary utilities simply stop responding.",
    "tags": ["sound", "foreshadowing", "domestic"]
  },
  {
    "quote": "‘It’s the brightness of the sun,’ I said. ‘It’s the same way clouds look from an airplane when you fly over them.’",
    "author": "Stephen King",
    "work": "The Mist",
    "year": 1980,
    "hook": "How to construct denial through rational scientific explanation",
    "why_it_lands": "King demonstrates how characters cling to mundane scientific analogies to ward off unthinkable terror, comforting themselves with logic even as their eyes witness the impossible.",
    "context": "Trapped inside a local supermarket with his son, David Drayton attempts to calm frightened shoppers by offering pseudo-meteorological explanations for the advancing white wall.",
    "takeaway": "In an emerging crisis, people instinctively invent comforting, familiar explanations to avoid acknowledging an unprecedented danger.",
    "tags": ["dialogue", "denial", "psychology"]
  },
  {
    "quote": "‘Plate glass,’ Myron LaFleur whispered. ‘Jesus Christ in a chariot-driven sidecar.’",
    "author": "Stephen King",
    "work": "The Mist",
    "year": 1980,
    "hook": "How to reveal structural fragility through a sudden architectural realization",
    "why_it_lands": "King pairs a cold architectural term ('plate glass') with a colorful regional swear, instantly flipping the supermarket from a place of refuge to a brittle glass cage.",
    "context": "The townspeople sheltering in the grocery store suddenly realize that the entire front wall separating them from the horrors in the fog is made of standard display glass.",
    "takeaway": "People frequently confuse familiar commercial convenience with genuine physical security until a crisis reveals how fragile their walls really are.",
    "tags": ["humor", "suspense", "realization"]
  },
  {
    "quote": "‘That bad, huh?’ he said. ‘That bad,’ Ollie agreed, and worked his beer.",
    "author": "Stephen King",
    "work": "The Mist",
    "year": 1980,
    "hook": "How to register catastrophe through small-town monosyllabic understatement",
    "why_it_lands": "Rather than screaming or panicking, the blue-collar characters compress unfathomable dread into three identical words, anchored by the casual, repetitive gesture of drinking a beer.",
    "context": "Ollie Weeks, the quiet supermarket assistant manager, confirms to another shopper that whatever is killing people outside the loading dock door is beyond human control.",
    "takeaway": "When disaster exceeds the mind's ability to process it, human beings often retreat into familiar small gestures and blunt understatement to keep their hands steady.",
    "tags": ["understatement", "dialogue", "stoicism"]
  },

  # Joe Abercrombie — The Last Argument of Kings (2008)
  {
    "quote": "‘You can never have too many knives,’ his father had told him, often enough, ‘unless you’re trying to swim.’",
    "author": "Joe Abercrombie",
    "work": "The Last Argument of Kings",
    "year": 2008,
    "hook": "How to anchor survivalist paranoia in a humorous parenthetic limit",
    "why_it_lands": "Abercrombie undercuts a grim barbarian combat maxim with a pragmatic domestic exception, defining a character's entire hyper-vigilant psychology in a single sentence.",
    "context": "Logen Ninefingers straps hidden blades into every fold of his northern armor before entering the treacherous, deceptive royal court of Adua.",
    "takeaway": "Over-preparation is an asset in combat, but carrying too much armor into fluid situations will drag you straight to the bottom.",
    "tags": ["voice", "paranoia", "humor"]
  },
  {
    "quote": "‘It is only natural that you made commitments, but your past life is gone, and your commitments have gone with it. You are a king, now, and your people demand that you behave like one.’",
    "author": "Joe Abercrombie",
    "work": "The Last Argument of Kings",
    "year": 2008,
    "hook": "How to strip personal loyalty in the name of sovereign necessity",
    "why_it_lands": "Abercrombie dramatizes the cold arithmetic of statecraft: personal honor and past friendships must be discarded once institutional authority takes hold.",
    "context": "Superior Glokta and the Arch Lector coldly inform the newly crowned northern ruler that his private promises to his war-band are void under imperial politics.",
    "takeaway": "Ascending to higher institutional leadership often requires ruthlessly shedding personal alliances that conflict with collective responsibility.",
    "tags": ["power", "statecraft", "duty"]
  },
  {
    "quote": "‘Crowns. Kings. The whole notion’s shit, and me the worst choice there could be.’",
    "author": "Joe Abercrombie",
    "work": "The Last Argument of Kings",
    "year": 2008,
    "hook": "How to deflate royal elevation with visceral northern profanity",
    "why_it_lands": "A blunt, staccato triplet ('Crowns. Kings. The whole notion’s shit') that rejects all epic fantasy glorification of hereditary majesty.",
    "context": "The Bloody-Nine, a scarred warrior who has spent his life wading through mud and blood, stares at the northern crown thrust upon him by cynical wizards.",
    "takeaway": "The most dangerous leaders are those who believe they were born to rule; genuine wisdom often begins with horror at your own inadequacy.",
    "tags": ["cynicism", "leadership", "profanity"]
  },
  {
    "quote": "‘Sometimes mercy buys you more than ruthlessness.’",
    "author": "Joe Abercrombie",
    "work": "The Last Argument of Kings",
    "year": 2008,
    "hook": "How to reframe compassion as a pragmatic transaction",
    "why_it_lands": "Abercrombie strips moral piety from mercy by phrasing it with commercial verb choice ('buys you'), turning clemency into calculated strategic leverage.",
    "context": "Inquisitor Glokta, a crippled torturer whose entire worldview is built on inflicting pain, realizes that sparing a dangerous enemy creates a debt far more useful than an execution.",
    "takeaway": "Mercy is not just a moral virtue; in tough negotiations, giving an adversary a face-saving exit yields far more cooperation than cornering them into a fight.",
    "tags": ["strategy", "morality", "leverage"]
  },

  # Uketsu — Strange Pictures (2022)
  {
    "quote": "‘It’s weird, right? It has none of the finesse of the others. And it was drawn on the back of a receipt.’",
    "author": "Uketsu",
    "work": "Strange Pictures",
    "year": 2022,
    "translator": "Louise Heal Kawai",
    "hook": "How to identify a dying message through material degradation",
    "why_it_lands": "Uketsu builds suspense not through dramatic monologues, but through subtle material clues: the abrupt drop in artistic technique and the shift from clean paper to scrap.",
    "context": "An internet sleuth and an art student analyze a series of intricate drawings posted on a blogger's website, noticing the final sketch was drawn in frantic panic.",
    "takeaway": "Sudden changes in medium and care reveal emergency; when someone's communicative style abruptly deteriorates, look for the duress behind the tool.",
    "tags": ["mystery", "observation", "materiality"]
  },
  {
    "quote": "‘His death is a shock, but honestly, I’m not sad about it at all.’",
    "author": "Uketsu",
    "work": "Strange Pictures",
    "year": 2022,
    "translator": "Louise Heal Kawai",
    "hook": "How to sever grief from etiquette with blunt dispassion",
    "why_it_lands": "A chillingly honest confession that strips away performative mourning, distinguishing between the intellectual surprise of mortality and actual emotional sorrow.",
    "context": "A witness being interviewed regarding an unexplained death refuses to feign sorrow for an abusive relative, speaking with disconcerting directness.",
    "takeaway": "Shock is an involuntary cognitive reaction to sudden change, while grief is an emotional response to love; people frequently conflate the two out of politeness.",
    "tags": ["psychology", "honesty", "dialogue"]
  },
  {
    "quote": "‘If they could have drawn the mountains even in the dark of the night, then they might not have been murdered after dawn.’",
    "author": "Uketsu",
    "work": "Strange Pictures",
    "year": 2022,
    "translator": "Louise Heal Kawai",
    "hook": "How to link artistic spatial memory to mortal survival",
    "why_it_lands": "Uketsu reframes a landscape drawing from a leisurely aesthetic exercise into a high-stakes, failed navigational escape plan.",
    "context": "The investigator realizes that a victim’s final mountain horizon sketch was not drawn for fun, but as a desperate attempt to record a fatal secret before morning.",
    "takeaway": "In high-stakes mysteries, what looks like decorative self-expression is often a coded signal of functional survival.",
    "tags": ["suspense", "puzzle", "deduction"]
  },
  {
    "quote": "‘I used to practise drawing from memory... I’d stare at it for ten seconds and memorize the shape. I did that over and over, and now it’s one of my biggest assets. I can perfectly recreate any scene after seeing it once.’",
    "author": "Uketsu",
    "work": "Strange Pictures",
    "year": 2022,
    "translator": "Louise Heal Kawai",
    "hook": "How to build sensory eidetic recall through repetitive childhood discipline",
    "why_it_lands": "Uketsu grounds an investigative superpower in believable, obsessive childhood training rather than mystical intuition, making the deduction feel earned.",
    "context": "An architecture student explains to the narrator how he is able to spot minute structural inconsistencies in hand-drawn floor plans that police detectives missed.",
    "takeaway": "Mastery in pattern recognition isn't born of genius; it is forged through thousands of hours of quiet, repetitive observation that hardens into instinct.",
    "tags": ["skill", "observation", "memory"]
  },

  # Andy Weir — Project Hail Mary (2021)
  {
    "quote": "‘The universe is a strange and beautiful place. It’s also incredibly hostile, and I was about to become part of it.’",
    "author": "Andy Weir",
    "work": "Project Hail Mary",
    "year": 2021,
    "hook": "How to balance cosmic awe against biological fragility",
    "why_it_lands": "Weir pairs lyrical wonder ('strange and beautiful') directly against cold mortal peril ('incredibly hostile'), using a simple transition to place the narrator inside the vacuum.",
    "context": "Ryland Grace, waking up with amnesia aboard an interstellar vessel, looks out the viewport and remembers that Earth’s sun is dying from a microbial infestation.",
    "takeaway": "Wonder and danger are inseparable in genuine exploration; stepping into the unknown requires holding awe in one hand and survival vigilance in the other.",
    "tags": ["sci-fi", "perspective", "wonder"]
  },
  {
    "quote": "‘That’s not what I meant,’ Voigt said. ‘There are processes and background checks to—’ Stratt put her hand on my shoulder. ‘Dr. Ryland Grace, I hereby grant you top-secret clearance to all information pertaining to Project Hail Mary.’",
    "author": "Andy Weir",
    "work": "Project Hail Mary",
    "year": 2021,
    "hook": "How to bypass bureaucratic inertia with absolute executive authority",
    "why_it_lands": "Weir dramatizes the sudden evaporation of peacetime protocol during an existential emergency, cutting through red tape with a single flat declaration.",
    "context": "A middle-school science teacher brought in as a minor biology consultant is instantly elevated by Eva Stratt, who holds unilateral UN authority to save human civilization.",
    "takeaway": "In an existential crisis, bureaucratic protocol is a lethal liability; decisive leadership cuts through red tape to put competence where it is needed.",
    "tags": ["leadership", "authority", "dialogue"]
  },
  {
    "quote": "‘Astrophage has a predator! If we find a predator…we take it home!’",
    "author": "Andy Weir",
    "work": "Project Hail Mary",
    "year": 2021,
    "hook": "How to ignite scientific breakthrough with an ecological parallel",
    "why_it_lands": "Weir captures the electric adrenaline of discovery by reducing a galaxy-scale astrophysical catastrophe to a simple biological truth: every organism has something that eats it.",
    "context": "Desperately seeking why the star Tau Ceti is immune to the energy-draining microorganisms devouring the Sun, Grace realizes the solar infection is subject to natural selection.",
    "takeaway": "Every runaway system in nature or organizations eventually breeds its own counter-force; when tackling an uncontrollable crisis, look for the natural predator that keeps it in check.",
    "tags": ["science", "breakthrough", "discovery"]
  },
  {
    "quote": "‘It must be your decision,’ said Stratt. ‘I will not have someone on my crew who is there against their will. You must come of your own volition.’",
    "author": "Andy Weir",
    "work": "Project Hail Mary",
    "year": 2021,
    "hook": "How to enforce voluntary consent under total coercion",
    "why_it_lands": "A chilling paradox of leadership: Stratt possesses the legal authority to force compliance, but recognizes that deep-space isolation will break anyone who didn't choose the burden.",
    "context": "Stratt demands that a scientist voluntarily agree to embark on a one-way suicide mission to save the species, refusing to deploy a conscript on a cosmic Hail Mary.",
    "takeaway": "You can compel physical presence through force, but long-range endurance and sacrifice require voluntary inner alignment.",
    "tags": ["choice", "sacrifice", "leadership"]
  }
]

def main():
    with open(QB_PATH, "r", encoding="utf-8") as f:
        bank = json.load(f)

    existing_quotes = set(q["quote"].strip() for q in bank)
    added = 0
    for q in NEW_QUOTES:
        if q["quote"].strip() not in existing_quotes:
            bank.append(q)
            existing_quotes.add(q["quote"].strip())
            added += 1

    with open(QB_PATH, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)

    print(f"Added {added} new quotes with context and takeaway. Total bank size now: {len(bank)}")

if __name__ == "__main__":
    main()
