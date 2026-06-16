# Performance Test Strategy Template

## Template

```markdown
# Performance Test Strategy: [Project Name]

## 1. Objectives

### Business Objectives
- Support [X] concurrent users
- Handle [Y] requests per second
- Achieve [Z]% availability during peak

### Technical Objectives
| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| Response Time (p50) | < 100ms | < 200ms |
| Response Time (p95) | < 200ms | < 500ms |
| Response Time (p99) | < 500ms | < 1000ms |
| Throughput | > 1000 RPS | > 500 RPS |
| Error Rate | < 0.1% | < 1% |
| CPU Utilization | < 70% | < 90% |
| Memory Utilization | < 75% | < 90% |

## 2. Scope

### In Scope
| Endpoint/Feature | Priority | Expected Load |
|------------------|----------|---------------|
| /api/orders (POST) | P1 | 100 RPS |
| /api/products (GET) | P1 | 500 RPS |
| /api/search | P2 | 200 RPS |

### Out of Scope
- [Third-party integrations (mocked)]
- [Admin endpoints (low traffic)]

## 3. Load Profile

### User Distribution
| User Type | Percentage | Actions/Session |
|-----------|------------|-----------------|
| Browse Only | 60% | 10 page views |
| Add to Cart | 25% | 5 views + 2 cart ops |
| Checkout | 15% | 5 views + checkout flow |

### Traffic Pattern
```text
     100% ──────────────────────────
      │         ┌─────────┐
      │    ┌────┤  Peak   ├────┐
  75% ├────┤    │ (2 hrs) │    ├────
      │    │    └─────────┘    │
  50% ┼────┘                   └────
      │
   0% └──────────────────────────────
        6am  9am  12pm  3pm  6pm  9pm
```

### Workload Model

- Ramp-up: 5 minutes to full load
- Steady state: 30 minutes at target load
- Peak: 15 minutes at 150% load
- Ramp-down: 5 minutes to zero

## 4. Test Environment

### Infrastructure

| Component | Prod Spec | Test Spec | Scale Factor |
|-----------|-----------|-----------|--------------|
| App Servers | 8 vCPU, 32GB | 4 vCPU, 16GB | 50% |
| Database | 16 vCPU, 64GB | 8 vCPU, 32GB | 50% |
| Cache | 3-node cluster | 1-node | 33% |

### Data Requirements

- [X] users in database
- [Y] products in catalog
- [Z] historical orders

## 5. Test Scenarios

### Scenario 1: Normal Load

- **Objective**: Validate SLA under expected load
- **Load**: 1000 concurrent users
- **Duration**: 30 minutes
- **Success Criteria**: All SLAs met

### Scenario 2: Peak Load

- **Objective**: Validate performance during peak
- **Load**: 2000 concurrent users
- **Duration**: 15 minutes
- **Success Criteria**: Response time < 500ms (p95)

### Scenario 3: Stress Test

- **Objective**: Find system breaking point
- **Load**: Increase until failure
- **Duration**: Until degradation
- **Success Criteria**: Document breaking point

## 6. Monitoring

### Metrics to Collect

- Application: Response times, throughput, errors
- Infrastructure: CPU, memory, disk I/O, network
- Database: Query times, connections, locks
- Cache: Hit ratio, memory usage

### Tools

- APM: [Application Insights / Datadog / New Relic]
- Infrastructure: [Prometheus + Grafana]
- Custom: [Application logs with correlation IDs]

## 7. Success Criteria

| Test Type | Criteria | Action if Failed |
|-----------|----------|------------------|
| Load Test | All SLAs met | Optimize and retest |
| Stress Test | Graceful degradation | Implement circuit breakers |
| Soak Test | No memory leaks | Fix and retest |

---

## Strategy Checklist

Before starting performance testing:

- [ ] Objectives defined (business and technical)
- [ ] Scope documented (in/out)
- [ ] Load profile designed
- [ ] Test environment configured
- [ ] Test scenarios defined
- [ ] Monitoring set up
- [ ] Success criteria agreed
