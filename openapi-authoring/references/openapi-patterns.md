# OpenAPI Design Patterns

## Resource Design Patterns

### Collection + Item Pattern

```yaml
pattern:
  name: "Collection + Item"
  description: "Standard CRUD pattern for resources"

  paths:
    /resources:
      get: "List collection (paginated)"
      post: "Create item in collection"

    /resources/{id}:
      get: "Get single item"
      put: "Replace item"
      patch: "Partially update item"
      delete: "Remove item"

  naming_conventions:
    collection: "Plural nouns (resources, users, orders)"
    id_parameter: "Singular + Id suffix (resourceId, userId)"
    avoid: "Verbs in paths, nested resources beyond 2 levels"

  example:
    /orders:
      get: "List orders"
      post: "Create order"
    /orders/{orderId}:
      get: "Get order"
      put: "Update order"
      delete: "Cancel order"
    /orders/{orderId}/items:
      get: "List order items (max 1 level nesting)"
```

### Sub-Resource Pattern

```yaml
pattern:
  name: "Sub-Resource"
  description: "Resources that exist only within a parent context"

  rules:
    - "Use when child cannot exist without parent"
    - "Maximum 2 levels of nesting"
    - "Consider flattening if sub-resource has own identity"

  example:
    paths:
      /users/{userId}/preferences:
        get: "Get user preferences"
        put: "Replace user preferences"
        patch: "Update user preferences"

      /orders/{orderId}/items:
        get: "List order items"
        post: "Add item to order"

      /orders/{orderId}/items/{itemId}:
        get: "Get order item"
        patch: "Update order item quantity"
        delete: "Remove item from order"

  anti_pattern:
    avoid: "/users/{userId}/orders/{orderId}/items/{itemId}/details"
    reason: "Too deeply nested"
    better: "/order-items/{itemId}"
```

### Action Pattern

```yaml
pattern:
  name: "Action (RPC-style)"
  description: "For operations that don't map to CRUD"

  when_to_use:
    - "State transitions (publish, archive, approve)"
    - "Complex operations (calculate, validate)"
    - "Batch operations"
    - "Long-running operations"

  approaches:
    verb_suffix:
      example: "POST /orders/{orderId}/cancel"
      pros: "Clear intent, discoverable"
      cons: "Not purely RESTful"

    controller_resource:
      example: "POST /order-cancellations"
      pros: "RESTful, auditable"
      cons: "Less intuitive"

  examples:
    state_transitions:
      - "POST /documents/{id}/publish"
      - "POST /orders/{id}/ship"
      - "POST /users/{id}/activate"

    calculations:
      - "POST /shipping/calculate"
      - "POST /quotes"

    batch_operations:
      - "POST /emails/send-bulk"
      - "DELETE /notifications/read"
```

### Search Pattern

```yaml
pattern:
  name: "Search"
  description: "Complex queries beyond simple filtering"

  approaches:
    query_parameters:
      example: "GET /products?category=electronics&minPrice=100"
      use_when: "Simple filters, few parameters"

    search_resource:
      example: "POST /products/search"
      use_when: "Complex queries, many parameters, saved searches"
      request_body:
        query: "laptop"
        filters:
          category: ["electronics"]
          priceRange:
            min: 100
            max: 1000
        sort:
          field: "relevance"
          direction: "desc"

  response_pattern:
    data: []
    pagination: {}
    facets:
      category:
        - value: "laptops"
          count: 45
        - value: "accessories"
          count: 12
    appliedFilters: []
```

## Response Patterns

### Envelope Pattern

