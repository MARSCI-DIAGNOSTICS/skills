# Contract Testing Strategy Template

## Template

```markdown
# Contract Testing Strategy: [Project Name]

## 1. Service Map

### Services and Dependencies
```text
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Web App   │────►│  Order API  │────►│ Inventory   │
│ (Consumer)  │     │ (Provider)  │     │  (Provider) │
└─────────────┘     └──────┬──────┘     └─────────────┘
                          │
                   ┌──────▼──────┐
                   │  Payment    │
                   │  (Provider) │
                   └─────────────┘
```

### Contract Matrix

| Consumer | Provider | Contract Type | Priority |
|----------|----------|---------------|----------|
| Web App | Order API | REST/Pact | P1 |
| Order API | Inventory | REST/Pact | P1 |
| Order API | Payment | REST/Pact | P1 |
| Order API | Notification | Async/Message | P2 |

## 2. Contract Scope

### Included in Contracts

- Request method, path, headers
- Request body schema
- Response status codes
- Response body schema
- Required vs optional fields

### Excluded from Contracts

- Performance/timing
- Security headers (test separately)
- Rate limiting behavior
- Exact error message text

## 3. Tooling

### Selected Stack

| Purpose | Tool | Rationale |
|---------|------|-----------|
| Contract Framework | PactNet | .NET native, mature |
| Broker | Pact Broker | Standard, free tier |
| Async Contracts | Pact Message | Same ecosystem |
| Schema Validation | OpenAPI | Industry standard |

## 4. Workflow

### Consumer Workflow

1. Write consumer contract test
2. Run test → generates pact file
3. Publish pact to broker
4. Tag with branch/version

### Provider Workflow

1. Fetch contracts from broker
2. Run provider verification
3. Publish verification results
4. Can-I-Deploy check

### CI/CD Integration

```yaml
Consumer Pipeline:
  build → test → publish-pact → can-i-deploy → deploy

Provider Pipeline:
  build → test → verify-pacts → can-i-deploy → deploy
```

## 5. Breaking Change Policy

### Breaking Changes (Blocked)

- Removing fields consumers use
- Changing field types
- Removing endpoints
- Changing required fields

### Non-Breaking Changes (Allowed)

- Adding new optional fields
- Adding new endpoints
- Adding new optional parameters
- Deprecating (with notice period)

### Deprecation Process

1. Mark field deprecated in schema
2. Notify consumers (3 months)
3. Remove from contract tests
4. Remove from provider

## Strategy Checklist

Before starting contract testing:

- [ ] Service dependencies mapped
- [ ] Contract matrix defined
- [ ] Tooling selected
- [ ] Consumer/provider workflows documented
- [ ] Breaking change policy established
- [ ] Deprecation process defined
- [ ] CI/CD integration planned
