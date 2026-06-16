# Pact Implementation (.NET)

## Consumer Test

```csharp
using PactNet;
using PactNet.Matchers;

public class OrderApiConsumerTests
{
    private readonly IPactBuilderV4 _pactBuilder;

    public OrderApiConsumerTests()
    {
        var pact = Pact.V4("WebApp", "OrderApi", new PactConfig
        {
            PactDir = "./pacts",
            LogLevel = PactLogLevel.Debug
        });

        _pactBuilder = pact.WithHttpInteractions();
    }

    [Fact]
    public async Task GetOrder_WhenOrderExists_ReturnsOrder()
    {
        // Arrange
        var orderId = "order-123";

        _pactBuilder
            .UponReceiving("a request to get an order")
            .Given("an order with id order-123 exists")
            .WithRequest(HttpMethod.Get, $"/api/orders/{orderId}")
            .WithHeader("Accept", "application/json")
            .WillRespond()
            .WithStatus(HttpStatusCode.OK)
            .WithHeader("Content-Type", "application/json")
            .WithJsonBody(new
            {
                id = Match.Type("order-123"),
                customerId = Match.Type("customer-456"),
                status = Match.Regex("pending|confirmed|shipped", "pending"),
                items = Match.MinType(new
                {
                    productId = Match.Type("prod-001"),
                    quantity = Match.Integer(2),
                    price = Match.Decimal(29.99m)
                }, 1),
                total = Match.Decimal(59.98m),
                createdAt = Match.Type("2024-01-15T10:30:00Z")
            });

        await _pactBuilder.VerifyAsync(async ctx =>
        {
            // Act
            var client = new OrderApiClient(ctx.MockServerUri);
            var order = await client.GetOrderAsync(orderId);

            // Assert
            Assert.NotNull(order);
            Assert.Equal("order-123", order.Id);
            Assert.Equal("pending", order.Status);
        });
    }

    [Fact]
    public async Task CreateOrder_WithValidData_ReturnsCreatedOrder()
    {
        // Arrange
        var newOrder = new CreateOrderRequest
        {
            CustomerId = "customer-456",
            Items = new List<OrderItemRequest>
            {
                new() { ProductId = "prod-001", Quantity = 2 }
            }
        };

        _pactBuilder
            .UponReceiving("a request to create an order")
            .Given("customer customer-456 exists")
            .WithRequest(HttpMethod.Post, "/api/orders")
            .WithHeader("Content-Type", "application/json")
            .WithJsonBody(new
            {
                customerId = Match.Type("customer-456"),
                items = Match.MinType(new
                {
                    productId = Match.Type("prod-001"),
                    quantity = Match.Integer(2)
                }, 1)
            })
            .WillRespond()
            .WithStatus(HttpStatusCode.Created)
            .WithHeader("Location", Match.Regex(@"/api/orders/[a-z0-9-]+", "/api/orders/order-789"))
            .WithJsonBody(new
            {
                id = Match.Type("order-789"),
                status = "pending"
            });

        await _pactBuilder.VerifyAsync(async ctx =>
        {
            var client = new OrderApiClient(ctx.MockServerUri);
            var result = await client.CreateOrderAsync(newOrder);

            Assert.NotNull(result.Id);
            Assert.Equal("pending", result.Status);
        });
    }

    [Fact]
    public async Task GetOrder_WhenNotFound_Returns404()
    {
        _pactBuilder
            .UponReceiving("a request for a non-existent order")
            .Given("no order with id missing-order exists")
            .WithRequest(HttpMethod.Get, "/api/orders/missing-order")
            .WillRespond()
            .WithStatus(HttpStatusCode.NotFound)
            .WithJsonBody(new
            {
                error = Match.Type("Order not found"),
                code = "ORDER_NOT_FOUND"
            });

        await _pactBuilder.VerifyAsync(async ctx =>
        {
            var client = new OrderApiClient(ctx.MockServerUri);
            var exception = await Assert.ThrowsAsync<OrderNotFoundException>(
                () => client.GetOrderAsync("missing-order"));

            Assert.Equal("ORDER_NOT_FOUND", exception.Code);
        });
    }
}
```

