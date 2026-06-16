---
name: sync-environment-variables
description: Add missing environment variable defaults to settings.json or settings.local.json
argument-hint: "[--target project|local] [--dry-run] [--include-undocumented]"
allowed-tools: Task, Skill, Read, Write, Edit, WebFetch, AskUserQuestion
---

# Sync Environment Variables

Add missing environment variable entries with explicit defaults to settings files.

## Arguments

| Argument | Description |
|----------|-------------|
| `--target project` | Update `.claude/settings.json` (default) |
| `--target local` | Update `.claude/settings.local.json` |
| `--dry-run` | Show changes without modifying files |
| `--include-undocumented` | Include changelog/discovered vars (not just official) |

## Phase 1: Discovery

Run environment variable discovery using the same process as `list-environment-variables`:

1. Invoke `docs-management` skill for official documentation
2. WebFetch CHANGELOG.md for additional variables
3. If `--include-undocumented`, spawn MCP research agents

Collect all discovered variables with their default values.

## Phase 2: Read Current Settings

Determine target file based on `--target` argument:

| Target | File Path |
|--------|-----------|
| `project` (default) | `.claude/settings.json` |
| `local` | `.claude/settings.local.json` |

Read the target file. If it doesn't exist:

- For `project`: Create new file with basic structure
- For `local`: Create new file (this is gitignored)

Parse the current `env` section (if present).

## Phase 3: Compare and Categorize

For each discovered environment variable, categorize:

| Category | Criteria | Action |
|----------|----------|--------|
| **MISSING** | Not in current settings, has known default | Add to settings |
| **EXISTS** | Already in current settings | Skip (preserve user value) |
| **USER-SPECIFIC** | No universal default (e.g., API keys) | Skip, report only |
| **CUSTOM** | `CLAUDE_HOOK_*` or repo-specific | Never touch |

### Variables to Add (with defaults)

These variables have known, safe defaults:

```json
{
  "env": {
    "DISABLE_AUTOUPDATER": "0",
    "DISABLE_TELEMETRY": "0",
    "CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR": "0",
    "CLAUDE_CODE_SKIP_EXT_PROMPT": "0"
  }
}
```

### Variables to NEVER Add Automatically

- `ANTHROPIC_API_KEY` - User-specific, no default
- `CLAUDE_CODE_USE_BEDROCK` - Provider choice, user decision
- `CLAUDE_CODE_USE_VERTEX` - Provider choice, user decision
- `AWS_*` - AWS credentials, user-specific
- `GOOGLE_*` - Google credentials, user-specific
- `HTTP_PROXY` / `HTTPS_PROXY` - Network-specific
- `CLAUDE_HOOK_*` - Repository-specific hook variables

## Phase 4: Preview Changes

Display what will be added:

```markdown
## Environment Variable Sync Preview

### Target: .claude/settings.json

### Variables to Add
| Variable | Default | Reason |
|----------|---------|--------|
| DISABLE_AUTOUPDATER | "0" | Official default, not in current settings |
| ... | ... | ... |

### Variables Skipped (Already Set)
| Variable | Current Value |
|----------|---------------|
| DISABLE_TELEMETRY | "1" |
| ... | ... |

### Variables Skipped (No Safe Default)
| Variable | Reason |
|----------|--------|
| ANTHROPIC_API_KEY | User-specific, no universal default |
| ... | ... |
```

## Phase 5: User Confirmation

Unless `--dry-run` is specified, ask for confirmation:

```yaml
AskUserQuestion:
  question: "Apply these changes to settings?"
  options:
    - "Yes, apply changes"
    - "No, abort"
    - "Show me the full file preview first"
```

If `--dry-run`, stop here and report "Dry run complete. No changes made."

## Phase 6: Apply and Validate

1. **Read current file** (or create new if doesn't exist)
2. **Merge new env vars** into existing `env` section
3. **Preserve existing values** - never overwrite user-set values
4. **Alphabetical order** - sort env vars alphabetically
5. **Write updated file**
6. **Validate JSON** - ensure file is valid JSON after write
7. **Report success**

### File Structure

```json
{
  "env": {
    "CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR": "0",
    "DISABLE_AUTOUPDATER": "0",
    "DISABLE_TELEMETRY": "0"
  }
}
```

If file has other sections (permissions, hooks, etc.), preserve them.

## Error Handling

| Error | Action |
|-------|--------|
| Target file not valid JSON | Report error, do not modify |
| Write permission denied | Report error with path |
| Discovery failed | Report partial results, ask to continue |

## Post-Sync Verification

After applying changes:

1. Read back the modified file
2. Validate JSON syntax
3. Confirm all intended changes were applied
4. Report any discrepancies

## Example Output

```markdown
## Sync Complete

**Target:** .claude/settings.json

### Added (3 variables)
- CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR = "0"
- DISABLE_AUTOUPDATER = "0"
- CLAUDE_CODE_SKIP_EXT_PROMPT = "0"

### Preserved (1 variable)
- DISABLE_TELEMETRY = "1" (user-set value kept)

### Skipped (2 variables)
- ANTHROPIC_API_KEY (no safe default)
- CLAUDE_CODE_USE_BEDROCK (provider choice)

**File validated:** JSON syntax OK
```
