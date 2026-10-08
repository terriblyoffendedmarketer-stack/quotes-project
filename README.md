# Marginalia

One great piece of writing a day, on your Android home screen. Each card takes a line or a short passage from a writer and files it under the job it does, like “How to make the impossible believable”. A few slides then show you how it works, so you fall for the writing and want the book.

## How a card works

1. **How to.** Just the job, like “How to make the impossible believable”, set big and bold in Fraunces on a cobalt slide. It's the hook.
2. **The line.** The quote. Some are punchy lines and some are short working passages, because some jobs need a paragraph.
3. **Look closer.** What the writing is doing that you wouldn't spot on your own.
4. **Steal it.** One small exercise for your own writing, often marketing copy. You can hide this slide.
5. **Around it.** A nice-to-have extra: true facts about the book and its author, ending on an open loop.

Every slide after the hook repeats the job in fine print at the bottom. Each slide has its own colour: cobalt, butter, bubblegum, lime and lilac. In dark mode the hook stays cobalt and the rest turn ochre, berry, forest and indigo.

## The library

- `content/cards.json` holds every card and is the single source of truth.
- `content/authors.md` is the author library: classic, contemporary, memoir and nonfiction.
- `content/quote-bank.md` holds verified lines waiting for a card.
- `content/VOICE.md` has the writing rules and the step-by-step process that keeps the explanations from reading like AI.

## The app

- `android/` contains the Android app and its home-screen widget. See `android/README.md`.
- **Install once.** The app downloads `content/cards.json` from this repository every few hours, so new and edited cards arrive without reinstalling. You only reinstall when the app's own code changes.
- `prototype/` is a browser version for reviewing cards. Run `python3 tools/build_prototype.py` to rebuild it.

## Tools

- `python3 tools/lint_cards.py` flags AI-sounding patterns, per card and across the set.
- `python3 tools/add_cards.py batch.json` appends a batch of cards and refuses duplicates or broken highlights.
- `python3 tools/build_prototype.py` rebuilds the prototype and checks every highlight appears in its quote.
