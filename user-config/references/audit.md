# Action: audit

Perform a comprehensive health audit of Claude Code user configuration, including drift detection against the known structure manifest.

## Arguments

| Argument | Description |
|----------|-------------|
| `--fix` | Automatically fix issues where safe to do so |
| `--verbose` | Show detailed findings for each check |
| (no args) | Run full audit with summary report |

## Audit Categories

### 1. JSON Validity

Check that all JSON configuration files parse correctly:

| File | Check |
|------|-------|
| `~/.claude/settings.json` | Valid JSON syntax |
| `~/.claude.json` | Valid JSON syntax |
| `~/.claude/todos/*.json` | Valid JSON syntax |
| `~/.claude/plugins/installed_plugins.json` | Valid JSON syntax |

```python
import json
from pathlib import Path

def validate_json(path: Path) -> tuple[bool, str]:
    """Validate JSON file. Returns (valid, message)."""
    if not path.exists():
        return True, "Not present (OK)"
    try:
        json.load(open(path))
        return True, "Valid"
    except json.JSONDecodeError as e:
        return False, f"Invalid: {e}"

claude_dir = Path.home() / ".claude"
files_to_check = [
    claude_dir / "settings.json",
    Path.home() / ".claude.json",
]
files_to_check.extend(claude_dir.glob("todos/*.json"))
files_to_check.extend(claude_dir.glob("plugins/*.json"))
```

### 2. Structure Drift Detection

Compare actual `~/.claude/` structure against known manifest:

**Load the known structure from skill reference:**

Invoke the `claude-ecosystem:user-config-management` skill to access `references/known-structure.yaml` and compare against actual filesystem.

**Drift Categories:**

| Finding | Severity | Action |
|---------|----------|--------|
| New unknown directory | INFO | May indicate Claude Code update |
| New unknown file | INFO | Investigate purpose |
| Expected directory missing | WARN | May indicate incomplete install |
| Expected file missing | WARN | May indicate corruption |
| Structure version mismatch | INFO | Update manifest after verification |

```python
import yaml
from pathlib import Path

claude_dir = Path.home() / ".claude"

# Get actual directories
actual_dirs = {d.name for d in claude_dir.iterdir() if d.is_dir()}
actual_files = {f.name for f in claude_dir.iterdir() if f.is_file()}

# Compare against expected (from known-structure.yaml)
expected_dirs = {"debug", "file-history", "ide", "plans", "plugins",
                 "projects", "session-env", "shell-snapshots", "statsig", "todos"}
expected_files = {"settings.json", "history.jsonl", ".credentials.json"}

unknown_dirs = actual_dirs - expected_dirs
missing_dirs = expected_dirs - actual_dirs
unknown_files = actual_files - expected_files
```

### 3. Orphaned Resources

Detect orphaned files that may indicate issues:

| Check | Description |
|-------|-------------|
| Orphaned sessions | Session files without corresponding project |
| Stale IDE locks | Lock files from processes no longer running |
| Orphaned todos | Todo files for non-existent sessions |
| Abandoned file-history | History for sessions that were cleaned up |

```python
# Check for stale IDE locks
ide_locks = list((claude_dir / "ide").glob("*.lock"))
for lock in ide_locks:
    # Check if lock is stale (process not running)
    pass
```

### 4. Security Scan

Check for potential security issues (without exposing sensitive data):

| Check | Risk |
|-------|------|
| Credentials file permissions | Should be user-only readable |
| API keys in settings | Should not be in settings.json |
| MCP server credentials | Validate structure, not content |

```python
import os
import stat

creds_path = claude_dir / ".credentials.json"
if creds_path.exists():
    mode = os.stat(creds_path).st_mode
    if mode & stat.S_IROTH or mode & stat.S_IWOTH:
        print("WARNING: Credentials file is world-readable!")
```

### 5. Cross-Reference Integrity

Verify references between configuration areas:

| Check | Description |
|-------|-------------|
| Plugin references | Installed plugins exist in cache |
| Session references | Projects reference valid sessions |
| Todo references | Todos reference valid sessions |

## Output Format

### Summary Report (Default)

```markdown
# Claude Code Configuration Audit

**Audit Date:** 2025-12-30 16:52 UTC
**Claude Code Version:** (if detectable)
**Manifest Version:** 1.0

## Summary

| Category | Status | Issues |
|----------|--------|--------|
| JSON Validity | PASS | 0 |
| Structure Drift | WARNING | 2 new directories |
| Orphaned Resources | PASS | 0 |
| Security | PASS | 0 |
| Cross-References | PASS | 0 |

## Findings

### Structure Drift (2 issues)

| Finding | Severity | Details |
|---------|----------|---------|
| New directory: `telemetry/` | INFO | Unknown - may be new Claude Code feature |
| New directory: `cache/` | INFO | Unknown - may be new Claude Code feature |

**Recommendation:** After verifying these are legitimate Claude Code additions, update the known-structure.yaml manifest.
```

### Verbose Report (`--verbose`)

Include detailed per-check output with file paths and specific findings.

### Fix Mode (`--fix`)

Automatically fix safe issues:

- Remove stale IDE lock files
- Fix file permissions on credentials
- Never delete unknown directories (might be important)
- Never modify JSON content (might break things)

## Drift Detection Philosophy

**Goal:** Detect when Claude Code updates change the `~/.claude/` structure.

**Why this matters:**

1. Claude Code updates frequently
2. New directories/files may appear
3. Old structures may be deprecated
4. Catching drift early prevents confusion

**Workflow after drift detected:**

1. Investigate new directories/files
2. Verify they are legitimate Claude Code additions
3. Update `known-structure.yaml` in the skill
4. Re-run audit to confirm clean
