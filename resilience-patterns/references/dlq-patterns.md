# Dead Letter Queue Patterns

## Overview

Dead Letter Queues (DLQs) capture messages that cannot be processed after retry attempts are exhausted. This guide covers DLQ implementation patterns and handling strategies.

## When Messages Go to DLQ

```text
Message Received
       ↓
 Handler Processing
       ↓
    Failure?
       │
   yes │ no
       ↓   ↓
    Retry   Success
       │
       ↓
  Retry 1, 2, 3...
       │
       ↓
  Max Retries Exceeded
       │
       ↓
  ┌─────────────────┐
  │  Dead Letter    │
  │     Queue       │
  └─────────────────┘
```

## Common DLQ Scenarios

| Scenario | Description | Action |
| --- | --- | --- |
| **Poison Message** | Malformed data that causes handler to crash | Fix data, republish |
| **Business Rule Violation** | Valid format but invalid business state | Manual review |
| **Dependency Failure** | External service permanently down | Fix dependency, replay |
| **Schema Mismatch** | Message version incompatible with handler | Update handler, replay |
| **Timeout** | Processing took too long | Investigate, optimize |

## Brighter DLQ Configuration

### Basic Setup

```csharp
services.AddBrighter()
    .UseExternalBus(config =>
    {
        config.Publication.RequeueCount = 3;     // 3 attempts before DLQ
        config.Publication.RequeueDelayInMs = 1000;  // 1s between attempts
    });
```

### RabbitMQ DLQ

```csharp
var connection = new RmqMessagingGatewayConnection
{
    AmpqUri = new AmqpUriSpecification(new Uri("amqp://guest:guest@localhost:5672")),
    Exchange = new Exchange("orders.exchange"),
    DeadLetterExchange = new Exchange("orders.dlx")  // Dead letter exchange
};
```

### AWS SQS DLQ

```csharp
var sqsConfig = new SqsPublication
{
    RedrivePolicy = new RedrivePolicy
    {
        DeadLetterQueueArn = "arn:aws:sqs:region:account:my-queue-dlq",
        MaxReceiveCount = 3
    }
};
```

## DLQ Message Structure

### Preserve Original Message

```csharp
public class DeadLetterMessage
{
    public string OriginalMessageId { get; set; }
    public string OriginalMessageBody { get; set; }
    public string OriginalQueue { get; set; }
    public DateTime OriginalTimestamp { get; set; }
    public DateTime DlqTimestamp { get; set; }
    public int RetryCount { get; set; }
    public string LastException { get; set; }
    public string LastExceptionStackTrace { get; set; }
    public Dictionary<string, string> Headers { get; set; }
}
```

### Enrichment on DLQ Entry

```csharp
public class DlqEnricher
{
    public DeadLetterMessage Enrich(Message original, Exception lastException)
    {
        return new DeadLetterMessage
        {
            OriginalMessageId = original.Header.Id,
            OriginalMessageBody = original.Body.Value,
            OriginalQueue = original.Header.Topic,
            OriginalTimestamp = original.Header.TimeStamp,
            DlqTimestamp = DateTime.UtcNow,
            RetryCount = GetRetryCount(original),
            LastException = lastException.Message,
            LastExceptionStackTrace = lastException.StackTrace,
            Headers = original.Header.Bag
        };
    }
}
```

## DLQ Processing Patterns

### Manual Review Dashboard

```csharp
public class DlqDashboardController : Controller
{
    [HttpGet]
    public async Task<IActionResult> GetMessages(int page = 1, int pageSize = 20)
    {
        var messages = await _dlqService.GetMessages(page, pageSize);
        return View(messages);
    }

    [HttpPost("replay/{messageId}")]
    public async Task<IActionResult> Replay(string messageId)
    {
        await _dlqService.ReplayMessage(messageId);
        return Ok();
    }

    [HttpPost("discard/{messageId}")]
    public async Task<IActionResult> Discard(string messageId)
    {
        await _dlqService.DiscardMessage(messageId);
        return Ok();
    }
}
```

### Automated Categorization

