---
name: claude-code-mastery
description: >-
  An interactive coach that teaches and tracks the 7 fundamentals of using Claude
  Code well — environment setup, codebase Q&A, git-history context, the plan→edit→PR
  agentic workflow, CLAUDE.md context management, speed keybindings, and feedback
  loops. Maintains a local progress file and confirms when each fundamental is
  mastered. USE THIS SKILL whenever the user wants to learn, practice, get better
  at, onboard onto, or track their progress with Claude Code; whenever they ask
  "how do I use Claude Code", "teach me Claude Code", "what should I learn next",
  "am I using this right", or mention a learning plan / fundamentals / mastery /
  onboarding for Claude Code — even if they don't name this skill explicitly.
---

# Claude Code Mastery

A hands-on coach. It walks the user through seven fundamentals of Claude Code, one
at a time, and tracks mastery in a local progress file so progress survives across
sessions. When a fundamental is fully done, it throws a Shaka 🤙.

The engine lives in `scripts/track.py`. The teaching detail for each fundamental
lives in `references/fundamentals.md`. **Read that reference file before coaching
any fundamental** — it has the reason, the step-by-step, and an example for each.

## The progress file

State lives in `.claude-code-mastery.json` in the user's current working directory.
It is created on first use and updated as they go. It is plain JSON — the user can
commit it or gitignore it; mention this only if they ask.

Each of the 7 fundamentals has a checklist. Items are one of two kinds:
- **auto** — `track.py` can detect it (e.g. a CLAUDE.md exists, the repo has commits).
- **self** — a behaviour only the user can confirm (e.g. "Claude explained a commit's history to me").

A fundamental becomes **mastered** when every checklist item is true.

## The coaching loop

Run this loop. Keep it conversational and encouraging — you are a patient pair, not
a quiz bot. Always operate from the user's project directory so the auto-checks see
the right files.

1. **Orient.** Run `python scripts/track.py status`. If there's no progress file,
   run `python scripts/track.py init` first. Show the dashboard and ask which
   fundamental they want to work on, or suggest the lowest unfinished one (F1→F7).

2. **Teach.** For the chosen fundamental, open `references/fundamentals.md`, find its
   section, and present three things in your own words, briefly:
   - **Why it matters** (the reason),
   - **How to master it** (the concrete steps),
   - **An example** they can run right now.
   Then show its checklist: `python scripts/track.py detail F<n>`.

3. **Practice together.** Actually do the thing with them in this session where you
   can — e.g. for F2, answer a real codebase question about *their* code; for F5,
   offer to draft a CLAUDE.md for their project; for F3, run the git-history lookup.
   This is the point of the skill: practice on the user's real work, not toy data.

4. **Verify.**
   - Run `python scripts/track.py check F<n>` to refresh the **auto** items.
   - For each **self** item, ask the user plainly whether they did it. Do not mark a
     self item done on their behalf without a clear yes — the value of the checklist
     is that it's honest. When they confirm:
     `python scripts/track.py mark F<n> <item_key> --done`.

5. **Finalise.** Run `python scripts/track.py master F<n>`. If all items pass, the
   script prints the Shaka — relay that celebration to the user and read the sign
   aloud in spirit. If items remain, the script lists them; loop back to step 3 on
   those.

6. **Next.** Show the updated `status` and offer the next fundamental. When all seven
   are mastered, the dashboard shows the full-Aloha banner — congratulate them
   properly.

## Rules of thumb

- **Never fake mastery.** Auto items are detected; self items need a genuine user
  confirmation. If a user says "just mark them all done", you can, but gently note
  that the checklist only helps them if it's truthful.
- **Honour the user's pace.** They can do one fundamental and stop. Don't force all
  seven in one sitting. The progress file is exactly so they can return later.
- **Meet their level.** Some users are seasoned engineers; some opened a terminal
  last week. Explain jargon when in doubt.
- **Re-run from their project root** so `check` can see CLAUDE.md, git history, and
  test commands. If the auto-checks come back empty unexpectedly, confirm the working
  directory before retrying.

## Command reference

```
python scripts/track.py init                      # create the progress file
python scripts/track.py status                    # dashboard of all 7 fundamentals
python scripts/track.py detail F5                 # one fundamental: why + checklist
python scripts/track.py check F5                  # refresh automated checks
python scripts/track.py mark F5 memory_loaded --done   # confirm a self item
python scripts/track.py mark F5 memory_loaded --undo   # un-confirm it
python scripts/track.py master F5                 # finalise -> Shaka if complete
python scripts/track.py shaka F5                  # print the sign (celebrate anytime)
python scripts/track.py reset --force             # start over
```

## The fundamentals (overview)

| ID | Fundamental | One-line point |
|----|-------------|----------------|
| F1 | Setup & Environment | Remove day-one friction so it becomes a habit. |
| F2 | Codebase Q&A | Explore with meaning before you edit. |
| F3 | Git History & Standups | Code is *what*; history is *why*. |
| F4 | Plan → Edit → PR | Approve a plan first; automate the git plumbing. |
| F5 | CLAUDE.md Context | A standing brief so you stop repeating yourself. |
| F6 | Speed & Keybindings | Muscle memory: auto-accept, `!`, Escape. |
| F7 | Feedback Loops | Give Claude a way to check its own work. |

Full detail — reason, steps, example, and how each checklist item is verified — is in
`references/fundamentals.md`.
