# Action: costs

Analyze Claude Code API costs and token usage across sessions to understand spending patterns and optimize usage.

## Arguments

| Argument | Description |
|----------|-------------|
| `--days N` | Analyze last N days (default: 30) |
| `--project` | Current project only |
| `--breakdown` | Detailed breakdown by model, session, day |
| `--export FILE` | Export analysis to CSV or markdown |
| `--compare` | Compare periods (this month vs last month) |
| (no args) | Summary of recent costs |

## Data Sources

Cost analysis uses multiple sources:

| Source | Data |
|--------|------|
| `/cost` command output | Current session costs |
| Session transcripts | Message counts, approximate tokens |
| Model inference | Input/output token estimation |

**Note:** Exact costs require API billing data. This command provides estimates based on message content and model pricing.

## Pricing Reference (as of 2025)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Claude Opus 4 | $15.00 | $75.00 |
| Claude Sonnet 4 | $3.00 | $15.00 |
| Claude Haiku | $0.25 | $1.25 |

**Note:** Prices may change. Verify current pricing at anthropic.com/pricing.

## Workflow

### Step 1: Collect Session Data

```python
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

claude_dir = Path.home() / ".claude"
projects_dir = claude_dir / "projects"

def collect_session_data(days=30, project_only=False):
    """Collect token usage data from sessions."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    sessions = []

    for project_dir in projects_dir.iterdir():
        if not project_dir.is_dir():
            continue
        for session_file in project_dir.glob("*.jsonl"):
            mtime = datetime.fromtimestamp(session_file.stat().st_mtime, tz=timezone.utc)
            if mtime < cutoff:
                continue
            session_data = analyze_session_costs(session_file)
            session_data["project"] = project_dir.name
            session_data["modified"] = mtime
            sessions.append(session_data)
    return sessions
```

### Step 2: Analyze Session Costs

```python
def analyze_session_costs(session_path):
    """Estimate costs for a single session."""
    data = {
        "path": session_path,
        "user_messages": 0,
        "assistant_messages": 0,
        "input_tokens_est": 0,
        "output_tokens_est": 0,
        "model": "sonnet"
    }

    with open(session_path) as f:
        for line in f:
            try:
                record = json.loads(line)
                record_type = record.get("type", "")
                if record_type == "user":
                    content = record.get("message", {}).get("content", "")
                    data["user_messages"] += 1
                    data["input_tokens_est"] += len(content) // 4
                elif record_type == "assistant":
                    content = record.get("message", {}).get("content", "")
                    data["assistant_messages"] += 1
                    data["output_tokens_est"] += len(content) // 4
            except json.JSONDecodeError:
                continue

    data["cost_est"] = estimate_cost(data["input_tokens_est"], data["output_tokens_est"], data["model"])
    return data

def estimate_cost(input_tokens, output_tokens, model="sonnet"):
    """Estimate cost based on token counts and model."""
    pricing = {
        "opus": {"input": 15.0, "output": 75.0},
        "sonnet": {"input": 3.0, "output": 15.0},
        "haiku": {"input": 0.25, "output": 1.25}
    }
    rates = pricing.get(model, pricing["sonnet"])
    input_cost = (input_tokens / 1_000_000) * rates["input"]
    output_cost = (output_tokens / 1_000_000) * rates["output"]
    return input_cost + output_cost
```

### Step 3: Generate Report

```python
def generate_cost_report(sessions, days):
    """Generate cost analysis report."""
    total_input = sum(s["input_tokens_est"] for s in sessions)
    total_output = sum(s["output_tokens_est"] for s in sessions)
    total_cost = sum(s["cost_est"] for s in sessions)

    by_project = {}
    for s in sessions:
        proj = s["project"]
        if proj not in by_project:
            by_project[proj] = {"sessions": 0, "cost": 0}
        by_project[proj]["sessions"] += 1
        by_project[proj]["cost"] += s["cost_est"]

    return {
        "total_sessions": len(sessions),
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "total_cost_est": total_cost,
        "by_project": by_project,
        "avg_per_session": total_cost / len(sessions) if sessions else 0,
        "avg_per_day": total_cost / days
    }
```

## Output Format

### Summary View

```markdown
# Claude Code Cost Analysis

**Period:** Last 30 days
**Sessions Analyzed:** 156

## Cost Summary

| Metric | Value |
|--------|-------|
| **Estimated Total Cost** | $23.45 |
| **Input Tokens** | ~2.1M |
| **Output Tokens** | ~890K |
| **Average per Session** | $0.15 |
| **Average per Day** | $0.78 |
```

## Limitations

- **Estimates only** - Actual costs from Anthropic billing may differ
- **Model detection approximate** - Based on heuristics
- **Agent costs separate** - Agent transcript analysis requires more work
- **Cached tokens not tracked** - Prompt caching savings not reflected
