#!/usr/bin/env python3
"""
Claude Code Mastery — progress tracker.

Creates and maintains a local progress file (.claude-code-mastery.json) in the
current directory and walks a learner through the fundamentals from Boris's
Claude Code talk. The fundamentals are organised into 9 modules (F1..F9), each
split into small, single-focus LESSONS (F1.1, F1.2, ...). Each lesson is taught
on its own and earns its own Shaka when its check passes. Completing every
lesson in a module completes that module.

Usage:
    python track.py init                   # create the progress file (idempotent)
    python track.py status                 # dashboard: modules + lessons
    python track.py detail F1              # a module: its lessons
    python track.py detail F1.2            # a lesson: why + its check
    python track.py check F1.1             # run automated checks for a lesson/module
    python track.py mark F1.2 theme_set --done   # confirm a self item (--undo to revert)
    python track.py master F1.2            # finalise a lesson -> Shaka if its check passes
    python track.py shaka                  # print the Shaka sign
    python track.py reset --force          # wipe progress and start over

The progress file is plain JSON and safe to commit or .gitignore — your call.
"""

import argparse
import datetime as _dt
import json
import subprocess
import sys
from pathlib import Path

# Windows consoles default to cp1252, which can't encode the em-dashes, box
# characters, and emoji this script prints — force UTF-8 so output never breaks.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

PROGRESS_FILENAME = ".claude-code-mastery.json"
SCHEMA_VERSION = 3


# --------------------------------------------------------------------------- #
# Modules — the 9 fundamentals, used purely for grouping in the dashboard.
# --------------------------------------------------------------------------- #
MODULES = {
    "F1": "Setup & Environment Optimization",
    "F2": "Codebase Q&A (start here)",
    "F3": "Git History & Standup Reports",
    "F4": "Agentic Workflow: Plan -> Edit -> PR",
    "F5": "Teach Claude Your Tools (CLIs + MCP)",
    "F6": "Feedback Loops (let Claude check its work)",
    "F7": "Context Management (CLAUDE.md & friends)",
    "F8": "Speed & Keybindings",
    "F9": "SDK as a Unix Utility (+ parallel)",
}


