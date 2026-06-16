---
name: update-mcp-servers
description: "Comprehensive MCP server management. Discovers, updates, and helps set up MCP servers with dependency detection and best practice guidance."
argument-hint: "[--all | --enabled-only | --server NAME] [--dry-run] [--interactive | --non-interactive] [--help]"
allowed-tools: Bash, Read, Glob, AskUserQuestion, Task
---

# Update MCP Servers

Comprehensive one-stop shop for MCP server management. Dynamically discovers all MCP servers, detects installation methods, identifies missing dependencies, offers installation assistance, and updates servers using best practices.

## When to Use

- After a fresh Claude Code installation
- When MCP server tools return connection errors
- Periodically to get latest package versions
- After seeing "package outdated" warnings
- When setting up a new development environment
- To install missing dependencies for MCP servers

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--all` | Update all updateable servers | Default if no args |
| `--enabled-only` | Only update currently connected servers | |
| `--server NAME` | Update specific server(s) | Can be repeated |
| `--dry-run` | Show what would be updated without executing | false |
| `--interactive` | Force interactive selection mode | Auto if <10 servers |
| `--non-interactive` / `--yes` | Skip all prompts, proceed with updates | |
| `--help` | Show comprehensive help and supported methods | |

## Workflow

### Step 1: Session-Aware Discovery

Discover all configured MCP servers by parsing configuration files directly. This avoids the limitation that `claude mcp list` cannot run inside an active Claude Code session.

#### Primary: File-Based Discovery (MANDATORY)

1. **Plugin configs**: Use `Glob` to find `plugins/*/.mcp.json` files
2. **Project config**: Read `.mcp.json` in the project root
3. **User config**: Read `~/.claude/settings.json` (or `$APPDATA/Claude/settings.json` on Windows)

Parse the `mcpServers` key from each file. Each entry has:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "perplexity-mcp"],
      "env": {}
    }
  }
}
```

**For each server, extract:**

- `server_name`: The JSON key
- `command`: The `command` field
- `args`: The `args` array (join for pattern matching)
- `source_file`: Which config file defined it
- `is_http`: `type` is `"url"` or command/args contain an HTTP URL
- `is_plugin_vendored`: `args` contain `${CLAUDE_PLUGIN_ROOT}` (treat as literal pattern, do not expand)

**Merge servers across files**, noting source. If a server appears in multiple files, note all sources.

#### Secondary: CLI Validation (Best-Effort)

Attempt `CLAUDECODE= claude mcp list` to get live connection status:

- If the command succeeds, merge `status` (Connected/Disconnected/Error) into each server entry
- If the command fails (e.g., inside active session), proceed with file-based discovery and set `status` to `unknown`
- Do NOT block on CLI failure -- file-based discovery is sufficient for updates

### Step 2: Detect Installation Methods

For each server, determine the update method based on the command pattern:

#### Package Manager Patterns (Direct Update)

| Pattern | Method | Update Command |
|---------|--------|----------------|
| Contains `npx -y` | npm | `npm install -g <package>` |
| Contains `npm exec` | npm | `npm install -g <package>` |
| Contains `uvx` | uvx | `uv tool upgrade <package>` |
| Contains `pipx run` | pipx | `pipx upgrade <package>` |
| Contains `python -m` or `.py` (not in repo) | python | `pip install --upgrade <package>` |
| Contains `uv run` (not in repo) | python (uv) | `uv pip install --upgrade <package>` |
| Contains `dotnet tool run` | dotnet-tool | `dotnet tool update -g <tool>` |
| Contains `dnx` | dnx (.NET 10) | None (auto-managed) |
| Contains `docker run` | docker | `docker pull <image>` |
| Starts with `https://` or has `(HTTP)` | remote | None (server-managed) |

#### dnx (Auto-Managed .NET Packages)

`dnx` is .NET 10 SDK's equivalent of `npx`. Packages auto-resolve to the latest version on each run -- there is no local install to update.

- **Detection**: Command or args contain `dnx`
- **Classification**: `dnx (auto-managed)` in report
- **Prerequisite**: .NET 10+ SDK must be installed (check via `dotnet --version`, major >= 10)
- **Update action**: None required. If .NET SDK < 10, provide install guidance (see Step 6.5)
- **Report note**: Show `.NET SDK version` and confirm auto-resolution is active

#### Git Clone / Local Repository Patterns (Multi-Step Update)

These patterns require detecting when an MCP server points to a local file path that is inside a git repository.

| Pattern | Method | Update Sequence |
|---------|--------|-----------------|
| `node /path/to/repo/...` (with .git) | git-node | `git pull && npm install && npm run build` |
| `python /path/to/repo/...` (with .git) | git-python | `git pull && pip install -r requirements.txt` |
| `uv run --directory /path/to/repo ...` (with .git) | git-python-uv | `git pull && uv sync` |
| `dotnet run --project /path/to/repo` (with .git) | git-dotnet | `git pull && dotnet build` |
| `dotnet /path/to/repo/bin/...` (with .git) | git-dotnet | `git pull && dotnet build` |

**Git Repository Detection:**

1. Extract the directory path from the command arguments
2. Check if the directory contains a `.git` folder
3. If yes, classify as `git-*` method based on runtime (node/python/dotnet)
4. If no `.git` folder, classify as `unknown` (manual update required)

#### Plugin-Vendored Patterns

Detect `${CLAUDE_PLUGIN_ROOT}` in command or args as plugin-vendored servers. These are managed by their owning plugin, not by this command.

**Detection:**

1. Check if `args` (joined) or `command` contains `${CLAUDE_PLUGIN_ROOT}` as a literal string
2. Extract the plugin name from the source file path (e.g., `plugins/microsoft/.mcp.json` -> `microsoft`)

**For each plugin-vendored server:**

- Check for a `VERSION` file in the vendor root (e.g., `plugins/<plugin>/vendor/<server>/VERSION`)
- Look for a plugin update command (e.g., `/microsoft:mssql update`)
- If `--check` is passed, run the plugin's update command with `--check` to see if upstream has changes

**Classification**: `plugin-vendored` -- delegate to the plugin's own update command.

**Report format**: Show server name, owning plugin, current version/commit, and the update command to run.

#### Dotnet Tool Name Resolution

Binary names used in MCP configs may differ from dotnet tool package names (e.g., `aspire` binary is installed as `aspire.cli` package). Resolve the correct package name before updating.

**Resolution process:**

1. Run `dotnet tool list -g` to get the installed tools table (`Package Id | Version | Commands`)
2. Build a command-to-package lookup map: `aspire` -> `aspire.cli`, etc.
3. When updating a dotnet tool, use the resolved **package name** (not the binary name) for `dotnet tool update -g <package-name>`
4. If resolution fails (binary not found in tool list), warn and fall back to binary name

**Package Name Extraction:**

- For `npx -y package-name@latest` -> extract `package-name` (strip `@latest`)
- For `cmd /c npx -y package` -> extract `package` (ignore Windows wrapper)
- For scoped packages `@org/package@version` -> extract `@org/package`
- For git repos: extract repo name from path for display purposes
- For dotnet tools: use resolved package name from `dotnet tool list -g`

**Group servers by updateable status:**

- `updateable`: Servers with npm, python, uvx, pipx, dotnet-tool, docker, or git methods
- `remote`: HTTP/SSE servers (no local update needed)
- `dnx`: Auto-managed by .NET SDK (no update needed, verify SDK version)
- `plugin-vendored`: Managed by plugin update commands (delegate, not auto-updated here)
- `unknown`: Unrecognized command patterns (report for manual handling)

### Step 2.5: Dependency Detection & Setup Assistance

Before attempting updates, check if required tools are available. If missing, offer installation assistance with best practices.

#### Dependency Check Matrix

| Runtime/Tool | Detection Command | Required For |
|--------------|-------------------|--------------|
| node | `node --version` | npm, npx, git-node |
| npm | `npm --version` | npm packages |
| nvm | `nvm --version` or check `$NVM_DIR` | Best practice for Node |
| python | `python --version` or `python3 --version` | python packages |
| pip | `pip --version` or `pip3 --version` | python packages |
| uv | `uv --version` | uv/uvx packages |
| pipx | `pipx --version` | pipx packages |
| dotnet | `dotnet --version` | dotnet tools |
| dotnet 10+ | `dotnet --version` (major >= 10) | dnx-based servers |
| docker | `docker --version` | docker images |
| git | `git --version` | git-cloned repos |

#### Installation Recommendations (Best Practices)

When a dependency is missing, offer installation options via AskUserQuestion:

**Node.js/npm:**

- Header: "Node.js Setup"
- Question: "Node.js/npm is required but not found. How would you like to install it?"
- Options:
  - "Install via nvm (Recommended)" - Best practice for version management
  - "Install via system package manager" - brew/apt/winget
  - "Skip npm-based servers" - Don't update these servers
  - "Show manual instructions" - Display installation guide

**nvm installation commands:**

```bash
# macOS/Linux
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
source ~/.bashrc  # or ~/.zshrc
nvm install --lts

# Windows - guide to nvm-windows
# https://github.com/coreybutler/nvm-windows
```

**Python:**

- Header: "Python Setup"
- Question: "Python is required but not found. How would you like to install it?"
- Options:
  - "Install via uv (Recommended)" - Fast, modern Python tooling
  - "Install via pyenv" - Best practice for version management
  - "Install via system package manager" - brew/apt/winget
  - "Skip Python-based servers"
  - "Show manual instructions"

**uv installation:**

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**.NET SDK:**

- Header: ".NET Setup"
- Question: ".NET SDK is required but not found. How would you like to install it?"
- Options:
  - "Install latest .NET SDK (Recommended)"
  - "Skip .NET-based servers"
  - "Show manual instructions"

**Docker:**

- Header: "Docker Setup"
- Question: "Docker is required but not found or not running."
- Options:
  - "Show Docker Desktop installation guide"
  - "Skip Docker-based servers"

#### Installation Execution

When user approves installation:

1. **Confirm before execution**: "I'll run the following command to install X. Proceed?"
2. **Execute installation command**
3. **Verify installation**: Re-run detection command
4. **Report result**: "X installed successfully" or "Installation failed: [error]"

#### Platform Detection

Detect platform for appropriate package manager suggestions:

```bash
# Check OS
uname -s  # Linux, Darwin (macOS), MINGW*/MSYS* (Windows Git Bash)
```

| Platform | Package Manager | Notes |
|----------|-----------------|-------|
| macOS | Homebrew (`brew`) | Preferred for system tools |
| Windows | winget / chocolatey | winget is built-in on modern Windows |
| Linux (Debian/Ubuntu) | apt | `sudo apt install` |
| Linux (Fedora/RHEL) | dnf | `sudo dnf install` |

### Step 3: Parse Arguments

Parse the command arguments to determine the operation mode:

**Mode selection (mutually exclusive):**

- `--all` (default): Update all updateable servers
- `--enabled-only`: Only update servers with "Connected" status
- `--server NAME`: Update only the specified server(s)
- `--help`: Show comprehensive help

**Options:**

- `--dry-run`: Display what would be updated without executing
- `--interactive`: Force interactive selection via AskUserQuestion
- `--non-interactive` or `--yes`: Skip all prompts

**Auto-interactive logic:**

If neither `--interactive` nor `--non-interactive` is specified:

- If updateable server count < 10: Enable interactive mode
- Otherwise: Proceed with non-interactive mode

### Step 4: Interactive Selection (if applicable)

When interactive mode is enabled, use AskUserQuestion to let the user select which servers to update.

#### Question 1: Update scope

- Header: "Update scope"
- Question: "Which MCP servers would you like to update?"
- Options:
  - "Update all (N servers)" - Update all updateable servers
  - "Update npm packages only" - If mixed methods exist
  - "Update git repositories only" - If git repos exist
  - "Select specific servers" - Choose individual servers
  - "Cancel" - Exit without updating

**Question 2 (if "Select specific servers"):**

- Header: "Server selection"
- Question: "Select the servers to update:"
- Options: List each updateable server with package/repo info
- multiSelect: true

### Step 4.5: Capture Pre-Update Versions

Before executing updates, snapshot current versions for before/after comparison in the report.

**NPM global packages:**

```bash
npm ls -g --depth=0 2>/dev/null
```

Parse `package@version` pairs. For npx-only packages (not globally installed), record as `(npx on-demand)`.

**Dotnet global tools:**

```bash
dotnet tool list -g 2>/dev/null
```

Parse the `Package Id | Version | Commands` table columns.

**Docker images:**

```bash
docker images --format "{{.Repository}}:{{.Tag}}" 2>/dev/null
```

**Git repositories:**

```bash
git -C /path/to/repo rev-parse --short HEAD 2>/dev/null
```

Capture the short commit hash for each git-cloned server.

**Plugin-vendored servers:**

```bash
cat plugins/<plugin>/vendor/<server>/VERSION 2>/dev/null
```

If no VERSION file, use git commit hash of the vendor directory.

**Python (uvx/pipx):**

```bash
uv tool list 2>/dev/null
pipx list --short 2>/dev/null
```

Store all versions in a lookup map keyed by server/package name for use in Step 6.

### Step 5: Execute Updates

#### Package Manager Updates (Batch)

Group packages by installation method and execute updates efficiently:

**NPM packages:**

```bash
npm install -g package1 package2 package3
```

**Python packages (pip):**

```bash
pip install --upgrade package1 package2
```

**Python packages (uvx):**

```bash
uv tool upgrade package1
uv tool upgrade package2
```

**pipx packages:**

```bash
pipx upgrade package1
pipx upgrade package2
```

**.NET tools (use resolved package names):**

Use the package names resolved in Step 2 (Dotnet Tool Name Resolution), NOT the binary names from the MCP config.

```bash
# Example: binary "aspire" resolves to package "aspire.cli"
dotnet tool update -g aspire.cli
dotnet tool update -g tool2-package-name
```

If package name resolution was not possible (tool not in `dotnet tool list -g`), warn and attempt with the binary name as fallback.

**Docker images:**

```bash
docker pull image1:latest
docker pull image2:latest
```

#### Git Repository Updates (Sequential, Multi-Step)

For git-cloned MCP servers, execute update sequence per repository:

**git-node:**

```bash
cd /path/to/repo
git status --porcelain  # Check for uncommitted changes
git pull origin $(git rev-parse --abbrev-ref HEAD)
npm install
npm run build  # if build script exists in package.json
```

**git-python:**

```bash
cd /path/to/repo
git status --porcelain
git pull origin $(git rev-parse --abbrev-ref HEAD)
pip install -r requirements.txt  # if exists
# or: pip install -e .  # if setup.py/pyproject.toml exists
```

**git-python-uv:**

```bash
cd /path/to/repo
git status --porcelain
git pull origin $(git rev-parse --abbrev-ref HEAD)
uv sync
```

**git-dotnet:**

```bash
cd /path/to/repo
git status --porcelain
git pull origin $(git rev-parse --abbrev-ref HEAD)
dotnet build
```

**Safety Checks for Git Updates:**

- Verify clean working directory before pull (no uncommitted changes)
- If dirty, offer to stash changes or skip
- Check for merge conflicts after pull
- Report if update requires manual intervention

#### Post-Update Version Capture

After all updates complete, re-run the same version detection commands from Step 4.5 to capture updated versions. Store in a separate lookup map for comparison in the report.

### Step 6: Report Results

After execution, display a summary of the update results with before/after version tracking:

```markdown
# MCP Server Update Results

