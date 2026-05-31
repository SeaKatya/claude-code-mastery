# Claude Code Fundamentals — Reference

The nine fundamentals from Boris's Claude Code talk, in the order a new user
should meet them. Read the section for whichever fundamental you're coaching.
Each has parts that map onto the five-phase teaching flow:

- **What it is & why it's needed** — phase 1: explain how it works, first.
- **How to use it (to-do list)** — phases 2 & 3: mine this for concrete examples to
  show, then present it as the detailed, step-by-step mastery plan. Reveal only after
  the user moves past the explanation.
- **Try it now** — phase 4: something to actually do together in their real project.
- **How it's verified** — phase 5: which checklist items are auto-detected vs. self-
  confirmed, and the exact item keys to pass to `track.py mark`. Do not reach this phase
  until phases 1–3 have been delivered.

## Contents
- [F1 — Setup & Environment Optimization](#f1)
- [F2 — Codebase Q&A](#f2)
- [F3 — Git History & Standup Reports](#f3)
- [F4 — Agentic Workflow: Plan → Edit → PR](#f4)
- [F5 — Teach Claude Your Tools (CLIs + MCP)](#f5)
- [F6 — Feedback Loops](#f6)
- [F7 — Context Management (CLAUDE.md & friends)](#f7)
- [F8 — Speed & Keybindings](#f8)
- [F9 — SDK as a Unix Utility (+ parallel)](#f9)

---

<a id="f1"></a>
## F1 — Setup & Environment Optimization

**What it is & why it's needed.** Claude Code is a free-form, fully agentic tool —
you open it to a bare prompt. A few minutes of setup removes the day-one friction
(awkward newlines, a harsh theme, repeated permission prompts) so it becomes a
daily habit instead of a novelty. All you need to run it is Node.js.

**How to use it (to-do list).**
1. Install Claude Code (needs Node.js). In a **plain terminal**, run `/terminal-setup`
   so **Shift+Enter** inserts a newline instead of submitting. *Note:* in the **VS Code
   / JetBrains extension** this is already built in and `/terminal-setup` doesn't exist
   there — Shift+Enter just works, so this item is satisfied by the environment.
2. Run `/theme` and pick light, dark, or daltonize — whatever's easy on your eyes.
3. Run `/install-github-app` to connect the GitHub app — then actually *use* it (see
   "Using the GitHub app" below). It's not done at install; the point is the workflows.
4. Customize your **allowed tools** so commands you run constantly aren't re-prompted
   every time. When Claude asks permission, choose "Yes, and don't ask again", or edit
   `.claude/settings.json` `permissions.allow` directly (big convenience win).
5. *(Optional, macOS)* Enable Dictation and double-tap the key to **speak** your
   prompts like you'd brief another engineer — specific spoken prompts work great.

**Using the GitHub app (what to do after install).** The app lets you delegate to
Claude from GitHub itself and wires it into CI:
- **`@`-mention on an issue:** comment `@claude can you implement this?` on a GitHub
  issue — Claude reads the thread, writes the code, and opens a PR with the fix.
- **`@`-mention on a pull request:** comment `@claude review this PR` or `@claude fix
  the failing test` on a PR; it pushes commits to that PR's branch.
- **Ask for an explanation:** `@claude why might this change break anything?` for a
  review-style answer inline on the PR.
- **Automate with a workflow:** the app runs as a GitHub Action, so you can trigger
  these from CI (e.g. auto-label or triage issues) — the same mechanism Claude Code's
  own repo uses to label issues.

**Try it now.** Pick a real (or test) issue in your repo and comment
`@claude summarize what this issue is asking for and suggest an approach`, then watch
it respond on GitHub. Also switch your theme once to confirm it takes effect.

**How it's verified.**
- `config_present` *(auto)* — track.py finds a Claude config on the machine.
- `terminal_setup` *(self)* — Shift+Enter adds a newline (auto-satisfied in the IDE
  extension; run `/terminal-setup` only in a plain terminal).
- `theme_set` *(self)* — you set a comfortable theme.
- `github_app` *(self)* — the app is connected **and** you've `@`-mentioned Claude on
  an issue or PR at least once.
- `allowed_tools` *(self)* — you allow-listed routine commands.

---

<a id="f2"></a>
## F2 — Codebase Q&A (start here)

**What it is & why it's needed.** The highest-value *first* use of Claude Code isn't
editing — it's asking questions about your codebase. It explores and explains with
meaning, not text-matching, so you get a wiki-style tour instead of a `Cmd+F` hit.
This is exactly how Anthropic onboards new hires (cutting onboarding from weeks to
days). There's no indexing and no upload — your code stays local, so there's zero
setup and you can ask immediately.

**How to use it (to-do list).**
1. Pick a class or function you don't fully understand. Ask how and where it's
   instantiated — the actual usage, not a string match.
2. Follow up: "How is this used across the project?" and let Claude trace the call
   sites and logic.
3. Use this to learn the *boundary* of what Claude can one-shot vs. where you need
   to guide it — that intuition makes every later step better.

**Try it now.** In their repo: "Explain how `<RealClass>` is constructed and every
place it's used, and what would break if I changed its constructor." Compare the
depth to what a plain search would have given.

**How it's verified.** All self-confirmed:
- `asked_question` — you asked Claude a real question about your code.
- `deeper_than_search` — the answer went deeper than a text search.
- `usage_followup` — you asked a "how is this used?" follow-up and got the logic.

---

<a id="f3"></a>
## F3 — Git History & Standup Reports

**What it is & why it's needed.** Source code tells you *what* the system does; git
history tells you *why* it got that way. Claude reads your local log and the issues
commits link to, with no special prompting — the model just knows to use git. It can
also summarise what *you personally* shipped, which is the standup nobody enjoys
writing.

**How to use it (to-do list).**
1. Find a function with a confusing signature. Ask: "Why does this take these
   arguments? Check the history." Claude digs through commits and linked issues.
2. Ask: "What did I ship this week?" Claude finds your git username and lists your
   commits in plain language — copy it straight into your standup doc.

**Try it now.** "Look at `<confusingFn>` — why does it take all these arguments? Check
the git history." Then: "Summarise my commits since Monday for standup."

**How it's verified.**
- `in_git_repo` *(auto)* — track.py confirms you're inside a git repository.
- `history_explained` *(self)* — Claude explained the historical "why".
- `shipped_summary` *(self)* — you got a "what did I ship" summary.

---

<a id="f4"></a>
## F4 — Agentic Workflow: Plan → Edit → PR

**What it is & why it's needed.** Claude has a small, powerful toolset (edit files,
run bash, search) and strings them together itself. But handing it a huge task cold
can produce something that isn't what you wanted. Asking it to **plan first** is the
easiest way to get the result you intended — and once you approve, "commit push PR"
automates the boring, error-prone git/PR plumbing.

**How to use it (to-do list).**
1. Before any non-trivial change: **"Before you write code, brainstorm and make a
   plan, then run it by me."** Read it, push back, approve. (No special plan mode
   needed — just ask.)
2. Let Claude implement the approved plan.
3. When you're happy: **"commit push PR"** — it makes the branch, writes the commit
   in your repo's style, pushes, and opens the pull request.

**Try it now.** "Add `<small feature>` to `<file>`. Before you write code, make a plan
and run it by me." Approve, let it implement, then: "commit push PR".

**How it's verified.**
- `recent_commits` *(auto)* — track.py sees recent commit activity.
- `plan_approved` *(self)* — you approved a plan before any file changed.
- `edit_made` *(self)* — Claude implemented the change.
- `pr_created` *(self)* — "commit push PR" opened a PR.

---

<a id="f5"></a>
## F5 — Teach Claude Your Tools (CLIs + MCP)

**What it is & why it's needed.** Claude Code really shines once it can drive *your
team's* tools. Two kinds: **bash CLIs** (tell Claude about a command and point it at
`--help`) and **MCP servers** (structured tool integrations). Give Claude the tools
your team already uses on a codebase and it operates them on your behalf — and an
`.mcp.json` checked into the repo means every teammate gets them automatically.

**How to use it (to-do list).**
1. Pick a CLI your team uses. Tell Claude: "Use `<cli>` — run `<cli> --help` first to
   learn it," and let it figure out the commands.
2. Add an MCP server (e.g. a Puppeteer server for browser screenshots) and ask Claude
   to use its tools.
3. Drop frequently-used tool instructions into CLAUDE.md (see F7) so Claude remembers
   them across sessions, and check `.mcp.json` into the repo to share with the team.

**Try it now.** Teach Claude one real CLI from their workflow via `--help`, or add one
MCP server and have Claude call a tool from it.

**How it's verified.**
- `mcp_config` *(auto)* — track.py finds an `.mcp.json` in the project.
- `cli_taught` *(self)* — you taught Claude a CLI via `--help` / had it run one.
- `mcp_used` *(self)* — you added or used an MCP server's tools.

---

<a id="f6"></a>
## F6 — Feedback Loops (let Claude check its work)

**What it is & why it's needed.** This is the single biggest quality lever. When Claude
can *check its own work* — run unit tests, screenshot a web page with Puppeteer, grab
the iOS simulator — it iterates to something that actually works instead of handing
you untested code. Give it a mock and a way to see the result and it'll often get a UI
almost perfect after two or three iterations.

**How to use it (to-do list).**
1. **Give it a checker.** Point Claude at your test command, or set up a screenshot
   tool, so it can verify and self-correct.
2. **Visual coding.** Drag a UI mock-up image into the terminal, ask Claude to build
   it, and let it screenshot + compare in a loop until it matches.
3. Whatever your domain (tests, integration, screenshots) — give it a way to *see* its
   result and tell it to iterate.

**Try it now.** "Implement `<change>`. After each edit, run the tests (or take a
screenshot) and keep iterating until it passes/matches."

**How it's verified.**
- `test_cmd_present` *(auto)* — track.py finds a test/build command.
- `iterated_on_feedback` *(self)* — Claude iterated using a test/screenshot it ran.
- `visual_coding` *(self)* — you tried a mock image, or wired up a checker tool.

---

<a id="f7"></a>
## F7 — Context Management (CLAUDE.md & friends)

**What it is & why it's needed.** Claude starts every session with no memory of your
project. A `CLAUDE.md` in your repo root is the standing brief it reads automatically
each session — common commands, style guide, key files, gotchas. The more good context
you give it, the smarter its decisions. Keep it short, or it just burns context.

**How to use it (to-do list).**
1. Create a `CLAUDE.md` in your project root: build/test commands, code-style rules,
   important files, "always do X / never do Y". Check it in to share with the team.
   (A `CLAUDE.local.md` is for personal, un-checked-in notes; nested CLAUDE.md files
   load on demand when Claude works in those directories.)
2. Run `/memory` to see exactly which context files are currently loaded.
3. Use the **`#` shortcut** mid-session (e.g. `# always run the test suite before
   declaring done`) to have Claude append a note to your context for you.
4. Add a custom **slash command** in `.claude/commands/` for a workflow you repeat;
   `@`-mention files to pull them into context.

**Try it now.** "Draft a CLAUDE.md for this project from what you can see — build
command, test command, directory layout." Refine and save it, then run `/memory`.

**How it's verified.**
- `claude_md_exists` *(auto)* — track.py finds a `CLAUDE.md` in the project.
- `memory_loaded` *(self)* — `/memory` showed your loaded files.
- `memory_shortcut` *(self)* — you used `#` to remember something.
- `slash_command` *(self)* — you created/used a custom slash command.

---

<a id="f8"></a>
## F8 — Speed & Keybindings

**What it is & why it's needed.** The terminal is minimal, so the fastest bindings are
easy to miss. A handful of them turn "neat" into "fast": trust routine work to
auto-accept, pipe shell output straight into context, and stop a bad edit the instant
you see it drift.

**How to use it (to-do list).**
1. **`!` bash mode** — prefix a command (`!npm run build`); its output goes into
   context so Claude sees it next turn without copy-paste.
2. **Escape to interrupt** — when an edit drifts, hit **Escape** to stop it safely
   (never corrupts the session), say what to change, and let it redo. **Escape twice**
   jumps back in history.
3. **Shift+Tab auto-accept** — for trusted work (e.g. iterating on unit tests), edits
   auto-apply; bash still asks. You can always have Claude undo later.
4. Resume work with `claude --resume` / `--continue`; hit **Ctrl+R** to see the full
   output Claude sees. (`#` to remember and `@` to mention files live here too.)

**Try it now.** Run `!<your test command>`, let Claude read the failures and fix them;
if it heads the wrong way, Escape and redirect. For boilerplate, Shift+Tab and let it run.

**How it's verified.** All self-confirmed:
- `bash_mode` — you used `!` to pipe command output into context.
- `escape_interrupt` — you stopped an edit with Escape and redirected it.
- `auto_accept` — you used Shift+Tab auto-accept for trusted work.
- `resume_session` — you used `--resume`/`--continue` or `Ctrl+R`.

---

<a id="f9"></a>
## F9 — SDK as a Unix Utility (+ parallel)

**What it is & why it's needed.** The `-p` flag *is* the Claude Code SDK — the same
engine Claude Code runs on. Think of it as a super-intelligent Unix utility: give it a
prompt, pipe data in, get text or JSON out, use it anywhere (CI, incident response,
pipelines). Power users also run **many sessions in parallel** to get more done at once.

**How to use it (to-do list).**
1. Run a one-shot: `claude -p "summarise the changes"` — or pipe into it, e.g.
   `git status | claude -p "summarise these changes"` or `git diff | claude -p "write a
   commit message"`.
2. Add flags: `--allowed-tools` to permit specific commands, `--output-format json`
   (or streaming JSON) when you need to process the result in a script.
3. Go parallel: run multiple sessions via tmux/SSH, separate checkouts of the repo, or
   **git worktrees** for isolation.

**Try it now.** `git diff | claude -p "write a commit message for these changes"`, then
try one parallel session in a second terminal or a git worktree.

**How it's verified.** All self-confirmed:
- `sdk_pipe` — you used `claude -p`, e.g. piping `git status` into it.
- `sdk_flags` — you tried `--output-format`/`--allowed-tools` or used it in a script.
- `parallel_sessions` — you ran parallel sessions (tmux / checkouts / worktrees).

---

## Mastery & the Shaka

A fundamental is mastered when **every** checklist item is true. At that moment
`track.py master F<n>` (or the final `mark`) prints the Shaka 🤙 — the "hang loose"
sign and a bit of Aloha spirit. When all nine are mastered, the dashboard shows the
full-Aloha banner. Honour the celebration; it's the point.