---

## Provider Verification

```csharp
using PactNet;
using PactNet.Verifier;

public class OrderApiProviderTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;
    private readonly ITestOutputHelper _output;

    public OrderApiProviderTests(
        WebApplicationFactory<Program> factory,
        ITestOutputHelper output)
    {
        _factory = factory;
        _output = output;
    }

    [Fact]
    public void VerifyPacts()
    {
        // Start the real API
        var client = _factory.CreateClient();
        var baseUri = client.BaseAddress!;

        // Configure provider states
        var providerStates = new Dictionary<string, Action>
        {
            ["an order with id order-123 exists"] = () =>
            {
                // Seed test data
                SeedOrder("order-123", "customer-456");
            },
            ["customer customer-456 exists"] = () =>
            {
                SeedCustomer("customer-456");
            },
            ["no order with id missing-order exists"] = () =>
            {
                // Ensure order doesn't exist
                DeleteOrder("missing-order");
            }
        };

        // Run verification
        var verifier = new PactVerifier(new PactVerifierConfig
        {
            LogLevel = PactLogLevel.Information,
            Outputters = new[] { new XUnitOutput(_output) }
        });

        verifier
            .ServiceProvider("OrderApi", baseUri)
            .WithProviderStateUrl(new Uri(baseUri, "/provider-states"))
            .WithPactBrokerSource(new Uri("https://your-broker.pactflow.io"), options =>
            {
                options.TokenAuthentication("your-token");
                options.ConsumerVersionSelectors(new ConsumerVersionSelector
                {
                    MainBranch = true
                });
                options.EnablePending();
                options.PublishResults("1.0.0");
            })
            .Verify();
    }

    private void SeedOrder(string orderId, string customerId)
    {
        using var scope = _factory.Services.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        db.Orders.Add(new Order
        {
            Id = orderId,
            CustomerId = customerId,
            Status = "pending",
            Items = new List<OrderItem>
            {
                new() { ProductId = "prod-001", Quantity = 2, Price = 29.99m }
            }
        });
        db.SaveChanges();
    }
}
```

---

## Provider State Endpoint

```csharp
// Add to provider API for test environment only
[ApiController]
[Route("provider-states")]
public class ProviderStatesController : ControllerBase
{
    private readonly IServiceProvider _services;

    [HttpPost]
    public IActionResult SetupProviderState([FromBody] ProviderState state)
    {
        switch (state.State)
        {
            case "an order with id order-123 exists":
                SetupExistingOrder("order-123");
                break;
            case "customer customer-456 exists":
                SetupCustomer("customer-456");
                break;
            case "no order with id missing-order exists":
                EnsureOrderDoesNotExist("missing-order");
                break;
        }

        return Ok();
    }
}

public class ProviderState
{
    public string Consumer { get; set; }
    public string State { get; set; }
    public Dictionary<string, string> Params { get; set; }
}
```

---

## Key Implementation Notes

### Consumer Test Structure

1. **Pact Builder Setup**: Initialize with consumer/provider names and config
2. **Interaction Definition**: Use `UponReceiving`, `Given`, `WithRequest`, `WillRespond`
3. **Matchers**: Use flexible matchers instead of exact values
4. **Verification**: Execute actual client code against mock server

### Provider Verification Structure

1. **Start Real API**: Use `WebApplicationFactory` or similar
2. **Provider States**: Set up test data for each interaction state
3. **Broker Integration**: Fetch contracts from Pact Broker
4. **Results Publishing**: Report verification results back to broker

### Provider State Best Practices

- Keep state setup idempotent
- Clean up between tests
- Use descriptive state names matching consumer tests
- Handle missing states gracefully
