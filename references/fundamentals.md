# Claude Code Fundamentals — Reference

The fundamentals from Boris's Claude Code talk, organised into **9 modules**
(F1–F9) and split into small, single-focus **lessons** (F1.1, F1.2, …). The
coach teaches **one lesson at a time** with the full five-phase flow, and each
lesson earns its own Shaka. Read the lesson you're about to coach before you
start it.

Every lesson section has the four parts that map onto the teaching flow:

- **What it is & why** — phase 1: explain how it works, first.
- **Examples** — phase 2: concrete prompts/commands and expected output.
- **To-do / mastery plan** — phase 3: the ordered steps + what "done" looks like.
- **Try it now / Verified** — phases 4–5: practise on real work, then the exact
  item key + kind (`auto` detected vs `self` confirmed) to pass to `track.py`.

Do not reveal examples or the to-do steps in the same turn as the explanation,
and do not reach the verification phase until phases 1–3 have been delivered.

## Contents
- **F1 — Setup & Environment Optimization** — F1.1 Install & detect · F1.2 Theme · F1.3 Terminal multi-line input · F1.4 GitHub app · F1.5 Allowed tools
- **F2 — Codebase Q&A** — F2.1 Ask a real question · F2.2 Deeper than search · F2.3 Usage follow-up
- **F3 — Git History & Standups** — F3.1 Inside a git repo · F3.2 Explain the "why" · F3.3 What did I ship
- **F4 — Plan → Edit → PR** — F4.1 Recent commits · F4.2 Approve a plan first · F4.3 Implement · F4.4 commit push PR
- **F5 — Teach Claude Your Tools** — F5.1 Shared .mcp.json · F5.2 Teach a CLI · F5.3 Use an MCP server
- **F6 — Feedback Loops** — F6.1 A command Claude can run · F6.2 Iterate on feedback · F6.3 Visual coding
- **F7 — Context Management** — F7.1 Create a CLAUDE.md · F7.2 /memory · F7.3 '#' shortcut · F7.4 Slash command
- **F8 — Speed & Keybindings** — F8.1 '!' bash mode · F8.2 Escape · F8.3 Shift+Tab auto-accept · F8.4 Resume & inspect
- **F9 — SDK as a Unix Utility** — F9.1 claude -p · F9.2 Flags & scripting · F9.3 Parallel sessions

---

# F1 — Setup & Environment Optimization

Claude Code is a free-form, fully agentic tool — you open it to a bare prompt.
A few minutes of setup removes day-one friction so it becomes a daily habit. All
you need to run it is Node.js. These five lessons each remove one piece of
friction.

## F1.1 — Install & detect Claude Code  · key `config_present` (auto)
**What it is & why.** The foundation: Claude Code installed (it needs only
Node.js) and writing its config file. Nothing else in F1 matters until this is
true. track.py confirms it by finding a Claude config on the machine.
**Examples.** Install via the documented installer/npm; launch `claude` once so
it writes `~/.claude.json` or `~/.claude/settings.json`. You're talking to it
now, so this is effectively already satisfied.
**To-do / mastery plan.** 1) Install Claude Code. 2) Launch it once so config is
written. "Done" = a Claude config exists on the machine.
**Try it now / Verified.** `auto` — `py -3 scripts/track.py check F1.1` detects
`config_present`.

## F1.2 — Theme  · key `theme_set` (self)
**What it is & why.** A harsh or low-contrast theme is friction you feel every
session. Picking a comfortable one keeps you reaching for the tool.
**Examples.** Type `/theme` → an interactive picker (Light / Dark /
Light-daltonized / Dark-daltonized). Arrow to one, Enter, the UI recolors live.
**To-do / mastery plan.** 1) Run `/theme`. 2) Try light vs dark. 3) Keep the one
that's easy on your eyes. "Done" = you set a theme deliberately.
**Try it now / Verified.** Switch your theme once and confirm it takes effect.
`self` — `mark F1.2 theme_set --done`.

## F1.3 — Terminal multi-line input  · key `terminal_setup` (self)
**What it is & why.** Good prompts span multiple lines. In a **plain terminal**,
`/terminal-setup` binds **Shift+Enter** to a newline instead of submitting. In
the **VS Code / JetBrains extension** this is built in and `/terminal-setup`
doesn't exist there — Shift+Enter just works, so the environment satisfies it.
**Examples.** Plain terminal: run `/terminal-setup`, then Shift+Enter drops a
line. In the IDE extension: type a word, press Shift+Enter — you get a newline
without submitting.
**To-do / mastery plan.** 1) If in a plain terminal, run `/terminal-setup`. 2)
Confirm Shift+Enter adds a newline. "Done" = multi-line input works (auto-true in
the IDE extension).
**Try it now / Verified.** Press Shift+Enter and watch it add a line. `self` —
`mark F1.3 terminal_setup --done`.

