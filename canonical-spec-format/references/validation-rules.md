# Canonical Specification Validation Rules

## Validation Categories

1. **Structural Validation** - Schema compliance
2. **Content Validation** - Field value correctness
3. **EARS Pattern Validation** - Requirement text format
4. **Cross-Reference Validation** - Internal consistency
5. **Quality Validation** - Best practices

## Structural Validation Rules

### Required Fields

| Path | Type | Rule |
| --- | --- | --- |
| `id` | string | Must be present, non-empty |
| `title` | string | Must be present, non-empty |
| `type` | enum | Must be valid type value |
| `context.problem` | string | Must be present |
| `context.motivation` | string | Must be present |
| `requirements` | array | Must have at least one item |
| `metadata.status` | enum | Must be valid status value |
| `metadata.created` | string | Must be valid ISO 8601 date |
| `metadata.provider` | string | Must be present |

### Requirement Fields

| Path | Type | Rule |
| --- | --- | --- |
| `requirements[].id` | string | Must be present, unique |
| `requirements[].text` | string | Must be present, non-empty |
| `requirements[].priority` | enum | Must be valid priority value |
| `requirements[].ears_type` | enum | Must be valid EARS type |
| `requirements[].acceptance_criteria` | array | Must have at least one item |

### Acceptance Criteria Fields

| Path | Type | Rule |
| --- | --- | --- |
| `acceptance_criteria[].id` | string | Must be present, unique within requirement |
| `acceptance_criteria[].given` | string | Must be present, non-empty |
| `acceptance_criteria[].when` | string | Must be present, non-empty |
| `acceptance_criteria[].then` | string | Must be present, non-empty |

## Content Validation Rules

### ID Formats

| Field | Pattern | Valid Examples | Invalid Examples |
| --- | --- | --- | --- |
| `id` | `SPEC-\d+` | SPEC-001, SPEC-42 | S-001, SPEC001 |
| `requirements[].id` | `REQ-\d+` | REQ-001, REQ-123 | R-001, REQ |
| `acceptance_criteria[].id` | `AC-\d+` | AC-001, AC-999 | A-001, AC |
| `adr_refs[]` | `ADR-\d+` | ADR-115, ADR-001 | ADR, A-115 |
| `epic_ref` | `EPIC-\d+` | EPIC-1118 | E-1118, EPIC |
| `user_story_refs[]` | `US-\d+` | US-042, US-001 | U-042, US |

### Content Constraints

| Field | Constraint | Error Message |
| --- | --- | --- |
| `context.problem` | minLength: 20 | "Problem description must be at least 20 characters" |
| `metadata.created` | ISO 8601 date | "Created date must be valid ISO 8601 format (YYYY-MM-DD)" |
| `metadata.version` | Semantic version | "Version must follow semantic versioning (X.Y.Z)" |

### Enum Validation

| Field | Valid Values |
| --- | --- |
| `type` | feature, bug, chore, spike, tech-debt |
| `priority` | must, should, could, wont |
| `ears_type` | ubiquitous, state-driven, event-driven, unwanted, complex, optional |
| `status` | draft, review, approved, implemented, deprecated |
| `bounded_context` | WorkManagement, Orchestration, Workflows, Expertise, ExecutionControl, TriggerManagement, Integrations |

## EARS Pattern Validation

Each requirement's `text` must match its declared `ears_type`:

### Ubiquitous Pattern

```text
ears_type: ubiquitous
Pattern: The <entity> SHALL <action>
```

**Valid:**

- "The system SHALL encrypt all data at rest"
- "The API SHALL respond in JSON format"

**Invalid:**

- "WHEN user clicks, the system SHALL..." (event-driven, not ubiquitous)
- "System should encrypt..." (wrong keyword)

### State-Driven Pattern

```text
ears_type: state-driven
Pattern: WHILE <condition>, the <entity> SHALL <action>
```

**Valid:**

- "WHILE in maintenance mode, the system SHALL display a banner"
- "WHILE the connection is active, the system SHALL send heartbeats"

