# Action: history

Search, analyze, and export Claude Code command history stored in `~/.claude/history.jsonl`.

## Arguments

| Argument | Description |
|----------|-------------|
| `<search-term>` | Search history for commands/prompts containing term |
| `--days N` | Limit search to last N days (default: all) |
| `--stats` | Show usage statistics and patterns |
| `--export FILE` | Export history to specified file |
| `--clear` | Clear history (with confirmation) |
| (no args) | Show recent history summary |

## History File Format

`~/.claude/history.jsonl` contains one JSON object per line:

```json
{"display":"/commit","pastedContents":{},"timestamp":1735570845123,"project":"D:/repos/project","sessionId":"abc123-def456"}
```

| Field | Description |
|-------|-------------|
| `display` | The command or prompt text |
| `pastedContents` | Any pasted content (usually empty) |
| `timestamp` | Unix timestamp in milliseconds |
| `project` | Project path where command was run |
| `sessionId` | Session identifier |

## Workflow

### Mode: Search

```python
import json
from pathlib import Path
from datetime import datetime, timezone

history_path = Path.home() / ".claude" / "history.jsonl"

results = []
now = datetime.now(timezone.utc)

with open(history_path) as f:
    for line in f:
        entry = json.loads(line)
        if days_limit:
            entry_time = datetime.fromtimestamp(entry["timestamp"] / 1000, tz=timezone.utc)
            if (now - entry_time).days > days_limit:
                continue
        if search_term.lower() in entry.get("display", "").lower():
            results.append(entry)

for entry in results[-50:]:
    ts = datetime.fromtimestamp(entry["timestamp"] / 1000, tz=timezone.utc)
    project = Path(entry.get("project", "")).name
    print(f"[{ts.strftime('%Y-%m-%d %H:%M')}] [{project}] {entry['display'][:80]}")
```

### Mode: Statistics (`--stats`)

```python
from collections import Counter, defaultdict

commands = Counter()
projects = Counter()
daily_usage = defaultdict(int)
slash_commands = Counter()

with open(history_path) as f:
    for line in f:
        entry = json.loads(line)
        display = entry.get("display", "")
        if display.startswith("/"):
            cmd = display.split()[0]
            slash_commands[cmd] += 1
        project = Path(entry.get("project", "unknown")).name
        projects[project] += 1
        ts = datetime.fromtimestamp(entry["timestamp"] / 1000, tz=timezone.utc)
        day = ts.strftime("%Y-%m-%d")
        daily_usage[day] += 1
```

### Mode: Export (`--export FILE`)

Export history to markdown or JSON:

```python
entries = []
with open(history_path) as f:
    for line in f:
        entries.append(json.loads(line))

with open(export_path, "w") as f:
    f.write("# Claude Code Command History\n\n")
    f.write(f"Exported: {datetime.now(timezone.utc).isoformat()}\n")
    f.write(f"Total entries: {len(entries)}\n\n")

    current_date = None
    for entry in sorted(entries, key=lambda x: x["timestamp"]):
        ts = datetime.fromtimestamp(entry["timestamp"] / 1000, tz=timezone.utc)
        date = ts.strftime("%Y-%m-%d")
        if date != current_date:
            f.write(f"\n## {date}\n\n")
            current_date = date
        time = ts.strftime("%H:%M")
        project = Path(entry.get("project", "")).name
        display = entry["display"][:100]
        f.write(f"- `{time}` [{project}] {display}\n")
```

### Mode: Clear (`--clear`)

Clear history with confirmation:

```python
with open(history_path) as f:
    count = sum(1 for _ in f)

# Use AskUserQuestion for confirmation
# If confirmed:
history_path.unlink()
history_path.touch()
print(f"Cleared {count} history entries")
```

### Mode: Recent Summary (no args)

Show recent history summary (last 24 hours, last 10 entries).
