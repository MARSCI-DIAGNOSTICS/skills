# Action: plans

Manage Claude Code plan files stored in `~/.claude/plans/`. Plans are markdown files created during plan mode sessions.

## Arguments

| Argument | Description |
|----------|-------------|
| `plan-name` | View a specific plan (partial name match) |
| `--list` | List all plans with metadata |
| `--archive` | Move old plans to archive subdirectory |
| `--cleanup N` | Delete plans older than N days |
| (no args) | List recent plans |

## Plan File Format

Plans are stored as markdown files with generated names:

```text
~/.claude/plans/
+-- reflective-sauteeing-riddle.md
+-- curious-dancing-penguin.md
+-- archive/
    +-- old-completed-plan.md
```

Plan filenames use a randomly generated adjective-verb-noun pattern.

## Workflow

### Mode: List Plans (`--list` or no args)

```python
from pathlib import Path
from datetime import datetime, timezone

plans_dir = Path.home() / ".claude" / "plans"

if not plans_dir.exists():
    print("No plans directory found (~/.claude/plans/)")
    exit(0)

plans = list(plans_dir.glob("*.md"))
plans.sort(key=lambda p: p.stat().st_mtime, reverse=True)

for plan in plans[:20]:
    stat = plan.stat()
    mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
    size_kb = stat.st_size / 1024
    with open(plan) as f:
        first_line = f.readline().strip()
        title = first_line[:50] if first_line else "(empty)"
    print(f"  {plan.stem}")
    print(f"    Modified: {mtime.strftime('%Y-%m-%d %H:%M')}")
    print(f"    Size: {size_kb:.1f} KB")
    print(f"    Preview: {title}")
```

### Mode: View Plan

View a specific plan by name (supports partial match):

```python
search = "reflective"  # From argument
matches = [p for p in plans_dir.glob("*.md") if search.lower() in p.stem.lower()]

if not matches:
    print(f"No plan found matching: {search}")
elif len(matches) > 1:
    print(f"Multiple matches for '{search}':")
    for m in matches:
        print(f"  {m.stem}")
else:
    plan = matches[0]
    print(f"# Plan: {plan.stem}\n")
    print(plan.read_text())
```

### Mode: Archive (`--archive`)

Move plans older than 30 days to archive:

```python
from datetime import timedelta
import shutil

archive_dir = plans_dir / "archive"
archive_dir.mkdir(exist_ok=True)

cutoff = datetime.now(timezone.utc) - timedelta(days=30)
archived = []

for plan in plans_dir.glob("*.md"):
    mtime = datetime.fromtimestamp(plan.stat().st_mtime, tz=timezone.utc)
    if mtime < cutoff:
        dest = archive_dir / plan.name
        shutil.move(str(plan), str(dest))
        archived.append(plan.name)

if archived:
    print(f"Archived {len(archived)} plan(s) to ~/.claude/plans/archive/")
else:
    print("No plans older than 30 days to archive")
```

### Mode: Cleanup (`--cleanup N`)

Delete plans older than N days (with confirmation via AskUserQuestion).

## Use Cases

1. **Review past planning sessions** - Find plans from previous work
2. **Resume abandoned plans** - Copy content back to continue work
3. **Learn from past approaches** - Review how problems were solved
4. **Clean up old plans** - Remove stale planning artifacts

## Notes

- Plans are created by Claude Code during plan mode
- Plan names are auto-generated (adjective-verb-noun pattern)
- Plans persist indefinitely unless manually cleaned
- Archive is just a subdirectory - no special behavior
