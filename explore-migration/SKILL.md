---
name: explore-migration
description: Explore migration paths when planning architecture changes. Documents current state, identifies options with trade-offs for informed decision-making.
allowed-tools: Read, Glob, Grep, Task
argument-hint: "<target-state-description>"
---

# Explore Migration Command

Explore technical migration options by analyzing current architecture and documenting possible paths with trade-offs.

## Usage

```text
/enterprise-architecture:explore-migration <target-state-description>
```

## Arguments

- `target-state-description` (required): Description of the desired end state
  - Examples: "microservices", "cloud-native", "event-driven", "containerized"

## Examples

```text
/enterprise-architecture:explore-migration microservices architecture
/enterprise-architecture:explore-migration migrate from monolith to modular monolith
/enterprise-architecture:explore-migration replace legacy ORM with modern data access
```

## Workflow

1. **Analyze Current State**
   - Scan codebase for architecture patterns
   - Identify dependencies and coupling
   - Document current technology stack

2. **Spawn Migration Explorer Agent**
   Use the `migration-explorer` agent to explore options. The agent:
   - Documents current state architecture
   - Identifies multiple migration paths
   - Analyzes trade-offs for each path
   - Explores rather than prescribes

3. **Present Migration Options**
   Display options organized by:
   - **Current State Summary**
   - **Migration Options** (with trade-offs)
   - **Risk Assessment**
   - **Next Steps for Planning**

## Important Note

This command explores technical options. Complete migration planning requires additional business context (budget, team capacity, timeline, compliance needs). The output should inform broader planning discussions, not replace them.

## Output Format

```text
## Migration Exploration: [Target State]

### Scope of This Analysis
This document explores technical migration options based on code structure analysis.
Complete migration planning requires additional business context:
- Budget constraints and approval processes
- Team capacity and skill availability
- Business timeline requirements
- Risk tolerance and compliance needs

### Current State
- Architecture pattern: [identified]
- Key dependencies: [list]
- Technical debt areas: [identified]

### Migration Option 1: [Name]
**Approach:** [Description]
**Pros:**
- [benefit]
**Cons:**
- [drawback]
**Estimated complexity:** [Low/Medium/High]

### Migration Option 2: [Name]
[Same structure]

### Migration Option 3: [Name]
[Same structure]

### Trade-off Comparison
| Factor | Option 1 | Option 2 | Option 3 |
| --- | --- | --- | --- |
| Complexity | ... | ... | ... |
| Risk | ... | ... | ... |
| Reversibility | ... | ... | ... |

### Recommended Next Steps
1. [Planning activity]
2. [Validation step]
3. [Stakeholder discussion]
```
