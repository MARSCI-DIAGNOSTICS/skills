---
name: audit-statuslines
description: Audit Claude Code status lines for quality and cross-platform compatibility. Use when creating or validating custom status line scripts, or troubleshooting terminal output issues.
argument-hint: [--force | --skip-validation]
allowed-tools: Read, Bash, Glob, Grep, Task
---

# Audit Status Lines Command

Audit Claude Code status line configurations for quality and cross-platform compatibility.

## Initialization

Before auditing, initialize the environment:

1. Get the current UTC date for audit timestamps.
2. Capture the project root path for subagent communication.
3. Ensure the temp directory (`.claude/temp/`) exists.
4. Clean up any stale audit files if the user confirms.

The `status-line-customization` skill provides authoritative validation guidance (auto-loaded when this command runs).

## What Gets Audited

- Script structure and execution
- JSON input handling
- Terminal color code usage
- Cross-platform compatibility (Windows, macOS, Linux)
- Helper function availability

## Command Arguments

| Argument | Description |
| --- | --- |
| *(none)* | Audit all discoverable status line scripts |
| `--force` | Audit regardless of modification status |
| `--skip-validation` | Skip finding validation (faster, but may include false positives) |

## Step 1: Discover Status Line Configurations

Check for `statusLine` settings in both project and user settings files.

For project settings, read `.claude/settings.json` and extract any `statusLine` value.

For user settings, detect the platform first: on Unix-like systems check `~/.claude/settings.json`, on Windows check `%USERPROFILE%\.claude\settings.json`. Then extract any `statusLine` value.

Each `statusLine` value points to a script file. Build a list of discovered scripts with their scope (project or user) and full path.

If no custom status lines are configured, report this and provide guidance on how to create one.

## Step 2: Parse Arguments

Check if the `--force` flag is present in the command arguments. Build the audit queue based on discovered scripts and the force flag.

## Step 3: Present Audit Plan

Display audit mode (SMART or FORCE), scripts discovered, and list each with scope and last modified date.

## Step 4: Execute Audits

For each script, spawn the `statusline-auditor` subagent with the following context:

- Scope (project or user)
- Full path to the script file
- Settings file reference
- Last audit date or "Never audited"
- Current audit date
- Project root path

Run subagents in parallel when multiple scripts exist.

Subagents write findings to `.claude/temp/` as both JSON (for recovery/aggregation) and markdown (for human review). The main conversation thread collects results and updates audit logs using its Write/Edit tools.

## Step 4.5: Validate Findings

**Unless `--skip-validation` flag is present:**

1. Spawn the `audit-finding-validator` agent with:
   - `project_root`: The captured project root path
   - `audit_type`: "statusline"
   - `audit_files`: List of `.claude/temp/audit-*-statusline-*.json` file paths
2. Wait for validation to complete
3. Read updated JSON files with validation results
4. Filter out FALSE_POSITIVE findings completely before aggregation
5. Note: Filtered findings are logged to `.claude/temp/audit-filtered-findings.json`

**If `--skip-validation` flag is present:**

- Skip validation phase entirely (current speed preserved)
- Present all findings without filtering
- Note in summary: "Validation: Skipped"

## Step 5: Final Summary

Report total scripts audited, results by scope, and details table. List cross-platform or JSON handling issues with remediation steps.

**Include validation statistics (if validation was performed):**

- Validation performed: Yes/No
- Findings validated: X
- False positives filtered: Y
- Verified findings: Z
- Unverified findings: W

## Important Notes

### Script Requirements

Status line scripts must accept JSON input via stdin, parse it correctly, output formatted terminal text, and work across Windows (Git Bash/PowerShell), macOS, and Linux.

### Cross-Platform Paths

| Platform | Settings Location |
| --- | --- |
| Unix | `~/.claude/settings.json` |
| Windows | `%USERPROFILE%\.claude\settings.json` |

### Terminal Color Codes

Use ANSI escape codes correctly with fallbacks for terminals without color support.

## Audit Log Location

All audit results are written to `.claude/audit/statuslines.md`.

Use `/audit-log statuslines` to view current audit status.

## Example Usage

### Example 1: Audit All Status Lines

```text
User: /audit-statuslines

Claude: Discovering status line configurations...

## Audit Plan
**Mode**: SMART
**Scripts discovered**: 2

1. [project] .claude/statusline.sh
2. [user] ~/scripts/my-statusline.py

[Spawns statusline-auditor subagents]

## Audit Complete
| Scope | Script | Result | Score |
| --- | --- | --- | --- |
| project | statusline.sh | PASS | 100/100 |
| user | my-statusline.py | PASS | 98/100 |
```

### Example 2: Force Audit

```text
User: /audit-statuslines --force

Claude: Auditing all scripts (force mode)...
```
