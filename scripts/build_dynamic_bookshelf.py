# scripts/build_dynamic_bookshelf.py — Normalizes, enriches, and compiles the dynamic Google Drive bookshelf and TBR list
# Usage: python3 scripts/build_dynamic_bookshelf.py
# Requires: content/gdrive_books_catalog.json, content/quote-bank.json, content/authors.md
#
# Gotchas:
# - Drives contain inverted filenames ("Author - Title" vs "Title - Author").
# - Multi-issue comics (Watchmen #1..#12, Oyasumi Punpun v1..v13) are grouped into complete series cards.
# - Screenplays have specific authors and directors mapped for clean attribution.
# - Output HTML includes full Tailwind UI, search, tag filters, TBR copy, and recommendation engine.

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "content" / "gdrive_books_catalog.json"
QUOTE_BANK_PATH = ROOT / "content" / "quote-bank.json"

TBR_OUTPUT_PATH = ROOT / "content" / "tbr_clean_list.txt"
SHELF_JSON_PATH = ROOT / "content" / "books_curated_shelf.json"
SHELF_HTML_PROTO = ROOT / "prototype" / "shelf.html"
SHELF_HTML_DOCS = ROOT / "docs" / "shelf.html"

# Precise mappings for filenames that need exact title/author normalization
EXACT_FILE_MAPPINGS = {
    "the-argumentative-indian-amartya.epub": {
        "title": "The Argumentative Indian",
        "author": "Amartya Sen",
        "category": "Philosophy, Essays & Misc",
        "pitch": "Nobel laureate Amartya Sen explores India's millennia-long tradition of rigorous public debate, pluralism, and intellectual skepticism.",
        "why_love": "Dismantles simplistic caricatures of Eastern thought by demonstrating how argument and dissent have always shaped Indian democracy.",
        "tags": ["philosophy", "essays", "history", "intellectual-history"]
    },
    "william_faulkner.epub": {
        "title": "Selected Works & Stories",
        "author": "William Faulkner",
        "category": "Fiction & Non-Fiction",
        "pitch": "The haunting, multi-voiced Southern Gothic tales of Yoknapatawpha County, capturing decay, racial trauma, and the unyielding weight of memory.",
        "why_love": "Faulkner's breathless, streaming sentences and shifting perspectives remain the peak of American modernism.",
        "tags": ["southern-gothic", "modernism", "memory", "american-epic"]
    },
    "alex verus #1 - fated_-_benedict_jacka.epub": {
        "title": "Fated (Alex Verus #1)",
        "author": "Benedict Jacka",
        "category": "Fiction & Non-Fiction",
        "pitch": "In the hidden magical underbelly of London, a probability mage who cannot throw fireballs must survive by seeing every possible immediate future.",
        "why_love": "Fast-paced urban fantasy where strategic cunning and foresight always beat raw brute force.",
        "tags": ["urban-fantasy", "fast-paced", "magic", "london"]
    },
    "how_to_win_at_chess 2 - next_level_-_levy_rozman.epub": {
        "title": "How to Win at Chess 2: Next Level",
        "author": "Levy Rozman (GothamChess)",
        "category": "Philosophy, Essays & Misc",
        "pitch": "Internet chess educator GothamChess breaks down intermediate positional play, pawn structures, and psychological attacking plans.",
        "why_love": "Breezy, humorous, and visual explanations that demystify intermediate board visualization.",
        "tags": ["chess", "strategy", "games", "tactics"]
    },
    "feline-philosophy-john-gray.epub": {
        "title": "Feline Philosophy: Cats and the Meaning of Life",
        "author": "John Gray",
        "category": "Philosophy, Essays & Misc",
        "pitch": "A witty, cutting philosophical critique of human anxiety and self-delusion through the unburdened, contented existence of cats.",
        "why_love": "John Gray strips away existential pretension, contrasting neurotic human philosophies with feline tranquility.",
        "tags": ["philosophy", "existentialism", "animals", "wry-humor"]
    },
    "a-wrinkle-in-time.epub": {
        "title": "A Wrinkle in Time",
        "author": "Madeleine L'Engle",
        "category": "Fiction & Non-Fiction",
        "pitch": "Meg Murry embarks on a cosmic tesseract journey across dimensions to rescue her scientist father from the psychic darkness of IT.",
        "why_love": "A genre-defining children's classic uniting astrophysics, love, and spiritual courage against totalitarian conformity.",
        "tags": ["classic", "sci-fi", "coming-of-age", "fantasy"]
    },
    "the-science-of-logic-[friedrich-hegel].epub": {
        "title": "The Science of Logic",
        "author": "G. W. F. Hegel",
        "category": "Philosophy, Essays & Misc",
        "pitch": "Hegel's masterwork on speculative dialectics: tracing pure thought as it moves through Being, Essence, and the Notion.",
        "why_love": "The foundational bedrock of 19th and 20th-century continental philosophy and dialectical materialism.",
        "tags": ["philosophy", "dialectics", "german-idealism", "deep-thought"]
    },
    "an-outline-of-philosophy-[ted-tripp].epub": {
        "title": "An Outline of Philosophy",
        "author": "Bertrand Russell & Ted Tripp",
        "category": "Philosophy, Essays & Misc",
        "pitch": "A lucid, analytical survey tracing epistemology, language, mind, and the physical universe from a naturalist standpoint.",
        "why_love": "Uncompromising clarity and British analytical rigor tackling life's grandest questions without jargon.",
        "tags": ["philosophy", "epistemology", "primer"]
    },
    "commodify-your-dissent-[thomas-frank].epub": {
        "title": "Commodify Your Dissent",
        "author": "Thomas Frank & Matt Weiland (eds.)",
        "category": "Philosophy, Essays & Misc",
        "pitch": "Incendiary essays from The Baffler exposing how American corporate advertising co-opted rebellion and counterculture into marketing fodder.",
        "why_love": "Ferocious cultural critique that anticipated the modern Silicon Valley commodification of rebellion.",
        "tags": ["media-critique", "counterculture", "advertising", "satire"]
    },
    "what-is-dialectical-materialism-a-study-guide-[rob-sewell].mobi": {
        "title": "What Is Dialectical Materialism? A Study Guide",
        "author": "Rob Sewell & Alan Woods",
        "category": "Philosophy, Essays & Misc",
        "pitch": "A concise introductory guide explaining the Marxist philosophy of change, contradiction, and historical development.",
        "why_love": "Clear, direct breakdown of philosophical materialism vs idealism for political students.",
        "tags": ["philosophy", "marxism", "politics", "study-guide"]
    },
    "zizek's-jokes-[slavoj-zizek].epub": {
        "title": "Žižek's Jokes: (Did You Hear the One about Hegel and Negation?)",
        "author": "Slavoj Žižek",
        "category": "Philosophy, Essays & Misc",
        "pitch": "A hilarious compendium of dirty Soviet jokes, obscene riddles, and Jewish humor used to explain Lacan, Hegel, and contemporary ideology.",
        "why_love": "Classic Žižek: using low-brow humor to unlock profound post-modern philosophical truths.",
        "tags": ["philosophy", "humor", "ideology", "lacan"]
    },
    "socialism-utopian-and-scientific-[frederick-engels].epub": {
        "title": "Socialism: Utopian and Scientific",
        "author": "Friedrich Engels",
        "category": "Philosophy, Essays & Misc",
        "pitch": "Engels traces the historical evolution of socialist thought from the moral dreams of French utopians to historical materialism.",
        "why_love": "One of the most accessible and influential political pamphlets in world history.",
        "tags": ["politics", "history", "economics", "classic"]
    },
    "qntm-there-is-no-antimemetics-di.epub": {
        "title": "There Is No Antimemetics Division",
        "author": "qntm (Sam Hughes)",
        "category": "Fiction & Non-Fiction",
        "pitch": "How do you fight an enemy that erases itself from your memory the instant you look at it? A brilliant thriller set in the SCP Foundation universe.",
        "why_love": "An astonishingly original concept executed with relentless suspense and cerebral mind-benders.",
        "tags": ["sci-fi", "horror", "mind-bending", "unputdownable"]
    },
    "how to research anything.epub": {
        "title": "How to Research Anything",
        "author": "Nat Eliason",
        "category": "Philosophy, Essays & Misc",
        "pitch": "A pragmatic operating system for deconstructing new domains, finding primary sources, and synthesizing complex knowledge fast.",
        "why_love": "Actionable frameworks for curious autodidacts and researchers.",
        "tags": ["research", "learning", "productivity", "frameworks"]
    },
    "lessons-in-stoicism-john-sellers (1).epub": {
        "title": "Lessons in Stoicism",
        "author": "John Sellars",
        "category": "Philosophy, Essays & Misc",
        "pitch": "A short, elegant distillation of Seneca, Epictetus, and Marcus Aurelius on controlling emotions, facing adversity, and living calmly.",
        "why_love": "Stripped of pop-self-help fluff; pure ancient philosophical therapy in under 100 pages.",
        "tags": ["stoicism", "philosophy", "ancient-wisdom", "mental-clarity"]
    },
    "sophies-world-a-novel-about-the (1).epub": {
        "title": "Sophie's World",
        "author": "Jostein Gaarder",
        "category": "Fiction & Non-Fiction",
        "pitch": "A 14-year-old Norwegian girl begins receiving mysterious letters from an anonymous philosopher, plunging into a meta-fictional history of Western thought.",
        "why_love": "A worldwide bestseller that turns 2,500 years of philosophy into an irresistible mystery novel.",
        "tags": ["philosophy", "coming-of-age", "mystery", "metafiction"]
    },
    "the-tao-te-ching-translated-by-g.epub": {
        "title": "Tao Te Ching",
        "author": "Lao Tzu (trans. Gia-Fu Feng & Jane English)",
        "category": "Philosophy, Essays & Misc",
        "pitch": "Eighty-one poetic chapters on the paradoxical power of non-action (wu wei), water-like flexibility, and harmony with nature.",
        "why_love": "The definitive English poetic translation; timeless sentences that re-center a distracted mind.",
        "tags": ["eastern-philosophy", "poetry", "taoism", "meditative"]
    },
    "good-stories-on-ai-and-future-ke.epub": {
        "title": "Good Stories on AI and the Future",
        "author": "Kevin Kelly",
        "category": "Philosophy, Essays & Misc",
        "pitch": "Wired co-founder Kevin Kelly outlines optimistic, proactive scenarios for humanity co-evolving alongside artificial intelligence.",
        "why_love": "A refreshingly expansive, non-apocalyptic antidote to prevailing tech pessimism.",
        "tags": ["technology", "ai", "futures", "optimism"]
    },
    "david-allen-getting-things-done.epub": {
        "title": "Getting Things Done: The Art of Stress-Free Productivity",
        "author": "David Allen",
        "category": "Marketing & Strategy",
        "pitch": "The legendary methodology for externalizing mental loops into trusted capture systems and clearing cognitive RAM.",
        "why_love": "The gold-standard productivity architecture that freed millions from executive overwhelm.",
        "tags": ["productivity", "systems", "mental-clarity", "focus"]
    },
    "no-more-mr-nice-guy-robert-glove.epub": {
        "title": "No More Mr. Nice Guy",
        "author": "Dr. Robert A. Glover",
        "category": "Philosophy, Essays & Misc",
        "pitch": "A clinical examination of covert contracts, passive-aggression, and fear of conflict, showing how to reclaim healthy assertiveness.",
        "why_love": "Direct, empathetic diagnosis of people-pleasing traps and boundary enforcement.",
        "tags": ["psychology", "boundaries", "relationships", "self-honesty"]
    },
    "the-great-business-reformation-h.epub": {
        "title": "The Great Business Reformation",
        "author": "H. W. Charles",
        "category": "Marketing & Strategy",
        "pitch": "A critical manifesto detailing how customer expectations and decentralized technology are forcing corporate institutions to reinvent themselves.",
        "why_love": "Sharply observed business strategy on agility and brand trust.",
        "tags": ["business-strategy", "innovation", "brand"]
    },
    "the-new-control-society-by-jon-a.epub": {
        "title": "The New Control Society",
        "author": "Jon Agar",
        "category": "Philosophy, Essays & Misc",
        "pitch": "Historical examination of government surveillance, digital databases, and administrative identity registers since WWII.",
        "why_love": "Scholarly, fascinating look at how bureaucratic data collection morphed into total digital oversight.",
        "tags": ["surveillance", "technology", "privacy", "history"]
    },
    "japans-historical-arc-from-feuda.epub": {
        "title": "Japan's Historical Arc: From Feudalism to Modernity",
        "author": "Mikiso Hane",
        "category": "Philosophy, Essays & Misc",
        "pitch": "A vivid historical chronicle detailing Japan's rapid leap from isolated Tokugawa shogunate to industrial world empire.",
        "why_love": "Focuses on the ordinary peasants, factory workers, and women who bore the human cost of rapid modernization.",
        "tags": ["japanese-history", "culture", "asia", "modernization"]
    },
    "ray-dalio-principles.epub": {
        "title": "Principles: Life and Work",
        "author": "Ray Dalio",
        "category": "Marketing & Strategy",
        "pitch": "Billionaire hedge fund founder Ray Dalio shares his systematic operating rules for radical truth, radical transparency, and machine-like execution.",
        "why_love": "An engineering mindset applied to organizational psychology and decision-making under uncertainty.",
        "tags": ["decision-making", "systems", "leadership", "principles"]
    },
    "all tomorrows cm kosemen .pdf": {
        "title": "All Tomorrows: A Billion Year Chronicle of the Post-Humans",
        "author": "C. M. Kôsemen (Nemo Ramjet)",
        "category": "Fiction & Non-Fiction",
        "pitch": "A chilling billion-year speculative chronicle tracing human descendants bio-engineered into grotesque alien forms by an enigmatic god-like race.",
        "why_love": "One of the most haunting, deeply imaginative works of cosmic body-horror and perseverance ever conceived.",
        "tags": ["cosmic-horror", "speculative-evolution", "sci-fi", "unforgettable"]
    },
    "the ones who walk away from omelas.pdf": {
        "title": "The Ones Who Walk Away from Omelas",
        "author": "Ursula K. Le Guin",
        "category": "Fiction & Non-Fiction",
        "pitch": "A utopian festival city whose boundless splendor and joy depends entirely on the perpetual, locked-room torment of a single innocent child.",
        "why_love": "Le Guin's devastating philosophical parable questioning utilitarian ethics and the price of social happiness.",
        "tags": ["philosophical-fiction", "parable", "ethics", "classic"]
    },
    "freakonomics.pdf": {
        "title": "Freakonomics: A Rogue Economist Explores the Hidden Side of Everything",
        "author": "Steven D. Levitt & Stephen J. Dubner",
        "category": "Philosophy, Essays & Misc",
        "pitch": "Economist Steven Levitt uses statistical correlations and behavioral incentives to investigate sumo wrestling, cheating teachers, and crime drops.",
        "why_love": "Delightfully counterintuitive data storytelling that changed popular non-fiction forever.",
        "tags": ["economics", "incentives", "psychology", "surprising-insights"]
    },
    "hbr on persuasive presentations.pdf": {
        "title": "HBR Guide to Persuasive Presentations",
        "author": "Nancy Duarte",
        "category": "Marketing & Strategy",
        "pitch": "Presentation expert Nancy Duarte shows how to structure executive pitches like dramatic hero journeys with contrast and emotional resonance.",
        "why_love": "Eliminates slide-deck clutter and teaches how to move cynical stakeholders to action.",
        "tags": ["presentations", "storytelling", "persuasion", "communication"]
    },
    "hbr on communication": {
        "title": "HBR's 10 Must Reads on Communication",
        "author": "Harvard Business Review",
        "category": "Marketing & Strategy",
        "pitch": "The definitive collection of executive essays on persuasive rhetoric, difficult conversations, and managing narrative.",
        "why_love": "Essential business strategy articles on the science of why arguments convince people.",
        "tags": ["communication", "leadership", "rhetoric", "management"]
    },
    "어린왕자.pdf": {
        "title": "The Little Prince (어린 왕자 - Korean Edition)",
        "author": "Antoine de Saint-Exupéry",
        "category": "Fiction & Non-Fiction",
        "pitch": "A stranded desert aviator encounters a boy prince from Asteroid B-612 who tends roses and tames foxes.",
        "why_love": "A poetic, tender masterpiece reminding adults that what is essential is invisible to the eye.",
        "tags": ["classic", "fable", "korean-language", "heartfelt"]
    },
    "barthes-the-death-of-the-author.pdf": {
        "title": "The Death of the Author",
        "author": "Roland Barthes",
        "category": "Philosophy, Essays & Misc",
        "pitch": "The landmark literary essay arguing that a text's true birth happens in the mind of the reader, not the biography of the author.",
        "why_love": "Shattered traditional literary criticism and opened modern subjective interpretation.",
        "tags": ["literary-theory", "philosophy", "essays", "foundational"]
    },
    "intercom on jobs to be done.pdf": {
        "title": "Intercom on Jobs to be Done",
        "author": "Des Traynor & Intercom Team",
        "category": "Marketing & Strategy",
        "pitch": "A practical product guide to Clay Christensen's Jobs-to-be-Done framework: discovering why customers actually 'hire' your software.",
        "why_love": "Cuts through vanity feature roadmaps to focus on real customer struggle.",
        "tags": ["product-management", "jobs-to-be-done", "saas", "user-research"]
    },
    "the-dream-of-a-ridiculous-man-fi.epub": {
        "title": "The Dream of a Ridiculous Man",
        "author": "Fyodor Dostoevsky",
        "category": "Fiction & Non-Fiction",
        "pitch": "A suicidal man falls asleep with a revolver and dreams he is transported to an uncorrupted, paradise version of Earth.",
        "why_love": "One of Dostoevsky's most visionary, emotionally intense short parables on human sin and redemption.",
        "tags": ["dostoevsky", "existentialism", "short-story", "philosophical-depth"]
    },
    "what the fortune 500 read.pdf": {
        "title": "What the Fortune 500 Read",
        "author": "Alan Scharf",
        "category": "Marketing & Strategy",
        "pitch": "A curated compendium dissecting the executive reading habits, foundational books, and mental models of elite corporate leaders.",
        "why_love": "High-signal filter on which business and management books genuinely endure.",
        "tags": ["reading-lists", "business", "executive-mindset"]
    },
    "worldclasspricingthejourney.pdf": {
        "title": "World Class Pricing: The Journey",
        "author": "Paul Hunt & Jim Saunders",
        "category": "Marketing & Strategy",
        "pitch": "A strategic playbook for B2B enterprises to transition from cost-plus pricing to value-based pricing architectures.",
        "why_love": "Demystifies the most potent yet neglected profit lever in business.",
        "tags": ["pricing", "b2b", "revenue", "strategy"]
    },
    "the art of seo.pdf": {
        "title": "The Art of SEO: Mastering Search Engine Optimization",
        "author": "Eric Enge, Stephan Spencer & Jessie Stricchiola",
        "category": "Marketing & Strategy",
        "pitch": "The authoritative industry encyclopedia on algorithmic search, crawl architecture, content strategy, and link authority.",
        "why_love": "Comprehensive, technical, and grounded in search engine reality.",
        "tags": ["seo", "digital-marketing", "technical-search", "strategy"]
    },
    "cinematography theory and practice.pdf": {
        "title": "Cinematography: Theory and Practice",
        "author": "Blain Brown",
        "category": "Cinema & Film Craft",
        "pitch": "An exhaustive, visual masterclass in camera movement, lighting aesthetics, visual composition, and cinematic visual language.",
        "why_love": "The standard university textbook that teaches how to translate written emotion into camera choreography.",
        "tags": ["cinematography", "film-craft", "visual-storytelling", "directing"]
    },
    "directing actors.pdf": {
        "title": "Directing Actors: Creating Memorable Performances for Film & Television",
        "author": "Judith Weston",
        "category": "Cinema & Film Craft",
        "pitch": "The industry's most acclaimed guide for directors on how to communicate with actors using active verbs and subtext rather than 'result directing'.",
        "why_love": "Crucial reading for both filmmakers and writers seeking genuine human behavior in their dialogue.",
        "tags": ["directing", "acting", "subtext", "film-craft"]
    }
}

