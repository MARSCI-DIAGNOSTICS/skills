# Settings Audit Framework

**Architecture:** This framework provides scoring criteria and query guides. **All validation rules are fetched from official documentation via docs-management skill** - this file contains NO duplicated official content.

## 🚨 MANDATORY: Use docs-management BEFORE Any Finding

> **ABSOLUTE REQUIREMENT - NEVER SKIP THIS STEP:**
>
> Before flagging ANY finding about type requirements, schema compliance, or "should be X instead of Y":
>
> 1. **INVOKE** `docs-management` skill with query: `"settings.json" "available settings" "env" example`
> 2. **READ** the official documentation examples
> 3. **VERIFY** your finding matches what official docs show
> 4. **IF UNCERTAIN** → Do NOT flag. Ask for clarification instead.
>
> **Flagging findings without verifying against official docs = AUDIT FAILURE**

### Verification Checkpoint

Before including ANY finding in your audit report:

- [ ] Did I invoke docs-management for this topic?
- [ ] Did I read the official example/schema?
- [ ] Does my finding contradict official documentation?
- [ ] If official docs show `"FOO": "bar"`, am I suggesting `"FOO": bar`? ← **WRONG**

**If you cannot verify against official docs, mark finding as UNVERIFIED and do not deduct points.**

## How Audits Work

1. **Auditor invokes** `docs-management` skill for official schema/examples
2. **Official docs provide** the actual validation criteria (types, formats, valid values)
3. **This framework provides** scoring weights and thresholds only
4. **NEVER assume** - always verify against fetched documentation

## External Technology Validation

**CRITICAL:** Before flagging any finding related to external technologies, validate with MCP servers.

For complete validation guidance, see: `../../shared-references/external-tech-validation.md`

**Quick Reference:**

- .NET/Azure: microsoft-learn + perplexity (REQUIRED)
- npm/PyPI: context7 + perplexity
- Version claims: perplexity ALWAYS
- MCP unavailable: Flag as UNVERIFIED

## Documentation Query Guide

Before auditing, query `docs-management` skill for these topics:

| Category | Query Keywords | What to Fetch |
| --- | --- | --- |
| Schema | `settings.json available settings schema options table` | Valid options list |
| Permission Rules | `permissions allow deny ask rules patterns tool` | Rule syntax |
| Sandbox | `sandbox settings bash sandboxing configuration` | Sandbox options |
| Environment | `env settings environment variables ANTHROPIC` | Env config |
| Precedence | `settings config precedence hierarchy` | Hierarchy rules |
| Model Config | `model settings ANTHROPIC_MODEL default aliases` | Model options |
| Hooks Setting | `hooks setting disableAllHooks hooks.json` | Hook configuration |
| Plugin Settings | `plugin configuration enabledPlugins marketplaces` | Plugin options |

**CRITICAL:** The auditor MUST query docs-management and use the returned official documentation as the source of truth for validation rules.

## Audit Scoring Rubric

This scoring rubric is used by the `settings-auditor` agent for formal audits.

### Category Scores

| Category | Points | Description |
| --- | --- | --- |
| JSON Validity | 20 | Valid JSON syntax, well-formed |
| Schema Compliance | 25 | Only valid settings options used |
| Permission Rules | 25 | Valid permission patterns, appropriate restrictions |
| Environment Config | 15 | Valid env vars, no secrets exposed |
| Precedence Awareness | 15 | Correct scope usage |

The maximum possible score is **Total: 100 points**.

### Scoring Details

**Note:** Pass conditions are validated against official documentation fetched via docs-management. The criteria below describe WHAT to check, not the specific rules (which come from docs).

#### JSON Validity (20 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Valid JSON syntax | 10 | Syntax check |
| Well-formed structure | 5 | Query: "settings.json structure" |
| No trailing commas | 5 | Syntax check |

#### Schema Compliance (25 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Valid top-level keys | 10 | Query: "settings schema", "available settings" |
| Valid option values | 10 | Query: specific option documentation |
| No deprecated options | 5 | Query: "deprecated settings" |

#### Permission Rules (25 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Valid rule syntax | 10 | Query: "permission rules syntax" |
| Appropriate tool patterns | 8 | Query: "permission patterns" |
| No overly permissive rules | 7 | Analysis: security assessment |

#### Environment Config (15 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Valid env var names | 5 | Analysis: naming conventions |
| No exposed secrets | 7 | Security check: no API keys, passwords |
| Appropriate hook env vars | 3 | Repository standard |

#### Precedence Awareness (15 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Correct file location | 8 | Query: "settings precedence" |
| Appropriate scope | 7 | Analysis: settings match intended scope |

### Thresholds

| Score Range | Result |
| --- | --- |
| 85-100 | **PASS** |
| 70-84 | **PASS WITH WARNINGS** |
| Below 70 | **FAIL** |

### Automatic Failures

Regardless of score, a settings file **automatically fails** if:

- Invalid JSON syntax
- Contains exposed secrets in **project or enterprise scope** (API keys, passwords, tokens)
- Uses completely invalid/unrecognized options

