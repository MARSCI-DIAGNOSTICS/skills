---
name: explain
description: Explain a systems design concept
argument-hint: <concept>
allowed-tools: Read, Glob, Grep, Skill
---

# Explain Systems Design Concept

Explain a systems design concept in practical, developer-friendly terms.

## Arguments

`$ARGUMENTS` - The concept to explain (e.g., "CAP theorem", "sharding", "circuit breaker", "load balancing")

## Workflow

1. **Identify the concept category** to load the appropriate skill:
   - Interview methodology → `design-interview-methodology`
   - Estimation/capacity → `estimation-techniques`
   - Quality attributes/NFRs → `quality-attributes-taxonomy`
   - Future phases: distributed systems, scalability, cloud-native

2. **Provide a practical explanation** that:
   - Explains what it is in plain terms
   - Shows why it matters for system design
   - Gives concrete examples when possible
   - Discusses trade-offs and when to use it
   - Links to related concepts

3. **Include reference examples** where helpful:
   - Back-of-envelope calculations for scale concepts
   - Decision criteria for pattern selection
   - Real-world analogies for complex concepts

## Example Usage

```bash
/sd:explain CAP theorem
/sd:explain sharding
/sd:explain circuit breaker
/sd:explain back-of-envelope
/sd:explain load balancing
/sd:explain eventual consistency
/sd:explain latency vs throughput
/sd:explain quality attributes
/sd:explain scalability
/sd:explain the "-ilities"
```

## Concept Categories

### Currently Available (Phase 1)

| Category | Example Concepts |
| -------- | ---------------- |
| Interview methodology | 4-step framework, requirements gathering, deep dives |
| Estimation | QPS, storage, bandwidth, latency numbers |
| Quality attributes | Scalability, reliability, availability, performance, security |

### Coming in Future Phases

| Category | Example Concepts |
| -------- | ---------------- |
| Distributed systems | CAP theorem, consensus, message queues |
| Scalability | Load balancing, sharding, caching |
| Cloud-native | Kubernetes, serverless, service mesh |

## Output

A clear, practical explanation that helps engineers understand and apply the concept in real system designs.
