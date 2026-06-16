---
name: solution-health
description: Analyze solution structure for orphaned projects, circular dependencies, and TFM inconsistencies
argument-hint: "[--solution <name>] [--check <category>]"
allowed-tools: Bash, Read, Glob, Grep
---

# /dotnet:solution-health

Comprehensive solution health analysis covering structure, dependencies, versioning, and best practices.

## Arguments

Parse arguments from `$ARGUMENTS`:

| Flag | Description | Default |
|------|-------------|---------|
| `--solution <path>` | Target solution (fuzzy matching) | Auto-detect |
| `--check <category>` | Run specific check only | All checks |
| `--fix-suggestions` | Include actionable fix commands | true |

## Health Checks

| Check | Category | Description |
|-------|----------|-------------|
| Orphaned projects | structure | Projects in folder but not in .sln |
| Missing references | dependencies | Referenced projects that don't exist |
| Circular dependencies | dependencies | A -> B -> A cycles |
| TFM inconsistencies | versioning | Mixed target frameworks |
| Duplicate packages | packages | Same package, different versions |
| Central package management | packages | Directory.Packages.props status |
| Build props | config | Directory.Build.props presence |
| EditorConfig | config | .editorconfig presence |
| Git ignored artifacts | hygiene | bin/obj in git |

## Workflow

### Step 1: Locate Solution

Find and parse solution file:

```bash
# Find .sln files
find . -name "*.sln" -maxdepth 2

# Parse solution for project references
grep "Project(" *.sln
```

### Step 2: Run Health Checks

Execute each check and collect findings.

### Step 3: Generate Report

## Output Format

```text
Solution Health Report

Solution: MyApp.sln
Location: D:\repos\myapp
Projects: 12
Generated: 2026-01-18 11:00:00 UTC

═══════════════════════════════════════════════════════════════
                        HEALTH SCORE: 78/100
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│ Category         Status    Issues    Score                  │
├─────────────────────────────────────────────────────────────┤
│ Structure        Warning   1         15/20                  │
│ Dependencies     Pass      0         20/20                  │
│ Versioning       Warning   2         12/20                  │
│ Packages         Warning   3         16/20                  │
│ Configuration    Pass      0         15/20                  │
└─────────────────────────────────────────────────────────────┘

───────────────────────────────────────────────────────────────
STRUCTURE CHECKS
───────────────────────────────────────────────────────────────

[WARNING] Orphaned Projects Found

  Projects in filesystem but not in solution:
    - tools/CodeGen/CodeGen.csproj
    - experimental/Prototype/Prototype.csproj

  Fix: Add to solution or delete if unused
    dotnet sln add tools/CodeGen/CodeGen.csproj
    dotnet sln add experimental/Prototype/Prototype.csproj

[PASS] No Missing Project References

  All referenced projects exist and are resolvable.

[PASS] No Circular Dependencies

  Dependency graph is acyclic.

───────────────────────────────────────────────────────────────
VERSIONING CHECKS
───────────────────────────────────────────────────────────────

[WARNING] Inconsistent Target Frameworks

  Most projects: net10.0 (10 projects)
  Outliers:
    - src/Legacy/Legacy.csproj: net8.0
    - tests/Integration/Integration.csproj: net9.0

  Recommendation: Standardize TFMs across solution
  Run: /dotnet:update-dotnet-version --check-only

[WARNING] LangVersion Not Standardized

  Projects without explicit LangVersion: 4
  Projects with LangVersion: 8

  Recommendation: Set LangVersion in Directory.Build.props

[INFO] SDK Version

  global.json: 10.0.100 (rollForward: latestPatch)
  Installed: 10.0.100

───────────────────────────────────────────────────────────────
PACKAGE CHECKS
───────────────────────────────────────────────────────────────

[WARNING] Duplicate Package Versions

  Newtonsoft.Json:
    - 13.0.1 in src/MyApp.Core
    - 13.0.3 in src/MyApp.Api
    - 12.0.3 in src/Legacy

  Microsoft.Extensions.Logging:
    - 8.0.0 in 3 projects
    - 10.0.0 in 7 projects

  Fix: Consolidate versions or enable Central Package Management

[WARNING] Central Package Management Not Enabled

  You have 12 projects with package references.
  Central Package Management would consolidate version management.

  Enable:
    1. Create Directory.Packages.props
    2. Add <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
    3. Move versions from .csproj to Directory.Packages.props

[PASS] No Vulnerable Packages

  Run 'dotnet list package --vulnerable' returned no results.

───────────────────────────────────────────────────────────────
CONFIGURATION CHECKS
───────────────────────────────────────────────────────────────

[PASS] Directory.Build.props Found

  Location: D:\repos\myapp\Directory.Build.props
  Contents:
    - TreatWarningsAsErrors: true
    - Nullable: enable
    - ImplicitUsings: enable

[PASS] .editorconfig Found

  Location: D:\repos\myapp\.editorconfig
  Enforcing: 45 rules

[PASS] .gitignore Configured

  bin/ and obj/ are properly ignored.

───────────────────────────────────────────────────────────────
RECOMMENDATIONS
───────────────────────────────────────────────────────────────

Priority fixes to improve health score:

1. [EASY] Add orphaned projects to solution
   Impact: +5 points
   Command: dotnet sln add tools/CodeGen/CodeGen.csproj

2. [MEDIUM] Standardize target frameworks
   Impact: +8 points
   Command: /dotnet:update-dotnet-version

3. [MEDIUM] Enable Central Package Management
   Impact: +5 points
   Creates: Directory.Packages.props

4. [EASY] Consolidate Newtonsoft.Json versions
   Impact: +2 points
   Command: Update all to 13.0.3

───────────────────────────────────────────────────────────────
PROJECT DEPENDENCY GRAPH
───────────────────────────────────────────────────────────────

MyApp.Api
  └── MyApp.Core
  └── MyApp.Infrastructure
        └── MyApp.Core
        └── MyApp.Domain
  └── MyApp.Domain

MyApp.Tests
  └── MyApp.Api
  └── MyApp.Core

(No circular dependencies detected)
```