## Summary
- **Discovered:** 14 MCP servers
- **Remote (no update needed):** 3 servers
- **Package managers updated:** 4 servers
- **Git repositories updated:** 2 servers
- **Plugin-vendored (delegated):** 2 servers
- **dnx (auto-managed):** 1 server
- **Unknown (manual):** 1 server
- **Failed:** 0 servers

## NPM Packages
| Package | Previous | Updated | Status |
|---------|----------|---------|--------|
| perplexity-mcp | 0.2.2 | 0.2.3 | Updated |
| firecrawl-mcp | 1.8.0 | 1.8.0 | Already latest |
| chrome-devtools-mcp | (npx on-demand) | (npx on-demand) | On-demand |
| @playwright/mcp | 0.1.5 | 0.1.6 | Updated |

## Dotnet Tools
| Package (resolved) | Previous | Updated | Status |
|---------------------|----------|---------|--------|
| aspire.cli (binary: aspire) | 9.1.0 | 9.2.0 | Updated |

## Git Repositories
| Repository | Method | Previous | Updated | Status |
|------------|--------|----------|---------|--------|
| mssql-mcp-server | git-node | a1b2c3d | f4e5d6a | Pulled + Rebuilt |
| custom-tools | git-python | 7g8h9i0 | 7g8h9i0 | Already latest |

