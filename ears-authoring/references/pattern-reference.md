# EARS Pattern Reference

Complete syntax and rules for all six EARS patterns.

## Pattern Syntax Summary

| Pattern | Syntax | ears_type Value |
| --- | --- | --- |
| Ubiquitous | `The <entity> SHALL <action>` | `ubiquitous` |
| State-Driven | `WHILE <condition>, the <entity> SHALL <action>` | `state-driven` |
| Event-Driven | `WHEN <trigger>, the <entity> SHALL <action>` | `event-driven` |
| Unwanted | `IF <condition>, THEN the <entity> SHALL <action>` | `unwanted` |
| Optional | `WHERE <feature>, the <entity> SHALL <action>` | `optional` |
| Complex | `<Pattern1>, <Pattern2>, the <entity> SHALL <action>` | `complex` |

## Ubiquitous Pattern

### Syntax

```text
The <entity> SHALL <action>
```

### Components

| Component | Description | Examples |
| --- | --- | --- |
| `<entity>` | The system component performing the action | system, API, application, service, component |
| `SHALL` | Mandatory keyword indicating obligation | - |
| `<action>` | The behavior or capability required | encrypt data, log events, validate input |

### Detection Rules

A requirement is Ubiquitous if:

- Starts with "The" (article)
- Contains "SHALL"
- Does NOT contain: WHILE, WHEN, IF...THEN, WHERE

### Validation Regex

```regex
^The\s+\w+(\s+\w+)*\s+SHALL\s+.+$
```

### Valid Examples

```text
The system SHALL encrypt all data at rest
The API SHALL respond in JSON format
The application SHALL maintain audit logs
The service SHALL authenticate all requests
```

### Invalid Examples

```text
WHEN user clicks, the system SHALL...  # Event-driven, not ubiquitous
System should encrypt...               # Uses "should", not "SHALL"
Data shall be encrypted                # Passive voice
```

## State-Driven Pattern

### Syntax

```text
WHILE <condition>, the <entity> SHALL <action>
```

### Components

| Component | Description | Examples |
| --- | --- | --- |
| `WHILE` | Keyword indicating state condition | - |
| `<condition>` | The state that must be true | in maintenance mode, connected, authenticated |
| `<entity>` | The system component | system, service, component |
| `SHALL` | Mandatory keyword | - |
| `<action>` | The behavior during the state | display banner, send heartbeats |

### Detection Rules

A requirement is State-Driven if:

- Starts with "WHILE"
- Contains "SHALL"
- Describes a continuous state (not a point-in-time event)

### Validation Regex

```regex
^WHILE\s+.+,\s+the\s+\w+(\s+\w+)*\s+SHALL\s+.+$
```

### Valid Examples

```text
WHILE in maintenance mode, the system SHALL display a banner
WHILE the connection is active, the system SHALL send heartbeats every 30 seconds
WHILE the user is authenticated, the system SHALL show the user menu
WHILE processing a batch, the system SHALL display progress
```

### Invalid Examples

```text
WHEN in maintenance mode...  # WHEN indicates event, use WHILE for state
The system WHILE active...   # WHILE must come first
While active, system SHALL...  # "While" not capitalized, "the" missing
```

### State vs Event Distinction

| State (WHILE) | Event (WHEN) |
| --- | --- |
| In maintenance mode | Entering maintenance mode |
| Connection is active | Connection established |
| User is authenticated | User logs in |
| System is running | System starts |

## Event-Driven Pattern

### Syntax

```text
WHEN <trigger>, the <entity> SHALL <action>
```

### Components

| Component | Description | Examples |
| --- | --- | --- |
| `WHEN` | Keyword indicating trigger | - |
| `<trigger>` | The event that initiates action | user clicks, timeout occurs, request received |
| `<entity>` | The system component | system, service, component |
| `SHALL` | Mandatory keyword | - |
| `<action>` | The response to the trigger | validate, save, notify |

### Detection Rules

A requirement is Event-Driven if:

- Starts with "WHEN"
- Contains "SHALL"
- Describes a point-in-time event (not a continuous state)

### Validation Regex

```regex
^WHEN\s+.+,\s+the\s+\w+(\s+\w+)*\s+SHALL\s+.+$
```

### Valid Examples

```text
WHEN a user submits the form, the system SHALL validate all inputs
WHEN an error occurs, the system SHALL log the error details
WHEN the session expires, the system SHALL redirect to the login page
WHEN a file is uploaded, the system SHALL scan for malware
```

### Invalid Examples

```text
When user submits...         # "When" not capitalized
IF user clicks, THEN...      # IF-THEN is for unwanted behavior
WHILE user submits...        # WHILE is for states, not events
```

## Unwanted Behavior Pattern

### Syntax

```text
IF <condition>, THEN the <entity> SHALL <action>
```

### Components

