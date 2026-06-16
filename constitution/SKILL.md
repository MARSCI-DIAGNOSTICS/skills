---
name: constitution
description: "Create or update the project constitution file (.constitution.md) for Spec Kit workflow."
argument-hint: "[--init | --update | --validate]"
allowed-tools: Read, Glob, Grep, Write, Edit, Skill
---

# Project Constitution

Create, update, or validate the project constitution file for the Spec Kit workflow.

## What is a Constitution?

The constitution (`.constitution.md`) defines project principles, constraints, and standards that guide all specification and implementation work. It's Phase 0 of the Spec Kit workflow.

## Constitution Structure

```markdown
# Project Constitution

## Mission

[One sentence describing the project's purpose]

## Principles

1. **[Principle Name]**: [Description]
2. **[Principle Name]**: [Description]

## Architecture Constraints

- [Technology constraint]
- [Pattern constraint]
- [Integration constraint]

## Quality Standards

- **Testing:** [Testing requirements]
- **Documentation:** [Documentation requirements]
- **Code Style:** [Style requirements]

## Team Conventions

- [Development workflow]
- [Communication patterns]
- [Review process]
```

## Workflow

### Initialize (--init)

1. **Check for Existing**
   - Look for `.constitution.md`
   - If exists, prompt to update instead

2. **Gather Project Context**
   - Analyze existing codebase
   - Identify patterns in use
   - Detect technology stack

3. **Generate Constitution**
   - Create mission statement
   - Define principles from patterns
   - Document constraints
   - Establish quality standards

4. **Save**
   - Write to `.constitution.md`
   - Report creation summary

### Update (--update)

1. **Load Existing**
   - Read current constitution
   - Parse sections

2. **Analyze Changes**
   - Check codebase for new patterns
   - Identify drift from principles

3. **Suggest Updates**
   - Present changes for approval
   - Apply approved changes

### Validate (--validate)

1. **Load Constitution**
   - Read `.constitution.md`

2. **Check Structure**
   - Required sections present
   - Principles well-formed
   - No conflicting constraints

3. **Check Alignment**
   - Compare codebase to principles
   - Identify violations
   - Report compliance status

## Arguments

- `--init` - Create new constitution (default)
- `--update` - Update existing constitution
- `--validate` - Validate constitution and check alignment
- `--force` - Overwrite existing without prompt

## Examples

```bash
# Create new constitution
/spec-driven-development:constitution --init

# Update existing
/spec-driven-development:constitution --update

# Validate alignment
/spec-driven-development:constitution --validate

# Force overwrite
/spec-driven-development:constitution --init --force
```

## Constitution Example

```markdown
# Project Constitution

## Mission

Build a secure, scalable e-commerce platform that enables small businesses
to sell products online with minimal technical expertise required.

## Principles

1. **Security First**: All features must consider security implications.
   User data protection is non-negotiable.

2. **Simplicity Over Cleverness**: Choose boring, proven solutions over
   novel approaches. Code should be readable by junior developers.

3. **Vertical Slices**: Features are implemented as complete vertical
   slices, not horizontal layers. Each feature is independently deployable.

4. **Test-Driven**: All business logic has unit tests. Integration tests
   cover critical paths. No feature merges without passing tests.

## Architecture Constraints

- **Language:** TypeScript (strict mode) for all application code
- **Database:** PostgreSQL for persistent storage
- **API Style:** REST with OpenAPI specifications
- **Authentication:** OAuth 2.0 + JWT tokens
- **Deployment:** Docker containers on Kubernetes

## Quality Standards

- **Test Coverage:** Minimum 80% for business logic
- **Documentation:** All public APIs documented with examples
- **Code Review:** All changes require one approval
- **Performance:** API responses under 200ms (p95)

## Team Conventions

- **Branching:** Feature branches from main, squash merge
- **Commits:** Conventional commits (feat:, fix:, docs:)
- **PRs:** Include description, test plan, screenshots if UI
- **Releases:** Semantic versioning, automated changelog
```

## Validation Report

```markdown
# Constitution Validation Report

**File:** .constitution.md
**Status:** ⚠️ VALID WITH WARNINGS

## Structure Check

✓ Mission section present
✓ Principles section present
✓ Architecture Constraints present
✓ Quality Standards present
✓ Team Conventions present

## Principle Conflicts

None detected

## Alignment Check

✓ TypeScript strict mode enabled (matches constraint)
✓ PostgreSQL in use (matches constraint)
⚠️ Test coverage at 72% (below 80% threshold)
⚠️ Some API endpoints missing OpenAPI docs

## Recommendations

1. Increase test coverage to meet 80% threshold
2. Add OpenAPI docs for: /api/orders/*, /api/users/*
```

## Related Commands

- `/spec-driven-development:speckit-run` - Full 5-phase workflow
- `/spec-driven-development:specify` - Generate specification (Phase 1)
- `/spec-driven-development:validate` - Validate specification
