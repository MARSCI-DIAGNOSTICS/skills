# Retry Strategy Patterns

## Overview

Retry strategies handle transient failures by automatically retrying failed operations. This guide covers common patterns and when to use them.

## Strategy Types

### Immediate Retry

Retry immediately without delay.

```csharp
.AddRetry(new RetryStrategyOptions
{
    MaxRetryAttempts = 2,
    Delay = TimeSpan.Zero
})
```

**Use when:**

- Failure is likely a momentary glitch
- Low-latency requirement
- Local operations (not network)

**Avoid when:**

- Calling remote services (can overwhelm)
- Rate-limited APIs

### Fixed Delay

Same delay between each retry.

```csharp
.AddRetry(new RetryStrategyOptions
{
    MaxRetryAttempts = 3,
    Delay = TimeSpan.FromSeconds(2),
    BackoffType = DelayBackoffType.Constant
})
```

**Delays:** 2s → 2s → 2s

**Use when:**

- Rate-limited with known limit
- Simple, predictable delay needed

### Linear Backoff

Delay increases linearly.

```csharp
.AddRetry(new RetryStrategyOptions
{
    MaxRetryAttempts = 4,
    Delay = TimeSpan.FromSeconds(1),
    BackoffType = DelayBackoffType.Linear
})
```

**Delays:** 1s → 2s → 3s → 4s

**Use when:**

- Gradual increase preferred
- Moderate recovery time expected

### Exponential Backoff

Delay doubles each attempt (most common).

```csharp
.AddRetry(new RetryStrategyOptions
{
    MaxRetryAttempts = 4,
    Delay = TimeSpan.FromSeconds(1),
    BackoffType = DelayBackoffType.Exponential
})
```

**Delays:** 1s → 2s → 4s → 8s

**Use when:**

- Network services
- Unknown recovery time
- Most HTTP client scenarios

### Exponential with Jitter

Randomized delay to prevent thundering herd.

```csharp
.AddRetry(new RetryStrategyOptions
{
    MaxRetryAttempts = 4,
    Delay = TimeSpan.FromSeconds(1),
    BackoffType = DelayBackoffType.Exponential,
    UseJitter = true  // Adds random variation
})
```

**Delays:** ~0.9s → ~2.1s → ~3.8s → ~8.2s (randomized)

**Use when:**

- Many clients calling same service
- Preventing synchronized retry storms

## Selecting What to Retry

### HTTP Transient Errors Only

```csharp
.AddRetry(new HttpRetryStrategyOptions
{
    ShouldHandle = new PredicateBuilder<HttpResponseMessage>()
        .Handle<HttpRequestException>()
        .HandleResult(r => r.StatusCode is
            HttpStatusCode.RequestTimeout or         // 408
            HttpStatusCode.TooManyRequests or        // 429
            HttpStatusCode.InternalServerError or   // 500
            HttpStatusCode.BadGateway or            // 502
            HttpStatusCode.ServiceUnavailable or    // 503
            HttpStatusCode.GatewayTimeout)          // 504
})
```

### Specific Exceptions

```csharp
.AddRetry(new RetryStrategyOptions
{
    ShouldHandle = new PredicateBuilder()
        .Handle<TimeoutException>()
        .Handle<OperationCanceledException>()
        .Handle<SocketException>()
})
```

### Combined Predicate

```csharp
.AddRetry(new RetryStrategyOptions<HttpResponseMessage>
{
    ShouldHandle = static args =>
    {
        // Retry on exception
        if (args.Outcome.Exception is HttpRequestException or TimeoutException)
            return ValueTask.FromResult(true);

        // Retry on certain status codes
        if (args.Outcome.Result?.StatusCode is HttpStatusCode.ServiceUnavailable)
            return ValueTask.FromResult(true);

        // Don't retry on business errors (4xx)
        if (args.Outcome.Result?.StatusCode == HttpStatusCode.BadRequest)
            return ValueTask.FromResult(false);

        return ValueTask.FromResult(false);
    }
})
```

## Custom Delay Logic

### Retry-After Header

```csharp
.AddRetry(new HttpRetryStrategyOptions
{
    DelayGenerator = static args =>
    {
        // Respect Retry-After header if present
        if (args.Outcome.Result?.Headers.RetryAfter?.Delta is { } delta)
        {
            return ValueTask.FromResult<TimeSpan?>(delta);
        }

        // Fallback to exponential
        var delay = TimeSpan.FromSeconds(Math.Pow(2, args.AttemptNumber));
        return ValueTask.FromResult<TimeSpan?>(delay);
    }
})
```

### Custom Delay Schedule

```csharp
.AddRetry(new RetryStrategyOptions
{
    MaxRetryAttempts = 5,
    DelayGenerator = static args =>
    {
        TimeSpan? delay = args.AttemptNumber switch
        {
            0 => TimeSpan.Zero,                    // Immediate
            1 => TimeSpan.FromMilliseconds(100),   // Quick
            2 => TimeSpan.FromSeconds(1),          // Wait
            3 => TimeSpan.FromSeconds(5),          // Longer
            _ => TimeSpan.FromSeconds(30)          // Max
        };
        return ValueTask.FromResult(delay);
    }
})
```

## Retry Callbacks

### Logging Retries

```csharp
.AddRetry(new RetryStrategyOptions
{
    OnRetry = args =>
    {
        _logger.LogWarning(
            "Retry {Attempt} after {Delay}. Exception: {Message}",
            args.AttemptNumber,
            args.RetryDelay,
            args.Outcome.Exception?.Message);
        return default;
    }
})
```

### Metrics Collection

```csharp
.AddRetry(new RetryStrategyOptions
{
    OnRetry = args =>
    {
        _metrics.IncrementRetryCounter(
            attempt: args.AttemptNumber,
            exception: args.Outcome.Exception?.GetType().Name);
        return default;
    }
})
```

## Retry Count Guidance

| Scenario | Attempts | Rationale |
| --- | --- | --- |
| Local resource lock | 2-3 | Quick resolution expected |
| Database connection | 3-4 | Connection pool issues |
| HTTP to internal service | 3 | Balance speed vs resilience |
| HTTP to external API | 2-3 | Respect their resources |
| Message queue publish | 5+ | Eventually consistent |

## Anti-Patterns

### Retrying Non-Idempotent Operations

```csharp
// DANGEROUS: May create duplicate orders
.AddRetry(new RetryStrategyOptions { MaxRetryAttempts = 3 })

// SAFE: Use idempotency key
httpClient.DefaultRequestHeaders.Add("Idempotency-Key", orderId);
```

### Retrying Business Errors

```csharp
// BAD: Retrying validation failures
ShouldHandle = static args =>
    ValueTask.FromResult(!args.Outcome.Result?.IsSuccessStatusCode ?? true)

// GOOD: Only retry transient errors
ShouldHandle = static args =>
    ValueTask.FromResult(
        args.Outcome.Result?.StatusCode == HttpStatusCode.ServiceUnavailable)
```

### Infinite or Excessive Retries

```csharp
// BAD: Too many retries
.AddRetry(new RetryStrategyOptions { MaxRetryAttempts = 100 })

// GOOD: Reasonable limit with circuit breaker
.AddRetry(new RetryStrategyOptions { MaxRetryAttempts = 3 })
.AddCircuitBreaker(/* options */)
```

---

**Related:** `polly-patterns.md`, `circuit-breaker-config.md`