## Plugin-Vendored Servers
| Server | Plugin | Current Version | Update Command |
|--------|--------|-----------------|----------------|
| mssql-node | microsoft | v1.2.0 | `/microsoft:mssql update` |
| mssql-dotnet | microsoft | v1.2.0 | `/microsoft:mssql update` |

## dnx Servers (Auto-Managed)
| Server | Package | .NET SDK | Status |
|--------|---------|----------|--------|
| nuget | nuget-mcp | 10.0.100 | Auto-resolves latest on each run |

## Remote Servers (no action needed)
| Server | URL |
|--------|-----|
| context7 | https://mcp.context7.com/mcp |
| microsoft-learn | https://... |
| Ref | https://... |

## Unknown / Manual Update Required
| Server | Command | Reason |
|--------|---------|--------|
| custom-local | /path/to/binary | Not a git repo, unknown package manager |

## Next Steps
- Restart Claude Code to use updated servers
- Run `/mcp` to verify server connections
- For plugin-vendored servers, run their update commands separately
```

### Step 6.5: Manual Step Instructions

When automation cannot complete an update, provide actionable manual instructions. Each template follows the format: problem statement, WHY explanation, numbered steps with copy-paste commands.

#### Tool Locked by Current Session

```text
Cannot update <tool> while Claude Code is running.