SWAPPED_AUTHOR_TITLES = {
    "andy weir": ("Project Hail Mary", "Andy Weir"),
    "ann handley": ("Everybody Writes: Your Go-To Guide to Creating Ridiculously Good Content", "Ann Handley"),
    "blake crouch": ("Dark Matter", "Blake Crouch"),
    "dan nelken": ("A Self-Help Guide for Copywriters", "Dan Nelken"),
    "dave gerhardt": ("Founder Brand: Turn Your Story Into Your Competitive Advantage", "Dave Gerhardt"),
    "eli schwartz": ("Product-Led SEO", "Eli Schwartz"),
    "jordan belfort": ("Way of the Wolf: Straight Line Selling", "Jordan Belfort"),
    "justin welsh": ("The LinkedIn Engagement Routine & Content Operating System", "Justin Welsh"),
    "matt barker": ("72 Viral LinkedIn Post Breakdown", "Matt Barker"),
    "neil french": ("The Neil French Collection: Master Copywriting & Advertising", "Neil French"),
    "rory sutherland": ("Alchemy: The Dark Art and Curious Science of Creating Magic in Brands", "Rory Sutherland"),
    "sabri suby": ("Sell Like Crazy: How to Get As Many Clients and Sales As You Can Possibly Handle", "Sabri Suby"),
    "seth godin": ("Permission Marketing / All Marketers Are Liars", "Seth Godin"),
    "stephen fox": ("The Mirror Makers: A History of American Advertising and Its Creators", "Stephen Fox"),
    "tiago amaral": ("The 6 Rules of Fiction", "Tiago Amaral"),
    "wynter / peep laja": ("9 Tips for Your Messaging Strategy", "Peep Laja (Wynter)")
}