## F1.4 — GitHub app  · key `github_app` (self)
**What it is & why.** Connecting the GitHub app lets you delegate to Claude from
GitHub itself and wire it into CI. Install is step one; *using* it is the point.
**Examples.** Connect with `/install-github-app`. Then on a GitHub issue comment
`@claude can you implement this?` (it reads the thread, writes code, opens a PR);
on a PR `@claude review this PR` or `@claude fix the failing test` (it pushes
commits to that branch). It runs as a GitHub Action, so CI can trigger it too.
**To-do / mastery plan.** 1) `/install-github-app` and authorize a repo. 2)
`@`-mention Claude on a real issue or PR at least once. "Done" = installed **and**
mentioned.
**Try it now / Verified.** Comment `@claude summarize what this issue is asking
for and suggest an approach` on a real issue and watch it respond. `self` —
`mark F1.4 github_app --done`.

## F1.5 — Allowed tools  · key `allowed_tools` (self)
**What it is & why.** The biggest day-to-day convenience win: allow-list the
commands you run constantly so Claude stops asking permission each time.
**Examples.** When Claude asks permission, choose **"Yes, and don't ask again for
`<cmd>`"**. Or edit `.claude/settings.json` directly:
```json
{ "permissions": { "allow": ["Bash(npm test:*)", "Bash(git status)", "Bash(py -3:*)"] } }
```
**To-do / mastery plan.** 1) Notice a command you approve repeatedly. 2) Pick
"don't ask again", or add a pattern to `permissions.allow`. "Done" = routine
commands run without re-prompting.
**Try it now / Verified.** Allow-list one command you use constantly. `self` —
`mark F1.5 allowed_tools --done`.

---

# F2 — Codebase Q&A (start here)

The highest-value *first* use of Claude Code isn't editing — it's asking
questions. It explores with meaning, not text-matching, so you get a wiki-style
tour. No indexing, no upload, code stays local — zero setup, ask immediately.
This is how Anthropic onboards new hires (weeks → days).

## F2.1 — Ask a real question  · key `asked_question` (self)
**What it is & why.** Before editing, interrogate the code. Pick a class or
function you don't fully understand and ask about it.
**Examples.** "Explain what `<RealClass>` does and where it's instantiated."
**To-do / mastery plan.** 1) Pick something real you don't fully get. 2) Ask
Claude about it. "Done" = you asked a genuine question about your code.
**Try it now / Verified.** Ask about a real symbol in their repo. `self` —
`mark F2.1 asked_question --done`.

## F2.2 — Deeper than search  · key `deeper_than_search` (self)
**What it is & why.** The win over Cmd+F is *meaning*: Claude traces how a thing
is built and what would break if you changed it.
**Examples.** "Explain how `<RealClass>` is constructed and what would break if I
changed its constructor." Compare the depth to a plain text search.
**To-do / mastery plan.** 1) Ask a how/why question. 2) Notice the answer reasons
about construction/usage, not string hits. "Done" = answer went deeper than
search.
**Try it now / Verified.** `self` — `mark F2.2 deeper_than_search --done`.

## F2.3 — Usage follow-up  · key `usage_followup` (self)
**What it is & why.** Following up with "how is this used across the project?"
makes Claude trace call sites and logic — and teaches you the boundary of what it
can one-shot.
**Examples.** "How is this used across the project, and which call sites are most
fragile?"
**To-do / mastery plan.** 1) After a first answer, ask a usage follow-up. 2) Let
it trace the call sites. "Done" = you got the cross-project usage logic.
**Try it now / Verified.** `self` — `mark F2.3 usage_followup --done`.

---

# F3 — Git History & Standup Reports

Source code tells you *what*; git history tells you *why*. Claude reads your
local log and the issues commits link to with no special prompting — and can
summarise what *you* shipped, the standup nobody enjoys writing.

## F3.1 — Inside a git repository  · key `in_git_repo` (auto)
**What it is & why.** The "why" lives in history, so Claude needs a repo to read.
This lesson confirms you're inside one.
**Examples.** `git rev-parse --is-inside-work-tree` → `true`.
**To-do / mastery plan.** 1) Work inside a git repo (or `git init`). "Done" =
track.py confirms a repo.
**Try it now / Verified.** `auto` — `check F3.1` detects `in_git_repo`.

