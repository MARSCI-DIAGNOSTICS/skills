# Plugin Audit Framework

**Architecture:** This framework provides scoring criteria and query guides. **All validation rules are fetched from official documentation via docs-management skill** - this file contains NO duplicated official content.

## 🚨 MANDATORY: Use docs-management BEFORE Any Finding

> **ABSOLUTE REQUIREMENT - NEVER SKIP THIS STEP:**
>
> Before flagging ANY finding about plugin manifest, structure, or component organization:
>
> 1. **INVOKE** `docs-management` skill with query: `"plugin.json" "plugin manifest" "plugin schema" example`
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
- [ ] Did I check if the field is optional with auto-discovery? ← **MANY FIELDS ARE OPTIONAL**

**If you cannot verify against official docs, mark finding as UNVERIFIED and do not deduct points.**

## How Audits Work

1. **Auditor loads** `plugin-development` skill
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

### Core Plugin Topics

| Category | Query Keywords | What to Fetch |
| --- | --- | --- |
| Broad Coverage | `plugins` | General plugin documentation - start here |
| Manifest | `plugin.json manifest schema name description version` | Required fields, structure |
| Structure | `plugin structure organization directory layout` | Directory layout requirements |
| Commands | `plugin commands slash commands directory integration` | Command integration |
| Skills | `plugin skills SKILL.md packaging distribution` | Skill packaging |
| Agents | `plugin agents subagents .md files` | Agent distribution |
| Hooks | `plugin hooks hooks.json configuration` | Hook configuration |
| Marketplace | `plugin marketplace distribution install publishing` | Publishing requirements |

### Component Discovery & Optional Fields

| Category | Query Keywords | What to Fetch |
| --- | --- | --- |
| Auto-Discovery | `plugin auto-discovery default locations component` | Which components are auto-discovered |
| Default Paths | `plugin default paths directory behavior locations` | Default locations for each component |
| Optional Fields | `plugin optional fields required manifest schema` | Which manifest fields are optional |
| Path Formats | `plugin path fields format hooks commands skills` | Valid path formats for each field |

### Validation Context

| Category | Query Keywords | What to Fetch |
| --- | --- | --- |
| Field Validation | `plugin manifest validation field format requirements` | Format requirements for each field |
| Error Messages | `plugin errors validation common issues` | Known error patterns and causes |
| Best Practices | `plugin best practices recommendations patterns` | Recommended patterns |

**CRITICAL:** The auditor MUST query docs-management and use the returned official documentation as the source of truth for validation rules. Never flag an issue without first verifying the rule exists in official documentation.

## 🚨 Required docs-management Queries Per Category

**MANDATORY:** Execute these queries BEFORE scoring each category:

| Category | Required Query | What to Verify |
| --- | --- | --- |
| Broad Coverage | `plugins` | Start here for general context |
| Manifest | `plugin.json manifest schema name description version required` | Required vs optional fields |
| Structure | `plugin structure organization directory layout auto-discovery` | Directory layout, auto-discovery |
| Commands | `plugin commands slash commands directory location` | Command locations, naming |
| Skills | `plugin skills SKILL.md structure packaging` | Skill packaging requirements |
| Agents | `plugin agents subagents configuration files` | Agent file requirements |
| Hooks | `plugin hooks hooks.json configuration organization` | Hook organization |
| Marketplace | `plugin marketplace distribution install publishing` | Publishing requirements |

### Query Execution Protocol

1. **Before each category** → Run the required query
2. **Read returned docs** → Find the relevant example/table
3. **Compare your finding** → Does it match official docs?
4. **If mismatch** → Your finding is WRONG, not the plugin
5. **If uncertain** → Do NOT deduct points, mark as NEEDS-VERIFICATION

## Extensive Validation Requirements

**CRITICAL:** Before flagging ANY finding, you MUST:

1. **Query docs-management EXTENSIVELY** - Use multiple keyword combinations
2. **Read the FULL official documentation** - Not just snippets
3. **Check for optional vs required fields** - Query: `"optional" "required" {topic}`
4. **Verify default behaviors** - Query: `"default" {topic}`
5. **Distinguish official vs repo-specific rules** - Only official rules are errors; repo-specific are suggestions
6. **Check auto-discovery behavior** - Query: `"plugin auto-discovery" "default locations"`

**If official documentation does not explicitly prohibit something, do NOT flag it as an error.**

**If you cannot find documentation supporting your finding, the finding is INVALID.**

## Audit Scoring Rubric

This scoring rubric is used by the `plugin-component-auditor` agent for formal audits.