**Note:** User-level settings with credentials receive WARNING (not auto-fail) since they are not version controlled. See "Scope-Aware Credential Detection" below.

### Scope-Aware Credential Detection

API keys and credentials in settings files are evaluated differently based on scope:

| Scope | Credentials Found | Severity | Score Impact | Rationale |
| --- | --- | --- | --- | --- |
| Project | Yes | CRITICAL | Auto-fail | Version controlled, shared with team |
| User | Yes | WARNING | -7 points (env config) | Not version controlled, personal use acceptable |
| Enterprise | Yes | CRITICAL | Auto-fail | Managed policy violation |

**Project-level (`.claude/settings.json`) messaging:**

- Impact: "Credentials exposed in version control history"
- Recommendations: Revoke keys, use environment variables, clean git history

**User-level (`~/.claude/settings.json`) messaging:**

- Impact: "Credentials stored in plaintext on local machine (not version controlled)"
- Recommendations: Consider using environment variables with `${VAR}` expansion
- Do NOT mention git history cleanup (not applicable)
- Acceptable: For personal development machines, hardcoded user-level keys are acceptable with warning

## Settings File Discovery

**Query docs-management:** `"settings.json" "settings file locations" "settings precedence"`

File locations come from official documentation. Do NOT hardcode paths - always verify current locations via docs-management.

## Repository-Specific Standards

These standards are specific to this repository and NOT from official Claude Code documentation:

| Standard | Value | Rationale |
| --- | --- | --- |
| Secrets in project settings | Never (CRITICAL) | Version controlled, shared |
| Secrets in user settings | Warning only | Not version controlled |
| Hook env var naming | `CLAUDE_HOOK_{NAME}_ENABLED` | Consistency |
| Descriptive comments | Via separate documentation | Settings is JSON (no comments) |

## 🚨 Required docs-management Queries Per Category

**MANDATORY:** Execute these queries BEFORE scoring each category:

| Category | Required Query | What to Verify |
| --- | --- | --- |
| Schema Compliance | `settings.json available settings schema options table` | Valid top-level keys, value types |
| Environment Config | `env settings environment variables example` | env values are STRINGS (see official example) |
| Permission Rules | `permissions allow deny ask rules patterns tool` | Valid rule patterns |
| Sandbox Settings | `sandbox settings bash sandboxing configuration` | Valid sandbox options |
| Precedence | `settings config precedence hierarchy` | Settings hierarchy |
| Model Config | `model settings ANTHROPIC_MODEL default aliases` | Model configuration |

**Query Execution Protocol:**

1. **Before each category** → Run the required query
2. **Read returned docs** → Find the relevant example/table
3. **Compare your finding** → Does it match official docs?
4. **If mismatch** → Your finding is WRONG, not the settings file
5. **If uncertain** → Do NOT deduct points, mark as NEEDS-VERIFICATION

## Extensive Validation Requirements

**CRITICAL:** Before flagging ANY finding, you MUST:

1. **Query docs-management EXTENSIVELY** - Use multiple keyword combinations
2. **Read the FULL official documentation** - Not just snippets
3. **Check for optional vs required fields** - Query: `"optional" "required" {topic}`
4. **Verify default behaviors** - Query: `"default" {topic}`
5. **Distinguish official vs repo-specific rules** - Only official rules are errors; repo-specific are suggestions
6. **Verify value types from official examples** - Query: `"env" settings example` to see actual types

**If official documentation does not explicitly prohibit something, do NOT flag it as an error.**

**If you cannot find documentation supporting your finding, the finding is INVALID.**

## Schema Validation Source

For authoritative schema validation, use the custom extended schema:

| Location | Path |
| --- | --- |
| Local | `references/claude-code-settings.schema.json` |
| Public URL | `https://raw.githubusercontent.com/melodic/claude-code-plugins/main/plugins/claude-ecosystem/skills/settings-management/references/claude-code-settings.schema.json` |

The custom schema extends SchemaStore with:

- **Changelog-discovered settings** - marked with `x-source: "changelog"` and `x-since: "version"`
- **Version introduction info** - `x-since` field tracks when each setting was added
- **Hook type additions** - agent hooks (v2.1.0+), PermissionRequest event (v2.0.45+)
- **Custom metadata** - `x-schema-version`, `x-claude-code-version`, `x-last-updated`

### Schema Update Command

To update the schema with latest changelog discoveries:

```bash
/update-settings-schema              # Full update
/update-settings-schema --dry-run    # Preview changes
/update-settings-schema --validate-only  # Just validate
```

## What This Framework Does NOT Contain

This file intentionally excludes:

- **Specific valid settings options** - Fetch from docs-management
- **Exact permission rule syntax** - Fetch from docs-management
- **Complete schema specification** - Fetch from docs-management
- **Any content that exists in official documentation**

---

**Last Updated:** 2025-12-25
**Architecture:** Query-based audit framework (no duplicated official content)
