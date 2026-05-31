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

A teach-first coach. It introduces the fundamentals of Claude Code, organised into
**9 modules** (F1–F9) that are each split into small, single-focus **lessons**
(F1.1, F1.2, …) — 32 lessons in all. It teaches **one lesson at a time** — explain
how it works, show examples, lay out a detailed mastery plan, practise, and only then
confirm — and tracks mastery in a local progress file so progress survives across
sessions. **Each lesson** earns its own Shaka 🤙; completing every lesson in a module
completes that module.

The engine is `scripts/track.py` (invoke with `py -3` on Windows; bare `python` may
hang). The teaching detail for every lesson — what it is, examples, the to-do steps,
and how it's verified — lives in `references/fundamentals.md`. **Read the relevant
lesson's section of that file before teaching it.**

## How the session opens (do this first, before anything else)

1. **Give the overview.** Before asking the user anything, explain in your own words
   what this skill is and why it exists: it coaches the fundamentals of Claude Code
   from Boris's talk — 9 modules split into 32 small lessons — teaching each lesson
   before asking the user to try it, and tracks their progress locally so they can stop
   and resume. List the nine modules by name (see table below). Do **not** start by
   asking what they've already done.

2. **Set up tracking.** Explain that progress is saved to a small local file
   (`.claude-code-mastery.json`) in their project. Confirm which project directory to
   use, then create it: `py -3 scripts/track.py init` (run from that directory). Show
   the dashboard. The file is plain JSON — they can commit it or gitignore it.

Then begin the per-lesson loop, starting at the first unfinished lesson (F1.1, or
wherever they left off). Work module by module, lesson by lesson, in order.

## The per-lesson flow

A **lesson** (e.g. F1.2) is the unit of teaching. For each lesson, deliver these five
phases **in order**. Read its section in `references/fundamentals.md` first.

**HARD GATE: you may not ask whether the user has done or mastered a lesson — and
must not run `mark` or `master` — until phases 1, 2, and 3 have all been delivered in
this session for that lesson.** Teaching comes first; the "is it done?" question
comes last. Do not collapse the phases into one turn or rush to the confirmation.

1. **Explain how it works.** In your own words, explain what the lesson is, *how*
   it actually works under the hood, and why it matters. Don't show the to-do steps
   yet. End with a **structured choice** (see "Always ask with closed options"): e.g.
   *Show me examples* / *Ask a question first* / *Skip this one*.

2. **Show examples.** On Proceed, give concrete examples of the lesson in action —
   real prompts to type, real commands, what the output looks like, and the kind of
   result to expect. Make it tangible, not abstract. Pull the examples from the
   reference and adapt them to *their* project where you can. End with a structured
   choice to move on to the mastery plan.

3. **Show a detailed mastery plan.** Present the lesson's **to-do steps** as an
   explicit, step-by-step plan for how to enable/set up and truly master it — each step,
   in order, with what "done" looks like. Run `py -3 scripts/track.py detail F<n>.<m>`
   to show the lesson's single check that the steps build toward. Lay it out fully
   before asking them to do anything.

4. **Practice on their real work where you can.** E.g. F2.1: answer a real question
   about *their* code; F4.2: make a plan for a real change; F7.1: offer to draft their
   CLAUDE.md. This is the point — practise on real work, not toy data. Walk them
   through the plan from phase 3.

5. **Only now, confirm or take questions.** If the lesson's check is **auto**, refresh
   it with `py -3 scripts/track.py check F<n>.<m>`. If it's **self**, ask whether they
   did it as a **closed choice** — *Yes, did it* / *No, skip for now* / *I have a
   question* (never an open-ended "did you?"). Only mark on a clear yes: `py -3
   scripts/track.py mark F<n>.<m> <key> --done`. Then run `py -3 scripts/track.py master
   F<n>.<m>` — it prints the Shaka for that lesson (and a 🌺 line when the lesson
   completes its whole module); relay the celebration. Then offer the next lesson as a
   structured choice.

## Rules of thumb

- **Always ask with closed options.** Every question to the user must be a structured
  multiple choice using the `AskUserQuestion` tool — relevant answers plus the implicit
  "Other" for free text (e.g. Yes / No / Ask a question). Never end a turn with a bare
  open-ended question. One question at a time; keep options short and mutually exclusive.
- **Teach before testing — no shortcuts.** Before you ever ask whether a lesson is
  done, you MUST have (1) explained how it works, (2) shown concrete examples, and (3)
  laid out the detailed mastery plan. Asking "is it mastered?" before those three is the
  exact failure this skill exists to prevent. The opening must be the overview, never a
  "what have you done?" quiz.
- **One lesson at a time.** A lesson is small and single-focus — teach exactly one per
  pass through the five phases. Never bundle several lessons (or a whole module) into
  one explanation; that is the merging this structure exists to prevent.
- **Honour the phase gates.** Don't dump examples or the to-do steps in the same breath
  as the explanation — let the user move forward through each phase when ready, or ask
  questions first. One phase per turn.
- **Never fake mastery.** Auto items are detected; self items need a genuine yes. If a
  user says "just mark them all", you may, but note the checklist only helps if honest.
- **Honour their pace.** One lesson and stop is fine — the file is so they return.
- **Meet their level** and explain jargon; some users are new to the terminal.
- **Run from their project root** (with `py -3`) so `check` sees CLAUDE.md, .mcp.json,
  git history, and test commands. If auto-checks come back empty, confirm the directory.

## Command reference

Commands accept a **module** id (`F7`) or a **lesson** id (`F7.2`). `mark` needs a
lesson id.

```
py -3 scripts/track.py init                     # create the progress file
py -3 scripts/track.py status                    # dashboard: modules + their lessons
py -3 scripts/track.py detail F7                 # a module: list its lessons
py -3 scripts/track.py detail F7.2               # a lesson: why + its single check
py -3 scripts/track.py check F7.1                # refresh an auto check (lesson or module)
py -3 scripts/track.py mark F7.2 <key> --done   # confirm a self lesson (--undo to revert)
py -3 scripts/track.py master F7.2              # finalise a lesson -> Shaka
py -3 scripts/track.py shaka F7.2              # print the sign (celebrate anytime)
py -3 scripts/track.py reset --force           # start over
```

## The modules (overview)

Each module splits into the lessons listed; teach them in order, one at a time.

| ID | Module | Lessons |
|----|--------|---------|
| F1 | Setup & Environment | Install & detect · Theme · Terminal newline · GitHub app · Allowed tools |
| F2 | Codebase Q&A | Ask a real question · Deeper than search · Usage follow-up |
| F3 | Git History & Standups | Inside a git repo · Explain the "why" · What did I ship |
| F4 | Plan → Edit → PR | Recent commits · Approve a plan first · Implement · commit push PR |
| F5 | Teach Claude Your Tools | Shared .mcp.json · Teach a CLI · Use an MCP server |
| F6 | Feedback Loops | A command to run · Iterate on feedback · Visual coding |
| F7 | Context with CLAUDE.md | Create a CLAUDE.md · /memory · '#' shortcut · Slash command |
| F8 | Speed & Keybindings | '!' bash mode · Escape · Shift+Tab auto-accept · Resume & inspect |
| F9 | SDK as a Unix Utility | claude -p · Flags & scripting · Parallel sessions |

Full detail for every lesson — what it is, examples, the to-do steps, and how it's
verified — is in `references/fundamentals.md`.
