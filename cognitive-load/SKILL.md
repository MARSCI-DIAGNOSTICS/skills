---
name: cognitive-load
description: Assess and optimize team cognitive load using cognitive load theory. Use for team health analysis and workload optimization.
allowed-tools: Read, Glob, Grep, Write, Skill, Task
argument-hint: <team> [--depth <quick|standard|detailed>]
---

# /cognitive-load Command

Assess and optimize cognitive load for a team using cognitive load theory.

## Usage

```bash
/cognitive-load "payments team"
/cognitive-load "platform team" depth=detailed
/cognitive-load "all teams" depth=quick
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `team` | Yes | Team name or "all teams" for organization-wide |
| `depth` | No | `quick` (scores only), `standard` (default), `detailed` (full analysis) |

## Depth Levels

### Quick

Rapid assessment producing scores only:

- Intrinsic, extraneous, germane scores
- Total load and status indicator
- One-line recommendation

### Standard (Default)

Complete assessment with recommendations:

- Full scores with breakdown
- Factor-by-factor analysis
- Prioritized recommendations
- Comparison to healthy thresholds

### Detailed

Comprehensive analysis with action plan:

- All standard content
- Root cause analysis for each factor
- Specific action items with owners
- Timeline for improvements
- Success metrics
- Follow-up assessment schedule

## Workflow

### Step 1: Load Cognitive Load Skill

```text
Load: cognitive-load-assessment skill
Purpose: Get assessment framework and questionnaire
```

### Step 2: Gather Team Context

Collect information about the team:

**Team Profile:**

- Team name and size
- Team type (stream-aligned, platform, etc.)
- Domain/bounded context owned
- Services and systems owned
- Duration team has been together

**Current State:**

- Recent changes or challenges
- Known pain points
- Delivery velocity trends
- Team satisfaction indicators

### Step 3: Conduct Assessment

If depth is `quick`:

- Estimate scores based on available information
- Return summary only

If depth is `standard` or `detailed`:

- Score each factor in all three load types
- Document reasoning for each score
- Identify highest-impact factors

### Step 4: Spawn Team Health Assessor (Detailed Only)

For detailed assessments, delegate to `team-health-assessor` agent:

```text
Task: Detailed cognitive load assessment for {team}
Include:
- Full factor analysis
- Root cause identification
- Action plan with timeline
- Success metrics
```

### Step 5: Generate Recommendations

Prioritize recommendations by:

1. **Quick wins** - High impact, low effort (extraneous load)
2. **Strategic changes** - High impact, higher effort (intrinsic load)
3. **Investments** - Protect learning capacity (germane load)

## Output Format

### Quick Depth

```markdown
# Cognitive Load: {Team Name}

| Load Type | Score | Status |
|-----------|-------|--------|
| Intrinsic | {X}/25 | {🟢🟡🔴} |
| Extraneous | {X}/25 | {🟢🟡🔴} |
| Germane | {X}/25 | {🟢🟡🔴} |
| **Total** | **{X}/75** | **{Status}** |

**Recommendation:** {One-line action}
```

### Standard Depth

```markdown
# Cognitive Load Assessment: {Team Name}

## Summary

| Load Type | Score | Status | Key Factor |
|-----------|-------|--------|------------|
| Intrinsic | {X}/25 | {🟢🟡🔴} | {Highest contributor} |
| Extraneous | {X}/25 | {🟢🟡🔴} | {Highest contributor} |
| Germane | {X}/25 | {🟢🟡🔴} | {Highest contributor} |
| **Total** | **{X}/75** | **{Status}** | |

**Interpretation:** {What this means for the team}

## Intrinsic Load (Domain Complexity): {X}/25

| Factor | Score | Notes |
|--------|-------|-------|
| Business domain complexity | {1-5} | {Details} |
| Number of systems owned | {1-5} | {Details} |
| Integration complexity | {1-5} | {Details} |
| Stakeholder coordination | {1-5} | {Details} |
| Compliance requirements | {1-5} | {Details} |

**Analysis:** {Summary of intrinsic load}

## Extraneous Load (Waste): {X}/25

| Factor | Score | Notes |
|--------|-------|-------|
| Tooling/infrastructure friction | {1-5} | {Details} |
| Manual processes | {1-5} | {Details} |
| Technical debt burden | {1-5} | {Details} |
| Waiting time for dependencies | {1-5} | {Details} |
| Context switching frequency | {1-5} | {Details} |

**Analysis:** {Summary of extraneous load - this is WASTE to eliminate}

## Germane Load (Learning): {X}/25

