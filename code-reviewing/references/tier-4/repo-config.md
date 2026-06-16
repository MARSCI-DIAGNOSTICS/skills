# Repository Configuration Reference

**Token Budget:** ~2,500 tokens | **Load Type:** When detecting repo-specific configuration

This reference documents the `.claude/code-review.md` configuration format for customizing code reviews on a per-repository basis.

## Configuration Priority

The code reviewer loads configuration in this priority order:

```text
1. .claude/code-review.md (primary - dedicated config)
   └── Found: Parse and apply, STOP
   └── Not found: Continue to fallback

2. CLAUDE.md + @imports (fallback - existing project instructions)
   └── Found: Read CLAUDE.md + follow ALL @imports
   └── Not found: Continue to fallback

3. No config found
   └── Interactive mode: AskUserQuestion "No review config found. Use defaults?"
   └── Non-interactive: Apply default rules only
```

## Native Rules Integration (.claude/rules/)

Claude Code auto-loads `.claude/rules/*.md` into ALL agent contexts. This provides a lightweight, zero-parsing alternative to `.claude/code-review.md`.

### When to Use Which

| Mechanism | Best For | Structured? | Auto-Loaded? |
| --- | --- | --- | --- |
| `.claude/code-review.md` | Severity overrides, exclude rules, custom checks with patterns | Yes | No (agents read) |
| `.claude/rules/*.md` | Natural language review guidelines, path-scoped rules | No (free-form) | Yes (runtime injects) |
| Both | Full customization | Mixed | Mixed |

### Example

A path-scoped rules file at `.claude/rules/code-review.md`:

```markdown
---
paths:
  - "src/legacy/**"
---

# Legacy Code Review Rules

- Do not flag `async-void` patterns in legacy event handlers
- Long methods (>50 lines) are acceptable in migration utilities
- Suppress `magic-numbers` findings in configuration constants
```

### Interaction with .claude/code-review.md

- `.claude/code-review.md` provides structured config (exclusions, overrides)
- `.claude/rules/` provides additional review rules (applied on top)
- If a rule in `.claude/rules/` contradicts a `.claude/code-review.md` exclusion, the exclusion wins (structured config takes precedence)

## File Location

Place the configuration file at: `.claude/code-review.md`

This location:

- Keeps repo root clean
- Consistent with other Claude Code configurations
- Automatically ignored by most tools
- Easy to find and maintain

## Configuration Sections

### Tech Stack

Declare the technology stack explicitly. Overrides auto-detection from manifests.

```markdown
## Tech Stack

- **Runtime**: .NET 10
- **Frameworks**: ASP.NET Core, Entity Framework Core 10
- **Packages**: MediatR, FluentValidation, Polly
- **Frontend**: React 19, TypeScript 5.7
- **Database**: SQL Server 2022
```

**Parsing Rules:**

- Each line starting with `- **` is a tech stack entry
- Key is text before `:` (e.g., "Runtime", "Frameworks")
- Value is text after `:` (comma-separated for multiple)
- Used to improve MCP query accuracy

**If omitted:** Auto-detect from `package.json`, `*.csproj`, `requirements.txt`, `Cargo.toml`

### Exclude Rules

Disable specific rules for this repository.

```markdown
## Exclude Rules

Disable these rules for this project:
- `sql-injection` - Not a database project
- `async-void` - Legacy codebase pattern, accepted here
- `missing-alt-text` - Internal tool, no accessibility requirement
- `CA1307` - String comparisons are culture-insensitive by design
```

**Parsing Rules:**

- Each line starting with `-` followed by backtick-quoted ID is an exclusion
- Rule ID is the backtick-quoted text (e.g., `sql-injection`, `CA1307`)
- Text after `-` is the reason (optional but recommended)
- Rule IDs match internal rule names or analyzer codes

**Valid Rule IDs:**

| Category | Rule ID Pattern | Examples |
| --- | --- | --- |
| Security | `sql-injection`, `xss`, `secrets-in-code` | OWASP-based rules |
| Quality | `long-method`, `god-class`, `magic-numbers` | Clean code rules |
| Analyzer | `CA####`, `IDE####`, `CS####` | Roslyn analyzer codes |
| Custom | Any string | Project-specific rules |

