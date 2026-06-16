# Polly v8 Patterns for .NET

## Overview

Polly v8 introduces a new API based on resilience pipelines. This guide covers common patterns for HTTP clients and general resilience.

## NuGet Packages

```xml
<!-- Core Polly -->
<PackageReference Include="Polly" Version="8.*" />

<!-- HttpClient integration -->
<PackageReference Include="Microsoft.Extensions.Http.Resilience" Version="8.*" />

<!-- For standalone pipelines -->
<PackageReference Include="Polly.Extensions" Version="8.*" />
```

## HttpClient Resilience

### Standard Resilience Handler

The simplest approach - preconfigured best practices:

```csharp
builder.Services.AddHttpClient<IMyService, MyService>()
    .AddStandardResilienceHandler();
```

**Included strategies:**

1. Rate limiter (concurrent requests)
2. Total request timeout (30s default)
3. Retry (3 attempts, exponential backoff)
4. Circuit breaker (10% failure ratio)
5. Attempt timeout (10s per attempt)

### Custom Resilience Pipeline

For fine-tuned control:

```csharp
builder.Services.AddHttpClient<IPaymentService, PaymentService>()
    .AddResilienceHandler("payment", builder =>
    {
        builder
            .AddTimeout(TimeSpan.FromSeconds(30))  // Total timeout
            .AddRetry(new HttpRetryStrategyOptions
            {
                MaxRetryAttempts = 3,
                Delay = TimeSpan.FromMilliseconds(500),
                BackoffType = DelayBackoffType.Exponential,
                UseJitter = true,
                ShouldHandle = static args => ValueTask.FromResult(
                    args.Outcome.Result?.StatusCode is
                        HttpStatusCode.ServiceUnavailable or
                        HttpStatusCode.GatewayTimeout ||
                    args.Outcome.Exception is HttpRequestException)
            })
            .AddCircuitBreaker(new HttpCircuitBreakerStrategyOptions
            {
                FailureRatio = 0.5,
                MinimumThroughput = 10,
                SamplingDuration = TimeSpan.FromSeconds(30),
                BreakDuration = TimeSpan.FromSeconds(30)
            })
            .AddTimeout(TimeSpan.FromSeconds(10));  // Per-attempt timeout
    });
```

### Per-Endpoint Configuration

Different resilience for different endpoints:

```csharp
builder.Services.AddHttpClient<IOrderService, OrderService>()
    .AddResilienceHandler("orders-read", (builder, context) =>
    {
        // Fast timeout for reads
        builder.AddTimeout(TimeSpan.FromSeconds(5));
    })
    .AddResilienceHandler("orders-write", (builder, context) =>
    {
        // Longer timeout + retry for writes
        builder.AddTimeout(TimeSpan.FromSeconds(30));
        builder.AddRetry(new HttpRetryStrategyOptions
        {
            MaxRetryAttempts = 2,
            ShouldHandle = static args => ValueTask.FromResult(
                args.Outcome.Exception is HttpRequestException)
        });
    });
```

## Standalone Resilience Pipelines

### Creating a Pipeline

```csharp
var pipeline = new ResiliencePipelineBuilder<HttpResponseMessage>()
    .AddRetry(new RetryStrategyOptions<HttpResponseMessage>
    {
        MaxRetryAttempts = 3,
        Delay = TimeSpan.FromSeconds(1),
        BackoffType = DelayBackoffType.Exponential
    })
    .AddTimeout(TimeSpan.FromSeconds(10))
    .Build();
```

### Using a Pipeline

```csharp
var result = await pipeline.ExecuteAsync(async token =>
{
    return await httpClient.GetAsync("/api/orders", token);
}, cancellationToken);
```

### Registering Pipelines with DI

