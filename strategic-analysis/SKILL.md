---
name: strategic-analysis
description: Analyze strategic position and recommend plays based on Wardley Mapping. Use for competitive analysis, evolution planning, and strategic decision-making.
allowed-tools: Read, Glob, Grep, Write, Skill, Task, mcp__perplexity__search, mcp__perplexity__reason
argument-hint: <context> [--perspective competitive|evolution|doctrine|comprehensive]
---

# Strategic Analysis

Analyze strategic position and recommend plays based on Wardley Mapping principles.

## Workflow

### Step 1: Parse Arguments

- **context** (required): The strategic situation to analyze
- **perspective** (optional): competitive | evolution | doctrine | comprehensive

### Step 2: Determine Analysis Scope

Based on perspective:

- **competitive**: Focus on competitive positioning and market plays
- **evolution**: Focus on component evolution and movement
- **doctrine**: Focus on organizational doctrine and capability
- **comprehensive**: All of the above (default)

### Step 3: Research Context

Use MCP servers to gather intelligence:

1. Research industry trends and competitive landscape
2. Identify technology evolution patterns
3. Find relevant case studies and precedents

### Step 4: Conduct Analysis

#### For Competitive Perspective

1. Invoke `strategy-mapmaker` agent for mapping
2. Invoke `strategic-plays` skill for play identification
3. Analyze competitor positions
4. Identify differentiation opportunities
5. Recommend competitive moves

#### For Evolution Perspective

1. Invoke `evolution-analysis` skill
2. Assess current component positions
3. Predict movement trajectories
4. Identify inertia sources
5. Plan evolution strategy

#### For Doctrine Perspective

1. Invoke `doctrine-advisor` agent
2. Assess current doctrine maturity
3. Identify capability gaps
4. Recommend doctrine improvements
5. Plan organizational development

#### For Comprehensive

Execute all three perspectives and synthesize findings.

### Step 5: Synthesize Recommendations

Combine findings into:

1. **Situation Assessment**: Where are you now?
2. **Strategic Options**: What can you do?
3. **Recommended Actions**: What should you do?
4. **Risk Analysis**: What could go wrong?
5. **Success Criteria**: How will you measure?

### Step 6: Return Results

Present comprehensive strategic analysis with prioritized recommendations.

## Examples

### Buy vs Build Decision

```text
/strategic-analysis "buy vs build for authentication"
```

Analyzes the strategic implications of building vs. buying authentication capability.

### Competitive Analysis

```text
/strategic-analysis "market entry strategy" perspective="competitive"
```

Focuses on competitive positioning for market entry.

### Technology Evolution

```text
/strategic-analysis "container orchestration strategy" perspective="evolution"
```

Analyzes the evolution of container orchestration options.

### Organizational Readiness

```text
/strategic-analysis "digital transformation readiness" perspective="doctrine"
```

Assesses organizational doctrine for digital transformation.

## Output Format

```markdown
# Strategic Analysis: [Context]

## Executive Summary
[Key findings and top recommendations in 3-5 bullets]

## Situation Assessment

### Current Position
[Where you are now on the map]

### Competitive Landscape
[Who else is here and where are they positioned]

### Evolution State
[What's evolving and how fast]

## Analysis by Perspective

### Competitive Analysis
[Positioning, threats, opportunities]

### Evolution Analysis
[Movement patterns, timing considerations]

### Doctrine Assessment
[Organizational capability and gaps]

## Strategic Options

| Option | Pros | Cons | Risk | Fit |
|--------|------|------|------|-----|
| [Option 1] | [Benefits] | [Drawbacks] | [Risk level] | [How well it fits] |

## Recommended Strategy

### Primary Recommendation
[What to do and why]

### Supporting Actions
1. [Action 1]
2. [Action 2]
3. [Action 3]

### Timeline
- Immediate: [Actions]
- Short-term (1-3 months): [Actions]
- Medium-term (3-6 months): [Actions]

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | High/Med/Low | High/Med/Low | [How to address] |

## Success Criteria

| Metric | Current | Target | Timeframe |
|--------|---------|--------|-----------|
| [Metric] | [Now] | [Goal] | [When] |

## Next Steps

1. [Immediate next step]
2. [Following step]
3. [Validation step]

## Assumptions and Limitations
- [What was assumed]
- [What couldn't be analyzed]
```

## Analysis Frameworks Used

Depending on context, the analysis may incorporate:

- **ILC Analysis**: Innovate-Leverage-Commoditize opportunities
- **Ecosystem Analysis**: Platform and partner dynamics
- **Pioneer-Settler-Town Planner**: Team structure implications
- **Inertia Analysis**: Resistance to change factors
- **Climatic Patterns**: Industry-wide forces

## Related Commands

- `/wardley-map`: Create a Wardley Map first
- `/doctrine-assessment`: Deep doctrine assessment

## Related Skills

- `strategic-plays`: Strategic gameplay patterns
- `evolution-analysis`: Component evolution assessment
- `doctrine-assessment`: Organizational doctrine evaluation