### Severity Overrides

Change the default severity of specific rules.

```markdown
## Severity Overrides

| Rule ID | Default | Override | Reason |
| --- | --- | --- | --- |
| CA1307 | major | minor | String comparisons are culture-insensitive by design |
| missing-tests | critical | warning | MVP phase, tests will be added later |
| long-method | warning | suggestion | Legacy code being gradually refactored |
```

**Parsing Rules:**

- Table format with 4 columns: Rule ID, Default, Override, Reason
- Override must be: `critical`, `major`, `minor`, `warning`, or `suggestion`
- Reason is optional but strongly recommended

**Severity Levels:**

| Level | Meaning |
| --- | --- |
| `critical` | Must fix before merge |
| `major` | Should fix, significant issue |
| `minor` | Should fix, minor issue |
| `warning` | Consider fixing |
| `suggestion` | Nice to have (prefix: "Nit:") |

### Custom Checks

Add project-specific checks that don't exist in default rules.

```markdown
## Custom Checks

### PowerShell Naming (major)
- **Pattern**: `*.ps1`
- **Check**: Filename must match PascalCase-VerbNoun pattern
- **Message**: PowerShell scripts must follow Verb-Noun naming (e.g., Get-Data.ps1)

### No Bash Scripts (critical)
- **Pattern**: `*.sh`
- **Check**: Should not exist
- **Message**: This repo uses PowerShell exclusively - no Bash scripts allowed

### Required License Header (minor)
- **Pattern**: `*.cs`
- **Check**: First 5 lines must contain "Copyright"
- **Message**: All C# files must include license header
```

**Parsing Rules:**

- Each `### Header (severity)` starts a custom check
- Header is the check name
- Severity in parentheses: `critical`, `major`, `minor`, `warning`, `suggestion`
- `**Pattern**`: File glob pattern to match
- `**Check**`: What to verify (natural language)
- `**Message**`: Message shown when check fails

**Check Types:**

| Check Description | Behavior |
| --- | --- |
| "Should not exist" | Fail if matching files exist |
| "Must exist" | Fail if no matching files |
| "Filename must match X" | Validate filename pattern |
| "Must contain X" | Grep for content |
| "First N lines must contain X" | Check file header |

### Patterns

**Profile**: `thorough`, `strict`

Configure expected codebase patterns for compliance checking. Overrides auto-detection.

```markdown
## Patterns

### Error Handling
- **Pattern**: Result<T>
- **Alternatives**: exceptions, Either, error-codes, Option

### Architecture
- **Patterns**: CQRS, mediator, repository
- **Layer Structure**: domain-driven

### Naming
- **Classes**: PascalCase
- **Methods**: PascalCase
- **Variables**: camelCase
- **Constants**: UPPER_SNAKE
- **Interfaces**: I-prefix
- **Private Fields**: _underscore

### File Organization
- **Style**: feature-folders
- **Alternatives**: layer-folders, domain-folders, hybrid
```

**Parsing Rules:**

- `### Error Handling` → `**Pattern**` is the expected error handling approach
- `### Architecture` → `**Patterns**` is comma-separated list of expected patterns
- `### Naming` → Each `**Key**` maps to naming convention for that element
- `### File Organization` → `**Style**` is the folder organization pattern

**If omitted:** Auto-detect patterns by sampling existing code (20+ files).

**Pattern Options:**

| Category | Valid Values |
| --- | --- |
| Error Handling | `Result<T>`, `Either`, `exceptions`, `error-codes`, `Option` |
| Architecture | `CQRS`, `mediator`, `repository`, `unit-of-work`, `domain-events` |
| Naming (classes) | `PascalCase`, `camelCase`, `snake_case` |
| Naming (interfaces) | `I-prefix`, `no-prefix`, `Interface-suffix` |
| File Organization | `feature-folders`, `layer-folders`, `domain-folders`, `hybrid` |

### Breaking Changes

Configure breaking change detection behavior.

