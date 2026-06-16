# Claude Desktop Setup Guide

## Installation

### Download

**URL:** <https://claude.ai/download>

### System Requirements

| Platform | Version | Notes |
| --- | --- | --- |
| macOS | macOS 11+ | Universal build (Intel + Apple Silicon) |
| Windows x64 | Windows 10+ | Standard 64-bit |
| Windows ARM64 | Windows 10+ | **Local sessions NOT supported** (cloud-only) |

### Post-Installation

1. **First launch** downloads bundled Claude Code version
2. Desktop **automatically manages** version updates
3. Bundled version may differ from CLI (Desktop prioritizes **stability**)

## Environment Configuration

### Automatic PATH Extraction

Desktop automatically extracts `$PATH` from your shell configuration, enabling access to:

- `yarn`, `npm`, `node`
- Development tools available in your terminal
- Custom binaries in your PATH

### Custom Environment Variables

**Steps:**

1. Select **"Local"** environment
2. Click **settings button** (gear icon)
3. Add key-value pairs in `.env` format

**Format:**

```env
API_KEY=your_api_key
DEBUG=true
DATABASE_URL=postgres://localhost:5432/mydb

# Multiline values - wrap in quotes
CERT="-----BEGIN CERT-----
MIIE...
-----END CERT-----"

PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
-----END RSA PRIVATE KEY-----"
```

**Rules:**

- One key-value pair per line
- No spaces around `=`
- Multiline values require double quotes
- Comments start with `#`

## Worktree Location

### Default Location

`~/.claude-worktrees`

### Customizing Location

1. Open Claude Desktop settings
2. Navigate to worktree configuration
3. Set custom path for worktree storage

**Considerations:**

- Choose location with sufficient disk space
- Avoid cloud-synced folders (Dropbox, OneDrive, iCloud)
- Use fast local storage for best performance

## Bundled Version vs CLI

| Aspect | Desktop (Bundled) | CLI |
| --- | --- | --- |
| Update Frequency | Stability-focused | Latest features |
| Management | Automatic | Manual (`npm update`) |
| Version Control | Anthropic-managed | User-managed |

**Note:** The bundled version may lag behind the CLI version. This is intentional - Desktop prioritizes stability over bleeding-edge features.

## Verification

After installation, verify setup:

1. Launch Claude Desktop
2. Create a new local session
3. Verify tools are accessible (try running a terminal command)
4. Check that environment variables are available

## Related Topics

- [Worktrees](worktrees.md) - Parallel session configuration
- [Cloud Sessions](cloud-sessions.md) - Cloud execution setup
- [MCP Configuration](mcp-configuration.md) - MCP server setup
