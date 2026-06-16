# Action: restore

Restore Claude Code user configuration from a backup created by the `backup` action.

## Arguments

| Argument | Description |
|----------|-------------|
| `backup-name` | Name of backup directory (e.g., `backup-2025-12-30-153045`) |
| `--list` | List available backups without restoring |
| `--mcp-only` | Only restore MCP server configurations |
| `--dry-run` | Show what would be restored without making changes |
| (no args) | Interactive selection from available backups |

## Workflow

### Mode: `--list`

List all available backups with details:

```python
import json
from pathlib import Path

backup_root = Path.home() / ".claude-backups"
backups = sorted(backup_root.glob("backup-*"), reverse=True)

for backup in backups:
    manifest_path = backup / "manifest.json"
    if manifest_path.exists():
        manifest = json.load(open(manifest_path))
        created = manifest.get("created_at", "Unknown")
        backup_type = manifest.get("backup_type", "unknown")
        file_count = len(manifest.get("files", []))
        print(f"  {backup.name}")
        print(f"    Created: {created}")
        print(f"    Type: {backup_type}")
        print(f"    Files: {file_count}")
```

### Mode: Interactive (no args)

1. List available backups
2. Use AskUserQuestion to let user select
3. Proceed with restore

### Mode: Restore Specific Backup

#### Step 1: Restore MCP Servers

```python
mcp_backup = backup_dir / "mcp-servers.json"
if mcp_backup.exists():
    mcp_servers = json.load(open(mcp_backup))
    if claude_json.exists():
        config = json.load(open(claude_json))
    else:
        config = {}
    existing_mcp = config.get("mcpServers", {})
    config["mcpServers"] = {**existing_mcp, **mcp_servers}
    json.dump(config, open(claude_json, "w"), indent=2)
    print(f"Restored {len(mcp_servers)} MCP servers")
```

#### Step 2: Restore Settings (if not `--mcp-only`)

```python
restore_mappings = [
    ("settings.json", claude_dir / "settings.json"),
    ("settings.local.json", claude_dir / "settings.local.json"),
    ("CLAUDE.md", claude_dir / "CLAUDE.md"),
    ("CLAUDE-home.md", home / "CLAUDE.md"),
    ("claudeignore", home / ".claudeignore"),
]

for backup_file, dest in restore_mappings:
    source = backup_dir / backup_file
    if source.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
```

#### Step 3: Restore History (if present)

Copy `history.jsonl` from backup if it exists.

## Safety Features

- **Non-destructive merge:** MCP servers are merged, not replaced
- **Existing config preserved:** Only missing/backed-up items restored
- **Dry-run mode:** Preview changes before applying
- **Manifest validation:** Only restores from valid backups
- **No credential restore:** .credentials.json is never restored

## Conflict Resolution

| Item | Behavior |
|------|----------|
| MCP servers | Merged (backup overrides existing with same name) |
| settings.json | Replaced entirely |
| CLAUDE.md | Replaced entirely |

**Note:** If you want to preserve existing settings, use `--mcp-only` to only restore MCP servers.
