# Action: transcript-search

Search across all Claude Code session transcripts to find past conversations, implementations, or patterns.

## Arguments

| Argument | Description |
|----------|-------------|
| `<query>` | Search term or pattern to find |
| `--days N` | Limit search to last N days (default: all) |
| `--project` | Search current project only (default: all projects) |
| `--regex` | Treat query as regex pattern |
| `--context N` | Show N lines of context around matches (default: 2) |
| `--files-only` | Only show matching session files, not content |

## What Gets Searched

### Session Transcript Location

```text
~/.claude/projects/
+-- D--repos-project-a/
|   +-- abc123.jsonl           # Session files
|   +-- agent-xyz789.jsonl     # Agent transcripts
+-- D--repos-project-b/
    +-- ...
```

### Searchable Content

| Content Type | Searched |
|--------------|----------|
| User messages | Yes |
| Assistant responses | Yes |
| Tool call content | Yes |
| Compaction summaries | Yes |
| File paths in context | Yes |

## Workflow

### Step 1: Find Session Files

```python
from pathlib import Path
from datetime import datetime, timezone, timedelta

claude_dir = Path.home() / ".claude"
projects_dir = claude_dir / "projects"

session_files = []
if project_only:
    current_project = Path.cwd()
    project_encoded = str(current_project).replace(":", "").replace("/", "-").replace("\\", "-")
    project_dir = projects_dir / project_encoded
    if project_dir.exists():
        session_files = list(project_dir.glob("*.jsonl"))
else:
    session_files = list(projects_dir.glob("**/*.jsonl"))

if days_limit:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_limit)
    session_files = [
        f for f in session_files
        if datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc) > cutoff
    ]
```

### Step 2: Search Sessions

```python
import json
import re

def search_session(session_path, query, use_regex=False):
    """Search a session file for matches."""
    matches = []
    if use_regex:
        pattern = re.compile(query, re.IGNORECASE)

    with open(session_path) as f:
        for line_num, line in enumerate(f, 1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            text = ""
            record_type = record.get("type", "")
            if record_type == "user":
                text = record.get("message", {}).get("content", "")
            elif record_type == "assistant":
                text = record.get("message", {}).get("content", "")
            elif record_type == "summary":
                text = record.get("summary", "")

            if use_regex:
                if pattern.search(text):
                    matches.append({"line": line_num, "type": record_type, "snippet": get_snippet(text, query)})
            else:
                if query.lower() in text.lower():
                    matches.append({"line": line_num, "type": record_type, "snippet": get_snippet(text, query)})
    return matches

def get_snippet(text, query, context_chars=100):
    idx = text.lower().find(query.lower())
    if idx == -1:
        return text[:200]
    start = max(0, idx - context_chars)
    end = min(len(text), idx + len(query) + context_chars)
    snippet = text[start:end]
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet + "..."
    return snippet
```

### Step 3: Format Results

Show matches grouped by session with snippets, line numbers, and resume commands.

## Search Tips

| Goal | Query Example |
|------|---------------|
| Find specific error | `"ENOENT: no such file"` |
| Find implementation | `"middleware authentication"` |
| Find by file path | `src/components/Button` |
| Find tool usage | `"Edit tool"` |
| Find decisions | `"decided to use"` |
| Find failures | `"let me try again"` |

## Performance Notes

- Searching all projects can be slow with many sessions
- Use `--project` for faster current-project searches
- Use `--days N` to limit search scope
- Very large sessions (>10MB) may take longer

## Privacy

- All searches are local
- No data sent externally
- Results stay in your terminal
