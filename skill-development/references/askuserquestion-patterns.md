# AskUserQuestion Tool Patterns

Best practices for using the `AskUserQuestion` tool in skills and commands.

## Tool Constraints

| Constraint | Value |
|------------|-------|
| Questions per call | 1-4 |
| Options per question | 2-4 |
| Header max length | 12 characters |
| Response timeout | 60 seconds |
| User "Other" option | Always available |

## Critical Limitation

**AskUserQuestion is NOT available in subagents (Task tool spawns).**

Commands/skills must gather all needed context BEFORE spawning agents.

## Established Usage Patterns

### 1. Interactive Workshops

Multi-step discovery sessions with progressive question flows.

```yaml
# Question 1: Mode selection
question: "Which workshop mode do you need?"
header: "Mode"
options:
  - label: "Full Simulation (Recommended)"
    description: "Comprehensive with all personas (~15K tokens)"
  - label: "Quick"
    description: "Single pass, faster execution (~3K tokens)"
  - label: "Guided"
    description: "Interactive, step-by-step with confirmations"
```

### 2. Scope Selection (Standard Pattern)

Use this pattern for any skill/command with variable depth.

```yaml
question: "How comprehensive should the output be?"
header: "Scope"
options:
  - label: "MVP (Recommended)"
    description: "Essential elements only, fast execution"
  - label: "Standard"
    description: "Balanced coverage and detail"
  - label: "Comprehensive"
    description: "Full analysis, all edge cases"
```

### 3. Destructive Operation Confirmation

**CRITICAL safety pattern** - always confirm before destructive actions.

```yaml
question: "Delete {count} files ({size})? This cannot be undone."
header: "Confirm"
options:
  - label: "Yes, delete files"
    description: "Permanently remove the selected files"
  - label: "No, cancel"
    description: "Keep files and abort operation"
```

### 4. Discovery Mode Selection

For multi-mode skills with different approaches.

```yaml
question: "How should entities be discovered?"
header: "Discovery"
options:
  - label: "From Description"
    description: "Extract from domain description provided"
  - label: "Interactive"
    description: "Walk through discovery with me"
  - label: "Codebase Analysis"
    description: "Analyze existing code structure"
  - label: "From Prior Work"
    description: "Use output from previous session"
```

### 5. Output Format Selection (multiSelect)

When users may want multiple output formats.

```yaml
question: "What output formats do you need?"
header: "Format"
multiSelect: true
options:
  - label: "Markdown"
    description: "Human-readable documentation"
  - label: "Mermaid"
    description: "Visual diagrams"
  - label: "YAML/JSON"
    description: "Structured data for tools"
```

## CLI Best Practices

### Use "(Recommended)" Suffix

Always mark the sensible default with "(Recommended)" in the label:

```yaml
- label: "Composition (Recommended)"
  description: "Build types from reusable parts - maximum flexibility"
```

### Headers Must Be Concise

Headers are displayed as chips/tags. Examples of good headers:

| Good (≤12 chars) | Bad (>12 chars) |
|------------------|-----------------|
| Mode | Workshop Mode |
| Scope | Analysis Depth |
| Discovery | Entity Discovery Mode |
| Depth | Modeling Depth Level |
| Clarity | Relationship Clarity |

### One Decision Per Question

Each question should represent one clear decision point:

- Scope selection (MVP vs Full)
- Mode selection (Quick vs Thorough vs Guided)
- Discovery approach (Interactive vs Automated)
- Output format (Markdown vs YAML vs Visual)

### Description Explains Implications

Descriptions should explain what happens if selected:

```yaml
# Good - explains the implication
- label: "Full Analysis"
  description: "Systematically analyze all bounded contexts with CML output"

# Bad - just restates the label
- label: "Full Analysis"
  description: "Performs a full analysis"
```

## MCP-Grounded Question Schemas

Questions should cite domain methodology sources in comments:

```yaml
# Question 1: Mapping Mode (MCP: DDD context mapping methodology)
question: "What level of context mapping analysis do you need?"
```

Source examples:

- `(MCP: CLI best practices - scope selection)`
- `(MCP: DDD bounded context patterns)`
- `(MCP: Event Storming methodology)`
- `(MCP: SEI Quality Attribute Workshop)`
- `(MCP: Data modeling progression)`

## Skill Integration Pattern

Add to SKILL.md frontmatter:

```yaml
allowed-tools: Read, Glob, Grep, Skill, Task, AskUserQuestion
```

Add Interactive Configuration section after frontmatter, before main content:

```markdown
## Interactive [Workshop/Modeling/Analysis] Configuration

Use AskUserQuestion to configure the session:

\`\`\`yaml
# Question 1: [Purpose] (MCP: [source])
question: "[question text]"
header: "[≤12 chars]"
options:
  - label: "[option] (Recommended)"
    description: "[implication]"
  - label: "[option]"
    description: "[implication]"
\`\`\`

Use these responses to [calibrate/determine/select] ...
```

## Anti-Patterns

### Header Too Long

```yaml
# Bad
header: "Analysis Depth"  # 14 chars, exceeds limit

# Good
header: "Depth"  # 5 chars
```

### Too Many Options

```yaml
# Bad - 6 options (max is 4)
options:
  - label: "Option 1"
  - label: "Option 2"
  - label: "Option 3"
  - label: "Option 4"
  - label: "Option 5"
  - label: "Option 6"

# Good - consolidate or use follow-up questions
options:
  - label: "Quick"
  - label: "Standard"
  - label: "Thorough"
  - label: "Custom"  # User can provide details via "Other"
```

### Missing Default Indicator

```yaml
# Bad - no clear default
options:
  - label: "Option A"
  - label: "Option B"
  - label: "Option C"

# Good - clear default
options:
  - label: "Option A (Recommended)"
  - label: "Option B"
  - label: "Option C"
```

### Vague Descriptions

```yaml
# Bad
- label: "Full"
  description: "Does more"

# Good
- label: "Full Analysis"
  description: "Analyze all bounded contexts with CML output (~15K tokens)"
```

## Related Documentation

- **skill-development** skill - Skill and command creation best practices
- **validation-checklist.md** - YAML frontmatter validation

---

**Last Updated:** 2026-01-10