KNOWN_SCREENPLAYS = {
    "arrival": ("Arrival (Screenplay)", "Eric Heisserer (dir. Denis Villeneuve)", "2016", ["sci-fi", "linguistics", "nonlinear-time", "grief"]),
    "the-martian": ("The Martian (Screenplay)", "Drew Goddard (dir. Ridley Scott)", "2015", ["survival", "problem-solving", "optimism", "science"]),
    "groundhogday": ("Groundhog Day (Screenplay)", "Danny Rubin & Harold Ramis", "1993", ["existential-comedy", "time-loop", "redemption", "classic"]),
    "올드보이": ("Oldboy (Screenplay)", "Park Chan-wook & Hwang Jo-yun", "2003", ["revenge", "neo-noir", "tragedy", "visceral"]),
    "jojo-rabbit": ("Jojo Rabbit (Screenplay)", "Taika Waititi", "2019", ["satire", "wwii", "loss-of-innocence", "heartfelt"]),
    "500-days-of-summer": ("(500) Days of Summer (Screenplay)", "Scott Neustadter & Michael H. Weber", "2009", ["romance-deconstruction", "nonlinear", "memory", "humor"]),
    "get-out": ("Get Out (Screenplay)", "Jordan Peele", "2017", ["social-horror", "paranoia", "tight-pacing", "satire"]),
    "logan": ("Logan (Screenplay)", "Scott Frank, James Mangold & Michael Green", "2017", ["neo-western", "mortality", "redemption", "gritty"]),
    "everything-everywhere-all-at-once": ("Everything Everywhere All at Once (Screenplay)", "Daniel Kwan & Daniel Scheinert", "2022", ["multiverse", "absurdism", "existential-nihilism", "family"]),
    "american-fiction": ("American Fiction (Screenplay)", "Cord Jefferson", "2023", ["literary-satire", "identity", "family-grief", "wit"])
}