WHY: The <tool> binary is currently in use by this Claude Code session.
Updating it while locked may fail or corrupt the installation.

MANUAL STEPS:
1. Close this Claude Code session:
   Press Ctrl+C or type /exit

2. Run the update command in your terminal:
   <update-command>

3. Restart Claude Code:
   claude

4. Verify the update:
   /update-mcp-servers --dry-run
```

#### npm Permission Denied

```text
npm install -g failed with EACCES (permission denied).

WHY: Global npm packages are installed in a system directory that
requires elevated permissions, or npm prefix is misconfigured.

MANUAL STEPS (Option A - Fix npm prefix, recommended):
1. Set npm prefix to user directory:
   npm config set prefix ~/.npm-global

2. Add to your shell profile (~/.bashrc or ~/.zshrc):
   export PATH="$HOME/.npm-global/bin:$PATH"

3. Reload shell and retry:
   source ~/.bashrc
   npm install -g <package>

MANUAL STEPS (Option B - Use sudo):
1. Run with elevated permissions:
   sudo npm install -g <package>
```

#### Git Merge Conflicts

```text
git pull failed with merge conflicts in <repo>.

WHY: Local changes conflict with upstream changes. Automatic merge
cannot resolve these differences.

MANUAL STEPS:
1. Navigate to the repository:
   cd <repo-path>

