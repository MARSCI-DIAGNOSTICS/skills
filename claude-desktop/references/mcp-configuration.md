# MCP Configuration for Claude Desktop

## Configuration Methods

### Method 1: CLI Commands (Recommended)

Use Claude Code CLI to manage MCP servers:

```bash
# HTTP transport (recommended for remote)
claude mcp add --transport http <name> <url>

# SSE transport (deprecated, use HTTP)
claude mcp add --transport sse <name> <url>

# Stdio transport (local processes)
claude mcp add --transport stdio <name> -- <command> [args...]
```

### Method 2: JSON Configuration (Manual)

Edit the configuration file directly.

**File Locations:**

| Platform | Path |
| --- | --- |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

**Format:**

```json
{
  "mcpServers": {
    "server-name": {
      "type": "stdio",
      "command": "/path/to/server",
      "args": [],
      "env": {}
    },
    "remote-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp"
    }
  }
}
```

### Method 3: Desktop Extensions (.mcpb)

One-click installation of MCP servers.

**Features:**

- File format: `.mcpb` (MCP Bundle)
- Double-click or drag-and-drop to install
- No terminal required
- No manual configuration
- Bundled Node.js runtime (no dependencies)

**Installing Extensions:**

1. Download `.mcpb` file
2. Drag into Claude Desktop Settings window
3. Click "Install"
4. Restart Claude Desktop if prompted

## MCP Scopes

| Scope | Storage | Use Case |
| --- | --- | --- |
| `local` (default) | `~/.claude.json` under project | Personal, project-specific |
| `project` | `.mcp.json` in project root | Team-shared, version controlled |
| `user` | `~/.claude.json` | Cross-project, personal |

```bash
# Specify scope when adding
claude mcp add --transport http --scope project myserver https://example.com/mcp
```

## Windows-Specific Configuration

**CRITICAL:** Native Windows (not WSL) requires `cmd /c` wrapper for npx:

```bash
# Wrong - will fail with "Connection closed"
claude mcp add --transport stdio my-server -- npx -y @some/package

# Correct - use cmd /c wrapper
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
```

## Import from Claude Desktop

If you've configured MCP servers in Claude Desktop, import them to CLI:

```bash
claude mcp add-from-claude-desktop
# Interactive dialog to select which servers to import
```

**Notes:**

- Works on macOS and WSL
- Imported servers keep their original names
- Duplicate names get numerical suffix (e.g., `server_1`)

## Use Claude Code as MCP Server

Connect Claude Desktop to Claude Code as an MCP server:

```json
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

**Finding the executable path:**

```bash
which claude
# Use full path if claude is not in PATH
```

## Managing Servers

```bash
# List all servers
claude mcp list

# Get server details
claude mcp get <name>

# Remove a server
claude mcp remove <name>

# In-session status
/mcp
```

## Authentication

For OAuth-protected servers:

1. Add the server: `claude mcp add --transport http myserver https://mcp.example.com`
2. Use `/mcp` in Claude Code
3. Select "Authenticate"
4. Complete OAuth flow in browser

## Troubleshooting

| Issue | Solution |
| --- | --- |
| "Connection closed" on Windows | Use `cmd /c` wrapper for npx |
| Server not appearing | Restart Claude Desktop |
| OAuth loop | Clear auth in `/mcp`, retry |
| Extension won't install | Verify `.mcpb` format |

## Related Topics

- [Setup Guide](setup-guide.md) - Basic Desktop configuration
- [Troubleshooting](troubleshooting.md) - Common issues
- For detailed MCP documentation, use the `mcp-integration` skill
