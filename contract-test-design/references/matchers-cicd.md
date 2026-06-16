# Pact Matchers & CI/CD Integration

## Pact Matchers Reference

| Matcher | Usage | Example |
|---------|-------|---------|
| `Match.Type()` | Any value of same type | `Match.Type("example")` |
| `Match.Integer()` | Any integer | `Match.Integer(42)` |
| `Match.Decimal()` | Any decimal | `Match.Decimal(99.99m)` |
| `Match.Regex()` | Pattern match | `Match.Regex(@"\d+", "123")` |
| `Match.MinType()` | Array with min items | `Match.MinType(item, 1)` |
| `Match.MaxType()` | Array with max items | `Match.MaxType(item, 10)` |
| `Match.Each()` | All items match | `Match.Each(item)` |
| `Match.Include()` | Contains substring | `Match.Include("error")` |

### Matcher Examples

```csharp
// Flexible status matching
status = Match.Regex("pending|confirmed|shipped|delivered", "pending")

// Array with at least 1 item
items = Match.MinType(new { productId = Match.Type("prod-001") }, 1)

// Optional field (can be null)
notes = Match.Type(default(string))

// UUID pattern
id = Match.Regex(@"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", "550e8400-e29b-41d4-a716-446655440000")

// ISO 8601 timestamp
createdAt = Match.Regex(@"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", "2024-01-15T10:30:00Z")
```

---

## Breaking Change Detection

### Schema Comparison

```csharp
public class BreakingChangeDetector
{
    public IEnumerable<BreakingChange> DetectBreakingChanges(
        JsonSchema oldSchema,
        JsonSchema newSchema)
    {
        var changes = new List<BreakingChange>();

        // Check for removed fields
        foreach (var field in oldSchema.Properties)
        {
            if (!newSchema.Properties.ContainsKey(field.Key))
            {
                changes.Add(new BreakingChange
                {
                    Type = ChangeType.RemovedField,
                    Field = field.Key,
                    Severity = Severity.Breaking
                });
            }
        }

        // Check for type changes
        foreach (var field in oldSchema.Properties)
        {
            if (newSchema.Properties.TryGetValue(field.Key, out var newField))
            {
                if (field.Value.Type != newField.Type)
                {
                    changes.Add(new BreakingChange
                    {
                        Type = ChangeType.TypeChange,
                        Field = field.Key,
                        OldType = field.Value.Type,
                        NewType = newField.Type,
                        Severity = Severity.Breaking
                    });
                }
            }
        }

        // Check for new required fields
        var newRequired = newSchema.Required.Except(oldSchema.Required);
        foreach (var field in newRequired)
        {
            if (!oldSchema.Properties.ContainsKey(field))
            {
                changes.Add(new BreakingChange
                {
                    Type = ChangeType.NewRequiredField,
                    Field = field,
                    Severity = Severity.Breaking
                });
            }
        }

        return changes;
    }
}
```

### Breaking vs Non-Breaking Changes

| Change Type | Breaking? | Action |
|-------------|-----------|--------|
| Remove field | Yes | Block deployment |
| Change field type | Yes | Block deployment |
| Add required field | Yes | Block deployment |
| Remove endpoint | Yes | Block deployment |
| Add optional field | No | Allow |
| Add new endpoint | No | Allow |
| Add optional parameter | No | Allow |
| Deprecate (with notice) | No | Allow |

---

## CI/CD Integration

### Can-I-Deploy Check (GitHub Actions)

```yaml
can-i-deploy:
  runs-on: ubuntu-latest
  steps:
    - name: Can I Deploy?
      run: |
        docker run --rm \
          pactfoundation/pact-cli:latest \
          pact-broker can-i-deploy \
          --pacticipant "WebApp" \
          --version "${{ github.sha }}" \
          --to-environment production \
          --broker-base-url https://your-broker.pactflow.io \
          --broker-token ${{ secrets.PACT_BROKER_TOKEN }}
```

### Full Consumer Pipeline

```yaml
name: Consumer Contract Tests
on: [push, pull_request]

jobs:
  contract-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Run Contract Tests
        run: dotnet test --filter Category=Contract

      - name: Publish Pacts
        run: |
          docker run --rm -v ./pacts:/pacts \
            pactfoundation/pact-cli:latest \
            pact-broker publish /pacts \
            --consumer-app-version ${{ github.sha }} \
            --branch ${{ github.ref_name }} \
            --broker-base-url https://your-broker.pactflow.io \
            --broker-token ${{ secrets.PACT_BROKER_TOKEN }}

      - name: Can I Deploy?
        run: |
          docker run --rm \
            pactfoundation/pact-cli:latest \
            pact-broker can-i-deploy \
            --pacticipant "WebApp" \
            --version "${{ github.sha }}" \
            --to-environment production \
            --broker-base-url https://your-broker.pactflow.io \
            --broker-token ${{ secrets.PACT_BROKER_TOKEN }}
```

### Full Provider Pipeline

```yaml
name: Provider Contract Verification
on: [push, pull_request]

jobs:
  verify-contracts:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Start Provider
        run: |
          dotnet run &
          sleep 10

      - name: Verify Consumer Contracts
        run: dotnet test --filter Category=ContractVerification

      - name: Can I Deploy?
        run: |
          docker run --rm \
            pactfoundation/pact-cli:latest \
            pact-broker can-i-deploy \
            --pacticipant "OrderApi" \
            --version "${{ github.sha }}" \
            --to-environment production \
            --broker-base-url https://your-broker.pactflow.io \
            --broker-token ${{ secrets.PACT_BROKER_TOKEN }}
```

---

## Deployment Workflow

```text
┌─────────────────────────────────────────────────────────────┐
│                    CONSUMER DEPLOYMENT                       │
│                                                             │
│  1. Run tests     2. Publish pact    3. Can-I-Deploy?       │
│     ┌─────┐          ┌─────┐            ┌─────┐             │
│     │Tests│  ──────► │Broker│  ──────►  │Check│  ──────►    │
│     └─────┘          └─────┘            └─────┘             │
│                                             │               │
│                                    ┌────────┴────────┐      │
│                                    │                 │      │
│                               Pass: Deploy      Fail: Block │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    PROVIDER DEPLOYMENT                       │
│                                                             │
│  1. Run tests     2. Verify pacts   3. Can-I-Deploy?        │
│     ┌─────┐          ┌─────┐            ┌─────┐             │
│     │Tests│  ──────► │Verify│  ──────►  │Check│  ──────►    │
│     └─────┘          └─────┘            └─────┘             │
│                                             │               │
│                                    ┌────────┴────────┐      │
│                                    │                 │      │
│                               Pass: Deploy      Fail: Block │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
