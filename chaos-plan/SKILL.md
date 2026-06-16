---
name: chaos-plan
description: Design chaos engineering experiments for a system - identifies failure modes, creates experiment hypotheses, and generates GameDay plans
allowed-tools: Read, Glob, Grep, Task, AskUserQuestion
argument-hint: <system-or-service-name>
---

# Chaos Plan Command

This command helps design chaos engineering experiments and GameDay plans for a system.

## Purpose

Generate comprehensive chaos engineering plans including:

1. System resilience assessment
2. Failure mode identification
3. Experiment hypotheses and designs
4. GameDay planning
5. Safety measures and rollback procedures

## Workflow

### Phase 1: System Discovery

First, understand the system:

**If a system/service name is provided:**

- Search the codebase for service definitions
- Identify dependencies and integrations
- Look for existing resilience patterns (circuit breakers, retries)
- Check for monitoring and alerting configuration

**Analyze architecture:**

```text
System Analysis Checklist:
□ Service boundaries and responsibilities
□ External dependencies (databases, APIs, queues)
□ Internal service dependencies
□ Data flows and critical paths
□ Current resilience patterns in place
□ Existing monitoring and observability
```

### Phase 2: Failure Mode Identification

Identify potential failure modes:

**Infrastructure failures:**

- Instance/container crashes
- Network partitions between services
- Disk exhaustion
- Memory pressure
- CPU saturation

**Application failures:**

- Service unavailability
- Slow responses / latency spikes
- Error responses
- Connection pool exhaustion
- Resource leaks

**Dependency failures:**

- Database failover/unavailability
- Cache miss/unavailability
- External API timeout/failure
- Message queue backup

**Data failures:**

- Corrupted data
- Stale data (replication lag)
- Schema incompatibility

### Phase 3: Steady State Definition

Define what "healthy" looks like:

**Identify key metrics:**

```text
Steady State Metrics:

Request-based (RED):
- Request rate: [baseline] requests/sec
- Error rate: < [threshold]%
- Duration (p99): < [threshold]ms

Resource-based (USE):
- CPU utilization: < [threshold]%
- Memory utilization: < [threshold]%
- Queue depth: < [threshold]

Business metrics:
- [Metric 1]: [baseline/threshold]
- [Metric 2]: [baseline/threshold]
```

### Phase 4: Experiment Design

Design experiments for identified failure modes:

**For each priority failure mode, create:**

```text
Experiment: [Name]

Hypothesis:
"When [fault condition] occurs, [system component] will
[expected behavior] because [reasoning]."

Fault Injection:
- Type: [Latency/Error/Termination/Partition/etc.]
- Target: [Service/instance/dependency]
- Magnitude: [Degree of fault]
- Duration: [How long]

Blast Radius:
- Affected components: [List]
- User impact estimate: [Percentage/description]

Abort Conditions:
- Error rate > [threshold]
- Latency p99 > [threshold]
- [Business metric] breached
- Customer complaints received

Rollback Steps:
1. [Step to revert fault]
2. [Step to verify recovery]

Success Criteria:
□ [Metric] remains within [bounds]
□ [Recovery] happens within [time]
□ [Alerts] fire as expected
```

### Phase 5: Experiment Prioritization

Prioritize experiments by:

**Risk-based prioritization:**

| Factor | Weight |
|--------|--------|
| Likelihood of failure | High |
| Impact if it occurs | High |
| Current uncertainty | Medium |
| Ease of testing | Low |

**Recommended order:**

1. High impact + high uncertainty
2. High impact + low uncertainty (validate assumptions)
3. Medium impact + high uncertainty
4. Lower priority items

### Phase 6: GameDay Planning

If multiple experiments or team exercise desired:

```text
GameDay Plan: [Title]

Date: [Proposed date]
Duration: [Hours]
Participants: [Teams/roles needed]

Objectives:
1. Validate [resilience pattern/assumption]
2. Practice [incident response/coordination]
3. Test [runbook/recovery procedure]

Pre-GameDay Checklist:
□ Stakeholder approval
□ Participant briefing scheduled
□ Monitoring dashboards verified
□ Kill switches tested
□ Rollback procedures documented
□ Communication channels set up

Schedule:
[Time] - Pre-brief and role assignment
[Time] - Baseline capture
[Time] - Scenario 1: [Name]
[Time] - Debrief / break
[Time] - Scenario 2: [Name]
[Time] - Hot debrief
[Time] - Cleanup and verification

Scenarios:

Scenario 1: [Name]
- Objective: [What we're testing]
- Hypothesis: [Expected behavior]
- Injection: [Fault details]
- Duration: [Time]
- Success criteria: [Metrics]

Scenario 2: [Name]
[Same structure]

Safety:
- Kill switch: [How to immediately stop]
- Rollback: [How to revert all changes]
- Communication: [Primary channel]
- Escalation: [Who to contact if real incident]

Roles:
- GameDay Lead: [Responsibilities]
- Scenario Executor: [Responsibilities]
- Observers: [Responsibilities]
- Scribe: [Responsibilities]

Post-GameDay:
- Hot debrief: Same day
- Formal postmortem: Within 1 week
- Action items tracked in: [System]
```

### Phase 7: Output Generation

Generate deliverables:

1. **Resilience Assessment** - Current state analysis
2. **Experiment Catalog** - Prioritized list of experiments
3. **Detailed Experiment Plans** - Ready-to-execute designs
4. **GameDay Plan** - If requested, full GameDay documentation
5. **Implementation Checklist** - Steps to execute safely

## Usage Examples

```bash
# Plan chaos for a specific service
/sd:chaos-plan order-service

# Plan with architecture context
/sd:chaos-plan @docs/architecture/payment-system.md

# Plan GameDay for entire system
/sd:chaos-plan "e-commerce platform" --gameday
```

## Interactive Elements

Use `AskUserQuestion` to:

- Clarify system boundaries
- Validate failure mode priorities
- Confirm blast radius acceptability
- Review experiment designs
- Finalize GameDay parameters

## Output

The command produces:

1. **Resilience Assessment Report**
2. **Prioritized Experiment Catalog**
3. **Detailed Experiment Designs**
4. **GameDay Plan** (if applicable)
5. **Safety Checklist**

## Related Skills

This command leverages:

- `chaos-engineering-fundamentals` - Experiment design principles
- `resilience-patterns` - Patterns to test and validate
- `gameday-planning` - GameDay execution guidance
- `incident-response` - Handling discovered issues

## Related Agent

For ongoing chaos engineering consultation:

- `chaos-engineer` - Resilience testing expertise
