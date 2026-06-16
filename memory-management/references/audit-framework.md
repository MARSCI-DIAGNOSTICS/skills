# Memory (CLAUDE.md) Audit Framework

**Architecture:** This framework provides scoring criteria and query guides. **All validation rules are fetched from official documentation via docs-management skill** - this file contains NO duplicated official content.

## 🚨 MANDATORY: Use docs-management BEFORE Any Finding

> **ABSOLUTE REQUIREMENT - NEVER SKIP THIS STEP:**
>
> Before flagging ANY finding about memory file structure, import syntax, or hierarchy:
>
> 1. **INVOKE** `docs-management` skill with query: `"CLAUDE.md" "memory" "import syntax" example`
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
- [ ] Am I applying rules from OTHER components (Skills, Hooks, MCP) to memory files? ← **STOP - WRONG**

**If you cannot verify against official docs, mark finding as UNVERIFIED and do not deduct points.**

## How Audits Work

1. **Auditor loads** `memory-management` skill
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
| Broad Coverage | `CLAUDE.md` | General memory documentation - start here |
| Structure | `CLAUDE.md memory file structure format markdown` | File format requirements |
| Import Syntax | `CLAUDE.md import syntax @path memory imports` | Valid import patterns |
| Hierarchy | `memory enterprise project user` | Memory types and precedence |
| All Memory Types | `memory types enterprise project user local` | Complete memory type reference |
| Content | `CLAUDE.md content memory organization sections` | Content guidelines |
| Memory Command | `/memory command add` | /memory slash command usage |
| Modular Rules | `modular rules .claude/rules` | Rules directory feature |
| File Locations | `CLAUDE.md file locations .claude memory directory` | Valid file paths |

**CRITICAL:** The auditor MUST query docs-management and use the returned official documentation as the source of truth for validation rules.

## 🚨 Required docs-management Queries Per Category

**MANDATORY:** Execute these queries BEFORE scoring each category:

| Category | Required Query | What to Verify |
| --- | --- | --- |
| Broad Coverage | `CLAUDE.md` | Start here for general context |
| Structure | `CLAUDE.md memory file structure format markdown` | File format, section requirements |
| Import Syntax | `CLAUDE.md import syntax @path memory imports example` | Valid import patterns, syntax |
| Hierarchy | `memory enterprise project user` | Precedence rules, file locations |
| All Types | `memory types enterprise project user local` | Complete type reference |
| Memory Command | `/memory command add` | Slash command usage |
| File Locations | `CLAUDE.md file locations .claude memory directory` | Valid file paths |
| Modular Rules | `modular rules .claude/rules` | Rules directory feature |
| Anti-Patterns | `memory circular imports nesting depth` | Import anti-patterns |

### Query Execution Protocol

1. **Before each category** → Run the required query
2. **Read returned docs** → Find the relevant example/table
3. **Compare your finding** → Does it match official docs?
4. **If mismatch** → Your finding is WRONG, not the memory file
5. **If uncertain** → Do NOT deduct points, mark as NEEDS-VERIFICATION

## Audit Scoring Rubric

This scoring rubric is used by the `memory-component-auditor` agent for formal audits.

### Category Scores

| Category | Points | Description |
| --- | --- | --- |
| Structure | 25 | Valid markdown, proper sections |
| Import Syntax | 25 | Correct @path syntax, files exist |
| Hierarchy Compliance | 20 | Correct level (enterprise/project/user) |
| Content Organization | 20 | Progressive disclosure, appropriate size |
| No Anti-Patterns | 10 | No circular imports, excessive nesting |

The maximum possible score is **Total: 100 points**.

### Scoring Details

**Note:** Pass conditions are validated against official documentation fetched via docs-management. The criteria below describe WHAT to check, not the specific rules (which come from docs).

#### Structure (25 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Valid markdown syntax | 10 | Markdown parsing |
| Proper section organization | 10 | Query: "CLAUDE.md structure" |
| Clear headings | 5 | Analysis: readability |

#### Import Syntax (25 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Valid @path syntax | 10 | Query: "import syntax", "@path import" |
| Referenced files exist | 10 | File system check |
| Relative paths resolve | 5 | Path resolution check |

#### Hierarchy Compliance (20 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Correct file location | 10 | Query: "memory hierarchy" |
| Appropriate scope content | 10 | Analysis: content matches level |

#### Content Organization (20 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Progressive disclosure used | 8 | Query: "progressive disclosure" |
| Appropriate file size | 7 | Query: "memory size" guidelines |
| Focused content | 5 | Analysis: not too broad |

#### No Anti-Patterns (10 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| No circular imports | 5 | Dependency graph analysis |
| No excessive nesting | 3 | Import depth check |
| No duplicate content | 2 | Content analysis |

### Thresholds

| Score Range | Result |
| --- | --- |
| 85-100 | **PASS** |
| 70-84 | **PASS WITH WARNINGS** |
| Below 70 | **FAIL** |

### Automatic Failures

Regardless of score, a memory file **automatically fails** if:

- Circular import chain detected
- References non-existent files
- Invalid markdown syntax that prevents parsing
- Excessive size without progressive disclosure (>500 lines with no imports)