### Category Scores

| Category | Points | Description |
| --- | --- | --- |
| Manifest Structure | 25 | Valid plugin.json, required fields present |
| Component Organization | 25 | Proper directories for all components |
| Namespace Compliance | 20 | Consistent naming, no conflicts |
| Documentation | 15 | README, descriptions, usage examples |
| Distribution Readiness | 15 | Version, dependencies, marketplace requirements |
| **Plugin Boundaries** | **15** | **Single responsibility, clear entry/exit, no overlap** |
| **Published Standard Test** | **15** | **Unique value beyond researchable standards** |
| **Plugin Necessity** | **10** | **Justified existence, no redundancy** |

The maximum possible score is **Total: 140 points**.

### Scoring Details

**Note:** Pass conditions are validated against official documentation fetched via docs-management. The criteria below describe WHAT to check, not the specific rules (which come from docs).

#### Manifest Structure (25 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Valid JSON syntax | 5 | Syntax check |
| Name field | 8 | Query: "plugin.json", "plugin name" |
| Description field | 4 | Query: "plugin manifest" |
| Version field | 4 | Query: "plugin version", "semver" |
| Other required fields | 4 | Query: "plugin schema" |

##### Manifest Efficiency (Simplification Opportunities)

Claude Code auto-discovers components in default locations. Declaring default paths explicitly is redundant and should be flagged as a simplification opportunity.

| Criterion | Deduction | Description |
| --- | --- | --- |
| Redundant `skills` path | -2 | `"skills": "./skills"` can be omitted (auto-discovered) |
| Redundant `commands` path | -2 | `"commands": "./commands"` can be omitted (auto-discovered) |
| Redundant `agents` path | -2 | `"agents": "./agents"` can be omitted (auto-discovered) |

**Default Paths (Auto-Discovered):**

| Component | Default Path | Manifest Field |
| --- | --- | --- |
| Skills | `./skills` | `skills` - OPTIONAL if using default |
| Commands | `./commands` | `commands` - OPTIONAL if using default |
| Agents | `./agents` | `agents` - OPTIONAL if using default |
| Output Styles | N/A | `outputStyles` - REQUIRED (not auto-discovered) |
| Hooks | `./hooks.json` or `./hooks/hooks.json` | `hooks` - file path, not directory |

**Rule:** If a component path field declares the exact default directory for that component type, flag as "SIMPLIFICATION: Can be omitted - uses default path".

**Severity:** LOW - This is a simplification opportunity, not a compliance error. Points are deducted to encourage cleaner manifests, but it does not cause automatic failure.

**Verification Query:** Before flagging, query docs-management with: `"plugin auto-discovery" "default locations" "component paths"`

##### Path & Format Validation

**CRITICAL:** Query docs-management for official path format requirements before flagging.

| Criterion | Deduction | Verification Query |
| --- | --- | --- |
| Invalid path prefix | -3 | `"plugin path format" "relative paths" "./"`  |
| Absolute path used | -3 | `"plugin manifest" "path format" "absolute"` |
| Path traversal | -5 | `"plugin security" "path traversal"` |
| Hooks format violation | -3 | `"plugin hooks" "file path" "hooks.json"` |
| Invalid name format | -5 | `"plugin name" "format" "naming convention"` |

**Required Queries Before Flagging:**

1. `"plugin path format" "relative paths"` - Get official path format requirements
2. `"plugin hooks" "file vs directory"` - Verify hooks field format requirements
3. `"plugin name" "naming convention" "format"` - Get official name format rules

**DO NOT hardcode rules.** Official documentation defines:

- Valid path prefixes
- Allowed/disallowed path patterns
- Hooks field format (file vs directory)
- Name field format requirements

**If official docs don't specify a requirement, do NOT flag it.**

#### Component Organization (25 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Commands directory | 7 | Query: "plugin commands structure" |
| Skills directory | 6 | Query: "plugin skills structure" |
| Agents directory | 6 | Query: "plugin agents structure" |
| Hooks directory | 6 | Query: "plugin hooks structure" |

##### Component Placement Validation

**CRITICAL:** Query docs-management for official component placement rules before flagging.

| Criterion | Deduction | Verification Query |
| --- | --- | --- |
| Component misplacement | -5 | `"plugin structure" "component location" ".claude-plugin directory"` |
| Undeclared output styles | -2 | `"plugin outputStyles" "auto-discovery" "manifest declaration"` |

**Required Queries Before Flagging:**