# --------------------------------------------------------------------------- #
# Lessons — single source of truth. Each lesson is one teachable unit and
# carries exactly one verification item:
#   key   -> the item key (also what auto_check() keys off, unchanged from v2)
#   kind  -> "auto" (track.py can detect it) | "self" (the learner confirms it)
# A lesson is mastered when its item is true. The lesson's `why` doubles as the
# one-line point used while teaching; the full prose lives in
# references/fundamentals.md.
# --------------------------------------------------------------------------- #
LESSONS = {
    # ---- F1 — Setup & Environment Optimization ---------------------------- #
    "F1.1": {
        "module": "F1",
        "title": "Install & detect Claude Code",
        "key": "config_present", "kind": "auto",
        "label": "Claude Code installed & config detected on this machine",
        "why": "Everything else depends on Claude Code actually being installed (it needs "
               "only Node.js) and writing its config. This lesson confirms the foundation "
               "is in place before you tune anything on top of it.",
    },
    "F1.2": {
        "module": "F1",
        "title": "Theme",
        "key": "theme_set", "kind": "self",
        "label": "Picked a comfortable theme via /theme (light / dark / daltonize)",
        "why": "A harsh or low-contrast theme is friction you feel every single session. "
               "Thirty seconds in /theme makes the tool easy on your eyes so you keep "
               "reaching for it.",
    },
    "F1.3": {
        "module": "F1",
        "title": "Terminal multi-line input",
        "key": "terminal_setup", "kind": "self",
        "label": "Ran /terminal-setup so Shift+Enter inserts a newline (or it works already)",
        "why": "Briefing Claude well means writing more than one line. /terminal-setup binds "
               "Shift+Enter to a newline in a plain terminal; in the VS Code / JetBrains "
               "extension it already works, so the environment satisfies it.",
    },
    "F1.4": {
        "module": "F1",
        "title": "GitHub app",
        "key": "github_app", "kind": "self",
        "label": "Installed the GitHub app AND @mentioned Claude on an issue/PR",
        "why": "Connecting the GitHub app lets you delegate to Claude from GitHub itself — "
               "@mention it on an issue or PR and it reads the thread, writes code, and "
               "pushes commits. Install is step one; using it is the point.",
    },
    "F1.5": {
        "module": "F1",
        "title": "Allowed tools",
        "key": "allowed_tools", "kind": "self",
        "label": "Customized allowed tools so routine commands aren't re-prompted",
        "why": "The biggest day-to-day convenience win: allow-list the commands you run "
               "constantly so Claude stops asking permission every time. 'Yes, and don't "
               "ask again', or edit .claude/settings.json permissions.allow directly.",
    },

    # ---- F2 — Codebase Q&A ------------------------------------------------ #
    "F2.1": {
        "module": "F2",
        "title": "Ask a real question",
        "key": "asked_question", "kind": "self",
        "label": "Asked Claude a real question about your codebase",
        "why": "The highest-value first use of Claude Code isn't editing — it's asking. No "
               "indexing, no upload, code stays local, so you can interrogate a class or "
               "function the moment you open it.",
    },
    "F2.2": {
        "module": "F2",
        "title": "Deeper than search",
        "key": "deeper_than_search", "kind": "self",
        "label": "Got an answer deeper than a text search (how something is built/used)",
        "why": "Claude explores with meaning, not string matching. The win is an answer that "
               "traces how something is constructed and what would break if you changed it — "
               "a wiki-style tour a Cmd+F can't give.",
    },
    "F2.3": {
        "module": "F2",
        "title": "Usage follow-up",
        "key": "usage_followup", "kind": "self",
        "label": "Asked a 'how is this used across the project?' follow-up",
        "why": "Following up with 'how is this used across the project?' makes Claude trace "
               "the call sites and logic. Doing this teaches you the boundary of what it can "
               "one-shot — intuition that makes every later step better.",
    },

    # ---- F3 — Git History & Standup Reports ------------------------------- #
    "F3.1": {
        "module": "F3",
        "title": "Inside a git repository",
        "key": "in_git_repo", "kind": "auto",
        "label": "Working inside a git repository",
        "why": "Git history is where the 'why' lives. This lesson confirms you're inside a "
               "repo so Claude has a log and linked issues to read — the raw material for "
               "the next two lessons.",
    },
    "F3.2": {
        "module": "F3",
        "title": "Explain the historical 'why'",
        "key": "history_explained", "kind": "self",
        "label": "Claude explained the historical 'why' of a confusing function",
        "why": "Source code tells you what the system does; the commits tell you why it got "
               "that way. Claude reads the log and the issues commits link to with no special "
               "prompting — it just knows to use git.",
    },
    "F3.3": {
        "module": "F3",
        "title": "What did I ship",
        "key": "shipped_summary", "kind": "self",
        "label": "Got a 'what did I ship this week?' summary of your commits",
        "why": "Claude can find your git username and summarise what YOU personally shipped in "
               "plain language — the standup nobody enjoys writing, generated from the log "
               "and ready to paste.",
    },

    # ---- F4 — Agentic Workflow: Plan -> Edit -> PR ------------------------ #
    "F4.1": {
        "module": "F4",
        "title": "Recent commit activity",
        "key": "recent_commits", "kind": "auto",
        "label": "Repository has recent commit activity",
        "why": "The Plan->Edit->PR loop ends in commits. This lesson confirms the repo is "
               "live with recent activity, so the workflow you're about to practise has "
               "somewhere real to land.",
    },
    "F4.2": {
        "module": "F4",
        "title": "Approve a plan first",
        "key": "plan_approved", "kind": "self",
        "label": "Asked for a plan and approved it BEFORE any file changed",
        "why": "Handing Claude a big task cold can produce something you didn't want. Asking "
               "it to brainstorm and plan first — and approving that plan before any file "
               "changes — is the easiest way to get the result you intended.",
    },
    "F4.3": {
        "module": "F4",
        "title": "Implement the plan",
        "key": "edit_made", "kind": "self",
        "label": "Let Claude implement the approved change",
        "why": "Claude has a small, powerful toolset (edit, run bash, search) and strings the "
               "steps together itself. Once the plan is approved, letting it implement is "
               "where the agent earns its keep.",
    },
    "F4.4": {
        "module": "F4",
        "title": "commit push PR",
        "key": "pr_created", "kind": "self",
        "label": "Used 'commit push PR' to branch, commit, push & open a PR",
        "why": "When you're happy, 'commit push PR' automates the boring, error-prone git "
               "plumbing: it makes the branch, writes the commit in your repo's style, "
               "pushes, and opens the pull request.",
    },

    # ---- F5 — Teach Claude Your Tools ------------------------------------- #
    "F5.1": {
        "module": "F5",
        "title": "Shared MCP config (.mcp.json)",
        "key": "mcp_config", "kind": "auto",
        "label": "An .mcp.json exists in the project (shared MCP servers)",
        "why": "An .mcp.json checked into the repo means every teammate gets the same MCP "
               "servers automatically. This lesson confirms that shared config exists in the "
               "project.",
    },
    "F5.2": {
        "module": "F5",
        "title": "Teach a CLI via --help",
        "key": "cli_taught", "kind": "self",
        "label": "Told Claude about a CLI and had it learn via --help / run it",
        "why": "The simplest way to extend Claude: name a CLI your team uses and tell it to "
               "run `<cli> --help` first. It learns the commands and drives the tool on your "
               "behalf — no integration code required.",
    },
    "F5.3": {
        "module": "F5",
        "title": "Use an MCP server",
        "key": "mcp_used", "kind": "self",
        "label": "Added or used an MCP server's tools in a session",
        "why": "MCP servers are structured tool integrations (e.g. a Puppeteer server for "
               "browser screenshots). Add one and Claude can call its tools directly — the "
               "richer cousin of teaching it a CLI.",
    },

    # ---- F6 — Feedback Loops ---------------------------------------------- #
    "F6.1": {
        "module": "F6",
        "title": "A command Claude can run",
        "key": "test_cmd_present", "kind": "auto",
        "label": "Project exposes a test/build command Claude can run",
        "why": "A feedback loop needs something to run. This lesson confirms the project "
               "exposes a test or build command Claude can execute to check its own work in "
               "the next lessons.",
    },
    "F6.2": {
        "module": "F6",
        "title": "Iterate on feedback",
        "key": "iterated_on_feedback", "kind": "self",
        "label": "Claude iterated on a change using a test or screenshot it ran itself",
        "why": "The single biggest quality lever: when Claude can run your tests (or screenshot "
               "a page) it iterates to something that actually works instead of handing you "
               "untested code. Point it at the checker and tell it to keep going.",
    },
    "F6.3": {
        "module": "F6",
        "title": "Visual coding",
        "key": "visual_coding", "kind": "self",
        "label": "Tried visual coding (dropped a mock image) OR wired up a checker tool",
        "why": "Drag a UI mock-up into the terminal, ask Claude to build it, and let it "
               "screenshot and compare in a loop until it matches — often near-perfect after "
               "two or three iterations. Give it a way to SEE its result.",
    },

    # ---- F7 — Context Management ------------------------------------------ #
    "F7.1": {
        "module": "F7",
        "title": "Create a CLAUDE.md",
        "key": "claude_md_exists", "kind": "auto",
        "label": "A CLAUDE.md exists in the project",
        "why": "CLAUDE.md is the standing brief Claude auto-reads every session — commands, "
               "style, key files, gotchas. Creating one (and checking it in) is the core of "
               "context management. Keep it short or it just burns context.",
    },
    "F7.2": {
        "module": "F7",
        "title": "See loaded context (/memory)",
        "key": "memory_loaded", "kind": "self",
        "label": "Ran /memory to see which context files are loaded",
        "why": "/memory shows exactly which context files are loaded right now — root "
               "CLAUDE.md, nested ones, personal CLAUDE.local.md. Knowing what Claude is "
               "actually reading is how you debug 'why doesn't it know X?'.",
    },
    "F7.3": {
        "module": "F7",
        "title": "The '#' remember shortcut",
        "key": "memory_shortcut", "kind": "self",
        "label": "Used the '#' shortcut to remember something mid-session",
        "why": "Mid-session, prefix a note with '#' (e.g. '# always run the tests before "
               "declaring done') and Claude appends it to your context file for you — the "
               "fastest way to grow CLAUDE.md without leaving the prompt.",
    },
    "F7.4": {
        "module": "F7",
        "title": "Custom slash command",
        "key": "slash_command", "kind": "self",
        "label": "Created or used a custom slash command (.claude/commands)",
        "why": "A workflow you repeat belongs in a custom slash command in .claude/commands. "
               "Define it once and invoke it with /name; @-mention files to pull them into "
               "context as part of the command.",
    },

    # ---- F8 — Speed & Keybindings ----------------------------------------- #
    "F8.1": {
        "module": "F8",
        "title": "'!' bash mode",
        "key": "bash_mode", "kind": "self",
        "label": "Used '!' to run a command and pipe its output into context",
        "why": "Prefix a command with '!' (e.g. !npm run build) and its output drops straight "
               "into context, so Claude sees it next turn with no copy-paste. The fastest way "
               "to show Claude what just happened.",
    },
    "F8.2": {
        "module": "F8",
        "title": "Escape to interrupt",
        "key": "escape_interrupt", "kind": "self",
        "label": "Hit Escape to stop an edit, then redirected it",
        "why": "When an edit drifts, hit Escape to stop it safely — it never corrupts the "
               "session. Say what to change and let it redo. Escape twice jumps back through "
               "history. This keeps you in control without starting over.",
    },
    "F8.3": {
        "module": "F8",
        "title": "Shift+Tab auto-accept",
        "key": "auto_accept", "kind": "self",
        "label": "Entered auto-accept mode (Shift+Tab) for trusted work",
        "why": "For work you trust (iterating on unit tests, boilerplate), Shift+Tab auto-"
               "applies edits while bash still asks. You can always have Claude undo later. "
               "Trust routine work to run so you only watch the interesting parts.",
    },
    "F8.4": {
        "module": "F8",
        "title": "Resume & inspect",
        "key": "resume_session", "kind": "self",
        "label": "Resumed a session (--resume / --continue) or viewed full output (Ctrl+R)",
        "why": "claude --resume / --continue picks up a past session where you left it; Ctrl+R "
               "expands the full output Claude sees. Together they mean no work is ever lost "
               "and nothing is hidden from you.",
    },

    # ---- F9 — SDK as a Unix Utility --------------------------------------- #
    "F9.1": {
        "module": "F9",
        "title": "claude -p (pipe in/out)",
        "key": "sdk_pipe", "kind": "self",
        "label": "Used `claude -p`, e.g. `git status | claude -p \"summarise\"`",
        "why": "The -p flag IS the Claude Code SDK — the same engine, as a scriptable Unix "
               "utility. Pipe data in, get text out: `git diff | claude -p \"write a commit "
               "message\"`. Use it anywhere a command-line tool fits.",
    },
    "F9.2": {
        "module": "F9",
        "title": "SDK flags & scripting",
        "key": "sdk_flags", "kind": "self",
        "label": "Tried --output-format / --allowed-tools, or used it in a script/CI",
        "why": "Add --output-format json (or streaming) when a script needs to process the "
               "result, and --allowed-tools to permit specific commands unattended. This is "
               "what turns `claude -p` into a building block for CI and pipelines.",
    },
    "F9.3": {
        "module": "F9",
        "title": "Parallel sessions",
        "key": "parallel_sessions", "kind": "self",
        "label": "Ran parallel sessions (tmux / extra checkouts / git worktrees)",
        "why": "Power users run many sessions at once to get more done — via tmux/SSH, "
               "separate checkouts of the repo, or git worktrees for isolation. Parallelism "
               "is how the SDK scales past one conversation.",
    },
}

