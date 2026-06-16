---
name: diagnose-performance
description: Run comprehensive Claude Code performance diagnostics - analyzes storage, API status, and known issues
allowed-tools: Bash, Read, Glob, Grep, Task, WebSearch, WebFetch
---

# Diagnose Performance

Comprehensive performance diagnostic for Claude Code. This orchestrator command combines local analysis with API status checks and known issue research.

## Usage

```text
/diagnose-performance
/diagnose-performance --quick    # Skip external checks
```

## Arguments

| Argument | Description |
|----------|-------------|
| `--quick` | Skip API status and GitHub issue checks (local analysis only) |

## What Gets Analyzed

1. **Local Storage** - ALL folders in ~/.claude/ with size and file counts
2. **Debug Folder** - Debug transcript accumulation (often overlooked)
3. **Session/Agent Files** - Per-project file counts and age breakdown
4. **Large Files** - Files >10MB that may indicate bloat
5. **API Status** - Anthropic service status (status.anthropic.com)
6. **Known Issues** - Recent GitHub issues affecting performance
7. **Version Check** - Current Claude Code version

## Workflow

### Step 1: Version and Environment Check

```bash
echo "Performance Diagnostic Report"
echo "============================="
echo "Generated: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo ""

# Get Claude Code version
VERSION=$(claude --version 2>/dev/null | head -1)
echo "Claude Code: $VERSION"
echo "Platform: $(uname -s) $(uname -m)"
echo ""
```

### Step 2: Comprehensive Storage Analysis

Analyze ALL folders in ~/.claude/:

```bash
echo "STORAGE ANALYSIS"
echo "================"
echo ""

# Total size
TOTAL=$(du -sh ~/.claude 2>/dev/null | cut -f1)
echo "Total ~/.claude size: $TOTAL"
echo ""

# Status determination
TOTAL_MB=$(du -sm ~/.claude 2>/dev/null | cut -f1)
if [ "$TOTAL_MB" -gt 1000 ]; then
  STATUS="CRITICAL"
elif [ "$TOTAL_MB" -gt 500 ]; then
  STATUS="WARNING"
else
  STATUS="HEALTHY"
fi
echo "Status: $STATUS"
echo ""

# By category - ALL folders
echo "By Category:"
echo "------------"
printf "  %-18s %10s %12s\n" "Folder" "Size" "Files"
printf "  %-18s %10s %12s\n" "------" "----" "-----"

for dir in projects debug plugins file-history plans shell-snapshots todos statsig local; do
  if [ -d "$HOME/.claude/$dir" ]; then
    SIZE=$(du -sh "$HOME/.claude/$dir" 2>/dev/null | cut -f1)
    COUNT=$(find "$HOME/.claude/$dir" -type f 2>/dev/null | wc -l)
    printf "  %-18s %10s %12d\n" "$dir/" "$SIZE" "$COUNT"
  fi
done

# Individual files
for file in history.jsonl settings.json; do
  if [ -f "$HOME/.claude/$file" ]; then
    SIZE=$(du -sh "$HOME/.claude/$file" 2>/dev/null | cut -f1)
    printf "  %-18s %10s\n" "$file" "$SIZE"
  fi
done
```

### Step 3: Current Project Deep Dive

