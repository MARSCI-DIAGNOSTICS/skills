# Action: cleanup-sessions

Remove old session files from Claude Code's project cache to free disk space. By default, removes files older than 7 days from the current project only.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `[days]` | Remove sessions older than N days (must be non-negative integer) | 7 |
| `--dry-run` | Preview without deleting | false |
| `--all-projects` | Clean all projects, not just current | false |

## Safety Features

- **Dry-run available**: Always preview before deleting
- **Confirmation required**: Claude MUST use AskUserQuestion tool before any deletion
- **Preserves recent files**: Never deletes today's sessions
- **Project scoped**: Defaults to current project only
- **Input validation**: DAYS must be a non-negative integer

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

### Step 2: Determine Target Directory

```bash
if ALL_PROJECTS; then
  TARGET_DIR="$HOME/.claude/projects"
else
  PROJECT_PATH=$(pwd | sed 's/[\/:]/-/g' | sed 's/^-//')
  TARGET_DIR="$HOME/.claude/projects/$PROJECT_PATH"
fi
```

### Step 3: Find Files to Delete

```bash
FILES=$(find "$TARGET_DIR" -name "*.jsonl" -mtime +$DAYS 2>/dev/null)
COUNT=$(echo "$FILES" | grep -c . 2>/dev/null || echo 0)
SIZE=$(find "$TARGET_DIR" -name "*.jsonl" -mtime +$DAYS -exec du -ch {} + 2>/dev/null | tail -1 | cut -f1)
```

### Step 4: Preview or Delete

**Dry Run Mode:**

```text
Cleanup Preview (Dry Run)
=========================
Target: {target_dir}
Files older than: {days} days

Files to remove: {count}
Space to free: {size}

Sample files:
  {first 10 files with sizes}

To execute cleanup, run: /user-config cleanup-sessions {days}
```

**Execution Mode (CONFIRMATION REQUIRED):**

```text
1. Show preview (same as dry run)
2. MANDATORY: Use AskUserQuestion tool to get explicit confirmation:
   Question: "Delete {count} session files ({size})? This cannot be undone."
   Options: ["Yes, delete files", "No, cancel"]
3. If user confirms "Yes", execute:
   find "$TARGET_DIR" -name "*.jsonl" -mtime +$DAYS -delete
4. If user selects "No" or any other response, abort without deletion
5. Report results:
   "Deleted {count} files, freed {size}"
```

**CRITICAL: Never delete files without explicit user confirmation via AskUserQuestion.**

### Step 5: Verification

```bash
REMAINING=$(find "$TARGET_DIR" -name "*.jsonl" 2>/dev/null | wc -l)
REMAINING_SIZE=$(du -sh "$TARGET_DIR" 2>/dev/null | cut -f1)
echo "Remaining: $REMAINING files ($REMAINING_SIZE)"
```

## Notes

- This command removes BOTH session files and agent transcript files by age
- For agent-only cleanup, use `cleanup-agents`
- Files from today are never deleted regardless of settings
- Claude Code has a default 30-day auto-cleanup, but this command allows manual intervention
- Use `storage` first to understand current usage
