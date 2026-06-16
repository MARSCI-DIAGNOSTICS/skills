---
name: update-dotnet-version
description: Comprehensive one-shot .NET version upgrade with SDK, TFM, packages, and build validation
argument-hint: "[--version <ver>] [--check-only] [--force] [--skip-packages]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, AskUserQuestion, mcp__perplexity__search, mcp__perplexity__reason, mcp__microsoft-learn__microsoft_docs_search
---

# /dotnet:update-dotnet-version

**Flagship command:** Comprehensive .NET version upgrade that handles SDK installation, TFM updates, package compatibility, and build validation with automatic error resolution.

## Arguments

Parse arguments from `$ARGUMENTS`:

| Flag | Description | Default |
|------|-------------|---------|
| `--version <version>` | Target .NET version (e.g., 10, 10.0) | Latest stable |
| `--check-only` | Analyze without making changes | false |
| `--force` | Skip compatibility warnings and proceed | false |
| `--skip-packages` | Skip package upgrades | false |
| `--skip-build` | Skip build validation | false |

## Workflow Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                 /dotnet:update-dotnet-version               │
├─────────────────────────────────────────────────────────────┤
│ 1. Pre-flight Analysis                                      │
│    ├── Detect current TFM across all projects               │
│    ├── Check package compatibility with target              │
│    └── Report blockers                                      │
├─────────────────────────────────────────────────────────────┤
│ 2. SDK Installation                                         │
│    ├── Check if target SDK installed                        │
│    └── Install via /dotnet:install-sdk if needed            │
├─────────────────────────────────────────────────────────────┤
│ 3. Update global.json                                       │
│    └── Set SDK version and rollForward policy               │
├─────────────────────────────────────────────────────────────┤
│ 4. Update Target Frameworks                                 │
│    ├── Update <TargetFramework> in all .csproj              │
│    ├── Update <LangVersion> if needed                       │
│    └── Update Directory.Build.props if centralized          │
├─────────────────────────────────────────────────────────────┤
│ 5. Upgrade Packages                                         │
│    └── Run /dotnet:upgrade-nuget-packages --major --auto    │
├─────────────────────────────────────────────────────────────┤
│ 6. Build & Fix Loop                                         │
│    ├── Run dotnet build                                     │
│    ├── If errors: spawn build-fixer agent                   │
│    └── Retry up to 5 times                                  │
├─────────────────────────────────────────────────────────────┤
│ 7. Verification                                             │
│    ├── Run tests if available                               │
│    └── Report final status                                  │
└─────────────────────────────────────────────────────────────┘
```

## Detailed Workflow

### Phase 1: Pre-flight Analysis

**1.1 Detect Current State:**

```bash
# Find all project files
find . -name "*.csproj" -type f