1. `"plugin structure" "directory layout"` - Get official directory structure
2. `"plugin .claude-plugin" "manifest location"` - Verify what goes in .claude-plugin/
3. `"plugin outputStyles" "auto-discovery"` - Check if output styles are auto-discovered

**DO NOT hardcode structure rules.** Official documentation defines:

- Where `.claude-plugin/` directory contents belong
- Where component directories (commands, skills, agents) should be located
- Which component types are auto-discovered vs require manifest declaration

**If official docs don't specify placement requirements, do NOT flag it.**

#### Namespace Compliance (20 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Consistent prefix | 10 | Repository standard: plugin name prefix |
| No reserved words | 5 | Query: "plugin naming restrictions" |
| No conflicts | 5 | Analysis: unique names |

#### Documentation (15 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| README exists | 5 | File system check |
| Component descriptions | 5 | Analysis: all components have descriptions |
| Usage examples | 5 | Repository standard: practical examples |

#### Distribution Readiness (15 points)

| Criterion | Points | Validation Source |
| --- | --- | --- |
| Valid semver version | 5 | Query: "plugin version" |
| Dependencies documented | 5 | Repository standard |
| Marketplace metadata | 5 | Query: "plugin marketplace" |

#### Plugin Boundaries (15 points)

These criteria assess whether the plugin has clear, well-defined boundaries that prevent overlap and confusion.

| Criterion | Points | Pass Condition |
| --- | --- | --- |
| Single Responsibility | 5 | Plugin purpose describable in ≤8 words |
| Clear Entry/Exit | 5 | Defined input and output for workflows |
| No Overlap | 5 | Techniques/skills not duplicated in other plugins |

##### Single Responsibility Test

```yaml
check: Can the plugin's purpose be described in ≤8 words?
pass_examples:
  - "Version control operations" (git)
  - "Claude Code meta-layer and documentation" (claude-ecosystem)
  - "Five-phase specification workflow" (spec-driven-development)
fail_examples:
  - "All BABOK techniques for business analysis" (vague, too broad)
  - "Various architecture patterns and methodologies" (unclear scope)
scoring: 5 pts if clear, 0 pts if vague
```

##### Clear Entry/Exit Test

```yaml
check: Does the plugin define clear workflow entry and exit points?
criteria:
  - Entry point: What triggers plugin use? (user asks, task type, file type)
  - Exit point: What does the plugin produce? (decision, artifact, transformation)
  - Handoff: How does it connect to other plugins?
pass_example: spec-driven-development - starts with requirements, ends with specs
fail_example: "Business analysis" - no clear starting/ending state
scoring: 5 pts if clear, 0 pts if unclear
```

##### No Overlap Test

```yaml
check: Do other plugins provide overlapping functionality?
method:
  - Grep skill/command names across all plugins
  - Compare descriptions for semantic similarity
  - Check for duplicate agents serving same purpose
pass_example: git plugin - unique version control focus, no other plugin covers this
fail_example: Three plugins with ADR management skills (overlap)
scoring: 5 pts if unique, -5 pts per significant overlap detected
deductions:
  - Same skill name in multiple plugins: -5 pts
  - Same command name in multiple plugins: -5 pts
  - >70% semantic overlap in descriptions: -3 pts
```

#### Published Standard Test (15 points)

These criteria assess whether the plugin provides unique value beyond what MCP research could provide on-demand.

| Criterion | Points | Pass Condition |
| --- | --- | --- |
| Unique Value | 10 | Provides opinionated guidance NOT in published literature |
| MCP Irreplaceability | 5 | Cannot be fully replaced by MCP research on-demand |

##### Unique Value Test

```yaml
check: Does the plugin provide opinionated architectural guidance beyond published standards?
published_standards_examples:
  - ISO 25010 (quality attributes)
  - CRISP-DM (ML lifecycle)
  - BABOK (business analysis)
  - Kimball methodology (data architecture)
  - Design Thinking (product discovery)
unique_value_examples:
  - Content type hierarchy patterns (composition vs inheritance decisions)
  - Specific EF Core JSON column patterns for dynamic schemas
  - Claude Code-specific workflow integrations
  - Tool-specific automation scripts
pass_example: content-management-system - composition patterns are opinionated, not standard
fail_example: quality-attributes - ISO 25010 is a published standard, fully researchable
scoring: 10 pts if unique opinionated value, 0 pts if just wrapping published standards
```

##### MCP Irreplaceability Test