| Component | Description | Examples |
| --- | --- | --- |
| `IF` | Keyword introducing unwanted condition | - |
| `<condition>` | The unwanted/error condition | authentication fails, timeout, invalid input |
| `THEN` | Keyword introducing response | - |
| `<entity>` | The system component | system, service, component |
| `SHALL` | Mandatory keyword | - |
| `<action>` | The handling response | lock account, retry, display error |

### Detection Rules

A requirement is Unwanted if:

- Contains "IF" and "THEN"
- Contains "SHALL"
- Describes error handling or exception response

### Validation Regex

```regex
^IF\s+.+,\s+THEN\s+the\s+\w+(\s+\w+)*\s+SHALL\s+.+$
```

### Valid Examples

```text
IF authentication fails, THEN the system SHALL lock the account after 3 attempts
IF the database is unavailable, THEN the system SHALL queue requests for retry
IF input validation fails, THEN the system SHALL display specific error messages
IF the request times out, THEN the system SHALL return a 504 Gateway Timeout
```

### Invalid Examples

```text
IF user clicks button, THEN...  # Normal behavior, use WHEN
IF feature is enabled, THEN...  # Optional feature, use WHERE
IF condition THEN system SHALL... # Missing comma after condition
```

### Reserved for Negative Conditions

IF-THEN is reserved for:

- Error handling
- Exception responses
- Failure modes
- Security violations
- Invalid states

NOT for:

- Normal user actions (use WHEN)
- Feature toggles (use WHERE)
- State-dependent behavior (use WHILE)

## Optional Feature Pattern

### Syntax

```text
WHERE <feature/config>, the <entity> SHALL <action>
```

### Components

| Component | Description | Examples |
| --- | --- | --- |
| `WHERE` | Keyword indicating optional feature | - |
| `<feature/config>` | The feature flag or configuration | dark mode enabled, audit logging configured |
| `<entity>` | The system component | system, service, component |
| `SHALL` | Mandatory keyword | - |
| `<action>` | The optional behavior | use dark theme, log access |

### Detection Rules

A requirement is Optional if:

- Starts with "WHERE"
- Contains "SHALL"
- Describes configurable or feature-flagged behavior

### Validation Regex

```regex
^WHERE\s+.+,\s+the\s+\w+(\s+\w+)*\s+SHALL\s+.+$
```

### Valid Examples

```text
WHERE dark mode is enabled, the system SHALL use the dark theme
WHERE audit logging is configured, the system SHALL log all data access
WHERE two-factor authentication is enabled, the system SHALL require OTP
WHERE caching is enabled, the system SHALL cache API responses
```

### Invalid Examples

```text
IF dark mode is enabled...   # IF is for unwanted behavior
WHEN dark mode is enabled... # WHEN is for events
Where feature enabled...     # "Where" not capitalized
```

## Complex Pattern

### Syntax

```text
<Pattern1>, <Pattern2>, the <entity> SHALL <action>
```

### Supported Combinations

| Combination | Example |
| --- | --- |
| WHILE + WHEN | WHILE active, WHEN timeout occurs, the system SHALL... |
| WHILE + IF-THEN | WHILE in prod mode, IF error occurs, THEN the system SHALL... |
| WHERE + WHEN | WHERE caching enabled, WHEN data changes, the system SHALL... |
| WHERE + IF-THEN | WHERE strict mode enabled, IF validation fails, THEN the system SHALL... |

### Detection Rules

A requirement is Complex if:

- Contains multiple pattern keywords (WHILE+WHEN, WHILE+IF, WHERE+WHEN, etc.)
- Contains "SHALL"

### Valid Examples

```text
WHILE active, WHEN timeout occurs, the system SHALL attempt reconnection
WHILE in production mode, IF error occurs, THEN the system SHALL notify the ops team
WHERE caching is enabled, WHEN data changes, the system SHALL invalidate the cache
WHERE strict validation is configured, IF input is invalid, THEN the system SHALL reject with details
```

### Guidelines

1. **Limit nesting:** Maximum 2 conditions recommended
2. **Order matters:** Outer condition first (WHILE/WHERE), inner condition second (WHEN/IF)
3. **Clarity:** If too complex, split into multiple requirements

## Keyword Summary

| Keyword | Pattern | Semantics |
| --- | --- | --- |
| (none) | Ubiquitous | Always applies |
| WHILE | State-Driven | During a state |
| WHEN | Event-Driven | Upon an event |
| IF...THEN | Unwanted | Error/exception handling |
| WHERE | Optional | When feature enabled |

## Canonical ears_type Values

For use in canonical specifications:

```yaml
ears_type: ubiquitous   # The system SHALL...
ears_type: state-driven # WHILE..., the system SHALL...
ears_type: event-driven # WHEN..., the system SHALL...
ears_type: unwanted     # IF..., THEN the system SHALL...
ears_type: optional     # WHERE..., the system SHALL...
ears_type: complex      # Combination of patterns
```