SPECIAL_CLEANUPS = {
    "damianthefatass": ("Cookbook of Gains", "Damian", "Cooking & Food", "High-protein, fitness-focused comfort recipes engineered for simple, consistent meal prep.", "Zero fluff, muscle-building fuel with actual taste."),
    "the book of ramen": ("The Book of Ramen", "Ramen Lords & Community", "Cooking & Food", "An exhaustive, obsessive guide to mastering authentic regional Japanese ramen broths, noodles, and tare at home.", "Unlocks the exact food chemistry behind legendary tonkotsu and shoyu bowls."),
    "the food lab better home cooking through science": ("The Food Lab: Better Home Cooking Through Science", "J. Kenji López-Alt", "Cooking & Food", "The culinary Bible breaking down every fundamental cooking technique using rigorous empirical food science.", "Turns cooking from superstitious guesswork into reproducible culinary perfection."),
    "maangchi's real korean cooking": ("Maangchi's Real Korean Cooking", "Maangchi (Emily Kim)", "Cooking & Food", "Authentic, vibrant homestyle Korean cuisine directly from the internet's most beloved Korean cooking mother.", "Foolproof recipes for kimchi, bulgogi, stews, and side dishes."),
    "the 4 hour chef": ("The 4-Hour Chef", "Tim Ferriss", "Cooking & Food", "A meta-learning blueprint disguised as a culinary journey, teaching rapid skill acquisition through cooking.", "Wildly entertaining masterclass on accelerated learning frameworks."),
    "akira": ("Akira (Complete)", "Katsuhiro Otomo", "Comics & Graphic Novels", "The monumental cyberpunk manga epic detailing psychic warfare, societal collapse, and motorcycle gangs in Neo-Tokyo.", "Pioneered modern cinematic manga storytelling and visceral kinetic action."),
    "the sandman complete": ("The Sandman (Complete Collection)", "Neil Gaiman", "Comics & Graphic Novels", "The legendary dark fantasy saga of Morpheus, the Lord of Dreams, weaving world mythology, history, and literature.", "Widely regarded as the single greatest literary comic book series ever written."),
    "the argumentative indian": ("The Argumentative Indian", "Amartya Sen", "Philosophy, Essays & Misc", "Nobel laureate Amartya Sen's classic essays on India's rich history of public debate, secularism, and pluralism.", "Demolishes narrow stereotypes with centuries of intellectual and philosophical tradition."),
    "influence": ("Influence: The Psychology of Persuasion", "Robert Cialdini", "Marketing & Strategy", "The seminal psychological study of the six universal principles of ethical and unyielding persuasion.", "The undisputed foundation stone of all modern marketing, sales, and behavioral economics."),
    "feline philosophy": ("Feline Philosophy: Cats and the Meaning of Life", "John Gray", "Philosophy, Essays & Misc", "A sharp philosophical critique of human anxiety and self-delusion through the quiet, contented nature of cats.", "Stripping away human hubris with witty, incisive philosophical clarity."),
    "letters to milena": ("Letters to Milena", "Franz Kafka", "Fiction & Non-Fiction", "Kafka's raw, agonizingly intimate epistolary relationship with the brilliant translator Milena Jesenská.", "One of literature's most vulnerable chronicles of nervous, obsessive romantic longing."),
    "style an anti textbook": ("Style: An Anti-Textbook", "Richard Lanham", "Cinema & Film Craft", "A playful, fierce rejection of stuffy bureaucratic prose in favor of vocal rhythm, drama, and rhetorical panache.", "Restores fun and muscular vitality to written English sentences."),
    "sculpting in time": ("Sculpting in Time", "Andrei Tarkovsky", "Cinema & Film Craft", "The master filmmaker's profound meditation on cinema as a direct imprint of lived human time.", "The ultimate sacred text for filmmakers seeking spiritual and artistic integrity."),
    "into the woods": ("Into the Woods: How Stories Work and Why We Tell Them", "John Yorke", "Cinema & Film Craft", "An architectural deep dive into universal five-act storytelling structure across theater, cinema, and literature.", "The single best structural breakdown of narrative psychology ever written."),
    "in the blink of an eye": ("In the Blink of an Eye: A Perspective on Film Editing", "Walter Murch", "Cinema & Film Craft", "Legendary editor/sound designer Walter Murch reveals how film editing reflects human consciousness.", "A timeless, poetic craft book on pacing, cuts, and the psychology of vision."),
    "save the cat": ("Save the Cat! The Last Book on Screenwriting", "Blake Snyder", "Cinema & Film Craft", "The legendary, punchy Hollywood screenwriting handbook with the famous 15-beat beat sheet.", "Essential blueprint for understanding commercial pacing and audience momentum."),
    "the death of the author": ("The Death of the Author", "Roland Barthes", "Philosophy, Essays & Misc", "The revolutionary post-structuralist essay severing a text's meaning from its creator's intent.", "The bedrock of modern literary criticism and open interpretation."),
    "the 22 immutable laws of branding": ("The 22 Immutable Laws of Branding", "Al Ries & Laura Ries", "Marketing & Strategy", "The battle-tested laws of category ownership, contraction, and singular focus.", "Brutally concise rules that prevent businesses from self-sabotaging their identity."),
    "permission marketing": ("Permission Marketing", "Seth Godin", "Marketing & Strategy", "The paradigm shift from interruptive spam to turning strangers into friends and friends into customers.", "The foundational doctrine of modern respect-based digital marketing."),
    "$100m offers": ("$100M Offers: How To Make Offers So Good People Feel Stupid Saying No", "Alex Hormozi", "Marketing & Strategy", "A ruthlessly practical, mathematically sound guide to creating irresistible value propositions.", "Zero-nonsense operational guide that simplifies pricing and pricing psychology.")
}

