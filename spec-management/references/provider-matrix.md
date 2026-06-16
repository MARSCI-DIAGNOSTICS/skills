# Specification Provider Matrix

## Provider Comparison

| Provider | Input Format | Output Format | Best For | Lossless Roundtrip |
| --- | --- | --- | --- | --- |
| `ears` | EARS text | EARS text | Precise requirements | Yes (core fields) |
| `gherkin` | .feature files | .feature files | BDD/Reqnroll tests | Yes (core fields) |
| `kiro` | Kiro JSON/MD | Kiro files | AWS Kiro IDE | Yes (core fields) |
| `speckit` | Spec Kit MD | Spec Kit MD | AI agent prompts | Yes (core fields) |
| `adr` | MADR format | MADR format | Architecture decisions | Partial |
| `userstory` | Agile format | Agile format | Product backlog | Partial |
| `canonical` | YAML/JSON | YAML/JSON | Direct manipulation | Yes (all fields) |

## Provider Details

### EARS Provider (`ears`)

**Input Format:** EARS-formatted text with pattern keywords

**Supported Patterns:**

- Ubiquitous: `The system SHALL...`
- State-Driven: `WHILE..., the system SHALL...`
- Event-Driven: `WHEN..., the system SHALL...`
- Unwanted: `IF..., THEN the system SHALL...`
- Optional: `WHERE..., the system SHALL...`
- Complex: Combinations of patterns

**Best For:**

- Precise, unambiguous requirements
- Formal specification documents
- Requirements that need mathematical rigor

**Canonical Mapping:**

- EARS text → `requirement.text`
- Pattern detection → `requirement.ears_type`
- No native acceptance criteria (generated from context)

### Gherkin Provider (`gherkin`)

**Input Format:** Cucumber .feature files

**Supported Elements:**

- Feature blocks with descriptions
- Scenario and Scenario Outline
- Given/When/Then/And/But steps
- Background sections
- @tags for metadata

**Best For:**

- BDD test automation with Reqnroll
- Executable specifications
- Living documentation

**Canonical Mapping:**

- Feature title → `title`
- Feature description → `context.problem`
- Scenario → Acceptance criterion
- Given → `acceptance_criteria.given`
- When → `acceptance_criteria.when`
- Then → `acceptance_criteria.then`
- And/But → `acceptance_criteria.and[]`
- @tags → `metadata.tags`

### AWS Kiro Provider (`kiro`)

**Input Format:** Kiro specification files

**Supported Files:**

- `requirements.md` - EARS-formatted requirements
- `design.md` - Implementation design
- `tasks.md` - Task breakdown
- Steering files for agent context

**Best For:**

- AWS Kiro IDE integration
- Agent-driven development
- Steering file generation

**Canonical Mapping:**

- Kiro requirements → `requirements[]`
- Kiro design → `design`
- Kiro tasks → External task tracking
- Steering context → Metadata extensions

### GitHub Spec Kit Provider (`speckit`)

**Input Format:** Spec Kit markdown files

**Supported Files:**

- `.constitution.md` - Project principles
- `feature.md` - Feature specification
- `design.md` - Implementation design
- `tasks.md` - Task breakdown

**Best For:**

- GitHub-based development
- AI agent prompts
- 5-phase workflow (Constitution → Specify → Plan → Tasks → Implement)

**Canonical Mapping:**

- Feature content → Full canonical spec
- Constitution → `context.background`
- Design → `design` section
- Tasks → External task tracking

### ADR Provider (`adr`)

**Input Format:** MADR (Markdown Any Decision Records) format

**Supported Sections:**

- Title and Status
- Context and Problem Statement
- Decision Drivers
- Considered Options
- Decision Outcome
- Consequences

**Best For:**

- Architecture decision documentation
- Design rationale capture
- Decision traceability

**Canonical Mapping:**

- Context → `context.problem`
- Decision Drivers → `context.motivation`
- Considered Options → `design.alternatives`
- Decision Outcome → `design.approach`
- Consequences → `design.dependencies`

**Note:** Partial roundtrip - some ADR-specific content may not survive canonical transformation.

### User Story Provider (`userstory`)

**Input Format:** Agile user story format

**Pattern:** As a [role], I want [goal], so that [benefit]

**Supported Elements:**

- Role/persona
- Goal/action
- Benefit/value
- Acceptance criteria (Gherkin format)

**Best For:**

- Product backlog items
- Agile/Scrum workflows
- Persona-based requirements

**Canonical Mapping:**

- "As a..." → Derived `requirement.text`
- "I want..." → `context.problem`
- "So that..." → `context.motivation`
- Acceptance criteria → `acceptance_criteria[]`

**Note:** Partial roundtrip - user story format is more concise than canonical.

### Canonical Provider (`canonical`)

**Input Format:** YAML or JSON matching canonical schema

**Best For:**

- Direct manipulation
- Programmatic creation
- Maximum fidelity

**Canonical Mapping:** Direct 1:1 mapping, all fields preserved.

## Format Detection

Providers implement `CanParse(input)` for automatic format detection:

| Provider | Detection Pattern |
| --- | --- |
| `ears` | Starts with "The system SHALL", "WHILE", "WHEN", "IF...THEN", "WHERE" |
| `gherkin` | Contains "Feature:", "Scenario:", or ends with `.feature` |
| `kiro` | Contains Kiro-specific markers or in `.kiro/` directory |
| `speckit` | Contains `constitution.md` markers or Spec Kit frontmatter |
| `adr` | Contains "# ADR-" or "## Status", "## Context" |
| `userstory` | Matches "As a .*I want .* so that" pattern |
| `canonical` | Valid YAML/JSON with `id`, `title`, `type` fields |

## Conversion Matrix

All conversions go through canonical format:

```text
Source → Canonical → Target

EARS → Canonical → Gherkin    ✓
Gherkin → Canonical → EARS    ✓
Kiro → Canonical → SpecKit    ✓
UserStory → Canonical → ADR   ✓ (partial)
Any → Canonical → Any         ✓
```

## Field Preservation

| Field | EARS | Gherkin | Kiro | SpecKit | ADR | UserStory |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `title` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `type` | ✓ | ✓ | ✓ | ✓ | ⚠ | ⚠ |
| `context.problem` | ⚠ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `context.motivation` | ⚠ | ⚠ | ✓ | ✓ | ✓ | ✓ |
| `requirements[]` | ✓ | ⚠ | ✓ | ✓ | ⚠ | ⚠ |
| `acceptance_criteria[]` | ⚠ | ✓ | ✓ | ✓ | ⚠ | ✓ |
| `design` | ⚠ | ⚠ | ✓ | ✓ | ✓ | ⚠ |
| `traceability` | ⚠ | ⚠ | ✓ | ✓ | ✓ | ⚠ |

**Legend:** ✓ = Full support, ⚠ = Partial/derived support
