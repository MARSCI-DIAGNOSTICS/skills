---
name: install-tool
description: Install or upgrade dotnet tools with alias support (ef, coverage, etc.) and manifest management
argument-hint: "--tool <name|alias> [--global] [--upgrade] [--upgrade-all] [--list]"
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
---

# /dotnet:install-tool

Install, manage, and upgrade .NET tools with alias resolution and tool manifest support.

## Arguments

Parse arguments from `$ARGUMENTS`:

| Flag | Description | Default |
|------|-------------|---------|
| `--tool <name\|alias>` | Tool name or alias (see table below) | Required unless --list or --upgrade-all |
| `--global` | Install globally | false (local by default) |
| `--version <version>` | Specific version | Latest |
| `--upgrade` | Upgrade specific tool to latest | false |
| `--upgrade-all` | Upgrade all tools in manifest (interactive) | false |
| `--list` | List installed tools | false |
| `--create-manifest` | Create tool manifest if missing | Auto |

## Tool Aliases

| Alias | Full Package Name | Description |
|-------|------------------|-------------|
| `coverage` | `dotnet-coverage` | Code coverage collection |
| `reportgen` | `dotnet-reportgenerator-globaltool` | Coverage report generation |
| `ef` | `dotnet-ef` | Entity Framework Core tools |
| `outdated` | `dotnet-outdated-tool` | Check outdated packages |
| `stryker` | `dotnet-stryker` | Mutation testing |
| `csharpier` | `csharpier` | Opinionated C# formatter |
| `husky` | `husky` | Git hooks management |
| `nbgv` | `nbgv` | Nerdbank.GitVersioning CLI |
| `swagger` | `swashbuckle.aspnetcore.cli` | Swagger/OpenAPI generation |
| `httprepl` | `microsoft.dotnet-httprepl` | HTTP REPL for API testing |

**Built-in tools** (no install needed):

- `format` - Code formatting (SDK 6+)
- `user-secrets` - User secrets management
- `watch` - Hot reload
- `dev-certs` - HTTPS development certificates

## Workflow

### Step 1: Resolve Tool Name

If alias provided, resolve to full package name:

```text
coverage -> dotnet-coverage
ef -> dotnet-ef
```

If built-in tool requested:

```text
'format' is a built-in SDK tool. No installation needed.

Usage:
  dotnet format [<PROJECT | SOLUTION>]

Run 'dotnet format --help' for options.
```

### Step 2: Check Current State

**List installed tools:**

```bash
# Global tools
dotnet tool list --global

# Local tools (from manifest)
dotnet tool list
```

**Check for manifest:**

```bash
# Look for .config/dotnet-tools.json
ls .config/dotnet-tools.json 2>/dev/null
```

### Step 3: Handle Manifest

If local install (default) and no manifest exists:

```text
No tool manifest found. Create one?

A tool manifest (.config/dotnet-tools.json) tracks local tools
for this project, making them reproducible across machines.

Options:
- Yes, create manifest (Recommended)
- No, install globally instead
```

Create manifest if approved:

```bash
dotnet new tool-manifest
```

### Step 4: Install Tool

**Local install (default):**

```bash
dotnet tool install <package-name> [--version <version>]
```

**Global install:**

```bash
dotnet tool install --global <package-name> [--version <version>]
```

### Step 5: Provide Usage Hints

After installation, provide relevant usage information:

```text
Tool Installed: dotnet-ef (alias: ef)

Usage:
  dotnet ef migrations add <name>
  dotnet ef database update
  dotnet ef dbcontext scaffold

Common commands:
  dotnet ef migrations add InitialCreate
  dotnet ef database update
  dotnet ef migrations script

Documentation: https://learn.microsoft.com/ef/core/cli/dotnet
```

## Upgrade Mode

### Single Tool Upgrade (`--upgrade`)

```bash
/dotnet:install-tool --tool ef --upgrade
```

Workflow:

1. Check current version
2. Check latest version
3. If newer available, upgrade:

```bash
dotnet tool update <package-name> [--global]
```

### Upgrade All (`--upgrade-all`)

```bash
/dotnet:install-tool --upgrade-all
```

Workflow:

1. Read `.config/dotnet-tools.json`
2. Check each tool for updates
3. Present interactive list:

```text
Tool Updates Available

  Tool                              Current   Latest    Action
  dotnet-ef                         8.0.0     10.0.0    [ ] Upgrade
  dotnet-coverage                   17.8.0    17.12.0   [ ] Upgrade
  dotnet-reportgenerator-globaltool 5.2.0     5.4.0     [ ] Upgrade

Select tools to upgrade:
  1. Upgrade all
  2. Select individually
  3. Skip (no changes)
```

4. Apply selected upgrades
5. Report results

## Output Format

**List Mode:**

```text
Installed .NET Tools

Local Tools (from .config/dotnet-tools.json):
  Package                             Version   Commands
  dotnet-ef                           10.0.0    dotnet-ef
  dotnet-coverage                     17.12.0   dotnet-coverage
  csharpier                           0.29.0    dotnet-csharpier

Global Tools:
  Package                             Version   Commands
  dotnet-outdated-tool                4.6.0     dotnet-outdated
  nbgv                                3.6.0     nbgv

Manifest: .config/dotnet-tools.json
```

**Install Success:**

```text
Tool Installed Successfully

  Package: dotnet-ef
  Alias: ef
  Version: 10.0.0
  Scope: Local (manifest)

Manifest updated: .config/dotnet-tools.json

Quick Start:
  dotnet ef migrations add InitialCreate
  dotnet ef database update

Run 'dotnet ef --help' for all commands.
```

**Upgrade Success:**

```text
Tool Upgrade Complete

  Updated:
    - dotnet-ef: 8.0.0 -> 10.0.0
    - dotnet-coverage: 17.8.0 -> 17.12.0

  Skipped:
    - csharpier: already at latest (0.29.0)

Manifest updated: .config/dotnet-tools.json
```

**Built-in Tool:**

```text
'format' is a built-in SDK tool (no installation required)

The 'dotnet format' command is included with .NET SDK 6.0+.

Usage:
  dotnet format                    # Format entire solution
  dotnet format --verify-no-changes # Check formatting (CI)
  dotnet format whitespace         # Format whitespace only
  dotnet format style              # Format code style only
  dotnet format analyzers          # Apply analyzer fixes

Your SDK: 10.0.100 (format included)
```

## Manifest Structure

`.config/dotnet-tools.json`:

```json
{
  "version": 1,
  "isRoot": true,
  "tools": {
    "dotnet-ef": {
      "version": "10.0.0",
      "commands": ["dotnet-ef"]
    },
    "dotnet-coverage": {
      "version": "17.12.0",
      "commands": ["dotnet-coverage"]
    }
  }
}
```

## Examples

```bash
# Install EF Core tools locally
/dotnet:install-tool --tool ef

# Install coverage tool globally
/dotnet:install-tool --tool coverage --global

# Install specific version
/dotnet:install-tool --tool ef --version 9.0.0

# List all installed tools
/dotnet:install-tool --list

# Upgrade specific tool
/dotnet:install-tool --tool ef --upgrade

# Upgrade all local tools interactively
/dotnet:install-tool --upgrade-all

# Use full package name
/dotnet:install-tool --tool dotnet-reportgenerator-globaltool
```

## Restore Tools

After cloning a repo with a tool manifest:

```bash
dotnet tool restore
```

This installs all tools from `.config/dotnet-tools.json` at their specified versions.