## F3.2 — Explain the historical "why"  · key `history_explained` (self)
**What it is & why.** Claude digs through commits and linked issues to explain why
code is the way it is — no special prompting; it just uses git.
**Examples.** "Look at `<confusingFn>` — why does it take all these arguments?
Check the git history."
**To-do / mastery plan.** 1) Find a confusing signature/decision. 2) Ask Claude to
explain it from history. "Done" = you got the historical reasoning.
**Try it now / Verified.** `self` — `mark F3.2 history_explained --done`.

## F3.3 — What did I ship  · key `shipped_summary` (self)
**What it is & why.** Claude finds your git username and lists your commits in
plain language — paste-ready standup.
**Examples.** "Summarise my commits since Monday for standup."
**To-do / mastery plan.** 1) Ask "what did I ship this week?". 2) Get a plain-
language summary. "Done" = you received your shipped summary.
**Try it now / Verified.** `self` — `mark F3.3 shipped_summary --done`.

---

# F4 — Agentic Workflow: Plan → Edit → PR

Claude has a small, powerful toolset and strings it together itself. Handing it a
huge task cold can miss the mark — asking it to **plan first** is the easiest way
to get what you intended; then "commit push PR" automates the git plumbing.

## F4.1 — Recent commit activity  · key `recent_commits` (auto)
**What it is & why.** The loop ends in commits; this confirms the repo is live so
the workflow has somewhere real to land.
**Examples.** `git log --since=14.days --oneline` shows recent commits.
**To-do / mastery plan.** 1) Have recent commits (the practice in F4.4 creates
them). "Done" = track.py sees activity in the last 14 days.
**Try it now / Verified.** `auto` — `check F4.1`.

## F4.2 — Approve a plan first  · key `plan_approved` (self)
**What it is & why.** Asking Claude to brainstorm and plan *before* touching files
keeps you in control. No special plan mode — just ask.
**Examples.** "Before you write code, brainstorm and make a plan, then run it by
me." Read it, push back, approve.
**To-do / mastery plan.** 1) State the change. 2) Ask for a plan first. 3) Review
& approve before any file changes. "Done" = you approved a plan pre-edit.
**Try it now / Verified.** `self` — `mark F4.2 plan_approved --done`.

## F4.3 — Implement the plan  · key `edit_made` (self)
**What it is & why.** Once approved, let Claude execute — edit, run, search,
iterate. This is the agent earning its keep.
**Examples.** "Go ahead and implement the plan."
**To-do / mastery plan.** 1) Approve. 2) Let Claude make the edits. "Done" = the
approved change was implemented.
**Try it now / Verified.** `self` — `mark F4.3 edit_made --done`.

## F4.4 — commit push PR  · key `pr_created` (self)
**What it is & why.** "commit push PR" automates the tedious plumbing: branch,
commit in your repo's style, push, open the PR.
**Examples.** Just type: `commit push PR`.
**To-do / mastery plan.** 1) When happy, say "commit push PR". 2) Confirm a PR
opened. "Done" = a PR was created from your change.
**Try it now / Verified.** `self` — `mark F4.4 pr_created --done`.

---

# F5 — Teach Claude Your Tools (CLIs + MCP)

Claude shines once it can drive *your team's* tools — bash CLIs (point it at
`--help`) and MCP servers (structured integrations). An `.mcp.json` in the repo
gives every teammate the same servers automatically.

## F5.1 — Shared MCP config (.mcp.json)  · key `mcp_config` (auto)
**What it is & why.** A checked-in `.mcp.json` shares MCP servers with the whole
team. This confirms one exists in the project.
**Examples.** A repo-root `.mcp.json` listing server commands.
**To-do / mastery plan.** 1) Add an `.mcp.json` to the project. "Done" = track.py
finds it.
**Try it now / Verified.** `auto` — `check F5.1`.

## F5.2 — Teach a CLI via --help  · key `cli_taught` (self)
**What it is & why.** Name a CLI and tell Claude to read its `--help` first — it
learns the commands and drives the tool. No integration code.
**Examples.** "Use `<cli>` — run `<cli> --help` first to learn it, then …"
**To-do / mastery plan.** 1) Pick a team CLI. 2) Tell Claude to learn it via
`--help`. 3) Have it run a real command. "Done" = Claude operated your CLI.
**Try it now / Verified.** `self` — `mark F5.2 cli_taught --done`.

