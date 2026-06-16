---
name: nullable-audit
description: Analyze nullable reference type adoption with warnings breakdown and migration recommendations
argument-hint: "[--project <name>] [--detailed] [--warnings]"
allowed-tools: Bash, Read, Glob, Grep, AskUserQuestion
---

# /dotnet:nullable-audit

Analyze nullable reference type (NRT) adoption across the codebase with detailed warnings breakdown and migration recommendations.

## Arguments

Parse arguments from `$ARGUMENTS`:

| Flag | Description | Default |
|------|-------------|---------|
| `--project <path>` | Target specific project (fuzzy matching) | All projects |
| `--detailed` | Show per-file breakdown | false |
| `--warnings` | Show all nullable warnings | false |

## Workflow

### Step 1: Scan Project Configuration

Check nullable status in project files:

```bash
# Find all project files
find . -name "*.csproj" -type f

# Check for nullable enable
grep -l "<Nullable>enable</Nullable>" **/*.csproj
grep -l "<Nullable>disable</Nullable>" **/*.csproj
grep -l "<Nullable>warnings</Nullable>" **/*.csproj
grep -l "<Nullable>annotations</Nullable>" **/*.csproj
```

Check Directory.Build.props for solution-wide settings.

### Step 2: Scan Source Files

For projects without solution-wide nullable:

```bash
# Find files with #nullable directives
grep -r "#nullable enable" --include="*.cs" .
grep -r "#nullable disable" --include="*.cs" .
grep -r "#nullable restore" --include="*.cs" .
```

Count total .cs files vs nullable-enabled files.

### Step 3: Gather Nullable Warnings

Build and capture nullable warnings:

```bash
dotnet build 2>&1 | grep -E "CS86[0-9]{2}|CS87[0-9]{2}"
```

Categorize by warning type:

- **CS8600**: Converting null literal
- **CS8601**: Possible null reference assignment
- **CS8602**: Dereference of possibly null reference
- **CS8603**: Possible null reference return
- **CS8604**: Possible null reference argument
- **CS8618**: Non-nullable field not initialized
- **CS8625**: Cannot convert null to non-nullable
- **CS8765**: Nullability of parameter doesn't match

### Step 4: Generate Report

## Output Format

**Summary Report:**

```text
Nullable Reference Types Audit

Solution: MyApp.sln
Projects: 12

┌─────────────────────────────────────────────────────────────┐
│ Nullable Adoption Status                                    │
├─────────────────────────────────────────────────────────────┤
│ Project                      Status        Files    Issues  │
├─────────────────────────────────────────────────────────────┤
│ src/MyApp.Core               enable        45       12      │
│ src/MyApp.Api                enable        32       8       │
│ src/MyApp.Infrastructure     enable        28       23      │
│ src/MyApp.Domain             enable        18       0       │
│ tests/MyApp.Tests            disable       42       N/A     │
│ src/MyApp.Legacy             (not set)     15       N/A     │
└─────────────────────────────────────────────────────────────┘

Adoption Rate: 83% (10/12 projects with nullable enabled)
Files with NRT: 123/180 (68%)

Warning Summary:
  CS8602 (Null dereference):        18
  CS8618 (Uninitialized field):     12
  CS8604 (Null argument):           8
  CS8600 (Null assignment):         5
  Total nullable warnings:          43
```

**Detailed Report (--detailed):**

