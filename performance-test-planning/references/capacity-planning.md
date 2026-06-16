# Capacity Planning

## Little's Law

```text
L = λ × W

L = Average number of items in system
λ = Average arrival rate
W = Average time in system

Example:
- 1000 requests/second arrival rate
- 100ms average response time
- L = 1000 × 0.1 = 100 concurrent requests
```

---

## Throughput Calculation

```text
Throughput = Concurrent Users / Average Response Time

Example:
- 100 concurrent users
- 200ms average response time
- Throughput = 100 / 0.2 = 500 requests/second
```

---

## Capacity Planning Template

| Metric | Current | 6 Months | 1 Year | 2 Years |
|--------|---------|----------|--------|---------|
| Daily Active Users | 10,000 | 25,000 | 50,000 | 100,000 |
| Peak Concurrent | 500 | 1,250 | 2,500 | 5,000 |
| Requests/Second | 100 | 250 | 500 | 1,000 |
| Data Volume (GB) | 50 | 125 | 250 | 500 |
| App Servers | 2 | 4 | 8 | 16 |
| DB Size (GB) | 100 | 200 | 400 | 800 |

---

## Response Time Percentiles

| Percentile | Description | Typical Target |
|------------|-------------|----------------|
| p50 (median) | Typical user experience | < 100ms |
| p90 | Good user experience | < 200ms |
| p95 | Most users experience | < 300ms |
| p99 | Edge case performance | < 500ms |
| p99.9 | Outlier detection | < 1000ms |

---

## Apdex Score

```text
Apdex = (Satisfied + Tolerating/2) / Total

Satisfied: Response < T (threshold)
Tolerating: Response < 4T
Frustrated: Response >= 4T

Example (T = 200ms):
- 800 requests < 200ms (Satisfied)
- 150 requests 200-800ms (Tolerating)
- 50 requests > 800ms (Frustrated)
- Apdex = (800 + 75) / 1000 = 0.875
```

---

## BenchmarkDotNet for Micro-Benchmarks

```csharp
using BenchmarkDotNet.Attributes;
using BenchmarkDotNet.Running;

[MemoryDiagnoser]
[SimpleJob(RuntimeMoniker.Net80)]
public class SerializationBenchmarks
{
    private readonly Customer _customer = new()
    {
        Id = Guid.NewGuid(),
        Name = "Test Customer",
        Email = "test@example.com"
    };

    [Benchmark(Baseline = true)]
    public string JsonSerializer_Serialize()
    {
        return JsonSerializer.Serialize(_customer);
    }

    [Benchmark]
    public string Newtonsoft_Serialize()
    {
        return JsonConvert.SerializeObject(_customer);
    }
}

// Run benchmarks
BenchmarkRunner.Run<SerializationBenchmarks>();
```

---

## Capacity Planning Questions

1. **Current capacity**: What can the system handle today?
2. **Growth projection**: What's the expected growth rate?
3. **Peak multiplier**: How much higher is peak vs average?
4. **Safety margin**: What buffer do you need (typically 30-50%)?
5. **Scaling triggers**: At what utilization do you scale?