## F5.3 — Use an MCP server  · key `mcp_used` (self)
**What it is & why.** MCP servers are structured tool integrations (e.g. a
Puppeteer server for screenshots). Add one and Claude calls its tools directly.
**Examples.** Add a Puppeteer MCP server, then "screenshot the homepage and tell
me what's broken."
**To-do / mastery plan.** 1) Add/enable an MCP server. 2) Have Claude call one of
its tools. "Done" = you used an MCP server's tools.
**Try it now / Verified.** `self` — `mark F5.3 mcp_used --done`.

---

# F6 — Feedback Loops (let Claude check its work)

The single biggest quality lever. When Claude can *check its own work* — run
tests, screenshot a page, grab the simulator — it iterates to something that
works instead of handing you untested code.

## F6.1 — A command Claude can run  · key `test_cmd_present` (auto)
**What it is & why.** A loop needs something to run. This confirms the project
exposes a test/build command.
**Examples.** A `test` script in package.json, a `test:` Makefile target, or
pytest config.
**To-do / mastery plan.** 1) Ensure a test/build command exists. "Done" = track.py
finds one.
**Try it now / Verified.** `auto` — `check F6.1`.

## F6.2 — Iterate on feedback  · key `iterated_on_feedback` (self)
**What it is & why.** Point Claude at your tests (or a screenshot) and it verifies
and self-corrects in a loop.
**Examples.** "Implement `<change>`. After each edit, run the tests and keep
iterating until they pass."
**To-do / mastery plan.** 1) Give Claude a checker. 2) Tell it to run and iterate.
"Done" = it iterated using a test/screenshot it ran itself.
**Try it now / Verified.** `self` — `mark F6.2 iterated_on_feedback --done`.

## F6.3 — Visual coding  · key `visual_coding` (self)
**What it is & why.** Drag a UI mock into the terminal; Claude builds it and
screenshots + compares in a loop until it matches — often near-perfect in 2–3
passes.
**Examples.** Drop a mock image, "build this and screenshot until it matches."
Or wire up any checker tool.
**To-do / mastery plan.** 1) Provide a mock image (or a checker). 2) Let it loop
to match. "Done" = you tried visual coding or wired a checker.
**Try it now / Verified.** `self` — `mark F6.3 visual_coding --done`.

---

# F7 — Context Management (CLAUDE.md & friends)

Claude starts each session with no memory of your project. A `CLAUDE.md` in the
repo root is the standing brief it reads automatically. Keep it short or it just
burns context.

## F7.1 — Create a CLAUDE.md  · key `claude_md_exists` (auto)
**What it is & why.** The core of context management — a standing brief
(commands, style, key files, gotchas) auto-read each session. Check it in to
share; `CLAUDE.local.md` is for personal un-checked-in notes; nested CLAUDE.md
files load on demand.
**Examples.** A repo-root CLAUDE.md with build/test commands and "always X / never
Y" rules.
**To-do / mastery plan.** 1) Draft a short CLAUDE.md (Claude can draft it from
what it sees). 2) Refine and save at the root. "Done" = a CLAUDE.md exists.
**Try it now / Verified.** "Draft a CLAUDE.md for this project — build/test
commands, layout." `auto` — `check F7.1`.

## F7.2 — See loaded context (/memory)  · key `memory_loaded` (self)
**What it is & why.** `/memory` shows exactly which context files are loaded right
now — how you debug "why doesn't it know X?".
**Examples.** Run `/memory` and read the list of loaded files.
**To-do / mastery plan.** 1) Run `/memory`. 2) Note which files are loaded. "Done"
= you viewed loaded context.
**Try it now / Verified.** `self` — `mark F7.2 memory_loaded --done`.

## F7.3 — The '#' remember shortcut  · key `memory_shortcut` (self)
**What it is & why.** Prefix a note with `#` mid-session and Claude appends it to
your context file for you — the fastest way to grow CLAUDE.md.
**Examples.** `# always run the test suite before declaring done`.
**To-do / mastery plan.** 1) Use `#` to record a real rule. 2) Confirm it landed in
your context file. "Done" = you used `#` to remember something.
**Try it now / Verified.** `self` — `mark F7.3 memory_shortcut --done`.

## F7.4 — Custom slash command  · key `slash_command` (self)
**What it is & why.** A workflow you repeat belongs in a custom slash command in
`.claude/commands/`. Define once, invoke with `/name`; `@`-mention files to pull
them in.
**Examples.** `.claude/commands/standup.md` invoked as `/standup`.
**To-do / mastery plan.** 1) Pick a repeated workflow. 2) Add a command file. 3)
Invoke it. "Done" = you created or used a custom slash command.
**Try it now / Verified.** `self` — `mark F7.4 slash_command --done`.