```markdown
## Breaking Changes

### Mode
- **Mode**: library
- **Alternatives**: internal, disabled

### Ignore Paths
- tests/**
- internal/**
- *.Tests.cs
- *.Spec.ts

### Allowed Breaking Changes
- Remove deprecated `GetUserById` method (scheduled for v3.0)
- Change `OrderStatus` enum values (internal only)
```

**Parsing Rules:**

- `### Mode` → `**Mode**` sets detection strictness
- `### Ignore Paths` → Glob patterns for paths to skip
- `### Allowed Breaking Changes` → Natural language descriptions of allowed changes

**Mode Options:**

| Mode | Behavior |
| --- | --- |
| `library` | Strict - all breaking changes CRITICAL (default for packages/libraries) |
| `internal` | Relaxed - breaking changes MAJOR (for internal projects) |
| `disabled` | No breaking change detection |

**If omitted:** Auto-detect based on project type:

- `package.json` with `main`/`exports` → `library` mode
- `.csproj` with `<IsPackable>true</IsPackable>` → `library` mode
- Otherwise → `internal` mode

### History Analysis

**Profile**: `thorough`, `strict` (configurable for all profiles via `--history` flag)

Configure git history analysis for coupling detection, hot spot identification, and ownership context.

```markdown
## History Analysis

### Thresholds
- **coupling_threshold**: 60
- **hotspot_window_months**: 3
- **hotspot_threshold**: 10

### Behavior
- **skip_history**: false
- **include_author_context**: false
```

**Parsing Rules:**

- `### Thresholds` → Numeric thresholds for detection algorithms
- `### Behavior` → Boolean flags controlling analysis behavior

**Threshold Options:**

| Field | Type | Default | Range | Description |
| --- | --- | --- | --- | --- |
| `coupling_threshold` | number | 60 | 40-90 | Co-change percentage to flag missing files |
| `hotspot_window_months` | number | 3 | 1-12 | Time window for change frequency analysis |
| `hotspot_threshold` | number | 10 | 5-50 | Changes count to flag as hot spot |

**Behavior Options:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `skip_history` | boolean | false | Disable history analysis entirely |
| `include_author_context` | boolean | false | Include author ownership (normally strict-only) |

**If omitted:** Use defaults:

- Coupling threshold: 60% (flag files that change together >60% of the time)
- Hot spot window: 3 months
- Hot spot threshold: 10+ changes = hot spot
- History analysis enabled for thorough/strict profiles

**Example Configurations:**

```markdown
## History Analysis

### Thresholds
- **coupling_threshold**: 70
- **hotspot_window_months**: 6
- **hotspot_threshold**: 15

### Behavior
- **skip_history**: false
- **include_author_context**: true
```

This configuration:

- Raises coupling threshold to 70% (fewer false positives)
- Extends hot spot window to 6 months (for slower-moving codebases)
- Requires 15+ changes to flag as hot spot
- Enables author context for all profiles (not just strict)

### Import Chain Control

Configure how CLAUDE.md @imports are followed (applies to fallback mode).

```markdown
## Import Chain

Control how CLAUDE.md is read:
- **Depth**: 2
- **Include Sections**: Critical Rules, Conventions, Architecture
- **Exclude Sections**: Version History, Contributors
```

**Parsing Rules:**

- `**Depth**`: How many levels of @imports to follow (0 = CLAUDE.md only, -1 = unlimited)
- `**Include Sections**`: Only include these `## Header` sections (comma-separated)
- `**Exclude Sections**`: Skip these `## Header` sections (comma-separated)

**Defaults (if omitted):**

- Depth: -1 (follow all @imports)
- Include Sections: all
- Exclude Sections: none

## Complete Example

