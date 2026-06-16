# Brighter Message Handler Resilience

## Overview

Brighter is a .NET library for implementing Command Query Responsibility Segregation (CQRS) with message-based patterns. This guide covers resilience patterns for Brighter message handlers.

## Basic Setup

### NuGet Packages

```xml
<PackageReference Include="Paramore.Brighter" Version="9.*" />
<PackageReference Include="Paramore.Brighter.Extensions.DependencyInjection" Version="9.*" />
<PackageReference Include="Paramore.Brighter.MessagingGateway.RMQ" Version="9.*" />
```

### Service Registration

```csharp
services.AddBrighter()
    .UseExternalBus(config =>
    {
        config.ProducerRegistry = producerRegistry;
    })
    .UsePolicyRegistry(policyRegistry)
    .MapperRegistryFromAssemblies(typeof(Program).Assembly)
    .HandlersFromAssemblies(typeof(Program).Assembly);
```

## Policy Registry

### Creating Policies

```csharp
var policyRegistry = new PolicyRegistry
{
    // Retry policy
    {
        "retry-policy",
        Policy
            .Handle<Exception>()
            .WaitAndRetry(
                retryCount: 3,
                sleepDurationProvider: attempt =>
                    TimeSpan.FromSeconds(Math.Pow(2, attempt)),
                onRetry: (exception, delay, attempt, context) =>
                {
                    _logger.LogWarning(
                        "Retry {Attempt} after {Delay}: {Message}",
                        attempt, delay, exception.Message);
                })
    },

    // Circuit breaker
    {
        "circuit-breaker",
        Policy
            .Handle<Exception>()
            .CircuitBreaker(
                exceptionsAllowedBeforeBreaking: 5,
                durationOfBreak: TimeSpan.FromSeconds(30))
    },

    // Timeout
    {
        "timeout-policy",
        Policy.Timeout(TimeSpan.FromSeconds(10))
    }
};
```

### Async Policies

```csharp
var policyRegistry = new PolicyRegistry
{
    {
        "async-retry-policy",
        Policy
            .Handle<Exception>()
            .WaitAndRetryAsync(
                retryCount: 3,
                sleepDurationProvider: attempt =>
                    TimeSpan.FromSeconds(Math.Pow(2, attempt)))
    }
};
```

## Applying Policies to Handlers

### Single Policy

```csharp
public class OrderCreatedHandler : RequestHandler<OrderCreated>
{
    [UsePolicy("retry-policy", step: 1)]
    public override OrderCreated Handle(OrderCreated command)
    {
        // Process order
        _orderService.Process(command);
        return base.Handle(command);
    }
}
```

### Multiple Policies (Ordered)

```csharp
public class PaymentHandler : RequestHandler<ProcessPayment>
{
    [UsePolicy("timeout-policy", step: 1)]      // Outer: timeout first
    [UsePolicy("retry-policy", step: 2)]         // Middle: retry
    [UsePolicy("circuit-breaker", step: 3)]      // Inner: circuit breaker
    public override ProcessPayment Handle(ProcessPayment command)
    {
        _paymentService.Process(command);
        return base.Handle(command);
    }
}
```

### Async Handlers

```csharp
public class AsyncOrderHandler : RequestHandlerAsync<OrderCreated>
{
    [UsePolicy("async-retry-policy", step: 1)]
    public override async Task<OrderCreated> HandleAsync(
        OrderCreated command,
        CancellationToken cancellationToken = default)
    {
        await _orderService.ProcessAsync(command, cancellationToken);
        return await base.HandleAsync(command, cancellationToken);
    }
}
```

## Fallback Handlers

### Implementing Fallback

```csharp
public class OrderFallbackHandler : RequestHandler<OrderCreated>
{
    [UseFallback(backstop: true, step: 1)]
    public override OrderCreated Handle(OrderCreated command)
    {
        // Fallback logic when main handler fails
        _logger.LogWarning("Fallback triggered for order {OrderId}", command.OrderId);

        // Store for later processing
        _failedOrderStore.Save(command);

        return base.Handle(command);
    }
}
```

### Fallback with Context

