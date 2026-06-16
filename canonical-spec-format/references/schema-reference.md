# Canonical Specification Schema Reference

## Complete Schema Structure

```yaml
# Root object
id: string                      # Required: SPEC-{number}
title: string                   # Required: Human-readable title
type: enum                      # Required: feature|bug|chore|spike|tech-debt

# Context object
context:
  problem: string               # Required: min 20 chars
  motivation: string            # Required
  background: string            # Optional

# Requirements array
requirements:                   # Required: at least one
  - id: string                  # Required: REQ-{number}
    text: string                # Required: EARS-formatted
    priority: enum              # Required: must|should|could|wont
    ears_type: enum             # Required: ubiquitous|state-driven|event-driven|unwanted|complex|optional
    acceptance_criteria:        # Required: at least one
      - id: string              # Required: AC-{number}
        given: string           # Required
        when: string            # Required
        then: string            # Required
        and: string[]           # Optional
    notes: string               # Optional

# Design object (optional)
design:
  approach: string              # Optional
  components: string[]          # Optional
  dependencies: string[]        # Optional
  alternatives:                 # Optional
    - name: string              # Required if alternatives present
      reason_rejected: string   # Required if alternatives present

# Traceability object (optional)
traceability:
  adr_refs: string[]            # Optional: ADR-{number} format
  requirement_refs: string[]    # Optional: FR-{n} or NFR-{n} format
  epic_ref: string              # Optional: EPIC-{number} format
  user_story_refs: string[]     # Optional: US-{number} format

# Metadata object
metadata:
  status: enum                  # Required: draft|review|approved|implemented|deprecated
  created: string               # Required: ISO 8601 date
  provider: string              # Required: provider name
  version: string               # Optional: semantic version
  bounded_context: string       # Optional: bounded context name
```

## Type Definitions

### SpecificationType

```yaml
type: enum
values:
  - feature     # New functionality
  - bug         # Defect fix
  - chore       # Maintenance task
  - spike       # Research/investigation
  - tech-debt   # Technical debt reduction
```

### Priority

```yaml
priority: enum
values:
  - must        # Non-negotiable
  - should      # Important
  - could       # Desirable
  - wont        # Excluded
```

### EarsType

```yaml
ears_type: enum
values:
  - ubiquitous     # Always active behavior
  - state-driven   # Behavior during state
  - event-driven   # Response to trigger
  - unwanted       # Error/exception handling
  - complex        # Multiple patterns
  - optional       # Configurable feature
```

### Status

```yaml
status: enum
values:
  - draft          # Initial creation
  - review         # Under review
  - approved       # Ready for implementation
  - implemented    # Complete
  - deprecated     # No longer valid
```

### BoundedContext

```yaml
bounded_context: enum
values:
  - WorkManagement      # Features, Kanban, planning
  - Orchestration       # Agent lifecycle, sessions
  - Workflows           # ADW/PITER execution
  - Expertise           # Agent experts
  - ExecutionControl    # Hooks, policies
  - TriggerManagement   # Cron, webhooks
  - Integrations        # AI providers, GitHub, MCP
```

## JSON Schema (Excerpt)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "title", "type", "context", "requirements", "metadata"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^SPEC-\\d+$"
    },
    "title": {
      "type": "string",
      "minLength": 1
    },
    "type": {
      "type": "string",
      "enum": ["feature", "bug", "chore", "spike", "tech-debt"]
    },
    "context": {
      "type": "object",
      "required": ["problem", "motivation"],
      "properties": {
        "problem": { "type": "string", "minLength": 20 },
        "motivation": { "type": "string", "minLength": 1 },
        "background": { "type": "string" }
      }
    },
    "requirements": {
      "type": "array",
      "minItems": 1,
      "items": { "$ref": "#/definitions/Requirement" }
    },
    "design": { "$ref": "#/definitions/Design" },
    "traceability": { "$ref": "#/definitions/Traceability" },
    "metadata": { "$ref": "#/definitions/Metadata" }
  }
}
```

## Full Schema Location

```text
schemas/canonical-spec.schema.json
```

## Example: Complete Specification

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
  background: |
    Currently, password recovery requires opening a support ticket
    with a 24-48 hour response time.

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
        and:
          - "the reset link expires after 1 hour"
          - "the reset link is single-use"

  - id: "REQ-002"
    text: "IF the email address is not registered, THEN the system SHALL display a generic message without revealing registration status"
    priority: must
    ears_type: unwanted
    acceptance_criteria:
      - id: "AC-002"
        given: "an email address that is not registered"
        when: "someone submits a password reset request with that email"
        then: "the system displays 'If an account exists, a reset link has been sent'"
    notes: "Security measure to prevent user enumeration"

design:
  approach: |
    Token-based reset flow using time-limited single-use tokens
    stored in Redis with 1-hour TTL.
  components:
    - "PasswordResetController"
    - "PasswordResetService"
    - "TokenGenerator"
    - "EmailService"
  dependencies:
    - "Redis for token storage"
    - "SMTP service for email"
  alternatives:
    - name: "Magic link via SMS"
      reason_rejected: "Adds SMS cost and complexity"
    - name: "Security questions"
      reason_rejected: "Poor UX and security concerns"

traceability:
  adr_refs:
    - "ADR-079"
  requirement_refs:
    - "SEC-003"
    - "FR-012"
  epic_ref: "EPIC-015"
  user_story_refs:
    - "US-042"

metadata:
  status: approved
  created: "2025-12-24"
  provider: canonical
  version: "1.0.0"
  bounded_context: "Orchestration"
```