**Invalid:**

- "The system SHALL..." (no WHILE clause)
- "WHEN active, the system SHALL..." (WHEN, not WHILE)

### Event-Driven Pattern

```text
ears_type: event-driven
Pattern: WHEN <trigger>, the <entity> SHALL <action>
```

**Valid:**

- "WHEN a user submits the form, the system SHALL validate inputs"
- "WHEN an error occurs, the system SHALL log the details"

**Invalid:**

- "The system SHALL validate..." (no WHEN clause)
- "IF user submits, THEN..." (IF-THEN, not WHEN)

### Unwanted Behavior Pattern

```text
ears_type: unwanted
Pattern: IF <condition>, THEN the <entity> SHALL <action>
```

**Valid:**

- "IF authentication fails, THEN the system SHALL lock the account"
- "IF the database is unavailable, THEN the system SHALL queue requests"

**Invalid:**

- "WHEN error occurs..." (WHEN, not IF-THEN)
- "The system SHALL handle errors" (no IF-THEN clause)

### Optional Feature Pattern

```text
ears_type: optional
Pattern: WHERE <feature/config>, the <entity> SHALL <action>
```

**Valid:**

- "WHERE dark mode is enabled, the system SHALL use dark theme"
- "WHERE audit logging is configured, the system SHALL log access"

**Invalid:**

- "IF dark mode is enabled..." (IF, not WHERE)
- "The system SHALL support dark mode" (no WHERE clause)

### Complex Pattern

```text
ears_type: complex
Pattern: Combination of multiple patterns
```

**Valid:**

- "WHILE active, WHEN timeout occurs, the system SHALL..."
- "WHILE in prod mode, IF error occurs, THEN the system SHALL..."

**Invalid:**

- "WHEN user clicks, the system SHALL..." (single pattern, not complex)

## Cross-Reference Validation

### ID Uniqueness

| Scope | Rule |
| --- | --- |
| `requirements[].id` | Unique across all requirements |
| `acceptance_criteria[].id` | Unique within parent requirement |

### Reference Integrity

| Reference Field | Target |
| --- | --- |
| `adr_refs[]` | Should reference existing ADRs |
| `epic_ref` | Should reference existing EPIC |
| `requirement_refs[]` | Should reference existing FR/NFR |
| `user_story_refs[]` | Should reference existing user stories |

## Quality Validation Rules

### Best Practices (Warnings)

| Rule | Message |
| --- | --- |
| Requirement without notes for complex logic | "Consider adding notes to explain complex requirement" |
| More than 5 acceptance criteria per requirement | "Consider splitting requirement for testability" |
| Generic problem description | "Problem description should be specific and measurable" |
| Missing traceability | "Consider adding traceability links" |

### Anti-Patterns (Errors)

| Pattern | Message |
| --- | --- |
| "should" instead of "SHALL" | "Use 'SHALL' for requirements, not 'should'" |
| Passive voice | "Use active voice: 'The system SHALL...' not 'Data shall be...'" |
| Multiple requirements in one | "Split into separate requirements for testability" |
| Implementation details in requirement | "Requirements specify 'what', not 'how'" |

## Validation Error Format

```yaml
errors:
  - path: "requirements[0].text"
    rule: "ears_pattern_match"
    message: "Requirement text does not match declared ears_type 'event-driven'. Expected to start with 'WHEN'"
    severity: error

  - path: "context.problem"
    rule: "min_length"
    message: "Problem description must be at least 20 characters (currently 15)"
    severity: error

warnings:
  - path: "traceability"
    rule: "missing_traceability"
    message: "Consider adding ADR or requirement references for traceability"
    severity: warning
```

## Validation Command

```bash
/spec:validate path/to/specification.yaml
```

Output:

```text
✓ Structural validation: PASS
✓ Content validation: PASS
✓ EARS pattern validation: PASS
⚠ Cross-reference validation: 1 warning
  - adr_refs: ADR-999 not found (may be external)
✓ Quality validation: PASS

Result: VALID (1 warning)
```
