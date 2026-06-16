---
name: audit-settings
description: Audit Claude Code settings.json files for quality, compliance, and security. Use to validate configuration before deployment or check for exposed secrets.
argument-hint: "[project | user | all] [--force | --skip-validation]"
allowed-tools: Read, Bash, Glob, Grep, Task
model: opus
---

# Audit Settings Command

Audit Claude Code settings.json files for quality, compliance, and security.

## Initialization

Before auditing, initialize the environment:

Get the current UTC date, capture the project root path, ensure the temp directory exists, and clean up stale audit files. The `settings-management` skill provides authoritative validation guidance (auto-loaded when this command runs).

## What Gets Audited

- JSON syntax validity
- Schema compliance (valid settings options)
- Permission rules configuration
- Sandbox settings
- Environment variable configuration
- Security (no exposed secrets)

## Command Arguments

| Argument | Description |
| --- | --- |
| *(none)* | Audit all discoverable settings files |
| `project` | Only audit `.claude/settings.json` |
| `user` | Only audit `~/.claude/settings.json` |
| `all` | Audit all scopes explicitly |
| `--force` | Audit regardless of modification status |
| `--skip-validation` | Skip finding validation (faster, but may include false positives) |

## Step 1: Discover Settings Files

Check project settings (`.claude/settings.json`), user settings (`~/.claude/settings.json` on Unix, `%USERPROFILE%\.claude\settings.json` on Windows), and plugin settings in marketplace repos.

## Step 2: Parse Arguments

Parse scope selector and `--force` flag. Filter files to match requested scope.

## Step 3: Present Audit Plan

Display mode, files discovered, and list with scope and last modified date.

## Step 4: Execute Audits

For each file, spawn the `settings-auditor` subagent with scope, path, and last audit date. Run in parallel when multiple exist.

Subagents write findings to `.claude/temp/`. The main conversation thread collects results and updates audit logs using its Write/Edit tools.

## Step 4.5: Validate Findings

**Unless `--skip-validation` flag is present:**

1. Spawn the `audit-finding-validator` agent with:
   - `project_root`: The captured project root path
   - `audit_type`: "settings"
   - `audit_files`: List of `.claude/temp/audit-*-settings-*.json` file paths
2. Wait for validation to complete
3. Read updated JSON files with validation results
4. Filter out FALSE_POSITIVE findings completely before aggregation
5. Note: Filtered findings are logged to `.claude/temp/audit-filtered-findings.json`

**If `--skip-validation` flag is present:**

- Skip validation phase entirely (current speed preserved)
- Present all findings without filtering
- Note in summary: "Validation: Skipped"

## Step 5: Final Summary

Report total audited by scope, results, and details table. List security alerts with remediation.

**Include validation statistics (if validation was performed):**

- Validation performed: Yes/No
- Findings validated: X
- False positives filtered: Y
- Verified findings: Z
- Unverified findings: W

## Security Considerations

| Scope | Credentials Found | Result |
| --- | --- | --- |
| Project | Yes | CRITICAL - version controlled |
| User | Yes | WARNING - not version controlled |

Project settings should NEVER contain API keys or tokens (version controlled).

### Cross-Platform Paths

| Platform | User Settings |
| --- | --- |
| Unix | `~/.claude/settings.json` |
| Windows | `%USERPROFILE%\.claude\settings.json` |

## Audit Log Location

All audit results are written to `.claude/audit/settings.md`.

Use `/audit-log settings` to view current audit status.

## Example Usage

### Example 1: Audit All Settings Files

```text
User: /audit-settings

Claude: Discovering settings files...

## Audit Plan
**Mode**: SMART
**Files discovered**: 2

1. [project] .claude/settings.json
2. [user] ~/.claude/settings.json

[Spawns settings-auditor subagents]

## Audit Complete
| Scope | File | Result | Score |
| --- | --- | --- | --- |
| project | .claude/settings.json | PASS | 100/100 |
| user | ~/.claude/settings.json | PASS | 98/100 |
```

### Example 2: Audit Project Only

```text
User: /audit-settings project
Claude: Auditing project settings...
```