| Factor | Score | Notes |
|--------|-------|-------|
| New technology adoption rate | {1-5} | {Details} |
| Process change frequency | {1-5} | {Details} |
| Skill development demands | {1-5} | {Details} |
| Innovation expectations | {1-5} | {Details} |
| Documentation/training work | {1-5} | {Details} |

**Analysis:** {Summary of germane load - this should be PROTECTED}

## Recommendations

### Reduce Extraneous Load (Priority)
1. {Action} - {Expected impact}
2. {Action} - {Expected impact}

### Manage Intrinsic Load
1. {Action} - {Expected impact}
2. {Action} - {Expected impact}

### Protect Germane Load
1. {Action} - {Expected impact}

## Next Steps
- {Immediate action}
- **Reassess:** {Recommended date}
```

### Detailed Depth

```markdown
# Comprehensive Cognitive Load Assessment: {Team Name}

## Executive Summary

**Overall Status:** {🟢🟡🔴} {Status description}
**Total Load:** {X}/75
**Risk Level:** {Low/Medium/High/Critical}
**Recommended Actions:** {N} immediate, {N} short-term, {N} long-term

## Team Profile

| Attribute | Value |
|-----------|-------|
| Team Size | {N} |
| Team Type | {Type} |
| Domain | {Bounded context} |
| Services Owned | {List} |
| Team Age | {Duration} |

## Load Analysis

[Full standard depth content]

## Root Cause Analysis

### Intrinsic Load Drivers

| Factor | Score | Root Cause | Impact |
|--------|-------|------------|--------|
| {Factor} | {Score} | {Why this is high} | {Effect on team} |

### Extraneous Load Sources

| Factor | Score | Root Cause | Effort to Fix |
|--------|-------|------------|---------------|
| {Factor} | {Score} | {Source of waste} | {H/M/L} |

### Germane Load Pressures

| Factor | Score | Root Cause | Sustainability |
|--------|-------|------------|----------------|
| {Factor} | {Score} | {Why learning load exists} | {Sustainable?} |

## Action Plan

### Immediate Actions (This Week)

| Action | Owner | Success Metric |
|--------|-------|----------------|
| {Action} | {Who} | {How to measure} |

### Short-term Actions (This Quarter)

| Action | Owner | Timeline | Success Metric |
|--------|-------|----------|----------------|
| {Action} | {Who} | {When} | {How to measure} |

### Long-term Actions (Next Quarter+)

| Action | Owner | Timeline | Success Metric |
|--------|-------|----------|----------------|
| {Action} | {Who} | {When} | {How to measure} |

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Team burnout | {H/M/L} | {H/M/L} | {Strategy} |
| Delivery slowdown | {H/M/L} | {H/M/L} | {Strategy} |
| Quality degradation | {H/M/L} | {H/M/L} | {Strategy} |

## Success Metrics

| Metric | Current | Target | Timeline |
|--------|---------|--------|----------|
| Total cognitive load | {X}/75 | <45/75 | {Date} |
| Extraneous load | {X}/25 | <10/25 | {Date} |
| Team satisfaction | {Score} | {Target} | {Date} |
| Delivery velocity | {Current} | {Target} | {Date} |

## Follow-up Schedule

| Date | Assessment Type | Focus |
|------|-----------------|-------|
| {Date} | Quick | Extraneous load reduction |
| {Date} | Standard | Full reassessment |
| {Date} | Detailed | Quarterly review |

## Appendix

### Assessment Methodology
[Brief description of cognitive load theory application]

### Scoring Rubric
[Reference to cognitive-load-assessment skill]

### Team Member Input
[Summary of any team feedback collected]
```

## Scoring Guidelines

```text
SCORING REFERENCE (per factor, 1-5):

1 = Minimal: Rarely an issue, well-managed
2 = Low: Occasional challenge, manageable
3 = Moderate: Regular challenge, noticeable impact
4 = High: Frequent challenge, significant impact
5 = Critical: Constant challenge, severe impact

TOTAL LOAD INTERPRETATION:

< 30: LOW LOAD
- Team has capacity
- Can take on new work
- Good time for innovation

30-45: MODERATE LOAD
- Sustainable workload
- Normal operating range
- Monitor for creep

45-60: HIGH LOAD
- At risk of overload
- Reduce extraneous immediately
- Defer new commitments

> 60: OVERLOADED
- Unsustainable state
- Immediate action required
- Risk of burnout/turnover
```

## Related Commands

- `/team-structure` - Design overall team topology

## Related Skills

- `cognitive-load-assessment` - Full methodology and questionnaire
- `team-topologies` - Team type context

---

**Last Updated:** 2025-12-26
