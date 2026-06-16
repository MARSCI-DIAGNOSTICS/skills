# Circuit Breaker Configuration Guide

## Overview

Circuit breakers prevent cascade failures by stopping calls to failing services. This guide covers configuration options and scenarios.

## Circuit Breaker States

```text
┌──────────┐     failure threshold     ┌──────────┐
│  CLOSED  │ ─────────exceeded──────> │   OPEN   │
│ (normal) │                          │  (fail)  │
└──────────┘                          └──────────┘
     ↑                                      │
     │                                      │
     │        ┌─────────────┐               │
     │        │ HALF-OPEN   │               │
     └─success┤ (testing)   │<──break timer─┘
              └─────────────┘
                    │
                    └─failure──> back to OPEN
```

## Configuration Parameters

| Parameter | Description | Typical Range |
| --- | --- | --- |
| `FailureRatio` | % of failures to trigger open | 0.25 - 0.75 |
| `MinimumThroughput` | Min calls before evaluating | 5 - 50 |
| `SamplingDuration` | Window for failure calculation | 10s - 60s |
| `BreakDuration` | How long to stay open | 15s - 120s |

## Configuration Scenarios

### Conservative (Critical Service)

When calling a critical service where you want early failure detection:

```csharp
.AddCircuitBreaker(new CircuitBreakerStrategyOptions
{
    FailureRatio = 0.25,              // Open after 25% failures
    MinimumThroughput = 5,            // Only 5 calls needed to evaluate
    SamplingDuration = TimeSpan.FromSeconds(10),
    BreakDuration = TimeSpan.FromSeconds(60)
})
```

**Behavior:** Opens quickly (25% of 5 = 2 failures), stays open longer (60s).

### Aggressive (High-Traffic Service)

When calling a high-traffic service that occasionally has transient issues:

```csharp
.AddCircuitBreaker(new CircuitBreakerStrategyOptions
{
    FailureRatio = 0.5,               // Open after 50% failures
    MinimumThroughput = 50,           // Need significant traffic
    SamplingDuration = TimeSpan.FromSeconds(30),
    BreakDuration = TimeSpan.FromSeconds(15)
})
```

**Behavior:** Tolerates more failures, needs more evidence, recovers faster.

### Per-Endpoint Configuration

Different thresholds for different endpoints:

```csharp
// Health check - very aggressive
.AddCircuitBreaker(new CircuitBreakerStrategyOptions
{
    FailureRatio = 0.1,               // Very sensitive
    MinimumThroughput = 3,
    BreakDuration = TimeSpan.FromSeconds(120)
})

// Data retrieval - moderate
.AddCircuitBreaker(new CircuitBreakerStrategyOptions
{
    FailureRatio = 0.4,
    MinimumThroughput = 20,
    BreakDuration = TimeSpan.FromSeconds(30)
})

// Mutation - conservative
.AddCircuitBreaker(new CircuitBreakerStrategyOptions
{
    FailureRatio = 0.6,               // Allow more failures
    MinimumThroughput = 10,
    BreakDuration = TimeSpan.FromSeconds(45)
})
```

## Calculating Settings

### MinimumThroughput

```text
MinimumThroughput = ExpectedCallsPerSecond × SamplingDurationSeconds × SafetyFactor

Example:
  10 calls/sec × 30 sec × 0.5 safety factor = 150 minimum
  But for faster detection, use 10-20
```

### BreakDuration

```text
BreakDuration = EstimatedRecoveryTime × MultiplierForSafety

Example:
  If service typically recovers in 15s, use 20-30s break duration
```

### FailureRatio

| Scenario | FailureRatio |
| --- | --- |
| Very critical, fail fast | 0.10 - 0.25 |
| Normal services | 0.30 - 0.50 |
| Tolerant of failures | 0.50 - 0.75 |

## Handling Circuit States

```csharp
.AddCircuitBreaker(new CircuitBreakerStrategyOptions<HttpResponseMessage>
{
    FailureRatio = 0.5,
    MinimumThroughput = 10,
    BreakDuration = TimeSpan.FromSeconds(30),

    OnOpened = async args =>
    {
        _logger.LogWarning(
            "Circuit opened for {Service}. Breaking for {Duration}",
            "PaymentService",
            args.BreakDuration);

        await _alertService.SendAlert("PaymentService circuit opened");
    },

    OnClosed = args =>
    {
        _logger.LogInformation("Circuit closed for {Service}", "PaymentService");
        return default;
    },

    OnHalfOpened = args =>
    {
        _logger.LogInformation("Circuit half-open for {Service}", "PaymentService");
        return default;
    }
})
```

## Manual Circuit Control

```csharp
var circuitBreakerStateProvider = new CircuitBreakerStateProvider();

.AddCircuitBreaker(new CircuitBreakerStrategyOptions
{
    StateProvider = circuitBreakerStateProvider
})

// Check state
var state = circuitBreakerStateProvider.CircuitState;
// CircuitState.Closed, CircuitState.Open, CircuitState.HalfOpen, CircuitState.Isolated

// Manually isolate
await circuitBreakerStateProvider.IsolateAsync();

// Reset
await circuitBreakerStateProvider.ResetAsync();
```

## Monitoring Metrics

| Metric | Purpose | Alert Condition |
| --- | --- | --- |
| `circuit.state` | Current state | State == Open |
| `circuit.opened.count` | Times opened | > 0 per hour |
| `circuit.break.duration` | Time in open state | > 5 minutes |
| `circuit.half_open.success_rate` | Recovery success | < 50% |

## Anti-Patterns

### Too Sensitive

```csharp
// BAD: Opens on single failure
.AddCircuitBreaker(new CircuitBreakerStrategyOptions
{
    FailureRatio = 0.01,
    MinimumThroughput = 1
})
```

### Too Tolerant

```csharp
// BAD: Never opens (need 100% failure rate with 1000 calls)
.AddCircuitBreaker(new CircuitBreakerStrategyOptions
{
    FailureRatio = 1.0,
    MinimumThroughput = 1000
})
```

### Break Duration Too Short

```csharp
// BAD: Immediate retry flood
.AddCircuitBreaker(new CircuitBreakerStrategyOptions
{
    BreakDuration = TimeSpan.FromSeconds(1)
})
```

---

**Related:** `polly-patterns.md`, `retry-strategies.md`