```yaml
check: Can equivalent guidance be obtained via MCP research?
test_query: "Help me do {plugin purpose} using {methodology}"
sources_to_check:
  - perplexity (for methodology explanation)
  - context7 (for library/framework docs)
  - microsoft-learn (for Microsoft tech)
  - firecrawl (for specific websites)
pass_criteria:
  - MCP cannot provide the specific decision guidance
  - Plugin integrates multiple concepts in unique way
  - Plugin provides tool-specific automation
fail_criteria:
  - MCP can fully explain the methodology
  - Claude can generate equivalent templates on-demand
  - No unique workflow beyond "apply standard X"
scoring: 5 pts if irreplaceable, 0 pts if MCP can replace
```

#### Plugin Necessity (10 points)

These criteria assess whether the plugin should exist at all.

| Criterion | Points | Pass Condition |
| --- | --- | --- |
| Existence Justified | 5 | Solves real problem with unique approach |
| No Redundancy | 5 | Doesn't duplicate existing plugin functionality |

##### Existence Justified Test

```yaml
check: Does the plugin solve a real problem that warrants its existence?
justification_criteria:
  - Clear use cases that cannot be served by existing plugins
  - Meaningful skill/command set (not just 1-2 trivial items)
  - Evidence of actual usage or need
pass_example: git plugin - version control is essential, unique tooling
fail_example: Plugin with single skill wrapping a simple API call
scoring: 5 pts if justified, 0 pts if unclear justification
```

##### No Redundancy Test

```yaml
check: Does another plugin already serve this purpose?
method:
  - Review plugin README descriptions
  - Check for semantic overlap in skills
  - Assess if consolidation would improve discoverability
pass_example: git plugin - no other plugin covers version control
fail_example: contract-testing when test-strategy exists (can consolidate)
scoring: 5 pts if unique, 0 pts if redundant
recommendation: If redundant, suggest consolidation target
```

#### Configuration File Validation (Optional, 0 base points)

**CRITICAL:** Query docs-management for official config file requirements before flagging.

| Criterion | Deduction | Verification Query |
| --- | --- | --- |
| Invalid config file syntax | -3 | `"plugin" "{file-type}" "configuration" "schema"` |

**Required Queries Before Flagging:**

1. `"plugin mcp" ".mcp.json" "configuration"` - Get MCP config requirements
2. `"plugin lsp" ".lsp.json" "servers"` - Get LSP config requirements
3. `"plugin hooks" "hooks.json" "schema"` - Get hooks file requirements

**Validation Approach:**

1. Query docs-management to identify which config files are expected
2. For each config file that exists, verify JSON syntax validity
3. Only deduct points if file exists AND has invalid syntax

**Note:** These files are optional per official docs. Query docs-management to confirm which files are expected and their format requirements. Do NOT assume file existence requirements.

### Thresholds

| Score Percentage | Result |
| --- | --- |
| 85%+ (119-140) | **PASS** |
| 70-84% (98-118) | **PASS WITH WARNINGS** |
| Below 70% (<98) | **FAIL** |

### Automatic Failures

Regardless of score, a plugin **automatically fails** if:

- plugin.json is invalid JSON
- Missing name field
- Missing description field

## Repository-Specific Standards

These standards are specific to this repository and NOT from official Claude Code documentation:

| Standard | Value | Rationale |
| --- | --- | --- |
| Namespace prefix | Plugin name | Consistency |
| README required | Yes | Discoverability |
| Descriptions required | All components | User guidance |

## Validation Protocol

**CRITICAL: All validation MUST be docs-driven.**

Before flagging ANY finding:

1. **Query docs-management** for the relevant topic (use expanded query keywords above)
2. **Verify the rule exists** in official documentation
3. **Check for auto-discovery behavior** - many components have default locations and don't require manifest declaration
4. **Verify path/format requirements** from official docs before flagging format issues
5. **If docs are unclear**, flag as "UNVERIFIED - requires manual review" rather than making assumptions

**General Principle:** If you cannot find an official rule requiring something, do not flag its absence as an issue. Query expansively using multiple keyword combinations before concluding something is missing or wrong.

## What This Framework Does NOT Contain

This file intentionally excludes:

- **Specific manifest field requirements** - Fetch from docs-management
- **Exact structure requirements** - Fetch from docs-management
- **Any content that exists in official documentation**

---

**Last Updated:** 2026-01-17
**Architecture:** Query-based audit framework (no duplicated official content)
**Update:** Added Plugin Boundaries (15pts), Published Standard Test (15pts), and Plugin Necessity (10pts) scoring categories (total 140pts). Added Path & Format Validation, Component Placement Validation, and Configuration File Validation sections
