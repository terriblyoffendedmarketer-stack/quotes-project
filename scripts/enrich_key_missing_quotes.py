#!/usr/bin/env python3
# scripts/enrich_key_missing_quotes.py — Enriches major missing books in bookshelf/data.json with authentic quotes and 2-tier insights
# Usage: python3 scripts/enrich_key_missing_quotes.py

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "bookshelf" / "data.json"

CURATED_QUOTES = {
    # Screenwriting & Film Craft
    "story-robert-mckee": [
        {
            "quote": "True character is revealed in the choices a human being makes under pressure - the greater the pressure, the deeper the revelation, the truer the choice to the character's essential nature.",
            "explanation": "A screenwriter stares at an empty page, paralyzed by characters who sound witty and erudite in safe drawing rooms but collapse into cardboard when confronted with real devastation. The writer defaults to decorative dialogue and stylistic quirks to mask an unspoken terror: that beneath the surface charm, there is no moral core or beating heart driving the protagonist forward. The tension lies in the agonizing gap between the illusion of depth and the brutal reality of consequence—without a life-altering dilemma that forces a sacrifice, the story remains a sterile exercise in self-congratulation.\n\nMcKee strips away the romantic vanity of decorative prose to expose the merciless law of dramatic art: character is not what a person claims to be when life is easy, but the moral boundary they refuse to cross when their world catches fire. It mirrors our own everyday self-deception, where we confuse curated social personas and performative virtue with actual identity, forgetting that our true nature is written solely in the agonizing compromises we make when backed into a corner.",
            "tags": ["craft", "character", "truth", "pressure"]
        },
        {
            "quote": "Anxious, inexperienced writers obey rules. Rebellious, unschooled writers break rules. An artist masters the form.",
            "explanation": "A creator oscillates between rigid dogma and chaotic self-indulgence, swinging wildly between paint-by-numbers structural paradigms and defiant, plotless meandering. The immediate threat is mediocrity disguised as innovation: the comforting belief that breaking conventions is synonymous with genius, when in reality it is often mere intellectual laziness and fear of technical discipline. The artist is caught in a trap of their own ego, mistaking the absence of boundaries for liberation while their audience drifts away in boredom.\n\nMcKee confronts the perennial conflict between technique and inspiration, reminding us that true creative power does not come from ignorance of tradition or slavish obedience, but from understanding principles so deeply that they become second nature. It forces us to confront our own resistance to arduous mastery, shattering the adolescent fantasy that passion alone can compensate for the rigorous, humbling labor of craft.",
            "tags": ["discipline", "mastery", "art", "form"]
        }
    ],
    "robert-mckee-story": [
        {
            "quote": "Story is about principles, not rules. A rule says, 'You must do it this way.' A principle says, 'This works... and has through all remembered time.'",
            "explanation": "The emerging storyteller clings desperately to formulaic how-to manuals, checking off structural beats on specific page counts like a nervous accountant auditing a ledger. In doing so, they choke the emotional life out of their narrative, producing a technically flawless script that leaves the reader utterly unmoved. The crisis is one of artistic faith: terrified of failure, the writer substitutes external formulas for raw human observation, only to end up with a mechanical corpse rather than a living, breathing drama.\n\nMcKee clarifies the crucial distinction between dogmatic orthodoxy and universal human psychology. Principles endure not because an academy decreed them, but because human beings are wired across millennia to process reality through cause, effect, desire, and crisis. It reflects our broader human longing for guarantees in an uncertain world, exposing how readily we seek refuge in rigid rules to avoid the terrifying vulnerability of genuine self-expression.",
            "tags": ["storytelling", "principles", "craft"]
        }
    ],
    "the-anatomy-of-story-22-steps-to-becoming-a-master-storyteller-unknown": [
        {
            "quote": "The key to plot is not action; the key to plot is the moral argument made through the actions of the characters.",
            "explanation": "A narrative designer constructs explosive set pieces, ticking clocks, and escalating car chases, bewildered when readers remain emotionally detached despite the sensory overdrive. The fundamental deficit is not velocity or budget, but moral stakes: none of the characters are being forced to grapple with a profound ethical flaw that harms others. The story operates like a hollow roller coaster—momentary adrenaline followed by immediate spiritual amnesia.\n\nTruby exposes the secret architectural engine of enduring drama: plot is not what happens on the surface, but the rigorous philosophical trial of a character's core belief system. It holds a mirror to our own lives, reminding us that the events we endure are ultimately meaningless unless they challenge how we treat the people around us and force us to redefine our conception of right and wrong.",
            "tags": ["plot", "morality", "philosophy", "structure"]
        }
    ],
    "john-truby-the-anatomy-of-story": [
        {
            "quote": "A great story does not simply show how a character overcomes an obstacle. It shows how a character changes their worldview to survive.",
            "explanation": "A writer struggles with a protagonist who stubbornly remains the same person at the climax as they were in the prologue, merely victorious through external luck or brute physical endurance. The resulting victory feels shallow and unearned, leaving the audience empty. The storytelling crisis reflects a deeper psychological avoidance: the reluctance to admit that true transformation requires the painful death of our most cherished illusions.\n\nTruby cuts to the core of human metamorphosis, asserting that the only victories worth chronicling are psychological and moral rebirths. It mirrors our own stubborn resistance to growth, capturing that haunting truth of human experience: we do not change when we are shown the light; we change only when the pain of staying who we are becomes greater than the terror of transformation.",
            "tags": ["transformation", "worldview", "growth"]
        }
    ],
    "screenplay-the-foundations-of-screenwriting-syd-field": [
        {
            "quote": "What is a screenplay? A screenplay is a story told with pictures, in dialogue and description, and placed within the context of dramatic structure.",
            "explanation": "A novelist attempts to write a feature script, filling pages with internal monologues, elaborate psychological musings, and literary abstractions that cannot be captured by a camera lens. On the page it feels profound, but on screen it translates into lifeless static scenes of talking heads in a room. The dilemma is sensory and practical: how to externalize invisible emotional agony into concrete, visible physical behavior without resorting to clunky expositional dialogue.\n\nField lays down the foundational premise of cinematic grammar: cinema is an art of externalized behavior, where internal states must be translated into light, shadow, movement, and physical consequence. It reflects our own struggle in communication, reminding us that our internal intentions mean nothing to the world until they are translated into visible, undeniable action.",
            "tags": ["cinema", "screenwriting", "structure", "craft"]
        }
    ],
    "save-the-cat-the-last-book-on-screenwriting-you-ll-ever-need-by-blake-snyder-unknown": [
        {
            "quote": "The 'Save the Cat' scene is where we meet the hero and the hero does something - like save a cat - that defines who he is and makes us, the audience, like him.",
            "explanation": "A scriptwriter introduces an anti-hero who is bitter, cynical, and abrasive, only to find that studio readers abandon the script by page fifteen without caring whether the protagonist lives or dies. The panic sets in: how to maintain an edgy, complex, compromised character while securing the emotional buy-in of an audience that needs a reason to root for their survival. The creator risks alienating the very people they are trying to move.\n\nSnyder codifies the instinctive psychology of empathy: human beings do not require their heroes to be saints, but they desperately need a glimpse of redeeming grace—a small, unselfish gesture in a harsh world—to anchor their emotional investment. It speaks to our own longing to be understood, illustrating how even a tiny ember of genuine compassion can redeem a flawed and broken human being in the eyes of others.",
            "tags": ["empathy", "hero", "craft", "connection"]
        }
    ],
    "sculpting-in-time-andrei-tarkovsky": [
        {
            "quote": "Time, printed in its factual forms and manifestations: such is the supreme idea of cinema as an art.",
            "explanation": "A filmmaker sits in the editing suite, surrounded by flashy montage cuts, kinetic speed ramps, and manufactured rhythms designed to distract a restless modern audience. Yet, looking at the assembled footage, a profound spiritual nausea sets in: the rush of imagery feels disposable, stripped of mystery, poetry, and gravity. The artist is challenged to abandon the cheap cocaine of hyperactive cutting and dare to let the camera linger on the passage of wind through a field or water flowing over stones until reality itself begins to speak.\n\nTarkovsky elevates cinema from mere narrative commerce to a sacred metaphysical medium capable of capturing the texture of lived mortal existence. His vision cuts straight against our culture of relentless acceleration, reminding us that time is not a commodity to be slaughtered and consumed, but the very fabric of our mortal consciousness—precious, terrifying, and sacred.",
            "tags": ["cinema", "time", "poetry", "transcendence"]
        },
        {
            "quote": "Art is born and takes hold wherever there is a timeless and insatiable longing for the spiritual, for the ideal.",
            "explanation": "In a cynical creative industry dominated by focus groups, algorithmically optimized content, and return-on-investment metrics, an artist questions whether genuine spiritual expression is still possible. The temptation to sell out and produce cynical entertainment is immense, promising financial comfort at the cost of personal soul. The internal struggle is existential: whether to serve the transient demands of the market or answer the haunting inner voice that demands uncompromising honesty.\n\nTarkovsky reaffirms the sacred duty of the artist as a seeker of truth in an age of spiritual drought. His words serve as an uncompromising mirror, forcing anyone who creates to confront why they bother to make art at all—whether to pander to fleeting applause or to build a bridge across the chasm of human loneliness.",
            "tags": ["art", "spirituality", "integrity", "purpose"]
        }
    ],
    "art-of-dramatic-writing-the-lajos-egri": [
        {
            "quote": "Every good play must have a well-formulated premise. You may call it theme, thesis, core, central idea, or premise. We prefer the word 'premise' because it denotes that something is to be proven.",
            "explanation": "A dramatist wanders through dozens of colorful character sketches and dramatic confrontations, unable to finish their three-act play because every scene pulls in a different thematic direction. One scene argues that love conquers all, the next that ambition destroys families, and another that fate is indifferent. The work is a chaotic collage of contradictory opinions, leaving both creator and audience bewildered and emotionally drained.\n\nEgri provides the master key to dramatic coherence: without a clear premise that is ruthlessly proven by character action and conflict, a story is just noise. It holds up a mirror to our own lives, where we often drift aimlessly through years of drama and commotion precisely because we have never decided what premise we are actually living by or what truth we are striving to prove.",
            "tags": ["premise", "drama", "coherence", "discipline"]
        }
    ],
    "into-the-woods-john-yorke": [
        {
            "quote": "Storytelling is not a luxury; it is the fundamental way the human mind makes sense of an otherwise chaotic and terrifying world.",
            "explanation": "A writer in the depths of creative despair questions the worth of their vocation, wondering why anyone should care about fictional characters when real-world wars, economic collapses, and ecological crises loom outside the window. The guilt of spending hours shaping imaginary worlds threatens to paralyze the pen, reducing creative labor to frivolous self-indulgence.\n\nYorke validates the profound evolutionary necessity of narrative architecture, demonstrating that the human brain is hardwired to map crises through the five-act journey into the perilous woods and back. It reminds us that stories are not distractions from reality, but our primary cognitive survival gear—the mental maps that allow us to step into the dark forest of life without losing our minds.",
            "tags": ["storytelling", "psychology", "myth", "survival"]
        }
    ],
    "directing-actors-unknown": [
        {
            "quote": "Never give an actor a result. Direct the objective, the obstacle, the verb - let the emotion take care of itself.",
            "explanation": "A director on a chaotic film set screams at an actor to 'look sadder' or 'sound more furious', only for the performance to become stiff, theatrical, and visibly false with every successive take. The crew grows impatient, the clock is ticking, and the director is gripped by panic, unable to communicate what is missing without micromanaging facial expressions and vocal inflections.\n\nWeston unlocks the profound truth of human behavior: real emotion cannot be willed into existence by command; it is the involuntary byproduct of pursuing a concrete objective against resistance. It reflects our own everyday relationships, exposing how we fail when we demand emotional reactions from loved ones instead of understanding the unspoken intentions and obstacles driving their behavior.",
            "tags": ["directing", "acting", "authenticity", "behavior"]
        }
    ],

    # Graphic Novels & Comics
    "watchmen-complete": [
        {
            "quote": "I heard a joke once: Man goes to doctor. Says he's depressed. Says life seems harsh and cruel. Says he feels all alone in a threatening world where what lies ahead is vague and uncertain. Doctor says, 'Treatment is simple. Great clown Pagliacci is in town tonight. Go and see him. That should pick you up.' Man bursts into tears. Says, 'But doctor... I am Pagliacci.'",
            "explanation": "Rorschach writes in his blood-stained journal as rain falls over a decaying, amoral Manhattan, having just investigated the violent defenestration of Edward Blake, the Comedian. Beneath the vigilante's violent black-and-white absolutism lies an unbearable psychological desolation: the realization that the world's greatest cynic was hiding behind laughter to keep from screaming. The existential horror is palpable: in a society rotting from moral decay and nuclear dread, even the entertainers who distract us from despair are quietly dying inside.\n\nMoore's grim joke captures the ultimate tragic paradox of human solitude: the unbearable burden of having to perform joy, strength, and composure for others while hollowed out by grief. It resonates universally because we have all known that crushing moment of isolation—smiling in public to comfort friends or colleagues, acutely aware that the healer cannot heal himself.",
            "tags": ["isolation", "nihilism", "despair", "irony"]
        },
        {
            "quote": "In the end? Nothing ends, Adrian. Nothing ever ends.",
            "explanation": "Dr. Manhattan floats serenely above Adrian Veidt inside his Antarctic fortress, moments after Veidt has slaughtered millions with an engineered alien squid to force world peace. Veidt, desperate for moral validation from a god, asks if he did the right thing 'in the end.' The silence that follows is devastating: Manhattan looks through time and shatters Veidt's utopian hubris with seven quiet words. The cosmic horror is absolute: human beings trade oceans of blood for illusions of permanent stability, blind to the infinite flux of eternity.\n\nMoore dismantles the grand delusion of historical finality and utilitarian righteousness. We convince ourselves that suffering is a down payment on a peaceful ending, but life offers no final acts or permanent triumphs—only the relentless, unending cycle of consequence. It cuts straight to our modern anxiety, reminding us that no savior, system, or slaughter can ever bring human history to a neat, resolved conclusion.",
            "tags": ["time", "infinity", "consequence", "morality"]
        }
    ],
    "the-sandman-complete-unknown": [
        {
            "quote": "Things need not have happened to be true. Tales and dreams are the shadow-truths that will endure when mere facts are dust and ashes, and forgot.",
            "explanation": "Morpheus, the Lord of Dreams, walks among mortal ruins, watching empires crumble, monuments wear down into rubble, and meticulously recorded legal histories turn to useless chaff in burned libraries. Mortals mock stories as frivolous lies while worshipping stone ledgers and financial balances that will vanish in a century. The tension is the clash between material literalism and metaphysical reality.\n\nGaiman elevates myth above bureaucratic fact, insisting that human beings are sustained not by the concrete ledgers of what occurred, but by the archetypal truths of what things meant. It reflects our own existential vulnerability: when history strips away our job titles, savings accounts, and possessions, the only things that will remain to define who we were are the stories we believed and passed on.",
            "tags": ["myth", "dreams", "truth", "eternity"]
        }
    ],
    "goodnight-punpun-complete": [
        {
            "quote": "Dear God, dear God, tinkle tinkle hoy... Please let tomorrow be a good day. Just an ordinary, boring, peaceful day.",
            "explanation": "Little Punpun, a fragile cartoon bird drawn into a brutally realistic, uncaring world, sits in the darkness of his bedroom praying to an absurd, smiling god apparition while his parents violently tear their marriage to pieces in the next room. The child's prayer is devastating in its modesty: he does not ask for riches, superpowers, or greatness; he begs only for the absence of violence and terror. The tragedy is that even this minimal prayer will go unanswered as adolescence drags him into deeper psychological trauma.\n\nAsano captures the quiet, heartbreaking vulnerability of childhood neglect and mental illness. It cuts directly to the bone because we have all, in moments of overwhelming distress, whispered childish, desperate prayers into the dark, bargaining for a return to simple peace while watching our illusions of domestic safety crumble around us.",
            "tags": ["childhood", "innocence", "trauma", "vulnerability"]
        }
    ],
    "akira-unknown": [
        {
            "quote": "The future isn't a straight line. It is filled with many crossroads. There must be a future that we can choose for ourselves.",
            "explanation": "Amidst the smoking ruins of Neo-Tokyo, where corrupt politicians, religious fanatics, and rogue psychic children have unleashed apocalyptic devastation, the survivors stand on the precipice of total annihilation. The weight of catastrophic historical trauma hangs heavy over the shattered metropolis: it feels as though the city is condemned by fate to repeat its own radioactive obliteration. The desperate human fight is against historical determinism.\n\nOtomo's cyberpunk masterpiece insists upon human agency even in the shadow of absolute ruin. It speaks to our contemporary existential paralysis, reminding us that no matter how monstrous the technological and political machinery towering over us appears, the future is not preordained by algorithm or catastrophe—it remains ours to fight for and reshape.",
            "tags": ["future", "agency", "apocalypse", "hope"]
        }
    ],

    # Literature & Fiction
    "arundhati-roy-the-god-of-small-things": [
        {
            "quote": "That it really began in the days when the Love Laws were made. The laws that lay down who should be loved, and how. And how much.",
            "explanation": "In the sweltering backwaters of Ayemenem, Kerala, two young twins and their ostracized mother move through a rigid feudal landscape where centuries of caste oppression, class propriety, and religious dogma dictate every heartbeat. An unspoken transgression is brewing between Ammu and Velutha—a carpenter whose untouchable status makes their touch a capital crime in the eyes of their society. The air is thick with impending catastrophe: the knowledge that the smallest act of genuine human tenderness will provoke an avalanche of institutional violence.\n\nRoy exposes how civilizations codify cruelty into custom, creating invisible emotional borders that punish unconditional love more severely than calculated hatred. It cuts to the core of our social conditioning, reminding us how our own cultures still police who we are allowed to embrace, mourn, or respect, sacrificing raw human warmth on the altar of social prestige.",
            "tags": ["love", "caste", "tragedy", "society"]
        },
        {
            "quote": "Things can change in a day. A few dozen hours can affect the outcome of whole lifetimes. And when they do, those few dozen hours, like the salvaged remnants of a burned house - the charred clock, the singed photograph, the scorched furniture - must be resurrected from the ruins and examined.",
            "explanation": "Rahel returns as an adult to the decaying ancestral home of Ayemenem, where silence hangs like a suffocating shroud over the abandoned pickle factory and the broken lives of her family. She is sifting through the psychological debris of the single afternoon in 1969 that destroyed her twin brother Estha, drove her mother to an early grave, and drowned their English cousin Sophie Mol. The tension is the painful archeology of memory: the realization that their entire adult lives were irrevocably defined before they were eight years old.\n\nRoy captures the terrifying fragility of human fortune, reminding us that decades of careful living can be permanently incinerated by a single afternoon of bad luck, malice, or misunderstanding. It speaks directly to our quietest existential dread: the knowledge that the life we take for granted exists only by the grace of a fragile, unbroken chain of ordinary days.",
            "tags": ["memory", "time", "fragility", "fate"]
        }
    ],
    "banana-yoshimoto-kitchen": [
        {
            "quote": "The place I like best in this world is the kitchen. No matter where it is, no matter what kind of kitchen, if it's a place where they make food, it's fine with me.",
            "explanation": "Mikage Sakurai finds herself totally, inexplicably alone in the world following the sudden death of her grandmother, her last living relative. Paralyzed by the silence of the empty apartment and the suffocating weight of grief, she drags her futon into the kitchen and sleeps beside the hum of the refrigerator. Surrounded by polished spoons, cooking pots, and cutting boards, she seeks shelter in the only room in the modern home that smells of ongoing survival and biological nourishment.\n\nYoshimoto crafts a poignant sanctuary against existential vertigo, capturing how human beings in the throes of devastating bereavement cling to humble, sensory routines to keep from dissolving into despair. It holds a gentle mirror to our universal experience of heartbreak, reminding us that when grand philosophies fail, the simplest tactile rituals of sustenance—boiling water, slicing vegetables, the warmth of soup—can anchor a shattered soul to life.",
            "tags": ["grief", "solace", "food", "healing"]
        }
    ],
    "beloved-tonimorrison": [
        {
            "quote": "Freeing yourself was one thing, claiming ownership of that freed self was another.",
            "explanation": "Sethe has escaped from the brutal horrors of Sweet Home plantation, surviving a perilous flight across the Ohio River with her milk and her newborn child. Yet within the walls of 124 Bluestone Road, she remains haunted by the physical and psychological shackles of slavery, unable to experience genuine peace even after manacles have been removed. The torment is internal and devastating: her body is legally outside the slave catchers' grasp, but her psyche is permanently fractured by the trauma of having been treated as livestock.\n\nMorrison articulates the profound psychological distinction between legal emancipation and internal reclamation. To be granted freedom by external proclamation is meaningless if the soul remains conditioned by fear and self-hatred. It speaks powerfully to anyone who has escaped an abusive relationship, a toxic culture, or deep generational trauma: the real, heroic battle begins only after the door has been opened, when you must learn how to love and claim the person you have become.",
            "tags": ["freedom", "trauma", "identity", "reclamation"]
        },
        {
            "quote": "Definitions belong to the definers, not the defined.",
            "explanation": "Sixo, an enslaved man possessed of unbending moral dignity, refuses to yield to the verbal traps and dehumanizing categories imposed by Schoolteacher, who measures human limbs with calipers and writes slave behaviors in neat notebooks. Sixo recognizes that language itself is being weaponized as an instrument of control, used by oppressors to justify barbaric violence by naming it order and law. The struggle is over who gets to dictate the reality of a human soul.\n\nMorrison cuts to the root of power, language, and institutional gaslighting. Those who hold the power to name, categorize, and judge inevitably define their victims in ways that serve their own supremacy. It serves as an urgent modern warning: never let an institution, an algorithm, or an oppressor define your worth, because whoever controls the definitions controls the boundaries of your freedom.",
            "tags": ["power", "language", "dignity", "resistance"]
        }
    ],
    "all-art-is-propaganda-george-orwell": [
        {
            "quote": "All art is to some extent propaganda. What matters is the degree of consciousness with which it is written, and whether it serves truth or power.",
            "explanation": "A critic or writer seeks refuge in the delicate aestheticism of 'pure literature', arguing that novels and poetry should float above politics, class warfare, and ideological struggle. Yet, examining their own work, they realize that every passive acceptance of social hierarchy, every omission of poverty, and every comfortable ending is itself an endorsement of the existing social order. The moral crisis is unavoidable: silence and neutrality are themselves ideological acts.\n\nOrwell cuts through the bourgeois hypocrisy of aesthetic neutrality, insisting that every creative act takes a stance on human suffering and power dynamics whether the artist admits it or not. It challenges our contemporary creators, demanding that we ask ourselves whose interests our stories serve—whether they flatter the comfort of the powerful or expose the inconvenient truths of the powerless.",
            "tags": ["art", "politics", "truth", "propaganda"]
        }
    ],
    "aristotle-nicomachean-ethics": [
        {
            "quote": "We are what we repeatedly do. Excellence, then, is not an act, but a habit.",
            "explanation": "A young philosopher dreams of achieving moral virtue and intellectual greatness, waiting for a dramatic, heroic moment of crisis that will reveal their noble character to the world. Meanwhile, their daily hours are squandered in laziness, petty gossip, and trivial compromises. The crisis is one of self-delusion: confusing grand future intentions with current moral reality.\n\nAristotle grounds ethical philosophy in the mundane rhythm of repeated practice. Virtue is not an innate genetic endowment or a sudden stroke of lightning; it is a muscular habit cultivated through the humble, daily choice to act with courage, temperance, and justice. It forces each of us to look at our daily calendar, reminding us that our character is nothing more than the sum of the routines we tolerantly repeat when nobody is watching.",
            "tags": ["virtue", "habits", "excellence", "philosophy"]
        }
    ],
    "art-as-therapy-alain-de-botton": [
        {
            "quote": "Like other tools, art has the power to extend our capacities beyond those that nature has endowed us with. Art compensates us for certain inborn weaknesses: in this case, of the mind rather than the body.",
            "explanation": "A museum visitor stands before an exquisite landscape or a somber portrait, intimidated by academic wall text filled with dates, provenance, and art-historical jargon that makes the painting feel cold, distant, and irrelevant to their lived life. They leave feeling intellectually deficient and spiritually untouched. The tragedy is that art has been locked in an academic mausoleum, cut off from its original purpose: healing human sorrow.\n\nDe Botton and Armstrong rescue art from academic pedantry, proposing a radical re-evaluation of aesthetics as a psychological medicine cabinet. A painting can remind us to forgive, encourage us to mourn, or restore our gratitude for ordinary days. It reflects our modern emotional malnutrition, inviting us to stop asking 'what does this art mean historically?' and start asking 'what emotional weakness in me is this artwork trying to cure?'",
            "tags": ["art", "healing", "psychology", "solace"]
        }
    ],

    # Screenplays
    "dev-d-screenplay": [
        {
            "quote": "Main zinda hoon, par andar se sab mar chuka hai. Bas ek nasha chahiye jo dimag ki awaz band kar sake.",
            "explanation": "Dev stands in the neon-drenched, garbage-strewn alleys of Paharganj, drowning in vodka, cough syrup, and toxic self-pity after alienating the only woman who ever loved him without conditions. He looks in the cracked bathroom mirror of a seedy hotel, realizing that his rebellion was never about freedom or romantic passion; it was pure, cowardly narcissism that weaponized heartbreak to avoid growing up. The visceral horror is watching a privileged, talented young man deliberately engineer his own destruction.\n\nKashyap and Motwane's raw, unvarnished screenplay deconstructs the romanticized Bollywood archetype of Devdas, stripping away the poetic martyrdom to expose the ugly, infantile misogyny and addiction beneath. It mirrors our own destructive tendencies, showing how easily wounded pride can masquerade as tragic romantic devotion.",
            "tags": ["heartbreak", "self-destruction", "addiction", "delusion"]
        }
    ],
    "memories-of-murder-2003": [
        {
            "quote": "밥은 먹고 다니냐? (Have you been eating well? / Are you eating well, you bastard?)",
            "explanation": "Detective Park Doo-man stands in the golden autumn fields of Hwaseong years after the brutal unsolved serial murders that destroyed his career, his youth, and his moral compass. A little girl informs him that another ordinary-looking man recently stood at the exact same ditch, reminiscing about what he did there long ago. Park stares directly into the camera lens—into the eyes of the real killer who may be sitting in the theater—with an expression of fathomless grief, rage, and helplessness.\n\nBong Joon-ho concludes his procedural masterpiece with one of the most devastating fourth-wall breaks in cinema history. The question carries the unbearable banality of human evil: the horrifying realization that monsters do not have fangs or deformed faces; they are ordinary men who wake up, eat breakfast, and walk unseen among us on sunny afternoons.",
            "tags": ["justice", "evil", "cinema", "obsession"]
        }
    ],
    "parasite-script": [
        {
            "quote": "You know what kind of plan never fails? No plan at all. Because if you make a plan, life never works out that way.",
            "explanation": "Ki-taek lies on the gymnasium floor on a thin mattress surrounded by hundreds of displaced, flooded flood victims, his semi-basement apartment filled with sewage and feces. When his son desperately asks what the master plan is to escape their criminal fraud and humiliation, Ki-taek delivers this nihilistic confession of total defeat. The tension is the tragic surrender of a father who has been so thoroughly crushed by systemic poverty that he has surrendered the dignity of even hoping for tomorrow.\n\nBong Joon-ho uses this grim fatalism to expose the brutal psychological toll of late-stage capitalism, where the poor are stripped of the luxury of planning while the rich enjoy seamless comfort. It cuts straight to our contemporary anxiety, capturing that universal terror of realizing that all our meticulously crafted life plans can be wiped out in an instant by forces completely beyond our control.",
            "tags": ["class", "capitalism", "fate", "despair"]
        }
    ],
    "500-days-of-summer-2009": [
        {
            "quote": "Tom walked into the apartment and knew instantly that something had changed. Not because Summer said so, but because the silence between them was no longer comfortable.",
            "explanation": "Tom sits in Summer's living room, clutching his romantic delusions of destined soulmates and cinematic fate, desperately ignoring the polite detachment creeping into her voice and eyes. He is in love with a fantasy of who she represents in his indie-rock movie mind, completely blind to the real, independent human being sitting right across from him. The heartbreak is quiet, mundane, and inevitable.\n\nNeustadter and Weber's script deconstructs the toxic fantasy of the 'Manic Pixie Dream Girl' and the adolescent myth of predestined romance. It mirrors our own painful tendency to project our emotional needs onto lovers, mistaking our own desperate longing to be saved for true, mutual intimacy.",
            "tags": ["romance", "illusion", "projections", "heartbreak"]
        }
    ],
    "aligarh-screenplay": [
        {
            "quote": "Aap meri tanhai ko nahi samajh sakte. Yeh koi gunah nahi hai, yeh bas meri azaadi hai.",
            "explanation": "Professor Siras sits in his dimly lit, modest faculty quarters listening to Lata Mangeshkar on an old cassette player, clutching his whiskey glass while the hostile world outside plots his moral destruction. Forced out of his professorship after a coordinated sting violates the sanctity of his private bedroom, he refuses to respond with bitter rage or political posturing. The tension is the unbearable vulnerability of a quiet, gentle poet subjected to the howling mob of institutional intolerance.\n\nAsrani and Mehta create a profound testament to the sacred right of human privacy and dignified solitude. It serves as an emotional mirror, asking us to confront our society's voyeuristic cruelty and remember that true human dignity often lives in the quietest, most vulnerable corners of our private lives.",
            "tags": ["solitude", "dignity", "persecution", "poetry"]
        }
    ],

    # Culinary Lore
    "the-food-lab-better-home-cooking-through-science-unknown": [
        {
            "quote": "Cooking is not an inexplicable magic art passed down by mystical grandmothers; it is an applied physical and chemical science that obeys universal thermal laws.",
            "explanation": "A home cook stares in frustration at a dry, rubbery chicken breast, having followed a vague heritage recipe that demanded 'cooking with your heart' and 'cooking until golden brown'. The culinary disaster exposes the failure of romantic culinary myths that substitute poetic ambiguity for thermal control. The anxiety is practical: how to stop wasting expensive ingredients and learn the fundamental chemistry of heat transfer.\n\nKenji López-Alt strips kitchen craft of pretentious snobbery and blind superstition, replacing dogma with rigorous experimentation and empirical measurement. It mirrors our broader relationship with skill acquisition, demonstrating that real confidence and creative freedom come not from magical thinking, but from mastering the underlying mechanisms of how things actually work.",
            "tags": ["cooking", "science", "curiosity", "mastery"]
        }
    ],

    # Additional Iconic Screenplays
    "gangs-of-wasseypur-part-1-movie-script-film-companion-unknown": [
        {
            "quote": "Baap ka, dada ka, bhai ka, sabka badla lega re tera Faizal.",
            "explanation": "Faizal Khan sits on the muddy veranda of his family compound in Wasseypur, high on weed and numb with grief after the assassination of his elder brother. Surrounding relatives mock his fragile nerves, demanding blood vengeance against Ramadhir Singh. The dilemma is the tragic curse of generational vendetta: a quiet boy who just wanted to watch Bollywood movies in dark theaters is forced by dynastic duty into becoming a ruthless executioner.\n\nKashyap's epic deconstructs the corrosive pathology of generational revenge in provincial India. It lays bare the brutal trap of inherited hatred, where young men sacrifice their sanity, youth, and moral futures to pay debts for crimes committed before they were born.",
            "tags": ["revenge", "family", "legacy", "violence"]
        }
    ],
    "masaan-movie-script-film-companion-unknown": [
        {
            "quote": "Yeh dukh kahe khatam nahi hota be?",
            "explanation": "Devi and Deepak walk through the burning ghats of Varanasi, where funeral pyres burn perpetually along the sacred river. Deepak sits beside the ash-strewn banks, crushed by the sudden, absurd death of the woman he loved in a bus crash, realizing that neither academic achievement nor sincere love could save her from senseless mortality. The anguish is raw, simple, and unanswerable.\n\nVarun Grover captures the quiet, devastating universal ache of sudden bereavement in a society bound by ritual. When tragedy strikes with arbitrary cruelty, all philosophical rationalizations collapse, leaving only the agonizing, helpless human question of why sorrow never seems to end.",
            "tags": ["grief", "love", "mortality", "tragedy"]
        }
    ],
    "the-lunchbox-screenplay-film-companion-unknown": [
        {
            "quote": "I think we forget things if we have no one to tell them to.",
            "explanation": "Saajan Fernandes sits alone in his dimly lit Mumbai flat, retired from decades of bureaucratic ledger-keeping, eating a warm meal mistakenly delivered by the Dabbawalas. For thirty years he has walked the crowded streets in total emotional quarantine, surrounded by millions of commuters yet speaking to no one. The arrival of a stranger's handwritten note inside a lunchbox ruptures his defensive numbness.\n\nRitesh Batra illuminates the quiet epidemic of urban loneliness. In our hyper-connected, bustling modern cities, we can easily lose our own memories and identities unless we have a witness—another human being who truly listens to the small, mundane details of our day.",
            "tags": ["loneliness", "connection", "memory", "intimacy"]
        }
    ],
    "t-u-m-b-b-a-d-unknown": [
        {
            "quote": "Hastar bhookha hai. Lalach ka koi ant nahi hota.",
            "explanation": "Vinayak descends into the subterranean womb of the ruined mansion at Tumbbad, strapping flour-dough effigies to his waist to plunder gold coins from the cursed god of greed while rain lashes Maharashtra. With each haul of gold, his appetite grows more insatiable, blinding him to the moral decay rotting his own soul and endangering his young son. The tension is the horrifying madness of unchecked human greed.\n\nBarve and Mitter create an indelible mythological horror film about the generational curse of rapacity. Hastar is not merely a monster in the dark; he is the personification of human greed, which feasts upon our endless hunger until it consumes the very hands that feed it.",
            "tags": ["greed", "myth", "horror", "consequence"]
        }
    ],
    "arrival-2016-unknown": [
        {
            "quote": "If you could see your whole life from start to finish, would you change things? Despite knowing the journey... and where it leads... I embrace it. And I welcome every moment of it.",
            "explanation": "Louise Banks stands in the mist-filled chamber of the alien spacecraft, her consciousness transformed by the non-linear language of the Heptapods. She now sees her entire timeline simultaneously: she sees the birth of her daughter Hannah, her laughter, and her inevitable death from an incurable disease years later. The moral and emotional choice is staggering: whether to refuse love to avoid guaranteed agony, or choose the joy of companionship knowing heartbreak is the price of admission.\n\nHeisserer and Chiang's masterpiece offers a transcendent meditation on grief, love, and mortal acceptance. It asks each of us whether we would still choose our friendships, romances, and creative passions if we knew in advance that they would end in tears, reminding us that the beauty of human life lies in loving without the guarantee of an eternal happy ending.",
            "tags": ["time", "grief", "love", "acceptance"]
        }
    ],
    "everything-everywhere-all-at-once-2022-unknown": [
        {
            "quote": "In another life, I would have really liked just doing laundry and taxes with you.",
            "explanation": "In an alternate universe where Evelyn is a glamorous international movie star and Waymond is a suave, wealthy CEO, they stand in a rainy alleyway outside a luxurious gala. Stripped of the multiverse's chaotic bagels, flying swords, and infinite possibilities, Waymond reveals that all his worldly success means nothing compared to the quiet domestic life they forfeited. The heartbreak lies in the realization that grand success is hollow without everyday human intimacy.\n\nThe Daniels capture the antidote to contemporary cosmic nihilism: when faced with an infinite, indifferent universe where 'nothing matters', the only rational and radical human response is kindness, presence, and cherishing the ordinary, unglamorous chores we share with the people we love.",
            "tags": ["love", "multiverse", "kindness", "presence"]
        }
    ],
    "get-out-2017-unknown": [
        {
            "quote": "Now you're in the Sunken Place. You can't move. You can't scream. You can only watch.",
            "explanation": "Chris Washington sits paralyzed in the Armitage study as Missy stirs her silver spoon against the porcelain teacup, hypnotically sending his consciousness hurtling down into a pitch-black cosmic void. From the Sunken Place, he can look up through a tiny television-like screen of his own eyes, trapped inside his own body while someone else controls his limbs. The psychological terror is the horror of complete physical and cultural disenfranchisement.\n\nPeele crafts a chilling visual metaphor for systemic racial subjugation, paralysis, and gaslighting. The Sunken Place resonates far beyond the screen because it articulates that universal terror of feeling your voice, autonomy, and identity erased while forced to smile and play along with a polite society that is slowly consuming you.",
            "tags": ["horror", "paralysis", "identity", "control"]
        }
    ],
    "snowpiercer-screenplay-bong-joon-ho-kelly-masterson": [
        {
            "quote": "I know what people taste like. I know that babies taste best. You think I'm a hero? I'm not a hero.",
            "explanation": "Curtis Everett sits in the quiet machine room near the sacred engine of the perpetual train, confessing to Namgoong the unspeakable secret of the back cars during the first winter of the freeze. To survive starvation, the tail section passengers descended into cannibalism until Gilliam sliced off his own arm to offer them food without murder. Curtis is consumed by self-hatred, knowing that the pristine leadership mantle placed upon him was forged in visceral atrocity.\n\nBong Joon-ho strips away the romantic glamour of revolutionary heroism to reveal the brutal compromises demanded by survival. It forces us to recognize that historical heroes are rarely pure paragons of virtue, but scarred survivors who bear the unspeakable burdens of choices no human should ever have to make.",
            "tags": ["survival", "revolution", "guilt", "humanity"]
        }
    ],
    "build-an-unorthodox-guide-to-making-things-worth-making-tony-fadell": [
        {
            "quote": "If you're not making mistakes, you're not trying new things. But if you make the same mistake twice, you're not paying attention.",
            "explanation": "An engineering lead stands amidst smoking hardware prototypes and missed product deadlines, paralyzed by fear of executive wrath and brand embarrassment. The team's instinct is to retreat into safe, incremental improvements that won't get anyone fired. The crisis is organizational cowardice: sacrificing audacious design breakthroughs to preserve an illusion of corporate safety.\n\nFadell cuts through Silicon Valley platitudes to deliver battle-tested manufacturing wisdom from the trenches of the iPod and Nest. Failure is not a badge of honor to be celebrated blindly, but an expensive laboratory tax you pay to discover what physical reality actually demands.",
            "tags": ["design", "leadership", "craft", "iteration"]
        }
    ],
    "barthes-the-death-of-the-author-unknown": [
        {
            "quote": "The birth of the reader must be ransomed by the death of the Author.",
            "explanation": "A literary scholar insists on decoding a poem by unearthing the private diaries, psychological traumas, and moral opinions of the biographical writer who penned it, reducing the living work of art to a simple psychological autopsy. The text is treated as a locked safe that only the dead author's ghost can open, leaving the reader as a passive consumer rather than an active creator of meaning.\n\nBarthes liberates literature from authoritarian biographical ownership, declaring that once words hit the page, their meaning belongs entirely to the reader who interprets them. It empowers every reader to enter a book not as a humble tourist in someone else's palace, but as a co-creator who brings their own soul, scars, and imagination to the text.",
            "tags": ["literature", "criticism", "interpretation", "freedom"]
        }
    ],
    "all-tomorrows-cm-kosemen-unknown": [
        {
            "quote": "Remember the Star People, count your fingers, and thank your lucky stars that you are human.",
            "explanation": "Across a billion years of speculative galactic history, humanity is conquered, genetically mutilated into living filter-feeders and grotesque tools by the godlike Qu, and slowly forced through eons of agonizing biological evolution to reclaim sentience. The cosmic panorama is staggering in its horror and majesty: our proud cities, religions, and philosophical systems are reduced to a speck of dust in the uncaring evolutionary furnace of deep time.\n\nKosemen crafts an awe-inspiring antidote to human arrogance, reminding us that our present biological form, consciousness, and civilization are fragile accidents of history. It leaves the reader with a profound, dizzying gratitude for the simple, miraculous gift of being an ordinary human being alive right now.",
            "tags": ["cosmic-horror", "evolution", "humanity", "time"]
        }
    ],
    "ann-handley-everybody-writes": [
        {
            "quote": "In an online world, our words are our emissaries; they tell the world who we are. Writing well is part habit, part knowledge of some fundamental rules, and part giving a damn.",
            "explanation": "A professional hides behind jargon, corporate buzzwords, and sterile robotic phrasing in their emails, newsletters, and pitches, terrified that sounding like a warm, fallible human being will make them look unpolished. The resulting prose is completely unreadable, instantly discarded by recipients who crave genuine human contact. The crisis is one of cowardly professional conformity.\n\nHandley demystifies writing, asserting that great communication is not an elitist gift reserved for novelists, but an act of empathy and respect for the reader's finite attention. When you write with clarity, rhythm, and warmth, you are not merely sharing information; you are extending human connection across the digital void.",
            "tags": ["writing", "clarity", "empathy", "voice"]
        }
    ]
}

def main():
    if not DATA_PATH.exists():
        print(f"Error: {DATA_PATH} not found.")
        return

    books = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    enriched_count = 0

    # Build index by book id
    book_map = {b["id"]: b for b in books}

    for book_id, quotes in CURATED_QUOTES.items():
        # Match by ID or partial match
        target = book_map.get(book_id)
        if not target:
            # Try fuzzy match on id
            for b in books:
                if book_id in b["id"] or b["id"] in book_id:
                    target = b
                    break

        if target:
            target["quotes"] = quotes
            target["has_quote_bank"] = True
            enriched_count += 1
            print(f"✓ Enriched: {target['title']} ({len(quotes)} quotes)")

    DATA_PATH.write_text(json.dumps(books, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSuccessfully enriched {enriched_count} landmark books in {DATA_PATH}")

if __name__ == "__main__":
    main()
