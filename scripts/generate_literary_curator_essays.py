#!/usr/bin/env python3
# scripts/generate_literary_curator_essays.py — Converts all 'why_love' entries into cohesive, passionate, book-nerd editorial notes
# Usage: python3 scripts/generate_literary_curator_essays.py

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "bookshelf" / "data.json"

# Bespoke, high-voltage book-nerd editorials for key works
NERD_EDITORIALS = {
    "art-of-dramatic-writing-the-lajos-egri": (
        "Lajos Egri wrote this in 1942, and eighty years later it remains the most ruthless reality check in dramatic literature. "
        "Before Blake Snyder gave us beat sheets and Robert McKee gave us principles, Egri gave us the unyielding law of Premise: "
        "if you don't know what truth your story is fighting to prove—not in your head, but through character action—you have nothing but noise. "
        "He dissects Molière, Shakespeare, and Ibsen not as museum relics, but as prize fighters who knew that dialectical character conflict "
        "is the only engine that keeps human beings glued to their seats. You read this to purge self-indulgent meandering from your work forever."
    ),
    "cinematography-theory-and-practice-unknown": (
        "Blain Brown's masterwork is the secret handbook of people who understand that cinema is a language written in photons rather than words. "
        "Most cinematography manuals get lost in optical sensor specs and lens charts; Brown treats the camera as an emotional weapon. "
        "He breaks down visual subtext, color palettes, and lighting continuity with the precision of a seasoned DP who has stood on freezing sets "
        "at 4 AM waiting for magic hour. On this shelf because it bridges the gap between raw optical physics and poetic visual psychology."
    ),
    "directing-actors-unknown": (
        "Judith Weston is the quiet titan behind two generations of indie film miracles. "
        "Her core revelation sounds deceptively simple—never direct results, direct verbs and objectives—but watching directors fail "
        "because they tell actors to 'be sadder' or 'sound angrier' proves how rare true directorial empathy is. "
        "This book belongs in any serious storyteller's collection because it forces you to understand human defense mechanisms: "
        "why people say the exact opposite of what they desire, and how true emotion only surfaces when characters hit concrete walls."
    ),
    "into-the-woods-john-yorke": (
        "John Yorke ran Channel 4 drama and BBC independent production, but this book is his magnum opus: a brilliant, obsessive dissection "
        "of why human brains across every civilization are chemically addicted to the five-act story shape. "
        "Yorke isn't peddling formulaic Hollywood screenwriting hacks; he unites Aristotle, Vladimir Propp, Shakespeare, and neurological science "
        "to prove that entering the dark woods of crisis and returning transformed is our primary cognitive survival mechanism. "
        "It is essential reading because it treats narrative not as cheap entertainment, but as the mental scaffolding that keeps sanity intact."
    ),
    "john-truby-the-anatomy-of-story": (
        "John Truby spent three decades consulting on over a thousand scripts before publishing this architecture of narrative genius. "
        "While standard manuals obsess over arbitrary three-act timing, Truby maps the 22 organic building blocks of character growth—"
        "grounding plot entirely in a protagonist's moral flaw and psychological weakness. "
        "He argues that great stories aren't about overcoming external obstacles, but about surviving the painful death of a false worldview. "
        "It belongs on this shelf because it elevates narrative design from commercial mechanics into moral philosophy."
    ),
    "the-anatomy-of-story-22-steps-to-becoming-a-master-storyteller-unknown": (
        "John Truby's 22-step framework is the definitive antidote to plot-driven emptiness. "
        "Too many modern books and films are explosive rollercoasters that leave you emotionally hollow twenty minutes later; "
        "Truby shows you how to design a story where the hero's internal battle against their own destructive moral blindness dictates "
        "every twist and betrayal. A cornerstone book-lover text for anyone fascinated by the invisible structural geometry that makes great art endure."
    ),
    "master-shots-100-advanced-camera-techniques-to-get-an-expensive-look-on-your-low-budget-movie-unknown": (
        "Christopher Kenworthy's visual guide is a cult favorite among guerrilla filmmakers who refuse to let small budgets look amateurish. "
        "Through 3D overhead computer models and frame-by-frame analysis, it demystifies how masters like Spielberg, Fincher, and Scorsese "
        "use camera movement, foreground blocking, and spatial depth to create unbearable tension without expensive crane rigs. "
        "A delightfully nerdy visual playbook that permanently alters how you watch every movie you see."
    ),
    "robert-mckee-story": (
        "Robert McKee's *Story* is the Vatican council of dramatic writing. "
        "His alumni have won over 60 Academy Awards and 200 Emmys, and his three-day marathon lectures have been attended by everyone "
        "from Pixar story leads to David Bowie. But beyond Hollywood prestige, McKee writes with Shakespearean fire about the sacred duty "
        "of the storyteller: that in a world awash in commercial lies and political cynicism, an honest, beautifully structured story "
        "is one of the few places left where human beings can encounter moral truth. Required reading for anyone who loves the craft."
    ),
    "story-robert-mckee": (
        "Robert McKee's *Story* is the Vatican council of dramatic writing. "
        "His alumni have won over 60 Academy Awards and 200 Emmys, and his three-day marathon lectures have been attended by everyone "
        "from Pixar story leads to David Bowie. But beyond Hollywood prestige, McKee writes with Shakespearean fire about the sacred duty "
        "of the storyteller: that in a world awash in commercial lies and political cynicism, an honest, beautifully structured story "
        "is one of the few places left where human beings can encounter moral truth. Required reading for anyone who loves the craft."
    ),
    "save-the-cat-the-last-book-on-screenwriting-you-ll-ever-need-by-blake-snyder-unknown": (
        "Blake Snyder's book is both the most worshipped and most vilified manual in Hollywood history. "
        "Purists hate it because it codified the 15-beat minute-by-minute commercial movie structure that dominated 2000s studio slates, "
        "yet every working screenwriter has dog-eared copies hidden in their drawer. Snyder understood audience psychology with terrifying clarity: "
        "the 'Save the Cat' beat, the 'All Hope is Lost' moment, and the 'Dark Night of the Soul' aren't cynical gimmicks—they are the primal beats "
        "where an audience either surrenders to emotional empathy or tunes out. Love it or debate it, you cannot understand modern film culture without it."
    ),
    "save-the-cat-writes-for-tv-jamie-nash": (
        "Jamie Nash takes Snyder's classic framework and adapts it for the Golden Age of serialized television, "
        "where character arcs must stretch across seasons rather than 110 pages. "
        "It's a brilliant deep dive into how shows like *Breaking Bad*, *Succession*, and *Stranger Things* construct episodic engines "
        "that sustain narrative velocity without running out of steam. Perfect for story nerds studying the golden era of peak TV."
    ),
    "save-the-cat-writes-a-novel-by-jessica-brody-unknown": (
        "Jessica Brody accomplished the unthinkable: she took Hollywood screenwriting discipline and translated it into language "
        "that novel writers could embrace without losing internal character depth. "
        "She breaks down the murky middle of novels—the dread-filled 'desert' where 90% of manuscript drafts die—into actionable emotional milestones. "
        "A beloved staff pick for novelists trying to marry literary prose with unputdownable pacing."
    ),
    "screenplay-the-foundations-of-screenwriting-syd-field": (
        "The Big Bang of modern screenwriting education. In 1979, Syd Field sat down with hundreds of Hollywood scripts and noticed that "
        "successful cinematic narratives invariably hinged on two tectonic plot points and a midpoint reversal. "
        "Before Field, screenwriting was treated as occult black magic; after Field, it was an intelligible architectural art form. "
        "Even when writers actively rebel against Field's three-act paradigm, they are defining their rebellion against *his* map."
    ),
    "sculpting-in-time-andrei-tarkovsky": (
        "Andrei Tarkovsky's philosophical manifesto is sacred scripture for cinephiles. "
        "Rejecting Eisenstein's kinetic montage cutting as intellectual manipulation, Tarkovsky argued that cinema's true metaphysical power "
        "is printing the actual texture of lived time onto film. Reading this feels like entering a monastery of pure artistic conviction: "
        "he writes of wind in the grass, spiritual longing, memory, and mortal decay with an intensity that shames commercial entertainment. "
        "It belongs on this shelf to remind us that image and sound can touch the divine."
    ),
    "the-6-rules-of-fiction-tiago-amaral": (
        "Tiago Amaral strips the pompous academic bloat from prose writing and focuses on the visceral mechanical triggers "
        "that keep a reader turning pages at 2:00 AM. A concise, punchy masterclass on scene economy, sensory anchor points, "
        "and subtext that cuts straight through writerly hesitation."
    ),
    "watchmen-complete": (
        "Alan Moore and Dave Gibbons' nine-issue masterpiece remains the greatest graphic work of the 20th century. "
        "Named by *Time* as one of the 100 best novels since 1923, it did far more than deconstruct superheroes; it interrogated Cold War dread, "
        "fascistic vigilante psychology, and the horrifying moral mathematics of killing millions to save billions. "
        "Gibbons' strict nine-panel grid acts like an ominous mechanical clock ticking down to midnight. "
        "A monumental work that proves graphic literature can match Dostoyevsky in psychological torment and Joyce in formal intricacy."
    ),
    "the-sandman-complete-unknown": (
        "Neil Gaiman's magnum opus transformed comics into an enduring mythic cathedral. "
        "From Shakespeare striking Faustian bargains in Elizabethan taverns to Lucifer retiring from Hell to run an Australian piano bar, "
        "Gaiman created a 75-issue meditation on mortality, storytelling, and change. "
        "The underlying truth that Morpheus must confront is the central tragedy of human life: that which cannot adapt to time must inevitably perish. "
        "One of the crowning achievements of contemporary fantasy."
    ),
    "goodnight-punpun-complete": (
        "Inio Asano's *Goodnight Punpun* is one of the most emotionally devastating manga series ever conceived. "
        "Drawing the protagonist as a simple, childlike bird doodle while placing him in hyper-detailed, photorealistic Japanese landscapes, "
        "Asano pulls you into a harrowing journey through domestic trauma, crippling depression, and toxic adolescent obsession. "
        "It is a brutal, beautiful masterpiece that refuses to offer easy redemption, capturing the raw, messy ache of growing up with unsparing empathy."
    ),
    "akira-unknown": (
        "Katsuhiro Otomo's sprawling 2,000-page epic is the undisputed titan of cyberpunk graphic art. "
        "Beyond its legendary 1988 anime adaptation, the original manga offers a staggering, panoramic look at post-apocalyptic Tokyo—"
        "combining teenage biker rebellion, military corruption, and cosmic psychic evolution with architectural drafting precision "
        "that remains unmatched in comic history. A jaw-dropping testament to the sheer kinetic scale of ink on paper."
    ),
    "the-food-lab-better-home-cooking-through-science-unknown": (
        "J. Kenji López-Alt took the nostalgic folklore and superstition out of home cooking and replaced it with rigorous empirical science. "
        "Armed with an MIT degree and thousands of temperature-logged experiments, Kenji shows why salting steak early alters osmotic pressure, "
        "why baking soda makes french fries shatteringly crisp, and why traditional recipes are often flat-out wrong. "
        "An absolute kitchen bible for people who want to understand *why* food tastes incredible rather than just blindly following instructions."
    ),
    "tim-feriss-the-4-hour-chef": (
        "Tim Ferriss uses the culinary arts as a trojan horse to teach metalearning—the science of mastering any complex human skill in minimum time. "
        "Part wild cookbook, part survival manual, part cognitive psychology handbook, it is filled with obsessive experiments, "
        "micro-habits, and fascinating culinary history. A testament to playful autodidact curiosity."
    ),
    "the-book-of-ramen-unknown": (
        "A passionate, deep-dive tribute to the artisanal alchemy of Japan's most obsessive noodle culture. "
        "From multi-day chashu braises and alkaline noodle chemistry to the metaphysical balance of dashi and tare, "
        "it celebrates the regional masters who dedicate their entire lives to perfecting a single steaming bowl. Pure culinary devotion."
    ),
    "maangchi-s-real-korean-cooking-unknown": (
        "Maangchi is the internet's beloved Korean mother, and this collection is the gold standard of accessible, authentic Korean culinary heritage. "
        "Her recipes don't water down fermentations or substitute shortcuts; she celebrates the funky, spicy, deeply comforting genius of kimchi, "
        "gochujang, and home-cooked banchan with warmth, generosity, and infectious joy."
    ),
    "arundhati-roy-the-god-of-small-things": (
        "Arundhati Roy's Booker Prize-winning debut is a linguistic miracle. "
        "Set amidst the humid riverways of Kerala, it maps the forbidden love between an upper-caste Syrian Christian mother and an Untouchable carpenter, "
        "interrogating the ancient 'Love Laws' that dictate who should be loved, how, and how much. "
        "Roy invented a fresh, sensory English dialect—inventing words, capitalising whimsically, and embedding child perspectives with heart-stopping beauty. "
        "On this shelf because it reminds you how breathtakingly alive the English language can be when written with poetic courage."
    ),
    "banana-yoshimoto-kitchen": (
        "Banana Yoshimoto's cult Japanese novella is an exquisite sanctuary against existential heartbreak. "
        "When Mikage's grandmother dies, leaving her completely orphaned, she finds solace sleeping on the kitchen floor beside the hum of the refrigerator. "
        "Yoshimoto writes about grief, trans identities, and the quiet ritual of making soup with a tender, translucent prose style "
        "that captures the fragility of modern urban youth like nobody else. A timeless comfort read."
    ),
    "beloved-tonimorrison": (
        "Toni Morrison's Pulitzer Prize masterpiece is the closest thing American literature has produced to ancient Greek tragedy. "
        "Based on the historical tragedy of Margaret Garner, it chronicles Sethe, an escaped enslaved mother haunted by the literal and psychological ghost "
        "of the baby daughter she slaughtered to spare her from the living hell of plantation bondage. "
        "Morrison's prose is Biblical in its moral weight, unsparing in its sorrow, and profound in its proclamation that reclaiming a freed self "
        "is the most heroic labor on earth. A towering, essential monument of world literature."
    ),
    "all-art-is-propaganda-george-orwell": (
        "George Orwell was the greatest essayist of the twentieth century, and this collection gathers his sharpest cultural criticism. "
        "From dissecting Charles Dickens and boys' boarding school penny weeklies to his immortal 'Politics and the English Language', "
        "Orwell dismantled the comfortable hypocrisies of literary elitism. "
        "He understood that aesthetic style is never neutral; clear prose is a moral weapon against authoritarian deceit. Essential food for the mind."
    ),
    "aristotle-nicomachean-ethics": (
        "Aristotle's foundational ethical treatise is not a collection of abstract dogmas; it is a practical guide to *eudaimonia*—human flourishing. "
        "He argues that virtue is not an innate genetic gift or a sudden stroke of lightning, but a muscular habit cultivated through the humble rhythm "
        "of daily action. His doctrine of the golden mean remains the most pragmatic framework ever conceived for navigating the chaotic extremes of modern life."
    ),
    "art-as-therapy-alain-de-botton": (
        "Alain de Botton and John Armstrong rescue visual art from the cold, intimidating mausoleum of academic art history. "
        "They propose a revolutionary new way to look at paintings: as a psychological medicine cabinet designed to heal human sorrow, "
        "correct our cognitive blind spots, and restore our gratitude for ordinary days. "
        "A gorgeously illustrated, compassionate book that changes how you walk through every gallery in the world."
    ),
    "all-tomorrows-cm-kosemen-unknown": (
        "C.M. Kosemen's cult speculative fiction epic is a billion-year cosmic roller coaster unlike anything else ever conceived. "
        "When humanity is conquered and genetically disfigured into bizarre biological tools by the godlike Qu, "
        "they must endure eons of agonizing evolutionary adaptation across the stars. "
        "It is terrifying, grotesque, and ultimately deeply moving—leaving you with a profound, dizzying gratitude for the simple miracle of being human."
    ),
    "ann-handley-everybody-writes": (
        "Ann Handley wrote the definitive modern manifesto for anyone whose career depends on words on screens. "
        "With humor, zero pretension, and deep empathy, she reminds us that good writing isn't a genetic lottery—it's a habit of caring about the reader. "
        "A warm, immensely practical desk companion that makes every email, post, and pitch you draft noticeably sharper."
    ),
    "bad-pharma-ben-goldacre": (
        "Ben Goldacre is the scourge of medical quackery and pharmaceutical manipulation. "
        "In *Bad Pharma*, he lays bare the systemic corruption of clinical drug trials: how negative results are buried, "
        "how regulatory agencies are captured, and how doctors are misled into prescribing expensive, ineffective treatments to real patients. "
        "A furious, meticulously footnoted exposé that every scientifically minded citizen needs to read."
    ),
    "barabara-oakley-a-mind-for-numbers": (
        "Barbara Oakley flunked high school math and science before retraining her brain in adulthood to become an engineering professor. "
        "This book is the gold-standard manual on neuroplasticity, chunking, and the crucial dance between focused and diffuse modes of thinking. "
        "If you have ever felt 'bad at numbers' or struggled to master technical disciplines, Oakley's compassionate cognitive toolkit is life-changing."
    ),
    "build-an-unorthodox-guide-to-making-things-worth-making-tony-fadell": (
        "Tony Fadell led the teams that created the iPod, the iPhone, and the Nest Learning Thermostat. "
        "Unlike most Silicon Valley memoirs that peddle frictionless success mythology, Fadell provides the gritty, unsanitized operational wisdom "
        "of real hardware manufacturing: firing friends, surviving executive battles with Steve Jobs, and obsessing over cardboard packaging boxes. "
        "The ultimate product builder's bible."
    ),
    "barthes-the-death-of-the-author-unknown": (
        "Roland Barthes' landmark 1967 essay shattered literary criticism by severing the text from the tyrannical authority of the author's biography. "
        "By declaring that 'the birth of the reader must be ransomed by the death of the Author', Barthes liberated literature, "
        "turning reading from a passive historical autopsy into an active, creative act of meaning-making. A short, revolutionary text that reshaped postmodern thought."
    ),
    "aligarh-screenplay": (
        "Apurva Asrani and Hansal Mehta's quiet masterpiece chronicles the true tragedy of Professor Shrinivas Ramchandra Siras, "
        "who was stripped of his university chair after being secretly filmed in his private bedroom. "
        "The screenplay is extraordinary for what it refuses to do: it avoids melodramatic speechifying and courtroom bombast, "
        "finding its power in quiet evenings, old cassette recordings of Lata Mangeshkar, and the sacred human right to gentle privacy."
    ),
    "dev-d-screenplay": (
        "Anurag Kashyap and Vikramaditya Motwane's script permanently ruptured Indian independent cinema in 2009. "
        "Transposing Sarat Chandra Chattopadhyay's classic *Devdas* into the neon-lit, drug-fueled alleys of Paharganj and affluent Punjab farms, "
        "they stripped the romanticized tragedy of alcoholism of its poetic martyrdom, exposing the toxic male narcissism underneath. "
        "Pioneering dialogue economy, visceral sound cues, and sensory excess on the page."
    ),
    "memories-of-murder-screenplay-bong-joon-ho-shim-sung-bo": (
        "Bong Joon-ho's procedural masterpiece set against the 1986 Hwaseong serial murders is arguably the greatest crime screenplay of this century. "
        "Balancing slapstick rural detective incompetence with the suffocating terror of military dictatorship, "
        "Bong crafts a murder mystery where the real antagonist isn't merely the faceless killer, but the systemic decay of an entire society. "
        "The final direct gaze into the camera lens remains an indelible cinematic shockwave."
    ),
    "parasite-script": (
        "The first foreign-language film to win Best Picture and Best Original Screenplay at the Academy Awards. "
        "Bong Joon-ho and Han Jin-won's screenplay is a marvel of spatial architecture: the multi-level verticality of Seoul—"
        "from sun-drenched hilltop architectural marvels down to rain-drowned semi-basements—mirrors the inescapable class trap of modern capitalism. "
        "Hilarious, shocking, and tragically profound."
    ),
    "gangs-of-wasseypur-part-1-movie-script-film-companion-unknown": (
        "Anurag Kashyap and Zeishan Quadri's sprawling coal-mafia epic is India's *Godfather*. "
        "Stretching across six decades of generational vendettas, union politics, and provincial violence, "
        "its dialogue crackles with dark rural humor and visceral rhythm. "
        "A monumental screenplay that redefined Indian cinematic storytelling and spawned a generation of imitators."
    ),
    "masaan-movie-script-film-companion-unknown": (
        "Varun Grover and Neeraj Ghaywan's Cannes-winning screenplay weaves two parallel stories along the burning ghats of Varanasi. "
        "Deepak, a lower-caste engineering student tending funeral pyres, and Devi, a young woman caught in moral blackmail after a hotel raid, "
        "are both struggling against centuries of caste and patriarchy. Grover's dialogue is steeped in poetic Hindi and authentic colloquial warmth, "
        "capturing grief and love with sublime, heart-wrenching grace."
    ),
    "the-lunchbox-screenplay-film-companion-unknown": (
        "Ritesh Batra's BAFTA-nominated screenplay is a masterclass in urban intimacy. "
        "Centering on a misplaced lunchbox delivery in Mumbai's legendary dabbawala network that sparks an epistolary romance "
        "between an isolated widower and an ignored housewife, the script proves that quiet observation and sensory specificity "
        "can convey more devastating emotional truth than a thousand dramatic explosions."
    ),
    "t-u-m-b-b-a-d-unknown": (
        "Rahi Anil Barve's decade-in-the-making mythological horror script is a visual and thematic wonder. "
        "Rooted in Maharashtrian folklore and the mythical demon of greed, Hastar, the story explores how multi-generational avarice "
        "rots an aristocratic family from the inside out amidst endless torrential monsoon rains. "
        "Original, unsettling, and atmospheric in every line."
    ),
    "arrival-2016-unknown": (
        "Eric Heisserer's Oscar-nominated adaptation of Ted Chiang's *Story of Your Life* is one of the smartest sci-fi scripts ever written. "
        "By structuring the narrative around the Sapir-Whorf hypothesis and non-linear Heptapod orthography, "
        "the script achieves an emotional gut punch that turns time travel into a heartbreaking meditation on parenting, grief, and unconditional love."
    ),
    "everything-everywhere-all-at-once-2022-unknown": (
        "Daniel Kwan and Daniel Scheinert's Oscar-winning screenplay is a sensory triumph that turns ADHD cosmic chaos into pure emotional catharsis. "
        "Beneath hot dog fingers, tax audits, and the infinite everything bagel lies the tender, beating heart of an immigrant mother and daughter "
        "discovering that radical kindness and presence are the only rational defenses against existential despair."
    ),
    "get-out-2017-unknown": (
        "Jordan Peele's Oscar-winning debut script permanently revitalized the social thriller genre. "
        "By translating the subtle, polite microaggressions of affluent liberal racism into literal, horrifying bodily theft, "
        "Peele crafted a cultural milestone. The 'Sunken Place' immediately entered the global cultural lexicon as the definitive metaphor "
        "for modern systemic gaslighting and disenfranchisement."
    ),
    "groundhogday-unknown": (
        "Danny Rubin and Harold Ramis's screenplay is one of the most structurally ingenious comedies ever written—"
        "so culturally pervasive that the title became an English idiom for endless repetition. "
        "Underneath the comedic premise of a cynical weatherman trapped in an infinite time loop lies a profound Buddhist fable "
        "about moving from narcissistic despair through nihilism into genuine altruistic grace."
    ),
    "snowpiercer-screenplay-bong-joon-ho-kelly-masterson": (
        "Bong Joon-ho and Kelly Masterson's sci-fi thriller sets class warfare inside a 1,000-car perpetual motion train circumnavigating a frozen Earth. "
        "Every single car represents a different socio-economic strata, from filthy tail-section squalor to lavish sushi bars and hedonistic nightclubs. "
        "Brilliant, kinetic, allegorical action that refuses to let the viewer look away from the ugly compromises of human survival."
    )
}

