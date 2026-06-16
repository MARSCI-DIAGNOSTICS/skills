# Action: backup

Create a comprehensive backup of Claude Code user configuration files to `~/.claude-backups/`.

## Arguments

| Argument | Description |
|----------|-------------|
| `--include-history` | Include history.jsonl in backup (can be large) |
| `--include-sessions` | Include session files for current project (very large) |
| (no args) | Backup essential config only (MCP servers, settings) |

## What Gets Backed Up

### Always Included (Essential Config)

| File | Description | Priority |
|------|-------------|----------|
| `~/.claude.json` (mcpServers section) | MCP server configurations | CRITICAL |
| `~/.claude/settings.json` | User settings and preferences | HIGH |
| `~/.claude/settings.local.json` | Machine-local settings | MEDIUM |
| `~/.claude/CLAUDE.md` | User-level instructions | HIGH |
| `~/CLAUDE.md` | Alternative user instructions | HIGH |
| `~/.claudeignore` | User ignore patterns | MEDIUM |

### Optional (`--include-history`)

| File | Description |
|------|-------------|
| `~/.claude/history.jsonl` | Command and prompt history |

### Optional (`--include-sessions`)

| Directory | Description |
|-----------|-------------|
| `~/.claude/projects/{current-project}/` | Session files for current project |

### Never Backed Up

| File | Reason |
|------|--------|
| `~/.claude/.credentials.json` | Contains sensitive OAuth tokens |
| `~/.claude/plugins/` | Use `/plugin install` to restore |
| `~/.claude/file-history/` | Large, auto-regenerated |

## Backup Location

All backups stored in `~/.claude-backups/`:

```text
~/.claude-backups/
+-- backup-2025-12-30-153045/
|   +-- manifest.json         # Backup metadata
|   +-- mcp-servers.json      # Extracted MCP servers
|   +-- settings.json         # User settings
|   +-- settings.local.json   # Local settings (if exists)
|   +-- CLAUDE.md             # User instructions (if exists)
|   +-- claudeignore          # Ignore patterns (if exists)
+-- backup-2025-12-29-100000/
    +-- ...
```

## Workflow

### Step 1: Create Backup Directory

```python
import json
from datetime import datetime, timezone
from pathlib import Path
import shutil

home = Path.home()
claude_dir = home / ".claude"
backup_root = home / ".claude-backups"

timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
backup_dir = backup_root / f"backup-{timestamp}"
backup_dir.mkdir(parents=True, exist_ok=True)

manifest = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "claude_code_version": "unknown",
    "backup_type": "essential",
    "files": []
}
```

### Step 2: Backup MCP Servers (Critical)

```python
claude_json = home / ".claude.json"
if claude_json.exists():
    config = json.load(open(claude_json))
    mcp_servers = config.get("mcpServers", {})
    if mcp_servers:
        mcp_backup = backup_dir / "mcp-servers.json"
        json.dump(mcp_servers, open(mcp_backup, "w"), indent=2)
        manifest["files"].append({
            "name": "mcp-servers.json",
            "source": str(claude_json),
            "type": "extracted",
            "count": len(mcp_servers)
        })
```

### Step 3: Backup Settings and Config Files

```python
backup_files = [
    (claude_dir / "settings.json", "settings.json"),
    (claude_dir / "settings.local.json", "settings.local.json"),
    (claude_dir / "CLAUDE.md", "CLAUDE.md"),
    (home / "CLAUDE.md", "CLAUDE-home.md"),
    (home / ".claudeignore", "claudeignore"),
]

for source, dest in backup_files:
    if source.exists():
        shutil.copy2(source, backup_dir / dest)
        manifest["files"].append({
            "name": dest,
            "source": str(source),
            "type": "copy",
            "size": source.stat().st_size
        })
```

### Step 4: Optional - History

If `--include-history` is specified:

```python
history_path = claude_dir / "history.jsonl"
if history_path.exists():
    shutil.copy2(history_path, backup_dir / "history.jsonl")
    manifest["files"].append({
        "name": "history.jsonl",
        "source": str(history_path),
        "type": "copy",
        "size": history_path.stat().st_size
    })
    manifest["backup_type"] = "with-history"
```

### Step 5: Save Manifest

```python
manifest_path = backup_dir / "manifest.json"
json.dump(manifest, open(manifest_path, "w"), indent=2)
```

## Output Format

```markdown
# Backup Created Successfully

**Location:** ~/.claude-backups/backup-2025-12-30-153045/
**Type:** Essential config

## Files Backed Up

| File | Size | Source |
|------|------|--------|
| mcp-servers.json | 2.4 KB | Extracted from ~/.claude.json (5 servers) |
| settings.json | 1.1 KB | ~/.claude/settings.json |
| CLAUDE.md | 3.2 KB | ~/.claude/CLAUDE.md |

**Total:** 3 files, 6.7 KB

## Restore Command

To restore this backup: `/user-config restore backup-2025-12-30-153045`
```

## Backup Retention

Backups are NOT automatically cleaned up. User should periodically review and delete old backups:

```bash
ls -la ~/.claude-backups/
rm -rf ~/.claude-backups/backup-2025-12-01-100000/
```