---

# F8 — Speed & Keybindings

The terminal is minimal, so the fastest bindings are easy to miss. A handful turn
"neat" into "fast".

## F8.1 — '!' bash mode  · key `bash_mode` (self)
**What it is & why.** Prefix a command with `!` (e.g. `!npm run build`); its
output drops into context so Claude sees it next turn — no copy-paste.
**Examples.** `!npm test` then ask Claude to fix the failures it now sees.
**To-do / mastery plan.** 1) Run a `!` command. 2) Let Claude read the output.
"Done" = you piped command output in via `!`.
**Try it now / Verified.** `self` — `mark F8.1 bash_mode --done`.

## F8.2 — Escape to interrupt  · key `escape_interrupt` (self)
**What it is & why.** When an edit drifts, **Escape** stops it safely (never
corrupts the session); say what to change and let it redo. Escape twice jumps back
in history.
**Examples.** Mid-edit, hit Escape → "actually, keep the old signature, just add
the param".
**To-do / mastery plan.** 1) Interrupt a drifting edit with Escape. 2) Redirect it.
"Done" = you stopped and redirected an edit.
**Try it now / Verified.** `self` — `mark F8.2 escape_interrupt --done`.

## F8.3 — Shift+Tab auto-accept  · key `auto_accept` (self)
**What it is & why.** For trusted work (iterating on tests, boilerplate),
**Shift+Tab** auto-applies edits while bash still asks. You can undo later.
**Examples.** Shift+Tab, then "fill in the rest of these unit tests."
**To-do / mastery plan.** 1) Enter auto-accept for low-risk work. 2) Let edits
apply. "Done" = you used auto-accept mode.
**Try it now / Verified.** `self` — `mark F8.3 auto_accept --done`.

## F8.4 — Resume & inspect  · key `resume_session` (self)
**What it is & why.** `claude --resume` / `--continue` picks up a past session;
**Ctrl+R** expands the full output Claude sees. No work lost, nothing hidden.
**Examples.** `claude --continue` to resume; Ctrl+R to see full tool output.
**To-do / mastery plan.** 1) Resume a session or expand output with Ctrl+R. "Done"
= you used resume/continue or Ctrl+R.
**Try it now / Verified.** `self` — `mark F8.4 resume_session --done`.

---

# F9 — SDK as a Unix Utility (+ parallel)

The `-p` flag *is* the Claude Code SDK — the same engine, as a scriptable Unix
utility. Pipe in, get text/JSON out, use it anywhere. Power users run many
sessions in parallel.

## F9.1 — claude -p (pipe in/out)  · key `sdk_pipe` (self)
**What it is & why.** Give it a prompt, pipe data in, get text out — usable in CI,
incident response, pipelines.
**Examples.** `git status | claude -p "summarise these changes"` or
`git diff | claude -p "write a commit message"`.
**To-do / mastery plan.** 1) Run `claude -p` with a prompt. 2) Try piping input in.
"Done" = you used `claude -p`.
**Try it now / Verified.** `self` — `mark F9.1 sdk_pipe --done`.

## F9.2 — SDK flags & scripting  · key `sdk_flags` (self)
**What it is & why.** `--output-format json` (or streaming) lets a script process
the result; `--allowed-tools` permits specific commands unattended.
**Examples.** `git diff | claude -p "list risks" --output-format json` consumed by
a script.
**To-do / mastery plan.** 1) Add `--output-format` or `--allowed-tools`, or use it
in a script/CI. "Done" = you used SDK flags or scripted it.
**Try it now / Verified.** `self` — `mark F9.2 sdk_flags --done`.

## F9.3 — Parallel sessions  · key `parallel_sessions` (self)
**What it is & why.** Run many sessions at once — tmux/SSH, separate checkouts, or
git worktrees for isolation. How the SDK scales past one conversation.
**Examples.** A git worktree per task, or two tmux panes each running Claude.
**To-do / mastery plan.** 1) Start a second session via tmux / extra checkout /
worktree. "Done" = you ran parallel sessions.
**Try it now / Verified.** `self` — `mark F9.3 parallel_sessions --done`.

---

## Mastery & the Shaka

A **lesson** is mastered when its single check is true; `track.py master F<n>.<m>`
(or the final `mark`) prints the Shaka 🤙 for that lesson. When every lesson in a
module is mastered, the module is complete (a 🌺 line). When all 9 modules are
complete, the dashboard shows the full-Aloha banner. Honour the celebration —
it's the point.