```csharp
public class ContextAwareFallbackHandler : RequestHandler<ProcessPayment>
{
    [UseFallback(backstop: true, step: 1)]
    public override ProcessPayment Handle(ProcessPayment command)
    {
        // Check if circuit is open
        if (Context.Bag.ContainsKey("CircuitBroken"))
        {
            // Queue for retry instead of immediate processing
            _queue.Enqueue(command);
            return command;
        }

        // Normal fallback
        _fallbackService.HandlePaymentFailure(command);
        return base.Handle(command);
    }
}
```

## Requeue and DLQ Behavior

### Configuring Requeue

```csharp
services.AddBrighter()
    .UseExternalBus(config =>
    {
        config.Publication.RequeueDelayInMs = 500;  // Delay before requeue
        config.Publication.RequeueCount = 3;         // Max requeues before DLQ
    });
```

### Custom Requeue Logic

```csharp
public class OrderHandler : RequestHandler<OrderCreated>
{
    public override OrderCreated Handle(OrderCreated command)
    {
        try
        {
            _orderService.Process(command);
        }
        catch (TransientException ex)
        {
            // Explicitly request requeue
            throw new DeferMessageAction();
        }
        catch (PermanentException ex)
        {
            // Don't requeue - will go to DLQ
            _logger.LogError("Permanent failure for {OrderId}", command.OrderId);
            throw;
        }

        return base.Handle(command);
    }
}
```

## Handler Pipeline

### Pipeline Order

```text
Message Received
       ↓
 [Timeout Policy]  ← step: 1 (outermost)
       ↓
 [Retry Policy]    ← step: 2
       ↓
 [Circuit Breaker] ← step: 3
       ↓
 [Handler Logic]   ← Your code
       ↓
 [Fallback]        ← If exception bubbles up
       ↓
 [DLQ]             ← If all retries exhausted
```

### Recommended Pipeline

```csharp
public class ResilientHandler : RequestHandler<MyCommand>
{
    [UsePolicy("timeout-policy", step: 1)]      // Prevent infinite waits
    [UsePolicy("circuit-breaker", step: 2)]     // Fail fast if service down
    [UsePolicy("retry-policy", step: 3)]        // Retry transient failures
    public override MyCommand Handle(MyCommand command)
    {
        // Handler logic
        return base.Handle(command);
    }
}
```

## Monitoring Handler Health

### Adding Metrics

```csharp
var policyRegistry = new PolicyRegistry
{
    {
        "instrumented-retry",
        Policy
            .Handle<Exception>()
            .WaitAndRetry(
                3,
                attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt)),
                onRetry: (exception, delay, attempt, context) =>
                {
                    _metrics.IncrementCounter("handler.retry", new[]
                    {
                        $"handler:{context["HandlerType"]}",
                        $"attempt:{attempt}"
                    });
                })
    }
};
```

### Handler Context

```csharp
public class ContextAwareHandler : RequestHandler<OrderCreated>
{
    public override OrderCreated Handle(OrderCreated command)
    {
        // Add context for policies
        Context.Bag["HandlerType"] = GetType().Name;
        Context.Bag["CorrelationId"] = command.CorrelationId;

        _orderService.Process(command);

        return base.Handle(command);
    }
}
```

## Anti-Patterns

### Catching and Swallowing

```csharp
// BAD: Swallows exception, prevents retry/DLQ
public override OrderCreated Handle(OrderCreated command)
{
    try
    {
        _service.Process(command);
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Failed");
        // Silently continues - message lost!
    }
    return base.Handle(command);
}

// GOOD: Let exceptions bubble for policy handling
public override OrderCreated Handle(OrderCreated command)
{
    _service.Process(command);  // Exception will trigger retry
    return base.Handle(command);
}
```

### Wrong Policy Order

```csharp
// BAD: Retry outside circuit breaker
[UsePolicy("retry-policy", step: 1)]         // Retries even when circuit open
[UsePolicy("circuit-breaker", step: 2)]

// GOOD: Circuit breaker outside retry
[UsePolicy("circuit-breaker", step: 1)]      // Fails fast when circuit open
[UsePolicy("retry-policy", step: 2)]         // Only retries when circuit closed
```

---

**Related:** `dlq-patterns.md`, `polly-patterns.md`
