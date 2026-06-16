---
name: doc-architecture
description: Generate architecture documentation using arc42 or C4 model. Use for creating system context, container, and component diagrams with narrative.
allowed-tools: Read, Glob, Grep, Write, Skill
argument-hint: <subject> [--format arc42|c4|both] [--level context|container|component]
---

# Generate Architecture Documentation

Create comprehensive architecture documentation for a system or component.

## Process

### 1. Parse Arguments

Extract from user input:

- **Subject**: System/component to document (required)
- **Format**: `arc42`, `c4`, or `both` (default: `c4`)
- **Level**: For C4 - `context`, `container`, or `component` (default: `container`)

### 2. Analyze System

Explore the codebase to understand:

1. **System boundaries**: What is in scope?
2. **External dependencies**: What systems does it interact with?
3. **Internal structure**: How is it organized?
4. **Technology stack**: What technologies are used?
5. **Key flows**: What are the important scenarios?

Use file exploration to gather information:

- Solution/project files for structure
- Configuration files for dependencies
- Entry points for architecture clues
- Existing documentation

### 3. Generate Documentation

Based on the format argument:

**If format = c4:**

1. Load the `c4-documentation` skill
2. Generate diagrams at the requested level:
   - **context**: System with users and external systems
   - **container**: Internal applications and data stores
   - **component**: Internal structure of a container
3. Include narrative description with each diagram

**If format = arc42:**

1. Load the `arc42-documentation` skill
2. Generate relevant sections:
   - Introduction and Goals
   - Architecture Constraints
   - System Scope and Context
   - Solution Strategy
   - Building Block View
   - Runtime View (key scenarios)
   - Deployment View
   - Cross-cutting Concepts

**If format = both:**

1. Generate arc42 document
2. Embed C4 diagrams in appropriate sections

### 4. Output Structure

Create documentation file(s):

```text
For C4:
docs/architecture/
└── {subject}-c4-{level}.md

For arc42:
docs/architecture/
└── {subject}-arc42.md

For both:
docs/architecture/
├── {subject}-architecture.md  # arc42 with embedded C4
└── diagrams/
    ├── context.mmd
    ├── container.mmd
    └── component.mmd
```

### 5. Include in Output

Every generated document should include:

1. **Header with metadata**
   - Title
   - Last updated date
   - Author (if known)
   - Version

2. **Diagrams** (Mermaid format)
   - Properly formatted C4 diagrams
   - Legend if needed

3. **Narrative**
   - Context and purpose
   - Key decisions and rationale
   - Technology choices
   - Trade-offs acknowledged

4. **References**
   - Links to related docs
   - External resources
   - ADRs if applicable

## Example Invocations

```text
/doc-architecture "order service"
→ Generates C4 container diagram for order service

/doc-architecture "payment gateway" format=arc42
→ Generates full arc42 documentation

/doc-architecture "api gateway" format=c4 level=component
→ Generates C4 component diagram

/doc-architecture "entire system" format=both level=context
→ Generates arc42 with embedded C4 context diagram
```

## Quality Criteria

Generated documentation must:

- [ ] Accurately reflect the system structure
- [ ] Use consistent terminology
- [ ] Include valid Mermaid/PlantUML syntax
- [ ] Explain the "why" not just the "what"
- [ ] Be actionable for readers
- [ ] Follow project documentation conventions
