# Project 01 — pyography

This folder is Project 1 of the user's 12-project geospatial and AI industry portfolio. Read `docs/PLAN.md` first.
It holds every settled decision and the remaining open questions.

## Working rules (set by the user)
- **The user is in charge.** Their commands overrule everything, including skills and Claude's recommendations.
- **One project at a time.** Work only on Project 1 here. Do not plan or ask about other projects. Move on only when the user says so.
- **Learning mode.** Claude writes the main code; the user studies it to learn. Build one step at a time and let the user study each step before continuing.
- **Hands-on loop (set 2026-11-23).** Every step follows `docs/PLAN.md` §5: the user predicts the approach first, writes some of the tests from English descriptions, runs `uv run pytest` / `uv run ruff check .` in their own terminal, finds one planted bug, and answers a quiz that includes an "explain this line" question. Don't run the user's hands-on commands for them, and don't write the tests they're assigned.
- **Ask in small rounds.** Do not dump every open question at once.
- **Document as you go.** Keep `docs/DECISIONS.md` and `docs/JOURNAL.md` current so the process can be pushed to GitHub and reused for job interviews.
- Before the first push, confirm `gh auth status` shows the user logged in.

## First thing to do in a new chat
Planning is complete (all questions settled 2026-11-23). Read the latest entry in `docs/JOURNAL.md` to see which build step (`docs/PLAN.md` §5) is current. If the user hasn't finished that step's quiz, help them with it first. Build the next step only when the user says "next".

## Shared references
- Original brief: `../Industry_Portfolio_12_Projects_Learning_Order.pdf` (page 1)
- Verified data sources for all projects: `../_planning/data-sources-verified-2026-11-23.md`
