# Action: file-versions

Browse file edit history stored in `~/.claude/file-history/` to find past versions, view diffs, and understand how files evolved across sessions.

## Arguments

| Argument | Description |
|----------|-------------|
| `<file-path>` | Path to file you want version history for |
| `--list` | List all versions of the file |
| `--diff VERSION` | Show diff between current and specified version |
| `--restore VERSION` | Restore file to specified version |
| `--sessions` | Group versions by session |
| (no args) | Show version summary for current directory |

## File History Structure

Claude Code stores file checkpoints in `~/.claude/file-history/`:

```text
~/.claude/file-history/
+-- {session-uuid-1}/
|   +-- {content-hash-a}@v1
|   +-- {content-hash-b}@v2
|   +-- {content-hash-c}@v3
+-- {session-uuid-2}/
    +-- ...
```

**Note:** File history enables the `/rewind` command. Cleaning this directory removes undo capability.

## Workflow

### Step 1: Find File Versions

```python
from pathlib import Path

claude_dir = Path.home() / ".claude"
file_history = claude_dir / "file-history"

def find_versions(target_path):
    """Find all versions of a file in history."""
    versions = []
    if not file_history.exists():
        return versions

    for session_dir in file_history.iterdir():
        if not session_dir.is_dir():
            continue
        for version_file in session_dir.iterdir():
            try:
                versions.append({
                    "session": session_dir.name,
                    "version": version_file.name,
                    "path": version_file,
                    "mtime": version_file.stat().st_mtime,
                    "size": version_file.stat().st_size
                })
            except Exception:
                continue
    return sorted(versions, key=lambda v: v["mtime"], reverse=True)
```

### Step 2: Display Version List

```python
from datetime import datetime, timezone

def display_versions(versions, target_file):
    """Display version list."""
    print(f"# File Versions: {target_file}\n")
    print(f"Found {len(versions)} version(s)\n")

    current_session = None
    for i, v in enumerate(versions):
        if v["session"] != current_session:
            current_session = v["session"]
            print(f"\n## Session: {current_session[:8]}...")
        mtime = datetime.fromtimestamp(v["mtime"], tz=timezone.utc)
        print(f"  v{i+1}: {mtime.strftime('%Y-%m-%d %H:%M')} ({v['size']} bytes)")
```

### Step 3: Show Diff

```python
import difflib

def show_diff(current_file, version_path):
    """Show diff between current file and historical version."""
    current_content = current_file.read_text().splitlines()
    version_content = version_path.read_text().splitlines()
    diff = difflib.unified_diff(
        version_content, current_content,
        fromfile=f"historical version",
        tofile="current",
        lineterm=""
    )
    for line in diff:
        print(line)
```

### Step 4: Restore Version

```python
import shutil

def restore_version(target_file, version_path):
    """Restore file to historical version."""
    backup_path = target_file.with_suffix(target_file.suffix + ".backup")
    shutil.copy2(target_file, backup_path)
    shutil.copy2(version_path, target_file)
    print(f"Restored {target_file} to version")
    print(f"Backup saved to {backup_path}")
```

## Relationship to /rewind

| Feature | /rewind | file-versions |
|---------|---------|---------------|
| **Purpose** | Undo recent changes | Browse full history |
| **Scope** | Current session | All sessions |
| **Interface** | Interactive | CLI with options |
| **History source** | Same (file-history/) | Same (file-history/) |

Use `/rewind` for quick undo, use this action for history exploration.

## Important Notes

- **Don't clean file-history/** - This removes undo capability
- **History persists across sessions** - You can find old versions
- **Not all files tracked** - Only files edited by Claude Code
- **Binary files excluded** - Only text files have history
