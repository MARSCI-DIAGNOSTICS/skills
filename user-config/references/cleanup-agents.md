# Action: cleanup-agents

Remove old agent transcript files from Claude Code's project cache. Agent files (prefixed with `agent-`) store subagent execution history and can accumulate rapidly.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `[days]` | Remove agent files older than N days (must be non-negative integer) | 7 |
| `--dry-run` | Preview without deleting | false |
| `--all-projects` | Clean all projects | false |

## Safety Features

- **Dry-run available**: Always preview before deleting
- **Confirmation required**: Claude MUST use AskUserQuestion tool before any deletion
- **Project scoped**: Defaults to current project only
- **Input validation**: DAYS must be a non-negative integer

## Why Agent Files Accumulate

Every time a subagent is spawned (via Task tool), Claude Code creates a new `agent-*.jsonl` file to store the agent's conversation transcript. In heavy development sessions with many parallel agents, this can result in hundreds or thousands of files.

**Example accumulation:**

- Single `/audit-skills` run: 20-50 agent files
- Heavy development day: 100-200 agent files
- Week of development: 500-1000 agent files

## Workflow

### Step 1: Parse and Validate Arguments

```text
DAYS = first numeric argument OR 7
DRY_RUN = true if --dry-run present
ALL_PROJECTS = true if --all-projects present

# VALIDATION: Ensure DAYS is a non-negative integer
if DAYS is not a valid non-negative integer:
  Report error: "Error: days must be a non-negative integer (got: {value})"
  Exit without action
```

### Step 2: Find Agent Files

```bash
PROJECT_PATH=$(pwd | sed 's/[\/:]/-/g' | sed 's/^-//')
TARGET_DIR="$HOME/.claude/projects/$PROJECT_PATH"

# Find agent-specific files
FILES=$(find "$TARGET_DIR" -name "agent-*.jsonl" -mtime +$DAYS 2>/dev/null)
COUNT=$(echo "$FILES" | grep -c . 2>/dev/null || echo 0)
SIZE=$(find "$TARGET_DIR" -name "agent-*.jsonl" -mtime +$DAYS -exec du -ch {} + 2>/dev/null | tail -1 | cut -f1)
```

### Step 3: Preview or Delete

**Dry Run:**

```text
Agent Cleanup Preview
=====================
Target: {target_dir}
Files older than: {days} days

Agent files to remove: {count}
Space to free: {size}

To execute, run: /user-config cleanup-agents {days}
```

**Execute (CONFIRMATION REQUIRED):**

```text
1. Show preview (same as dry run)
2. MANDATORY: Use AskUserQuestion tool to get explicit confirmation:
   Question: "Delete {count} agent files ({size})? This cannot be undone."
   Options: ["Yes, delete files", "No, cancel"]
3. If user confirms "Yes", execute:
   find "$TARGET_DIR" -name "agent-*.jsonl" -mtime +$DAYS -delete
4. If user selects "No" or any other response, abort without deletion
5. Report results:
   "Deleted {count} files, freed {size}"
```

**CRITICAL: Never delete files without explicit user confirmation via AskUserQuestion.**

## Notes

- Agent files are separate from session files - use `cleanup-sessions` for those
- Agent files grow quickly with heavy Task tool usage
- For comprehensive cleanup, use `prune`
- Agent files can be safely deleted - they are only used for `/resume` functionality
