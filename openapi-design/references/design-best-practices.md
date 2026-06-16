# OpenAPI Design Best Practices

**Load when:** Reviewing API design decisions, naming conventions, status codes, versioning, or validation

## Table of Contents

- [Naming Conventions](#naming-conventions)
- [HTTP Methods](#http-methods)
- [Status Codes](#status-codes)
- [Versioning Strategies](#versioning-strategies)
- [JSON Schema Validation](#json-schema-validation)

## Naming Conventions

```yaml
# Use camelCase for properties
customerId: string  # Good
customer_id: string # Avoid

# Use plural for collections
/orders          # Good
/order           # Avoid

# Use nouns for resources
/orders          # Good
/getOrders       # Avoid

# Use kebab-case for multi-word paths
/line-items      # Good
/lineItems       # Avoid
```

## HTTP Methods

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Retrieve resource(s) | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource | Yes | No |
| PATCH | Partial update | No* | No |
| DELETE | Remove resource | Yes | No |

*PATCH is idempotent if applying the same patch yields the same result

## Status Codes

| Code | Use For |
|------|---------|
| 200 | Successful GET, PUT, PATCH |
| 201 | Successful POST (resource created) |
| 204 | Successful DELETE (no content) |
| 400 | Malformed request syntax |
| 401 | Authentication required |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 409 | Conflict (state transition, duplicate) |
| 422 | Validation error |
| 500 | Server error |

## Versioning Strategies

### URL Path (Recommended for Breaking Changes)

```yaml
servers:
  - url: https://api.example.com/v1
  - url: https://api.example.com/v2
```

### Header-Based

```yaml
parameters:
  - name: API-Version
    in: header
    schema:
      type: string
      enum: ['2024-01-01', '2024-06-01']
```

## JSON Schema Validation

### Constraints

```yaml
# Numeric constraints
quantity:
  type: integer
  minimum: 1
  maximum: 1000

# String constraints
email:
  type: string
  format: email
  maxLength: 255

# Pattern validation
productCode:
  type: string
  pattern: '^[A-Z]{3}-\d{6}$'
```

### Enums for Known Values

```yaml
status:
  type: string
  enum: [draft, submitted, paid]
```

### Nullable Fields (OpenAPI 3.1)

```yaml
middleName:
  type: ['string', 'null']
```

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Verbs in URLs | `/getOrders` | Use HTTP methods: `GET /orders` |
| Inconsistent casing | Mix of camelCase/snake_case | Pick one, use consistently |
| Missing error schemas | Clients can't handle errors | Define ProblemDetails |
| No pagination | Large result sets crash clients | Always paginate collections |
| No versioning | Breaking changes break clients | Version from day one |
