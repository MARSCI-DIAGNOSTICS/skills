# Steering Files Guide

Context configuration for Kiro agent steering.

## Overview

Steering files provide persistent context to the Kiro agent, ensuring consistent behavior across sessions. They capture project-specific knowledge that the agent should always consider.

## File Types

### context.md

**Purpose:** Primary project context and constraints.

**Location:** `.kiro/steering/context.md`

**Structure:**

```markdown
# Project Context

## Overview

<1-2 paragraph project description>

## Goals

- <Primary goal 1>
- <Primary goal 2>

## Technology Stack

| Category | Technology |
| --- | --- |
| Language | TypeScript |
| Framework | Next.js 15 |
| Database | PostgreSQL 17 |
| Cache | Redis 7 |

## Architecture

<Brief architecture description>

### Patterns

- Vertical Slice Architecture
- CQRS for commands/queries
- Event Sourcing for audit

### Constraints

- All APIs must be RESTful
- Authentication via OAuth 2.0
- Multi-tenant isolation required

## Quality Standards

- Test coverage > 80%
- Response time < 200ms (p95)
- Zero critical security issues
```

### glossary.md

**Purpose:** Domain terminology definitions.

**Location:** `.kiro/steering/glossary.md`

**Structure:**

```markdown
# Domain Glossary

## Core Concepts

### Tenant

A customer organization that uses the platform. Each tenant has isolated data and configuration.

### Workspace

A logical container within a tenant for organizing projects. Users can belong to multiple workspaces.

### Project

A collection of related work items, specifications, and code.

## Abbreviations

| Abbr | Meaning |
| --- | --- |
| SLA | Service Level Agreement |
| TTL | Time To Live |
| MFA | Multi-Factor Authentication |

## Domain Events

| Event | Description |
| --- | --- |
| TenantCreated | New tenant provisioned |
| WorkspaceActivated | Workspace ready for use |
| ProjectArchived | Project marked inactive |
```

### conventions.md

**Purpose:** Code and documentation conventions.

**Location:** `.kiro/steering/conventions.md`

**Structure:**

````markdown
# Conventions

## Naming

### Files

- Use kebab-case: `user-service.ts`
- Test files: `*.test.ts` or `*.spec.ts`
- Type files: `*.types.ts`

### Code

- Variables: camelCase
- Classes/Types: PascalCase
- Constants: SCREAMING_SNAKE_CASE
- Private members: _prefixed

## Code Organization

### Folder Structure

```text
src/
├── features/
│   └── <feature>/
│       ├── commands/
│       ├── queries/
│       ├── components/
│       └── index.ts
├── shared/
│   ├── ui/
│   ├── utils/
│   └── types/
└── infrastructure/
```

### Feature Structure

Each feature should contain:

- Commands (write operations)
- Queries (read operations)
- Components (UI)
- Types (interfaces)
- Tests (co-located)

## Git Conventions

### Branch Naming

- `feature/<ticket>-<description>`
- `bugfix/<ticket>-<description>`
- `hotfix/<ticket>-<description>`

### Commit Messages

Follow Conventional Commits:

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `refactor:` code refactoring
- `test:` adding tests
- `chore:` maintenance

## Documentation

### Comments

- Use JSDoc for public APIs
- Explain "why" not "what"
- No commented-out code

### README

Each feature should have a README with:

- Purpose
- Usage examples
- Configuration
- Testing instructions
````

## Configuration Best Practices

### Keep It Focused

Each steering file should have a clear, single purpose:

- ✅ `context.md` - project context
- ✅ `glossary.md` - domain terms
- ✅ `conventions.md` - code standards
- ❌ `everything.md` - too broad

### Keep It Current

Steering files should be living documents:

- Update when conventions change
- Add new domain terms as discovered
- Revise constraints as architecture evolves

### Keep It Actionable

Content should guide behavior:

- ✅ "Use kebab-case for file names"
- ❌ "File names should be readable"

## Loading Behavior

### Auto-Loading

When `auto_load: true` in config.yaml:

- All steering files load at session start
- Agent always has project context
- Consistent behavior across sessions

### Manual Loading

When `auto_load: false`:

- Use `/load steering` command
- Selective loading for large projects
- Reduces token usage

## Steering Variables

### Template Variables

Steering files can include template variables:

```markdown
## Technology Stack

- Runtime: {{runtime_version}}
- Database: {{db_version}}
```

### Environment-Specific

For environment-specific context:

```markdown
## Environments

### Development
- Database: localhost:5432
- Cache: localhost:6379

### Production
- Database: prod-db.example.com
- Cache: prod-cache.example.com
```

## Integration with Specifications

### Informing Requirements

Steering context informs requirement generation:

```markdown
## Constraints (from steering)

- All APIs must be RESTful
- Response time < 200ms

## Generated Requirement

NFR-1: The system SHALL respond to all API requests within 200ms (p95).
```

### Informing Design

Steering patterns inform design decisions:

```markdown
## Architecture (from steering)

- Follow vertical slice architecture
- Use CQRS for commands/queries

## Generated Design

### Component Structure

Using vertical slice pattern, the feature will be organized as:
- `features/user-auth/commands/` - Write operations
- `features/user-auth/queries/` - Read operations
```

## Validation

### context.md Checklist

- [ ] Project overview is clear
- [ ] Technology stack is complete
- [ ] Architecture patterns documented
- [ ] Constraints are specific and measurable
- [ ] Quality standards defined

### glossary.md Checklist

- [ ] All domain terms defined
- [ ] Definitions are precise
- [ ] Abbreviations listed
- [ ] No circular definitions

### conventions.md Checklist

- [ ] Naming conventions for all types
- [ ] Folder structure documented
- [ ] Git conventions specified
- [ ] Documentation standards defined