def clean_title_author(raw_title, raw_author, filename):
    fn_lower = filename.lower()
    
    # Check exact filename mapping
    for exact_k, data in EXACT_FILE_MAPPINGS.items():
        if exact_k in fn_lower:
            return data["title"], data["author"], data["category"], data["pitch"], data["why_love"], data["tags"]
            
    # Check swapped patterns
    for auth_k, (true_title, true_author) in SWAPPED_AUTHOR_TITLES.items():
        if auth_k in raw_title.lower() or auth_k in raw_author.lower():
            return true_title, true_author, None, None, None, None
            
    return raw_title, raw_author, None, None, None, None

def normalize_all():
    with open(CATALOG_PATH) as f:
        gbooks = json.load(f)
        
    qb_index = {}
    if QUOTE_BANK_PATH.exists():
        with open(QUOTE_BANK_PATH) as f:
            qb_data = json.load(f)
        for q in qb_data:
            work = (q.get("work") or "").strip().lower()
            if not work:
                continue
            if work not in qb_index:
                qb_index[work] = {
                    "author": q.get("author"),
                    "work": q.get("work"),
                    "tags": set(),
                    "quotes": []
                }
            qb_index[work]["tags"].update(q.get("tags", []))
            qb_index[work]["quotes"].append({
                "quote": q.get("quote"),
                "explanation": q.get("explanation")
            })

    shelf = []
    seen_keys = set()
    tbr_dict = {}

    for item in gbooks:
        fn = item["filename"]
        fn_lower = fn.lower()
        cat = item["category"]
        fmt = item["format"].upper()
        drive_path = item["drive_path"]
        
        # Collapse multi-issue series
        if "watchmen" in fn_lower and ("00" in fn_lower or "01" in fn_lower):
            if "watchmen_all" in seen_keys:
                continue
            seen_keys.add("watchmen_all")
            shelf.append({
                "title": "Watchmen (Complete Series)",
                "author": "Alan Moore & Dave Gibbons",
                "category": "Comics & Graphic Novels",
                "format": "CBR",
                "pitch": "The monumental superhero deconstruction set against the ticking clock of nuclear armageddon. Rorschach investigates the murder of a former masked vigilante, uncovering a cosmic conspiracy.",
                "why_love": "Redefined what comic art could achieve; a dense, nine-panel grid masterpiece of political dread and flawed human gods.",
                "tags": ["graphic-novel", "superhero-deconstruction", "cold-war", "classic", "dark"],
                "drive_path": drive_path,
                "filename": fn,
                "has_quote_bank": False,
                "quotes": []
            })
            tbr_dict["Watchmen (Complete Series)"] = "Alan Moore & Dave Gibbons"
            continue

        if "oyasumi punpun" in fn_lower:
            if "punpun_all" in seen_keys:
                continue
            seen_keys.add("punpun_all")
            shelf.append({
                "title": "Goodnight Punpun (Oyasumi Punpun - Complete Series)",
                "author": "Inio Asano",
                "category": "Comics & Graphic Novels",
                "format": "PDF",
                "pitch": "A coming-of-age psychological masterpiece depicting Punpun Onodera, an innocent child drawn as a simple bird caricature navigating parental domestic abuse, crippling depression, and turbulent young adulthood.",
                "why_love": "Universally acclaimed for its raw, unfiltered vulnerability and devastatingly photorealistic backgrounds.",
                "tags": ["manga", "coming-of-age", "psychological", "raw-honesty", "dark"],
                "drive_path": drive_path,
                "filename": fn,
                "has_quote_bank": False,
                "quotes": []
            })
            tbr_dict["Goodnight Punpun (Complete Series)"] = "Inio Asano"
            continue

        # Check clean title author mappings
        t, a, c, p, w, tg = clean_title_author(item["title"], item["author"], fn)
        if c:
            cat = c
        
        # Check special cleanups
        for sk, (stitle, sauthor, scat, spitch, swhy) in SPECIAL_CLEANUPS.items():
            if sk in fn_lower:
                t, a, cat, p, w = stitle, sauthor, scat, spitch, swhy
                tg = [scat.lower().replace(" & ", "-"), "essential"]
                break
                
        # Check screenplays
        if cat == "Screenplays" or "screenplay" in fn_lower:
            for spk, (spt, spa, spyear, sptags) in KNOWN_SCREENPLAYS.items():
                if spk in fn_lower:
                    t, a = spt, spa
                    p = f"Original production screenplay from {spyear}. A pristine masterclass in scene geometry, pacing, and visual description."
                    w = "Essential reading for screenwriters and novelists studying story architecture and subtext."
                    tg = sptags + ["screenplay", "cinema"]
                    cat = "Screenplays"
                    break

        # Check graphic guides
        if "graphic guide" in cat.lower() or "introducing" in fn_lower:
            cat = "Graphic Guides"
            if not p:
                subject = t.replace("Introducing", "").strip()
                p = f"An accessible, illustrated comic-format primer deconstructing {subject} from fundamental origins to modern impact."
                w = "Visual mnemonic illustrations paired with high-density intellectual history."
                tg = ["graphic-guide", "illustrated", "primer"]

        # Check quote bank cross reference
        qb_match = None
        t_low = t.lower()
        for qwork, qdata in qb_index.items():
            if qwork == t_low or (len(qwork) > 4 and qwork in t_low) or (len(t_low) > 4 and t_low in qwork):
                qb_match = qdata
                break
                
        quotes = []
        has_qb = False
        if qb_match:
            has_qb = True
            t = qb_match["work"]
            a = qb_match["author"]
            quotes = qb_match["quotes"][:3]
            tags = list(qb_match["tags"])
            if not p:
                sample_exp = quotes[0]["explanation"] if quotes else ""
                first_p = sample_exp.split("\n\n")[0] if sample_exp else ""
                p = first_p[:320] + "..." if len(first_p) > 320 else first_p
            if not w:
                w = "Celebrated for its striking prose rhythm, emotional clarity, and unforgettable cold-reader scenes."
            tg = tags + [cat.lower().replace(" & ", "-")]

        if not p:
            p = f"A notable work in {cat} by {a} exploring key themes, human observation, and perspective."
        if not w:
            w = "Widely admired for its sharp insight, distinct narrative voice, and enduring ideas."
        if not tg:
            tg = [cat.lower().replace(" & ", "-")]

        # Deduplicate entry by (title, author)
        key = (t.lower().strip(), a.lower().strip())
        if key in seen_keys:
            continue
        seen_keys.add(key)
        
        shelf.append({
            "title": t,
            "author": a,
            "category": cat,
            "format": fmt,
            "pitch": p,
            "why_love": w,
            "tags": tg,
            "drive_path": drive_path,
            "filename": fn,
            "has_quote_bank": has_qb,
            "quotes": quotes
        })
        
        tbr_dict[t] = a

    # Sort shelf and TBR
    shelf.sort(key=lambda x: (x["category"], x["title"]))
    tbr_clean_lines = [f"{t} — {a}" for t, a in sorted(tbr_dict.items(), key=lambda x: x[0].lower())]

    print(f"Processed {len(shelf)} unique books for shelf.")
    print(f"Generated {len(tbr_clean_lines)} unique clean TBR items.")

    # Save data
    SHELF_JSON_PATH.write_text(json.dumps(shelf, indent=2, ensure_ascii=False), encoding="utf-8")
    TBR_OUTPUT_PATH.write_text("\n".join(tbr_clean_lines), encoding="utf-8")
    print(f"Saved: {SHELF_JSON_PATH}")
    print(f"Saved: {TBR_OUTPUT_PATH}")

    # Build HTML app
    build_html_app(shelf, tbr_clean_lines)