LESSON_ORDER = list(LESSONS.keys())
MODULE_ORDER = list(MODULES.keys())


def lessons_in(module_id: str) -> list[str]:
    return [lid for lid in LESSON_ORDER if LESSONS[lid]["module"] == module_id]


# --------------------------------------------------------------------------- #
# Storage
# --------------------------------------------------------------------------- #
def progress_path() -> Path:
    return Path.cwd() / PROGRESS_FILENAME


def now_iso() -> str:
    return _dt.datetime.now().isoformat(timespec="seconds")


def fresh_state() -> dict:
    lessons = {}
    for lid in LESSON_ORDER:
        spec = LESSONS[lid]
        lessons[lid] = {
            "title": spec["title"],
            "module": spec["module"],
            "status": "not_started",
            "mastered_at": None,
            "checklist": {spec["key"]: False},
        }
    return {
        "schema_version": SCHEMA_VERSION,
        "created": now_iso(),
        "updated": now_iso(),
        "lessons": lessons,
    }


def _collect_old_item_values(state: dict) -> dict:
    """Pull every earned checklist value (by item key) from any prior schema so
    a migration can preserve progress. Handles both the v2 'fundamentals' shape
    and the current 'lessons' shape."""
    earned = {}
    for container_key in ("fundamentals", "lessons"):
        container = state.get(container_key, {})
        if not isinstance(container, dict):
            continue
        for node in container.values():
            cl = node.get("checklist", {}) if isinstance(node, dict) else {}
            for k, v in cl.items():
                if v:
                    earned[k] = True
    return earned


