---
name: team-structure
description: Design team topology using Team Topologies principles. Use for organizational design, team restructuring, or evolving team structure.
allowed-tools: Read, Glob, Grep, Write, Skill, Task
argument-hint: <context> [--teams <N>] [--mode <design|analyze|evolve>]
---

# /team-structure Command

Design team topology for an organization using Team Topologies principles.

## Usage

```bash
/team-structure "e-commerce platform"
/team-structure "data platform" teams=5
/team-structure "current org" mode=analyze
/team-structure "microservices migration" mode=evolve
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `context` | Yes | Organization, product, or system to design teams for |
| `teams` | No | Target number of teams (helps constrain design) |
| `mode` | No | `design` (default), `analyze`, or `evolve` |

## Modes

### Design Mode (Default)

Create a new team structure from scratch:

1. Analyze architecture/bounded contexts
2. Identify team types needed
3. Map contexts to teams
4. Define interaction patterns
5. Assess cognitive load
6. Produce structure recommendation

### Analyze Mode

Evaluate an existing team structure:

1. Map current teams and responsibilities
2. Classify team types
3. Identify anti-patterns
4. Assess cognitive load
5. Score interaction health
6. Recommend improvements

### Evolve Mode

Plan evolution from current to target state:

1. Document current structure
2. Define target structure
3. Identify gaps
4. Plan transition phases
5. Define success criteria
6. Create roadmap

## Workflow

### Step 1: Load Skills

Load required skills for team design guidance:

```text
Skills to load:
- team-topologies (team type definitions)
- inverse-conway (architecture alignment)
- cognitive-load-assessment (load analysis)
- interaction-patterns (interaction modes)
- team-api-design (team interfaces)
```

### Step 2: Gather Context

Based on mode, gather relevant information:

**For Design Mode:**

- Architecture documentation
- Bounded context map
- Business value streams
- Technical complexity areas
- Organizational constraints

**For Analyze Mode:**

- Current team list and composition
- Team responsibilities
- Current pain points
- Delivery metrics (if available)
- Known friction areas

**For Evolve Mode:**

- Current state (teams, interactions)
- Target architecture
- Business drivers for change
- Timeline constraints
- Risk tolerance

### Step 3: Spawn Team Architect Agent

Delegate to the `team-architect` agent for comprehensive analysis:

```text
Task: Design team structure for {context}
Mode: {mode}
Constraints: {teams if specified}

Provide:
- Team type recommendations
- Bounded context mapping
- Interaction patterns
- Cognitive load assessment
- Evolution roadmap (if evolve mode)
```

### Step 4: Present Results

Present the team structure design with:

1. **Executive Summary** - One paragraph overview
2. **Team Structure Diagram** - Visual representation
3. **Team Details** - Each team's type, mission, ownership
4. **Interaction Map** - How teams work together
5. **Cognitive Load Summary** - Load per team
6. **Recommendations** - Prioritized action items
7. **Risks** - Potential issues and mitigations

## Output Format

```markdown
# Team Structure: {context}

## Summary
{One paragraph overview of recommended structure}

## Team Structure Diagram
```text
{ASCII diagram showing teams and relationships}
```

## Teams ({N} total)

### Stream-Aligned Teams ({N})

| Team | Mission | Bounded Context |
|------|---------|-----------------|
| {Name} | {Mission} | {Context} |

### Platform Teams ({N})

| Team | Mission | Capabilities |
|------|---------|--------------|
| {Name} | {Mission} | {What they provide} |

### Enabling Teams ({N})

| Team | Focus | Current Engagements |
|------|-------|---------------------|
| {Name} | {Focus} | {Who they're helping} |

### Complicated-Subsystem Teams ({N})

| Team | Specialist Area | Interface |
|------|-----------------|-----------|
| {Name} | {Specialization} | {How others consume} |

## Interaction Patterns

{ASCII diagram showing interaction modes}

| From | To | Mode | Notes |
|------|----|------|-------|
| {Team} | {Team} | {Mode} | {Details} |

## Cognitive Load Summary

| Team | Load Score | Status |
|------|------------|--------|
| {Team} | {X/75} | {🟢🟡🔴} |

## Recommendations

### Immediate

1. {Action}
2. {Action}

### Short-term

1. {Action}
2. {Action}

### Long-term

1. {Action}
2. {Action}

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| {Risk} | {Impact} | {Strategy} |

## Examples

### Example 1: E-commerce Platform

```bash
/team-structure "e-commerce platform"
```

Output highlights:

- 6 stream-aligned teams (Catalog, Cart, Checkout, Payments, Fulfillment, Customer)
- 1 platform team (Developer Platform)
- 1 enabling team (DevOps Enablement)
- 1 complicated-subsystem team (Search/Recommendations)

### Example 2: Analyze Existing Structure

```bash
/team-structure "current org" mode=analyze
```

Output highlights:

- 12 teams analyzed
- 3 anti-patterns identified (layer-oriented teams, shared service bottleneck)
- Cognitive load issues in 2 teams
- Recommendations for restructuring

### Example 3: Plan Evolution

```bash
/team-structure "monolith to microservices" mode=evolve
```

Output highlights:

- Current: 2 large teams
- Target: 5 stream-aligned teams + platform
- 3-phase transition plan
- Risk mitigations for each phase

## Related Commands

- `/cognitive-load` - Deep dive on cognitive load for a team
- `/wardley-map` - Strategic analysis for team positioning

## Related Skills

- `team-topologies` - Team type definitions and patterns
- `inverse-conway` - Architecture-team alignment
- `cognitive-load-assessment` - Load measurement methodology
- `interaction-patterns` - Interaction mode guidance

---

**Last Updated:** 2025-12-26
