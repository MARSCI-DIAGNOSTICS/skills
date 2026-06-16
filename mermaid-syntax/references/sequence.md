# Sequence Diagram Syntax

Sequence diagrams show interactions between participants over time.

## Basic Syntax

```mermaid
sequenceDiagram
    participant A as Alice
    participant B as Bob
    A->>B: Hello Bob
    B-->>A: Hi Alice
```

## Arrow Types

| Syntax | Description |
| --- | --- |
| `->` | Solid line without arrow |
| `-->` | Dotted line without arrow |
| `->>` | Solid line with arrow |
| `-->>` | Dotted line with arrow |
| `-x` | Solid line with cross |
| `--x` | Dotted line with cross |
| `-)` | Solid line with open arrow (async) |
| `--)` | Dotted line with open arrow (async) |

## Participant Types

```mermaid
sequenceDiagram
    participant U as User
    actor A as Admin
    participant S as Server
    participant D as Database
```

## Activation and Notes

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server

    C->>+S: Request
    Note right of S: Processing...
    S-->>-C: Response

    Note over C,S: Communication complete
```

## Loops, Alternatives, and Optionals

```mermaid
sequenceDiagram
    participant U as User
    participant S as Server
    participant DB as Database

    U->>S: Login Request

    alt Valid Credentials
        S->>DB: Verify
        DB-->>S: Success
        S-->>U: Token
    else Invalid Credentials
        S-->>U: Error 401
    end

    opt Remember Me
        S->>DB: Store Session
    end

    loop Health Check
        S->>DB: Ping
        DB-->>S: Pong
    end
```

## Complete Example

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant FE as Frontend
    participant API as API Server
    participant Auth as Auth Service
    participant DB as Database

    U->>FE: Click Login
    FE->>+API: POST /login
    API->>+Auth: Validate Token
    Auth->>DB: Check User
    DB-->>Auth: User Data
    Auth-->>-API: Valid
    API-->>-FE: 200 OK + JWT
    FE-->>U: Redirect to Dashboard
```
