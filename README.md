# Claude Code Mastery 🤙

An interactive Claude Code **skill** that teaches and tracks the seven fundamentals of
using Claude Code well. It coaches you through each one, keeps a local progress file so
your progress survives across sessions, and throws a **Shaka** when you master a
fundamental.

For every fundamental you get:
1. **Why it's needed** — the reason it earns a place in your workflow.
2. **How to master it** — concrete steps to do.
3. **An example** — something to run on your own code right now.
4. **A verification checklist** — some items auto-detected, some you confirm.

## The seven fundamentals

| ID | Fundamental |
|----|-------------|
| F1 | Setup & Environment Optimization |
| F2 | Codebase Q&A (explore before you edit) |
| F3 | Git History & Standup Reports |
| F4 | Agentic Workflow: Plan → Edit → PR |
| F5 | Context Management with CLAUDE.md |
| F6 | Speed & Keybindings |
| F7 | Feedback Loops & Advanced Tools |

## Install

Skills live in `~/.claude/skills/<name>/` (personal, all projects) or
`.claude/skills/<name>/` inside a repo (project-scoped, commit it for your team). The
`SKILL.md` file must sit at the root of the skill folder. Pick one:

**Personal install (every project on your machine):**
```bash
git clone https://github.com/<your-username>/claude-code-mastery.git \
  ~/.claude/skills/claude-code-mastery
```

**Project install (just this repo, shared with teammates):**
```bash
mkdir -p .claude/skills
git clone https://github.com/<your-username>/claude-code-mastery.git \
  .claude/skills/claude-code-mastery
```

**If your repo wraps the skill in a subfolder**, copy the inner folder so `SKILL.md`
ends up at the skill root — not double-nested:
```bash
cp -r claude-code-mastery/ ~/.claude/skills/
```

Then **restart Claude Code** (skills load at startup) and run `/skills` to confirm
`claude-code-mastery` is listed.

### Requirements
- Python 3.9+ (the tracker uses only the standard library — no `pip install`).
- Git, for the history/standup fundamentals and a couple of auto-checks.

## Use it

From inside one of your real projects, just ask Claude Code something like:

> "Coach me through the Claude Code fundamentals."
> "What should I learn next in Claude Code?"
> "Track my progress on the fundamentals."

Claude will create a `.claude-code-mastery.json` progress file in that directory, walk
you through a fundamental, practice it on your actual code, verify the checklist, and
celebrate when you finish one.

You can also drive the tracker directly:

```bash
python scripts/track.py init        # create the progress file
python scripts/track.py status      # dashboard
python scripts/track.py detail F5   # why + checklist for one fundamental
python scripts/track.py check F5    # refresh automated checks
python scripts/track.py mark F5 memory_loaded --done   # confirm a self item
python scripts/track.py master F5   # finalise -> Shaka if all items pass
python scripts/track.py shaka       # celebrate anytime
python scripts/track.py reset --force
```

## How verification works

Each fundamental's checklist mixes two kinds of item:
- **auto** — the tracker detects it (a `CLAUDE.md` exists, you're in a git repo, the
  project has a test command, etc.).
- **self** — a behaviour only you can vouch for ("Claude explained a commit's history
  to me"). You confirm these honestly; the checklist only helps if it's truthful.

A fundamental is **mastered** when every item is true. Master all seven and the
dashboard gives you the full Aloha banner.

## The progress file

`.claude-code-mastery.json` is plain JSON in your working directory. Commit it to track
a team's onboarding, or add it to `.gitignore` to keep it personal — your call.

## Layout

```
claude-code-mastery/
├── SKILL.md                    # instructions Claude Code follows
├── README.md                   # this file
├── scripts/
│   └── track.py                # progress engine + Shaka renderer
└── references/
    └── fundamentals.md         # reason / steps / example / verification per fundamental
```

## License

MIT — do what you like. Aloha. 🤙