```yaml
pattern:
  name: "Response Envelope"
  description: "Wrap responses in consistent structure"

  structure:
    data: "Primary response content"
    meta: "Metadata (pagination, timing)"
    links: "HATEOAS links"

  single_item:
    data:
      id: "123"
      name: "Example"
    links:
      self: "/resources/123"

  collection:
    data:
      - { id: "1", name: "First" }
      - { id: "2", name: "Second" }
    meta:
      pagination:
        page: 1
        pageSize: 20
        totalItems: 100
    links:
      self: "/resources?page=1"
      next: "/resources?page=2"

  pros:
    - "Consistent response structure"
    - "Room for metadata without breaking clients"
    - "HATEOAS support built-in"

  cons:
    - "Extra nesting"
    - "Slightly larger payloads"
```

### HATEOAS Pattern

```yaml
pattern:
  name: "HATEOAS (Hypermedia)"
  description: "Include navigational links in responses"

  link_relations:
    standard:
      self: "Current resource"
      collection: "Parent collection"
      next: "Next page"
      prev: "Previous page"
      first: "First page"
      last: "Last page"

    custom:
      cancel: "Cancel action link"
      approve: "Approval action"
      related: "Related resource"

  example:
    id: "order-123"
    status: "pending"
    total: 99.99
    _links:
      self:
        href: "/orders/order-123"
      items:
        href: "/orders/order-123/items"
      customer:
        href: "/customers/cust-456"
      cancel:
        href: "/orders/order-123/cancel"
        method: "POST"
      approve:
        href: "/orders/order-123/approve"
        method: "POST"
        condition: "status == 'pending'"

  maturity_levels:
    level_0: "Plain JSON, no links"
    level_1: "Self link only"
    level_2: "Navigation links (next/prev)"
    level_3: "Action links with methods"
```

### Partial Response Pattern

```yaml
pattern:
  name: "Partial Response (Field Selection)"
  description: "Allow clients to request specific fields"

  implementation:
    parameter: "fields"
    format: "Comma-separated field names"

  example:
    request: "GET /users/123?fields=id,name,email"
    response:
      id: "123"
      name: "John Doe"
      email: "john@example.com"

  nested_fields:
    request: "GET /orders/123?fields=id,total,customer(name,email)"
    response:
      id: "123"
      total: 99.99
      customer:
        name: "John Doe"
        email: "john@example.com"

  expand_pattern:
    parameter: "expand"
    description: "Include related resources inline"
    request: "GET /orders/123?expand=customer,items"
    response:
      id: "123"
      customer:
        id: "cust-456"
        name: "John Doe"
      items:
        - id: "item-1"
          name: "Product A"
```

## Async Operation Patterns

### Long-Running Operation Pattern

```yaml
pattern:
  name: "Long-Running Operation"
  description: "Handle operations that take significant time"

  flow:
    1_initiate:
      request: "POST /reports/generate"
      response:
        status: 202
        headers:
          Location: "/operations/op-123"
        body:
          operationId: "op-123"
          status: "pending"
          links:
            status: "/operations/op-123"

    2_poll:
      request: "GET /operations/op-123"
      response_pending:
        status: 200
        body:
          operationId: "op-123"
          status: "running"
          progress: 45
          estimatedCompletion: "2025-01-15T10:30:00Z"

      response_complete:
        status: 200
        body:
          operationId: "op-123"
          status: "completed"
          result:
            reportId: "report-456"
          links:
            result: "/reports/report-456"

    3_retrieve:
      request: "GET /reports/report-456"
      response: "The generated report"

  status_values:
    - "pending"
    - "running"
    - "completed"
    - "failed"
    - "cancelled"

  webhook_alternative:
    description: "Callback instead of polling"
    request:
      callbackUrl: "https://client.example.com/webhooks/report-ready"
```

### Idempotency Pattern

```yaml
pattern:
  name: "Idempotency Key"
  description: "Ensure safe retries for non-idempotent operations"

  implementation:
    header: "Idempotency-Key"
    format: "Client-generated UUID"
    validity: "24-48 hours typically"

  request:
    POST /payments HTTP/1.1
    Idempotency-Key: "550e8400-e29b-41d4-a716-446655440000"
    Content-Type: application/json

    { "amount": 100.00, "currency": "USD" }

  behavior:
    first_request: "Process and store result"
    duplicate_request: "Return stored result"
    different_body_same_key: "Return 422 Unprocessable Entity"

  response_header:
    Idempotency-Replayed: "true"  # Indicates cached response

  storage_requirements:
    - "Store request hash + response"
    - "TTL-based expiration"
    - "Consider distributed cache for scalability"
```

