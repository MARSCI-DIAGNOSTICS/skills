# Action: prune

Comprehensive cleanup of Claude Code's cache directory. This is the "nuclear option" for freeing maximum disk space.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `[days]` | Remove files older than N days (must be non-negative integer) | 7 |
| `--dry-run` | Preview without deleting | false |
| `--all-projects` | Clean all projects, not just current | false |
| `--include-debug` | Also clean debug/ folder | false |
| `--include-todos` | Also clean old todo state files | false |
| `--nuclear` | Maximum cleanup: 0 days + all flags + stale locks | false |

## Safety Features

- **Dry-run available**: Always preview before deleting
- **Confirmation required**: Claude MUST use AskUserQuestion tool before any deletion
- **Project scoped**: Defaults to current project only
- **Protected files**: User settings, CLAUDE.md, and commands are NEVER deleted
- **Input validation**: DAYS must be a non-negative integer

## What Gets Cleaned

### Always Cleaned

| Category | Location | Files | Notes |
|----------|----------|-------|-------|
| Sessions | `projects/*/` | `*.jsonl` (non-agent) | Conversation history |
| Agents | `projects/*/` | `agent-*.jsonl` | Subagent transcripts |
| Statsig | `statsig/` | All | Analytics cache (always safe) |
| Shell Snapshots | `shell-snapshots/` | All | Shell state snapshots |
| Plans | `plans/` | `*.json` older than N days | Saved execution plans |

### With --include-debug

| Category | Location | Files |
|----------|----------|-------|
| Debug | `debug/` | All older than N days |

### With --include-todos

| Category | Location | Files |
|----------|----------|-------|
| Todos | `todos/` | `*.json` older than N days |

### With --nuclear

Maximum cleanup mode: Sets DAYS=0 (all files regardless of age) and enables all flags: `--include-debug --include-todos --all-projects`

Additionally, --nuclear cleans:

| Category | Location | Notes |
|----------|----------|-------|
| Stale Locks | `~/.local/state/claude/locks/` | Fixes "Another Claude process is currently running" errors |

## What is NEVER Cleaned

| Category | Reason |
|----------|--------|
| `~/.claude/CLAUDE.md` | User instructions |
| `~/.claude/settings.json` | User settings |
| `~/.claude/settings.local.json` | Local settings |
| `~/.claude/commands/` | User commands |
| `~/.claude/skills/` | User skills |
| `~/.claude/agents/` | User agents |
| `~/.claude/hooks/` | User hooks |
| `~/.claude/history.jsonl` | Command history |
| `~/.claude/plugins/` | Installed plugins (use /plugin uninstall) |
| `~/.claude/file-history/` | Edit undo history (dangerous to clear) |

## Workflow

### Step 1: Parse and Validate Arguments

```text
DAYS = first numeric argument OR 7
DRY_RUN = true if --dry-run present
ALL_PROJECTS = true if --all-projects present
INCLUDE_DEBUG = true if --include-debug present
INCLUDE_TODOS = true if --include-todos present

# VALIDATION: Ensure DAYS is a non-negative integer
if DAYS is not a valid non-negative integer:
  Report error: "Error: days must be a non-negative integer (got: {value})"
  Exit without action

# Handle --nuclear flag
if --nuclear present:
  DAYS = 0
  INCLUDE_DEBUG = true
  INCLUDE_TODOS = true
  ALL_PROJECTS = true
  CLEAN_LOCKS = true
```

### Step 2: Calculate Cleanup Totals

Calculate file counts and sizes for each category.

### Step 3: Preview or Execute

**Execute (CONFIRMATION REQUIRED):**

```text
1. Show cleanup summary
2. MANDATORY: Use AskUserQuestion tool to get explicit confirmation:
   Question: "Delete {total_count} files (~{total_size})? This cannot be undone."
   Options: ["Yes, delete files", "No, cancel"]
3. If user confirms "Yes", proceed with cleanup
4. If user selects "No" or any other response, abort without deletion
```

**CRITICAL: Never delete files without explicit user confirmation via AskUserQuestion.**

### Step 4: Verification

After deletion, report new total size of ~/.claude directory.

## Cleanup Strategies

| Goal | Command |
|------|---------|
| Quick cleanup | `/user-config prune 7` |
| Aggressive | `/user-config prune 3` |
| Preview only | `/user-config prune --dry-run` |
| Include debug | `/user-config prune --include-debug` |
| All projects | `/user-config prune --all-projects` |
| Maximum cleanup | `/user-config prune --nuclear` |

## Notes

- This is the most comprehensive cleanup command
- For targeted cleanup, use `cleanup-sessions`, `cleanup-agents`, or `cleanup-debug`
- Statsig cache is always safe to delete - it is analytics data
- Shell snapshots are always cleaned (they are temporary)
- Command history (`history.jsonl`) is preserved
- Plugin cache requires `/plugin uninstall` to clean
- File history (`file-history/`) is intentionally NOT cleaned
- Stale locks only cleaned with --nuclear - fixes `claude update` blocking issues
