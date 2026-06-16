---
name: hook-schema-audit
description: Audit hook event schema for drift. Compares implementation against official docs.
user-invocable: true
argument-hint: "[--fix | --json | --verbose]"
allowed-tools: Read, Bash, Glob, Grep, Task, Skill, WebFetch
---

# Audit Hook Schema

Detect drift between the hook dispatcher's `EVENT_FIELD_REGISTRY` and official Claude Code documentation.

## Arguments

- `--fix`: Generate updated registry code (output only, does not auto-apply)
- `--json`: Machine-readable JSON output for CI/automation
- `--verbose`: Show all fields, not just differences

## Workflow

### Step 1: Load Official Documentation

Load the hook-management skill and query for official hook event schemas:

```text
Skill(hook-management)
```

Also spawn the claude-code-guide agent for live web documentation:

```text
Task(claude-code-guide, "WebFetch https://code.claude.com/docs/en/claude_code_docs_map.md to find hook event documentation pages. Then WebFetch those pages. Extract the input fields for each hook event: PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest, Notification, UserPromptSubmit, Stop, SubagentStart, SubagentStop, PreCompact, SessionStart, SessionEnd, TeammateIdle, TaskCompleted. Return structured data with event name and field lists.")
```

### Step 2: Parse Current Implementation

Read the `EVENT_FIELD_REGISTRY` from `hook_dispatcher.py`:

```bash
# Extract the registry definition
grep -A 30 "EVENT_FIELD_REGISTRY = {" plugins/claude-code-observability/hooks/hook_dispatcher.py
```

Parse the registry into a structured format for comparison.

### Step 3: Compare and Report

For each hook event, compare:

1. **Documented fields** (from official docs)
2. **Implemented fields** (from `EVENT_FIELD_REGISTRY`)

Generate a report showing:

| Event | Documented | Implemented | Missing | Extra |
|-------|------------|-------------|---------|-------|
| pretooluse | 5 | 3 | tool_input | - |
| notification | 2 | 0 | message, notification_type | - |

### Step 4: Output Format

**Default output:**

```text
Hook Schema Audit Report
========================
Schema Version: 1.7.0
Audit Date: 2026-02-15T15:30:00Z

Coverage Summary:
- Total events: 14
- Fully covered: 11 (79%)
- Partially covered: 2 (14%)
- Missing: 1 (7%)

Findings:
[WARNING] notification: Missing fields: message, notification_type
[WARNING] userpromptsubmit: Missing fields: prompt
[OK] pretooluse: All documented fields present
...

Recommendation: Update EVENT_FIELD_REGISTRY to include missing fields.
```

**With `--json`:**

```json
{
  "schema_version": "1.7.0",
  "audit_timestamp": "2026-02-15T15:30:00Z",
  "coverage": {
    "total_events": 14,
    "fully_covered": 11,
    "partially_covered": 2,
    "missing": 1
  },
  "events": {
    "pretooluse": {
      "status": "ok",
      "documented": ["tool_name", "tool_input", "tool_use_id"],
      "implemented": ["tool_name", "tool_input", "tool_use_id"],
      "missing": [],
      "extra": []
    }
  }
}
```

**With `--fix`:**

Output updated Python code for `EVENT_FIELD_REGISTRY` that can be copy-pasted into `hook_dispatcher.py`.

### Step 5: Recommendations

Based on findings, provide actionable recommendations:

- If fields are missing: Suggest adding them to the registry
- If extra fields found in logs: Investigate if they're new Claude Code fields
- If schema version outdated: Suggest incrementing SCHEMA_VERSION

## Usage Examples

```bash
# Basic audit
/claude-code-observability:audit-hook-schema

# CI integration (machine-readable)
/claude-code-observability:audit-hook-schema --json

# Generate fix
/claude-code-observability:audit-hook-schema --fix

# Detailed output
/claude-code-observability:audit-hook-schema --verbose
```

## Exit Codes (for CI)

When using `--json`:

- `0`: All events fully covered
- `1`: Some fields missing (partial coverage)
- `2`: Critical drift detected (events missing entirely)
