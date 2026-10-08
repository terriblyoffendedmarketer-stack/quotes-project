# Project context for Claude

This is Marginalia, a personal daily-writing-example app for its owner, a B2B SaaS marketer. Read this before changing anything.

## Decisions already made

- **Android, always.** Never suggest iOS or a PWA. The surface is a home-screen widget plus a full-screen reader app.
- **Widget behaviour.** One slide at a time, filling whatever size the widget is. Tap the right side for the next slide and the left side to go back. Slides are drawn directly into the widget's views. Don't reintroduce a StackView, a list adapter or a RemoteViewsService. The StackView warped at large sizes, and the adapter left the widget blank for a second or two when returning to the home screen.
- **Typography.** The quote is big and bold, while explanations are regular weight. The widget follows the phone's light or dark mode.
- **Content updates without reinstalling.** The app fetches `content/cards.json` from this public repo (`ContentSync.kt`). Keep the JSON format backwards compatible. Adding fields is fine; renaming or removing them breaks installed apps.
- **Slide order:** How to (the hook: just the job, as large as it fits), The line, Look closer, Steal it (can be hidden), Around it (last, a nice-to-have). The hook also shows the author's name, small. Slides after the hook show the job in fine print. Slide colours change every day (`Palette.kt`).
- **Formatting in card text.** Wrap titles of books, magazines and newspapers in `*asterisks*` in lookCloser, aroundIt and stealIt; the app and prototype render them as italics. Story, essay, poem and speech titles go in “curly quotes”. Line breaks in a quote (`\n`) are kept, as for poems.

## Content rules (the most important part)

- The explanation slides must be genuinely interesting and must not read like AI. `content/VOICE.md` is binding: banned patterns, the slide-by-slide jobs, sourcing rules, and the one-card-at-a-time process.
- **Slide 1 must pass the cold-reader test.** A line that only works if you know the book gets swapped for a better line or a fuller passage.
- **The library is a toolbox.** Aim for roughly half punchy lines and half working passages of up to about 120 words, fiction included.
- **Pick the slide 2 angle each line deserves**: close reading, the structural move, the dead metaphor or the scene. Plain nonfiction rarely deserves a word-by-word reading.
- **Verify every quote** against a published source before writing about it. Name the translator. If a phrase can't be confirmed, say so in the card's `verification` field. If a fact can't be checked, leave it out.
- **Run `python3 tools/lint_cards.py`** after every edit. If a flag is deliberate, list it in the card's `lintAccepted`.
- **The owner's favourite book is *Four Thousand Weeks* by Oliver Burkeman.** More good Burkeman is always welcome.

## Writing style for anything addressed to the owner

- Sentence case for headings, never title case.
