#!/usr/bin/env python3
"""
Skills Lazy-Loader

Usage:
    python _loader.py "keyword1 keyword2 ..."
    python _loader.py --list-categories
    python _loader.py --skill <name>

Behavior:
    - Searches _SKILLS_INDEX.json by keyword
    - Prints matching skill name + description + path
    - Agent then reads only the chosen skill file
"""
import json
import os
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).parent
INDEX_FILE = SKILLS_DIR / "_SKILLS_INDEX.json"


def load_index():
    if not INDEX_FILE.exists():
        print(f"ERROR: {INDEX_FILE} not found. Run _rebuild_index.py first.", file=sys.stderr)
        sys.exit(1)
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def search(query: str, limit: int = 10):
    """Search skills by keyword. Splits query on whitespace, matches any word."""
    idx = load_index()
    keywords = [k.lower().strip() for k in query.split() if k.strip()]
    if not keywords:
        print("Usage: _loader.py 'keyword1 keyword2 ...'", file=sys.stderr)
        sys.exit(1)

    scored = []
    for s in idx:
        name_l = s["name"].lower()
        desc_l = s.get("description", "").lower()
        cat_l = s.get("category", "").lower()
        score = 0
        for kw in keywords:
            if kw in name_l:
                score += 10
            if kw in desc_l:
                score += 3
            if kw in cat_l:
                score += 5
        if score > 0:
            scored.append((score, s))

    scored.sort(key=lambda x: -x[0])
    return scored[:limit]


def list_categories():
    idx = load_index()
    from collections import Counter
    cats = Counter(s.get("category", "general") for s in idx)
    print("Categories (skill count):")
    for cat, count in cats.most_common():
        print(f"  {cat:30s} {count}")


def get_skill_path(name: str) -> Path | None:
    """Resolve skill name to its SKILL.md path."""
    idx = load_index()
    for s in idx:
        if s["name"] == name:
            # index path is like "skills/seo-audit/SKILL.md"
            # SKILLS_DIR is ~/.claude/skills/ — strip "skills/" prefix
            rel = s["path"]
            if rel.startswith("skills/"):
                rel = rel[len("skills/"):]
            return SKILLS_DIR / rel
    return None


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)
    if args[0] == "--list-categories":
        list_categories()
        return
    if args[0] == "--skill" and len(args) > 1:
        path = get_skill_path(args[1])
        if path and path.exists():
            print(f"Loading skill: {args[1]}")
            print(f"Path: {path}")
            print("---")
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                print(f.read())
        else:
            print(f"Skill not found: {args[1]}", file=sys.stderr)
            sys.exit(1)
        return
    if args[0] == "--json":
        # Output as JSON for programmatic use
        results = search(" ".join(args[1:]))
        print(json.dumps([s for _, s in results], indent=2, ensure_ascii=False))
        return

    # Default: search mode
    query = " ".join(args)
    results = search(query)
    if not results:
        print(f"No skills matched: {query}")
        sys.exit(0)
    print(f"Top {len(results)} matches for: {query}\n")
    for score, s in results:
        print(f"[{s.get('category','general'):15s}] {s['name']}  (score={score})")
        if s.get("description"):
            print(f"    {s['description'][:120]}")
        print(f"    path: {s['path']}")
        print()


if __name__ == "__main__":
    main()
