# Canonical Specification Format Reference

## Overview

The canonical specification format is a provider-agnostic intermediate representation for specifications. It enables transformation between any two supported formats (EARS, Gherkin, Kiro, SpecKit, ADR, UserStory) via a common model.

**Architecture Source:** ADR-115 - Specification Provider Abstraction

## Full Schema

```yaml
id: "SPEC-{number}"
title: "{Feature/Capability Title}"
type: feature | bug | chore | spike | tech-debt

context:
  problem: |
    Clear description of the problem being solved.
    What pain point or gap does this address?
    Minimum 20 characters.
  motivation: |
    Business value or user benefit.
    Why should we invest in this?
  background: |
    Optional: Additional context, history, or constraints

requirements:
  - id: "REQ-001"
    text: "{EARS-formatted requirement}"
    priority: must | should | could | wont
    ears_type: ubiquitous | state-driven | event-driven | unwanted | complex | optional
    acceptance_criteria:
      - id: "AC-001"
        given: "{Precondition - system state before action}"
        when: "{Action or trigger that occurs}"
        then: "{Expected outcome - observable result}"
        and:
          - "{Additional conditions if needed}"
    notes: "{Optional clarification}"

design:
  approach: "{High-level implementation approach - OPTIONAL}"
  components:
    - "{Component 1 affected or created}"
    - "{Component 2}"
  dependencies:
    - "{External dependency 1}"
    - "{Prerequisite 2}"
  alternatives:
    - name: "{Alternative approach considered}"
      reason_rejected: "{Why this was not chosen}"

traceability:
  adr_refs:
    - "ADR-{number}"
  requirement_refs:
    - "FR-{number}"
    - "NFR-{number}"
  epic_ref: "EPIC-{number}"
  user_story_refs:
    - "US-{number}"

metadata:
  status: draft | review | approved | implemented | deprecated
  created: "{YYYY-MM-DD}"
  provider: canonical | ears | gherkin | kiro | speckit | adr | userstory
  version: "1.0.0"
  bounded_context: "{One of: WorkManagement, Orchestration, Workflows, Expertise, ExecutionControl, TriggerManagement, Integrations}"
```

## Field Descriptions

### Root Fields

| Field | Required | Description |
| --- | --- | --- |
| `id` | Yes | Unique specification identifier (SPEC-XXX format) |
| `title` | Yes | Human-readable feature/capability title |
| `type` | Yes | Specification type for categorization |

### Context Section

| Field | Required | Description |
| --- | --- | --- |
| `problem` | Yes | Clear description of the problem (min 20 chars) |
| `motivation` | Yes | Business value or user benefit |
| `background` | No | Additional context, history, constraints |

### Requirements Section

| Field | Required | Description |
| --- | --- | --- |
| `id` | Yes | Requirement identifier (REQ-XXX format) |
| `text` | Yes | EARS-formatted requirement text |
| `priority` | Yes | MoSCoW priority level |
| `ears_type` | Yes | EARS pattern type |
| `acceptance_criteria` | Yes | List of Given/When/Then criteria |
| `notes` | No | Optional clarification |

### Acceptance Criteria

| Field | Required | Description |
| --- | --- | --- |
| `id` | Yes | Criterion identifier (AC-XXX format) |
| `given` | Yes | Precondition - system state before action |
| `when` | Yes | Action or trigger that occurs |
| `then` | Yes | Expected outcome - observable result |
| `and` | No | Additional conditions if needed |

### Design Section (Optional)

| Field | Required | Description |
| --- | --- | --- |
| `approach` | No | High-level implementation approach |
| `components` | No | List of affected/created components |
| `dependencies` | No | External dependencies and prerequisites |
| `alternatives` | No | Alternative approaches considered |

### Traceability Section

| Field | Required | Description |
| --- | --- | --- |
| `adr_refs` | No | Related Architecture Decision Records |
| `requirement_refs` | No | Related functional/non-functional requirements |
| `epic_ref` | No | Parent EPIC reference |
| `user_story_refs` | No | Related user stories |

### Metadata Section

| Field | Required | Description |
| --- | --- | --- |
| `status` | Yes | Specification lifecycle status |
| `created` | Yes | Creation date (ISO 8601) |
| `provider` | Yes | Source provider that created this spec |
| `version` | No | Semantic version of the specification |
| `bounded_context` | No | Bounded context from ADR-024 |

## Type Values

### Specification Types

| Type | Description |
| --- | --- |
| `feature` | New functionality or capability |
| `bug` | Defect fix |
| `chore` | Maintenance task, no user-visible change |
| `spike` | Research or investigation task |
| `tech-debt` | Technical debt reduction |

### Priority Levels (MoSCoW)

| Priority | Description |
| --- | --- |
| `must` | Non-negotiable, system fails without it |
| `should` | Important but not critical |
| `could` | Desirable if time/resources permit |
| `wont` | Explicitly excluded from this scope |

### EARS Types

| Type | Pattern |
| --- | --- |
| `ubiquitous` | The system SHALL... |
| `state-driven` | WHILE..., the system SHALL... |
| `event-driven` | WHEN..., the system SHALL... |
| `unwanted` | IF..., THEN the system SHALL... |
| `complex` | Combinations of above |
| `optional` | WHERE..., the system SHALL... |

### Status Values

| Status | Description |
| --- | --- |
| `draft` | Initial creation, not reviewed |
| `review` | Under review/refinement |
| `approved` | Approved for implementation |
| `implemented` | Implementation complete |
| `deprecated` | No longer valid/applicable |

## JSON Schema Location

The complete JSON Schema for validation is at:

```text
schemas/canonical-spec.schema.json
```

## Provider Transformation

All providers implement `ISpecificationProvider` with methods:

- `ParseAsync(input)` → `CanonicalSpec`
- `GenerateAsync(spec)` → Provider-specific output
- `ValidateAsync(spec)` → Validation results
- `CanParse(input)` → Boolean detection

This enables any-to-any format conversion via the canonical intermediate.