2. Check conflict status:
   git status

3. Resolve conflicts in each file (edit and remove conflict markers)

4. Mark resolved and complete merge:
   git add .
   git commit -m "Resolve merge conflicts"

5. Rebuild the project:
   <build-command>

6. Verify server works:
   /update-mcp-servers --server <name> --dry-run
```

#### Missing .NET 10 SDK for dnx

```text
dnx-based server requires .NET 10+ SDK but found version <version> (or none).

WHY: dnx is a .NET 10 SDK feature (equivalent of npx). Packages
auto-resolve to latest on each run, but the SDK must be version 10+.

MANUAL STEPS:

Windows:
  winget install Microsoft.DotNet.SDK.10

macOS:
  brew install dotnet@10

Linux (Ubuntu/Debian):
  sudo apt-get update
  sudo apt-get install -y dotnet-sdk-10.0

Linux (Fedora):
  sudo dnf install dotnet-sdk-10.0

Verify installation:
  dotnet --version
  # Should show 10.x.xxx or higher
```

## Intelligent Guidance System

This command acts as an intelligent assistant that can handle any situation:

### Scenario Handling

| Scenario | Behavior |
|----------|----------|
| **All deps present** | Proceed with updates normally |
| **Some deps missing** | Offer installation for missing, skip unavailable servers if declined |
| **No MCP servers** | Guide user on how to add MCP servers with `claude mcp add` |
| **All servers remote** | Explain no local updates needed, offer to verify connectivity |
| **Git repo dirty** | Offer to stash changes, or skip with explanation |
| **Network unavailable** | Detect and report, suggest retry later |
| **Partial failure** | Continue with remaining, summarize what succeeded/failed |

### Proactive Recommendations

When analyzing servers, proactively suggest improvements:

```text
Recommendations:
- Consider using nvm to manage Node.js versions (you're using system Node)
- Server 'custom-mcp' uses deprecated SSE transport - consider migrating to HTTP
- 3 npm packages could use @latest for auto-updates in config
```

### Help Mode

If user runs with `--help`, display comprehensive help:

```text
MCP Server Update Command - Comprehensive Management Tool

DISCOVERY:
  Automatically finds all MCP servers from:
  - .mcp.json files (project + plugins)
  - User settings.json
  - claude mcp list (best-effort for live status)

SUPPORTED UPDATE METHODS:
  npm/npx packages
  Python (pip, uv, uvx, pipx)
  .NET tools (with package name resolution)
  Docker images
  Git-cloned repositories (Node, Python, .NET)
  dnx packages (auto-managed, .NET 10+ SDK)
  Plugin-vendored servers (delegated to plugin commands)
  Remote HTTP/SSE (no update needed)

DEPENDENCY MANAGEMENT:
  Missing tools? We'll help you install them with best practices:
  - Node.js via nvm (recommended)
  - Python via uv or pyenv
  - .NET SDK via official installer
  - Docker Desktop

COMMON USAGE:
  /update-mcp-servers              # Interactive update of all servers
  /update-mcp-servers --dry-run    # Preview what would be updated
  /update-mcp-servers --server X   # Update specific server
  /update-mcp-servers --all --yes  # Update all, no prompts

For more details, see: https://code.claude.com/docs/en/mcp
```

### Troubleshooting Assistance

When errors occur, provide actionable troubleshooting:

```text
npm install failed for 'perplexity-mcp'

Possible causes:
1. Network connectivity issue
2. npm registry temporarily unavailable
3. Package name changed or deprecated

Suggested actions:
- Retry: /update-mcp-servers --server perplexity
- Check npm status: https://status.npmjs.org/
- Verify package: npm view perplexity-mcp
- Search for alternatives: Would you like me to search for similar MCP servers?
```

## Transport Types

| Type | Description | Update Required |
|------|-------------|-----------------|
| **stdio** | Local process (npm, python, docker, git) | Yes - update package/image/repo |
| **http** | Remote HTTP server | No - server-managed |
| **sse** | Server-Sent Events (deprecated) | No - server-managed |

## Error Handling

| Error | Handling |
|-------|----------|
| `claude mcp list` fails | Proceed with file-based discovery; set status to `unknown` |
| No updateable servers | Report "All servers are remote HTTP - no local updates needed" |
| npm install fails | Report failure, continue with remaining packages |
| pip install fails | Report failure, suggest venv activation if needed |
| dotnet tool update fails | Report failure, show resolved package name, suggest SDK version check |
| git pull fails | Report failure (dirty working directory, network, etc.) |
| git repo has conflicts | Skip update, report "Manual merge required" (see Step 6.5) |
| Unknown method | Report "Cannot auto-update: unknown method" with guidance |
| Permission denied | Suggest `sudo` or npm prefix configuration (see Step 6.5) |
| Missing dependency | Offer to install with best practices (see Step 2.5) |
| Tool locked by session | Provide manual steps to close session, update, restart (see Step 6.5) |
| dnx requires .NET 10+ SDK | Show SDK version found, provide install commands (see Step 6.5) |
| Plugin-vendored server | Delegate to plugin update command, do not attempt direct update |

## Examples

### Example 1: Update All Servers (Default)

```text
User: /claude-ecosystem:update-mcp-servers

# Discovery output:
Found 10 MCP servers:
- 4 updateable (npm)
- 2 updateable (git-node)
- 3 remote (no update needed)
- 1 unknown (manual)

# Interactive prompt (auto-enabled, <10 updateable):
Which MCP servers would you like to update?
> Update all (6 servers)

# Execution:
npm install -g chrome-devtools-mcp firecrawl-mcp perplexity-mcp @playwright/mcp
Updating git repo: mssql-mcp-server...
Updating git repo: custom-tools...

# Results:
Updated 6 servers successfully.
```

### Example 2: Dry Run

```text
User: /claude-ecosystem:update-mcp-servers --dry-run

# Shows what would be updated without executing:
Would update 4 npm packages:
  npm install -g chrome-devtools-mcp firecrawl-mcp perplexity-mcp @playwright/mcp

Would update 2 git repositories:
  mssql-mcp-server (git-node): git pull && npm install && npm run build
  custom-tools (git-python): git pull && pip install -r requirements.txt

Remote servers (no update needed): context7, microsoft-learn, Ref
Unknown (manual): custom-local
```

### Example 3: Missing Dependency

```text
User: /claude-ecosystem:update-mcp-servers

# Dependency check:
Node.js/npm is required but not found.

# AskUserQuestion:
How would you like to install Node.js?
> Install via nvm (Recommended)

# Installation:
Installing nvm...
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
nvm install --lts
Node.js v22.x installed successfully

# Continue with updates...
```

### Example 4: Git Repository with Uncommitted Changes

```text
User: /claude-ecosystem:update-mcp-servers --server mssql

# Git status check:
Repository 'mssql-mcp-server' has uncommitted changes.

# AskUserQuestion:
How would you like to handle this?
> Stash changes and continue

# Execution:
git stash
git pull origin main
npm install
npm run build
git stash pop
Updated mssql-mcp-server
```

### Example 5: Non-Interactive Mode

```text
User: /claude-ecosystem:update-mcp-servers --all --non-interactive

# Skips prompts, updates all immediately:
Checking dependencies...
All required dependencies available

Updating 6 servers...
npm install -g chrome-devtools-mcp firecrawl-mcp perplexity-mcp @playwright/mcp
Updating mssql-mcp-server...
Updating custom-tools...

Done. Updated 6 servers.
```

### Example 6: Plugin-Vendored and dnx Servers

```text
User: /claude-ecosystem:update-mcp-servers --dry-run

# Discovery:
Found 14 MCP servers from 5 config files

# Classification:
- 4 npm packages (updateable)
- 1 dotnet tool: aspire.cli (resolved from binary "aspire")
- 1 dnx server: nuget-mcp (auto-managed, .NET SDK 10.0.100)
- 2 plugin-vendored: mssql-node, mssql-dotnet (plugin: microsoft)
- 3 remote (no update needed)
- 2 git repositories
- 1 unknown

# Plugin-vendored note:
mssql-node and mssql-dotnet are managed by the microsoft plugin.
Run `/microsoft:mssql update` to update these servers.

# dnx note:
nuget-mcp uses dnx (auto-resolves latest on each run).
.NET SDK 10.0.100 detected -- no update action needed.
```

## Related Commands

- `/audit-mcp` - Audit MCP server configurations
- `/user-config:mcp` - Manage MCP server configurations
- `/mcp` - Check MCP server status (built-in)

## Related Skill

Invoke `mcp-integration` skill for MCP transport type guidance and validation patterns.
