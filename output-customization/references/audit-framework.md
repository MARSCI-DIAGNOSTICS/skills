# Output Style Audit Framework

**Architecture:** This framework provides scoring criteria and query guides. **All validation rules are fetched from official documentation via docs-management skill** - this file contains NO duplicated official content.

## 🚨 MANDATORY: Use docs-management BEFORE Any Finding

> **ABSOLUTE REQUIREMENT - NEVER SKIP THIS STEP:**
>
> Before flagging ANY finding about output style structure, frontmatter, or content:
>
> 1. **INVOKE** `docs-management` skill with query: `"output styles" "output-styles" "output style frontmatter" example`
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
- [ ] Am I confusing output styles with other components (Skills, Commands)? ← **DIFFERENT REQUIREMENTS**

**If you cannot verify against official docs, mark finding as UNVERIFIED and do not deduct points.**

## How Audits Work

1. **Auditor loads** `output-customization` skill
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
| Broad Coverage | `output styles` | General output styles documentation - start here |
| File Structure | `output styles output-styles directory location .claude` | Valid locations |
| Frontmatter | `output style frontmatter name description YAML` | Required fields |
| Content | `output style content instructions markdown body` | Content requirements |
| Switching | `output-style switching command setting` | Compatibility rules |
| Built-in Styles | `built-in output styles Default Explanatory Learning` | What to avoid duplicating |
| Configuration | `outputStyle settings.json configuration` | Config options |

**CRITICAL:** The auditor MUST query docs-management and use the returned official documentation as the source of truth for validation rules.

## 🚨 Required docs-management Queries Per Category

**MANDATORY:** Execute these queries BEFORE scoring each category:

| Category | Required Query | What to Verify |
| --- | --- | --- |
| Broad Coverage | `output styles` | Start here for general context |
| File Structure | `output styles output-styles directory location .claude` | Valid file locations, naming |
| Frontmatter | `output style frontmatter name description YAML required` | Required vs optional fields |
| Content | `output style content instructions markdown body` | Content structure requirements |
| Compatibility | `built-in output styles Default Explanatory Learning` | Built-in style names to avoid |
| Configuration | `outputStyle settings.json configuration option` | Config options |
| Switching | `output-style command switching selection` | Style selection syntax |

### Query Execution Protocol

1. **Before each category** → Run the required query
2. **Read returned docs** → Find the relevant example/table
3. **Compare your finding** → Does it match official docs?
4. **If mismatch** → Your finding is WRONG, not the output style
5. **If uncertain** → Do NOT deduct points, mark as NEEDS-VERIFICATION

## Extensive Validation Requirements

**CRITICAL:** Before flagging ANY finding, you MUST:

1. **Query docs-management EXTENSIVELY** - Use multiple keyword combinations
2. **Read the FULL official documentation** - Not just snippets
3. **Check for optional vs required fields** - Query: `"optional" "required" {topic}`
4. **Verify default behaviors** - Query: `"default" {topic}`
5. **Distinguish official vs repo-specific rules** - Only official rules are errors; repo-specific are suggestions
6. **Check built-in style names** - Query: `"built-in output styles" names list`

**If official documentation does not explicitly prohibit something, do NOT flag it as an error.**

**If you cannot find documentation supporting your finding, the finding is INVALID.**

## Audit Scoring Rubric

This scoring rubric is used by the `output-style-auditor` agent for formal audits.

### Category Scores

| Category | Points | Description |
| --- | --- | --- |
| File Structure | 20 | Correct location, .md extension |
| YAML Frontmatter | 30 | Required fields present and valid |
| Content Quality | 30 | Clear instructions, proper structure |
| Compatibility | 20 | Works with style switching, no conflicts |

The maximum possible score is **Total: 100 points**.

### Scoring Details

**Note:** Pass conditions are validated against official documentation fetched via docs-management. The criteria below describe WHAT to check, not the specific rules (which come from docs).

#### File Structure (20 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Correct directory | 10 | Query: "output-styles directory" |
| .md file extension | 5 | Convention check |
| Kebab-case filename | 5 | Convention check |

#### YAML Frontmatter (30 points)

**Note:** Per official documentation, ALL frontmatter fields are OPTIONAL:

- `name` - optional (defaults to filename)
- `description` - optional
- `keep-coding-instructions` - optional (defaults to `false`)

Do NOT deduct points for missing optional fields. Score based on quality when fields ARE present.

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Valid YAML syntax (if frontmatter present) | 10 | Syntax check |
| Well-formed `name` (if present) | 8 | Clarity and conciseness |
| Clear `description` (if present) | 8 | Useful for style selection menu |
| Appropriate `keep-coding-instructions` | 4 | Matches style purpose (coding vs non-coding) |

#### Content Quality (30 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Clear instructions | 12 | Analysis: readability |
| Actionable guidance | 10 | Analysis: Claude can follow |
| Appropriate length | 8 | Query: "output style content" guidelines |

#### Compatibility (20 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| No built-in style conflicts | 10 | Query: "built-in output styles" |
| Works with /output-style | 10 | Query: "style switching" |

### Thresholds

| Score Range | Result |
| --- | --- |
| 85-100 | **PASS** |
| 70-84 | **PASS WITH WARNINGS** |
| Below 70 | **FAIL** |

### Automatic Failures

Regardless of score, an output style **automatically fails** if:

- Invalid YAML frontmatter syntax (when frontmatter is present)
- Empty content (no instructions after frontmatter)
- Not a markdown file

**Note:** Missing frontmatter fields are NOT automatic failures. Per official documentation, all frontmatter fields (`name`, `description`, `keep-coding-instructions`) are optional with sensible defaults.

## Output Style Discovery

**Query docs-management:** `"output-styles" "file locations" "output style directory"`

File locations come from official documentation. Do NOT hardcode paths - always verify current locations via docs-management.

## Repository-Specific Standards

These standards are specific to this repository and NOT from official Claude Code documentation:

| Standard | Value | Rationale |
| --- | --- | --- |
| Filename convention | kebab-case | Consistency |
| Description length | 1-2 sentences | Clarity in style list |
| Content organization | Sections with headers | Readability |

## What This Framework Does NOT Contain

This file intentionally excludes:

- **Specific frontmatter field requirements** - Fetch from docs-management
- **Built-in style names** - Fetch from docs-management
- **Exact content guidelines** - Fetch from docs-management
- **Any content that exists in official documentation**

---

**Last Updated:** 2026-01-12
**Architecture:** Query-based audit framework (no duplicated official content)
**Update:** Fixed false positive scoring - all frontmatter fields are optional per official docs (2026-01-12)
