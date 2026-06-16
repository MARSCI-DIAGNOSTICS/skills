# Action: session-stats

Display aggregate statistics about Claude Code session history, including file counts, storage usage, and trends over time.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--all-projects` | Analyze all projects | false |

## Workflow

### Step 1: Gather Statistics

```bash
PROJECT_PATH=$(pwd | sed 's/[\/:]/-/g' | sed 's/^-//')
PROJECT_DIR="$HOME/.claude/projects/$PROJECT_PATH"

# Count files
TOTAL=$(ls "$PROJECT_DIR"/*.jsonl 2>/dev/null | wc -l)
SESSIONS=$(ls "$PROJECT_DIR"/*.jsonl 2>/dev/null | grep -v "agent-" | wc -l)
AGENTS=$(ls "$PROJECT_DIR"/agent-*.jsonl 2>/dev/null | wc -l)

# Size calculations
TOTAL_SIZE=$(du -sh "$PROJECT_DIR" 2>/dev/null | cut -f1)

# By age
TODAY=$(find "$PROJECT_DIR" -name "*.jsonl" -mtime 0 2>/dev/null | wc -l)
WEEK=$(find "$PROJECT_DIR" -name "*.jsonl" -mtime -7 2>/dev/null | wc -l)
MONTH=$(find "$PROJECT_DIR" -name "*.jsonl" -mtime -30 2>/dev/null | wc -l)
OLDER=$(find "$PROJECT_DIR" -name "*.jsonl" -mtime +30 2>/dev/null | wc -l)
```

### Step 2: Display Statistics

```text
Session Statistics
==================
Project: {project_name}

File Counts:
  Total files:     {total}
  Session files:   {sessions}
  Agent files:     {agents}

Storage Usage:
  Total size:      {size}

Age Distribution:
  Today:           {today} files
  Last 7 days:     {week} files
  Last 30 days:    {month} files
  Older:           {older} files

Cleanup Potential:
  Files >7 days:   {count} (reclaimable: ~{size})

Growth Rate:
  Last 7 days:     +{count} files
  Average/day:     {avg} files/day
```

## Notes

- High agent-to-session ratio indicates heavy Task tool usage
- Large average session size suggests long conversations
- Growth rate helps predict storage needs
- Use `cleanup-sessions` or `cleanup-agents` to act on findings