def _migrate(state: dict) -> bool:
    """Bring an older progress file up to the lesson-based schema, preserving
    every checklist value the user already earned (matched by item key)."""
    needs = (
        state.get("schema_version") != SCHEMA_VERSION
        or "lessons" not in state
        or "fundamentals" in state
    )
    if not needs:
        return False

    earned = _collect_old_item_values(state)
    lessons = {}
    for lid in LESSON_ORDER:
        spec = LESSONS[lid]
        lessons[lid] = {
            "title": spec["title"],
            "module": spec["module"],
            "status": "not_started",
            "mastered_at": None,
            "checklist": {spec["key"]: bool(earned.get(spec["key"], False))},
        }
    state.pop("fundamentals", None)
    state["lessons"] = lessons
    state["schema_version"] = SCHEMA_VERSION
    state.setdefault("created", now_iso())
    for lid in LESSON_ORDER:
        _recompute_status(state, lid)
    return True


def load_state() -> dict:
    p = progress_path()
    if not p.exists():
        print(f"No progress file found at {p}. Run:  python track.py init")
        sys.exit(1)
    try:
        state = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"Could not read progress file ({e}). You may need to reset.")
        sys.exit(1)
    if _migrate(state):
        save_state(state)
    return state


def save_state(state: dict) -> None:
    state["updated"] = now_iso()
    progress_path().write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# Automated checks (best-effort, never crash) — keyed by item key, unchanged.
