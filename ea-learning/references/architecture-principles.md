# Architecture Principles Template

## What Are Architecture Principles?

Architecture principles are foundational rules that guide design decisions across an organization. They provide guardrails without micromanagement, ensuring consistency while allowing flexibility.

## Principle Format

Each principle should have:

1. **Name**: Short, memorable identifier
2. **Statement**: Clear, actionable declaration
3. **Rationale**: Why this principle matters
4. **Implications**: What this means in practice

## Template

```markdown
## [Principle Name]

**Statement:** [Clear, actionable declaration of the principle]

**Rationale:** [Why this principle is important for the organization]

**Implications:**
- [What teams must do differently]
- [What decisions this guides]
- [What trade-offs are implied]
```

## Example Principles

### API-First Design

**Statement:** All services must expose functionality through well-defined APIs before building user interfaces.

**Rationale:** APIs enable integration, reuse, and future flexibility. Building APIs first ensures services are consumable by multiple clients and partners.

**Implications:**

- Start with OpenAPI/AsyncAPI specifications
- UI development depends on stable API contracts
- API versioning strategy required from day one

---

### Prefer Managed Services

**Statement:** Use cloud-managed services over self-hosted solutions when they meet requirements at acceptable cost.

**Rationale:** Managed services reduce operational burden, provide built-in scaling, and allow teams to focus on business value rather than infrastructure.

**Implications:**

- Evaluate managed vs. self-hosted for each component
- Accept some vendor coupling for operational benefits
- Document exceptions and their justifications

---

### Single Source of Truth

**Statement:** Each piece of business data has exactly one authoritative source; all other uses are derived or cached.

**Rationale:** Multiple sources of truth lead to inconsistency, reconciliation overhead, and conflicting decisions.

**Implications:**

- Identify data owners for each domain
- Other systems sync from the source, not to it
- Build clear data contracts between domains

---

### Fail Fast, Recover Gracefully

**Statement:** Systems should detect failures quickly but degrade gracefully rather than cascading failures.

**Rationale:** Early failure detection enables faster recovery. Graceful degradation maintains partial functionality during issues.

**Implications:**

- Implement health checks and circuit breakers
- Design for partial availability
- Build timeout and retry strategies

## Creating Your Principles

### Step 1: Identify Key Decisions

What architectural decisions are made repeatedly? Those need principles.

### Step 2: Draft Principles (3-7 to Start)

Start with essential principles. Too many become unmanageable.

### Step 3: Validate Against Past Decisions

Would these principles have guided past decisions correctly?

### Step 4: Socialize and Refine

Get feedback from teams who will apply them.

### Step 5: Document Exceptions

No principle is absolute. Document when and why to deviate.

## Anti-Patterns to Avoid

| Anti-Pattern | Problem |
| --- | --- |
| Too many principles | Teams can't remember or apply them |
| Too vague | "Use good design" isn't actionable |
| Too prescriptive | "Always use PostgreSQL" removes judgment |
| No rationale | Teams don't understand the "why" |
| No implications | Teams don't know how to apply them |

## Governance

- Review principles annually
- Track principle violations in ADRs
- Update principles based on lessons learned
- Maintain a principles decision log
