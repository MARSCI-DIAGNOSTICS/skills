---
name: ears-author
description: "Interactive EARS pattern authoring assistant. Guides through pattern selection and requirement construction."
argument-hint: "[requirement description or --interactive]"
allowed-tools: Read, Glob, Grep, Write, Edit, Skill, Task
---

# EARS Pattern Authoring

Interactive assistant for creating requirements using EARS (Easy Approach to Requirements Syntax) patterns.

## EARS Patterns Overview

| Pattern | Use When | Template |
| --- | --- | --- |
| Ubiquitous | Always true | The system SHALL [action] |
| Event-Driven | Triggered by event | WHEN [event], the system SHALL [action] |
| State-Driven | Depends on state | WHILE [state], the system SHALL [action] |
| Unwanted | Handle failures | IF [condition], THEN the system SHALL [action] |
| Optional | Feature-dependent | WHERE [feature], the system SHALL [action] |
| Complex | Multiple conditions | Combination of above |

## Workflow

1. **Gather Context**
   - If argument provided, analyze the requirement description
   - If `--interactive`, prompt for requirement details

2. **Pattern Selection**
   - Spawn `spec-author ears` agent
   - Agent guides through pattern selection based on:
     - Is this always true? → Ubiquitous
     - Triggered by an event? → Event-Driven
     - Depends on system state? → State-Driven
     - Handling an error/failure? → Unwanted
     - Optional feature? → Optional
     - Multiple conditions? → Complex

3. **Construct Requirement**
   - Fill in pattern template
   - Validate EARS syntax
   - Check for common anti-patterns

4. **Generate Acceptance Criteria**
   - Create Given/When/Then scenarios
   - Cover happy path and edge cases

5. **Output**
   - Display formatted requirement
   - Optionally append to specification file

## Arguments

- `$ARGUMENTS` - Requirement description to convert to EARS
- `--interactive` - Step-by-step guided authoring
- `--append` - Append to specification file
- `--pattern` - Force specific pattern (ubiquitous, event, state, unwanted, optional, complex)

## Examples

```bash
# From description
/spec-driven-development:ears-author "User can log in with email and password"

# Interactive mode
/spec-driven-development:ears-author --interactive

# Force pattern
/spec-driven-development:ears-author "Handle timeout errors" --pattern unwanted

# Append to spec
/spec-driven-development:ears-author "Session expires after 30 minutes" --append .specs/auth/spec.md
```

## Pattern Selection Guide

```text
                    ┌─────────────────────┐
                    │ What triggers this? │
                    └─────────┬───────────┘
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
           ▼                  ▼                  ▼
    ┌──────────┐       ┌──────────┐       ┌──────────┐
    │ Nothing  │       │ An event │       │ A state  │
    │(always)  │       │          │       │          │
    └────┬─────┘       └────┬─────┘       └────┬─────┘
         │                  │                  │
         ▼                  ▼                  ▼
    Ubiquitous         Event-Driven       State-Driven


    ┌─────────────────────────────────────────────┐
    │ Is this handling an error or failure case? │
    └─────────────────────┬───────────────────────┘
                          │
                    ┌─────┴─────┐
                    │    Yes    │
                    └─────┬─────┘
                          │
                          ▼
                      Unwanted
```

## Output Format

```markdown
## FR-X: [Generated Title]

WHEN the user submits valid login credentials,
the system SHALL authenticate the user
AND create a session token.

### Acceptance Criteria

- [ ] AC-X.1: Given valid email and password, when submitted, then user is authenticated
- [ ] AC-X.2: Given valid credentials, when authenticated, then session token is returned
- [ ] AC-X.3: Given invalid password, when submitted, then authentication fails with error
```

## Related Commands

- `/spec-driven-development:ears-convert` - Convert between EARS and other formats
- `/spec-driven-development:gherkin-author` - Create Gherkin scenarios
- `/spec-driven-development:specify` - Generate full specification
