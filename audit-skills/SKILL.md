---
name: audit-skills
description: Audit Claude Code skills for quality, compliance, delegation pattern, and maintainability. Use after creating skills, before releases, or for periodic quality checks.
argument-hint: "[skill-name] [--force | --skip-validation | --plugin-only | --project-only | --global-only]"
allowed-tools: Read, Bash, Glob, Grep, Task
---

# Audit Skills

Audit Claude Code skills for quality, compliance, delegation pattern, and maintainability.

## Initialization

Before auditing, initialize the environment:

Get the current UTC date, capture the project root path, ensure the temp directory exists, and clean up stale audit files. The `skill-development` skill provides authoritative validation guidance (auto-loaded when this command runs).

## Audit Types

### Type A: Standard Skill Audit

For regular skills (git-setup, markdown-linting): YAML frontmatter, naming, file structure, progressive disclosure, documentation quality.

### Type B: Meta-Skill Audit

For Claude Code meta-skills (skill-development, docs-management): Zero duplication, delegation pattern compliance, metadata-only content.

The audit auto-detects type based on the skill's name and description.

## Arguments

| Argument | Description |
| --- | --- |
| *(none)* | Smart mode: audit modified, never-audited, or stale (>90 days) skills |
| `--force` | Audit ALL skills regardless of status |
| `--skip-validation` | Skip finding validation (faster, but may include false positives) |
| `--plugin-only` | Only audit local plugin skills |
| `--project-only` | Only audit project skills (`.claude/skills/`) |
| `--global-only` | Only audit globally installed plugin skills |
| `skill-name` | Audit specific skill(s) by name |

## Step 1: Discover Skill Sources

Detect all skill sources in local repo and globally installed plugins.

For local discovery, check marketplace repos, single plugin repos, and `.claude/skills/`. For each plugin, scan `skills/` directories. Track plugin names for deduplication.

For global discovery, check `~/.claude/plugins/` (Unix) or `%USERPROFILE%\.claude\plugins\` (Windows). Scan `skills/` directories within each plugin. Skip globals with local dev versions.

## Step 2: Parse Arguments

Parse flags and skill names. Read audit logs for each source.

## Step 3: Present Audit Plan

Display mode, sources discovered, type distribution (A vs B), and audit queue.

## Step 4: Execute Audits

For each skill, detect type then spawn the `skill-auditor` subagent with source, path, type (A or B), and last audit date. Run in parallel batches of 3-5.

Subagents write findings to `.claude/temp/`. The main conversation thread collects results and updates audit logs using its Write/Edit tools.

## Step 4.5: Validate Findings

**Unless `--skip-validation` flag is present:**

1. Spawn the `audit-finding-validator` agent with:
   - `project_root`: The captured project root path
   - `audit_type`: "skill"
   - `audit_files`: List of `.claude/temp/audit-*-skill-*.json` file paths
2. Wait for validation to complete
3. Read updated JSON files with validation results
4. Filter out FALSE_POSITIVE findings completely before aggregation
5. Note: Filtered findings are logged to `.claude/temp/audit-filtered-findings.json`

**If `--skip-validation` flag is present:**

- Skip validation phase entirely (current speed preserved)
- Present all findings without filtering
- Note in summary: "Validation: Skipped"

## Step 5: Final Summary

Report total audited by source and type, results, and details table. Note that global skill fixes must be applied manually.

**Include validation statistics (if validation was performed):**

- Validation performed: Yes/No
- Findings validated: X
- False positives filtered: Y
- Verified findings: Z
- Unverified findings: W

## Scoring

- **PASS** (85+): Ready for use
- **PASS WITH WARNINGS** (70-84): Functional with improvement opportunities
- **FAIL** (<70): Issues that should be addressed

## Audit Log Location

All audit results are written to `.claude/audit/skills.md`.

Use `/audit-log skills` to view current audit status.

## Example Usage

### Example 1: Audit All Skills

```text
User: /audit-skills

Claude: Discovering skill sources...

## Audit Plan
**Mode**: SMART
- Plugin: claude-ecosystem (41 skills)
- Plugin: code-quality (9 skills)
- Type A: 43, Type B: 7
- Deduplicated: claude-ecosystem (global skipped)

**Will audit**: 12 items

[Spawns skill-auditor subagents]

## Audit Complete
| Source | Name | Type | Result | Score |
| --- | --- | --- | --- | --- |
| plugin | docs-management | B | PASS | 100/100 |
| plugin | scrape-docs | A | PASS | 95/100 |
```

### Example 2: Audit Specific Skill

```text
User: /audit-skills plugin:docs-management
Claude: PASS (Score: 100/100) - Excellent delegation pattern compliance
```
