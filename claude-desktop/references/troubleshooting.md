# Troubleshooting Claude Desktop

## Common Issues

| Issue | Solution |
| --- | --- |
| "Connection closed" on Windows MCP | Use `cmd /c` wrapper (see below) |
| No worktree created | Initialize Git in directory |
| Extension won't install | Verify `.mcpb` format, check manifest.json |
| OAuth loops | Clear auth in `/mcp`, re-authenticate |
| Local sessions unavailable (ARM64) | Use cloud sessions instead |
| Environment variables not working | Check format, restart Desktop |

## Detailed Solutions

### Worktree Not Created

**Symptom:** New sessions don't get isolated worktrees.

**Cause:** Git is not initialized in the project directory.

**Solution:**

```bash
cd /path/to/your/project
git init
```

**Verification:** Run `git status` - should show repo status, not "not a git repository" error.

### Windows MCP "Connection Closed"

**Symptom:** MCP servers fail with "Connection closed" on Windows.

**Cause:** Windows cannot directly execute `npx` without shell wrapper.

**Solution:** Use `cmd /c` wrapper:

```bash
# Wrong
claude mcp add --transport stdio my-server -- npx -y @some/package

# Correct
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
```

### Desktop Extension Won't Install

**Symptoms:**

- Drag-and-drop does nothing
- Install button doesn't appear
- Error on installation

**Solutions:**

1. Verify file is `.mcpb` format (not `.zip`)
2. Check if extension is compatible with your OS
3. Restart Claude Desktop and retry
4. Check Desktop logs for detailed error

### OAuth Authentication Loops

**Symptom:** Repeatedly asked to authenticate, authentication never completes.

**Solutions:**

1. Use `/mcp` command
2. Select "Clear authentication" for the problematic server
3. Restart Claude Desktop
4. Re-authenticate

### Windows ARM64 Local Sessions

**Symptom:** Cannot start local sessions on Windows ARM64.

**Cause:** Local sessions are not supported on Windows ARM64.

**Solution:** Use cloud sessions instead:

1. Create new session
2. Select "Remote environment"
3. Session runs on Anthropic cloud infrastructure

### .worktreeinclude Not Working

**Symptom:** Files aren't copied to new worktrees despite being in `.worktreeinclude`.

**Checklist:**

- [ ] File is also listed in `.gitignore` (must be in BOTH)
- [ ] Pattern syntax is correct
- [ ] `.worktreeinclude` is in project root
- [ ] File path matches pattern exactly

**Debug:**

```bash
# Check if file is gitignored
git check-ignore -v .env

# Should output something like:
# .gitignore:3:.env    .env
```

### Environment Variables Not Available

**Symptom:** Commands can't find tools like `npm`, `node`, etc.

**Solutions:**

1. Verify tools are in your shell's PATH
2. Restart Claude Desktop (to re-extract PATH)
3. For custom env vars, check format:

```env
# Correct
API_KEY=value

# Wrong
API_KEY = value
API_KEY="value"  # (only quote multiline)
```

## Diagnostic Commands

### In Claude Desktop/Code

```text
/mcp                    # Check MCP server status
/doctor                 # System diagnostics
/config                 # View configuration
```

### In Terminal

```bash
# List all MCP servers
claude mcp list

# Get details on specific server
claude mcp get <server-name>

# Check Claude Code version
claude --version

# Test if tools are in PATH
which npm
which node
```

## Logs Location

| Platform | Location |
| --- | --- |
| macOS | `~/Library/Logs/Claude/` |
| Windows | `%APPDATA%\Claude\logs\` |

## Getting Help

1. Check [official documentation](https://code.claude.com/docs/en/desktop)
2. Search [GitHub issues](https://github.com/anthropics/claude-code/issues)
3. Use `claude-code-issue-researcher` agent for known bugs
4. Contact [Anthropic support](https://support.claude.com)

## Related Topics

- [Setup Guide](setup-guide.md) - Installation
- [Worktrees](worktrees.md) - Parallel sessions
- [MCP Configuration](mcp-configuration.md) - MCP setup