## Memory File Discovery

**Query docs-management:** `"CLAUDE.md" "memory file locations" "memory hierarchy"`

File locations and hierarchy precedence come from official documentation. Do NOT hardcode paths - always verify current locations via docs-management.

## Memory Hierarchy

**Query docs-management:** `"memory hierarchy" "enterprise project user" precedence`

Precedence rules come from official documentation. Always fetch current hierarchy before auditing.

## Repository-Specific Standards

These standards are specific to this repository and NOT from official Claude Code documentation:

| Standard | Value | Rationale |
| --- | --- | --- |
| Root CLAUDE.md size | < 100 lines with imports | Progressive disclosure |
| Import depth | Max 3 levels | Maintainability |
| Memory file size | < 500 lines each | Context efficiency |
| Token estimates | Document in imports | Budget awareness |

### Token Budget Analysis (included by default)

Token budget analysis is included in the default audit. Use `--token-budget` to run ONLY token analysis (skip full audit).

#### Official Guidance vs Repo-Specific Thresholds

**Official Claude Code docs** recommend keeping memory "concise and focused" with progressive disclosure. They do NOT specify exact token limits.

**Repo-specific thresholds** (this repository's standards, not from official docs):

| Status | Token Range | Guidance |
| --- | --- | --- |
| PASS | ≤12,000 tokens | Within repo budget |
| WARN | 12,001-15,000 tokens | At upper limit, monitor |
| FAIL | >15,000 tokens | Over budget, remediation needed |

These thresholds are calibrated for this repository's memory architecture. Other repos may need different values.

#### Token Estimation Methodology

- **Formula:** `characters / 4` (approximate for English markdown)
- **Scope:** Only always-loaded files (marked "Always-loaded" in CLAUDE.md or @-imported with no on-demand indicators)
- **Excludes:** On-demand/context-dependent files that load selectively

#### Declared vs Actual Tolerance

Files with Token Budget headers (e.g., `**Token Budget:** ~1,800 tokens`) are validated:

- **Acceptable variance:** ±20%
- **Flagged for review:** >20% variance between declared and actual

#### Remediation Guidance

When over budget, invoke `memory-management` skill for official progressive disclosure guidance. General recommendations:

1. **Move to on-demand:** Files not needed every session can use context-dependent loading
2. **Split large files:** Files >2,000 tokens should use hub pattern (hub + child imports)
3. **Review necessity:** Some always-loaded content may be obsolete or redundant

## Anti-Pattern Detection

### Circular Import Detection

Build import graph and check for cycles:

```text
CLAUDE.md -> memory/a.md -> memory/b.md -> CLAUDE.md  [CYCLE!]
```

### Excessive Nesting

```text
CLAUDE.md
  -> memory/level1.md
    -> memory/level2.md
      -> memory/level3.md
        -> memory/level4.md  [TOO DEEP!]
```

## What This Framework Does NOT Contain

This file intentionally excludes:

- **Specific import syntax rules** - Fetch from docs-management
- **Exact size limits** - Fetch from docs-management
- **Memory hierarchy details** - Fetch from docs-management
- **Any content that exists in official documentation**

## Extensive Validation Requirements

**CRITICAL:** Before flagging ANY finding, you MUST:

1. **Query docs-management EXTENSIVELY** - Use multiple keyword combinations
2. **Read the FULL official documentation** - Not just snippets
3. **Check for optional vs required fields** - Query: `"optional" "required" {topic}`
4. **Verify default behaviors** - Query: `"default" {topic}`
5. **Distinguish official vs repo-specific rules** - Only official rules are errors; repo-specific are suggestions
6. **Verify component scope** - Query: `"memory" "CLAUDE.md"` to confirm rules apply to memory files specifically

**If official documentation does not explicitly prohibit something, do NOT flag it as an error.**

**If you cannot find documentation supporting your finding, the finding is INVALID.**

## Citation Requirements for Audit Findings

**Every audit finding MUST include a citation.** Findings without citations are invalid.

### Required Citation Format

```markdown
### Finding: [Issue description]

**Source:** [One of the following]
- `doc_id: [id]` - From docs-management query
- `repo-specific: audit-framework.md` - Repository-specific standard
- `analysis: [type]` - Technical analysis (circular imports, file existence)

**Rule:** [Exact quote or description of the rule being applied]
**Violation:** [How this specific file violates the rule]
```

### Valid Citation Sources

| Source Type | Example | When to Use |
| --- | --- | --- |
| Official docs | `doc_id: memory-hierarchy` | Rules from Claude Code documentation |
| Repo-specific | `repo-specific: audit-framework.md` | Standards specific to this repository |
| Technical analysis | `analysis: circular-import-detection` | Factual checks (file exists, syntax valid) |

### Invalid Citations

These are NOT valid citation sources:

- "Common sense" or "best practice" without documentation
- Rules from Skills/Hooks/MCP documentation applied to memory files
- Inferred rules that aren't explicitly documented
- "Security concern" without specific documented rule

**If you cannot cite a source, the finding is invalid and must be removed.**

---

**Last Updated:** 2026-01-17
**Architecture:** Query-based audit framework (no duplicated official content)