# --------------------------------------------------------------------------- #
def _git(*args) -> tuple[bool, str]:
    try:
        out = subprocess.run(
            ["git", *args], capture_output=True, text=True, timeout=8
        )
        return out.returncode == 0, out.stdout.strip()
    except Exception:
        return False, ""


def _find_upwards(filename: str, start: Path) -> Path | None:
    cur = start.resolve()
    for parent in [cur, *cur.parents]:
        candidate = parent / filename
        if candidate.exists():
            return candidate
    return None


def _exists_in_tree_or_root(filename: str) -> bool:
    cwd = Path.cwd()
    if _find_upwards(filename, cwd):
        return True
    ok, root = _git("rev-parse", "--show-toplevel")
    return bool(ok and root and (Path(root) / filename).exists())


def auto_check(item_key: str) -> bool | None:
    """Return True/False for a known auto item, or None if undetermined."""
    cwd = Path.cwd()

    if item_key == "config_present":
        home = Path.home()
        for c in [home / ".claude.json", home / ".claude" / "settings.json",
                  home / ".config" / "claude" / "settings.json"]:
            if c.exists():
                return True
        return False

    if item_key == "in_git_repo":
        ok, val = _git("rev-parse", "--is-inside-work-tree")
        return ok and val == "true"

    if item_key == "recent_commits":
        ok, val = _git("log", "--since=14.days", "--oneline")
        if not ok:
            return None
        return bool(val.strip())

    if item_key == "claude_md_exists":
        return _exists_in_tree_or_root("CLAUDE.md")

    if item_key == "mcp_config":
        return _exists_in_tree_or_root(".mcp.json")

    if item_key == "test_cmd_present":
        pkg = _find_upwards("package.json", cwd)
        if pkg:
            try:
                data = json.loads(pkg.read_text(encoding="utf-8"))
                if data.get("scripts", {}).get("test"):
                    return True
            except Exception:
                pass
        mk = _find_upwards("Makefile", cwd)
        if mk:
            try:
                if "test:" in mk.read_text(encoding="utf-8"):
                    return True
            except Exception:
                pass
        for cfg in ("pytest.ini", "tox.ini", "pyproject.toml"):
            f = _find_upwards(cfg, cwd)
            if f:
                try:
                    txt = f.read_text(encoding="utf-8")
                    if "pytest" in txt or "[tool.pytest" in txt:
                        return True
                except Exception:
                    pass
        return False

    return None


