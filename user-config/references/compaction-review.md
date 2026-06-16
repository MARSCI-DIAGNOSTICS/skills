# Action: compaction-review

After a compaction event (`/compact` or automatic), review what context was summarized away to understand potential information loss.

## Arguments

| Argument | Description |
|----------|-------------|
| `session-id` | Specific session ID to review |
| `--current` | Review current session's last compaction |
| `--compare` | Compare pre/post compaction context |
| `--list` | List all compaction events in session |
| (no args) | Review most recent compaction in current session |

## What is Compaction?

Compaction is Claude Code's context management feature that summarizes older conversation turns when the context window fills up:

| Aspect | Description |
|--------|-------------|
| **Trigger** | Context window approaching limit (~85%+) |
| **Process** | Older turns summarized into compact form |
| **Result** | Reduced context, preserved key information |
| **Record** | `{"type":"summary","summary":"..."}` in transcript |

## What Information Can Be Lost

| Category | Risk | Examples |
|----------|------|----------|
| **Specific file paths** | Medium | Exact paths may be summarized to "several files" |
| **Error details** | Medium | Stack traces, error codes compressed |
| **Code snippets** | High | Inline code examples may be omitted |
| **Decision rationale** | Medium | Why choices were made |
| **User preferences** | Low | Usually preserved in summary |
| **Technical constraints** | Medium | Specific requirements may be generalized |

## Workflow

### Step 1: Find Compaction Events

```python
import json
from pathlib import Path

claude_dir = Path.home() / ".claude"
projects_dir = claude_dir / "projects"

def find_compaction_events(session_path):
    """Find all compaction summaries in a session."""
    events = []
    with open(session_path) as f:
        for line_num, line in enumerate(f, 1):
            try:
                record = json.loads(line)
                if record.get("type") == "summary":
                    events.append({
                        "line": line_num,
                        "summary": record.get("summary", ""),
                        "timestamp": record.get("timestamp")
                    })
            except json.JSONDecodeError:
                continue
    return events
```

### Step 2: Analyze Pre-Compaction Content

```python
def get_pre_compaction_content(session_path, compaction_line):
    """Get content that was summarized in compaction."""
    content = []
    with open(session_path) as f:
        lines = f.readlines()

    start_line = 0
    for i in range(compaction_line - 2, -1, -1):
        try:
            record = json.loads(lines[i])
            if record.get("type") == "summary":
                start_line = i + 1
                break
        except:
            continue

    for i in range(start_line, compaction_line - 1):
        try:
            record = json.loads(lines[i])
            content.append(record)
        except:
            continue
    return content
```

### Step 3: Analyze What Was Lost

```python
def analyze_loss(pre_content, summary):
    """Analyze what was potentially lost in compaction."""
    analysis = {
        "files_mentioned": set(),
        "code_snippets": 0,
        "error_messages": 0,
        "decisions": [],
        "preserved_in_summary": []
    }

    for record in pre_content:
        content = ""
        if record.get("type") == "user":
            content = record.get("message", {}).get("content", "")
        elif record.get("type") == "assistant":
            content = record.get("message", {}).get("content", "")

        import re
        paths = re.findall(r'[/\\][\w/\\.-]+\.\w+', content)
        analysis["files_mentioned"].update(paths)
        analysis["code_snippets"] += content.count("```")

        if any(word in content.lower() for word in ["error", "exception", "failed"]):
            analysis["error_messages"] += 1

    for item in analysis["files_mentioned"]:
        if item in summary:
            analysis["preserved_in_summary"].append(item)

    analysis["files_mentioned"] = list(analysis["files_mentioned"])
    return analysis
```

## Output Format

```markdown
# Compaction Review

**Session:** abc123-def456
**Compaction Event:** #1 (line 523)

## Compaction Summary

> [Summary text displayed here]

## What Was Summarized

**Pre-compaction context:**
- User turns: 12
- Assistant turns: 12
- Approximate tokens: ~45,000

**Content analysis:**

| Category | Count | Preserved |
|----------|-------|-----------|
| Files mentioned | 8 | 3 (38%) |
| Code snippets | 15 | Summary only |
| Error messages | 2 | Partial |
| Technical decisions | 4 | 2 |

## Recovery Options

If you need details that were compacted:

1. **Search transcript:** `/user-config transcript-search "keyword"`
2. **Check file history:** `/user-config file-versions src/auth/auth.ts`
3. **Review session:** `claude --resume abc123-def456`
```

## Use Cases

1. **Understand context loss** - Know what was summarized
2. **Recover lost details** - Find paths to retrieve information
3. **Improve future sessions** - Learn when to save details
4. **Debug confusion** - Understand why Claude "forgot" something
5. **Session continuity** - Know what to re-explain after compaction

## Limitations

- Cannot reconstruct exact pre-compaction content
- Timestamps may be approximate
- Some session formats may vary
- Very old sessions may have different compaction format
