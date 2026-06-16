---
name: edge-strategy
description: Design CDN and edge deployment strategy for global distribution - optimizes latency, plans caching architecture, and recommends edge compute placement
allowed-tools: Read, Glob, Grep, Task, AskUserQuestion
argument-hint: <requirements-or-system>
---

# Edge Strategy Command

This command designs CDN and edge deployment strategies for globally distributed systems.

## Purpose

Generate edge architecture plans including:

1. Geographic distribution requirements
2. CDN and caching strategy
3. Edge compute placement decisions
4. Latency optimization plan
5. Multi-region failover design

## Workflow

### Phase 1: Requirements Gathering

Understand the distribution needs:

**If requirements provided:**

- Parse geographic and latency requirements
- Identify user distribution patterns
- Determine content types and caching potential
- Check compliance/data residency constraints

**If no requirements provided, ask:**

```text
What are your edge/CDN requirements?

1. User Geography:
   - Primary regions: [US/EU/APAC/Global]
   - User distribution: [Concentrated/Distributed]

2. Latency Requirements:
   - Target P50: [50ms/100ms/200ms/Best effort]
   - Target P99: [100ms/200ms/500ms/Best effort]

3. Content Profile:
   - Static content percentage: [High/Medium/Low]
   - API/dynamic content: [Yes/No]
   - Real-time requirements: [Yes/No]

4. Compliance:
   - Data residency requirements: [GDPR/CCPA/None]
   - Specific country restrictions: [List]
```

### Phase 2: Current State Analysis

If a system is provided, analyze current architecture:

```text
Current State Analysis:
□ Existing deployment regions
□ Current CDN configuration (if any)
□ Content types and caching headers
□ Origin architecture
□ Traffic patterns and volumes
□ Current latency measurements
```

**Search patterns:**

- CDN config: `cdn`, `cloudfront`, `cloudflare`, `akamai`, `cache-control`
- Multi-region: `region`, `failover`, `replica`, `primary`, `secondary`
- Edge: `edge`, `lambda@edge`, `workers`, `edge function`

### Phase 3: Content Analysis

Categorize content for caching strategy:

```text
Content Classification:

Static Assets (Long Cache):
□ JavaScript bundles
□ CSS stylesheets
□ Images and media
□ Fonts
□ Static HTML

Dynamic Content (Short Cache):
□ API responses (cacheable)
□ Generated pages
□ Search results
□ Aggregated data

Real-time/Uncacheable:
□ User-specific data
□ Transactional endpoints
□ WebSocket connections
□ Real-time feeds

Estimated Cacheable Percentage: [X]%
```

### Phase 4: Geographic Distribution Design

Plan the geographic architecture:

```text
Geographic Distribution Plan:

User Distribution Analysis:
- Region 1: [X]% of users
- Region 2: [Y]% of users
- Region 3: [Z]% of users

Recommended Architecture:
┌─────────────────────────────────────────────────────────────┐
│                         USERS                                │
│    [Region 1]      [Region 2]      [Region 3]              │
└────────┬─────────────┬─────────────┬────────────────────────┘
         │             │             │
         ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│                    CDN EDGE LAYER                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ Edge POP │  │ Edge POP │  │ Edge POP │                  │
│  │ [Region] │  │ [Region] │  │ [Region] │                  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                  │
└───────┼─────────────┼─────────────┼─────────────────────────┘
        │             │             │
        └─────────────┼─────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   ORIGIN LAYER                               │
│  [Primary Region]         [Secondary Region]                │
└─────────────────────────────────────────────────────────────┘

Region Selection Rationale:
- [Region 1]: [Reason - user concentration, compliance, etc.]
- [Region 2]: [Reason]
```

### Phase 5: CDN Architecture Design

Design the caching strategy:

```text
CDN Architecture Design:

Provider Recommendation: [Cloudflare/CloudFront/Akamai/Fastly]
Rationale: [Why this provider]

Cache Hierarchy:
┌─────────────────────────────────────────────────────────────┐
│  Browser Cache (L1)                                          │
│  - Static assets: max-age=31536000, immutable               │
│  - API responses: max-age=0, must-revalidate                │
├─────────────────────────────────────────────────────────────┤
│  CDN Edge Cache (L2)                                         │
│  - Static: 1 year TTL, versioned URLs                       │
│  - Dynamic: 60s TTL, stale-while-revalidate                 │
│  - Personalized: Cache key includes auth header             │
├─────────────────────────────────────────────────────────────┤
│  Origin Shield (L3)                                          │
│  - Location: [Region closest to origin]                     │
│  - Collapses cache misses                                   │
│  - Reduces origin load by ~80%                              │
└─────────────────────────────────────────────────────────────┘

Cache Rules:

| Path Pattern | Cache Location | TTL | Vary Headers | Invalidation |
|--------------|----------------|-----|--------------|--------------|
| /static/*    | Edge + Browser | 1yr | None         | Versioned URLs |
| /api/public/*| Edge only      | 60s | Accept       | Cache tags   |
| /api/user/*  | Edge           | 30s | Authorization| Purge on change |
| /api/auth/*  | None           | N/A | N/A          | N/A          |
```

### Phase 6: Edge Compute Strategy

Determine edge compute placement:

```text
Edge Compute Analysis:

Use Cases for Edge Compute:
□ Authentication/token validation
□ Request routing and A/B testing
□ Personalization (basic)
□ Security (WAF, rate limiting)
□ Response transformation
□ Geolocation-based logic

Recommended Edge Functions:

Function 1: Auth Validation
- Location: Edge (every POP)
- Purpose: Validate JWT before origin
- Latency savings: ~50-100ms
- Technology: [Cloudflare Workers/Lambda@Edge]

Function 2: Geo Router
- Location: Edge (every POP)
- Purpose: Route to optimal origin
- Implementation: [Details]

Function 3: [Custom function]
- [Details]

Edge vs Origin Decision Matrix:

| Operation | Edge | Origin | Reason |
|-----------|------|--------|--------|
| JWT validation | ✓ | | Fast, stateless |
| Rate limiting | ✓ | | Distributed enforcement |
| User lookup | | ✓ | Requires DB |
| Transactions | | ✓ | ACID requirements |
| ML inference | | ✓ | Compute intensive |
```