```csharp
builder.Services.AddResiliencePipeline<string, HttpResponseMessage>("http-pipeline", builder =>
{
    builder
        .AddRetry(new RetryStrategyOptions<HttpResponseMessage>())
        .AddCircuitBreaker(new CircuitBreakerStrategyOptions<HttpResponseMessage>())
        .AddTimeout(TimeSpan.FromSeconds(10));
});

// Inject and use
public class MyService
{
    private readonly ResiliencePipeline<HttpResponseMessage> _pipeline;

    public MyService(ResiliencePipelineProvider<string> provider)
    {
        _pipeline = provider.GetPipeline<HttpResponseMessage>("http-pipeline");
    }
}
```

## Strategy Patterns

### Retry with Custom Backoff

```csharp
.AddRetry(new RetryStrategyOptions<HttpResponseMessage>
{
    MaxRetryAttempts = 5,
    DelayGenerator = static args =>
    {
        // Custom delay based on attempt
        var delay = args.AttemptNumber switch
        {
            0 => TimeSpan.Zero,           // Immediate first retry
            1 => TimeSpan.FromMilliseconds(200),
            2 => TimeSpan.FromSeconds(1),
            3 => TimeSpan.FromSeconds(5),
            _ => TimeSpan.FromSeconds(10)
        };
        return ValueTask.FromResult<TimeSpan?>(delay);
    }
})
```

### Retry with OnRetry Callback

```csharp
.AddRetry(new RetryStrategyOptions<HttpResponseMessage>
{
    MaxRetryAttempts = 3,
    OnRetry = static args =>
    {
        Console.WriteLine($"Retry {args.AttemptNumber} after {args.RetryDelay}");
        Console.WriteLine($"Exception: {args.Outcome.Exception?.Message}");
        return default;
    }
})
```

### Retry-After Header Support

```csharp
.AddRetry(new HttpRetryStrategyOptions
{
    MaxRetryAttempts = 3,
    DelayGenerator = static args =>
    {
        if (args.Outcome.Result?.Headers.RetryAfter?.Delta is { } delta)
        {
            return ValueTask.FromResult<TimeSpan?>(delta);
        }
        // Fallback to exponential
        return ValueTask.FromResult<TimeSpan?>(
            TimeSpan.FromSeconds(Math.Pow(2, args.AttemptNumber)));
    }
})
```

### Circuit Breaker with Events

```csharp
.AddCircuitBreaker(new CircuitBreakerStrategyOptions<HttpResponseMessage>
{
    FailureRatio = 0.5,
    MinimumThroughput = 10,
    BreakDuration = TimeSpan.FromSeconds(30),
    OnOpened = static args =>
    {
        Console.WriteLine($"Circuit opened for {args.BreakDuration}");
        return default;
    },
    OnClosed = static args =>
    {
        Console.WriteLine("Circuit closed - service recovered");
        return default;
    },
    OnHalfOpened = static args =>
    {
        Console.WriteLine("Circuit half-open - testing service");
        return default;
    }
})
```

### Timeout with Fallback

```csharp
var pipeline = new ResiliencePipelineBuilder<HttpResponseMessage>()
    .AddTimeout(TimeSpan.FromSeconds(5))
    .AddFallback(new FallbackStrategyOptions<HttpResponseMessage>
    {
        ShouldHandle = static args => ValueTask.FromResult(
            args.Outcome.Exception is TimeoutRejectedException),
        FallbackAction = static args =>
        {
            return Outcome.FromResultAsValueTask(
                new HttpResponseMessage(HttpStatusCode.GatewayTimeout));
        }
    })
    .Build();
```

### Bulkhead Isolation

```csharp
.AddConcurrencyLimiter(new ConcurrencyLimiterOptions
{
    PermitLimit = 10,       // Max concurrent executions
    QueueLimit = 100        // Max queued requests
})
```

## Combined Pipelines

### Full HTTP Resilience Stack

