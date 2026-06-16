# Skill Validation Checklist

**Architecture:** This checklist provides validation criteria. **All validation rules MUST be verified via docs-management skill** - this file contains curated summaries, not the authoritative source.

## 🚨 MANDATORY: Use docs-management BEFORE Any Finding

> **ABSOLUTE REQUIREMENT - NEVER SKIP THIS STEP:**
>
> Before flagging ANY finding about skill structure, frontmatter, or naming:
>
> 1. **INVOKE** `docs-management` skill with query: `"skills" "SKILL.md" "skill frontmatter" example`
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
- [ ] Am I confusing Skills with Commands? ← **DIFFERENT YAML REQUIREMENTS** (`allowed-tools` for Skills, not Commands)

**If you cannot verify against official docs, mark finding as UNVERIFIED and do not deduct points.**

## 🚨 Required docs-management Queries

**MANDATORY:** Execute these queries BEFORE validating each area:

| Topic | Required Query | What to Verify |
| --- | --- | --- |
| Broad Coverage | `skills` | General skills documentation - start here |
| Frontmatter | `skill frontmatter name description allowed-tools YAML` | Required fields, limits |
| Naming | `skill naming convention pattern kebab lowercase` | Valid patterns |
| Structure | `SKILL.md structure body references progressive` | File organization |
| Best Practices | `skill best practices progressive disclosure token` | Recommended patterns |
| vs Commands | `skills commands differences frontmatter allowed-tools` | Skill/command distinctions |
| Tool Access | `skill allowed-tools tool access permissions` | Tool restriction patterns |

### Query Execution Protocol

1. **Before each validation** → Run the required query
2. **Read returned docs** → Find the relevant example/table
3. **Compare against checklist** → Verify rules match official docs
4. **If mismatch** → Trust official docs, not this checklist
5. **If uncertain** → Do NOT flag, mark as NEEDS-VERIFICATION

## Extensive Validation Requirements

**CRITICAL:** Before flagging ANY finding, you MUST:

1. **Query docs-management EXTENSIVELY** - Use multiple keyword combinations
2. **Read the FULL official documentation** - Not just snippets
3. **Check for optional vs required fields** - Query: `"optional" "required" {topic}`
4. **Verify default behaviors** - Query: `"default" {topic}`
5. **Distinguish official vs repo-specific rules** - Only official rules are errors; repo-specific are suggestions
6. **Verify skill vs command distinctions** - Query: `"skills" "commands" differences frontmatter`

**If official documentation does not explicitly prohibit something, do NOT flag it as an error.**

**If you cannot find documentation supporting your finding, the finding is INVALID.**

---

**Source:** Official Claude Code documentation (platform.claude.com, code.claude.com)

Use this checklist before creating or renaming skills. All rules are extracted from official documentation.

## YAML Frontmatter Requirements

### `name` Field (Required)

- [ ] **Maximum 64 characters**
- [ ] **Lowercase letters, numbers, and hyphens only** (no uppercase, no spaces)
- [ ] **No XML tags** in the name
- [ ] **No reserved words:** Cannot contain "anthropic" or "claude"
- [ ] **Non-empty**

**Valid examples:**

- `processing-pdfs`
- `analyzing-spreadsheets`
- `managing-databases`
- `skill-development`

**Invalid examples:**

- `Processing-PDFs` (uppercase letters)
- `claude-helper` (reserved word "claude")
- `anthropic-docs` (reserved word "anthropic")
- `my skill name` (spaces)
- `helper` (too vague per best practices)

### `description` Field (Required)

- [ ] **Non-empty**
- [ ] **Maximum 1024 characters**
- [ ] **No XML tags**
- [ ] **Written in third person** (not "I can help" or "You can use")
- [ ] **Describes what the Skill does AND when to use it**
- [ ] **Includes specific triggers/contexts**

**Good example:**

```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Bad examples:**

```yaml
description: Helps with documents  # Too vague
description: I can process PDFs for you  # First person
description: You can use this to extract text  # Second person
```

## Naming Convention Consistency

Per official documentation:

- [ ] **Gerund form recommended:** `processing-pdfs`, `analyzing-data`
- [ ] **Noun phrases acceptable:** `pdf-processing`, `data-analysis`
- [ ] **Action-oriented acceptable:** `process-pdfs`, `analyze-data`
- [ ] **Consistent within plugin:** All skills in same plugin use same pattern

**This plugin uses:** Noun-phrase pattern (e.g., `skill-development`, `docs-management`)

## SKILL.md Structure

- [ ] **Starts with YAML frontmatter** (between `---` delimiters)
- [ ] **Body under 500 lines** for optimal performance
- [ ] **Progressive disclosure** - reference files for detailed content
- [ ] **References one level deep** - no nested references

## Pre-Creation Verification

Before creating a new skill:

1. [ ] Check name is unique within the plugin
2. [ ] Verify name follows naming pattern used by other skills in plugin
3. [ ] Confirm no reserved words in name
4. [ ] Description is specific enough for Claude to select correctly
5. [ ] Description includes both "what" and "when"

## Common Mistakes to Avoid

- Using "anthropic" or "claude" in skill names
- Inconsistent naming patterns within a plugin
- Vague descriptions that don't help with skill selection
- First/second person in descriptions
- Deeply nested reference files
- SKILL.md files over 500 lines

## What This Checklist Does NOT Contain

This file intentionally excludes:

- **Specific frontmatter field formats** - Fetch from docs-management
- **Exact character limits** - Fetch from docs-management (limits shown above are summaries)
- **Reserved word lists** - Fetch from docs-management
- **Any content that exists in official documentation**

The checklist items above are curated summaries for quick reference. **Always verify against docs-management before applying any rule.**

---

**Last Updated:** 2025-12-25
**Architecture:** Query-based validation (docs-management is authoritative source)
**Update:** Added MANDATORY docs-management enforcement section