# Extract current TFMs
grep -h "<TargetFramework" **/*.csproj | sort -u
```

Parse and report:

```text
Current .NET Version Analysis

  Projects found: 12
  Current TFM: net9.0 (10 projects), net8.0 (2 projects)
  Target TFM: net10.0

  Mixed TFM detected: 2 projects on net8.0
    - src/Legacy/Legacy.csproj
    - tests/Legacy.Tests/Legacy.Tests.csproj
```

**1.2 Package Compatibility Check:**

For each unique package, check .NET 10 support:

```text
Use mcp__perplexity__search:
  query: "<package-name> .NET 10 support compatibility January 2026"
```

Report findings:

```text
Package Compatibility Analysis

  Compatible (confirmed):
    - Microsoft.Extensions.* (10.0.0 available)
    - Serilog (4.0.0 supports net10.0)
    - xunit (2.9.0 supports net10.0)

  Needs Upgrade:
    - Newtonsoft.Json 12.0.0 -> 13.0.3 (net10.0 support)
    - AutoMapper 11.0.0 -> 13.0.0 (net10.0 support)

  Potential Blockers:
    - OldLibrary 2.0.0 - No .NET 10 support found
      Options: Find alternative, wait for update, or remove dependency

  Unknown (verify manually):
    - CustomInternalLib 1.0.0
```

**1.3 Breaking Changes Research:**

```text
Use mcp__microsoft-learn__microsoft_docs_search:
  query: ".NET 10 breaking changes migration from .NET 9"

Use mcp__perplexity__reason:
  query: ".NET 9 to .NET 10 migration breaking changes C# 14 what to watch for"
```

Report relevant breaking changes:

```text
Breaking Changes to Watch

  .NET 10 Breaking Changes:
    - System.Text.Json: New source generator requirements
    - ASP.NET Core: Minimal API changes
    - EF Core: Query behavior changes

  C# 14 New Features Available:
    - Field keyword in properties
    - Collection expressions improvements
    - Extension types (preview)
```

**1.4 Decision Point:**

If `--check-only`:

- Report analysis and exit

If blockers found and NOT `--force`:

```text
Blockers Found - Cannot Proceed

  1. OldLibrary 2.0.0 has no .NET 10 support

Options:
  1. Remove OldLibrary dependency first
  2. Run with --force to proceed anyway (may fail)
  3. Cancel and resolve manually

[AskUserQuestion with options]
```

### Phase 2: SDK Installation

Check if target SDK is installed:

```bash
dotnet --list-sdks | grep "^10\."
```

If not installed:

```text
.NET 10 SDK not found. Installing...

[Invoke /dotnet:install-sdk --version 10.0 --update-global-json]
```

### Phase 3: Update global.json

Create or update global.json:

```json
{
  "sdk": {
    "version": "10.0.100",
    "rollForward": "latestPatch"
  }
}
```

### Phase 4: Update Target Frameworks

**4.1 Check for centralized TFM:**

Look for Directory.Build.props with:

```xml
<TargetFramework>net9.0</TargetFramework>
```

If found, update only Directory.Build.props.

**4.2 Update individual projects:**

For each .csproj file:

```xml
<!-- Before -->
<TargetFramework>net9.0</TargetFramework>

<!-- After -->
<TargetFramework>net10.0</TargetFramework>
```

**4.3 Update LangVersion if explicit:**

```xml
<!-- If LangVersion is set explicitly -->
<LangVersion>13.0</LangVersion>
<!-- Update to -->
<LangVersion>14.0</LangVersion>
<!-- Or remove to use SDK default -->
```

**4.4 Handle multi-targeting:**

```xml
<!-- Before -->
<TargetFrameworks>net8.0;net9.0</TargetFrameworks>

<!-- After -->
<TargetFrameworks>net9.0;net10.0</TargetFrameworks>
```

### Phase 5: Upgrade Packages

Unless `--skip-packages`:

```text
Upgrading packages for .NET 10 compatibility...

[Invoke internal package upgrade logic]
```

Focus on:

- Microsoft.* packages (align with .NET version)
- Packages with known .NET 10 versions
- Security-vulnerable packages

### Phase 6: Build & Fix Loop

**6.1 Initial Build:**

```bash
dotnet build --verbosity minimal
```

**6.2 If errors, spawn build-fixer:**

```text
Build failed with 12 errors. Attempting auto-fix...

[Task: dotnet:build-fixer with error context]
```

**6.3 Retry loop:**

```text
Fix attempt 1/5:
  - Fixed 8 errors
  - 4 errors remaining

Fix attempt 2/5:
  - Fixed 3 errors
  - 1 error remaining

Fix attempt 3/5:
  - Fixed 1 error
  - Build successful!
```

**6.4 Max attempts reached:**

```text
Build still failing after 5 fix attempts.

Remaining errors:
  CS0012: Type 'OldType' is defined in assembly not referenced

These errors require manual intervention:
  1. OldLibrary uses types not available in .NET 10
  2. Consider removing or replacing OldLibrary

Partial upgrade complete. Manual fixes required.
```

### Phase 7: Verification

**7.1 Run tests (if available):**

```bash
dotnet test --no-build
```

**7.2 Report final status:**

## Output Format

**Check-Only Mode:**

```text
.NET Version Upgrade Analysis (--check-only)

  Current: net9.0
  Target: net10.0
  Projects: 12

Package Compatibility:
  Compatible: 45 packages
  Needs Upgrade: 8 packages
  Blockers: 1 package (OldLibrary)

Breaking Changes: 3 relevant changes found
  - System.Text.Json source generator changes
  - ASP.NET Core minimal API updates
  - EF Core query translation changes

Recommendation: Resolve OldLibrary dependency before upgrading.
Run without --check-only to proceed with upgrade.
```

**Successful Upgrade:**

```text
.NET Version Upgrade Complete

  Upgraded: net9.0 -> net10.0
  Projects modified: 12
  SDK: 10.0.100

Changes Made:
  - global.json: Created with SDK 10.0.100
  - Directory.Build.props: Updated TFM to net10.0
  - 12 .csproj files: Updated TFM
  - 8 packages upgraded to .NET 10 compatible versions

Build: Successful (after 2 fix iterations)
Tests: 142 passed, 0 failed

Fixes Applied:
  - Added System.Text.Json source generator attribute (3 files)
  - Updated deprecated API calls (5 files)

Upgrade complete! Your project now targets .NET 10.
```

**Partial Upgrade:**

```text
.NET Version Upgrade Partial

  Target: net10.0
  Projects modified: 12

Changes Made:
  - TFM updated to net10.0
  - 6 packages upgraded

Build Status: FAILED (after 5 fix attempts)

Remaining Issues:
  1. OldLibrary.OldType not available (3 errors)
     - src/MyApp/Services/LegacyService.cs:42
     - src/MyApp/Services/LegacyService.cs:78
     - src/MyApp/Models/LegacyModel.cs:15

Manual Action Required:
  Replace or remove OldLibrary dependency.
  Then run: dotnet build

Rollback Command (if needed):
  git checkout -- .
  dotnet restore
```

## Examples

```bash
# Analyze upgrade without making changes
/dotnet:update-dotnet-version --check-only

# Upgrade to latest stable .NET
/dotnet:update-dotnet-version

# Upgrade to specific version
/dotnet:update-dotnet-version --version 10.0

# Force upgrade despite warnings
/dotnet:update-dotnet-version --force

# Upgrade TFM only, skip packages
/dotnet:update-dotnet-version --skip-packages
```

## Rollback

If upgrade fails or causes issues:

```bash
# Revert all changes
git checkout -- .

# Restore original packages
dotnet restore

# Verify original state builds
dotnet build
```

## Related Commands

- `/dotnet:install-sdk` - Install SDK only
- `/dotnet:upgrade-nuget-packages` - Upgrade packages only
- `/dotnet:build --fix` - Build with auto-fix
- `/dotnet:solution-health` - Analyze project health
