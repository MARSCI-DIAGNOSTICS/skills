# Action: storage

Analyze the Claude Code storage directory (`~/.claude/`) to identify bloat, session accumulation, and provide cleanup recommendations.

## Arguments

- `--verbose` - Show detailed file listings in addition to summary

## Workflow

### Step 1: Comprehensive Storage Analysis

```bash
echo "Claude Code Storage Analysis"
echo "============================"

TOTAL=$(du -sh ~/.claude 2>/dev/null | cut -f1)
echo "Total: $TOTAL"

echo "By Category:"
for dir in projects debug plugins file-history plans shell-snapshots todos statsig local; do
  if [ -d "$HOME/.claude/$dir" ]; then
    SIZE=$(du -sh "$HOME/.claude/$dir" 2>/dev/null | cut -f1)
    COUNT=$(find "$HOME/.claude/$dir" -type f 2>/dev/null | wc -l)
    printf "  %-16s %8s  (%d files)\n" "$dir/" "$SIZE" "$COUNT"
  fi
done

for file in history.jsonl settings.json settings.local.json CLAUDE.md; do
  if [ -f "$HOME/.claude/$file" ]; then
    SIZE=$(du -sh "$HOME/.claude/$file" 2>/dev/null | cut -f1)
    printf "  %-16s %8s\n" "$file" "$SIZE"
  fi
done
```

### Step 2: Project Breakdown (Top 5)

```bash
echo "Projects (top 5 by size):"
du -sh ~/.claude/projects/*/ 2>/dev/null | sort -rh | head -5
```

### Step 3: Current Project Analysis

Analyze session and agent files for the current project with age breakdown.

### Step 4: Debug Folder Analysis

```bash
if [ -d "$HOME/.claude/debug" ]; then
  DEBUG_SIZE=$(du -sh "$HOME/.claude/debug" 2>/dev/null | cut -f1)
  DEBUG_COUNT=$(find "$HOME/.claude/debug" -type f 2>/dev/null | wc -l)
  OLD_DEBUG=$(find "$HOME/.claude/debug" -type f -mtime +7 2>/dev/null | wc -l)
fi
```

### Step 5: Large Files Detection

```bash
find ~/.claude -type f -size +10M 2>/dev/null
```

### Step 6: Reclaimable Space Summary

Calculate space reclaimable from old sessions, agents, debug files, and statsig cache.

### Step 7: Generate Recommendations

| Condition | Severity | Recommendation |
|-----------|----------|----------------|
| Total > 1GB | CRITICAL | Run `/user-config prune --include-debug` |
| Total > 500MB | WARNING | Run `/user-config prune 7` |
| Agent files > 1000 | WARNING | Run `/user-config cleanup-agents 7` |
| Debug > 100MB | WARNING | Run `/user-config cleanup-debug 7` |
| Files >7 days exist | TIP | Run `/user-config cleanup-sessions 7 --dry-run` |

### Step 8: Quick Commands Summary

```text
Quick Commands:
/user-config cleanup-sessions 7     - Remove session files >7 days old
/user-config cleanup-agents 7       - Remove agent transcripts >7 days old
/user-config cleanup-debug 7        - Remove debug transcripts >7 days old
/user-config prune 7                - Comprehensive cleanup
/user-config prune --include-debug  - Full cleanup including debug folder
```

## Folder Reference

| Folder | Contents | Safe to Clean |
|--------|----------|---------------|
| `projects/` | Session and agent transcripts per project | Yes (old files) |
| `debug/` | Debug transcripts for troubleshooting | Yes (old files) |
| `plugins/` | Installed plugin cache | Only via reinstall |
| `file-history/` | File edit history for undo | Careful - loses undo |
| `plans/` | Saved execution plans | Yes (old files) |
| `shell-snapshots/` | Shell state snapshots | Yes |
| `todos/` | Todo list state | Yes (old files) |
| `statsig/` | Analytics cache | Always safe |
| `history.jsonl` | Command history | Usually keep |
| `settings.json` | User settings | Never clean |
| `CLAUDE.md` | User instructions | Never clean |

## Notes

- Storage analysis is read-only and makes no changes
- Use specific cleanup actions to actually free space
- Plugin cache can only be cleaned by reinstalling plugins
