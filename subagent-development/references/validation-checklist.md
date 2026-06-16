# Subagent/Agent Audit Framework

**Architecture:** This framework provides scoring criteria and query guides. **All validation rules are fetched from official documentation via docs-management skill** - this file contains NO duplicated official content.

## 🚨 MANDATORY: Use docs-management BEFORE Any Finding

> **ABSOLUTE REQUIREMENT - NEVER SKIP THIS STEP:**
>
> Before flagging ANY finding about agent structure, frontmatter, or field requirements:
>
> 1. **INVOKE** `docs-management` skill with query: `"agents" "subagent" "agent frontmatter" example`
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
- [ ] Did I check `undocumented-features.md` for fields like `color`? ← **NOT ALL FIELDS ARE IN OFFICIAL DOCS**

**If you cannot verify against official docs, mark finding as UNVERIFIED and do not deduct points.**

## Table of Contents

- [How Audits Work](#how-audits-work)
- [Documentation Query Guide](#documentation-query-guide)
- [Undocumented Features](#undocumented-features)
- [Audit Scoring Rubric](#audit-scoring-rubric)
  - [Category Scores](#category-scores)
  - [Thresholds](#thresholds)
- [Repository-Specific Standards](#repository-specific-standards)
- [What This Framework Does NOT Contain](#what-this-framework-does-not-contain)

## How Audits Work

1. **Auditor loads** `subagent-development` skill
2. **Skill delegates** to `docs-management` for official rules
3. **Official docs provide** the actual validation criteria
4. **This framework provides** scoring weights and thresholds
5. **Undocumented features** checked via `references/undocumented-features.md`

## Documentation Query Guide

Before auditing, query `docs-management` skill for these topics:

| Category | Query Keywords | What to Fetch |
| --- | --- | --- |
| Broad Coverage | `subagents agents` | General agent documentation - start here |
| Name Field | `agent name subagent name requirements characters` | Character restrictions, length limits, reserved words |
| Description Field | `agent description automatic delegation triggers` | Description requirements, delegation triggers |
| Tools Configuration | `agent tools allowed-tools subagent specification` | Tool specification format, inheritance |
| Model Selection | `agent model selection inherit sonnet haiku opus` | Valid model values, when to use each |
| File Locations | `agent file locations .claude/agents directory` | Valid directories, priority resolution |
| Optional Fields | `agent YAML frontmatter configuration fields optional` | All valid frontmatter fields |
| Color Field | `agent color frontmatter undocumented features` | Color configuration (undocumented) |
| Skills Field | `agent skills skill-loading subagent` | Skill auto-loading patterns |

**CRITICAL:** The auditor MUST query docs-management and use the returned official documentation as the source of truth for validation rules.

## 🚨 Required docs-management Queries Per Category

**MANDATORY:** Execute these queries BEFORE scoring each category:

| Category | Required Query | What to Verify |
| --- | --- | --- |
| Broad Coverage | `subagents agents` | Start here for general context |
| Name Field | `agent name subagent name requirements characters limits` | Character limits, restrictions |
| Description | `agent description delegation triggers automatic proactive` | Description requirements |
| Tools | `agent tools tools field configuration specification` | Tool specification syntax |
| Model | `agent model selection inherit sonnet haiku opus` | Valid model values |
| File Location | `agent file .claude/agents directory location plugins` | Valid file locations |
| Undocumented | Check `references/undocumented-features.md` | Color, skills, permissionMode |

### Query Execution Protocol

1. **Before each category** → Run the required query
2. **Read returned docs** → Find the relevant example/table
3. **Compare your finding** → Does it match official docs?
4. **If mismatch** → Your finding is WRONG, not the agent
5. **If uncertain** → Do NOT deduct points, mark as NEEDS-VERIFICATION

## Extensive Validation Requirements

**CRITICAL:** Before flagging ANY finding, you MUST:

1. **Query docs-management EXTENSIVELY** - Use multiple keyword combinations
2. **Read the FULL official documentation** - Not just snippets
3. **Check for optional vs required fields** - Query: `"optional" "required" {topic}`
4. **Verify default behaviors** - Query: `"default" {topic}`
5. **Distinguish official vs repo-specific rules** - Only official rules are errors; repo-specific are suggestions
6. **Check undocumented features** - Query `references/undocumented-features.md` for fields like `color`

**If official documentation does not explicitly prohibit something, do NOT flag it as an error.**

**If you cannot find documentation supporting your finding, the finding is INVALID.**

## Undocumented Features

For features NOT in official docs (color, permissionMode details, skills field), see:

- `references/undocumented-features.md`

These are validated separately from official documentation.

## Audit Scoring Rubric

This scoring rubric is used by the `agent-auditor` agent for formal audits.

### Category Scores

| Category | Points | Description |
| --- | --- | --- |
| Name Field | 20 | Lowercase, hyphens, max 64 chars, no reserved words |
| Description Field | 25 | Third person, delegation triggers, when-to-use guidance |
| Tools Configuration | 20 | Appropriate restrictions, not over/under restricted |
| Model Selection | 15 | Appropriate for task complexity (haiku/sonnet/opus/inherit) |
| Additional Fields | 20 | Color, skills, permissionMode correctly configured |

The maximum possible score is **Total: 100 points**.

### Scoring Details

**Note:** Pass conditions are validated against official documentation fetched via docs-management. The criteria below describe WHAT to check, not the specific rules (which come from docs).

#### Name Field (20 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Character restrictions | 6 | Query: "agent name", "subagent name requirements" |
| Valid characters | 4 | Query: "agent name", "subagent name requirements" |
| Length limit | 4 | Query: "agent name", "subagent name requirements" |
| No reserved words | 6 | Query: "agent name", "reserved words" |

#### Description Field (25 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Present and non-empty | 5 | Query: "agent description", "required fields" |
| Third person voice | 5 | Repository standard: no "I" or "You" |
| Delegation triggers | 8 | Query: "automatic delegation", "agent description" |
| When-to-use guidance | 7 | Repository standard: clear usage scenarios |

#### Tools Configuration (20 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Tools specified | 5 | Query: "agent tools", "tools field" |
| Not over-restricted | 8 | Analysis: tools match stated purpose |
| Not under-restricted | 7 | Analysis: excludes unnecessary tools |

#### Model Selection (15 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Model specified | 5 | Query: "agent model selection" |
| Appropriate selection | 10 | Repository standard (see below) |

**Model Selection Guidance (Repository Standard):**

- `haiku`: Simple tasks, parallel audits, search/lookup, low-latency needs
- `sonnet`: Complex reasoning, code analysis, multi-step workflows
- `opus`: Critical decisions, comprehensive analysis, highest capability needs
- `inherit`: Use parent conversation's model (default if unspecified)

#### Additional Fields (20 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Color (if used) | 8 | Undocumented: see `references/undocumented-features.md` |
| Skills (if used) | 6 | Undocumented: see `references/undocumented-features.md` |
| PermissionMode (if used) | 6 | Undocumented: see `references/undocumented-features.md` |

### Thresholds

| Score Range | Result |
| --- | --- |
| 85-100 | **PASS** |
| 70-84 | **PASS WITH WARNINGS** |
| Below 70 | **FAIL** |

### Automatic Failures

Regardless of score, an agent **automatically fails** if:

- Missing required fields - Query docs-management to verify which are required
- Name violates official requirements - Query docs-management for name rules
- File is empty or malformed YAML - Repository policy

## Repository-Specific Standards

These standards are specific to this repository and NOT from official Claude Code documentation:

| Standard | Value | Rationale |
| --- | --- | --- |
| Third person descriptions | No "I" or "You" | Consistency, delegation clarity |
| Model selection guidance | haiku/sonnet/opus mapping | Performance/cost optimization |
| Color assignments | Semantic categories | Visual consistency |
| When-to-use in description | Clear usage scenarios | Effective auto-delegation |

## What This Framework Does NOT Contain

This file intentionally excludes:

- **Specific name character rules** - Fetch from docs-management
- **Exact field requirements** - Fetch from docs-management
- **Precise syntax specifications** - Fetch from docs-management
- **Any content that exists in official documentation**

The authoritative source for all validation rules is official Claude Code documentation accessed via the docs-management skill.

For undocumented features (color, permissionMode, skills), see `references/undocumented-features.md`.

---

**Last Updated:** 2025-12-25
**Architecture:** Query-based audit framework (no duplicated official content)
**Update:** Added MANDATORY docs-management enforcement section
