# Sequence & Class Diagram Patterns

## Sequence Diagram Patterns

### API Request/Response

```mermaid
sequenceDiagram
    actor User
    participant FE as Frontend
    participant API as API Server
    participant DB as Database

    User->>FE: Action
    FE->>+API: Request
    API->>+DB: Query
    DB-->>-API: Data
    API-->>-FE: Response
    FE-->>User: Update UI
```

### Authentication Flow

```mermaid
sequenceDiagram
    actor User
    participant App as Application
    participant Auth as Auth Service
    participant Token as Token Store

    User->>App: Login request
    App->>Auth: Validate credentials
    alt Valid
        Auth->>Token: Generate token
        Token-->>Auth: JWT
        Auth-->>App: Success + JWT
        App-->>User: Redirect to dashboard
    else Invalid
        Auth-->>App: 401 Unauthorized
        App-->>User: Show error
    end
```

### Async Processing

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Queue
    participant Worker

    Client->>API: Submit job
    API->>Queue: Enqueue task
    API-->>Client: 202 Accepted + job ID

    Worker->>Queue: Poll for tasks
    Queue-->>Worker: Task data
    Worker->>Worker: Process

    Client->>API: Check status (polling)
    API-->>Client: Status: processing

    Worker->>API: Report completion
    Client->>API: Check status
    API-->>Client: Status: complete + result
```

---

## Class Diagram Patterns

### Domain Model

```mermaid
classDiagram
    class Entity {
        <<abstract>>
        +UUID id
        +DateTime createdAt
        +DateTime updatedAt
    }

    class User {
        +String email
        +String name
        +authenticate()
    }

    class Order {
        +OrderStatus status
        +Money total
        +submit()
        +cancel()
    }

    class OrderItem {
        +int quantity
        +Money price
    }

    Entity <|-- User
    Entity <|-- Order
    User "1" --> "*" Order : places
    Order "1" *-- "*" OrderItem : contains
```

### Repository Pattern

```mermaid
classDiagram
    class IRepository~T~ {
        <<interface>>
        +findById(id) T
        +findAll() List~T~
        +save(entity) T
        +delete(id) void
    }

    class UserRepository {
        +findByEmail(email) User
    }

    class InMemoryUserRepository {
        -Map~UUID,User~ store
    }

    class PostgresUserRepository {
        -DataSource ds
    }

    IRepository~T~ <|.. UserRepository
    UserRepository <|-- InMemoryUserRepository
    UserRepository <|-- PostgresUserRepository
```

### Service Layer

```mermaid
classDiagram
    class OrderService {
        -OrderRepository orderRepo
        -PaymentService paymentService
        -InventoryService inventoryService
        +createOrder(request) Order
        +cancelOrder(orderId) void
    }

    class PaymentService {
        -PaymentGateway gateway
        +processPayment(order) PaymentResult
        +refund(paymentId) void
    }

    class InventoryService {
        -InventoryRepository inventoryRepo
        +reserve(items) Reservation
        +release(reservationId) void
    }

    OrderService --> PaymentService
    OrderService --> InventoryService
```
