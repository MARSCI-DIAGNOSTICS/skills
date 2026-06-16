# Action: mcp

Manage MCP (Model Context Protocol) server configurations stored in `~/.claude.json`.

## Arguments

| Argument | Description |
|----------|-------------|
| `--list` | List all configured MCP servers with details |
| `--export FILE` | Export MCP configs to JSON file (for sharing) |
| `--import FILE` | Import MCP configs from JSON file |
| `--add NAME` | Add a new MCP server interactively |
| `--remove NAME` | Remove an MCP server (with confirmation) |
| (no args) | Show MCP server summary |

## MCP Server Location

**User-scope MCP servers** are stored in `~/.claude.json` under the `mcpServers` field:

```json
{
  "mcpServers": {
    "perplexity": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic/perplexity-mcp"]
    }
  }
}
```

**Note:** There is NO `~/.mcp.json` file. User-scope MCP servers go in `~/.claude.json`.

## Workflow

### Mode: List (`--list` or no args)

```python
import json
from pathlib import Path

claude_json = Path.home() / ".claude.json"
config = json.load(open(claude_json))
servers = config.get("mcpServers", {})

for name, server in servers.items():
    server_type = server.get("type", "unknown")
    command = server.get("command", "N/A")
    args = server.get("args", [])
    print(f"## {name}")
    print(f"  Type: {server_type}")
    print(f"  Command: {command}")
    if args:
        print(f"  Args: {' '.join(args)}")
    if "env" in server:
        env_keys = list(server["env"].keys())
        print(f"  Env vars: {', '.join(env_keys)}")
```

### Mode: Export (`--export FILE`)

Export MCP configurations to a shareable JSON file, redacting sensitive env vars:

```python
sanitized = {}
for name, server in servers.items():
    server_copy = server.copy()
    if "env" in server_copy:
        sanitized_env = {}
        for key, value in server_copy["env"].items():
            if any(s in key.upper() for s in ["KEY", "TOKEN", "SECRET", "PASSWORD"]):
                sanitized_env[key] = "[REDACTED - set your own value]"
            else:
                sanitized_env[key] = value
        server_copy["env"] = sanitized_env
    sanitized[name] = server_copy

export_data = {
    "exported_at": datetime.now(timezone.utc).isoformat(),
    "note": "Exported MCP server configurations. Review and update any [REDACTED] values.",
    "mcpServers": sanitized
}
json.dump(export_data, open(export_path, "w"), indent=2)
```

### Mode: Import (`--import FILE`)

Import MCP configurations from a JSON file, merging with existing:

```python
import_data = json.load(open(import_path))
new_servers = import_data.get("mcpServers", {})

existing = config.get("mcpServers", {})
for name in new_servers:
    status = "UPDATE" if name in existing else "NEW"
    print(f"  - {name} [{status}]")

# Check for [REDACTED] values and warn
# Use AskUserQuestion for confirmation
config["mcpServers"] = {**existing, **new_servers}
json.dump(config, open(claude_json, "w"), indent=2)
print("Restart Claude Code to activate new servers")
```

### Mode: Add (`--add NAME`)

Add a new MCP server interactively using AskUserQuestion to gather type, command, args, and env vars.

### Mode: Remove (`--remove NAME`)

Remove an MCP server with confirmation via AskUserQuestion.

## Common MCP Servers

| Package | Purpose |
|---------|---------|
| `@anthropic/perplexity-mcp` | AI-powered web search |
| `@anthropic/microsoft-learn-mcp` | Microsoft documentation |
| `@anthropic/firecrawl-mcp` | Web scraping and crawling |
| `@anthropic/context7-mcp` | Library documentation |
| `@anthropic/ref-mcp` | Reference documentation |

## Sharing MCP Configurations

1. Export: `/user-config mcp --export team-mcp.json`
2. Review and update any [REDACTED] API keys
3. Share file with team
4. Team imports: `/user-config mcp --import team-mcp.json`
5. Each team member sets their own API keys
