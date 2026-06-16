# ER, State & Flowchart Patterns

## ER Diagram Patterns

### Blog Schema

```mermaid
erDiagram
    USER {
        uuid id PK
        string email UK
        string password_hash
        string name
        timestamp created_at
    }

    POST {
        uuid id PK
        uuid author_id FK
        string title
        text content
        enum status
        timestamp published_at
    }

    COMMENT {
        uuid id PK
        uuid post_id FK
        uuid user_id FK
        text content
        timestamp created_at
    }

    TAG {
        uuid id PK
        string name UK
    }

    POST_TAG {
        uuid post_id PK,FK
        uuid tag_id PK,FK
    }

    USER ||--o{ POST : writes
    USER ||--o{ COMMENT : writes
    POST ||--o{ COMMENT : has
    POST ||--o{ POST_TAG : has
    TAG ||--o{ POST_TAG : has
```

### E-Commerce Schema

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : "ordered in"
    PRODUCT }|--|| CATEGORY : "belongs to"
    CUSTOMER ||--o{ ADDRESS : has
    ORDER ||--|| ADDRESS : "ships to"
    ORDER ||--o| PAYMENT : "paid by"

    CUSTOMER {
        uuid id PK
        string email UK
        string name
    }

    ORDER {
        uuid id PK
        uuid customer_id FK
        uuid shipping_address_id FK
        enum status
        decimal total
    }

    ORDER_ITEM {
        uuid order_id PK,FK
        uuid product_id PK,FK
        int quantity
        decimal unit_price
    }

    PRODUCT {
        uuid id PK
        string sku UK
        string name
        decimal price
        int stock
    }
```

---

## State Diagram Patterns

### Order Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Draft

    Draft --> Submitted : submit
    Submitted --> Confirmed : confirm
    Submitted --> Cancelled : cancel

    Confirmed --> Processing : process
    Processing --> Shipped : ship
    Processing --> Cancelled : cancel

    Shipped --> Delivered : deliver
    Shipped --> Returned : return

    Delivered --> [*]
    Returned --> Refunded : refund
    Refunded --> [*]
    Cancelled --> [*]
```

### Authentication State

```mermaid
stateDiagram-v2
    [*] --> Anonymous

    Anonymous --> Authenticating : login
    Authenticating --> Authenticated : success
    Authenticating --> Anonymous : failure

    Authenticated --> Anonymous : logout
    Authenticated --> TokenRefresh : token_expiring
    TokenRefresh --> Authenticated : refresh_success
    TokenRefresh --> Anonymous : refresh_failure
```

---

## Flowchart Patterns

### Decision Tree

```mermaid
flowchart TD
    Start([Start]) --> Q1{Is it urgent?}
    Q1 -->|Yes| Q2{Is it important?}
    Q1 -->|No| Q3{Is it important?}

    Q2 -->|Yes| Do[Do it now]
    Q2 -->|No| Delegate[Delegate it]

    Q3 -->|Yes| Schedule[Schedule it]
    Q3 -->|No| Eliminate[Eliminate it]

    Do --> End([End])
    Delegate --> End
    Schedule --> End
    Eliminate --> End
```

### Error Handling Flow

```mermaid
flowchart TD
    Request([Request]) --> Validate{Valid?}

    Validate -->|Yes| Process[Process Request]
    Validate -->|No| ValidationError[Return 400]

    Process --> ExternalCall[Call External API]
    ExternalCall --> Success{Success?}

    Success -->|Yes| Transform[Transform Response]
    Success -->|No| Retry{Retries left?}

    Retry -->|Yes| Wait[Wait & Retry]
    Wait --> ExternalCall
    Retry -->|No| ServiceError[Return 503]

    Transform --> Cache[Cache Result]
    Cache --> Response([Return 200])

    ValidationError --> End([End])
    ServiceError --> End
    Response --> End
```