def run_auto_checks(state: dict, lid: str) -> list[str]:
    """Run the auto check for a lesson (if it has one), update state, return notes."""
    notes = []
    spec = LESSONS[lid]
    if spec["kind"] == "auto":
        key = spec["key"]
        result = auto_check(key)
        if result is True:
            state["lessons"][lid]["checklist"][key] = True
            notes.append(f"  [auto PASS] {spec['label']}")
        elif result is False:
            notes.append(f"  [auto  --] {spec['label']}  (not detected yet)")
        else:
            notes.append(f"  [auto  ??] {spec['label']}  (could not determine)")
    _recompute_status(state, lid)
    return notes


# --------------------------------------------------------------------------- #
# Status logic
# --------------------------------------------------------------------------- #
def _recompute_status(state: dict, lid: str) -> None:
    cl = state["lessons"][lid]["checklist"]
    done = sum(1 for v in cl.values() if v)
    total = len(cl)
    f = state["lessons"][lid]
    if done == total and total > 0:
        if f["status"] != "mastered":
            f["status"] = "mastered"
            f["mastered_at"] = now_iso()
    elif done == 0:
        f["status"] = "not_started"
        f["mastered_at"] = None
    else:
        f["status"] = "in_progress"
        f["mastered_at"] = None


STATUS_ICON = {"not_started": "[ ]", "in_progress": "[~]", "mastered": "[x] 🤙"}


# --------------------------------------------------------------------------- #
# The Shaka 🤙
# --------------------------------------------------------------------------- #
SHAKA = r"""
        🤙  S H A K A !  🤙
   ============================
        __
       /  \
      |    |        Aloha spirit, you earned it.
      |    |___
      |        \___
      |            \___
       \               \
        |               |   {title}
        |               |   M A S T E R E D
        |               |
   ============================
     Hang loose. On to the next one, braddah.
"""


def print_shaka(title: str) -> None:
    print(SHAKA.format(title=title))


# --------------------------------------------------------------------------- #
# ID resolution — accept a lesson ("F1.2") or a module ("F1").
# --------------------------------------------------------------------------- #
def _resolve(raw: str) -> tuple[str, str]:
    """Return ('lesson', id) or ('module', id). Exit on unknown id."""
    rid = raw.upper()
    if rid in LESSONS:
        return "lesson", rid
    if rid in MODULES:
        return "module", rid
    print(f"Unknown id '{raw}'.")
    print(f"  Modules: {', '.join(MODULE_ORDER)}")
    print(f"  Lessons: {', '.join(LESSON_ORDER)}")
    sys.exit(1)


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #
def cmd_init(args) -> None:
    p = progress_path()
    if p.exists() and not args.force:
        print(f"Progress file already exists at {p}.")
        print("Run 'python track.py status' to see it, or 'init --force' to wipe it.")
        return
    save_state(fresh_state())
    print(f"Created progress file: {p}")
    cmd_status(args)


def _lesson_done(state: dict, lid: str) -> bool:
    return state["lessons"][lid]["status"] == "mastered"


