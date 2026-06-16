---
name: slo-workshop
description: Interactive SLO definition workshop - guides through defining SLIs, setting SLO targets, and establishing error budget policies for a service
allowed-tools: Read, Glob, Grep, Task, AskUserQuestion
argument-hint: [service-name-or-context]
---

# SLO Workshop Command

This command runs an interactive workshop to help define SLOs (Service Level Objectives) for a service.

## Purpose

Guide teams through the complete SLO definition process:

1. Identifying critical user journeys
2. Selecting appropriate SLIs (Service Level Indicators)
3. Setting realistic SLO targets
4. Establishing error budget policies
5. Designing alerting strategies

## Workflow

### Phase 1: Service Understanding

First, understand the service context:

**If a service name or file is provided:**

- Search the codebase for the service
- Identify endpoints, dependencies, and user-facing functionality
- Look for existing metrics, SLOs, or monitoring configuration

**Gather context through questions:**

1. What does this service do for users?
2. Who are the primary users (internal/external)?
3. What are the critical user journeys?
4. What does "working correctly" mean for users?

### Phase 2: SLI Selection

Guide through selecting meaningful SLIs:

**Present SLI categories:**

```text
Common SLI Types:

1. Availability
   "Can users access the service?"
   Measurement: Successful requests / Total requests

2. Latency
   "How fast does the service respond?"
   Measurement: Request duration at percentile (p50, p90, p99)

3. Correctness
   "Does the service return correct results?"
   Measurement: Correct responses / Total responses

4. Throughput
   "Can the service handle the load?"
   Measurement: Requests processed per time unit

5. Freshness
   "How current is the data?"
   Measurement: Age of data served to users
```

**For each relevant SLI type, define:**

- What counts as a "good" event
- What counts as a "valid" event (denominator)
- How it will be measured (metrics, logs, synthetic)

### Phase 3: SLO Target Setting

Help set appropriate targets:

**Consider factors:**

- Current baseline (what are we achieving today?)
- User expectations (what do users need?)
- Engineering capacity (what can we sustain?)
- Business requirements (what's contractually required?)

**Provide guidance:**

```text
SLO Target Guidance:

Starting Point Recommendations:
- Availability: Start at current baseline - 0.1%
- Latency: Start at current p99 + 20% buffer

Common Targets:
- 99.9% = 43 minutes downtime/month
- 99.5% = 3.6 hours downtime/month
- 99% = 7.3 hours downtime/month

Tips:
- Don't start at 100% (impossible to maintain)
- Don't set targets you can't measure
- Conservative targets are easier to achieve
- You can tighten targets over time
```

### Phase 4: Error Budget Policy

Define what happens when the error budget is consumed:

**Error budget calculation:**

```text
Error Budget = 100% - SLO Target

Example:
SLO = 99.9% availability
Error Budget = 0.1% = 43.2 minutes/month
```

**Policy framework:**

```text
Error Budget Policy Template:

Budget > 50%:
- Normal development velocity
- Standard change process

Budget 25-50%:
- Increased review for risky changes
- Prioritize reliability improvements

Budget < 25%:
- Pause non-critical feature work
- Focus on reliability improvements

Budget exhausted:
- Stop all non-critical deployments
- All hands on reliability
- Postmortem for budget-burning incidents
```

### Phase 5: Alerting Strategy

Design multi-window burn rate alerting:

**Explain burn rate concept:**

```text
Burn Rate Alerting:

Burn rate = Rate of consuming error budget

1x burn rate = Exactly consuming monthly budget
2x burn rate = Will exhaust budget in 15 days
10x burn rate = Will exhaust budget in 3 days

Multi-window alerts:
- Fast burn: 14.4x rate over 1 hour (page)
- Slow burn: 3x rate over 3 days (ticket)
```

#### Define alert thresholds based on SLO targets

### Phase 6: Documentation

Generate SLO documentation:

```text
# [Service Name] SLO Definition

## Service Overview
[Description from workshop]

## Critical User Journeys
1. [Journey 1]
2. [Journey 2]

## SLIs

### [SLI Name]
- Type: [Availability/Latency/etc.]
- Definition: [How measured]
- Good event: [What counts as good]
- Valid event: [What counts as valid]

## SLO Targets

| SLI | Target | Window | Error Budget |
|-----|--------|--------|--------------|
| [SLI 1] | [%] | [days] | [time] |

## Error Budget Policy

### Budget > 50%
[Actions]

### Budget 25-50%
[Actions]

### Budget < 25%
[Actions]

### Budget Exhausted
[Actions]

## Alerting

| Alert | Burn Rate | Window | Severity |
|-------|-----------|--------|----------|
| [Name] | [rate]x | [time] | [Page/Ticket] |

## Review Schedule
- Quarterly SLO review
- Monthly error budget review
- After significant incidents
```

## Usage Examples

```bash
# Start workshop for a specific service
/sd:slo-workshop order-service

# Start workshop with context file
/sd:slo-workshop @docs/services/payment-api.md

# Start general workshop
/sd:slo-workshop
```

## Interactive Elements

Throughout the workshop, use `AskUserQuestion` to:

- Gather service context
- Validate SLI selections
- Confirm target appropriateness
- Review error budget policies

## Output

The workshop produces:

1. **SLO Definition Document** - Complete SLO specification
2. **Implementation Checklist** - Steps to implement the SLOs
3. **Review Schedule** - When to revisit and adjust

## Related Skills

This command leverages:

- `slo-sli-error-budget` - SLO methodology details
- `observability-patterns` - Measurement approaches
- `distributed-tracing` - Trace-based SLIs

## Related Agent

For SLO consultation without interactive workshop:

- `observability-consultant` - General observability guidance