```bash
echo ""
echo "CURRENT PROJECT"
echo "==============="

# Cross-platform project path detection
if [ -n "$MSYSTEM" ]; then
  PROJECT_NAME=$(pwd | sed 's|^/\([a-z]\)/|\U\1--|' | sed 's|/|--|g')
else
  PROJECT_NAME=$(pwd | sed 's/[\/:]/-/g' | sed 's/^-//')
fi
PROJECT_DIR="$HOME/.claude/projects/$PROJECT_NAME"

echo "Project: $PROJECT_NAME"

if [ -d "$PROJECT_DIR" ]; then
  PROJECT_SIZE=$(du -sh "$PROJECT_DIR" 2>/dev/null | cut -f1)
  TOTAL_FILES=$(find "$PROJECT_DIR" -maxdepth 1 -name "*.jsonl" 2>/dev/null | wc -l)
  AGENT_FILES=$(find "$PROJECT_DIR" -maxdepth 1 -name "agent-*.jsonl" 2>/dev/null | wc -l)
  SESSION_FILES=$((TOTAL_FILES - AGENT_FILES))

  echo "Size: $PROJECT_SIZE"
  echo "Session files: $SESSION_FILES"
  echo "Agent transcripts: $AGENT_FILES"
  echo ""
  echo "By Age:"
  echo "  Today:     $(find "$PROJECT_DIR" -maxdepth 1 -name "*.jsonl" -mtime 0 2>/dev/null | wc -l)"
  echo "  1-3 days:  $(find "$PROJECT_DIR" -maxdepth 1 -name "*.jsonl" -mtime +0 -mtime -3 2>/dev/null | wc -l)"
  echo "  3-7 days:  $(find "$PROJECT_DIR" -maxdepth 1 -name "*.jsonl" -mtime +2 -mtime -7 2>/dev/null | wc -l)"
  echo "  >7 days:   $(find "$PROJECT_DIR" -maxdepth 1 -name "*.jsonl" -mtime +7 2>/dev/null | wc -l)"
else
  echo "No session data found"
fi
```

### Step 4: Debug Folder Analysis

```bash
echo ""
echo "DEBUG TRANSCRIPTS"
echo "================="

if [ -d "$HOME/.claude/debug" ]; then
  DEBUG_SIZE=$(du -sh "$HOME/.claude/debug" 2>/dev/null | cut -f1)
  DEBUG_COUNT=$(find "$HOME/.claude/debug" -type f 2>/dev/null | wc -l)
  OLD_DEBUG=$(find "$HOME/.claude/debug" -type f -mtime +7 2>/dev/null | wc -l)

  echo "Total: $DEBUG_SIZE ($DEBUG_COUNT files)"
  echo ">7 days: $OLD_DEBUG files"

  # Warning if debug is large
  DEBUG_MB=$(du -sm "$HOME/.claude/debug" 2>/dev/null | cut -f1)
  if [ "$DEBUG_MB" -gt 100 ]; then
    echo "WARNING: Debug folder is large. Run /cleanup-debug to reclaim space."
  fi
else
  echo "No debug folder found"
fi
```

### Step 5: Large Files Detection

```bash
echo ""
echo "LARGE FILES (>10MB)"
echo "==================="

LARGE_COUNT=$(find ~/.claude -type f -size +10M 2>/dev/null | wc -l)
if [ "$LARGE_COUNT" -gt 0 ]; then
  find ~/.claude -type f -size +10M -exec ls -lh {} \; 2>/dev/null | \
    awk '{print "  " $5 "  " $9}' | head -10
  if [ "$LARGE_COUNT" -gt 10 ]; then
    echo "  ... and $((LARGE_COUNT - 10)) more"
  fi
else
  echo "  None found"
fi
```

### Step 6: Reclaimable Space Summary

```bash
echo ""
echo "RECLAIMABLE SPACE"
echo "================="

TOTAL_RECLAIMABLE=0

# Sessions >7 days
if [ -d "$PROJECT_DIR" ]; then
  OLD_SESSIONS=$(find "$PROJECT_DIR" -maxdepth 1 -name "*.jsonl" ! -name "agent-*" -mtime +7 2>/dev/null | wc -l)
  OLD_AGENTS=$(find "$PROJECT_DIR" -maxdepth 1 -name "agent-*.jsonl" -mtime +7 2>/dev/null | wc -l)
  echo "  Sessions >7 days: $OLD_SESSIONS files"
  echo "  Agents >7 days:   $OLD_AGENTS files"
fi

# Debug
if [ -d "$HOME/.claude/debug" ]; then
  OLD_DEBUG=$(find "$HOME/.claude/debug" -type f -mtime +7 2>/dev/null | wc -l)
  OLD_DEBUG_SIZE=$(find "$HOME/.claude/debug" -type f -mtime +7 -exec du -ch {} + 2>/dev/null | tail -1 | cut -f1)
  echo "  Debug >7 days:    $OLD_DEBUG files (${OLD_DEBUG_SIZE:-0})"
fi

# Statsig (always safe)
if [ -d "$HOME/.claude/statsig" ]; then
  STATSIG_SIZE=$(du -sh "$HOME/.claude/statsig" 2>/dev/null | cut -f1)
  echo "  Statsig cache:    $STATSIG_SIZE (always safe)"
fi
```

