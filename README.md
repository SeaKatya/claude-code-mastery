# Claude Code Mastery 🤙

An interactive Claude Code **skill** that teaches and tracks the fundamentals of
using Claude Code well. It coaches you through them, keeps a local progress file so
your progress survives across sessions, and throws a **Shaka** when you master each one.

The fundamentals are organised into **9 modules** (F1–F9), each split into small,
single-focus **lessons** (F1.1, F1.2, …) — **32 lessons** in total. The coach teaches
**one lesson at a time**, and every lesson earns its own Shaka. Finish all the lessons
in a module and the module is complete.

For every lesson you get:
1. **How it works & why** — the reason it earns a place in your workflow.
2. **Examples** — concrete prompts/commands and what the output looks like.
3. **A mastery plan** — the ordered steps and what "done" looks like.
4. **Practice + verification** — try it on your real work; one item is auto-detected
   or self-confirmed.

## The nine modules (and their lessons)

| ID | Module | Lessons |
|----|--------|---------|
| F1 | Setup & Environment Optimization | Install & detect · Theme · Terminal newline · GitHub app · Allowed tools |
| F2 | Codebase Q&A (explore before you edit) | Ask a real question · Deeper than search · Usage follow-up |
| F3 | Git History & Standup Reports | Inside a git repo · Explain the "why" · What did I ship |
| F4 | Agentic Workflow: Plan → Edit → PR | Recent commits · Approve a plan first · Implement · commit push PR |
| F5 | Teach Claude Your Tools (CLIs + MCP) | Shared .mcp.json · Teach a CLI · Use an MCP server |
| F6 | Feedback Loops | A command to run · Iterate on feedback · Visual coding |
| F7 | Context Management with CLAUDE.md | Create a CLAUDE.md · /memory · '#' shortcut · Slash command |
| F8 | Speed & Keybindings | '!' bash mode · Escape · Shift+Tab auto-accept · Resume & inspect |
| F9 | SDK as a Unix Utility | claude -p · Flags & scripting · Parallel sessions |

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
you through a lesson, practice it on your actual code, verify it, and celebrate when you
finish one.

You can also drive the tracker directly. Commands accept a **module** id (`F7`) or a
**lesson** id (`F7.2`); `mark` needs a lesson id.

```bash
python scripts/track.py init           # create the progress file
python scripts/track.py status         # dashboard: modules + their lessons
python scripts/track.py detail F7      # a module: list its lessons
python scripts/track.py detail F7.2    # a lesson: why + its single check
python scripts/track.py check F7.1     # refresh an auto check
python scripts/track.py mark F7.2 memory_loaded --done   # confirm a self lesson
python scripts/track.py master F7.2    # finalise a lesson -> Shaka
python scripts/track.py shaka          # celebrate anytime
python scripts/track.py reset --force
```

## How verification works

Each lesson has a single check, of one of two kinds:
- **auto** — the tracker detects it (a `CLAUDE.md` exists, you're in a git repo, the
  project has a test command, etc.).
- **self** — a behaviour only you can vouch for ("Claude explained a commit's history
  to me"). You confirm these honestly; the checklist only helps if it's truthful.

A **lesson** is mastered when its check is true; a **module** is complete when all its
lessons are mastered. Finish every module and the dashboard gives you the full Aloha
banner.

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
    └── fundamentals.md         # why / examples / steps / verification per lesson
```

## License

MIT — do what you like. Aloha. 🤙
