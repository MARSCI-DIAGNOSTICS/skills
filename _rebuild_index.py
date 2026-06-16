#!/usr/bin/env python3
"""
Rebuild Skills Index

Scans ~/.claude/skills/*/SKILL.md, extracts frontmatter, regenerates
_SKILLS_INDEX.md and _SKILLS_INDEX.json.
"""
import json
import os
import re
from collections import defaultdict
from pathlib import Path

SKILLS_DIR = Path(__file__).parent
INDEX_JSON = SKILLS_DIR / "_SKILLS_INDEX.json"
INDEX_MD = SKILLS_DIR / "_SKILLS_INDEX.md"


def parse_frontmatter(content: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return {}
    fm = m.group(1)
    out = {}
    # name
    nm = re.search(r'^name:\s*["\']?([^"\'\n]+)["\']?', fm, re.MULTILINE)
    if nm:
        out["name"] = nm.group(1).strip()
    # description (may be multi-line quoted, take first chunk)
    dm = re.search(
        r'^description:\s*[|>_-]?\s*["\']?(.+?)(?:["\']?\s*\n[a-z\-]+:|\Z)',
        fm, re.MULTILINE | re.DOTALL
    )
    if dm:
        desc = dm.group(1).strip().replace("\n", " ")
        # Collapse multiple spaces
        desc = re.sub(r"\s+", " ", desc)
        out["description"] = desc[:200]
    # category
    cm = re.search(r'category:\s*([^\s\n]+)', fm)
    if cm:
        out["category"] = cm.group(1).strip()
    # Triggers (in description text)
    if "description" in out:
        desc_l = out["description"].lower()
        if "also use when" in desc_l:
            tpart = desc_l.split("also use when", 1)[-1]
            tpart = tpart.split("for tracking")[0].split(" see ")[0]
            words = re.findall(r'"([^"]+)"', tpart)
            out["triggers"] = [w for w in words[:8] if 1 < len(w) < 40]
    return out


def build_index():
    index = []
    errors = []
    for entry in sorted(os.listdir(SKILLS_DIR)):
        skill_path = SKILLS_DIR / entry / "SKILL.md"
        if not skill_path.is_file():
            continue
        try:
            with open(skill_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(2000)
            fm = parse_frontmatter(content)
            if not fm.get("name"):
                # Use directory name as fallback
                fm["name"] = entry
            fm.setdefault("category", "general")
            fm.setdefault("description", "")
            fm.setdefault("triggers", [])
            fm["path"] = f"skills/{entry}/SKILL.md"
            index.append(fm)
        except Exception as e:
            errors.append((entry, str(e)))

    # Dedupe by name
    seen = {}
    for s in index:
        if s["name"] not in seen:
            seen[s["name"]] = s
    index = list(seen.values())
    index.sort(key=lambda s: (s.get("category", "z"), s["name"].lower()))

    # Save JSON
    with open(INDEX_JSON, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    # Generate MD
    by_cat = defaultdict(list)
    for s in index:
        by_cat[s.get("category", "general")].append(s)

    lines = [
        "# Skills Index (Lazy-Load)",
        "",
        "**Status:** ACTIVE — Auto-generated",
        f"**Total unique skills:** {len(index)}",
        "**Source:** `skills/*/SKILL.md` frontmatter",
        "",
        "---",
        "",
        "## Loading Rule",
        "",
        "**DO NOT auto-load all SKILL.md files.** Each is 5-50KB.",
        "",
        "This index lets the agent:",
        "1. Scan this file to see what skills exist",
        "2. Match user task against skill name + description + category",
        "3. Read ONLY the chosen skill's full `SKILL.md`",
        "",
        "Use `_loader.py` to search:",
        "```bash",
        'python ~/.claude/skills/_loader.py "marketing seo"',
        'python ~/.claude/skills/_loader.py --list-categories',
        'python ~/.claude/skills/_loader.py --skill brand-guidelines',
        "```",
        "",
        "---",
        "",
        "## Index by Category",
        "",
    ]
    for cat in sorted(by_cat.keys(), key=lambda c: -len(by_cat[c])):
        skills_list = by_cat[cat]
        if not skills_list:
            continue
        lines.append(f"### {cat} ({len(skills_list)})")
        lines.append("")
        for s in skills_list:
            desc = s.get("description", "").strip()[:120]
            if desc and desc != s["name"]:
                lines.append(f"- `{s['name']}` — {desc}")
            else:
                lines.append(f"- `{s['name']}`")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## How to Use",
        "",
        "1. User asks task → identify keywords",
        "2. Search this index (or run `_loader.py 'keyword'`)",
        "3. Read the matching skill's full file",
        "4. Do NOT pre-load all skills",
        "",
        "## Files",
        "",
        "- `_SKILLS_INDEX.md` — this file (human-readable)",
        "- `_SKILLS_INDEX.json` — machine-readable",
        "- `_loader.py` — keyword search + skill loader",
        "- `_rebuild_index.py` — regenerate from skills/*/SKILL.md",
        "",
    ])
    with open(INDEX_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Indexed {len(index)} unique skills")
    print(f"  JSON: {INDEX_JSON}")
    print(f"  MD:   {INDEX_MD} ({INDEX_MD.stat().st_size:,} bytes)")
    if errors:
        print(f"  Errors: {len(errors)}")
        for e, msg in errors[:5]:
            print(f"    {e}: {msg}")


if __name__ == "__main__":
    build_index()
