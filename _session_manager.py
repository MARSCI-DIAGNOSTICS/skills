#!/usr/bin/env python3
"""
Skills Session Manager

Tracks which skills the AI agent has currently "activated" in this session.
Enforces a hard cap of 20 active skills. The AI decides what to activate;
this script just enforces the cap.

Storage: ~/.claude/skills/.session_state.json
  {
    "active_skills": ["seo-audit", "brand-guidelines", ...],
    "last_updated": "2026-06-07T15:30:00",
    "total_loads_this_session": 47
  }

Usage:
    python _session_manager.py status
    python _session_manager.py add <skill-name> [skill-name ...]
    python _session_manager.py clear
    python _session_manager.py list
    python _session_manager.py search "keyword1 keyword2"

Note: There is NO auto-pick. The AI agent decides which skills to activate
based on the current task and context. The manager only enforces the cap.
"""
import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

SKILLS_DIR = Path(__file__).parent
STATE_FILE = SKILLS_DIR / ".session_state.json"
LOADER = SKILLS_DIR / "_loader.py"
MAX_ACTIVE = 20


def load_state():
    if not STATE_FILE.exists():
        return {"active_skills": [], "last_updated": None, "total_loads_this_session": 0}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"active_skills": [], "last_updated": None, "total_loads_this_session": 0}


def save_state(state):
    state["last_updated"] = datetime.now().isoformat(timespec="seconds")
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def status():
    state = load_state()
    n = len(state["active_skills"])
    print(f"Active skills: {n}/{MAX_ACTIVE}")
    print(f"Total loads this session: {state.get('total_loads_this_session', 0)}")
    print(f"Last updated: {state.get('last_updated', 'never')}")
    if state["active_skills"]:
        print("\nCurrently active:")
        for s in state["active_skills"]:
            print(f"  - {s}")


def list_active():
    state = load_state()
    for s in state["active_skills"]:
        print(s)


def clear():
    state = load_state()
    cleared = len(state["active_skills"])
    state["active_skills"] = []
    state["total_loads_this_session"] = 0
    save_state(state)
    print(f"Cleared {cleared} active skills. Session reset.")


def add(*skill_names):
    """Add skills to active set. Auto-clear if would exceed MAX_ACTIVE."""
    if not skill_names:
        print("No skill names provided.", file=sys.stderr)
        sys.exit(1)
    state = load_state()
    added = []
    skipped = []
    for name in skill_names:
        if name in state["active_skills"]:
            skipped.append(f"{name} (already active)")
            continue
        # Check if would exceed cap
        if len(state["active_skills"]) >= MAX_ACTIVE:
            print(f"  Cap reached ({MAX_ACTIVE}). Auto-clearing old activations...")
            cleared = state["active_skills"][:]
            state["active_skills"] = []
            print(f"  Cleared {len(cleared)} skills: {', '.join(cleared)}")
        state["active_skills"].append(name)
        state["total_loads_this_session"] = state.get("total_loads_this_session", 0) + 1
        added.append(name)
    save_state(state)
    if added:
        print(f"Activated: {', '.join(added)}")
    if skipped:
        print(f"Skipped: {', '.join(skipped)}")
    print(f"Now active: {len(state['active_skills'])}/{MAX_ACTIVE}")


def search(*keywords, limit=10):
    """Search skills by keyword. Returns candidates — user decides which to activate."""
    if not keywords:
        print("Usage: _session_manager.py search 'keyword1 keyword2'", file=sys.stderr)
        sys.exit(1)
    query = " ".join(keywords)
    result = subprocess.run(
        [sys.executable, str(LOADER), "--json", query],
        capture_output=True, text=True, encoding="utf-8"
    )
    if result.returncode != 0 or not result.stdout.strip():
        print(f"No matches for: {query}")
        return
    try:
        matches = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("Loader returned invalid JSON:", result.stdout[:200])
        return
    for m in matches[:limit]:
        print(f"  {m['name']}  [{m.get('category','general')}]")
        if m.get("description"):
            print(f"    {m['description'][:120]}")
    print(f"\n{len(matches[:limit])} candidates shown. Use 'add <name>' to activate.")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)
    cmd = args[0]
    rest = args[1:]
    if cmd == "status":
        status()
    elif cmd == "list":
        list_active()
    elif cmd == "clear":
        clear()
    elif cmd == "add":
        add(*rest)
    elif cmd == "search":
        search(*rest)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
