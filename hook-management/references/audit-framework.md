# Hook Audit Framework

**Architecture:** This framework provides scoring criteria and query guides. **All validation rules are fetched from official documentation via docs-management skill** - this file contains NO duplicated official content.

## 🚨 MANDATORY: Use docs-management BEFORE Any Finding

> **ABSOLUTE REQUIREMENT - NEVER SKIP THIS STEP:**
>
> Before flagging ANY finding about hook events, configuration, matchers, or decision control:
>
> 1. **INVOKE** `docs-management` skill with query: `"hooks" "hook events" "hooks.json" example`
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
- [ ] If official docs show a pattern, am I suggesting something different? ← **CHECK THIS**

**If you cannot verify against official docs, mark finding as UNVERIFIED and do not deduct points.**

## How Audits Work

1. **Auditor loads** `hook-management` skill
2. **Skill delegates** to `docs-management` for official rules
3. **Official docs provide** the actual validation criteria
4. **This framework provides** scoring weights and thresholds

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
| Broad Coverage | `hooks` | General hooks documentation - start here |
| Hook Events | `hook events PreToolUse PostToolUse SessionStart` | Valid event types, timing |
| Configuration | `hooks configuration hooks.json schema structure` | Required fields, structure |
| Matchers | `hook matchers tool matchers pattern regex` | Matcher syntax and patterns |
| Decision Control | `hooks reference exit code decision approve block` | Valid decision values |
| Exit Codes | `hook exit codes return values command` | Exit code meanings |
| Environment | `hook environment variables CLAUDE_PROJECT_DIR` | Available variables |
| Prompt Hooks | `prompt hooks LLM evaluation type prompt` | Prompt-based hook configuration |
| Security | `hooks security considerations best practices` | Security guidelines |

**CRITICAL:** The auditor MUST query docs-management and use the returned official documentation as the source of truth for validation rules.

## 🚨 Required docs-management Queries Per Category

**MANDATORY:** Execute these queries BEFORE scoring each category:

| Category | Required Query | What to Verify |
| --- | --- | --- |
| Broad Coverage | `hooks` | Start here for general context |
| Configuration | `hooks configuration hooks.json schema structure` | Valid structure, required fields |
| Hook Events | `hook events PreToolUse PostToolUse SessionStart Notification` | Valid event types list |
| Matchers | `hook matchers tool matchers pattern regex` | Matcher syntax and examples |
| Decision Control | `hooks reference exit code decision approve block` | Valid decision values |
| Exit Codes | `hooks reference exit code decision` | Exit code meanings |
| Prompt Hooks | `prompt hooks type prompt LLM evaluation` | Prompt-based hook syntax |
| Hook Locations | `hooks hooks.json hook file locations plugin hooks` | Valid file locations |

### Query Execution Protocol

1. **Before each category** → Run the required query
2. **Read returned docs** → Find the relevant example/table
3. **Compare your finding** → Does it match official docs?
4. **If mismatch** → Your finding is WRONG, not the hook config
5. **If uncertain** → Do NOT deduct points, mark as NEEDS-VERIFICATION

## Extensive Validation Requirements

**CRITICAL:** Before flagging ANY finding, you MUST:

1. **Query docs-management EXTENSIVELY** - Use multiple keyword combinations
2. **Read the FULL official documentation** - Not just snippets
3. **Check for optional vs required fields** - Query: `"optional" "required" {topic}`
4. **Verify default behaviors** - Query: `"default" {topic}`
5. **Distinguish official vs repo-specific rules** - Only official rules are errors; repo-specific are suggestions
6. **Verify hook event types and matchers** - Query: `"hook events" "matchers" syntax patterns`

**If official documentation does not explicitly prohibit something, do NOT flag it as an error.**

**If you cannot find documentation supporting your finding, the finding is INVALID.**

## Audit Scoring Rubric

This scoring rubric is used by the `hook-auditor` agent for formal audits.

### Category Scores

| Category | Points | Description |
| --- | --- | --- |
| Configuration Structure | 25 | Valid hooks.json, required fields present, valid event types |
| Hook Scripts | 20 | Scripts exist, proper structure, correct exit codes |
| Matchers | 20 | Appropriate tool/path matchers, not over/under matching |
| Environment Variables | 15 | Follows naming convention, documented, properly used |
| Testing | 20 | Has tests, tests pass, adequate coverage |

The maximum possible score is **Total: 100 points**.

### Scoring Details

**Note:** Pass conditions are validated against official documentation fetched via docs-management. The criteria below describe WHAT to check, not the specific rules (which come from docs).

#### Configuration Structure (25 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Valid hooks.json syntax | 8 | Query: "hooks configuration", "hooks.json" |
| Required fields present | 7 | Query: "hooks.json schema", "required fields" |
| Valid event types | 5 | Query: "hook events", "PreToolUse PostToolUse" |
| Command paths valid | 5 | File system check: scripts exist |

#### Hook Scripts (20 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Script exists | 5 | File system check |
| Proper shebang/structure | 5 | Repository standard: bash/python/node |
| Correct exit codes | 5 | Query: "hook exit codes" |
| JSON output format | 5 | Query: "hook JSON output schema" |

#### Matchers (20 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Valid matcher syntax | 8 | Query: "hook matchers", "tool matchers" |
| Not over-matching | 6 | Analysis: matchers appropriate for purpose |
| Not under-matching | 6 | Analysis: catches intended cases |

#### Environment Variables (15 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Follows naming convention | 8 | Repository standard: `CLAUDE_HOOK_{NAME}_ENABLED` |
| Variables documented | 4 | Repository standard: README or hook.yaml |
| Proper defaults | 3 | Repository standard: sensible defaults |

#### Testing (20 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Tests exist | 8 | File system check: tests/ directory |
| Tests pass | 7 | Execution check: run tests |
| Adequate coverage | 5 | Analysis: key scenarios covered |

### Thresholds

| Score Range | Result |
| --- | --- |
| 85-100 | **PASS** |
| 70-84 | **PASS WITH WARNINGS** |
| Below 70 | **FAIL** |

### Automatic Failures

Regardless of score, a hook **automatically fails** if:

- hooks.json is invalid JSON - Syntax error
- Referenced scripts don't exist - Broken configuration
- Uses invalid event types - Query docs-management to verify

## Repository-Specific Standards

These standards are specific to this repository and NOT from official Claude Code documentation:

| Standard | Value | Rationale |
| --- | --- | --- |
| Environment variable naming | `CLAUDE_HOOK_{NAME}_ENABLED` | Consistency across hooks |
| Script languages | Bash, Python, Node.js | Supported in shared utilities |
| Test location | `tests/` subdirectory | Vertical slice organization |
| Config file | `config.yaml` per hook | Externalized configuration |

## Hook Discovery Patterns

**Query docs-management:** `"hooks" "hooks.json" "hook file locations" "plugin hooks"`

Hook file locations come from official documentation. Do NOT hardcode paths - always verify current locations via docs-management.

## What This Framework Does NOT Contain

This file intentionally excludes:

- **Specific event type lists** - Fetch from docs-management
- **Exact matcher syntax** - Fetch from docs-management
- **Precise exit code meanings** - Fetch from docs-management
- **Any content that exists in official documentation**

The authoritative source for all validation rules is official Claude Code documentation accessed via the docs-management skill.

---

**Last Updated:** 2025-12-25
**Architecture:** Query-based audit framework (no duplicated official content)