## Check Details

### Orphaned Projects

Projects found in filesystem but not referenced in .sln:

```bash
# Find all .csproj files
find . -name "*.csproj" -type f

# Compare against solution references
# Report difference
```

### Circular Dependencies

Build dependency graph from ProjectReference elements:

```xml
<ProjectReference Include="..\Other\Other.csproj" />
```

Detect cycles using DFS traversal.

### TFM Inconsistencies

Parse TargetFramework(s) from all projects:

```bash
grep -h "<TargetFramework" **/*.csproj
```

Report when projects use different TFMs without apparent reason.

### Duplicate Package Versions

Parse PackageReference elements:

```xml
<PackageReference Include="Newtonsoft.Json" Version="13.0.1" />
```

Group by package, flag different versions.

## Examples

```bash
# Full health check
/dotnet:solution-health

# Check specific category only
/dotnet:solution-health --check dependencies

# Check specific solution
/dotnet:solution-health --solution MyApp.sln

# Quick check without fix suggestions
/dotnet:solution-health --fix-suggestions false
```

## Health Score Calculation

| Category | Max Points | Criteria |
|----------|------------|----------|
| Structure | 20 | No orphaned projects, no missing refs |
| Dependencies | 20 | No circular deps, clean graph |
| Versioning | 20 | Consistent TFMs, global.json present |
| Packages | 20 | No duplicates, CPM enabled, no vulnerabilities |
| Configuration | 20 | Build.props, editorconfig, gitignore |

**Score Interpretation:**

- 90-100: Excellent - Well-maintained solution
- 70-89: Good - Minor improvements recommended
- 50-69: Fair - Several issues to address
- Below 50: Needs attention - Significant technical debt
