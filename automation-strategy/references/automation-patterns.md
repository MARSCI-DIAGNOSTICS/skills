# Automation Patterns (.NET Playwright)

## Page Object Model

```csharp
public class LoginPage
{
    private readonly IPage _page;

    public LoginPage(IPage page)
    {
        _page = page;
    }

    // Locators
    private ILocator EmailInput => _page.Locator("[data-testid='email']");
    private ILocator PasswordInput => _page.Locator("[data-testid='password']");
    private ILocator LoginButton => _page.Locator("[data-testid='login-button']");
    private ILocator ErrorMessage => _page.Locator("[data-testid='error-message']");

    // Actions
    public async Task<DashboardPage> LoginAsync(string email, string password)
    {
        await EmailInput.FillAsync(email);
        await PasswordInput.FillAsync(password);
        await LoginButton.ClickAsync();
        await _page.WaitForURLAsync("**/dashboard");
        return new DashboardPage(_page);
    }

    public async Task<LoginPage> LoginWithInvalidCredentialsAsync(string email, string password)
    {
        await EmailInput.FillAsync(email);
        await PasswordInput.FillAsync(password);
        await LoginButton.ClickAsync();
        await ErrorMessage.WaitForAsync();
        return this;
    }

    // Assertions
    public async Task<string> GetErrorMessageAsync()
    {
        return await ErrorMessage.TextContentAsync();
    }
}
```

---

## Fluent Test Builder

```csharp
public class OrderBuilder
{
    private readonly Order _order = new();

    public OrderBuilder WithCustomer(string customerId)
    {
        _order.CustomerId = customerId;
        return this;
    }

    public OrderBuilder WithItem(string productId, int quantity)
    {
        _order.Items.Add(new OrderItem { ProductId = productId, Quantity = quantity });
        return this;
    }

    public OrderBuilder WithShipping(string address)
    {
        _order.ShippingAddress = address;
        return this;
    }

    public OrderBuilder AsPremiumCustomer()
    {
        _order.IsPremium = true;
        _order.DiscountRate = 0.10m;
        return this;
    }

    public Order Build() => _order;
}

// Usage in tests
var order = new OrderBuilder()
    .WithCustomer("CUST-001")
    .WithItem("PROD-123", 2)
    .WithItem("PROD-456", 1)
    .AsPremiumCustomer()
    .Build();
```

---

## Test Fixture Pattern

```csharp
public class OrderTestFixture : IAsyncLifetime
{
    public IPage Page { get; private set; } = null!;
    public IBrowser Browser { get; private set; } = null!;
    public string BaseUrl { get; } = "https://localhost:5001";

    public async Task InitializeAsync()
    {
        var playwright = await Playwright.CreateAsync();
        Browser = await playwright.Chromium.LaunchAsync(new()
        {
            Headless = true
        });
        Page = await Browser.NewPageAsync();

        // Seed test data
        await SeedTestData();

        // Login once
        var loginPage = new LoginPage(Page);
        await Page.GotoAsync($"{BaseUrl}/login");
        await loginPage.LoginAsync("test@example.com", "password123");
    }

    public async Task DisposeAsync()
    {
        await CleanupTestData();
        await Browser.DisposeAsync();
    }

    private async Task SeedTestData()
    {
        // Create test products, customers, etc.
    }

    private async Task CleanupTestData()
    {
        // Remove test artifacts
    }
}

// Usage
public class OrderTests : IClassFixture<OrderTestFixture>
{
    private readonly OrderTestFixture _fixture;

    public OrderTests(OrderTestFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public async Task CreateOrder_ValidItems_Succeeds()
    {
        var ordersPage = new OrdersPage(_fixture.Page);
        await _fixture.Page.GotoAsync($"{_fixture.BaseUrl}/orders/new");

        await ordersPage.AddItemAsync("PROD-123", 2);
        await ordersPage.SubmitOrderAsync();

        var confirmationPage = new OrderConfirmationPage(_fixture.Page);
        Assert.True(await confirmationPage.IsDisplayedAsync());
    }
}
```

---

## Pattern Summary

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| Page Object Model | Encapsulate page interactions | All UI tests |
| Fluent Builder | Create test data | Complex object setup |
| Test Fixture | Shared setup/teardown | Expensive initialization |
| Repository | Test data access | Database interactions |
| Factory | Create test instances | Multiple test variants |

---

## Best Practices

1. **Locators**: Use `data-testid` attributes for stability
2. **Waits**: Use explicit waits, never `Thread.Sleep`
3. **Isolation**: Each test should be independent
4. **Naming**: Descriptive test names: `Action_Condition_ExpectedResult`
5. **Assertions**: One logical assertion per test
6. **Cleanup**: Always clean up test data in `DisposeAsync`
