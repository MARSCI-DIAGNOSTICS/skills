# OpenAPI Paths Definition

**Load when:** Defining REST API endpoints, operations, parameters, and responses

## Table of Contents

- [Complete Paths Example](#complete-paths-example)
- [Path Patterns Summary](#path-patterns-summary)

## Complete Paths Example

```yaml
paths:
  /orders:
    get:
      operationId: listOrders
      summary: List orders
      description: Retrieve a paginated list of orders with optional filtering
      tags:
        - Orders
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/PageNumber'
        - $ref: '#/components/parameters/PageSize'
        - name: status
          in: query
          description: Filter by order status
          schema:
            $ref: '#/components/schemas/OrderStatus'
        - name: customerId
          in: query
          description: Filter by customer ID
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderListResponse'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'

    post:
      operationId: createOrder
      summary: Create order
      description: Create a new order in draft status
      tags:
        - Orders
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderRequest'
            examples:
              basic:
                summary: Basic order
                value:
                  customerId: "550e8400-e29b-41d4-a716-446655440000"
                  items:
                    - productId: "prod-123"
                      quantity: 2
      responses:
        '201':
          description: Order created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderResponse'
          headers:
            Location:
              description: URL of created order
              schema:
                type: string
                format: uri
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '422':
          $ref: '#/components/responses/ValidationError'

  /orders/{orderId}:
    parameters:
      - name: orderId
        in: path
        required: true
        description: Unique order identifier
        schema:
          type: string
          format: uuid

    get:
      operationId: getOrder
      summary: Get order by ID
      tags:
        - Orders
      security:
        - bearerAuth: []
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderResponse'
        '404':
          $ref: '#/components/responses/NotFound'

    patch:
      operationId: updateOrder
      summary: Update order
      description: Partially update an order (only allowed for draft orders)
      tags:
        - Orders
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateOrderRequest'
      responses:
        '200':
          description: Order updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '404':
          $ref: '#/components/responses/NotFound'
        '409':
          $ref: '#/components/responses/Conflict'

    delete:
      operationId: deleteOrder
      summary: Delete order
      description: Delete a draft order (cannot delete submitted orders)
      tags:
        - Orders
      security:
        - bearerAuth: []
      responses:
        '204':
          description: Order deleted
        '404':
          $ref: '#/components/responses/NotFound'
        '409':
          $ref: '#/components/responses/Conflict'

  /orders/{orderId}/submit:
    post:
      operationId: submitOrder
      summary: Submit order
      description: Submit order for processing (transitions from Draft to Submitted)
      tags:
        - Orders
      security:
        - bearerAuth: []
      parameters:
        - name: orderId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Order submitted
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderResponse'
        '400':
          description: Order cannot be submitted
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'
        '404':
          $ref: '#/components/responses/NotFound'
```

## Path Patterns Summary

| Pattern | Purpose | Example |
|---------|---------|---------|
| `/{resource}` | Collection | `/orders` |
| `/{resource}/{id}` | Single resource | `/orders/{orderId}` |
| `/{resource}/{id}/{action}` | Resource action | `/orders/{orderId}/submit` |
| `/{parent}/{id}/{child}` | Nested resource | `/orders/{orderId}/items` |
