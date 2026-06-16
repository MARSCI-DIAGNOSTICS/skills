# Action: status

Display a comprehensive overview of Claude Code user configuration including health, storage, and quick links to management actions.

## Task

Generate a unified status report covering all user configuration areas.

### Step 1: Detect Platform and Paths

```bash
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
  CLAUDE_DIR="$USERPROFILE/.claude"
  CLAUDE_JSON="$USERPROFILE/.claude.json"
else
  CLAUDE_DIR="$HOME/.claude"
  CLAUDE_JSON="$HOME/.claude.json"
fi
```

### Step 2: Configuration Health Check

Check existence and validity of key configuration files:

| File | Check | Status |
|------|-------|--------|
| `~/.claude/` | Directory exists | Yes/No |
| `~/.claude/settings.json` | Exists + valid JSON | OK/Missing/Invalid |
| `~/.claude.json` | Exists + valid JSON | OK/Missing/Invalid |
| `~/.claude/.credentials.json` | Exists (do NOT read contents) | OK/Missing |
| `~/.claude/history.jsonl` | Exists | OK/Missing |

### Step 3: Storage Summary

Get quick storage metrics:

```bash
du -sh "$CLAUDE_DIR" 2>/dev/null
du -sh "$CLAUDE_DIR/projects" 2>/dev/null
du -sh "$CLAUDE_DIR/debug" 2>/dev/null
du -sh "$CLAUDE_DIR/file-history" 2>/dev/null
du -sh "$CLAUDE_DIR/plugins" 2>/dev/null
```

### Step 4: MCP Server Count

Extract MCP server count from global config (names only, no sensitive data).

### Step 5: Session Statistics (Quick)

Count total session files.

### Step 6: Generate Status Report

```markdown
# Claude Code Configuration Status

## Health Check
| Component | Status |
|-----------|--------|
| ~/.claude/ directory | OK |
| settings.json | Valid JSON |
| .claude.json (global) | Valid JSON |
| credentials | Present |
| history | Present |

## Storage Overview
| Area | Size |
|------|------|
| Total ~/.claude/ | X MB |
| Projects/Sessions | X MB |
| Debug logs | X MB |
| File history | X MB |
| Plugins | X MB |

## MCP Servers (N configured)
- server1
- server2

## Quick Actions
- **Detailed storage:** `/user-config storage`
- **Session stats:** `/user-config session-stats`
- **Cleanup sessions:** `/user-config cleanup-sessions`
- **Full cleanup:** `/user-config prune`
- **Backup config:** `/user-config backup`
- **Reset workflow:** `/user-config reset`
```

## Notes

- **Privacy:** Never display contents of credentials, tokens, or API keys
- **Performance:** Keep checks lightweight (no deep scanning)
- **Cross-platform:** Use Python pathlib for path handling when possible
- **Delegation:** For detailed breakdowns, refer users to specific actions
