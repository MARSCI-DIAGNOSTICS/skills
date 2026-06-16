---
name: log-inspection
description: "Inspect and query hook event logs. Subcommands: sessions, timeline, trace, agents, team, stats, coverage, daily."
user-invocable: true
argument-hint: "<subcommand> [options]"
allowed-tools: Read, Bash, Glob, Grep
---

# Log Inspection

Query and inspect observability hook logs from JSONL files.

## Arguments

Subcommand is the first argument:

- **`sessions`** -- List all sessions with event counts and duration
- **`timeline [session-id]`** -- Chronological event list with seq numbers
- **`trace <tool-use-id>`** -- Show pre/post pairing for a tool invocation
- **`agents`** -- Subagent lifecycle (start/stop/duration)
- **`team`** -- TeammateIdle and TaskCompleted activity
- **`stats`** -- Aggregate statistics (event breakdown, tool usage, corruption count)
- **`coverage`** -- Which of 14 event types have been observed
- **`daily`** -- Show daily summaries from sessions-index.jsonl (v1.6.0)

## Log File Location

Look for log files at:

```text
{project}/.claude/logs/hooks/events-{YYYY-MM-DD}.jsonl
{project}/.claude/logs/hooks/events-{YYYY-MM-DD}.jsonl.gz  (compressed cold logs)
```

Use Glob to find all available log files:

```text
Glob(".claude/logs/hooks/events-*.jsonl")
Glob(".claude/logs/hooks/events-*.jsonl.gz")
```

**Note:** Files older than 7 days are automatically compressed to `.jsonl.gz` (configurable via `CLAUDE_HOOK_LOG_COMPRESS_AFTER_DAYS`). DuckDB reads `.jsonl.gz` natively; use `zcat | jq` on Unix for manual inspection.

## Workflow

### Step 1: Locate Log Files

Find all hook log files in the project:

```text
Glob(".claude/logs/hooks/events-*.jsonl")
Glob(".claude/logs/hooks/events-*.jsonl.gz")
Glob(".claude/logs/hooks/sessions-index.jsonl")
```

If no log files exist, inform the user that logging must be enabled via `CLAUDE_HOOK_LOG_EVENTS_ENABLED=1`.

### Step 2: Execute Subcommand

#### `sessions`

Parse `sessions-index.jsonl` if it exists. Use the `type` field to discriminate entries (`session_start`, `session_end`, `agent_start`, `agent_stop`). For backward compatibility, entries without `type` are inferred from the presence of `started_at` (session_start) or `ended_at` (session_end). Otherwise, scan event log files for `sessionstart` and `sessionend` events. Display:

| Session ID | Started | Ended | Model | Events | Duration |
|------------|---------|-------|-------|--------|----------|

The enriched index also includes `cwd`, `transcript_path`, `model`, and `agent_type` on session_start entries.

#### `timeline [session-id]`

Read the log file and display events in seq order. If session-id is provided, filter to that session. Display:

```text
seq  timestamp            event              tool_name    pid
1    2026-02-15T18:13:23  sessionstart       -            12345
2    2026-02-15T18:13:24  userpromptsubmit   -            12345
3    2026-02-15T18:13:25  pretooluse         Read         12346
4    2026-02-15T18:13:25  posttooluse        Read         12346
```

#### `trace <tool-use-id>`

Find pretooluse and posttooluse/posttoolusefailure entries with the given tool_use_id. Display the pair showing timing and success/failure.

#### `agents`

First check `sessions-index.jsonl` for `agent_start` and `agent_stop` entries (direct lookup, no event scanning needed). Fall back to scanning event log files for `subagentstart` and `subagentstop` events if index is missing. Display:

| Agent ID | Type | Started (seq) | Stopped (seq) | Duration |
|----------|------|---------------|---------------|----------|

#### `team`

First check `sessions-index.jsonl` for `task_completed` and `teammate_idle` entries (direct lookup, added in v1.8.0). Fall back to scanning event log files for `teammateidle` and `taskcompleted` events if index entries are missing. Display:

| Time | Type | Teammate | Team | Task Subject |
|------|------|----------|------|--------------|

#### `stats`

Parse all entries and compute:

- **Event breakdown**: Count of each event type
- **Tool usage**: Most frequently used tools (from pretooluse events)
- **Error rate**: posttoolusefailure count / total tool uses
- **Avg duration_ms**: Average hook processing time
- **Corruption count**: Lines that fail JSON parsing
- **Unique sessions**: Count of distinct session_id values
- **Seq range**: Min and max seq values

Use Bash with Python one-liners for aggregation. For `.jsonl.gz` files, use `gzip.open` to read:

```bash
python3 -c "
import json, gzip, glob
from collections import Counter
events = Counter()
tools = Counter()
errors = 0
corrupt = 0
durations = []
sessions = set()

def read_lines(path):
    if path.endswith('.gz'):
        with gzip.open(path, 'rt', encoding='utf-8') as f:
            return f.readlines()
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines()

for path in sorted(glob.glob('.claude/logs/hooks/events-*.jsonl') + glob.glob('.claude/logs/hooks/events-*.jsonl.gz')):
    for line in read_lines(path):
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
            events[e.get('event','')] += 1
            if 'tool_name' in e:
                tools[e['tool_name']] += 1
            if e.get('event') == 'posttoolusefailure':
                errors += 1
            durations.append(e.get('duration_ms', 0))
            sessions.add(e.get('session_id',''))
        except json.JSONDecodeError:
            corrupt += 1
print(f'Events: {dict(events)}')
print(f'Top tools: {tools.most_common(10)}')
print(f'Error rate: {errors}/{events.get(\"pretooluse\",0)} tool uses')
print(f'Avg duration: {sum(durations)/len(durations):.2f}ms' if durations else 'No entries')
print(f'Corrupted lines: {corrupt}')
print(f'Unique sessions: {len(sessions)}')
"
```

**Note:** `hook_event_name` was removed from entries in v1.4.0 and fully suppressed from `extra_fields` in v1.7.0.

#### `coverage`

Check which of the 14 event types have been captured. Display:

```text
Event Coverage Report
=====================
[x] pretooluse (142 events)
[x] posttooluse (140 events)
[x] userpromptsubmit (8 events)
[ ] precompact (0 events)
...
Coverage: 12/14 event types observed
```

The 14 required types are: `pretooluse`, `posttooluse`, `posttoolusefailure`, `permissionrequest`, `notification`, `userpromptsubmit`, `stop`, `subagentstart`, `subagentstop`, `precompact`, `sessionstart`, `sessionend`, `teammateidle`, `taskcompleted`.

#### `daily`

Parse `sessions-index.jsonl` for `daily_summary` entries (v1.6.0). Display:

| Date | Events | Sessions | Errors | Avg Duration |
|------|--------|----------|--------|--------------|

Daily summaries are generated automatically on the first `sessionstart` of each day for the previous day's logs.

### Step 3: Format Output

Present results in a clear, readable format. Use markdown tables where appropriate. Include the log file path and date range in the header.

## DuckDB Queries (Advanced)

For large log files, suggest DuckDB for analytical queries:

```sql
-- Load JSONL directly
SELECT event, count(*) as cnt
FROM read_json_auto('.claude/logs/hooks/events-2026-02-15.jsonl')
GROUP BY event ORDER BY cnt DESC;

-- Tool usage with timing
SELECT tool_name, count(*) as uses, avg(duration_ms) as avg_ms
FROM read_json_auto('.claude/logs/hooks/events-2026-02-15.jsonl')
WHERE event = 'pretooluse'
GROUP BY tool_name ORDER BY uses DESC;

-- Find corrupted entries (seq gaps)
SELECT seq, lag(seq) OVER (ORDER BY seq) as prev_seq
FROM read_json_auto('.claude/logs/hooks/events-2026-02-15.jsonl')
WHERE seq - lag(seq) OVER (ORDER BY seq) > 1;
```

## Usage Examples

```bash
# List sessions
/claude-code-observability:log-inspection sessions

# Timeline for current session
/claude-code-observability:log-inspection timeline

# Trace a specific tool call
/claude-code-observability:log-inspection trace toolu_01abc123

# Event type coverage
/claude-code-observability:log-inspection coverage

# Full statistics
/claude-code-observability:log-inspection stats
```