## Security Patterns

### API Key Pattern

```yaml
pattern:
  name: "API Key Authentication"
  description: "Simple key-based authentication"

  locations:
    header:
      name: "X-API-Key"
      example: "X-API-Key: sk_live_abc123"

    query:
      name: "api_key"
      example: "/resources?api_key=sk_live_abc123"
      warning: "Less secure, logged in URLs"

  key_types:
    publishable: "pk_* - Safe for client-side"
    secret: "sk_* - Server-side only"
    test: "*_test_* - Test environment"
    live: "*_live_* - Production environment"

  openapi:
    components:
      securitySchemes:
        apiKey:
          type: apiKey
          in: header
          name: X-API-Key
```

### OAuth 2.0 Pattern

```yaml
pattern:
  name: "OAuth 2.0"
  description: "Token-based authentication with scopes"

  flows:
    authorization_code:
      use_case: "User-facing applications"
      steps:
        - "Redirect user to authorization server"
        - "User approves scopes"
        - "Receive authorization code"
        - "Exchange code for tokens"

    client_credentials:
      use_case: "Service-to-service"
      steps:
        - "POST client_id + client_secret to token endpoint"
        - "Receive access token"

  token_usage:
    header: "Authorization: Bearer {token}"

  scopes:
    pattern: "resource:action"
    examples:
      - "users:read"
      - "users:write"
      - "orders:read"
      - "orders:write"
      - "admin:all"

  openapi:
    components:
      securitySchemes:
        oauth2:
          type: oauth2
          flows:
            authorizationCode:
              authorizationUrl: "https://auth.example.com/authorize"
              tokenUrl: "https://auth.example.com/token"
              scopes:
                users:read: "Read user data"
                users:write: "Modify user data"
```

## Versioning Patterns

### URL Path Versioning

```yaml
pattern:
  name: "URL Path Versioning"
  description: "Version as part of URL path"

  format: "/v{major}/resources"

  examples:
    - "/v1/users"
    - "/v2/users"

  server_definition:
    servers:
      - url: "https://api.example.com/v1"
        description: "Version 1 (current)"
      - url: "https://api.example.com/v2"
        description: "Version 2 (preview)"

  routing:
    approach: "Route at load balancer/gateway level"
    benefits: "Clean separation, easy rollback"
```

### Header Versioning

```yaml
pattern:
  name: "Header Versioning"
  description: "Version specified in request header"

  header_options:
    custom: "API-Version: 2"
    accept: "Accept: application/vnd.example.v2+json"

  server_handling:
    default: "Latest stable version if no header"
    sunset: "Include Sunset header for deprecated versions"

  response_headers:
    API-Version: "2"
    Deprecation: "true"
    Sunset: "Sat, 31 Dec 2025 23:59:59 GMT"
    Link: '<https://api.example.com/v3/docs>; rel="successor-version"'
```

### Date-Based Versioning

```yaml
pattern:
  name: "Date-Based Versioning"
  description: "Version by release date"

  format: "YYYY-MM-DD"

  header: "API-Version: 2025-01-15"

  benefits:
    - "Clear timeline of changes"
    - "Fine-grained versioning"
    - "Easy to communicate deprecation"

  example:
    versions:
      - "2024-06-01"  # Original release
      - "2024-09-15"  # Added pagination
      - "2025-01-15"  # Breaking change to user schema

  sunset_policy:
    minimum_support: "12 months"
    deprecation_notice: "6 months before sunset"
```

---

**Last Updated:** 2025-12-26
