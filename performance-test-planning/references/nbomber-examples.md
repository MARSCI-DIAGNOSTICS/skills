# NBomber .NET Performance Testing

## Installation

```bash
dotnet add package NBomber
dotnet add package NBomber.Http
```

---

## Basic Load Test

```csharp
using NBomber.CSharp;
using NBomber.Http.CSharp;

var scenario = Scenario.Create("http_scenario", async context =>
{
    var request = Http.CreateRequest("GET", "https://api.example.com/products")
        .WithHeader("Accept", "application/json");

    var response = await Http.Send(request);

    return response.IsSuccessStatusCode
        ? Response.Ok()
        : Response.Fail();
})
.WithLoadSimulations(
    Simulation.Inject(rate: 100, interval: TimeSpan.FromSeconds(1), during: TimeSpan.FromMinutes(5)),
    Simulation.KeepConstant(copies: 100, during: TimeSpan.FromMinutes(10))
);

NBomberRunner
    .RegisterScenarios(scenario)
    .WithReportFileName("load_test_report")
    .WithReportFormats(ReportFormat.Html, ReportFormat.Csv)
    .Run();
```

---

## Complex Scenario with Steps

```csharp
var httpClient = new HttpClient();

var scenario = Scenario.Create("checkout_flow", async context =>
{
    // Step 1: Browse products
    var browseStep = await Step.Run("browse_products", context, async () =>
    {
        var response = await httpClient.GetAsync("https://api.example.com/products");
        return response.IsSuccessStatusCode
            ? Response.Ok(sizeBytes: (int)response.Content.Headers.ContentLength!)
            : Response.Fail();
    });

    // Step 2: Add to cart
    var cartStep = await Step.Run("add_to_cart", context, async () =>
    {
        var content = new StringContent("{\"productId\": 1, \"quantity\": 2}",
            Encoding.UTF8, "application/json");
        var response = await httpClient.PostAsync("https://api.example.com/cart", content);
        return response.IsSuccessStatusCode ? Response.Ok() : Response.Fail();
    });

    // Step 3: Checkout (only 15% of users)
    if (context.Random.NextDouble() < 0.15)
    {
        var checkoutStep = await Step.Run("checkout", context, async () =>
        {
            var response = await httpClient.PostAsync("https://api.example.com/checkout", null);
            return response.IsSuccessStatusCode ? Response.Ok() : Response.Fail();
        });
    }

    return Response.Ok();
})
.WithWarmUpDuration(TimeSpan.FromSeconds(30))
.WithLoadSimulations(
    Simulation.RampingConstant(copies: 100, during: TimeSpan.FromMinutes(2)),
    Simulation.KeepConstant(copies: 100, during: TimeSpan.FromMinutes(10))
);
```

---

## Data-Driven Load Test

```csharp
public class TestDataFeed
{
    public static IEnumerable<string> ProductIds()
    {
        return Enumerable.Range(1, 1000).Select(i => i.ToString());
    }
}

var productIds = new Queue<string>(TestDataFeed.ProductIds());

var scenario = Scenario.Create("product_load", async context =>
{
    string productId;
    lock (productIds)
    {
        productId = productIds.Count > 0 ? productIds.Dequeue() : "1";
    }

    var response = await httpClient.GetAsync($"https://api.example.com/products/{productId}");
    return response.IsSuccessStatusCode ? Response.Ok() : Response.Fail();
});
```

---

## Load Simulation Types

| Simulation | Description | Use Case |
|------------|-------------|----------|
| `Inject(rate, interval, during)` | Injects new scenarios at fixed rate | Constant arrival rate |
| `KeepConstant(copies, during)` | Maintains fixed number of copies | Steady load |
| `RampingConstant(copies, during)` | Ramps up to target copies | Gradual increase |
| `Pause(during)` | Pauses injection | Cool-down periods |

---

## Report Configuration

```csharp
NBomberRunner
    .RegisterScenarios(scenario)
    .WithReportFileName("performance_report")
    .WithReportFormats(ReportFormat.Html, ReportFormat.Csv, ReportFormat.Md)
    .WithReportFolder("./reports")
    .Run();
```
