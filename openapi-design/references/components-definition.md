# OpenAPI Components Definition

**Load when:** Defining schemas, parameters, responses, and security schemes

## Table of Contents

- [Schemas](#schemas)
- [Parameters](#parameters)
- [Responses](#responses)
- [Security Schemes](#security-schemes)

## Schemas

### Enums

```yaml
components:
  schemas:
    OrderStatus:
      type: string
      enum:
        - draft
        - submitted
        - paid
        - shipped
        - delivered
        - cancelled
      description: Current status of the order
```

### Value Objects

```yaml
    Money:
      type: object
      required:
        - amount
        - currency
      properties:
        amount:
          type: number
          format: decimal
          minimum: 0
          example: 99.99
        currency:
          type: string
          pattern: '^[A-Z]{3}$'
          example: USD
```

### Entities

```yaml
    Order:
      type: object
      required:
        - id
        - customerId
        - status
        - createdAt
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        customerId:
          type: string
          format: uuid
        status:
          $ref: '#/components/schemas/OrderStatus'
        items:
          type: array
          items:
            $ref: '#/components/schemas/LineItem'
        subtotal:
          $ref: '#/components/schemas/Money'
        tax:
          $ref: '#/components/schemas/Money'
        total:
          $ref: '#/components/schemas/Money'
        createdAt:
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          type: string
          format: date-time
          readOnly: true

    LineItem:
      type: object
      required:
        - productId
        - productName
        - quantity
        - unitPrice
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        productId:
          type: string
        productName:
          type: string
        quantity:
          type: integer
          minimum: 1
          maximum: 1000
        unitPrice:
          $ref: '#/components/schemas/Money'
        lineTotal:
          $ref: '#/components/schemas/Money'
          readOnly: true
```

### Request/Response Wrappers

```yaml
    CreateOrderRequest:
      type: object
      required:
        - customerId
      properties:
        customerId:
          type: string
          format: uuid
        items:
          type: array
          items:
            $ref: '#/components/schemas/CreateLineItemRequest'

    CreateLineItemRequest:
      type: object
      required:
        - productId
        - quantity
      properties:
        productId:
          type: string
        quantity:
          type: integer
          minimum: 1

    UpdateOrderRequest:
      type: object
      properties:
        customerId:
          type: string
          format: uuid

    OrderResponse:
      allOf:
        - $ref: '#/components/schemas/Order'
        - type: object
          properties:
            _links:
              $ref: '#/components/schemas/OrderLinks'

    OrderLinks:
      type: object
      properties:
        self:
          type: string
          format: uri
        submit:
          type: string
          format: uri
        cancel:
          type: string
          format: uri

    OrderListResponse:
      type: object
      required:
        - items
        - pagination
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/OrderResponse'
        pagination:
          $ref: '#/components/schemas/Pagination'

    Pagination:
      type: object
      required:
        - page
        - pageSize
        - totalItems
        - totalPages
      properties:
        page:
          type: integer
          minimum: 1
        pageSize:
          type: integer
          minimum: 1
          maximum: 100
        totalItems:
          type: integer
          minimum: 0
        totalPages:
          type: integer
          minimum: 0
```

### Error Responses (RFC 7807)

```yaml
    ProblemDetails:
      type: object
      required:
        - type
        - title
        - status
      properties:
        type:
          type: string
          format: uri
          description: URI reference identifying the problem type
        title:
          type: string
          description: Short, human-readable summary
        status:
          type: integer
          description: HTTP status code
        detail:
          type: string
          description: Human-readable explanation
        instance:
          type: string
          format: uri
          description: URI reference to specific occurrence
        errors:
          type: object
          additionalProperties:
            type: array
            items:
              type: string
          description: Validation errors by field
```

## Parameters

```yaml
  parameters:
    PageNumber:
      name: page
      in: query
      description: Page number (1-based)
      schema:
        type: integer
        minimum: 1
        default: 1

    PageSize:
      name: pageSize
      in: query
      description: Number of items per page
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20
```

## Responses

```yaml
  responses:
    BadRequest:
      description: Invalid request
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'

    Unauthorized:
      description: Authentication required
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'

    Forbidden:
      description: Insufficient permissions
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'

    NotFound:
      description: Resource not found
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'

    Conflict:
      description: Resource conflict (e.g., state transition not allowed)
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'

    ValidationError:
      description: Validation failed
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'
```

## Security Schemes

```yaml
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token from authentication service

    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
      description: API key for service-to-service calls
```
