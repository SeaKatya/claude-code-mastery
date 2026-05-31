#!/usr/bin/env python3
"""
Claude Code Mastery — progress tracker.

Creates and maintains a local progress file (.claude-code-mastery.json) in the
current directory, walks a learner through the 9 fundamentals from Boris's Claude
Code talk, runs best-effort automated checks, lets them confirm the behavioural
items, and throws a Shaka when a fundamental is fully mastered.

Usage:
    python track.py init                 # create the progress file (idempotent)
    python track.py status               # dashboard of all fundamentals
    python track.py detail F5            # show one fundamental + its checklist
    python track.py check F5             # run automated checks, update those items
    python track.py mark F5 memory_loaded --done   # toggle a self-attested item
    python track.py mark F5 memory_loaded --undo
    python track.py master F5            # mark mastered IF all items pass -> Shaka
    python track.py shaka                # print the Shaka sign
    python track.py reset --force        # wipe progress and start over

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
SCHEMA_VERSION = 2


# --------------------------------------------------------------------------- #
# Fundamentals — single source of truth.
# Each checklist item: key -> {label, kind}
#   kind "auto"  : track.py can detect it (still overridable by hand)
#   kind "self"  : a behaviour the learner confirms ("I did this with Claude")
# The checklist doubles as the fundamental's "to-do list" in the teaching flow.
# --------------------------------------------------------------------------- #
FUNDAMENTALS = {
    "F1": {
        "title": "Setup & Environment Optimization",
        "why": "A tool you fight on day one is a tool you abandon by day three. A few "
               "minutes removing input friction and connecting your repo turns Claude "
               "Code from a novelty into something you reach for without thinking.",
        "checklist": {
            "config_present": {"label": "Claude Code installed & config detected on this machine", "kind": "auto"},
            "terminal_setup": {"label": "Ran /terminal-setup so Shift+Enter inserts a newline", "kind": "self"},
            "theme_set": {"label": "Picked a comfortable theme via /theme (light / dark / daltonize)", "kind": "self"},
            "github_app": {"label": "Ran /install-github-app so @mentions work on issues/PRs", "kind": "self"},
            "allowed_tools": {"label": "Customized allowed tools so routine commands aren't re-prompted", "kind": "self"},
        },
    },
    "F2": {
        "title": "Codebase Q&A (start here)",
        "why": "The first move isn't editing — it's using Claude as a search engine that "
               "understands meaning. Asking how a thing is used gives a wiki-style tour a "
               "Cmd+F never could. No indexing, code stays local, zero setup.",
        "checklist": {
            "asked_question": {"label": "Asked Claude a real question about your codebase", "kind": "self"},
            "deeper_than_search": {"label": "Got an answer deeper than a text search (how something is built/used)", "kind": "self"},
            "usage_followup": {"label": "Asked a 'how is this used across the project?' follow-up", "kind": "self"},
        },
    },
    "F3": {
        "title": "Git History & Standup Reports",
        "why": "Code tells you what; git history tells you why. Claude reads your local "
               "log and linked issues to reconstruct decisions — and summarises what you "
               "personally shipped, the standup nobody enjoys writing.",
        "checklist": {
            "in_git_repo": {"label": "Working inside a git repository", "kind": "auto"},
            "history_explained": {"label": "Claude explained the historical 'why' of a confusing function", "kind": "self"},
            "shipped_summary": {"label": "Got a 'what did I ship this week?' summary of your commits", "kind": "self"},
        },
    },
    "F4": {
        "title": "Agentic Workflow: Plan -> Edit -> PR",
        "why": "Turning the agent loose unsupervised gives sprawling surprise diffs. "
               "Asking for a plan first keeps you in control; once you approve, the "
               "'commit push PR' incantation automates the tedious git/PR plumbing.",
        "checklist": {
            "recent_commits": {"label": "Repository has recent commit activity", "kind": "auto"},
            "plan_approved": {"label": "Asked for a plan and approved it BEFORE any file changed", "kind": "self"},
            "edit_made": {"label": "Let Claude implement the approved change", "kind": "self"},
            "pr_created": {"label": "Used 'commit push PR' to branch, commit, push & open a PR", "kind": "self"},
        },
    },
    "F5": {
        "title": "Teach Claude Your Tools (CLIs + MCP)",
        "why": "Claude shines when it can drive your team's tools. Tell it about a CLI "
               "(point it at --help), or add an MCP server, and it uses them on your "
               "behalf. Check an .mcp.json into the repo so the whole team gets them.",
        "checklist": {
            "mcp_config": {"label": "An .mcp.json exists in the project (shared MCP servers)", "kind": "auto"},
            "cli_taught": {"label": "Told Claude about a CLI and had it learn via --help / run it", "kind": "self"},
            "mcp_used": {"label": "Added or used an MCP server's tools in a session", "kind": "self"},
        },
    },
    "F6": {
        "title": "Feedback Loops (let Claude check its work)",
        "why": "The single biggest quality lever. Give Claude a test command or a way to "
               "screenshot, and it iterates to a working result instead of handing you "
               "untested code. Drop in a UI mock and let it iterate to match.",
        "checklist": {
            "test_cmd_present": {"label": "Project exposes a test/build command Claude can run", "kind": "auto"},
            "iterated_on_feedback": {"label": "Claude iterated on a change using a test or screenshot it ran itself", "kind": "self"},
            "visual_coding": {"label": "Tried visual coding (dropped a mock image) OR wired up a checker tool", "kind": "self"},
        },
    },
    "F7": {
        "title": "Context Management (CLAUDE.md & friends)",
        "why": "Claude starts each session with no memory of your project. CLAUDE.md is "
               "the standing brief it auto-reads every time — commands, style, gotchas. "
               "Slash commands, /memory and the '#' shortcut extend it. Keep it short.",
        "checklist": {
            "claude_md_exists": {"label": "A CLAUDE.md exists in the project", "kind": "auto"},
            "memory_loaded": {"label": "Ran /memory to see which context files are loaded", "kind": "self"},
            "memory_shortcut": {"label": "Used the '#' shortcut to remember something mid-session", "kind": "self"},
            "slash_command": {"label": "Created or used a custom slash command (.claude/commands)", "kind": "self"},
        },
    },
    "F8": {
        "title": "Speed & Keybindings",
        "why": "The gap between 'neat' and 'fast' is muscle memory. Auto-accept for work "
               "you trust, '!' to feed command output back in, and Escape to stop a "
               "wayward edit are the bindings that compound the most.",
        "checklist": {
            "bash_mode": {"label": "Used '!' to run a command and pipe its output into context", "kind": "self"},
            "escape_interrupt": {"label": "Hit Escape to stop an edit, then redirected it", "kind": "self"},
            "auto_accept": {"label": "Entered auto-accept mode (Shift+Tab) for trusted work", "kind": "self"},
            "resume_session": {"label": "Resumed a session (--resume / --continue) or viewed full output (Ctrl+R)", "kind": "self"},
        },
    },
    "F9": {
        "title": "SDK as a Unix Utility (+ parallel)",
        "why": "`claude -p` is a scriptable, super-intelligent Unix utility: pipe in, pipe "
               "out, choose JSON or streaming. Power users run many sessions at once via "
               "tmux/SSH, extra checkouts, or git worktrees.",
        "checklist": {
            "sdk_pipe": {"label": "Used `claude -p`, e.g. `git status | claude -p \"summarise\"`", "kind": "self"},
            "sdk_flags": {"label": "Tried --output-format / --allowed-tools, or used it in a script/CI", "kind": "self"},
            "parallel_sessions": {"label": "Ran parallel sessions (tmux / extra checkouts / git worktrees)", "kind": "self"},
        },
    },
}

ORDER = list(FUNDAMENTALS.keys())


# --------------------------------------------------------------------------- #
# Storage
# --------------------------------------------------------------------------- #
def progress_path() -> Path:
    return Path.cwd() / PROGRESS_FILENAME


def now_iso() -> str:
    return _dt.datetime.now().isoformat(timespec="seconds")


def fresh_state() -> dict:
    fundamentals = {}
    for fid in ORDER:
        spec = FUNDAMENTALS[fid]
        fundamentals[fid] = {
            "title": spec["title"],
            "status": "not_started",
            "mastered_at": None,
            "checklist": {k: False for k in spec["checklist"]},
        }
    return {
        "schema_version": SCHEMA_VERSION,
        "created": now_iso(),
        "updated": now_iso(),
        "fundamentals": fundamentals,
    }


def _migrate(state: dict) -> bool:
    """Bring an older progress file up to the current fundamentals schema.

    Preserves every checklist value the user already earned (matched by key),
    adds any new fundamentals/items as False, drops obsolete ones, and refreshes
    titles. Returns True if anything changed.
    """
    changed = False
    state.setdefault("fundamentals", {})
    fts = state["fundamentals"]

    # Drop fundamentals that no longer exist.
    for fid in list(fts.keys()):
        if fid not in FUNDAMENTALS:
            del fts[fid]
            changed = True

    for fid in ORDER:
        spec = FUNDAMENTALS[fid]
        if fid not in fts:
            fts[fid] = {"title": spec["title"], "status": "not_started",
                        "mastered_at": None, "checklist": {}}
            changed = True
        f = fts[fid]
        if f.get("title") != spec["title"]:
            f["title"] = spec["title"]
            changed = True
        cl = f.setdefault("checklist", {})
        # Add missing items.
        for key in spec["checklist"]:
            if key not in cl:
                cl[key] = False
                changed = True
        # Remove obsolete items.
        for key in list(cl.keys()):
            if key not in spec["checklist"]:
                del cl[key]
                changed = True

    if changed:
        state["schema_version"] = SCHEMA_VERSION
        for fid in ORDER:
            _recompute_status(state, fid)
    return changed


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
# Automated checks (best-effort, never crash)
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


def run_auto_checks(state: dict, fid: str) -> list[str]:
    """Run auto checks for a fundamental, update state, return human notes."""
    notes = []
    spec = FUNDAMENTALS[fid]
    for key, meta in spec["checklist"].items():
        if meta["kind"] != "auto":
            continue
        result = auto_check(key)
        if result is True:
            state["fundamentals"][fid]["checklist"][key] = True
            notes.append(f"  [auto PASS] {meta['label']}")
        elif result is False:
            notes.append(f"  [auto  --] {meta['label']}  (not detected yet)")
        else:
            notes.append(f"  [auto  ??] {meta['label']}  (could not determine)")
    _recompute_status(state, fid)
    return notes


# --------------------------------------------------------------------------- #
# Status logic
# --------------------------------------------------------------------------- #
def _recompute_status(state: dict, fid: str) -> None:
    cl = state["fundamentals"][fid]["checklist"]
    done = sum(1 for v in cl.values() if v)
    total = len(cl)
    f = state["fundamentals"][fid]
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


def cmd_status(args) -> None:
    state = load_state()
    print("\n  CLAUDE CODE — FUNDAMENTALS PROGRESS")
    print("  " + "-" * 52)
    mastered = 0
    for fid in ORDER:
        f = state["fundamentals"][fid]
        cl = f["checklist"]
        done = sum(1 for v in cl.values() if v)
        total = len(cl)
        if f["status"] == "mastered":
            mastered += 1
        icon = STATUS_ICON[f["status"]]
        print(f"  {icon:<7} {fid}  {f['title']:<42} {done}/{total}")
    print("  " + "-" * 52)
    print(f"  Mastered: {mastered}/{len(ORDER)} fundamentals\n")
    if mastered == len(ORDER):
        print("  🌺 All fundamentals mastered. You ARE the Aloha spirit. 🤙\n")


def _resolve_fid(raw: str) -> str:
    fid = raw.upper()
    if fid not in FUNDAMENTALS:
        print(f"Unknown fundamental '{raw}'. Valid: {', '.join(ORDER)}")
        sys.exit(1)
    return fid


def cmd_detail(args) -> None:
    state = load_state()
    fid = _resolve_fid(args.fundamental)
    spec = FUNDAMENTALS[fid]
    f = state["fundamentals"][fid]
    print(f"\n  {fid} — {spec['title']}   [{f['status']}]")
    print("  " + "-" * 60)
    print(f"  WHY: {spec['why']}\n")
    print("  CHECKLIST / TO-DO:")
    for key, meta in spec["checklist"].items():
        box = "[x]" if f["checklist"][key] else "[ ]"
        tag = "auto" if meta["kind"] == "auto" else "self"
        print(f"    {box} ({tag}) {meta['label']}")
        print(f"          key: {key}")
    print()
    print("  To confirm a 'self' item:  python track.py mark "
          f"{fid} <key> --done")
    print(f"  To re-run auto checks:     python track.py check {fid}")
    print(f"  To finalise:               python track.py master {fid}\n")


def cmd_check(args) -> None:
    state = load_state()
    fid = _resolve_fid(args.fundamental)
    notes = run_auto_checks(state, fid)
    save_state(state)
    print(f"\n  Auto-checks for {fid} — {FUNDAMENTALS[fid]['title']}:")
    if notes:
        print("\n".join(notes))
    else:
        print("  (no automated checks for this fundamental — all items are self-confirmed)")
    print()
    cmd_detail(args)


def cmd_mark(args) -> None:
    state = load_state()
    fid = _resolve_fid(args.fundamental)
    spec = FUNDAMENTALS[fid]
    if args.item not in spec["checklist"]:
        print(f"Unknown item '{args.item}' for {fid}. Valid keys:")
        for k in spec["checklist"]:
            print(f"  - {k}")
        sys.exit(1)
    value = not args.undo  # --done -> True, --undo -> False
    was_mastered = state["fundamentals"][fid]["status"] == "mastered"
    state["fundamentals"][fid]["checklist"][args.item] = value
    _recompute_status(state, fid)
    save_state(state)
    print(f"  {fid}.{args.item} set to {value}.")
    now_mastered = state["fundamentals"][fid]["status"] == "mastered"
    if now_mastered and not was_mastered:
        print_shaka(spec["title"])


def cmd_master(args) -> None:
    state = load_state()
    fid = _resolve_fid(args.fundamental)
    spec = FUNDAMENTALS[fid]
    # Refresh auto items first so the learner doesn't have to.
    run_auto_checks(state, fid)
    cl = state["fundamentals"][fid]["checklist"]
    missing = [k for k, v in cl.items() if not v]
    if missing:
        print(f"\n  Not yet — {fid} still has open items:")
        for k in missing:
            meta = spec["checklist"][k]
            tag = "auto" if meta["kind"] == "auto" else "self"
            print(f"    [ ] ({tag}) {meta['label']}")
        print("\n  Auto items: do the thing, then `python track.py check "
              f"{fid}`.")
        print("  Self items: confirm with `python track.py mark "
              f"{fid} <key> --done`.\n")
        save_state(state)
        return
    was_mastered = state["fundamentals"][fid]["status"] == "mastered"
    _recompute_status(state, fid)
    save_state(state)
    if not was_mastered:
        print_shaka(spec["title"])
    else:
        print(f"  {fid} was already mastered. 🤙")


def cmd_shaka(args) -> None:
    title = "Claude Code"
    if getattr(args, "fundamental", None):
        fid = _resolve_fid(args.fundamental)
        title = FUNDAMENTALS[fid]["title"]
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

    s = sub.add_parser("detail", help="show one fundamental + checklist")
    s.add_argument("fundamental")
    s.set_defaults(func=cmd_detail)

    s = sub.add_parser("check", help="run automated checks for a fundamental")
    s.add_argument("fundamental")
    s.set_defaults(func=cmd_check)

    s = sub.add_parser("mark", help="toggle a checklist item")
    s.add_argument("fundamental")
    s.add_argument("item")
    g = s.add_mutually_exclusive_group()
    g.add_argument("--done", action="store_true", help="mark item complete (default)")
    g.add_argument("--undo", action="store_true", help="mark item incomplete")
    s.set_defaults(func=cmd_mark)

    s = sub.add_parser("master", help="finalise a fundamental if all items pass")
    s.add_argument("fundamental")
    s.set_defaults(func=cmd_master)

    s = sub.add_parser("shaka", help="print the Shaka sign")
    s.add_argument("fundamental", nargs="?")
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
