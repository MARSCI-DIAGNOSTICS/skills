---
name: latency-budget
description: Calculate and allocate latency budgets for a system - breaks down end-to-end latency into component budgets with optimization recommendations
allowed-tools: Read, Glob, Grep, Task, AskUserQuestion
argument-hint: <target-latency> [system-description-or-file]
---

# Latency Budget Command

This command calculates and allocates latency budgets for a system, helping teams understand where time is spent and how to meet latency targets.

## Purpose

Provide latency budget analysis including:

1. End-to-end latency breakdown
2. Per-component budget allocation
3. Bottleneck identification
4. Optimization recommendations
5. Monitoring strategy for latency

## Workflow

### Phase 1: Requirements Gathering

**If target latency and system provided:**

- Parse latency target (e.g., "100ms", "500ms P99")
- Search codebase for system architecture
- Identify components in the request path

**If not provided, ask:**

```text
Latency Budget Analysis Setup:

1. Target Latency:
   - P50 target: [e.g., 50ms, 100ms, 200ms]
   - P99 target: [e.g., 100ms, 200ms, 500ms]

2. Request Type:
   - Read path (query, fetch, search)
   - Write path (create, update, delete)
   - Mixed (both reads and writes)

3. System Scope:
   - Single service latency
   - End-to-end user request
   - Specific flow (e.g., "checkout", "search")

4. Current State (if known):
   - Current P50: [value]
   - Current P99: [value]
   - Known bottlenecks: [components]
```

### Phase 2: Component Identification

Identify all components in the request path:

```text
Request Path Analysis:

┌─────────────────────────────────────────────────────────────┐
│                      REQUEST FLOW                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Client ──► CDN ──► LB ──► API ──► Service ──► DB          │
│    │        │       │      │        │          │            │
│    ▼        ▼       ▼      ▼        ▼          ▼            │
│  [?ms]    [?ms]   [?ms]  [?ms]    [?ms]      [?ms]         │
│                                                              │
└─────────────────────────────────────────────────────────────┘

Components Identified:

1. Network Segments
   □ Client → CDN/Edge
   □ CDN → Load Balancer
   □ Load Balancer → API Gateway
   □ API Gateway → Service
   □ Service → Database

2. Processing Components
   □ CDN processing
   □ Load balancer routing
   □ API gateway (auth, rate limiting)
   □ Service logic
   □ Database query

3. External Dependencies
   □ Third-party APIs
   □ Cache lookups
   □ Message queue operations
```

### Phase 3: Budget Allocation

Allocate latency budget across components:

```text
Latency Budget Allocation

Target: [X]ms P99 end-to-end

═══════════════════════════════════════════════════════════════

                    BUDGET BREAKDOWN

  ┌────────────────────────────────────────────────────────┐
  │                    [TOTAL]ms                            │
  ├────────────────────────────────────────────────────────┤
  │                                                         │
  │  ┌──────┬──────┬──────┬──────┬──────┬──────┐          │
  │  │Network│ Edge │  LB  │ API  │Service│  DB  │          │
  │  │ Xms  │ Xms  │ Xms  │ Xms  │ Xms   │ Xms  │          │
  │  └──────┴──────┴──────┴──────┴──────┴──────┘          │
  │                                                         │
  │  Allocation:                                            │
  │  ├── Network (client → edge):     [X]ms  ([Y]%)        │
  │  ├── Edge/CDN processing:         [X]ms  ([Y]%)        │
  │  ├── Load balancer:               [X]ms  ([Y]%)        │
  │  ├── API gateway:                 [X]ms  ([Y]%)        │
  │  ├── Service processing:          [X]ms  ([Y]%)        │
  │  ├── Database query:              [X]ms  ([Y]%)        │
  │  └── Response serialization:      [X]ms  ([Y]%)        │
  │                                                         │
  │  Buffer/Slack:                    [X]ms  ([Y]%)        │
  │                                                         │
  └────────────────────────────────────────────────────────┘

Per-Component Budgets:

| Component | Budget | Typical | Notes |
|-----------|--------|---------|-------|
| Network RTT | [X]ms | 10-50ms | Varies by geography |
| CDN/Edge | [X]ms | 5-20ms | Cache hit vs miss |
| Load Balancer | [X]ms | 1-5ms | Usually minimal |
| API Gateway | [X]ms | 5-20ms | Auth, rate limiting |
| Service Logic | [X]ms | 10-100ms | Main application |
| Database | [X]ms | 5-50ms | Query dependent |
| Serialization | [X]ms | 1-10ms | Response size dependent |
```

### Phase 4: Latency Reference Data

Provide reference data for realistic estimates:

```text
Latency Reference Numbers (2024):

Network Latencies:
├── Same datacenter: 0.5ms
├── Same region (cross-AZ): 1-2ms
├── Cross-region (same continent): 30-100ms
├── Cross-continent: 100-300ms
└── Client → nearest edge: 10-50ms (varies)

Service Latencies (P99):
├── Redis cache hit: 0.5-2ms
├── Memcached cache hit: 0.5-2ms
├── PostgreSQL simple query: 2-10ms
├── PostgreSQL complex query: 10-100ms
├── Elasticsearch search: 10-50ms
├── Kafka produce (ack=1): 2-10ms
└── HTTP call to another service: 10-100ms

Processing Latencies:
├── JSON serialization (1KB): 0.1-1ms
├── JWT validation: 0.5-2ms
├── Connection pool acquire: 0.1-1ms
└── Context switch: 0.01ms

Geographic Examples:
├── US East → US West: 60-80ms
├── US → Europe: 80-120ms
├── US → Asia: 150-250ms
└── Europe → Asia: 150-300ms
```

### Phase 5: Optimization Recommendations

Based on budget allocation and bottlenecks:

```text
Latency Optimization Recommendations

Priority 1: Quick Wins
─────────────────────────────────────────────────────────────
[ ] Add caching layer
    Current: [X]ms database queries
    Target: [Y]ms cache hits
    Savings: ~[Z]ms

[ ] Connection pooling
    Current: New connection per request
    Target: Pool of persistent connections
    Savings: ~[Z]ms

Priority 2: Architecture Changes
─────────────────────────────────────────────────────────────
[ ] Add edge caching
    Current: All requests hit origin
    Target: 80% cache hit at edge
    Savings: ~[Z]ms P50

[ ] Async processing
    Current: Synchronous full processing
    Target: Defer non-critical work
    Savings: ~[Z]ms

Priority 3: Infrastructure
─────────────────────────────────────────────────────────────
[ ] Deploy to additional regions
    Current: Single region
    Target: Multi-region
    Savings: ~[Z]ms for remote users

[ ] Upgrade database tier
    Current: [tier]
    Target: [higher tier]
    Savings: ~[Z]ms query time

Estimated Impact:

| Optimization | Effort | P50 Savings | P99 Savings |
|--------------|--------|-------------|-------------|
| [Opt 1] | Low | [X]ms | [Y]ms |
| [Opt 2] | Medium | [X]ms | [Y]ms |
| [Opt 3] | High | [X]ms | [Y]ms |
```

### Phase 6: Monitoring Strategy

Define how to monitor latency budget:

```text
Latency Monitoring Strategy

Per-Component Metrics:

| Component | Metric Name | Alert Threshold |
|-----------|-------------|-----------------|
| Total | request_latency_p99 | > [target]ms |
| Database | db_query_latency_p99 | > [budget]ms |
| Cache | cache_latency_p99 | > [budget]ms |
| External | external_api_p99 | > [budget]ms |

Dashboard Panels:

1. End-to-end latency (P50, P90, P99)
2. Component breakdown (stacked)
3. Budget consumption (% of budget used)
4. Geographic distribution

Alert Rules:

1. P99 > Target
   - Condition: request_latency_p99 > [target]ms for 5 min
   - Severity: Warning

2. P99 > 1.5x Target
   - Condition: request_latency_p99 > [1.5x target]ms for 2 min
   - Severity: Critical

3. Component Budget Exceeded
   - Condition: [component]_latency_p99 > [budget]ms for 5 min
   - Severity: Warning
```

### Phase 7: Generate Report

Produce a complete latency budget report:

```text
# Latency Budget Report: [System Name]

## Executive Summary

Target Latency: [X]ms P99
Current State: [Y]ms P99 (if known)
Gap: [Z]ms

## Request Flow

[ASCII diagram of request path with latencies]

## Budget Allocation

[Table of component budgets]

## Bottleneck Analysis

1. [Primary bottleneck]: [Impact]
2. [Secondary bottleneck]: [Impact]

## Optimization Roadmap

### Phase 1: Quick Wins ([X]ms savings)
- [Optimization 1]
- [Optimization 2]

### Phase 2: Medium Term ([X]ms savings)
- [Optimization 1]
- [Optimization 2]

### Phase 3: Long Term ([X]ms savings)
- [Optimization 1]
- [Optimization 2]

## Monitoring Setup

[Metrics and alerts to implement]

## Next Steps

1. [Immediate action]
2. [Short-term action]
3. [Long-term action]
```

## Usage Examples

```bash
# Analyze with specific target
/sd:latency-budget 100ms

# Analyze with P99 target and system context
/sd:latency-budget "200ms P99" @docs/api-architecture.md

# Analyze specific flow
/sd:latency-budget 50ms "checkout flow"

# Analyze with current measurements
/sd:latency-budget "100ms target, currently at 180ms"
```

## Interactive Elements

Use `AskUserQuestion` to:

- Clarify latency targets (P50 vs P99)
- Understand current bottlenecks
- Validate component identification
- Confirm optimization priorities

## Output

The command produces:

1. **Budget Breakdown** - Per-component latency allocation
2. **Bottleneck Analysis** - Where time is being spent
3. **Optimization Roadmap** - Prioritized improvements
4. **Monitoring Strategy** - How to track latency

## Related Skills

This command leverages:

- `latency-optimization` - Latency reduction techniques
- `caching-strategies` - Cache-based optimizations
- `database-scaling` - Database performance
- `cdn-architecture` - Edge optimization

## Related Agent

For capacity planning including latency:

- `capacity-planner` - Back-of-envelope calculations
