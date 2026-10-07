# Voice rules for the explanation slides

The explanation slides are drafted with Claude, so they have to work hard not to read like AI. These rules are what every card is checked against before it goes in.

## What each slide does

- **Slide 1 (the line):** the job, the quote, the author and the work. Nothing else.
  - **The cold-reader test.** Someone who has never heard of the book should find the line interesting on its own. If it only lands once you know the context, pick another line or take in the sentences around it.
  - **Length follows the thought.** End the quote where the idea is complete. That might be one sentence or a whole paragraph. Never trim to look tidy, and never pad.
- **Slide 2 (look closer):** tell the reader something they wouldn't have seen on a second read by themselves. If a sentence could be pasted under a different quote, cut it. Choose the angle the line deserves rather than always doing a word-by-word reading:
  - *Close reading*: specific words, sounds, grammar. Best for literary lines.
  - *The move*: the structure that makes it work, such as a zoom, a list that builds a fantasy or a reversal. Best for plain-spoken nonfiction, where a word-by-word reading says the obvious.
  - *The dead metaphor*: an everyday phrase the writer brings back to life.
  - *The scene*: who's saying it, to whom and why it lands in that moment.
  - If no angle produces something the reader didn't already see, keep the quote and drop the card into the quote bank until one does.
- **Slide 3 (steal it):** one small exercise you could do on your own writing today, ideally on marketing copy. Give a concrete example. Can be switched off.
- **Slide 4 (around it):** the nice-to-have extra at the end. True facts only. Where the line sits in the book, who wrote it and when, something odd about how it was made. End on an open question the card doesn't answer. Never tell the reader to read the book.

## The library is a toolbox

The library is a toolbox for writing, so it needs both kinds of tool:

- **Punchy lines.** One or two sentences that work on their own, like the Kafka, Morrison and Palahniuk cards.
- **Working passages.** A short paragraph that does an instrumental job a single line can't, like setting up a fantasy and puncturing it, zooming out and back in, or building a character over four sentences. The passage doesn't need to be dazzling sentence by sentence. It needs to do its job visibly. The Burkeman cards are the model.

Aim for roughly half of each batch to be working passages, fiction included. A passage should still fit on one phone screen, about 120 words at most.

## Banned patterns

- "It's not X, it's Y" and "He doesn't X. He Y." Make the point positively.
- Lists of three for rhythm's sake.
- Colon reveals ("Here's the thing:") and em-dash asides.
- Words that praise without showing: genius, masterful, masterclass, stunning, haunting, powerful, quietly, deceptively, effortlessly.
- Rhetorical questions as closers.
- "This is why you should read…", "a must-read" or any other recommendation.
- Summing up the card's own point in the last line.

## What to do instead

- Quote the words you're talking about.
- Use facts in place of opinions wherever you can. Facts are much harder to make sound generated.
- Write like someone telling a friend about a book over coffee. Contractions are fine and short sentences are fine.
- Keep slide 2 under 80 words and slide 3 under 100.

## Sourcing

- Quotes come from the published texts, with the translator named for anything translated.
- Each card has a `verification` note saying how the quote was checked. Anything marked "check against your edition" should be checked against a real copy before it ships.
- Facts on slide 3 come from the book itself, its foreword or afterword, or well-documented biography. If a fact can't be checked, it comes out.

## How cards get written (so quality holds at 100+)

Writing quality drops in bulk for a simple reason. After a few cards, the writer runs out of specific things to say and falls back on shapes that worked before. The fix is to make each card start fresh, with its own material, and to judge it cold.

1. **One card at a time, never in batches.** Each card is written in its own fresh context, with only this file, the gold examples and its dossier. It never sees the previous card.
2. **Dossier first.** Before any writing, collect the verified quote, the passage around it, three to five checkable facts and anything the author said about it. If the dossier is thin, the card waits. Thin material is what produces thin writing.
3. **Three drafts of slide 2, keep one.** Each draft must point at different words in the quote. Keep the one only this quote could have.
4. **Mechanical check.** `python3 lint_cards.py` catches banned shapes, repeated openers and phrases shared across cards. A flag that's deliberate gets listed in the card's `lintAccepted`.
5. **Cold read.** A separate critic, who didn't write the card, reads only the finished slides and marks any sentence that "sounds like AI". It also marks any sentence that could sit under a different quote. Every marked sentence is rewritten or cut.
6. **Your taste pass.** You read in batches of ten and mark each card *love*, *fine* or *slop*. Cards you love become gold examples for future drafts. Phrases you mark as slop go into the linter.
