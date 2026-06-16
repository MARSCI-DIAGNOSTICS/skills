---
name: upgrade-nuget-packages
description: Interactive NuGet package upgrade with vulnerability detection and breaking change warnings
argument-hint: "[--vulnerable] [--major] [--dry-run] [--auto] [--project <name>]"
allowed-tools: Bash, Read, Edit, Glob, Grep, AskUserQuestion, mcp__perplexity__search
---

# /dotnet:upgrade-nuget-packages

Interactive NuGet package upgrade command with intelligence about vulnerabilities, breaking changes, and compatibility.

## Arguments

Parse arguments from `$ARGUMENTS`:

| Flag | Description | Default |
|------|-------------|---------|
| `--outdated` | Show only outdated packages | true |
| `--vulnerable` | Show only packages with known CVEs | false |
| `--major` | Include major version upgrades | false |
| `--preview` | Include preview/prerelease versions | false |
| `--dry-run` | Show what would change without applying | false |
| `--project <path>` | Target specific project (fuzzy matching) | All projects |
| `--interactive` | Use AskUserQuestion for each upgrade decision | true |
| `--auto` | Upgrade all without prompting (opposite of --interactive) | false |

## Workflow

### Step 1: Gather Package Information

Run the appropriate dotnet command:

```bash
# For outdated packages
dotnet list package --outdated [--include-prerelease]

# For vulnerable packages
dotnet list package --vulnerable

# For specific project
dotnet list "<project>" package --outdated
```

Parse the output to extract:

- Project name
- Package name
- Current version (Requested)
- Resolved version
- Latest version available

### Step 2: Analyze Upgrades

For each outdated package, categorize:

**Version Change Type:**

- **Patch** (1.0.0 -> 1.0.1): Bug fixes, safe to auto-upgrade
- **Minor** (1.0.0 -> 1.1.0): New features, backward compatible
- **Major** (1.0.0 -> 2.0.0): Breaking changes possible

**Risk Assessment:**

- Check if package has known breaking changes (use perplexity for major versions)
- Check if package is deprecated
- Check if newer version supports current TFM

### Step 3: Present Upgrades

Group packages by project and present summary:

```text
Package Upgrades Available

Project: src/MyApp/MyApp.csproj
  Package                    Current   Latest    Change
  Newtonsoft.Json            13.0.1    13.0.3    Patch
  Microsoft.Extensions.DI    8.0.0     10.0.0    Major (!)
  Serilog                    3.1.0     4.0.0     Major (!)

Project: tests/MyApp.Tests/MyApp.Tests.csproj
  Package                    Current   Latest    Change
  xunit                      2.6.0     2.9.0     Minor
  Moq                        4.18.0    4.20.0    Minor

Legend: (!) = Major version, may have breaking changes
```

### Step 4: Interactive Upgrade (if --interactive)

For each package (or group), use AskUserQuestion:

**For Patch/Minor versions:**

```text
Upgrade Newtonsoft.Json from 13.0.1 to 13.0.3 (patch)?

Options:
- Yes, upgrade
- Skip this package
- Upgrade all patches automatically
```

**For Major versions:**
First, research breaking changes:

```text
Use mcp__perplexity__search:
  query: "<package> <old version> to <new version> breaking changes migration"
```

Then present with context:

```text
Upgrade Microsoft.Extensions.DependencyInjection from 8.0.0 to 10.0.0?

Breaking Changes Found:
- IServiceCollection.AddXxx methods now return IServiceCollection
- Some obsolete APIs removed

Options:
- Yes, upgrade (will need code changes)
- Skip this package
- Show more details
```

### Step 5: Apply Upgrades

For each approved upgrade:

**If using Central Package Management (Directory.Packages.props):**

```bash
# Update version in Directory.Packages.props
# Use Edit tool to modify the file
```

**If using per-project references:**

```bash
dotnet add <project> package <package> --version <version>
```

### Step 6: Validate

After all upgrades:

```bash
dotnet restore
dotnet build
```

If build fails:

- Report which packages may have caused issues
- Suggest running `/dotnet:build --fix` to auto-resolve

## Output Format

**Dry Run:**

```text
[DRY RUN] Would upgrade the following packages:

Project: src/MyApp/MyApp.csproj
  Newtonsoft.Json: 13.0.1 -> 13.0.3 (patch)
  Serilog: 3.1.0 -> 4.0.0 (major)

Project: tests/MyApp.Tests/MyApp.Tests.csproj
  xunit: 2.6.0 -> 2.9.0 (minor)

Total: 3 packages across 2 projects
Run without --dry-run to apply upgrades.
```

**After Upgrade:**

```text
Package Upgrade Complete

Upgraded:
  - Newtonsoft.Json: 13.0.1 -> 13.0.3
  - Serilog: 3.1.0 -> 4.0.0
  - xunit: 2.6.0 -> 2.9.0

Skipped:
  - Microsoft.Extensions.DI (user skipped)

Validation:
  - dotnet restore: Success
  - dotnet build: Success

All packages upgraded successfully.
```

**With Build Errors:**

```text
Package Upgrade Complete (with issues)

Upgraded:
  - Serilog: 3.1.0 -> 4.0.0

Build Errors Detected:
  CS0619: 'Log.Logger' is obsolete in Serilog 4.0

Recommendations:
  1. Run /dotnet:build --fix to attempt auto-resolution
  2. Or revert with: dotnet add package Serilog --version 3.1.0
```

## Vulnerability Mode

When `--vulnerable` is specified:

```bash
dotnet list package --vulnerable
```

Output focuses on security:

```text
Vulnerable Packages Found

CRITICAL:
  - System.Text.Json 6.0.0 - CVE-2024-XXXXX (RCE)
    Fixed in: 6.0.10, 8.0.5

HIGH:
  - Newtonsoft.Json 12.0.0 - CVE-2024-YYYYY (DoS)
    Fixed in: 13.0.1

Recommendation: Upgrade vulnerable packages immediately.
Proceed with upgrade? [Y/n]
```

## Central Package Management Support

Detects and respects Directory.Packages.props:

1. Check for `<ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>`
2. If found, modify Directory.Packages.props instead of individual .csproj files
3. Report which file was modified

## Examples

```bash
# Show and interactively upgrade outdated packages
/dotnet:upgrade-nuget-packages

# Show vulnerable packages only
/dotnet:upgrade-nuget-packages --vulnerable

# Include major version upgrades
/dotnet:upgrade-nuget-packages --major

# Preview without applying
/dotnet:upgrade-nuget-packages --dry-run

# Upgrade all without prompting
/dotnet:upgrade-nuget-packages --auto

# Upgrade specific project
/dotnet:upgrade-nuget-packages --project MyApp.Api
```