### Step 7: Spawn Performance Diagnostician (unless --quick)

If `--quick` is NOT specified, use the Task tool to spawn the `performance-diagnostician` agent:

```text
Spawn performance-diagnostician agent to:
1. Check API status at status.anthropic.com
2. Search for known Claude Code performance issues on GitHub
3. Provide prioritized recommendations based on current version
```

### Step 8: Aggregate and Present Results

Combine local analysis with agent findings into a unified report:

```text
EXTERNAL CHECKS (from agent)
============================
API Status: {OPERATIONAL | DEGRADED | OUTAGE}
- Recent incidents: {list}

Known Issues:
- {issue number}: {title}
  Workaround: {workaround}

RECOMMENDATIONS
===============
Priority 1: {most impactful action}
Priority 2: {second action}
Priority 3: {third action}

QUICK COMMANDS
==============
/cleanup-sessions 7     - Remove old session files
/cleanup-agents 7       - Remove old agent transcripts
/cleanup-debug 7        - Remove old debug transcripts
/prune-cache 7          - Comprehensive cleanup
/prune-cache --nuclear  - Maximum cleanup (all folders)
/clear                  - Reset context window
```

## Example Output

```text
Performance Diagnostic Report
=============================
Generated: 2025-12-26 16:45:00 EST

Claude Code: 2.0.75 (Claude Code)
Platform: MINGW64_NT-10.0 x86_64

STORAGE ANALYSIS
================

Total ~/.claude size: 1.5G

Status: CRITICAL

By Category:
------------
  Folder                   Size        Files
  ------                   ----        -----
  projects/               950M         4928
  debug/                  359M          878
  plugins/                149M          312
  file-history/            53M         1205
  plans/                  2.4M           15
  shell-snapshots/        1.5M           12
  todos/                  1.1M           45
  history.jsonl           480K

CURRENT PROJECT
===============
Project: D--repos-gh-melodic-claude-code-plugins
Size: 948M
Session files: 510
Agent transcripts: 2140

By Age:
  Today:     492
  1-3 days:  948
  3-7 days:  353
  >7 days:   406

DEBUG TRANSCRIPTS
=================
Total: 359M (878 files)
>7 days: 0 files

LARGE FILES (>10MB)
===================
  15M   ~/.claude/projects/.../session-abc123.jsonl
  14M   ~/.claude/projects/.../session-def456.jsonl

RECLAIMABLE SPACE
=================
  Sessions >7 days: 406 files
  Agents >7 days:   0 files
  Debug >7 days:    0 files (0)
  Statsig cache:    34K (always safe)

EXTERNAL CHECKS
===============
API Status: OPERATIONAL
- Dec 23: Opus 4.5 elevated errors (resolved)
- Dec 22: Opus 4.5 elevated errors (resolved)

Known Issues:
- #14476: Input lag in v2.0.72+ (OPEN)
  Workaround: Rollback to v2.0.36
- #10881: Long session degradation (OPEN)
  Workaround: Restart Claude Code periodically

RECOMMENDATIONS
===============
Priority 1: Run /prune-cache --nuclear (frees ~400MB)
Priority 2: Restart Claude Code to reset session state
Priority 3: Use /clear proactively at 75% context

QUICK COMMANDS
==============
/cleanup-sessions 7     - Remove old session files
/cleanup-agents 7       - Remove old agent transcripts
/cleanup-debug 7        - Remove old debug transcripts
/prune-cache 7          - Comprehensive cleanup
/prune-cache --nuclear  - Maximum cleanup (all folders)
/clear                  - Reset context window
```

## Notes

- This is the main entry point for performance troubleshooting
- For storage-only analysis, use `/check-claude-storage`
- For quick cleanup, use individual `/cleanup-*` commands
- The `--quick` flag skips network requests for offline diagnostics
- Debug folder is now included in analysis (was previously missed)