```csharp
public class DlqCategorizer
{
    public DlqCategory Categorize(DeadLetterMessage message)
    {
        var exception = message.LastException;

        return exception switch
        {
            var e when e.Contains("ValidationException") => DlqCategory.InvalidData,
            var e when e.Contains("TimeoutException") => DlqCategory.Timeout,
            var e when e.Contains("ConnectionException") => DlqCategory.DependencyFailure,
            var e when e.Contains("JsonException") => DlqCategory.PoisonMessage,
            _ => DlqCategory.Unknown
        };
    }
}

public enum DlqCategory
{
    InvalidData,      // Business validation failure
    Timeout,          // Processing too slow
    DependencyFailure, // External service down
    PoisonMessage,    // Can't deserialize
    Unknown           // Needs investigation
}
```

### Auto-Retry by Category

```csharp
public class DlqAutoRetryService
{
    public async Task ProcessDlqMessages()
    {
        var messages = await _dlqService.GetMessages();

        foreach (var message in messages)
        {
            var category = _categorizer.Categorize(message);

            switch (category)
            {
                case DlqCategory.Timeout:
                    // Auto-retry timeouts after delay
                    if (DateTime.UtcNow - message.DlqTimestamp > TimeSpan.FromMinutes(5))
                    {
                        await _dlqService.ReplayMessage(message.OriginalMessageId);
                    }
                    break;

                case DlqCategory.DependencyFailure:
                    // Check if dependency is healthy, then replay
                    if (await _healthCheck.IsHealthy(message.OriginalQueue))
                    {
                        await _dlqService.ReplayMessage(message.OriginalMessageId);
                    }
                    break;

                case DlqCategory.PoisonMessage:
                case DlqCategory.InvalidData:
                    // These need manual intervention
                    await _alertService.NotifyDlqReview(message);
                    break;
            }
        }
    }
}
```

## Replay Patterns

### Single Message Replay

```csharp
public class DlqReplayService
{
    public async Task ReplayMessage(string messageId)
    {
        var dlqMessage = await _repository.GetById(messageId);

        // Reconstruct original message
        var message = new Message(
            new MessageHeader(dlqMessage.OriginalMessageId, dlqMessage.OriginalQueue),
            new MessageBody(dlqMessage.OriginalMessageBody));

        // Republish to original queue
        await _producer.SendAsync(message);

        // Mark as replayed
        await _repository.MarkReplayed(messageId);
    }
}
```

### Bulk Replay with Filter

```csharp
public async Task BulkReplay(DlqCategory category, DateTime since)
{
    var messages = await _repository.GetByCategory(category, since);

    foreach (var batch in messages.Chunk(100))
    {
        await Task.WhenAll(batch.Select(m => ReplayMessage(m.Id)));
        await Task.Delay(1000);  // Rate limit
    }
}
```

## Monitoring and Alerting

### Key Metrics

| Metric | Description | Alert Threshold |
| --- | --- | --- |
| `dlq.depth` | Messages in DLQ | > 0 |
| `dlq.age.oldest` | Age of oldest message | > 1 hour |
| `dlq.growth_rate` | Messages added per minute | > 10/min |
| `dlq.replay.success_rate` | Successful replays | < 90% |

### Alert Configuration

```csharp
public class DlqMonitor
{
    public async Task CheckDlqHealth()
    {
        var depth = await _dlqService.GetDepth();
        var oldestAge = await _dlqService.GetOldestMessageAge();

        if (depth > 0)
        {
            await _alertService.SendWarning($"DLQ has {depth} messages");
        }

        if (oldestAge > TimeSpan.FromHours(1))
        {
            await _alertService.SendCritical(
                $"DLQ has unprocessed messages older than {oldestAge}");
        }
    }
}
```

## Anti-Patterns

### Ignoring DLQ

**Problem:** DLQ becomes a black hole.

**Fix:** Monitor depth, set up alerts, establish review process.

### Auto-Replay Everything

**Problem:** Poison messages replay infinitely.

**Fix:** Categorize before replay, limit replay attempts.

### No Metadata

**Problem:** Can't diagnose why message failed.

**Fix:** Preserve original message, exception, retry count.

### DLQ as Archive

**Problem:** Messages never cleaned up.

**Fix:** Establish retention policy, archive or delete old messages.

---

**Related:** `brighter-resilience.md`, `retry-strategies.md`