```csharp
builder.Services.AddHttpClient<ICriticalService, CriticalService>()
    .AddResilienceHandler("critical-service", builder =>
    {
        // 1. Rate limiting (outermost)
        builder.AddConcurrencyLimiter(new ConcurrencyLimiterOptions
        {
            PermitLimit = 100,
            QueueLimit = 500
        });

        // 2. Total timeout
        builder.AddTimeout(TimeSpan.FromSeconds(60));

        // 3. Retry
        builder.AddRetry(new HttpRetryStrategyOptions
        {
            MaxRetryAttempts = 3,
            Delay = TimeSpan.FromSeconds(1),
            BackoffType = DelayBackoffType.Exponential,
            UseJitter = true
        });

        // 4. Circuit breaker
        builder.AddCircuitBreaker(new HttpCircuitBreakerStrategyOptions
        {
            FailureRatio = 0.25,
            MinimumThroughput = 20,
            SamplingDuration = TimeSpan.FromSeconds(60),
            BreakDuration = TimeSpan.FromMinutes(1)
        });

        // 5. Per-attempt timeout (innermost)
        builder.AddTimeout(TimeSpan.FromSeconds(10));
    });
```

### Pipeline with Hedging

```csharp
.AddHedging(new HttpHedgingStrategyOptions
{
    MaxHedgedAttempts = 2,
    Delay = TimeSpan.FromMilliseconds(500),
    ActionGenerator = static args =>
    {
        // Create hedged request
        return () => args.Callback(args.ActionContext);
    }
})
```

## Telemetry and Observability

### Enabling Telemetry

```csharp
builder.Services.AddResiliencePipeline("my-pipeline", builder =>
{
    builder.AddRetry(/* options */);
});

// Configure telemetry
builder.Services.Configure<TelemetryOptions>(options =>
{
    options.LoggerFactory = LoggerFactory.Create(builder =>
    {
        builder.AddConsole();
        builder.SetMinimumLevel(LogLevel.Debug);
    });
});
```

### OpenTelemetry Integration

```csharp
builder.Services.AddOpenTelemetry()
    .WithMetrics(metrics =>
    {
        metrics.AddMeter("Polly");
    })
    .WithTracing(tracing =>
    {
        tracing.AddSource("Polly");
    });
```

## Configuration from appsettings.json

```json
{
  "Resilience": {
    "PaymentService": {
      "Retry": {
        "MaxRetryAttempts": 3,
        "DelayMs": 500,
        "BackoffType": "Exponential"
      },
      "CircuitBreaker": {
        "FailureRatio": 0.5,
        "MinimumThroughput": 10,
        "BreakDurationSeconds": 30
      },
      "TimeoutSeconds": 10
    }
  }
}
```

```csharp
var config = builder.Configuration.GetSection("Resilience:PaymentService");

builder.Services.AddHttpClient<IPaymentService, PaymentService>()
    .AddResilienceHandler("payment", (builder, context) =>
    {
        var retryConfig = config.GetSection("Retry");
        builder.AddRetry(new HttpRetryStrategyOptions
        {
            MaxRetryAttempts = retryConfig.GetValue<int>("MaxRetryAttempts"),
            Delay = TimeSpan.FromMilliseconds(retryConfig.GetValue<int>("DelayMs"))
        });
    });
```

## Migration from Polly v7

### Policy → Strategy

```csharp
// v7
Policy
    .Handle<HttpRequestException>()
    .WaitAndRetryAsync(3, attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt)));

// v8
new ResiliencePipelineBuilder()
    .AddRetry(new RetryStrategyOptions
    {
        MaxRetryAttempts = 3,
        Delay = TimeSpan.FromSeconds(1),
        BackoffType = DelayBackoffType.Exponential
    })
    .Build();
```

### PolicyRegistry → ResiliencePipelineRegistry

```csharp
// v7
var registry = new PolicyRegistry();
registry.Add("my-policy", myPolicy);

// v8
builder.Services.AddResiliencePipeline("my-pipeline", builder => { /* ... */ });
```

---

**Related:** `circuit-breaker-config.md`, `retry-strategies.md`
