# Skill Audit Framework

**Architecture:** This framework provides scoring criteria and query guides. **All validation rules are fetched from official documentation via docs-management skill** - this file contains NO duplicated official content.

## MANDATORY: Use docs-management BEFORE Any Finding

> **ABSOLUTE REQUIREMENT - NEVER SKIP THIS STEP:**
>
> Before flagging ANY finding about skill structure, frontmatter, or tool configuration:
>
> 1. **INVOKE** `docs-management` skill with query: `"skills" "skill frontmatter" "allowed-tools" example`
> 2. **READ** the official documentation examples
> 3. **VERIFY** your finding matches what official docs show
> 4. **IF UNCERTAIN** -> Do NOT flag. Ask for clarification instead.
>
> **Flagging findings without verifying against official docs = AUDIT FAILURE**

### Verification Checkpoint

Before including ANY finding in your audit report:

- [ ] Did I invoke docs-management for this topic?
- [ ] Did I read the official example/schema?
- [ ] Does my finding contradict official documentation?

**If you cannot verify against official docs, mark finding as UNVERIFIED and do not deduct points.**

## Table of Contents

- [How Audits Work](#how-audits-work)
- [Documentation Query Guide](#documentation-query-guide)
- [Audit Scoring Rubric](#audit-scoring-rubric)
  - [Category Scores](#category-scores)
  - [Thresholds](#thresholds)
- [Repository-Specific Standards](#repository-specific-standards)
- [What This Framework Does NOT Contain](#what-this-framework-does-not-contain)

## How Audits Work

1. **Auditor loads** `skill-development` skill
2. **Skill delegates** to `docs-management` for official rules
3. **Official docs provide** the actual validation criteria
4. **This framework provides** scoring weights and thresholds

## Documentation Query Guide

Before auditing, query `docs-management` skill for these topics:

| Category | Query Keywords | What to Fetch |
| --- | --- | --- |
| Broad Coverage | `skills` | General skill documentation - start here |
| File Structure | `skills SKILL.md directory structure` | Valid directories, file requirements |
| YAML Frontmatter | `skill frontmatter description allowed-tools YAML` | Required/optional fields, valid values |
| Description | `skill description discovery` | Description requirements and best practices |
| Tool Configuration | `allowed-tools skills permissions tool restrictions` | How to restrict tools, valid tool names |
| Keywords | `skill keywords discoverability` | Keyword coverage and patterns |
| Progressive Disclosure | `progressive disclosure references token efficiency` | Content loading patterns |

**CRITICAL:** The auditor MUST query docs-management and use the returned official documentation as the source of truth for validation rules.

## Required docs-management Queries Per Category

**MANDATORY:** Execute these queries BEFORE scoring each category:

| Category | Required Query | What to Verify |
| --- | --- | --- |
| Broad Coverage | `skills` | Start here for general context |
| File Structure | `skills SKILL.md directory structure` | Valid file locations |
| Frontmatter | `skill frontmatter description allowed-tools YAML required` | Required vs optional fields |
| Description | `skill description discovery` | Description requirements |
| Tool Config | `allowed-tools skills permissions tool restrictions valid` | Tool restriction syntax |
| Keywords | `skill keywords discoverability coverage` | Keyword patterns |
| Progressive Disclosure | `progressive disclosure references token efficiency` | Content loading patterns |

### Query Execution Protocol

1. **Before each category** -> Run the required query
2. **Read returned docs** -> Find the relevant example/table
3. **Compare your finding** -> Does it match official docs?
4. **If mismatch** -> Your finding is WRONG, not the skill
5. **If uncertain** -> Do NOT deduct points, mark as NEEDS-VERIFICATION

## Extensive Validation Requirements

**CRITICAL:** Before flagging ANY finding, you MUST:

1. **Query docs-management EXTENSIVELY** - Use multiple keyword combinations
2. **Read the FULL official documentation** - Not just snippets
3. **Check for optional vs required fields** - Query: `"optional" "required" {topic}`
4. **Verify default behaviors** - Query: `"default" {topic}`
5. **Distinguish official vs repo-specific rules** - Only official rules are errors; repo-specific are suggestions

**If official documentation does not explicitly prohibit something, do NOT flag it as an error.**

**If you cannot find documentation supporting your finding, the finding is INVALID.**

## Audit Scoring Rubric

This scoring rubric is used by the `skill-auditor` agent for formal skill audits.

### Category Scores

| Category | Points | Description |
| --- | --- | --- |
| YAML Frontmatter | 20 | Correct structure, required fields present and valid |
| Delegation Pattern | 20 | Proper docs-management delegation, no hardcoded rules |
| Keywords Coverage | 20 | Discoverable keywords, comprehensive coverage |
| Progressive Disclosure | 20 | Token-efficient loading, on-demand content |
| Maintainability | 20 | Clear structure, good organization, easy to update |

The maximum possible score is **Total: 100 points**.

### Thresholds

| Score Range | Result |
| --- | --- |
| 85-100 | **PASS** |
| 70-84 | **PASS WITH WARNINGS** |
| Below 70 | **FAIL** |

### Automatic Failures

Regardless of score, a skill **automatically fails** if:

- No frontmatter AND no description (undiscoverable) - Repository policy
- File is empty or only contains frontmatter - Repository policy

## Repository-Specific Standards

These standards are specific to this repository and NOT from official Claude Code documentation:

| Standard | Value | Rationale |
| --- | --- | --- |
| Description length | Under 100 words | Conciseness for discoverability |
| Naming convention | Noun-phrase kebab-case | Consistency with skill naming |
| Structure | Clear sections | Maintainability |

## What This Framework Does NOT Contain

This file intentionally excludes:

- **Specific YAML field requirements** - Fetch from docs-management
- **Exact naming rules** - Fetch from docs-management
- **Precise syntax requirements** - Fetch from docs-management
- **Any content that exists in official documentation**

The authoritative source for all validation rules is official Claude Code documentation accessed via the docs-management skill.

---

**Last Updated:** 2026-02-15
**Architecture:** Query-based audit framework (no duplicated official content)
**Migrated from:** slash-commands/command-validation-checklist.md (commands-to-skills migration)
