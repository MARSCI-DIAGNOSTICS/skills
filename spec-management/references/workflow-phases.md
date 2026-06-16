# Spec Kit 5-Phase Workflow Reference

## Overview

The GitHub Spec Kit defines a 5-phase specification-driven development workflow that guides features from inception to implementation.

## Phase Summary

| Phase | Name | Artifact | Command |
| --- | --- | --- | --- |
| 0 | Constitution | `.constitution.md` | `/spec:constitution` |
| 1 | Specify | `feature.md` | `/spec:specify` |
| 2 | Plan | `design.md` | `/spec:plan` |
| 3 | Tasks | `tasks.md` | `/spec:tasks` |
| 4 | Implement | Code | `/spec:implement` |

## Phase Details

### Phase 0: Constitution

**Purpose:** Establish project principles, constraints, and context that apply to all features.

**Artifact:** `.constitution.md`

**Contents:**

- Project principles and values
- Technical constraints
- Quality standards
- Team conventions
- Architectural guardrails

**Command:** `/spec:constitution`

**When to Execute:**

- At project inception
- When major architectural changes occur
- When team conventions change

**Example:**

```markdown
# Project Constitution

## Principles
- User experience first
- Performance within acceptable bounds
- Maintainability over cleverness

## Technical Constraints
- .NET 10, C# 13
- PostgreSQL 17
- OpenTelemetry for observability

## Quality Standards
- All code must have unit tests
- Integration tests for external boundaries
- Architecture tests for layer enforcement
```

### Phase 1: Specify

**Purpose:** Transform a feature request or user story into a formal specification.

**Artifact:** `feature.md` or canonical specification YAML

**Contents:**

- Problem statement and motivation
- EARS-formatted requirements
- Given/When/Then acceptance criteria
- Traceability links

**Command:** `/spec:specify`

**Input:** Feature request, user story, or problem description

**Output:** Canonical specification with requirements and acceptance criteria

**Validation:**

- Each requirement is testable
- EARS syntax is correct
- Acceptance criteria use Given/When/Then
- Priority uses MoSCoW (must/should/could/wont)

**Example:**

```yaml
id: "SPEC-042"
title: "Password Reset Capability"
type: feature

context:
  problem: |
    Users who forget their password cannot access their accounts
    and must contact support, causing delays and frustration.
  motivation: |
    Self-service password reset reduces support burden and
    improves user experience with immediate account recovery.

requirements:
  - id: "REQ-001"
    text: "WHEN a user requests a password reset, the system SHALL send a reset link to their registered email within 30 seconds"
    priority: must
    ears_type: event-driven
    acceptance_criteria:
      - id: "AC-001"
        given: "a user with a registered email exists"
        when: "the user submits a password reset request with their email"
        then: "the system sends a reset link email within 30 seconds"
```

### Phase 2: Plan

**Purpose:** Design the implementation approach before coding.

**Artifact:** `design.md`

**Contents:**

- High-level approach
- Components to create/modify
- Dependencies and prerequisites
- Alternatives considered
- Risk assessment

**Command:** `/spec:plan`

**Input:** Completed specification from Phase 1

**Output:** Implementation design document

**Validation:**

- All requirements addressed
- Dependencies identified
- Alternatives documented
- Technical approach is feasible

**Example:**

```markdown
# Design: Password Reset Capability

## Approach
Implement a token-based password reset flow using time-limited
single-use tokens stored in Redis with 1-hour TTL.

## Components
- `PasswordResetController` - API endpoints
- `PasswordResetService` - Business logic
- `TokenGenerator` - Secure token generation
- `EmailService` - Reset email sending

## Dependencies
- Redis for token storage
- SMTP service for email
- Existing User repository

## Alternatives Considered
1. **Magic link via SMS** - Rejected: Adds SMS cost
2. **Security questions** - Rejected: Poor UX, security concerns
```

### Phase 3: Tasks

**Purpose:** Break down the implementation into discrete, executable tasks.

**Artifact:** `tasks.md`

**Contents:**

- Task list with clear deliverables
- Task dependencies
- Verification steps per task
- Mapping to requirements

**Command:** `/spec:tasks`

**Input:** Completed design from Phase 2

**Output:** Task breakdown with acceptance criteria

**Validation:**

- Tasks are appropriately sized
- Dependencies are clear
- Each task produces testable output
- Full requirement coverage

**Example:**

```markdown
# Tasks: Password Reset Capability

## Task 1: Create Token Generator
- [ ] Implement `ITokenGenerator` interface
- [ ] Create `SecureTokenGenerator` with crypto-random tokens
- [ ] Add unit tests for token uniqueness and format
**Produces:** `TokenGenerator.cs`, `TokenGeneratorTests.cs`
**Verifies:** Token generation is cryptographically secure

## Task 2: Create Reset Request Handler
- [ ] Create `RequestPasswordReset` command
- [ ] Implement handler with token storage
- [ ] Add integration test with Redis
**Produces:** `RequestPasswordReset.cs`, handler, tests
**Verifies:** REQ-001 (reset request handling)
```

### Phase 4: Implement

**Purpose:** Execute tasks with guided implementation.

**Artifact:** Working code

**Contents:**

- Code implementing each task
- Tests verifying functionality
- Documentation updates

**Command:** `/spec:implement`

**Input:** Task list from Phase 3

**Process:**

1. Select task to implement
2. Review task requirements
3. Write failing test (TDD)
4. Implement code
5. Verify acceptance criteria
6. Mark task complete
7. Repeat for next task

**Validation:**

- All tasks completed
- All tests passing
- Acceptance criteria verified
- Code review ready

## Workflow Transitions

```text
┌─────────────────────────────────────────────────────────────┐
│                      PHASE 0                                 │
│                    Constitution                              │
│              (Project principles)                            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      PHASE 1                                 │
│                      Specify                                 │
│              (Requirements → Spec)                           │
└─────────────────────────────────────────────────────────────┘
                           │
                    Validation Gate
                    (Spec complete?)
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      PHASE 2                                 │
│                       Plan                                   │
│              (Spec → Design)                                 │
└─────────────────────────────────────────────────────────────┘
                           │
                    Validation Gate
                    (Design feasible?)
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      PHASE 3                                 │
│                       Tasks                                  │
│              (Design → Task List)                            │
└─────────────────────────────────────────────────────────────┘
                           │
                    Validation Gate
                    (Tasks complete?)
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      PHASE 4                                 │
│                     Implement                                │
│              (Tasks → Working Code)                          │
└─────────────────────────────────────────────────────────────┘
```

## Validation Gates

Each phase transition includes a validation gate:

| Gate | From | To | Validation |
| --- | --- | --- | --- |
| Spec Gate | Phase 1 | Phase 2 | All requirements have acceptance criteria |
| Design Gate | Phase 2 | Phase 3 | All requirements covered by design |
| Task Gate | Phase 3 | Phase 4 | All design components have tasks |
| Complete Gate | Phase 4 | Done | All tests pass, criteria met |

## Quick Start

To run the complete workflow:

```bash
# Set up project constitution (once per project)
/spec:constitution

# For each feature:
/spec:speckit:run "User authentication with OAuth"
```

Or step by step:

```bash
/spec:specify "User authentication with OAuth"
/spec:plan path/to/spec.yaml
/spec:tasks path/to/spec.yaml
/spec:implement path/to/spec.yaml
```
