# Action: reset

Reset Claude Code configuration with MCP server preservation. This action helps you perform a clean reinstall while keeping your MCP server configurations intact.

## Arguments

| Argument | Description |
|----------|-------------|
| `--backup` | Create backup of MCP servers and settings (Step 1) |
| `--restore` | Restore MCP servers from backup (Step 3, after relaunch) |
| `--list-backups` | List available backups |
| (no args) | Interactive wizard guiding through full reset workflow |

## Workflow Overview

```text
Step 1: /user-config reset --backup
  -> Extracts MCP servers from ~/.claude.json
  -> Saves to ~/.claude-backups/

Step 2: User Action (Manual)
  -> Delete ~/.claude/ directory
  -> Delete ~/.claude.json
  -> Relaunch Claude Code (creates fresh config)

Step 3: /user-config reset --restore
  -> Injects MCP servers into fresh ~/.claude.json
  -> Optionally restores settings.json
```

## Mode: `--backup`

Create a backup before reset:

```python
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

home = Path.home()
claude_dir = home / ".claude"
claude_json = home / ".claude.json"
backup_root = home / ".claude-backups"

timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
backup_dir = backup_root / f"backup-{timestamp}"
backup_dir.mkdir(parents=True, exist_ok=True)

backed_up = []

# 1. Extract and save MCP servers
if claude_json.exists():
    config = json.load(open(claude_json))
    mcp_servers = config.get("mcpServers", {})
    if mcp_servers:
        mcp_backup = backup_dir / "mcp-servers.json"
        json.dump(mcp_servers, open(mcp_backup, "w"), indent=2)
        backed_up.append(f"MCP servers ({len(mcp_servers)} servers)")

# 2. Copy settings.json
settings_path = claude_dir / "settings.json"
if settings_path.exists():
    shutil.copy2(settings_path, backup_dir / "settings.json")
    backed_up.append("settings.json")
```

**Output:**

```text
Backup created: ~/.claude-backups/backup-2025-12-30-165217/
  - MCP servers (5 servers) -> mcp-servers.json
  - settings.json -> settings.json

Next steps:
1. Delete ~/.claude/ directory
2. Delete ~/.claude.json
3. Relaunch Claude Code
4. Run: /user-config reset --restore
```

## Mode: `--restore`

Restore MCP servers after fresh install:

```python
backup_root = Path.home() / ".claude-backups"
backups = sorted(backup_root.glob("backup-*"), reverse=True)

latest_backup = backups[0]
mcp_backup = latest_backup / "mcp-servers.json"
mcp_servers = json.load(open(mcp_backup))

claude_json = Path.home() / ".claude.json"
if claude_json.exists():
    config = json.load(open(claude_json))
else:
    config = {}

existing_mcp = config.get("mcpServers", {})
config["mcpServers"] = {**existing_mcp, **mcp_servers}

json.dump(config, open(claude_json, "w"), indent=2)
print(f"Restored {len(mcp_servers)} MCP servers")
print("Restart Claude Code to activate MCP servers")
```

## Mode: `--list-backups`

List available backups with contents summary.

## Mode: Interactive (no args)

Guide user through the full reset workflow:

1. **Check current state** - Show what exists
2. **Create backup** - Run `--backup` logic
3. **Show deletion commands** - Provide exact commands for user to run manually
4. **Explain next steps** - Instructions for restore after relaunch

**IMPORTANT:** This action does NOT perform the actual deletion. It prepares the backup and provides instructions. The user must manually delete files to prevent accidental data loss.

## Safety Features

- **No automatic deletion** - User must manually delete files
- **Backup before any changes** - MCP servers preserved
- **Confirmation required** - Use AskUserQuestion before proceeding
- **Clear instructions** - Step-by-step guidance

## What Gets Backed Up

| Item | Backed Up | Rationale |
|------|-----------|-----------|
| MCP servers | Always | Critical - hard to recreate |
| settings.json | Always | User preferences |
| history.jsonl | Optional | Large, less critical |
| credentials | Never | Security - will re-auth |
| sessions | Never | Ephemeral, large |
| debug logs | Never | Ephemeral |
