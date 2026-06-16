---
name: clean
description: Recursively clean bin/obj folders with optional package cache and artifacts cleanup
argument-hint: "[--all] [--packages] [--artifacts] [--dry-run] [--project <name>]"
allowed-tools: Bash, Glob, Read, AskUserQuestion
---

# /dotnet:clean

Recursively clean build artifacts (bin/obj folders) with options for package cache and artifacts folders.

## Arguments

Parse arguments from `$ARGUMENTS`:

| Flag | Description | Default |
|------|-------------|---------|
| `--all` | Clean bin, obj, packages, and artifacts | false |
| `--packages` | Also clear NuGet packages cache for solution | false |
| `--artifacts` | Also clean publish/artifacts folders | false |
| `--project <path>` | Target specific project (fuzzy matching) | All projects |
| `--dry-run` | Show what would be deleted without deleting | false |

## Workflow

### Step 1: Locate Target

If `--project` specified:

1. Use Glob to find matching `.csproj` file
2. Scope cleaning to that project's directory only

If no project specified:

1. Find solution file in current/parent directories
2. Clean all projects in solution directory tree

### Step 2: Find Directories to Clean

Always clean:

- `**/bin/` directories
- `**/obj/` directories

If `--packages` or `--all`:

- Local `.packages/` folder if exists
- NuGet HTTP cache for this solution (use `dotnet nuget locals http-cache --clear`)

If `--artifacts` or `--all`:

- `**/publish/` directories
- `**/artifacts/` directories
- `**/.artifacts/` directories (SDK-style artifacts output)

### Step 3: Calculate Size

Before deletion, calculate total size:

```bash
# For each directory found, sum sizes
du -sh <directories>
```

### Step 4: Execute or Report

If `--dry-run`:

```text
Would delete the following directories:

  bin/obj folders:
    src/MyApp/bin/ (45 MB)
    src/MyApp/obj/ (12 MB)
    tests/MyApp.Tests/bin/ (23 MB)
    tests/MyApp.Tests/obj/ (8 MB)

  Total: 88 MB across 4 directories

Run without --dry-run to delete.
```

If NOT `--dry-run`:

1. Delete directories using platform-appropriate commands:
   - Windows: `Remove-Item -Recurse -Force` or `rm -rf` (Git Bash)
   - Unix: `rm -rf`

2. Report results:

```text
Cleaned 4 directories, freed 88 MB

  Deleted:
    src/MyApp/bin/
    src/MyApp/obj/
    tests/MyApp.Tests/bin/
    tests/MyApp.Tests/obj/
```

### Step 5: Clear NuGet Cache (if requested)

If `--packages` or `--all`:

```bash
dotnet nuget locals http-cache --clear
dotnet nuget locals temp --clear
```

Report cache clearing results.

## Platform Considerations

**Windows (Git Bash):**

```bash
find . -type d \( -name "bin" -o -name "obj" \) -exec rm -rf {} + 2>/dev/null || true
```

**Windows (PowerShell) - AVOID:**
Do NOT use PowerShell for deletion. Use Git Bash `rm -rf` instead.

**Unix/macOS:**

```bash
find . -type d \( -name "bin" -o -name "obj" \) -exec rm -rf {} + 2>/dev/null || true
```

## Output Format

**Dry Run:**

```text
[DRY RUN] Would clean the following:

bin/obj folders (4 directories, 88 MB):
  - src/MyApp/bin/ (45 MB)
  - src/MyApp/obj/ (12 MB)
  - tests/MyApp.Tests/bin/ (23 MB)
  - tests/MyApp.Tests/obj/ (8 MB)

Run without --dry-run to delete.
```

**Actual Clean:**

```text
Cleaned .NET build artifacts

  Removed: 4 directories
  Freed: 88 MB

  Directories deleted:
    - src/MyApp/bin/
    - src/MyApp/obj/
    - tests/MyApp.Tests/bin/
    - tests/MyApp.Tests/obj/
```

**With Packages:**

```text
Cleaned .NET build artifacts and NuGet cache

  Build artifacts: 4 directories, 88 MB
  NuGet HTTP cache: cleared
  NuGet temp cache: cleared

  Total freed: ~150 MB
```

## Examples

```bash
# Clean bin and obj folders
/dotnet:clean

# Preview what would be cleaned
/dotnet:clean --dry-run

# Clean everything including package cache
/dotnet:clean --all

# Clean specific project
/dotnet:clean --project MyApp.Api

# Clean including artifacts folders
/dotnet:clean --artifacts
```

## Safety

- Always shows what will be deleted before proceeding (unless --dry-run)
- Does not delete source files
- Does not delete git-tracked files
- Skips directories that fail to delete (reports them)