def clean_and_synthesize(text, title="", author=""):
    """Transforms arbitrary 4-tier blocks into a smooth, compelling, literate editorial paragraph."""
    if not text:
        return f"An essential addition to this collection, celebrated for visionary craft and narrative resonance."

    # If it's the generic boilerplate, synthesize a clean literate note
    if "celebrated for original thought and lasting thematic resonance" in text:
        return (
            f"A celebrated work in {author}'s repertoire that stands out for its sharp observational eye and uncompromising voice. "
            f"Added to this collection because it cuts through standard genre clichés, rewarding curious readers with "
            f"rich narrative rhythm and ideas that linger long after the final page."
        )

    # Check for legacy sections
    has_headers = any(h in text for h in ["Accolades & Standing", "Cultural Impact", "Behind-the-Scenes Lore", "The 'Damn' Factor"])
    if not has_headers:
        # Already clean prose
        return text.strip()

    # Extract components
    m_acc = re.search(r"\*\*Accolades & Standing:\*\*\s*(.*?)(?=\n\n|$)", text, re.S)
    m_cult = re.search(r"\*\*Cultural Impact( & Shockwaves)?:\*\*\s*(.*?)(?=\n\n|$)", text, re.S)
    m_lore = re.search(r"\*\*Behind-the-Scenes Lore:\*\*\s*(.*?)(?=\n\n|$)", text, re.S)
    m_damn = re.search(r"\*\*The 'Damn' Factor:\*\*\s*(.*?)(?=\n\n|$)", text, re.S)

    acc = m_acc.group(1).strip() if m_acc else ""
    cult = m_cult.group(2 if m_cult.lastindex == 2 else 1).strip() if m_cult else ""
    lore = m_lore.group(1).strip() if m_lore else ""
    damn = m_damn.group(1).strip() if m_damn else ""

    parts = []
    # If lore exists and is juicy, lead or weave it
    if lore and len(lore) > 20:
        parts.append(lore)
    if cult and len(cult) > 20 and cult != lore:
        parts.append(cult)
    if damn and len(damn) > 20 and damn != cult:
        parts.append(damn)
    elif acc and len(acc) > 20:
        parts.append(acc)

    if parts:
        # Join into 1 or 2 clean flowing paragraphs
        return "\n\n".join(parts)

    # Fallback to stripped text
    clean = re.sub(r"\*\*(Accolades & Standing|Cultural Impact( & Shockwaves)?|Behind-the-Scenes Lore|The 'Damn' Factor):\*\*\s*", "", text).strip()
    return clean

def main():
    if not DATA_PATH.exists():
        print(f"Error: {DATA_PATH} not found.")
        return

    books = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    updated = 0
    nerd_count = 0

    for b in books:
        bid = b.get("id", "")
        # Check if we have a bespoke nerd editorial
        if bid in NERD_EDITORIALS:
            b["why_love"] = NERD_EDITORIALS[bid]
            nerd_count += 1
            updated += 1
            continue

        # Try partial match on bespoke nerd editorials
        matched_bespoke = False
        for k, essay in NERD_EDITORIALS.items():
            if k in bid or bid in k:
                b["why_love"] = essay
                nerd_count += 1
                updated += 1
                matched_bespoke = True
                break
        if matched_bespoke:
            continue

        # Otherwise synthesize existing why_love
        current_why = b.get("why_love", "")
        synthesized = clean_and_synthesize(current_why, b.get("title", ""), b.get("author", ""))
        b["why_love"] = synthesized
        updated += 1

    DATA_PATH.write_text(json.dumps(books, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated all {updated} books in {DATA_PATH}!")
    print(f"Bespoke book-nerd editorials injected: {nerd_count}")

if __name__ == "__main__":
    main()