### Phase 7: Latency Budget

Create latency budget allocation:

```text
Latency Budget: [Target]ms P99

┌─────────────────────────────────────────────────────────────┐
│                    [Total]ms Total Budget                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │ Network  │   Edge   │  Origin  │    DB    │ Response │  │
│  │   Xms    │   Xms    │   Xms    │   Xms    │   Xms    │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
│                                                              │
│  Budget Allocation:                                          │
│  ├── Network (client → edge): [X]ms                         │
│  ├── Edge processing: [X]ms                                 │
│  ├── Edge → Origin: [X]ms                                   │
│  ├── Origin processing: [X]ms                               │
│  ├── Database queries: [X]ms                                │
│  └── Response serialization: [X]ms                          │
└─────────────────────────────────────────────────────────────┘

Optimization Strategies:
1. Cache at edge (eliminate origin roundtrip)
2. Edge compute for auth (reduce origin work)
3. Database optimization (indexes, connection pooling)
4. Protocol upgrade (HTTP/3, connection reuse)
```

### Phase 8: Multi-Region Failover Design

Plan failover architecture:

```text
Failover Architecture:

Deployment Model: [Active-Active / Active-Passive]

Region Configuration:
┌─────────────────┐         ┌─────────────────┐
│  [Primary]      │         │  [Secondary]    │
│  ┌───────────┐  │   ───►  │  ┌───────────┐  │
│  │  Active   │  │ Async   │  │  [Mode]   │  │
│  │  Origin   │  │ Repl    │  │  Origin   │  │
│  └───────────┘  │         │  └───────────┘  │
└─────────────────┘         └─────────────────┘

Failover Mechanism:
- Health checks: [Interval and thresholds]
- Detection time: [X] seconds
- Failover time: [X] seconds
- Total RTO: [X] seconds

Recovery Objectives:
- RTO (Recovery Time Objective): [X minutes]
- RPO (Recovery Point Objective): [X minutes]

Traffic Routing:
- Normal: [X]% Primary, [Y]% Secondary
- Failover: 100% to healthy region
- Failback: Gradual shift back

Data Replication:
- Method: [Sync/Async]
- Lag tolerance: [X]ms
- Conflict resolution: [Strategy]
```

### Phase 9: Generate Strategy Document

Create comprehensive edge strategy:

```text
# Edge Strategy: [System Name]

## Executive Summary

Target: [Latency target] P99 globally
Approach: [CDN provider] + [X] origin regions + edge compute
Expected improvement: [X]% latency reduction

## Architecture Overview

[ASCII diagram of complete architecture]

## CDN Configuration

| Setting | Value | Rationale |
|---------|-------|-----------|
| Provider | [Name] | [Why] |
| Edge POPs | [Regions] | [Coverage] |
| Origin shield | [Location] | [Collapse misses] |
| Cache strategy | [Approach] | [Token efficiency] |

## Edge Compute

| Function | Location | Purpose | Technology |
|----------|----------|---------|------------|
| [Name] | Edge | [Purpose] | [Tech] |

## Regional Deployment

| Region | Role | Services | Rationale |
|--------|------|----------|-----------|
| [Region 1] | Primary | All | [Reason] |
| [Region 2] | Secondary | All | [Reason] |

## Implementation Roadmap

### Phase 1: CDN Setup (Week 1-2)
- [ ] CDN provider configuration
- [ ] DNS migration
- [ ] Cache rules implementation
- [ ] Origin shield setup

### Phase 2: Edge Compute (Week 3-4)
- [ ] Edge function development
- [ ] Testing and validation
- [ ] Gradual rollout

### Phase 3: Multi-Region (Week 5-8)
- [ ] Secondary region provisioning
- [ ] Data replication setup
- [ ] Failover testing
- [ ] Go-live

## Monitoring

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Cache hit ratio | >90% | <80% |
| Edge latency P50 | <20ms | >30ms |
| Origin latency P99 | <100ms | >150ms |
| Availability | 99.99% | <99.9% |
```

## Usage Examples

```bash
# Design edge strategy for requirements
/sd:edge-strategy "Global users, <100ms P99, static-heavy site"

# Analyze existing system
/sd:edge-strategy @src/infra/

# Review current CDN config
/sd:edge-strategy "Review and optimize current CloudFront setup"

# Plan multi-region expansion
/sd:edge-strategy "Expand from US to EU and APAC"
```

## Interactive Elements

Use `AskUserQuestion` to:

- Clarify geographic requirements
- Understand latency targets
- Identify compliance constraints
- Validate CDN provider preference
- Confirm failover requirements

## Output

The command produces:

1. **Geographic Distribution Plan** - Region selection and rationale
2. **CDN Architecture** - Caching strategy and configuration
3. **Edge Compute Strategy** - Function placement and design
4. **Latency Budget** - End-to-end latency allocation
5. **Failover Design** - Multi-region resilience plan
6. **Implementation Roadmap** - Phased rollout plan

## Related Skills

This command leverages:

- `cdn-architecture` - CDN design patterns
- `edge-computing` - Edge function design
- `multi-region-deployment` - Global distribution strategies
- `latency-optimization` - Latency reduction techniques

## Related Agent

For ongoing edge architecture consultation:

- `edge-architect` - CDN and edge expertise
