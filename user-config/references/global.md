# Action: global

View and safely edit the `~/.claude.json` global configuration file. This file contains critical settings including MCP servers, OAuth tokens, and feature flags.

## Arguments

| Argument | Description |
|----------|-------------|
| `--view` | View current configuration (redacted sensitive data) |
| `--edit SECTION` | Edit a specific section interactively |
| `--validate` | Validate JSON syntax and structure |
| (no args) | View configuration summary |

## File Structure

`~/.claude.json` contains these sections:

| Section | Description | Editable |
|---------|-------------|----------|
| `mcpServers` | MCP server configurations | Yes |
| `oauthAccount` | OAuth authentication tokens | No (managed by Claude) |
| `statsigFeatureFlags` | Statsig feature flags | No (managed by Claude) |
| `growthBookFeatureFlags` | GrowthBook feature flags | No (managed by Claude) |

## Safety Rules

**NEVER expose or modify:**

- OAuth tokens or credentials
- Authentication state
- Session identifiers

**SAFE to view/modify:**

- MCP server configurations
- MCP server names and types

## Workflow

### Mode: View (`--view` or no args)

Display configuration with sensitive data redacted:

```python
import json
from pathlib import Path

claude_json = Path.home() / ".claude.json"

if not claude_json.exists():
    print("No global configuration found (~/.claude.json)")
    exit(0)

config = json.load(open(claude_json))

def redact(obj, keys_to_redact):
    if isinstance(obj, dict):
        return {
            k: "[REDACTED]" if k in keys_to_redact else redact(v, keys_to_redact)
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [redact(item, keys_to_redact) for item in obj]
    return obj

sensitive_keys = {"accessToken", "refreshToken", "token", "secret", "password", "key"}
redacted = redact(config, sensitive_keys)
print(json.dumps(redacted, indent=2))
```

### Mode: View Summary (no args)

Show high-level summary:

```python
mcp_servers = config.get("mcpServers", {})
print(f"## MCP Servers ({len(mcp_servers)})")
for name, server_config in mcp_servers.items():
    server_type = server_config.get("type", "unknown")
    print(f"  - {name} ({server_type})")

oauth = config.get("oauthAccount", {})
if oauth:
    email = oauth.get("email", "[not set]")
    print(f"\n## OAuth Account")
    print(f"  - Email: {email}")
    print(f"  - Tokens: [REDACTED]")

statsig = config.get("statsigFeatureFlags", {})
growthbook = config.get("growthBookFeatureFlags", {})
print(f"\n## Feature Flags")
print(f"  - Statsig: {len(statsig)} flags")
print(f"  - GrowthBook: {len(growthbook)} flags")
```

### Mode: Edit Section (`--edit SECTION`)

Edit a specific section interactively:

```python
section = "mcpServers"  # From argument
allowed_sections = ["mcpServers"]
if section not in allowed_sections:
    print(f"Cannot edit section: {section}")
    print(f"Allowed sections: {', '.join(allowed_sections)}")
    exit(1)

current = config.get(section, {})
print(f"Current {section}:")
print(json.dumps(current, indent=2))

# Use AskUserQuestion to confirm edit approach
# Options: Add server, Remove server, Modify server, Cancel
```

### Mode: Validate (`--validate`)

Check JSON syntax and structure:

```python
try:
    config = json.load(open(claude_json))
    issues = []

    if "mcpServers" in config and not isinstance(config["mcpServers"], dict):
        issues.append("mcpServers should be an object")

    for name, server in config.get("mcpServers", {}).items():
        if not isinstance(server, dict):
            issues.append(f"MCP server '{name}' should be an object")
        elif "command" not in server and "type" not in server:
            issues.append(f"MCP server '{name}' missing command or type")

    if issues:
        print("Validation warnings:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("Configuration is valid")

except json.JSONDecodeError as e:
    print(f"Invalid JSON syntax: {e}")
```

## Security Notes

- **Never commit** `~/.claude.json` to version control
- **Backup safely** using `backup` action (extracts mcpServers only)
- **OAuth tokens** are managed by Claude Code - don't modify
- **Feature flags** are synced remotely - local changes are overwritten
