# Kiro Structure Reference

Detailed file organization patterns for AWS Kiro specifications.

## Directory Structure

### Standard Layout

```text
<project-root>/
├── .kiro/
│   ├── specs/
│   │   ├── requirements.md      # EARS requirements
│   │   ├── design.md            # Technical design
│   │   └── tasks.md             # Task breakdown
│   ├── steering/
│   │   ├── context.md           # Project context
│   │   ├── glossary.md          # Domain terms
│   │   └── conventions.md       # Code conventions
│   └── config.yaml              # Kiro configuration
├── src/                         # Source code
└── ...
```

### Multi-Feature Layout

For projects with multiple features:

```text
.kiro/
├── specs/
│   ├── user-auth/
│   │   ├── requirements.md
│   │   ├── design.md
│   │   └── tasks.md
│   ├── data-export/
│   │   ├── requirements.md
│   │   ├── design.md
│   │   └── tasks.md
│   └── shared/
│       └── common-requirements.md
├── steering/
│   └── context.md
└── config.yaml
```

## File Specifications

### requirements.md

**Purpose:** Define what the system must do using EARS patterns.

**Required Sections:**

| Section | Description |
| --- | --- |
| Context | Background and problem statement |
| Functional Requirements | EARS-formatted requirements |
| Non-Functional Requirements | Performance, security, etc. |

**Requirement Structure:**

```markdown
### FR-<number>: <Title>

**Pattern:** <EARS pattern type>
**Priority:** <Must|Should|Could>
**Status:** <Draft|Approved|Implemented>

<EARS-formatted requirement text>

#### Acceptance Criteria

- [ ] AC-<req>.<number>: Given..., when..., then...
```

**ID Conventions:**

- `FR-1`, `FR-2`, etc. for functional requirements
- `NFR-1`, `NFR-2`, etc. for non-functional requirements
- `AC-1.1`, `AC-1.2` for acceptance criteria (linked to requirement)

### design.md

**Purpose:** Define how the system will implement requirements.

**Required Sections:**

| Section | Description |
| --- | --- |
| Overview | High-level design summary |
| Architecture | Component structure |
| Data Model | Entities and relationships |
| API Design | Endpoints and contracts |
| Technical Decisions | Approach selection with rationale |

**Component Format:**

````markdown
### <ComponentName>

**Responsibility:** <Single sentence describing purpose>

**Dependencies:**
- <Dependency 1>
- <Dependency 2>

**Interface:**
```typescript
interface ComponentName {
  method(param: Type): ReturnType;
}
```
````

### tasks.md

**Purpose:** Break down design into executable tasks.

**Required Sections:**

| Section | Description |
| --- | --- |
| Task List | Phased task breakdown |
| Dependency Graph | Task dependencies |
| Progress | Status summary |

**Task Format:**

```markdown
- [ ] **TSK-<number>**: <Title>
  - Requirement: <FR-x reference>
  - Effort: <S|M|L|XL>
  - Deliverables: <File paths>
  - Acceptance: <How to verify>
```

**Task States:**

| Marker | State |
| --- | --- |
| `- [ ]` | Pending |
| `- [~]` | In Progress |
| `- [x]` | Complete |
| `- [-]` | Blocked |

## config.yaml

### Configuration Options

```yaml
# .kiro/config.yaml

version: "1.0"

project:
  name: "My Project"
  description: "Project description"

specs:
  path: "specs"
  format: "markdown"

steering:
  path: "steering"
  auto_load: true

sync:
  canonical_path: ".specs"
  auto_sync: false

validation:
  require_ears: true
  require_acceptance_criteria: true
  require_priority: true
```

## Naming Conventions

### File Names

| Type | Convention | Example |
| --- | --- | --- |
| Spec files | lowercase, static | `requirements.md` |
| Feature folders | kebab-case | `user-auth/` |
| Steering files | lowercase | `context.md` |

### Requirement IDs

| Pattern | Use Case |
| --- | --- |
| `FR-1` | Functional requirement |
| `NFR-1` | Non-functional requirement |
| `AC-1.1` | Acceptance criterion for FR-1 |
| `TSK-001` | Task (zero-padded) |

## Cross-References

### Linking Requirements to Tasks

In `tasks.md`:

```markdown
- [ ] **TSK-001**: Implement user login
  - Requirement: FR-1, FR-2
```

### Linking Tasks to Code

In task completion:

```markdown
- [x] **TSK-001**: Implement user login
  - Requirement: FR-1, FR-2
  - Deliverables:
    - `src/auth/login.ts`
    - `src/auth/login.test.ts`
  - Commit: `abc123`
```

## Validation Rules

### requirements.md

- [ ] All requirements use EARS patterns
- [ ] All requirements have unique IDs
- [ ] All requirements have priority
- [ ] All functional requirements have acceptance criteria
- [ ] No orphaned acceptance criteria

### design.md

- [ ] All requirements are addressed
- [ ] All components have clear responsibilities
- [ ] Alternatives are documented
- [ ] Data model is complete

### tasks.md

- [ ] All requirements mapped to tasks
- [ ] All tasks have effort estimates
- [ ] Dependencies are documented
- [ ] No circular dependencies
- [ ] Progress section is current

## Migration Patterns

### From User Story to Kiro

1. Extract "As a..." → Context section
2. Extract "I want..." → FR-1 with Event-Driven pattern
3. Extract "So that..." → Motivation in context
4. Convert bullet points → Acceptance criteria

### From Gherkin to Kiro

1. Feature → Context section
2. Background → Preconditions in requirements
3. Scenario → Acceptance criteria
4. Scenario Outline → Parameterized acceptance criteria

### From Canonical to Kiro

1. `context.problem` → Context section
2. `requirements[]` → FR-x entries with EARS
3. `requirements[].acceptance_criteria` → AC-x.y checkboxes
4. `implementation_notes` → design.md content