def build_html_app(shelf, tbr_lines):
    shelf_json = json.dumps(shelf, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Personal Library & Dynamic Reading Shelf</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    :root {{
      --background: #0f141c;
      --card: #181f2c;
      --card-hover: #1f2838;
      --border: #2a3447;
      --foreground: #f1f5f9;
      --muted-foreground: #94a3b8;
      --accent: #38bdf8;
      --accent-hover: #0ea5e9;
      --pill-bg: #222d3f;
    }}
    .light {{
      --background: #f8fafc;
      --card: #ffffff;
      --card-hover: #f1f5f9;
      --border: #e2e8f0;
      --foreground: #0f172a;
      --muted-foreground: #64748b;
      --accent: #0284c7;
      --accent-hover: #0369a1;
      --pill-bg: #e2e8f0;
    }}
    body {{
      background-color: var(--background);
      color: var(--foreground);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    .line-clamp-3 {{
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    .line-clamp-2 {{
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
  </style>
</head>
<body class="min-h-screen p-4 md:p-8">
  <div class="max-w-7xl mx-auto">
    <!-- Header -->
    <header class="flex flex-col md:flex-row md:items-center justify-between pb-6 mb-8 border-b border-[var(--border)] gap-4">
      <div>
        <div class="flex items-center gap-3">
          <span class="text-3xl">📚</span>
          <h1 class="text-2xl md:text-3xl font-bold tracking-tight text-[var(--foreground)]">My Drive Library & Dynamic Shelf</h1>
        </div>
        <p class="text-[var(--muted-foreground)] text-sm mt-1">
          {len(shelf)} indexed volumes & screenplays • Back-cover pitches • Why readers love each work • Instant TBR exporter
        </p>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="openRecommender()" class="px-4 py-2 bg-[var(--accent)] hover:bg-[var(--accent-hover)] text-white text-sm font-semibold rounded-lg shadow transition flex items-center gap-2">
          <span>✨</span>
          <span>What to Read Next?</span>
        </button>
        <button onclick="copyAllTbr()" class="px-4 py-2 bg-[var(--card)] hover:bg-[var(--border)] border border-[var(--border)] text-[var(--foreground)] text-sm font-medium rounded-lg transition flex items-center gap-2">
          <span>📋</span>
          <span id="copyAllBtnText">Copy TBR ({len(tbr_lines)})</span>
        </button>
      </div>
    </header>

    <!-- Controls / Filters -->
    <div class="bg-[var(--card)] border border-[var(--border)] rounded-xl p-4 md:p-5 mb-8 shadow-sm">
      <div class="flex flex-col md:flex-row gap-4 items-center justify-between mb-4">
        <!-- Search Input -->
        <div class="relative w-full md:w-96">
          <input 
            type="text" 
            id="searchInput" 
            oninput="renderShelf()"
            placeholder="Search title, author, keyword, or mood..." 
            class="w-full pl-10 pr-4 py-2 bg-[var(--background)] border border-[var(--border)] rounded-lg text-sm text-[var(--foreground)] placeholder-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
          />
          <span class="absolute left-3 top-2.5 text-[var(--muted-foreground)] text-sm">🔍</span>
        </div>

        <!-- Quick filter toggle -->
        <div class="flex items-center gap-4 w-full md:w-auto justify-between md:justify-end">
          <label class="flex items-center gap-2 text-sm text-[var(--muted-foreground)] cursor-pointer select-none">
            <input type="checkbox" id="quoteBankOnly" onchange="renderShelf()" class="rounded border-[var(--border)] accent-[var(--accent)] w-4 h-4" />
            <span>Has Marginalia Quotes Only</span>
          </label>
          <span id="itemCount" class="text-xs font-semibold px-2.5 py-1 bg-[var(--pill-bg)] rounded-full text-[var(--muted-foreground)]">
            Showing {len(shelf)}
          </span>
        </div>
      </div>

      <!-- Category Filter Pills -->
      <div class="flex flex-wrap gap-2 pt-2 border-t border-[var(--border)]" id="categoryPills">
        <!-- dynamically populated -->
      </div>
    </div>

    <!-- Book Grid -->
    <div id="booksGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- dynamically populated -->
    </div>
  </div>

  <!-- Recommender Modal -->
  <div id="recommenderModal" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl max-w-2xl w-full p-6 shadow-2xl overflow-y-auto max-h-[90vh]">
      <div class="flex items-center justify-between pb-4 border-b border-[var(--border)] mb-5">
        <div class="flex items-center gap-2">
          <span class="text-2xl">✨</span>
          <h2 class="text-xl font-bold text-[var(--foreground)]">What Should I Read Next?</h2>
        </div>
        <button onclick="closeRecommender()" class="text-[var(--muted-foreground)] hover:text-[var(--foreground)] text-xl font-bold px-2">✕</button>
      </div>

      <p class="text-sm text-[var(--muted-foreground)] mb-4">
        Pick what kind of experience you are in the mood for, or spin the wheel for a high-conviction book from your drive:
      </p>

      <!-- Mood selection buttons -->
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5 mb-6">
        <button onclick="recommendByMood('fast-paced')" class="p-3 text-left border border-[var(--border)] rounded-xl hover:bg-[var(--border)] transition">
          <div class="font-semibold text-sm text-[var(--foreground)]">⚡ Unputdownable</div>
          <div class="text-xs text-[var(--muted-foreground)]">High momentum, page-turner</div>
        </button>
        <button onclick="recommendByMood('sci-fi')" class="p-3 text-left border border-[var(--border)] rounded-xl hover:bg-[var(--border)] transition">
          <div class="font-semibold text-sm text-[var(--foreground)]">🌌 Mind-Bending Sci-Fi</div>
          <div class="text-xs text-[var(--muted-foreground)]">Cosmic scope & concepts</div>
        </button>
        <button onclick="recommendByMood('existential')" class="p-3 text-left border border-[var(--border)] rounded-xl hover:bg-[var(--border)] transition">
          <div class="font-semibold text-sm text-[var(--foreground)]">🧠 Existential & Absurd</div>
          <div class="text-xs text-[var(--muted-foreground)]">Quiet depth & dark humor</div>
        </button>
        <button onclick="recommendByMood('craft')" class="p-3 text-left border border-[var(--border)] rounded-xl hover:bg-[var(--border)] transition">
          <div class="font-semibold text-sm text-[var(--foreground)]">✍️ Masterful Prose</div>
          <div class="text-xs text-[var(--muted-foreground)]">Didion, Dillard, Baldwin</div>
        </button>
        <button onclick="recommendByMood('screenplay')" class="p-3 text-left border border-[var(--border)] rounded-xl hover:bg-[var(--border)] transition">
          <div class="font-semibold text-sm text-[var(--foreground)]">🎬 Cinema & Story</div>
          <div class="text-xs text-[var(--muted-foreground)]">Scripts & narrative craft</div>
        </button>
        <button onclick="recommendByMood('marketing')" class="p-3 text-left border border-[var(--border)] rounded-xl hover:bg-[var(--border)] transition">
          <div class="font-semibold text-sm text-[var(--foreground)]">🎯 Persuasion & Strategy</div>
          <div class="text-xs text-[var(--muted-foreground)]">Influence, branding, offers</div>
        </button>
      </div>

      <div class="flex items-center gap-3 mb-6">
        <div class="h-px bg-[var(--border)] flex-1"></div>
        <button onclick="surpriseMe()" class="px-5 py-2.5 bg-[var(--accent)] hover:bg-[var(--accent-hover)] text-white text-sm font-semibold rounded-xl shadow transition flex items-center gap-2">
          <span>🎲</span>
          <span>Surprise Me / Spin Shelf</span>
        </button>
        <div class="h-px bg-[var(--border)] flex-1"></div>
      </div>

      <!-- Recommendation Result Card -->
      <div id="recommendationResult" class="p-5 bg-[var(--background)] border border-[var(--border)] rounded-xl hidden">
        <div class="flex items-start justify-between gap-4 mb-2">
          <div>
            <div id="recCategory" class="text-xs font-semibold text-[var(--accent)] uppercase tracking-wider"></div>
            <h3 id="recTitle" class="text-lg font-bold text-[var(--foreground)] mt-0.5"></h3>
            <p id="recAuthor" class="text-sm font-medium text-[var(--muted-foreground)]"></p>
          </div>
          <button onclick="copySingleTbr(document.getElementById('recTitle').innerText, document.getElementById('recAuthor').innerText)" class="px-3 py-1 bg-[var(--card)] hover:bg-[var(--border)] border border-[var(--border)] text-xs font-medium rounded-lg">
            Copy
          </button>
        </div>
        <div class="mt-3 text-sm text-[var(--foreground)] leading-relaxed">
          <div class="font-semibold text-xs text-[var(--muted-foreground)] uppercase tracking-wider mb-1">The Pitch</div>
          <p id="recPitch"></p>
        </div>
        <div class="mt-3 p-3 bg-[var(--card)] rounded-lg text-xs text-[var(--muted-foreground)] border border-[var(--border)]">
          <span class="font-semibold text-[var(--foreground)]">Why read it:</span> <span id="recWhyLove"></span>
        </div>
      </div>
    </div>
  </div>

  <!-- Toast Notification -->
  <div id="toast" class="fixed bottom-6 right-6 bg-[var(--foreground)] text-[var(--background)] px-4 py-2.5 rounded-lg shadow-xl text-sm font-medium transition-all transform translate-y-16 opacity-0 pointer-events-none z-50">
    Copied to clipboard!
  </div>

  <script>
    const SHELF_DATA = {shelf_json};
    let activeCategory = "All";

    const CATEGORIES = [
      "All",
      "Fiction & Non-Fiction",
      "Cinema & Film Craft",
      "Screenplays",
      "Marketing & Strategy",
      "Philosophy, Essays & Misc",
      "Graphic Guides",
      "Comics & Graphic Novels",
      "Cooking & Food"
    ];

    function showToast(msg) {{
      const t = document.getElementById("toast");
      t.innerText = msg;
      t.classList.remove("translate-y-16", "opacity-0");
      setTimeout(() => {{
        t.classList.add("translate-y-16", "opacity-0");
      }}, 2500);
    }}

    function copyToClipboard(text, msg) {{
      navigator.clipboard.writeText(text).then(() => {{
        showToast(msg || "Copied to clipboard!");
      }});
    }}

    function copySingleTbr(title, author) {{
      copyToClipboard(`${{title}} — ${{author}}`, `Copied: "${{title}} — ${{author}}"`);
    }}

    function copyAllTbr() {{
      const q = document.getElementById("searchInput").value.toLowerCase().trim();
      const quoteOnly = document.getElementById("quoteBankOnly").checked;

      const filtered = SHELF_DATA.filter(b => {{
        if (activeCategory !== "All" && b.category !== activeCategory) return false;
        if (quoteOnly && !b.has_quote_bank) return false;
        if (q) {{
          const matchTitle = b.title.toLowerCase().includes(q);
          const matchAuthor = b.author.toLowerCase().includes(q);
          const matchPitch = (b.pitch || "").toLowerCase().includes(q);
          const matchTags = (b.tags || []).some(t => t.toLowerCase().includes(q));
          if (!matchTitle && !matchAuthor && !matchPitch && !matchTags) return false;
        }}
        return true;
      }});

      const lines = filtered.map(b => `${{b.title}} — ${{b.author}}`);
      copyToClipboard(lines.join("\\n"), `Copied ${{lines.length}} books to clipboard!`);
    }}

    function renderCategoryPills() {{
      const container = document.getElementById("categoryPills");
      container.innerHTML = CATEGORIES.map(cat => {{
        const isAct = cat === activeCategory;
        const count = cat === "All" ? SHELF_DATA.length : SHELF_DATA.filter(b => b.category === cat).length;
        if (count === 0) return "";
        return `
          <button 
            onclick="setCategory('${{cat}}')" 
            class="px-3 py-1.5 rounded-full text-xs font-medium transition ${{
              isAct 
                ? 'bg-[var(--accent)] text-white shadow-sm' 
                : 'bg-[var(--pill-bg)] text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--border)]'
            }}">
            ${{cat}} (${{count}})
          </button>
        `;
      }}).join("");
    }}

    function setCategory(cat) {{
      activeCategory = cat;
      renderCategoryPills();
      renderShelf();
    }}

    function renderShelf() {{
      const q = document.getElementById("searchInput").value.toLowerCase().trim();
      const quoteOnly = document.getElementById("quoteBankOnly").checked;
      const grid = document.getElementById("booksGrid");

      const filtered = SHELF_DATA.filter(b => {{
        if (activeCategory !== "All" && b.category !== activeCategory) return false;
        if (quoteOnly && !b.has_quote_bank) return false;
        if (q) {{
          const matchTitle = b.title.toLowerCase().includes(q);
          const matchAuthor = b.author.toLowerCase().includes(q);
          const matchPitch = (b.pitch || "").toLowerCase().includes(q);
          const matchTags = (b.tags || []).some(t => t.toLowerCase().includes(q));
          if (!matchTitle && !matchAuthor && !matchPitch && !matchTags) return false;
        }}
        return true;
      }});

      document.getElementById("itemCount").innerText = `Showing ${{filtered.length}} of ${{SHELF_DATA.length}}`;

      if (filtered.length === 0) {{
        grid.innerHTML = `
          <div class="col-span-full py-16 text-center text-[var(--muted-foreground)]">
            <span class="text-4xl block mb-2">🔍</span>
            <p class="font-medium">No matching books found for "${{q}}"</p>
            <p class="text-xs mt-1">Try clearing your search query or switching categories.</p>
          </div>
        `;
        return;
      }}

      grid.innerHTML = filtered.map((b, idx) => {{
        const hasQuote = b.quotes && b.quotes.length > 0;
        const quoteSnippet = hasQuote ? b.quotes[0].quote : "";

        return `
          <div class="bg-[var(--card)] hover:bg-[var(--card-hover)] border border-[var(--border)] rounded-xl p-5 shadow-sm transition flex flex-col justify-between group">
            <div>
              <!-- Category and Format badges -->
              <div class="flex items-center justify-between gap-2 mb-2">
                <span class="text-[11px] font-semibold text-[var(--accent)] tracking-wider uppercase">${{b.category}}</span>
                <span class="text-[10px] font-mono px-2 py-0.5 bg-[var(--background)] rounded border border-[var(--border)] text-[var(--muted-foreground)]">
                  ${{b.format}}
                </span>
              </div>

              <!-- Title & Author -->
              <h3 class="text-base font-bold text-[var(--foreground)] tracking-tight group-hover:text-[var(--accent)] transition leading-snug">
                ${{b.title}}
              </h3>
              <p class="text-xs font-semibold text-[var(--muted-foreground)] mb-3">
                ${{b.author}}
              </p>

              <!-- Pitch / Back-cover synopsis -->
              <div class="text-xs text-[var(--foreground)] leading-relaxed mb-3 line-clamp-3">
                ${{b.pitch}}
              </div>

              <!-- Why people love it -->
              <div class="p-2.5 bg-[var(--background)] rounded-lg text-[11px] text-[var(--muted-foreground)] border border-[var(--border)] mb-3">
                <span class="font-semibold text-[var(--foreground)]">Why read it:</span> ${{b.why_love}}
              </div>

              <!-- Excerpt Quote (if available) -->
              ${{quoteSnippet ? `
                <div class="p-2.5 bg-blue-500/5 border border-blue-500/20 rounded-lg text-xs italic text-[var(--foreground)] mb-3">
                  “${{quoteSnippet.length > 140 ? quoteSnippet.substring(0, 140) + '...' : quoteSnippet}}”
                </div>
              ` : ''}}
            </div>

            <!-- Footer / Copy button -->
            <div class="pt-3 border-t border-[var(--border)] flex items-center justify-between text-xs">
              <span class="text-[10px] text-[var(--muted-foreground)]">
                ${{b.has_quote_bank ? '★ In Quote Bank' : ''}}
              </span>
              <button 
                onclick="copySingleTbr('${{b.title.replace(/'/g, "\\\\\\'")}}', '${{b.author.replace(/'/g, "\\\\\\'")}}')" 
                class="px-2.5 py-1 bg-[var(--background)] hover:bg-[var(--border)] border border-[var(--border)] rounded text-[11px] font-medium text-[var(--foreground)] transition flex items-center gap-1">
                <span>📋</span>
                <span>Copy TBR</span>
              </button>
            </div>
          </div>
        `;
      }}).join("");
    }}

    function openRecommender() {{
      document.getElementById("recommenderModal").classList.remove("hidden");
    }}

    function closeRecommender() {{
      document.getElementById("recommenderModal").classList.add("hidden");
    }}

    function displayRecommendation(b) {{
      const res = document.getElementById("recommendationResult");
      document.getElementById("recCategory").innerText = b.category;
      document.getElementById("recTitle").innerText = b.title;
      document.getElementById("recAuthor").innerText = b.author;
      document.getElementById("recPitch").innerText = b.pitch;
      document.getElementById("recWhyLove").innerText = b.why_love;
      res.classList.remove("hidden");
    }}

    function surpriseMe() {{
      const randomBook = SHELF_DATA[Math.floor(Math.random() * SHELF_DATA.length)];
      displayRecommendation(randomBook);
    }}

    function recommendByMood(mood) {{
      let pool = [];
      if (mood === 'fast-paced') {{
        pool = SHELF_DATA.filter(b => (b.tags || []).some(t => t.includes('fast-paced') || t.includes('unputdownable') || t.includes('thriller') || t.includes('pacing')));
        if (pool.length === 0) pool = SHELF_DATA.filter(b => b.category === "Fiction & Non-Fiction");
      }} else if (mood === 'sci-fi') {{
        pool = SHELF_DATA.filter(b => (b.tags || []).some(t => t.includes('sci-fi') || t.includes('speculative') || t.includes('cosmic')));
      }} else if (mood === 'existential') {{
        pool = SHELF_DATA.filter(b => (b.tags || []).some(t => t.includes('existential') || t.includes('absurd') || t.includes('satire') || t.includes('philosophy')));
      }} else if (mood === 'craft') {{
        pool = SHELF_DATA.filter(b => (b.tags || []).some(t => t.includes('craft') || t.includes('writing') || t.includes('memoir') || t.includes('observation')));
      }} else if (mood === 'screenplay') {{
        pool = SHELF_DATA.filter(b => b.category === "Screenplays" || b.category === "Cinema & Film Craft");
      }} else if (mood === 'marketing') {{
        pool = SHELF_DATA.filter(b => b.category === "Marketing & Strategy");
      }}

      if (pool.length === 0) pool = SHELF_DATA;
      const pick = pool[Math.floor(Math.random() * pool.length)];
      displayRecommendation(pick);
    }}

    // Initial render
    renderCategoryPills();
    renderShelf();
  </script>
</body>
</html>
"""
    SHELF_HTML_PROTO.parent.mkdir(exist_ok=True)
    SHELF_HTML_PROTO.write_text(html, encoding="utf-8")
    
    SHELF_HTML_DOCS.parent.mkdir(exist_ok=True)
    SHELF_HTML_DOCS.write_text(html, encoding="utf-8")
    print(f"Generated prototype page: {SHELF_HTML_PROTO}")
    print(f"Generated docs page: {SHELF_HTML_DOCS}")

if __name__ == "__main__":
    normalize_all()