```markdown
# Code Review Configuration

## Tech Stack

- **Runtime**: .NET 10
- **Frameworks**: ASP.NET Core 10, Entity Framework Core 10
- **Packages**: MediatR 12, FluentValidation 11, Polly 8
- **Frontend**: None (API-only project)
- **Database**: SQL Server 2022

## Exclude Rules

Disable these rules for this project:
- `missing-frontend-tests` - API-only project, no frontend
- `async-void` - Legacy event handlers, will be refactored in Q2
- `magic-numbers` - Configuration values are intentionally inline

## Severity Overrides

| Rule ID | Default | Override | Reason |
| --- | --- | --- | --- |
| CA1307 | major | minor | Internal API, locale-insensitive |
| missing-swagger | critical | warning | Swagger added incrementally |

## Custom Checks

### Verb-Noun PowerShell Scripts (major)
- **Pattern**: `*.ps1`
- **Check**: Filename must match PascalCase-VerbNoun pattern
- **Message**: PowerShell scripts must follow Verb-Noun naming

### No Console.WriteLine (warning)
- **Pattern**: `*.cs`
- **Check**: Must not contain Console.WriteLine
- **Message**: Use ILogger instead of Console.WriteLine

## History Analysis

### Thresholds
- **coupling_threshold**: 60
- **hotspot_window_months**: 3
- **hotspot_threshold**: 10

### Behavior
- **skip_history**: false
- **include_author_context**: false

## Import Chain

- **Depth**: 2
- **Include Sections**: Critical Rules, Conventions
```

## Validation Rules

The reviewer validates the configuration file:

| Check | Severity | Message |
| --- | --- | --- |
| Invalid severity level | Error | "Override severity must be: critical, major, minor, warning, suggestion" |
| Unknown rule ID in override | Warning | "Rule ID 'X' not found in default rules - may be custom" |
| Conflicting exclusion and override | Error | "Rule 'X' is both excluded and has severity override" |
| Missing Pattern in custom check | Error | "Custom check 'X' missing required **Pattern**" |
| Missing Check in custom check | Error | "Custom check 'X' missing required **Check**" |
| Invalid depth value | Error | "Depth must be integer >= -1" |
| Invalid coupling_threshold | Error | "coupling_threshold must be integer 40-90" |
| Invalid hotspot_window_months | Error | "hotspot_window_months must be integer 1-12" |
| Invalid hotspot_threshold | Error | "hotspot_threshold must be integer 5-50" |

## Provenance Reporting

When configuration is loaded, the review report includes a Configuration Summary:

```markdown
## Configuration Summary

**Source**: `.claude/code-review.md`
**Tech Stack**: .NET 10, ASP.NET Core 10 (config override)
**Rules Excluded**: 3 (missing-frontend-tests, async-void, magic-numbers)
**Severity Overrides**: 2 (CA1307: major→minor, missing-swagger: critical→warning)
**Custom Checks**: 2 (Verb-Noun PowerShell Scripts, No Console.WriteLine)
**History Analysis**: enabled (coupling: 60%, window: 3mo, threshold: 10)
**Import Chain**: N/A (primary config used)
```

For fallback mode:

```markdown
## Configuration Summary

**Source**: CLAUDE.md + @imports (fallback)
**Files Parsed**: CLAUDE.md, .claude/memory/behavioral-guardrails.md, .claude/memory/rule-compliance.md
**Sections Applied**: Critical Rules, Conventions
**Import Depth**: 2
**Rules Extracted**: 5 (from "Critical Rules" sections)
```

## Migration from CLAUDE.md

If you have review rules scattered in CLAUDE.md, consolidate them:

1. Create `.claude/code-review.md`
2. Extract rules from CLAUDE.md `## Critical Rules` sections
3. Convert natural language rules to structured format
4. Test with `--show-rules` flag to verify parsing

**Before (CLAUDE.md):**

```markdown
## Critical Rules

- Always use explicit types, not var
- PowerShell scripts must use Verb-Noun naming
- No Console.WriteLine in production code
```

**After (.claude/code-review.md):**

```markdown
## Custom Checks

### Explicit Types Required (major)
- **Pattern**: `*.cs`
- **Check**: Must not contain "var " at line start
- **Message**: Use explicit types, not var

### PowerShell Naming (major)
- **Pattern**: `*.ps1`
- **Check**: Filename must match PascalCase-VerbNoun
- **Message**: PowerShell scripts must use Verb-Noun naming

### No Console.WriteLine (warning)
- **Pattern**: `*.cs`
- **Check**: Must not contain Console.WriteLine
- **Message**: Use ILogger instead of Console.WriteLine
```

---

**Last Updated:** 2025-12-31