def cmd_status(args) -> None:
    state = load_state()
    print("\n  CLAUDE CODE — FUNDAMENTALS PROGRESS")
    print("  " + "=" * 56)
    modules_done = 0
    lessons_done_total = 0
    for mid in MODULE_ORDER:
        lids = lessons_in(mid)
        done = sum(1 for lid in lids if _lesson_done(state, lid))
        lessons_done_total += done
        complete = done == len(lids) and lids
        if complete:
            modules_done += 1
        flag = "🤙" if complete else "  "
        print(f"\n  {flag} {mid}  {MODULES[mid]}   ({done}/{len(lids)})")
        for lid in lids:
            f = state["lessons"][lid]
            icon = STATUS_ICON[f["status"]]
            print(f"        {icon:<7} {lid:<5} {f['title']}")
    print("\n  " + "=" * 56)
    print(f"  Lessons mastered: {lessons_done_total}/{len(LESSON_ORDER)}    "
          f"Modules complete: {modules_done}/{len(MODULE_ORDER)}\n")
    if modules_done == len(MODULE_ORDER):
        print("  🌺 Every lesson mastered. You ARE the Aloha spirit. 🤙\n")


def _print_lesson_detail(state: dict, lid: str) -> None:
    spec = LESSONS[lid]
    f = state["lessons"][lid]
    mid = spec["module"]
    print(f"\n  {lid} — {spec['title']}   [{f['status']}]")
    print(f"  module {mid}: {MODULES[mid]}")
    print("  " + "-" * 60)
    print(f"  WHY: {spec['why']}\n")
    key = spec["key"]
    box = "[x]" if f["checklist"][key] else "[ ]"
    tag = "auto" if spec["kind"] == "auto" else "self"
    print("  THIS LESSON IS DONE WHEN:")
    print(f"    {box} ({tag}) {spec['label']}")
    print(f"          key: {key}")
    print()
    if spec["kind"] == "self":
        print(f"  Confirm it:   python track.py mark {lid} {key} --done")
    else:
        print(f"  Re-check it:  python track.py check {lid}")
    print(f"  Finalise:     python track.py master {lid}\n")


def _print_module_detail(state: dict, mid: str) -> None:
    print(f"\n  {mid} — {MODULES[mid]}")
    print("  " + "-" * 60)
    print("  LESSONS:")
    for lid in lessons_in(mid):
        f = state["lessons"][lid]
        icon = STATUS_ICON[f["status"]]
        print(f"    {icon:<7} {lid:<5} {f['title']}")
    print(f"\n  Drill into one:  python track.py detail {lessons_in(mid)[0]}\n")


def cmd_detail(args) -> None:
    state = load_state()
    kind, rid = _resolve(args.target)
    if kind == "lesson":
        _print_lesson_detail(state, rid)
    else:
        _print_module_detail(state, rid)


def cmd_check(args) -> None:
    state = load_state()
    kind, rid = _resolve(args.target)
    lids = [rid] if kind == "lesson" else lessons_in(rid)
    all_notes = []
    for lid in lids:
        all_notes += run_auto_checks(state, lid)
    save_state(state)
    label = rid if kind == "lesson" else f"{rid} — {MODULES[rid]}"
    print(f"\n  Auto-checks for {label}:")
    if all_notes:
        print("\n".join(all_notes))
    else:
        print("  (no automated checks here — this lesson/module is self-confirmed)")
    print()
    if kind == "lesson":
        _print_lesson_detail(state, rid)
    else:
        _print_module_detail(state, rid)


def cmd_mark(args) -> None:
    state = load_state()
    kind, rid = _resolve(args.target)
    if kind != "lesson":
        print(f"'mark' needs a lesson id (e.g. F1.2), not a module. "
              f"Lessons in {rid}: {', '.join(lessons_in(rid))}")
        sys.exit(1)
    spec = LESSONS[rid]
    if args.item != spec["key"]:
        print(f"Unknown item '{args.item}' for {rid}. The key for this lesson is: "
              f"{spec['key']}")
        sys.exit(1)
    value = not args.undo  # --done -> True, --undo -> False
    was_mastered = _lesson_done(state, rid)
    state["lessons"][rid]["checklist"][args.item] = value
    _recompute_status(state, rid)
    save_state(state)
    print(f"  {rid}.{args.item} set to {value}.")
    if _lesson_done(state, rid) and not was_mastered:
        print_shaka(f"{rid}  {spec['title']}")
        _maybe_celebrate_module(state, spec["module"])


