---
name: update-settings-schema
description: Update the custom Claude Code settings JSON schema with changelog-discovered and web-verified settings.
argument-hint: [--dry-run | --validate-only | --diff]
allowed-tools: Read, Bash, Skill, Task, WebFetch
---

# Update Settings Schema Command

Update the custom JSON schema for Claude Code settings by researching official documentation, parsing the CHANGELOG, and merging discovered settings.

## Arguments

| Argument | Description |
|----------|-------------|
| (none) | Full update: research, generate, validate, write |
| `--dry-run` | Show changes without writing |
| `--validate-only` | Validate current schema without updating |
| `--diff` | Show diff between current and generated |
| `--sync-env-vars` | Force sync environment variables from canonical docs |

## Workflow

### Step 1: Load Current State

Read the current schema and extract version metadata:

```text
Schema location: plugins/claude-ecosystem/skills/settings-management/references/claude-code-settings.schema.json
Extract: x-schema-version, x-claude-code-version, x-changelog-hash
```

### Step 2: Extract Environment Variables

Run the env var extraction from canonical docs (stored in docs-management):

```bash
python plugins/claude-ecosystem/skills/settings-management/scripts/schema/extract_env_vars.py
```

This extracts 68+ environment variables from the settings.md documentation with:

- Full descriptions
- Category tags (authentication, model-config, provider, bash-behavior, etc.)
- Boolean flag detection (`enum: ["0", "1"]`)
- Deprecation markers
- Version annotations (`x-since`)

### Step 3: Research Sources (Parallel)

Invoke all three research sources in the SAME message:

1. **docs-management skill** - Query for settings documentation:

   ```text
   Invoke docs-management skill with query: "settings.json available settings schema options table env hooks permissions sandbox"
   ```

2. **claude-code-guide agent** - Live web search:

   ```text
   Spawn claude-code-guide subagent with prompt:
   "First WebFetch https://code.claude.com/docs/en/claude_code_docs_map.md to find relevant doc pages about settings configuration. Then WebFetch the settings.md page. Use WebSearch only if needed for additional context about new settings fields. Return a list of all settings fields with their types and descriptions."
   ```

3. **Changelog fetch** - Get latest CHANGELOG.md:

   ```text
   WebFetch https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
   Extract settings-related entries from v2.1.0 onwards.
   ```

### Step 4: Merge and Deduplicate

Priority order for conflicting information:

1. **Official docs** (via docs-management) - highest priority
2. **Web search** (via claude-code-guide) - medium priority
3. **Changelog** (via WebFetch) - lowest priority

For each setting field:

- If in official docs: mark `x-source: "official"`
- If only in web search: mark `x-source: "web"`
- If only in changelog: mark `x-source: "changelog"`
- Add `x-since: "version"` for changelog-discovered fields

### Step 5: Validate

Run the validation script:

```bash
python plugins/claude-ecosystem/skills/settings-management/scripts/schema/validate_schema.py --verbose
```

Schema must:

- Be valid JSON Schema draft-07
- Have all required x- metadata fields
- Pass example validation (if --check-examples)

### Step 6: Write (unless --dry-run)

If validation passes and not --dry-run:

1. Update the schema file
2. Increment x-schema-version (patch version)
3. Update x-last-updated to today
4. Update x-changelog-hash with new hash
5. Update x-env-var-count with current env var count

### Step 7: Report

Show summary:

```text
Schema Update Summary
--------------------
Previous version: 1.0.0
New version: 1.1.0
Claude Code tracked: 2.1.9
Properties: 40 (+3 new)
  + plansDirectory (v2.1.9, changelog)
  + showTurnDuration (v2.1.7, changelog)
  + mcpToolSearch (v2.1.7, changelog)

Environment Variables: 68
  Categories: authentication (6), model-config (10), provider (6),
              bash-behavior (7), configuration (15), disable-flags (13),
              proxy (3), mcp (5), vertex-bedrock (5), tools (2)

Validation: PASSED
Written to: .../claude-code-settings.schema.json
```

## What This Command Does NOT Do

- Does NOT modify SchemaStore directly (that requires a PR to SchemaStore repo)
- Does NOT scrape arbitrary web pages (only official Claude docs)
- Does NOT auto-commit changes (user must commit manually)

## Mode-Specific Behavior

### --validate-only

Skip research and write steps. Only validate current schema:

```bash
python .../validate_schema.py --verbose --check-examples
```

Report validation results and exit.

### --dry-run

Execute full workflow but skip Step 5 (write). Show what would change.

### --diff

Execute full workflow, generate new schema in memory, show diff:

```text
+ Added: mcpToolSearch (string)
~ Modified: hooks.PreToolUse (added additionalContext note)
  x-schema-version: 1.0.0 -> 1.0.1
  x-last-updated: 2026-01-15 -> 2026-01-16
```

## Related Commands

- `/audit-settings` - Audit settings.json files against this schema
- `/list settings` - List available settings fields

## Related Files

| File | Purpose |
|------|---------|
| `references/claude-code-settings.schema.json` | The custom schema file with 68 env vars |
| `scripts/schema/generate_schema.py` | Schema generation and env var sync |
| `scripts/schema/extract_env_vars.py` | Extract env vars from canonical docs |
| `scripts/schema/validate_schema.py` | Standalone validator |
| `.claude/ecosystem-health.yaml` | Tracks schema version |
