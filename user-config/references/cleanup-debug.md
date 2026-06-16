# Action: cleanup-debug

Remove old debug transcript files from Claude Code's debug directory. Debug files store execution traces for troubleshooting and can accumulate significantly.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `[days]` | Remove debug files older than N days (must be non-negative integer) | 7 |
| `--dry-run` | Preview without deleting | false |

## Safety Features

- **Dry-run available**: Always preview before deleting
- **Confirmation required**: Claude MUST use AskUserQuestion tool before any deletion
- **Preserves recent files**: Never deletes today's debug files
- **Input validation**: DAYS must be a non-negative integer

## What Are Debug Files?

The `~/.claude/debug/` folder contains transcript files generated when Claude Code encounters issues or when debug mode is enabled. These files help Anthropic diagnose problems but are not needed for normal operation.

**Characteristics:**

- Location: `~/.claude/debug/`
- File types: `.jsonl` transcripts, crash logs, trace files
- Growth rate: Varies with usage; can grow 50-100 MB/week in heavy usage
- Safe to delete: Yes, completely safe

## Workflow

### Step 1: Parse and Validate Arguments

```text
DAYS = first numeric argument OR 7
DRY_RUN = true if --dry-run present

# VALIDATION: Ensure DAYS is a non-negative integer
if DAYS is not a valid non-negative integer:
  Report error: "Error: days must be a non-negative integer (got: {value})"
  Exit without action
```

### Step 2: Analyze Debug Directory

```bash
DEBUG_DIR="$HOME/.claude/debug"

echo "Debug Cleanup"
echo "============="

if [ ! -d "$DEBUG_DIR" ]; then
  echo "No debug directory found at $DEBUG_DIR"
  exit 0
fi

TOTAL_SIZE=$(du -sh "$DEBUG_DIR" 2>/dev/null | cut -f1)
TOTAL_COUNT=$(find "$DEBUG_DIR" -type f 2>/dev/null | wc -l)

echo "Debug directory: $DEBUG_DIR"
echo "Total size: $TOTAL_SIZE ($TOTAL_COUNT files)"
```

### Step 3: Show Age Breakdown

```bash
echo "Age Breakdown:"
echo "  Today:     $(find "$DEBUG_DIR" -type f -mtime 0 2>/dev/null | wc -l) files"
echo "  1-3 days:  $(find "$DEBUG_DIR" -type f -mtime +0 -mtime -3 2>/dev/null | wc -l) files"
echo "  3-7 days:  $(find "$DEBUG_DIR" -type f -mtime +2 -mtime -7 2>/dev/null | wc -l) files"
echo "  >7 days:   $(find "$DEBUG_DIR" -type f -mtime +7 2>/dev/null | wc -l) files"
```

### Step 4: Preview or Delete

**Dry Run Mode:**

```bash
echo "[DRY RUN] Would remove $REMOVE_COUNT files (${REMOVE_SIZE:-0})"
echo "To execute, run: /user-config cleanup-debug $DAYS"
```

**Execute (CONFIRMATION REQUIRED):**

```text
1. Show preview (same as dry run)
2. MANDATORY: Use AskUserQuestion tool to get explicit confirmation:
   Question: "Delete {count} debug files ({size})? This cannot be undone."
   Options: ["Yes, delete files", "No, cancel"]
3. If user confirms "Yes", execute:
   if [ "$DAYS" -eq 0 ]; then
     rm -rf "$DEBUG_DIR"/*
   else
     find "$DEBUG_DIR" -type f -mtime +$DAYS -delete
   fi
4. If user selects "No" or any other response, abort without deletion
5. Report results with before/after comparison
```

**CRITICAL: Never delete files without explicit user confirmation via AskUserQuestion.**

### Step 5: Verification

```bash
NEW_SIZE=$(du -sh "$DEBUG_DIR" 2>/dev/null | cut -f1)
NEW_COUNT=$(find "$DEBUG_DIR" -type f 2>/dev/null | wc -l)

echo "Cleanup Complete!"
echo "Before: $TOTAL_SIZE ($TOTAL_COUNT files)"
echo "After:  ${NEW_SIZE:-0} ($NEW_COUNT files)"
echo "Freed:  ${REMOVE_SIZE:-0}"
```

## Cleanup Strategies

| Goal | Command |
|------|---------|
| Conservative | `/user-config cleanup-debug 7` |
| Moderate | `/user-config cleanup-debug 3` |
| Aggressive | `/user-config cleanup-debug 1` |
| Nuclear (all) | `/user-config cleanup-debug 0` |
| Preview | `/user-config cleanup-debug --dry-run` |

## Notes

- Debug files are completely safe to delete - they are only for troubleshooting
- Unlike session files, debug files are not per-project - they are global
- Debug files are NOT included in `prune` by default - use `--include-debug`
- For maximum cleanup including debug, use `prune --nuclear`
- If you need to report a bug, keep recent debug files (last 24 hours)
