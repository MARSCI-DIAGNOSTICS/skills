---
name: social-intelligence
description: Twitter/X social intelligence monitoring for the Claude Code ecosystem. Scans feeds from Anthropic/Claude Code team members, extracts actionable insights, tracks state, and produces reports. Uses claude-in-chrome MCP for browser automation.
argument-hint: scan [--accounts critical|high|all] [--depth shallow|deep] | report [--since YYYY-MM-DD] [--status pending|all] [--format markdown|json] [--save] | apply | refresh-accounts | discover-accounts | status
allowed-tools: Read, Write, Bash, Glob, Grep, Task, ToolSearch
---

# Social Intelligence

Monitor Twitter/X feeds from Anthropic and Claude Code team members to catch new features, updates, and insights before official documentation is updated.

## Subcommands

Parse the user's argument to determine the subcommand:

| Argument Pattern | Subcommand |
|-----------------|------------|
| `scan`, `scan --accounts critical`, `scan --depth deep` | [Scan Feeds](#scan-feeds) |
| `report`, `report --since 2026-02-01`, `report --save` | [Generate Report](#generate-report) |
| `apply` | [Apply Insights](#apply-insights) |
| `refresh-accounts` | [Refresh Accounts](#refresh-accounts) |
| `discover-accounts` | [Discover Accounts](#discover-accounts) |
| `status` | [Show Status](#show-status) |
| `migrate` | [Data Maintenance](#data-maintenance) |
| `compact` | [Data Maintenance](#data-maintenance) |
| (no argument) | Default to `scan --accounts critical --depth shallow` |

## Prerequisites

Before any operation, ensure the data directory is initialized:

```bash
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}" python "plugins/claude-ecosystem/skills/social-intelligence/scripts/state_manager.py" init
```

## Scan Feeds

### Arguments

| Flag | Default | Options |
|------|---------|---------|
| `--accounts` | `critical` | `critical`, `high`, `all` |
| `--depth` | `shallow` | `shallow`, `deep` |

### Workflow

#### Step 1: Load Configuration

Read these config files:

- `plugins/claude-ecosystem/skills/social-intelligence/config/accounts.json` -- Monitored accounts
- `plugins/claude-ecosystem/skills/social-intelligence/config/scan-config.json` -- Scan parameters, keywords, area mappings

If `accounts.json` has an empty `accounts` array, prompt the user:

> No accounts configured. Run `/claude-ecosystem:social-intelligence refresh-accounts` first to populate the account list from your X following list.

#### Step 2: Filter Accounts by Priority

Based on `--accounts` flag:

- `critical`: Only accounts with `priority == "critical"`
- `high`: Accounts with `priority` in `["critical", "high"]`
- `all`: All accounts

#### Step 2.5: Check Account Freshness

For each filtered account, check when it was last scanned:

```bash
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}" python "plugins/claude-ecosystem/skills/social-intelligence/scripts/state_manager.py" last-scanned "@handle"
```

If `last_scanned` is within the last 2 hours for shallow scans (or 30 minutes for deep scans), skip that account and note it in the summary. This prevents redundant scanning.

#### Step 3: Load claude-in-chrome MCP Tools

Before delegating to the scanner agent, load the required MCP tools:

```text
Use ToolSearch to load:
- mcp__claude-in-chrome__tabs_context_mcp
- mcp__claude-in-chrome__tabs_create_mcp
- mcp__claude-in-chrome__navigate
- mcp__claude-in-chrome__get_page_text
- mcp__claude-in-chrome__javascript_tool
- mcp__claude-in-chrome__read_page
```

#### Step 4: Delegate to x-feed-scanner Agent

Spawn the `claude-ecosystem:x-feed-scanner` agent (subagent_type: `general-purpose`) with:

```json
{
  "accounts": [filtered account list with profile URLs],
  "depth": "shallow|deep",
  "max_posts_per_account": 20,
  "max_scroll_attempts": 3,
  "navigation_delay_ms": 2500,
  "known_post_ids": [list from dedup-check-batch],
  "since_date": "ISO timestamp of oldest desired post"
}
```

**Important**: The agent must use the claude-in-chrome MCP tools to:

1. Call `tabs_context_mcp` to check browser state
2. Call `tabs_create_mcp` to open a dedicated scan tab
3. For each account: `navigate` to profile, wait, `get_page_text` to extract content
4. Use `javascript_tool` for scroll pagination and post ID extraction
5. Return structured post data

#### Step 5: Batch Dedup Against Existing Posts

Collect all post IDs from the scanner output and check them in a single pass:

```bash
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}" python "plugins/claude-ecosystem/skills/social-intelligence/scripts/state_manager.py" dedup-check-batch post_id_1 post_id_2 post_id_3
```

The response includes `new_ids` (not yet stored) and `existing_ids` (already in index). Filter to new posts only.

#### Step 6: Delegate to intelligence-analyst Agent

Spawn the `claude-ecosystem:intelligence-analyst` agent (subagent_type: `general-purpose`) with:

- New posts (after dedup)
- Scan config (keywords, scoring weights, area mappings)

The agent classifies posts, scores relevance, extracts insights, and maps to plugin areas.

#### Step 7: Persist State

Write results using `state_manager.py append`:

```bash
# Log the scan run
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}" python "plugins/claude-ecosystem/skills/social-intelligence/scripts/state_manager.py" append scan-log.jsonl '{"scan_id":"scan-YYYYMMDD-HHMMSS","timestamp":"...","accounts_scanned":N,...}'

# Write each analyzed post
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}" python "plugins/claude-ecosystem/skills/social-intelligence/scripts/state_manager.py" append posts-index.jsonl '{"post_id":"...","author_handle":"...","text":"...","relevance_score":0.92,...}'

# Write each insight
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}" python "plugins/claude-ecosystem/skills/social-intelligence/scripts/state_manager.py" append insights-log.jsonl '{"insight_id":"insight-{seq}","summary":"...","status":"pending_review",...}'
```

#### Step 8: Update Last Scanned Timestamps

For each successfully scanned account, update the last_scanned timestamp:

```bash
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}" python "plugins/claude-ecosystem/skills/social-intelligence/scripts/state_manager.py" last-scanned "@handle" "2026-02-15T14:30:00Z"
```

#### Step 9: Present Summary

Display a concise summary to the user:

```markdown
## Scan Complete

**Accounts scanned:** 5 | **Posts found:** 47 | **New posts:** 8 | **Relevant:** 3

### Key Findings

1. [@borischerny] New hook event type announced (score: 0.92, feature_announcement)
   > "Just shipped support for a new SessionPause hook event..."
   [View on X](https://x.com/borischerny/status/1893456789012345678)

### Pending Insights (1)

- **insight-42**: New SessionPause hook event (confidence: 0.85)
  - Areas: hook-management, claude-code-observability
  - Action: Update hook documentation

Run `/claude-ecosystem:social-intelligence report` to see full details.
```

## Generate Report

### Arguments

| Flag | Default | Options |
|------|---------|---------|
| `--since` | (all time) | Any ISO date `YYYY-MM-DD` |
| `--status` | `all` | `pending`, `all`, `new`, `analyzed`, `actioned`, `dismissed` |
| `--format` | `markdown` | `markdown`, `json` |
| `--save` | (off) | When present, saves report to `.claude/social-intelligence/reports/` |

### Workflow

Run the report generator:

```bash
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}" python "plugins/claude-ecosystem/skills/social-intelligence/scripts/generate_report.py" --since "YYYY-MM-DD" --status "pending" --format markdown --save
```

Display the output directly to the user. If `--save` is used, confirm the saved file path.

## Apply Insights

Read pending insights, execute suggested actions, and update insight status.

### Workflow

#### Step 1: Read Pending Insights

```bash
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}" python "plugins/claude-ecosystem/skills/social-intelligence/scripts/state_manager.py" read insights-log.jsonl --status pending_review
```

#### Step 2: Present to User

Display pending insights with their suggested actions and ask user to select which to apply.

#### Step 3: Execute Selected Actions

For each approved insight:

1. Execute the `action_suggested` (e.g., update documentation, create issue, modify skill)
2. Log the action to `actions-log.jsonl`:

```bash
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}" python "plugins/claude-ecosystem/skills/social-intelligence/scripts/state_manager.py" append actions-log.jsonl '{"action_id":"action-{seq}","insight_id":"...","action_type":"...","description":"...","status":"completed","timestamp":"..."}'
```

#### Step 4: Update Insight Status

```bash
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}" python "plugins/claude-ecosystem/skills/social-intelligence/scripts/state_manager.py" update insights-log.jsonl insight_id "insight-42" '{"status":"actioned"}'
```

## Refresh Accounts

Navigate to the user's X following list and extract account handles to populate `accounts.json`.

### Workflow

#### Step 1: Load MCP Tools

Load `claude-in-chrome` tools via ToolSearch (same as scan step 3).

#### Step 2: Navigate to Following List

Read the `following_list_url` from `accounts.json`, then:

1. `tabs_create_mcp` -- Open a new tab
2. `navigate` to the following list URL
3. `get_page_text` -- Extract the page content
4. `javascript_tool` -- Scroll to load more accounts if needed

#### Step 3: Extract Handles

From the page text, extract X handles (patterns like `@username`).

#### Step 4: Classify Accounts

For each extracted handle, attempt to classify priority:

- Search for "anthropic" or "claude" in their bio/description text
- Known Claude Code team members -> `critical`
- Anthropic employees -> `high`
- AI/ML community -> `medium`
- Others -> `low`

**Note**: Priority classification may need manual refinement. Present the list to the user for review before saving.

#### Step 5: Update accounts.json

After user confirmation, update `plugins/claude-ecosystem/skills/social-intelligence/config/accounts.json`:

- Add new accounts
- Preserve existing priority overrides
- Update `last_refreshed` timestamp

## Discover Accounts

Search X for new Anthropic/Claude Code-related accounts not yet in the monitored list. Uses X search to find people actively tweeting about Claude Code.

### Workflow

#### Step 1: Load MCP Tools

Load `claude-in-chrome` tools via ToolSearch (same as scan step 3).

#### Step 2: Read Discovery Config

Read `discover_searches` from `accounts.json` for pre-configured search queries:

```json
[
  {"query": "\"claude code\" from:verified", "description": "Find verified accounts tweeting about Claude Code"},
  {"query": "\"anthropic\" \"claude\" engineer OR developer", "description": "Find Anthropic engineers discussing Claude"},
  {"query": "\"claude code\" shipped OR launched OR released", "description": "Find accounts announcing Claude Code features"},
  {"query": "\"@anthropicai\" claude code tip OR trick OR feature", "description": "Find accounts sharing Claude Code tips that mention Anthropic"}
]
```

#### Step 3: Execute Searches

For each search query:

1. `tabs_create_mcp` -- Open a new tab (reuse for subsequent searches)
2. `navigate` to `https://x.com/search?q={encoded_query}&f=user` for people search, then also `&f=live` for recent tweets
3. `get_page_text` -- Extract search results
4. Wait `navigation_delay_ms` between navigations

#### Step 4: Extract Candidate Accounts

From search results, extract:

- Account handles (`@username`)
- Display names
- Bio text snippets (for priority classification)

Filter out accounts already in `accounts.json`.

#### Step 5: Classify Candidates

Auto-classify priority based on bio/content signals:

| Signal | Priority |
|--------|----------|
| Bio contains "claude code" AND ("anthropic" OR "@anthropic") | `critical` |
| Bio contains "anthropic" AND (engineer OR developer OR research) | `high` |
| Bio contains "anthropic" (any role) | `high` |
| Tweets frequently about Claude Code (3+ results) | `medium` |
| Single mention or retweet | `low` |

#### Step 6: Present Candidates for Review

Display discovered accounts to the user:

```markdown
## Discovered Accounts

Found 7 new accounts not yet monitored:

### Suggested Critical
- **@newengineer** - "Building Claude Code at Anthropic"

### Suggested High
- **@anthropicdev** - "Software engineer at Anthropic"

### Suggested Medium
- **@aidevtips** - Tweets about Claude Code frequently

### Suggested Low
- **@techblogger** - One tweet about Claude Code

Add all suggested? Or select specific accounts to add?
```

#### Step 7: Update accounts.json

After user confirmation, add selected accounts to `accounts.json` with `"source": "discovered"` tag.

### Custom Search

Users can also pass a custom search query:

```text
/claude-ecosystem:social-intelligence discover-accounts "agent SDK anthropic"
```

This runs a single X search with the provided query and follows the same extract/classify/review flow.

## Show Status

Display scan history and data statistics.

### Workflow

```bash
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}" python "plugins/claude-ecosystem/skills/social-intelligence/scripts/state_manager.py" stats
```

Parse the JSON output and display:

```markdown
## Social Intelligence Status

**Data directory:** .claude/social-intelligence/data/
**Current sequence:** 42

| File | Entries | Size | Newest | Oldest |
|------|---------|------|--------|--------|
| scan-log.jsonl | 5 | 2.1 KB | 2026-02-15T14:30:00Z | 2026-02-10T09:00:00Z |
| posts-index.jsonl | 127 | 45.3 KB | 2026-02-15T14:30:05Z | 2026-02-10T09:01:00Z |
| insights-log.jsonl | 8 | 3.2 KB | 2026-02-15T14:31:00Z | 2026-02-10T09:15:00Z |
| actions-log.jsonl | 2 | 0.8 KB | 2026-02-14T16:00:00Z | 2026-02-11T10:30:00Z |

**Orphaned batch files:** 0
**Orphaned lock files:** 0
```

## Data Maintenance

### Migrate

Normalize all existing JSONL data to v2 schema and deduplicate:

```bash
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}" python "plugins/claude-ecosystem/skills/social-intelligence/scripts/state_manager.py" migrate
```

This command:

- Renames deprecated fields (`content_text` -> `text`, `relevance_category` -> `category`, etc.)
- Constructs missing `url` fields from `author_handle` + `post_id`
- Normalizes `post_id` to `{handle}-{numeric_id}` format
- Deduplicates posts by numeric ID (keeps last occurrence)
- Deduplicates insights by `insight_id`
- Removes orphaned batch and lock files

### Compact

Remove duplicates from a specific file:

```bash
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}" python "plugins/claude-ecosystem/skills/social-intelligence/scripts/state_manager.py" compact posts-index.jsonl
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}" python "plugins/claude-ecosystem/skills/social-intelligence/scripts/state_manager.py" compact insights-log.jsonl
```

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `CLAUDE_X_SCAN_DEV_ROOT` | (unset) | Dev mode: override data directory |
| `CLAUDE_X_SCAN_DEPTH` | `shallow` | Default scan depth |
| `CLAUDE_X_SCAN_THRESHOLD` | `0.4` | Relevance score threshold |

When `CLAUDE_X_SCAN_DEV_ROOT` is set, all data writes go to `{DEV_ROOT}/.claude/social-intelligence/data/` instead of the project directory.

## Data Files

All state is stored in `{project}/.claude/social-intelligence/data/` (gitignored):

| File | Purpose | Dedup Key |
|------|---------|-----------|
| `.seq` | Monotonic sequence counter | N/A |
| `scan-log.jsonl` | Scan activity log | `scan_id` |
| `posts-index.jsonl` | Processed posts | `post_id` (numeric suffix) |
| `insights-log.jsonl` | Extracted intelligence | `insight_id` |
| `actions-log.jsonl` | Actions taken | `action_id` |

Reports are saved to `{project}/.claude/social-intelligence/reports/` when `--save` is used.

## Encapsulation

This skill follows the anti-duplication principle:

- Stores ONLY tweet text, metadata, insights, and action proposals
- When an insight references Claude Code documentation, queries `docs-management` at runtime
- No Claude Code documentation content is duplicated in state files

## Future: Scheduling

> **Research needed**: Scheduling can be added later. Potential approaches:
>
> 1. Windows Task Scheduler + headless `claude -p` with this skill as prompt
> 2. SessionStart hook with time-since-last-scan check
> 3. Cron job (Unix) or Task Scheduler (Windows) invoking Claude CLI
>
> Key constraint: `claude-in-chrome` requires Chrome to be running with the extension active.
> Research via MCP (perplexity) for best practices on scheduling Claude Code tasks.
