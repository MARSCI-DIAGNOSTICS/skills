---
name: fix-warnings
description: Batch-fix analyzer warnings with category filtering and interactive review options
argument-hint: "[--category <cat>] [--preview] [--interactive] [--project <name>]"
allowed-tools: Bash, Read, Edit, Glob, Grep, AskUserQuestion
---

# /dotnet:fix-warnings

Batch-fix analyzer warnings with category filtering, preview mode, and interactive review options.

## Arguments

Parse arguments from `$ARGUMENTS`:

| Flag | Description | Default |
|------|-------------|---------|
| `--category <cat>` | Fix specific category (see below) | All fixable |
| `--severity <level>` | Minimum severity (error, warning, suggestion, hidden) | warning |
| `--preview` | Show changes without applying | false |
| `--interactive` | Review each fix before applying | false |
| `--project <path>` | Target specific project (fuzzy matching) | All projects |

## Warning Categories

| Category | Description | Analyzer Prefix |
|----------|-------------|-----------------|
| `style` | Code style (IDE*) | IDE0001-IDE0999 |
| `quality` | Code quality (CA*) | CA1000-CA9999 |
| `naming` | Naming conventions | CA1700-CA1727, IDE1006 |
| `performance` | Performance issues | CA1800-CA1869 |
| `security` | Security concerns | CA2100-CA2399, CA3000-CA3147 |
| `reliability` | Reliability issues | CA2000-CA2099 |
| `usage` | API usage issues | CA2200-CA2249 |
| `nullable` | Nullable reference warnings | CS8600-CS8799 |
| `async` | Async/await issues | CA2007, CA2008, CS8892 |

## Workflow

### Step 1: Run Analyzers

Build with detailed diagnostics:

```bash
dotnet build --no-incremental -warnaserror:0 2>&1
```

Or use format for fixable warnings:

```bash
dotnet format analyzers --verify-no-changes --verbosity diagnostic
```

### Step 2: Parse and Categorize Warnings

Group warnings by:

- Category (style, quality, naming, etc.)
- Severity (error, warning, suggestion)
- File location
- Fixability (auto-fixable vs manual)

### Step 3: Present Summary

```text
Analyzer Warnings Summary

  Category      Count   Auto-fixable
  ─────────────────────────────────────
  Style         42      38
  Quality       15      8
  Naming        7       7
  Nullable      23      12
  Performance   3       1
  ─────────────────────────────────────
  Total         90      66

Files affected: 28

Run with --preview to see specific warnings.
Run without flags to fix all auto-fixable warnings.
```

### Step 4: Preview Mode (--preview)

Show what would be changed:

```text
Preview: Warnings to Fix

IDE0008 (Style): Use explicit type instead of 'var' (12 occurrences)
  - src/MyApp/Services/UserService.cs:42
  - src/MyApp/Services/UserService.cs:56
  - src/MyApp/Controllers/ApiController.cs:23
  ... and 9 more

CA1062 (Quality): Validate arguments of public methods (5 occurrences)
  - src/MyApp/Services/DataService.cs:18
  - src/MyApp/Handlers/CommandHandler.cs:31
  ... and 3 more

CS8618 (Nullable): Non-nullable field not initialized (8 occurrences)
  - src/MyApp/Models/User.cs:12
  - src/MyApp/Models/Order.cs:8
  ... and 6 more

Total: 66 auto-fixable warnings across 28 files

Run without --preview to apply fixes.
```

### Step 5: Apply Fixes

**Automatic Mode (default):**

```bash
# Fix all style warnings
dotnet format style

# Fix all analyzer warnings
dotnet format analyzers

# Fix whitespace
dotnet format whitespace
```

**Category-specific:**

```bash
# Fix only naming warnings
dotnet format analyzers --diagnostics=CA1700,CA1707,CA1708,CA1710,CA1711,CA1712,CA1713,CA1714,CA1715,CA1716,CA1717,CA1720,CA1721,CA1724,CA1725,CA1727,IDE1006
```

**Interactive Mode (--interactive):**

For each warning category:

```text
Fix IDE0008: Use explicit type instead of 'var'? (12 occurrences)

Example:
  Before: var service = new UserService();
  After:  UserService service = new UserService();

Options:
  1. Fix all 12 occurrences
  2. Skip this rule
  3. Review each occurrence individually
```

### Step 6: Validate

After fixes:

```bash
dotnet build --no-restore
```

Report any issues introduced by fixes.

## Output Format

**Summary Mode (no flags):**

```text
Fixing Analyzer Warnings...

Applied fixes:
  Style (IDE*):      38 warnings fixed
  Quality (CA*):     8 warnings fixed
  Naming:            7 warnings fixed
  Nullable:          12 warnings fixed

Remaining (not auto-fixable):
  CA1062:  5 warnings - Validate arguments (manual review needed)
  CA2000:  3 warnings - Dispose objects (manual review needed)
  CS8604:  11 warnings - Possible null reference (context-dependent)

Files modified: 28
Build: Successful

Run with --category to fix specific categories.
Review remaining warnings manually or suppress with justification.
```

**Interactive Mode:**

```text
Fixing Warnings Interactively

[1/5] IDE0008: Use explicit type (12 occurrences)
  Fix all? [Y/n/s(kip)/r(eview)]
  > Y
  Fixed 12 occurrences

[2/5] CA1707: Remove underscores from member names (3 occurrences)
  Fix all? [Y/n/s(kip)/r(eview)]
  > r

  1. _myField -> MyField in User.cs:15
     Fix? [y/n] > y

  2. Get_Data() -> GetData() in DataService.cs:42
     Fix? [y/n] > n (skip - intentional convention)

  3. API_VERSION -> ApiVersion in Constants.cs:8
     Fix? [y/n] > y

  Fixed 2 of 3 occurrences

... (continues for each category)

Summary:
  Fixed: 52 warnings
  Skipped: 14 warnings (user choice)

Build: Successful
```

## Common Warning Fixes

| Warning | Auto-Fix | Manual Action |
|---------|----------|---------------|
| IDE0008 | Yes | Change `var` to explicit type |
| IDE0003 | Yes | Remove `this.` qualification |
| IDE0059 | Yes | Remove unnecessary assignment |
| CA1062 | Partial | Add null checks (context-dependent) |
| CA2000 | No | Add `using` or `.Dispose()` calls |
| CS8618 | Partial | Add `= null!` or `required` |
| CA1707 | Yes | Remove underscores |
| CA1716 | Yes | Rename to avoid keyword conflict |

## Examples

```bash
# Fix all auto-fixable warnings
/dotnet:fix-warnings

# Preview without fixing
/dotnet:fix-warnings --preview

# Fix only style warnings
/dotnet:fix-warnings --category style

# Fix only naming issues
/dotnet:fix-warnings --category naming

# Interactive mode - review each fix
/dotnet:fix-warnings --interactive

# Fix warnings in specific project
/dotnet:fix-warnings --project MyApp.Api

# Fix only errors and warnings (skip suggestions)
/dotnet:fix-warnings --severity warning
```

## Warnings That Cannot Be Auto-Fixed

Some warnings require manual review:

- **CA2000** (Dispose): Context-dependent object lifetime
- **CA1062** (Null check): May need different validation strategy
- **CA2007** (ConfigureAwait): Library vs app decision
- **CS8604** (Null flow): May need design change

For these, the command reports them but doesn't modify code.

## Integration with .editorconfig

Respects `.editorconfig` settings:

```ini
# These rules will be applied during fix
dotnet_style_var_for_built_in_types = false:warning
dotnet_naming_rule.public_members_must_be_capitalized.severity = warning
```
