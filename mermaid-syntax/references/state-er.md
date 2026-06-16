# State and ER Diagram Syntax

## State Diagram Syntax

State diagrams show state machines and transitions.

### Basic Syntax

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing : start
    Processing --> Complete : finish
    Processing --> Error : fail
    Error --> Idle : reset
    Complete --> [*]
```

### Composite States

```mermaid
stateDiagram-v2
    [*] --> Active

    state Active {
        [*] --> Idle
        Idle --> Running : start
        Running --> Paused : pause
        Paused --> Running : resume
        Running --> Idle : stop
    }

    Active --> Terminated : shutdown
    Terminated --> [*]
```

### Fork and Join

```mermaid
stateDiagram-v2
    state fork_state <<fork>>
    state join_state <<join>>

    [*] --> fork_state
    fork_state --> Task1
    fork_state --> Task2
    Task1 --> join_state
    Task2 --> join_state
    join_state --> [*]
```

### Complete Example

```mermaid
stateDiagram-v2
    [*] --> Draft

    Draft --> Submitted : submit
    Submitted --> UnderReview : assign_reviewer

    state UnderReview {
        [*] --> Reviewing
        Reviewing --> NeedsChanges : request_changes
        NeedsChanges --> Reviewing : resubmit
        Reviewing --> Approved : approve
    }

    UnderReview --> Published : publish
    UnderReview --> Rejected : reject

    Rejected --> Draft : revise
    Published --> [*]

    note right of Draft : Initial state
    note left of Published : Final state
```

---

## Entity Relationship Diagram Syntax

ER diagrams show database schemas and relationships.

### Basic Syntax

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "ordered in"
```

### Relationship Types

| Syntax | Meaning |
| --- | --- |
| `\|\|` | Exactly one |
| `o\|` | Zero or one |
| `}o` | Zero or more |
| `}\|` | One or more |

### Full Relationship Notation

| Syntax | Meaning |
| --- | --- |
| `\|\|--\|\|` | One to one |
| `\|\|--o{` | One to many |
| `o\|--o{` | Zero-or-one to many |
| `}\|--}\|` | Many to many |

### Entity Attributes

```mermaid
erDiagram
    CUSTOMER {
        string id PK
        string name
        string email UK
        date created_at
    }

    ORDER {
        string id PK
        string customer_id FK
        date order_date
        decimal total
        string status
    }

    CUSTOMER ||--o{ ORDER : places
```

### Complete Example

```mermaid
erDiagram
    USER {
        uuid id PK
        string email UK
        string password_hash
        string name
        timestamp created_at
        timestamp updated_at
    }

    POST {
        uuid id PK
        uuid author_id FK
        string title
        text content
        string status
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
        uuid post_id FK,PK
        uuid tag_id FK,PK
    }

    USER ||--o{ POST : writes
    USER ||--o{ COMMENT : writes
    POST ||--o{ COMMENT : has
    POST ||--o{ POST_TAG : has
    TAG ||--o{ POST_TAG : has
```
