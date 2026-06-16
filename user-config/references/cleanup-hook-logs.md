# Action: cleanup-hook-logs

Delete old hook log files to free up disk space.

## Arguments

- First argument (optional): Number of days - delete logs older than N days (default: 30, or from `CLAUDE_HOOK_LOG_RETENTION_MAX_AGE_DAYS`)
- `--dry-run` or `-n`: Preview what would be deleted without actually deleting

## Task

Find and run the `cleanup_logs.py` script from the `claude-code-observability` plugin to delete old log files.

**Script location**: Look for `cleanup_logs.py` in the installed plugin at:

- `plugins/claude-code-observability/hooks/cleanup_logs.py`
- Or use glob: `**/claude-code-observability/**/cleanup_logs.py`

**Arguments**:

- Days: Use the first argument if provided, otherwise default to 30 days
- If `--dry-run` or `-n` was specified, pass that flag
- Otherwise pass `--verbose` to show progress

**Example command** (adjust path based on where script is found):

```bash
python /path/to/cleanup_logs.py --days 30 --verbose
```

The script uses `CLAUDE_PROJECT_DIR` environment variable (already available in session) to locate the log directory at `.claude/logs/hooks/`. No `CLAUDE_PLUGIN_ROOT` is needed.

## What Gets Deleted

- All `.jsonl` files in `.claude/logs/hooks/` older than the specified days
- Both base files (`events-2025-12-05.jsonl`) and rotated files (`events-2025-12-05-001.jsonl`)

## Configuration

The default retention period can be configured via environment variable:

```bash
# In .claude/settings.json "env" section:
"CLAUDE_HOOK_LOG_RETENTION_MAX_AGE_DAYS": "30"
```

## Safety Notes

- Use `--dry-run` first to preview what will be deleted
- Deleted files cannot be recovered
- Log files contain session metadata for debugging - ensure you don't need them before deleting
