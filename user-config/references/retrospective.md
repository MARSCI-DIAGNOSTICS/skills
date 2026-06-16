# Action: retrospective

Analyze a session transcript to generate a postmortem/retrospective report with improvement recommendations.

## Arguments

| Argument | Description |
|----------|-------------|
| `session-id` | Specific session ID to analyze |
| `--current` | Analyze current session (default) |
| `--days N` | Analyze sessions from last N days |
| (no args) | Analyze most recent completed session |

## What Gets Analyzed

### Session Transcript Format

Session files are JSONL with records like:

```json
{"type":"user","message":{"role":"user","content":"Fix the login bug"}}
{"type":"assistant","message":{"role":"assistant","content":"I'll help..."}}
{"type":"summary","summary":"Session summary text..."}
```

### Analysis Categories

| Category | What We Look For |
|----------|------------------|
| **Success Patterns** | Clean tool calls, efficient paths, good outcomes |
| **Failure Patterns** | Errors, retries, failed attempts, corrections |
| **Context Usage** | Files read, context bloat, compaction events |
| **Tool Efficiency** | Tool call counts, retry rates, edit failures |
| **Time Distribution** | Where time was spent (if timestamps available) |

## Workflow

### Step 1: Find Session Transcript

```python
import json
from pathlib import Path

claude_dir = Path.home() / ".claude"
projects_dir = claude_dir / "projects"

current_project = Path.cwd()
project_encoded = str(current_project).replace(":", "").replace("/", "-").replace("\\", "-")

session_dir = projects_dir / project_encoded
sessions = [f for f in session_dir.glob("*.jsonl") if not f.name.startswith("agent-")]
sessions.sort(key=lambda f: f.stat().st_mtime, reverse=True)
```

### Step 2: Parse Session Transcript

Parse JSONL into structured data: messages, summaries, tool calls.

### Step 3: Analyze Patterns

Identify success and failure patterns by checking for error keywords, retries, and corrections.

### Step 4: Generate Recommendations

Generate improvement recommendations for:

- **CLAUDE.md additions** - Guidance for common failure patterns
- **Hook opportunities** - Automation candidates
- **Command/skill updates** - Based on usage patterns
- **Prompting improvements** - Better prompt strategies

## Output Format

```markdown
# Session Retrospective

**Session ID:** abc123-def456
**Date:** 2025-12-30
**Turns:** 23 user, 23 assistant

## What Went Well
- Successfully created N components with minimal iterations
- Efficient use of parallel subagents

## What Could Improve
- N Edit tool retries on Windows
- Context grew large before compaction

## Improvement Recommendations

### CLAUDE.md Additions
- [specific guidance based on failures]

### Hook Opportunities
| Hook Type | Trigger | Action |
|-----------|---------|--------|

### Prompting Improvements
- [specific suggestions]

## Session Statistics
| Metric | Value |
|--------|-------|
| Total turns | N |
| Tool calls | N |
| Retries | N (X%) |
| Compaction events | N |
```

## Use Cases

1. **Learning from mistakes** - Identify patterns that caused failures
2. **Improving CLAUDE.md** - Add guidance based on recurring issues
3. **Hook opportunities** - Find automation candidates
4. **Prompting refinement** - Learn what prompts work best
5. **Workflow optimization** - Identify inefficient patterns

## Notes

- Retrospectives work best on completed sessions
- Large sessions may take longer to analyze
- Privacy: Session content stays local, not sent anywhere
- Recommendations are suggestions, not automatic changes