```text
Nullable Reference Types Audit (Detailed)

═══════════════════════════════════════════════════════════════
Project: src/MyApp.Infrastructure
Nullable: enable (project-level)
═══════════════════════════════════════════════════════════════

Files with warnings:
  src/MyApp.Infrastructure/Repositories/UserRepository.cs
    - CS8602: line 42 - _context.Users may be null
    - CS8602: line 67 - user.Email may be null
    - CS8618: line 12 - _context not initialized

  src/MyApp.Infrastructure/Services/CacheService.cs
    - CS8604: line 28 - argument may be null
    - CS8600: line 35 - null assignment

  ... (more files)

Files without warnings (clean):
  src/MyApp.Infrastructure/Extensions/ServiceCollectionExtensions.cs
  src/MyApp.Infrastructure/DependencyInjection.cs
  ... (15 more)

───────────────────────────────────────────────────────────────
Project: src/MyApp.Legacy
Nullable: NOT ENABLED
───────────────────────────────────────────────────────────────

This project does not have nullable reference types enabled.
To enable, add to .csproj:
  <PropertyGroup>
    <Nullable>enable</Nullable>
  </PropertyGroup>

Or enable per-file with #nullable enable directive.
```

**Warnings Report (--warnings):**

```text
Nullable Warnings by Category

CS8602: Dereference of a possibly null reference (18 warnings)
────────────────────────────────────────────────────────────────
  src/MyApp.Infrastructure/Repositories/UserRepository.cs:42
    var name = user.Name.ToUpper();  // user.Name may be null

  src/MyApp.Api/Controllers/UsersController.cs:67
    return Ok(result.Data.Items);    // result.Data may be null

  ... (16 more)

  Fix: Add null checks or use null-conditional operator (?.)
  Example: var name = user.Name?.ToUpper() ?? string.Empty;

CS8618: Non-nullable field must be initialized (12 warnings)
────────────────────────────────────────────────────────────────
  src/MyApp.Core/Models/User.cs:12
    public string Email { get; set; }  // Not initialized

  src/MyApp.Core/Models/Order.cs:8
    public Customer Customer { get; set; }  // Not initialized

  ... (10 more)

  Fix options:
    1. Initialize with default: public string Email { get; set; } = string.Empty;
    2. Make nullable: public string? Email { get; set; }
    3. Use required modifier (C# 11+): public required string Email { get; set; }
    4. Initialize in constructor

CS8604: Possible null reference argument (8 warnings)
────────────────────────────────────────────────────────────────
  ... (details)
```

## Migration Recommendations

Based on audit results, provide recommendations:

```text
Migration Recommendations

1. IMMEDIATE (High Impact, Low Effort)
   ─────────────────────────────────────
   - Enable nullable in src/MyApp.Legacy (15 files, expected ~20 warnings)
   - Enable nullable in test projects (optional but recommended)

2. QUICK WINS (Auto-fixable)
   ─────────────────────────────────────
   - CS8618 warnings: Add = null! or required modifier (12 warnings)
   - CS8625 warnings: Fix null literal assignments (5 warnings)

   Run: /dotnet:fix-warnings --category nullable

3. REVIEW NEEDED (Context-dependent)
   ─────────────────────────────────────
   - CS8602 dereference warnings: Add null checks (18 warnings)
   - CS8604 argument warnings: Validate inputs (8 warnings)

   These require understanding of whether null is valid.

4. OPTIONAL CLEANUP
   ─────────────────────────────────────
   - Remove #nullable disable directives in enabled projects (3 files)
   - Consider enabling nullable in test projects

Estimated effort: 2-4 hours for full migration
```

## Nullable Status Reference

| Setting | Annotations | Warnings |
|---------|-------------|----------|
| `enable` | Yes | Yes |
| `disable` | No | No |
| `warnings` | No | Yes |
| `annotations` | Yes | No |

## Examples

```bash
# Basic audit summary
/dotnet:nullable-audit

# Detailed per-file breakdown
/dotnet:nullable-audit --detailed

# Show all nullable warnings with fixes
/dotnet:nullable-audit --warnings

# Audit specific project
/dotnet:nullable-audit --project MyApp.Core
```

## Integration with Other Commands

After audit, use these commands to address findings:

```bash
# Auto-fix what's possible
/dotnet:fix-warnings --category nullable

# Enable nullable in a project (manual edit or use Edit tool)
# Add <Nullable>enable</Nullable> to .csproj

# Rebuild to see remaining warnings
/dotnet:build
```