def _maybe_celebrate_module(state: dict, mid: str) -> None:
    lids = lessons_in(mid)
    if lids and all(_lesson_done(state, lid) for lid in lids):
        print(f"\n  🌺 MODULE {mid} COMPLETE — {MODULES[mid]} — every lesson mastered! 🤙\n")


def cmd_master(args) -> None:
    state = load_state()
    kind, rid = _resolve(args.target)
    if kind == "module":
        # Refresh autos, report what's left, celebrate if all done.
        for lid in lessons_in(rid):
            run_auto_checks(state, lid)
        save_state(state)
        remaining = [lid for lid in lessons_in(rid) if not _lesson_done(state, lid)]
        if remaining:
            print(f"\n  Module {rid} not complete yet. Open lessons:")
            for lid in remaining:
                print(f"    [ ] {lid}  {LESSONS[lid]['title']}")
            print(f"\n  Master one:  python track.py master {remaining[0]}\n")
        else:
            _maybe_celebrate_module(state, rid)
        return

    spec = LESSONS[rid]
    run_auto_checks(state, rid)
    cl = state["lessons"][rid]["checklist"]
    missing = [k for k, v in cl.items() if not v]
    was_mastered = _lesson_done(state, rid)
    if missing:
        tag = "auto" if spec["kind"] == "auto" else "self"
        print(f"\n  Not yet — {rid} still open:")
        print(f"    [ ] ({tag}) {spec['label']}")
        if spec["kind"] == "auto":
            print(f"\n  Do the thing, then: python track.py check {rid}")
        else:
            print(f"\n  Confirm with: python track.py mark {rid} {spec['key']} --done")
        print()
        save_state(state)
        return
    _recompute_status(state, rid)
    save_state(state)
    if not was_mastered:
        print_shaka(f"{rid}  {spec['title']}")
        _maybe_celebrate_module(state, spec["module"])
    else:
        print(f"  {rid} was already mastered. 🤙")


def cmd_shaka(args) -> None:
    title = "Claude Code"
    if getattr(args, "target", None):
        kind, rid = _resolve(args.target)
        title = LESSONS[rid]["title"] if kind == "lesson" else MODULES[rid]
    print_shaka(title)


def cmd_reset(args) -> None:
    p = progress_path()
    if not p.exists():
        print("Nothing to reset — no progress file here.")
        return
    if not args.force:
        print(f"This will erase {p}. Re-run with --force to confirm.")
        return
    p.unlink()
    print("Progress reset. Run 'python track.py init' to start fresh.")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Claude Code Mastery progress tracker.")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("init", help="create the progress file")
    s.add_argument("--force", action="store_true", help="overwrite existing progress")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("status", help="show the dashboard")
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("detail", help="show a module's lessons, or one lesson + its check")
    s.add_argument("target", help="a module (F1) or a lesson (F1.2)")
    s.set_defaults(func=cmd_detail)

    s = sub.add_parser("check", help="run automated checks for a lesson or module")
    s.add_argument("target", help="a module (F1) or a lesson (F1.1)")
    s.set_defaults(func=cmd_check)

    s = sub.add_parser("mark", help="toggle a lesson's checklist item")
    s.add_argument("target", help="a lesson id, e.g. F1.2")
    s.add_argument("item", help="the lesson's item key")
    g = s.add_mutually_exclusive_group()
    g.add_argument("--done", action="store_true", help="mark item complete (default)")
    g.add_argument("--undo", action="store_true", help="mark item incomplete")
    s.set_defaults(func=cmd_mark)

    s = sub.add_parser("master", help="finalise a lesson (or report a module's progress)")
    s.add_argument("target", help="a module (F1) or a lesson (F1.2)")
    s.set_defaults(func=cmd_master)

    s = sub.add_parser("shaka", help="print the Shaka sign")
    s.add_argument("target", nargs="?", help="optional module or lesson id")
    s.set_defaults(func=cmd_shaka)

    s = sub.add_parser("reset", help="erase all progress")
    s.add_argument("--force", action="store_true")
    s.set_defaults(func=cmd_reset)

    return p


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
