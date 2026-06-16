---
name: create-adr
description: Create a new Architecture Decision Record. Use when documenting significant technical decisions with context, options, and rationale.
allowed-tools: Read, Glob, Grep, Write, Skill
argument-hint: <title> [--status proposed|accepted|deprecated|superseded] [--template basic|madr|extended]
---

# Create Architecture Decision Record

Create a new ADR documenting a significant technical decision.

## Process

### 1. Parse Arguments

Extract from user input:

- **Title**: Decision topic (required) - e.g., "Use PostgreSQL for primary database"
- **Status**: `proposed`, `accepted`, `deprecated`, `superseded` (default: `proposed`)
- **Template**: `basic` (Nygard), `madr`, or `extended` (default: `madr`)

### 2. Determine ADR Number

1. Find existing ADRs in the project:

   ```text
   Look in: docs/decisions/, docs/adr/
   Pattern: ADR-*.md, [0-9][0-9][0-9][0-9]-*.md
   ```

2. Calculate next number:
   - If no ADRs exist, start at 001
   - Otherwise, increment highest existing number

### 3. Gather Context

If context is not provided, prompt for or infer:

1. **Problem Statement**: What issue motivated this decision?
2. **Constraints**: What limitations affect the decision?
3. **Options Considered**: What alternatives exist?
4. **Decision Drivers**: What factors are most important?

### 4. Load Skill and Generate

1. Load the `enterprise-architecture:adr-management` skill for templates and guidance
2. Select template based on `template` argument
3. Generate ADR content with:
   - Proper frontmatter/header
   - All required sections
   - Placeholder guidance for sections needing human input

### 5. Create File

Determine file location based on project conventions:

```text
Priority order:
1. docs/decisions/ADR-{number}-{slug}.md (if docs/decisions/ exists)
2. docs/adr/ADR-{number}-{slug}.md (if docs/adr/ exists)
4. docs/decisions/ADR-{number}-{slug}.md (create directory)
```

Slug format: lowercase, hyphens, from title
Example: "Use PostgreSQL" → `ADR-001-use-postgresql.md`

### 6. Update Index

If an ADR index/registry exists, add entry:

- Add to ADR-INDEX.md or README.md in decisions folder
- Include: number, title, status, date

## Output Content

### Basic Template (Nygard)

```markdown
# ADR-{NUMBER}: {TITLE}

## Status

{STATUS}

## Context

[What is the issue that we're seeing that is motivating this decision?]

## Decision

[What is the change that we're proposing and/or doing?]

## Consequences

[What becomes easier or more difficult to do because of this change?]
```

### MADR Template

```markdown
# ADR-{NUMBER}: {TITLE}

## Status

{STATUS}

Date: {YYYY-MM-DD}

## Context and Problem Statement

[Describe the context and problem statement]

## Decision Drivers

* [Driver 1]
* [Driver 2]

## Considered Options

1. [Option 1]
2. [Option 2]
3. [Option 3]

## Decision Outcome

**Chosen option:** "[Option X]", because [justification].

### Consequences

**Good:**
* [Positive consequence]

**Bad:**
* [Negative consequence]

## Pros and Cons of Options

### [Option 1]

* Good, because [argument]
* Bad, because [argument]

### [Option 2]

* Good, because [argument]
* Bad, because [argument]
```

### Extended Template

Include additional sections:

- Executive Summary
- Constraints and Assumptions
- Trade-offs table
- Implementation action items
- Validation criteria
- Related decisions
- References

## Example Invocations

```text
/create-adr "Use PostgreSQL for primary database"
→ Creates ADR-XXX-use-postgresql.md with MADR template, status=proposed

/create-adr "Switch to event sourcing" status=accepted template=extended
→ Creates ADR-XXX-switch-to-event-sourcing.md with extended template

/create-adr "Deprecate REST API v1" status=deprecated
→ Creates ADR-XXX-deprecate-rest-api-v1.md marking v1 as deprecated
```

## Post-Creation Guidance

After creating the ADR, remind user to:

1. **Fill in placeholders** marked with `[brackets]`
2. **Add specific options** with pros/cons
3. **Document the actual decision** once made
4. **Link related ADRs** if applicable
5. **Update status** when decision is finalized
6. **Get review** from stakeholders

## Quality Criteria

Generated ADR must:

- [ ] Have unique, sequential number
- [ ] Follow project's ADR location conventions
- [ ] Include all required sections for template type
- [ ] Have clear placeholder guidance
- [ ] Be linked from ADR index (if exists)
- [ ] Use consistent date format (ISO 8601)
