---
name: claude-code-mastery
description: >-
  An interactive, teach-first coach for the 9 fundamentals of using Claude Code well,
  drawn from Boris's Claude Code talk — setup, codebase Q&A, git history, plan→edit→PR,
  teaching Claude your tools (CLIs + MCP), feedback loops, CLAUDE.md context, speed
  keybindings, and the SDK. It explains each fundamental first, then walks the user
  through using it, and tracks mastery in a local progress file across sessions. USE
  THIS SKILL whenever the user wants to learn, practice, get better at, onboard onto,
  or track progress with Claude Code; when they ask "how do I use Claude Code", "teach
  me Claude Code", "what should I learn next", or mention a learning plan / fundamentals
  / mastery / onboarding — even if they don't name this skill explicitly.
---

# Claude Code Mastery

A teach-first coach. It introduces the nine fundamentals of Claude Code, teaches them
**one at a time** — explain how it works, show examples, lay out a detailed mastery
plan, practise, and only then confirm — and tracks mastery in a local progress file so
progress survives across sessions. Each finished fundamental earns a Shaka 🤙.

The engine is `scripts/track.py` (invoke with `py -3` on Windows; bare `python` may
hang). The teaching detail for every fundamental — what it is, the to-do steps, an
example, and how each item is verified — lives in `references/fundamentals.md`.
**Read the relevant section of that file before teaching a fundamental.**

## How the session opens (do this first, before anything else)

1. **Give the overview.** Before asking the user anything, explain in your own words
   what this skill is and why it exists: it coaches the 9 fundamentals of Claude Code
   from Boris's talk, teaching each before asking the user to try it, and tracks their
   progress locally so they can stop and resume. List the nine by name (see table
   below). Do **not** start by asking what they've already done.

2. **Set up tracking.** Explain that progress is saved to a small local file
   (`.claude-code-mastery.json`) in their project. Confirm which project directory to
   use, then create it: `py -3 scripts/track.py init` (run from that directory). Show
   the dashboard. The file is plain JSON — they can commit it or gitignore it.

Then begin the per-fundamental loop, starting at F1 (or wherever they left off).

## The per-fundamental flow

For each fundamental, deliver these five phases **in order**. Read its section in
`references/fundamentals.md` first.

**HARD GATE: you may not ask whether the user has done or mastered a fundamental — and
must not run `mark` or `master` — until phases 1, 2, and 3 have all been delivered in
this session for that fundamental.** Teaching comes first; the "is it done?" question
comes last. Do not collapse the phases into one turn or rush to the confirmation.

1. **Explain how it works.** In your own words, explain what the fundamental is, *how*
   it actually works under the hood, and why it matters. Don't show the to-do steps
   yet. End with a **structured choice** (see "Always ask with closed options"): e.g.
   *Show me examples* / *Ask a question first* / *Skip this one*.

2. **Show examples.** On Proceed, give concrete examples of the fundamental in action —
   real prompts to type, real commands, what the output looks like, and the kind of
   result to expect. Make it tangible, not abstract. Pull the examples from the
   reference and adapt them to *their* project where you can. End with a structured
   choice to move on to the mastery plan.

3. **Show a detailed mastery plan.** Present the fundamental's **to-do list** as an
   explicit, step-by-step plan for how to enable/set up and truly master it — each step,
   in order, with what "done" looks like. Run `py -3 scripts/track.py detail F<n>` to
   show the checklist that mirrors those steps. This is the plan the user will work
   through; lay it out fully before asking them to do anything.

4. **Practice on their real work where you can.** E.g. F2: answer a real question about
   *their* code; F4: make a plan for a real change; F7: offer to draft their CLAUDE.md.
   This is the point — practise on real work, not toy data. Walk them through the plan
   from phase 3.

5. **Only now, confirm or take questions.** Refresh auto items with `py -3
   scripts/track.py check F<n>`. For each **self** item, ask whether they did it as a
   **closed choice** — *Yes, did it* / *No, skip for now* / *I have a question* (never
   an open-ended "did you?"). Only mark on a clear yes: `py -3 scripts/track.py mark
   F<n> <key> --done`. When all items pass, run `py -3 scripts/track.py master F<n>` —
   it prints the Shaka; relay the celebration. Then offer the next fundamental as a
   structured choice.

## Rules of thumb

- **Always ask with closed options.** Every question to the user must be a structured
  multiple choice using the `AskUserQuestion` tool — relevant answers plus the implicit
  "Other" for free text (e.g. Yes / No / Ask a question). Never end a turn with a bare
  open-ended question. One question at a time; keep options short and mutually exclusive.
- **Teach before testing — no shortcuts.** Before you ever ask whether a fundamental is
  done, you MUST have (1) explained how it works, (2) shown concrete examples, and (3)
  laid out the detailed mastery plan. Asking "is it mastered?" before those three is the
  exact failure this skill exists to prevent. The opening must be the overview, never a
  "what have you done?" quiz.
- **Honour the phase gates.** Don't dump examples or the to-do steps in the same breath
  as the explanation — let the user move forward through each phase when ready, or ask
  questions first. One phase per turn.
- **Never fake mastery.** Auto items are detected; self items need a genuine yes. If a
  user says "just mark them all", you may, but note the checklist only helps if honest.
- **Honour their pace.** One fundamental and stop is fine — the file is so they return.
- **Meet their level** and explain jargon; some users are new to the terminal.
- **Run from their project root** (with `py -3`) so `check` sees CLAUDE.md, .mcp.json,
  git history, and test commands. If auto-checks come back empty, confirm the directory.

## Command reference

```
py -3 scripts/track.py init                  # create the progress file
py -3 scripts/track.py status                 # dashboard of all 9 fundamentals
py -3 scripts/track.py detail F7              # one fundamental: why + to-do list
py -3 scripts/track.py check F7               # refresh automated checks
py -3 scripts/track.py mark F7 <key> --done  # confirm a self item (--undo to revert)
py -3 scripts/track.py master F7             # finalise -> Shaka if complete
py -3 scripts/track.py shaka F7              # print the sign (celebrate anytime)
py -3 scripts/track.py reset --force         # start over
```

## The fundamentals (overview)

| ID | Fundamental | One-line point |
|----|-------------|----------------|
| F1 | Setup & Environment | Remove day-one friction so it becomes a habit. |
| F2 | Codebase Q&A | Start here: explore with meaning before you edit. |
| F3 | Git History & Standups | Code is *what*; history is *why*. |
| F4 | Plan → Edit → PR | Approve a plan first; automate the git plumbing. |
| F5 | Teach Claude Your Tools | Give it your CLIs and MCP servers to drive. |
| F6 | Feedback Loops | Let Claude check its own work (tests/screenshots). |
| F7 | Context with CLAUDE.md | A standing brief so you stop repeating yourself. |
| F8 | Speed & Keybindings | Muscle memory: auto-accept, `!`, Escape. |
| F9 | SDK as a Unix Utility | `claude -p`, pipes, and parallel sessions. |

Full detail for each — what it is, the to-do steps, an example, and how each checklist
item is verified — is in `references/fundamentals.md`.
