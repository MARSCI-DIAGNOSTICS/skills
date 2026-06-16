# Status Line Audit Framework

**Architecture:** This framework provides scoring criteria and query guides. **All validation rules are fetched from official documentation via docs-management skill** - this file contains NO duplicated official content.

## 🚨 MANDATORY: Use docs-management BEFORE Any Finding

> **ABSOLUTE REQUIREMENT - NEVER SKIP THIS STEP:**
>
> Before flagging ANY finding about status line scripts, JSON handling, or output format:
>
> 1. **INVOKE** `docs-management` skill with query: `"status line" "statusLine" "custom status line" example`
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
- [ ] Did I test the script actually works before flagging issues? ← **RUNTIME CHECK MATTERS**

**If you cannot verify against official docs, mark finding as UNVERIFIED and do not deduct points.**

## How Audits Work

1. **Auditor loads** `status-line-customization` skill
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
| Broad Coverage | `statusLine` | General status line docs - start here (most effective query) |
| Script Requirements | `settings statusLine script` | Script requirements (focused) |
| JSON Input | `statusline stdin JSON` | Input format (specific) |
| Output Format | `status line output terminal stdout format` | Output requirements |
| Color Codes | `terminal color ANSI escape codes status` | Color handling |
| Cross-Platform | `cross-platform script bash python node` | Platform support |
| Configuration | `statusLine settings.json configuration path` | Config location |

**Note:** The simple query `statusLine` returns 6 focused results - this is the most effective starting point. Status line has limited docs coverage in the canonical index.

**CRITICAL:** The auditor MUST query docs-management and use the returned official documentation as the source of truth for validation rules.

## 🚨 Required docs-management Queries Per Category

**MANDATORY:** Execute these queries BEFORE scoring each category:

| Category | Required Query | What to Verify |
| --- | --- | --- |
| Broad Coverage | `statusLine` | Start here for general context |
| Script Structure | `settings statusLine script` | Script requirements (focused) |
| JSON Handling | `statusline stdin JSON` | Expected JSON fields |
| Output Format | `status line output terminal stdout format` | Output requirements |
| Cross-Platform | `status line cross-platform bash python node` | Platform support |
| Configuration | `statusLine settings.json configuration path` | Config location |
| Color Support | `terminal color ANSI escape codes status` | Color code handling |

**Query Tip:** Prefer simple queries like `statusLine` over complex multi-word queries. Status line documentation is limited in canonical index - if docs-management returns few results, use `claude-code-guide` subagent for supplemental web search.

### Query Execution Protocol

1. **Before each category** → Run the required query
2. **Read returned docs** → Find the relevant example/table
3. **Compare your finding** → Does it match official docs?
4. **If mismatch** → Your finding is WRONG, not the status line script
5. **If uncertain** → Do NOT deduct points, mark as NEEDS-VERIFICATION

## Extensive Validation Requirements

**CRITICAL:** Before flagging ANY finding, you MUST:

1. **Query docs-management EXTENSIVELY** - Use multiple keyword combinations
2. **Read the FULL official documentation** - Not just snippets
3. **Check for optional vs required fields** - Query: `"optional" "required" {topic}`
4. **Verify default behaviors** - Query: `"default" {topic}`
5. **Distinguish official vs repo-specific rules** - Only official rules are errors; repo-specific are suggestions
6. **Verify platform-specific behaviors** - Query: `"status line" cross-platform Windows Linux macOS`

**If official documentation does not explicitly prohibit something, do NOT flag it as an error.**

**If you cannot find documentation supporting your finding, the finding is INVALID.**

## Audit Scoring Rubric

This scoring rubric is used by the `statusline-auditor` agent for formal audits.

### Category Scores

| Category | Points | Description |
| --- | --- | --- |
| Script Structure | 25 | Valid script, proper shebang, executable |
| JSON Handling | 25 | Correctly parses JSON input structure |
| Output Format | 25 | Proper terminal formatting, colors |
| Cross-Platform | 25 | Works on Windows, macOS, Linux |

The maximum possible score is **Total: 100 points**.

### Scoring Details

**Note:** Pass conditions are validated against official documentation fetched via docs-management. The criteria below describe WHAT to check, not the specific rules (which come from docs).

#### Script Structure (25 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Valid shebang line | 8 | Script analysis |
| Executable permissions | 7 | File permissions check |
| No syntax errors | 10 | Script validation |

#### JSON Handling (25 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Reads stdin correctly | 10 | Script analysis |
| Parses JSON structure | 10 | Query: "status line input structure" |
| Handles missing fields | 5 | Robustness check |

#### Output Format (25 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Outputs to stdout | 8 | Script analysis |
| Valid terminal formatting | 10 | Query: "status line output" |
| Color codes if used | 7 | Query: "terminal color codes" |

#### Cross-Platform (25 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Bash compatibility | 8 | Script portability |
| No OS-specific features | 8 | Platform analysis |
| Fallback handling | 9 | Robustness check |

### Thresholds

| Score Range | Result |
| --- | --- |
| 85-100 | **PASS** |
| 70-84 | **PASS WITH WARNINGS** |
| Below 70 | **FAIL** |

### Automatic Failures

Regardless of score, a status line script **automatically fails** if:

- Script cannot be parsed/validated
- Does not read from stdin
- No output to stdout
- Critical syntax errors

## Status Line Discovery

**Query docs-management:** `"statusLine" "settings.json" "status line configuration"`

Configuration locations come from official documentation. Do NOT hardcode paths - always verify current locations via docs-management.

## Script Language Support

**Query docs-management:** `"status line script" "supported languages" "script requirements"`

Supported script languages and requirements come from official documentation. Verify current requirements before auditing.

## Repository-Specific Standards

These standards are specific to this repository and NOT from official Claude Code documentation:

| Standard | Value | Rationale |
| --- | --- | --- |
| Preferred language | Bash or Python | Cross-platform |
| Color support | Optional with fallback | Terminal compatibility |
| Error handling | Silent fallback | Don't break Claude |

## What This Framework Does NOT Contain

This file intentionally excludes:

- **Specific JSON input structure** - Fetch from docs-management
- **Required output format details** - Fetch from docs-management
- **Terminal color code specifications** - Fetch from docs-management
- **Any content that exists in official documentation**

---

**Last Updated:** 2025-12-25
**Architecture:** Query-based audit framework (no duplicated official content)
**Update:** Added MANDATORY docs-management enforcement section
