# Message/Event Contract Testing

## Overview

Message contract testing verifies that async messages/events between services conform to agreed schemas. This is essential for event-driven architectures using message queues, event buses, or pub/sub systems.

---

## Async Message Consumer Test

```csharp
public class OrderEventConsumerTests
{
    [Fact]
    public void ReceiveOrderCreatedEvent_ProcessesSuccessfully()
    {
        var pact = Pact.V4("NotificationService", "OrderApi", new PactConfig
        {
            PactDir = "./pacts"
        });

        var messagePact = pact.WithMessageInteractions();

        messagePact
            .ExpectsToReceive("an order created event")
            .Given("order-123 was just created")
            .WithMetadata(new { contentType = "application/json" })
            .WithJsonContent(new
            {
                eventType = "OrderCreated",
                orderId = Match.Type("order-123"),
                customerId = Match.Type("customer-456"),
                orderTotal = Match.Decimal(99.99m),
                timestamp = Match.Type("2024-01-15T10:30:00Z")
            })
            .Verify<OrderCreatedEvent>(message =>
            {
                // Verify consumer can process the message
                var handler = new OrderCreatedEventHandler();
                var result = handler.Handle(message);
                Assert.True(result.IsSuccess);
            });
    }
}
```

---

## Async Message Provider Test

```csharp
public class OrderEventProviderTests
{
    [Fact]
    public void VerifyMessageContracts()
    {
        var verifier = new PactVerifier(new PactVerifierConfig());

        verifier
            .MessagingProvider("OrderApi")
            .WithProviderMessages(scenarios =>
            {
                scenarios.Add("an order created event", () =>
                {
                    return new OrderCreatedEvent
                    {
                        EventType = "OrderCreated",
                        OrderId = "order-123",
                        CustomerId = "customer-456",
                        OrderTotal = 99.99m,
                        Timestamp = DateTime.UtcNow
                    };
                });
            })
            .WithPactBrokerSource(new Uri("https://your-broker.pactflow.io"))
            .Verify();
    }
}
```

---

## Message Contract Patterns

### Event Versioning

```csharp
// Support multiple event versions
messagePact
    .ExpectsToReceive("an order created event v2")
    .WithJsonContent(new
    {
        version = Match.Integer(2),
        eventType = "OrderCreated",
        orderId = Match.Type("order-123"),
        // New fields in v2
        correlationId = Match.Type("corr-789"),
        metadata = new
        {
            source = Match.Type("web-app"),
            traceId = Match.Type("trace-abc")
        }
    });
```

### Multiple Event Types

```csharp
// Test different event types from same producer
[Theory]
[InlineData("OrderCreated", "order created")]
[InlineData("OrderUpdated", "order updated")]
[InlineData("OrderCancelled", "order cancelled")]
public void ReceiveOrderEvent_ProcessesSuccessfully(string eventType, string description)
{
    messagePact
        .ExpectsToReceive($"an {description} event")
        .WithJsonContent(new
        {
            eventType = eventType,
            orderId = Match.Type("order-123"),
            timestamp = Match.Type("2024-01-15T10:30:00Z")
        })
        .Verify<OrderEvent>(message =>
        {
            var handler = _handlers[eventType];
            Assert.True(handler.CanHandle(message));
        });
}
```

---

## Key Differences from HTTP Contracts

| Aspect | HTTP Contracts | Message Contracts |
|--------|----------------|-------------------|
| Direction | Request/Response | Fire-and-forget |
| Timing | Synchronous | Asynchronous |
| Provider verification | HTTP endpoint | Message producer |
| Consumer verification | HTTP client | Message handler |
| Metadata | Headers | Message properties |

---

## Best Practices

1. **Version your events**: Include version field for schema evolution
2. **Test all event types**: Each event type needs its own contract
3. **Include metadata**: Test correlation IDs, timestamps, sources
4. **Verify handlers**: Consumer tests should invoke actual handler code
5. **Provider produces real messages**: Verification should use actual event builders
