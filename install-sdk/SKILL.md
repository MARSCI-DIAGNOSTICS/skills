---
name: install-sdk
description: Install .NET SDK with cross-platform support and optional interactive global.json configuration
argument-hint: "[--version <ver>] [--update-global-json] [--interactive] [--list]"
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion, mcp__perplexity__search
---

# /dotnet:install-sdk

Install .NET SDK versions with cross-platform package manager support and interactive global.json configuration.

## Arguments

Parse arguments from `$ARGUMENTS`:

| Flag | Description | Default |
|------|-------------|---------|
| `--version <version>` | SDK version to install (e.g., 10.0, 10.0.100) | Latest stable |
| `--update-global-json` | Also update/create global.json | false |
| `--interactive` | Interactive mode for global.json configuration | false |
| `--list` | List installed SDKs | false |
| `--channel <channel>` | Release channel (LTS, STS, Preview) | STS |

## Workflow

### Step 1: Detect Environment

Determine current state:

```bash
# Check installed SDKs
dotnet --list-sdks

# Check current global.json if exists
cat global.json 2>/dev/null || echo "No global.json"
```

Detect OS:

- Windows: Check for `winget` availability
- macOS: Check for `brew` availability
- Linux: Check for `apt`, `dnf`, or `pacman`

### Step 2: Determine Target Version

If `--version` specified:

- Parse version (accept "10", "10.0", or "10.0.100")
- Normalize to full SDK version

If `--version` not specified:

- Query latest stable version:

```text
Use mcp__perplexity__search:
  query: ".NET SDK latest stable version January 2026"
```

### Step 3: Check If Already Installed

```bash
dotnet --list-sdks | grep "^<version>"
```

If already installed:

```text
.NET SDK <version> is already installed.

Installed location: <path>
Current global.json: <version or none>

Would you like to:
- Update global.json to use this version
- Install a different version
- Exit
```

### Step 4: Install SDK

**Windows (winget):**

```bash
winget install Microsoft.DotNet.SDK.<major> --version <version>
```

**Windows (manual/chocolatey fallback):**

```bash
# If winget not available
choco install dotnet-sdk --version=<version>
```

**macOS (Homebrew):**

```bash
# For latest
brew install --cask dotnet-sdk

# For specific version (if available)
brew install --cask dotnet-sdk@<major>
```

**Linux (apt - Ubuntu/Debian):**

```bash
# Add Microsoft package repository if needed
wget https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb

# Install SDK
sudo apt-get update
sudo apt-get install -y dotnet-sdk-<major>.0
```

**Linux (dnf - Fedora/RHEL):**

```bash
sudo dnf install dotnet-sdk-<major>.0
```

### Step 5: Verify Installation

```bash
dotnet --list-sdks
dotnet --version
```

Confirm the installed version appears in the list.

### Step 6: Global.json Configuration

If `--update-global-json` or `--interactive`:

**Interactive Mode (`--interactive`):**

Present SDK selection:

```text
Configure global.json for this project

Installed SDKs:
  1. 10.0.100 (just installed)
  2. 9.0.200
  3. 8.0.400

Which SDK version should this project use?
```

Then present rollForward policy:

```text
Select rollForward policy:

  1. latestPatch (Recommended) - Use latest patch version
  2. latestMinor - Use latest minor version
  3. latestMajor - Use latest major version
  4. latestFeature - Use latest feature band
  5. disable - Use exact version only
```

Then present allowPrerelease:

```text
Allow prerelease SDK versions?

  1. No (Recommended for production)
  2. Yes (For testing preview features)
```

**Non-Interactive Mode:**

Create/update global.json with sensible defaults:

```json
{
  "sdk": {
    "version": "<installed-version>",
    "rollForward": "latestPatch"
  }
}
```

### Step 7: Write Global.json

If global.json exists, preserve other settings:

```json
{
  "sdk": {
    "version": "10.0.100",
    "rollForward": "latestPatch",
    "allowPrerelease": false
  },
  // Preserve existing msbuild-sdks, tools, etc.
}
```

## Output Format

**List Mode:**

```text
Installed .NET SDKs:

  Version     Location                              Status
  10.0.100    C:\Program Files\dotnet\sdk\10.0.100  Active (global.json)
  9.0.200     C:\Program Files\dotnet\sdk\9.0.200   Installed
  8.0.400     C:\Program Files\dotnet\sdk\8.0.400   Installed

Current global.json:
  Version: 10.0.100
  RollForward: latestPatch
  Path: D:\repos\myproject\global.json
```

**Install Success:**

```text
.NET SDK Installation Complete

  Installed: .NET SDK 10.0.100
  Location: C:\Program Files\dotnet\sdk\10.0.100
  Method: winget

Verification:
  dotnet --version: 10.0.100

Global.json: Updated to use 10.0.100 with latestPatch rollForward
```

**Install with Global.json Interactive:**

```text
.NET SDK Installation Complete

  Installed: .NET SDK 10.0.100

Global.json Configuration:
  {
    "sdk": {
      "version": "10.0.100",
      "rollForward": "latestMinor",
      "allowPrerelease": false
    }
  }

Written to: D:\repos\myproject\global.json
```

## RollForward Policy Reference

| Policy | Behavior |
|--------|----------|
| `patch` | Exact patch version only |
| `feature` | Latest patch, same feature band |
| `minor` | Latest patch, same minor version |
| `major` | Latest patch, same major version |
| `latestPatch` | Latest patch of specified feature band |
| `latestFeature` | Latest feature band of specified minor |
| `latestMinor` | Latest minor of specified major |
| `latestMajor` | Latest available SDK |
| `disable` | Exact version only, no roll-forward |

## Examples

```bash
# List installed SDKs
/dotnet:install-sdk --list

# Install latest stable SDK
/dotnet:install-sdk

# Install specific version
/dotnet:install-sdk --version 10.0.100

# Install and update global.json
/dotnet:install-sdk --version 10.0 --update-global-json

# Interactive global.json configuration
/dotnet:install-sdk --interactive

# Install preview SDK
/dotnet:install-sdk --channel Preview
```

## Troubleshooting

**winget not found (Windows):**

```text
winget is not available. Options:
1. Install App Installer from Microsoft Store
2. Use chocolatey: choco install dotnet-sdk
3. Download manually from https://dotnet.microsoft.com/download
```

**Permission denied (Linux):**

```text
Installation requires sudo. Run:
  sudo apt-get install dotnet-sdk-10.0

Or use the install script (user-local):
  curl -sSL https://dot.net/v1/dotnet-install.sh | bash /dev/stdin --version 10.0.100
```
