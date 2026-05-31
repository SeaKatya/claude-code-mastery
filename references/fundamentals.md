# Claude Code Fundamentals — Reference

Read the section for whichever fundamental you're coaching. Each has four parts:
**Why it's needed**, **How to master it** (steps), **Example**, and **How it's
verified** (which checklist items are auto-detected vs. self-confirmed, and the
exact item keys to pass to `track.py mark`).

## Contents
- [F1 — Setup & Environment Optimization](#f1)
- [F2 — Codebase Q&A](#f2)
- [F3 — Git History & Standup Reports](#f3)
- [F4 — Agentic Workflow: Plan → Edit → PR](#f4)
- [F5 — Context Management with CLAUDE.md](#f5)
- [F6 — Speed & Keybindings](#f6)
- [F7 — Feedback Loops & Advanced Tools](#f7)

---

<a id="f1"></a>
## F1 — Setup & Environment Optimization

**Why it's needed.** A tool you fight with on day one is a tool you abandon by day
three. Five minutes spent making input comfortable and connecting your repo turns
Claude Code from a novelty into something you reach for without thinking.

**How to master it.**
1. Confirm Node.js is installed, then install Claude Code per the terminal install
   command.
2. Run `terminal-setup` so **Shift+Enter** inserts a newline instead of submitting —
   essential for writing multi-line prompts.
3. Run `theme` and pick light, dark, or daltonize — whatever's easy on your eyes.
4. Run the GitHub app install (`/install-github-app`) so you can `@`-mention Claude
   on issues and pull requests.

**Example.** Open a long prompt across three lines using Shift+Enter, switch the
theme once to confirm it takes effect, then `@`-mention Claude on a test issue in
your repo and watch it respond.

**How it's verified.**
- `config_present` *(auto)* — track.py looks for a Claude config on the machine.
- `newline_without_submit` *(self)* — you confirm Shift+Enter adds a newline.
- `theme_set` *(self)* — you confirm you set a comfortable theme.
- `github_app` *(self)* — you confirm the GitHub app is connected.

---

<a id="f2"></a>
## F2 — Codebase Q&A (explore before you edit)

**Why it's needed.** The instinct is to let the AI edit immediately. The higher-value
first move is to use it as a search engine that understands *meaning*. "Where is this
instantiated and how is it used?" gets you a wiki-style tour that a `Cmd+F` for the
string never could — and that understanding makes every later edit safer.

**How to master it.**
1. Pick a class or function you don't fully understand. Ask how and where it's
   instantiated — not a text match, the actual usage.
2. Follow up: "How is this piece of code used across the project?" and let Claude
   explain the logic and call sites.
3. (Optional, Mac) Enable Dictation and double-tap the key to *talk* your questions,
   like briefing another engineer, instead of typing long prose.

**Example.** In your own repo: "Explain how `PaymentProcessor` is constructed and
every place it's used, and what would break if I changed its constructor." Compare the
depth of that answer to what a plain search would have given you.

**How it's verified.** Both items are *self*-confirmed:
- `deeper_than_search` — you got an explanation deeper than a text search.
- `usage_followup` — you asked a "how is this used?" follow-up and got the logic.

---

<a id="f3"></a>
## F3 — Git History & Standup Reports

**Why it's needed.** Source code tells you *what* the system does; git history tells
you *why* it ended up that way. Claude can read your local log and linked issues to
reconstruct decisions — and it can summarise what *you personally* shipped, which is
the standup nobody enjoys writing.

**How to master it.**
1. Find a function with a confusing signature. Ask: "Why does this function take these
   arguments?" Claude will dig through git history and linked issues to explain.
2. Ask: "What did I ship this week?" Claude identifies your git username and lists your
   commits in plain language.

**Example.** "Look at `retryWithBackoff` — why does it take both a `jitter` flag and a
`maxDelay`? Check the history." Then: "Summarise my commits since Monday for standup."

**How it's verified.**
- `in_git_repo` *(auto)* — track.py confirms you're inside a git repository.
- `history_explained` *(self)* — you confirm Claude explained the historical "why".
- `shipped_summary` *(self)* — you got a "what did I ship" summary.

---

<a id="f4"></a>
## F4 — Agentic Workflow: Plan → Edit → PR

**Why it's needed.** Turning an agent loose to edit unsupervised is how you get
surprised by a sprawling diff. Asking for a plan *first* keeps you in the driver's
seat. Once you approve, the "commit push PR" incantation automates the boring,
error-prone git and pull-request plumbing.

**How to master it.**
1. Before any non-trivial change, prompt: **"Before you write code, make a plan and
   run it by me."** Read it, push back, approve.
2. After the change is made and you're happy, say **"commit push PR"**. Claude creates
   the branch, writes the commit message, pushes, and opens the pull request.

**Example.** "Add rate-limiting to the `/login` endpoint. Before you write code, make a
plan and run it by me." Approve the plan, let it implement, then: "commit push PR".

**How it's verified.**
- `recent_commits` *(auto)* — track.py sees recent commit activity in the repo.
- `plan_approved` *(self)* — you confirm you approved a plan before any file changed.
- `pr_created` *(self)* — you confirm Claude opened a PR via "commit push PR".

---

<a id="f5"></a>
## F5 — Context Management with CLAUDE.md

**Why it's needed.** Claude starts every session with zero memory of your project. A
`CLAUDE.md` in your repo is the standing brief it reads automatically each time — your
common commands, style conventions, key file paths, and gotchas — so you stop
re-explaining the same things.

**How to master it.**
1. Create a `CLAUDE.md` in your project root. Put in the build/test commands, code
   style rules, and any "always do X / never do Y" instructions.
2. Mid-session, use the **`#` shortcut** (e.g. `# always run the test suite before
   declaring done`) to have Claude append a note to your context files for you.
3. Run `/memory` to see exactly which files and rules are currently loaded.

**Example.** Ask Claude: "Draft a CLAUDE.md for this project based on what you can see —
build commands, test command, and the directory layout." Refine it, save it, then run
`/memory` to confirm it's loaded.

**How it's verified.**
- `claude_md_exists` *(auto)* — track.py finds a `CLAUDE.md` in the project tree.
- `memory_loaded` *(self)* — `/memory` shows your project rules are loaded.
- `memory_shortcut` *(self)* — you added a note using the `#` shortcut.

---

<a id="f6"></a>
## F6 — Speed & Keybindings

**Why it's needed.** The gap between "this is neat" and "this is fast" is muscle
memory. Three keybindings compound more than any others: trusting routine work to
auto-accept, feeding shell output straight back to Claude, and stopping a bad edit the
instant you see it going sideways.

**How to master it.**
1. **`!` bash mode** — prefix a command (e.g. `!ls -la` or `!npm run build`). Claude
   sees the output on the next turn, so you don't copy-paste it.
2. **Escape to interrupt** — when an edit drifts, hit **Escape** to stop it, tell Claude
   what to change, then let it redo. Don't sit through a wrong edit.
3. **Shift+Tab auto-accept** — for work you trust (e.g. repetitive unit tests), enter
   auto-accept mode so you're not approving each diff.

**Example.** Run `!npm test`, let Claude read the failures, and ask it to fix them.
Mid-fix, if it heads the wrong way, Escape and redirect. For the boilerplate tests,
Shift+Tab and let it run.

**How it's verified.** All three are *self*-confirmed:
- `bash_mode` — you used `!` to pipe command output into context.
- `escape_undo` — you stopped an edit with Escape and redirected it.
- `auto_accept` — you used Shift+Tab auto-accept for trusted work.

---

<a id="f7"></a>
## F7 — Feedback Loops & Advanced Tools

**Why it's needed.** Claude is dramatically better when it can *check its own work*.
Hand it a test command or a way to take a screenshot and it iterates to something that
actually works, instead of returning untested code you then have to debug. This is the
single biggest quality lever.

**How to master it.**
1. **Give it a checker.** Point Claude at your test command, or set up a screenshot tool
   (e.g. a Puppeteer MCP server) so it can see the rendered UI and self-correct.
2. **Visual coding.** Drag a UI mock-up image into the terminal and ask Claude to build
   it, then let it screenshot the result and compare.
3. **SDK as a Unix tool.** Try a pipe like `git status | claude -p "summarise these
   changes"` to use Claude as a scriptable command-line utility.

**Example.** "Implement this layout [drop image]. After each change, run the tests and
take a screenshot, and keep iterating until it matches." Separately, try
`git diff | claude -p "write a commit message"`.

**How it's verified.**
- `test_cmd_present` *(auto)* — track.py finds a test/build command in your project.
- `iterated_on_feedback` *(self)* — Claude iterated using a test or screenshot it ran.
- `sdk_pipe` *(self)* — you used a `-p` pipe like `git status | claude -p "..."`.

---

## Mastery & the Shaka

A fundamental is mastered when **every** checklist item is true. At that moment
`track.py master F<n>` (or the final `mark`) prints the Shaka 🤙 — the "hang loose"
sign and a bit of Aloha spirit. When all seven are mastered, the dashboard shows the
full-Aloha banner. Honour the celebration; it's the point.
