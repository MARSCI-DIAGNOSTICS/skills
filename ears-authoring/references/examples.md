# EARS Pattern Examples

Real-world examples for each EARS pattern organized by domain.

## Ubiquitous Pattern Examples

### Security Domain

```yaml
- id: "REQ-SEC-001"
  text: "The system SHALL encrypt all data at rest using AES-256"
  ears_type: ubiquitous
  priority: must

- id: "REQ-SEC-002"
  text: "The API SHALL authenticate all incoming requests"
  ears_type: ubiquitous
  priority: must

- id: "REQ-SEC-003"
  text: "The system SHALL hash passwords using bcrypt with cost factor 12"
  ears_type: ubiquitous
  priority: must
```

### Performance Domain

```yaml
- id: "REQ-PERF-001"
  text: "The API SHALL respond to health checks within 100ms"
  ears_type: ubiquitous
  priority: must

- id: "REQ-PERF-002"
  text: "The system SHALL support 10,000 concurrent connections"
  ears_type: ubiquitous
  priority: should

- id: "REQ-PERF-003"
  text: "The database queries SHALL complete within 500ms"
  ears_type: ubiquitous
  priority: should
```

### Data Integrity Domain

```yaml
- id: "REQ-DATA-001"
  text: "The system SHALL validate all user input before processing"
  ears_type: ubiquitous
  priority: must

- id: "REQ-DATA-002"
  text: "The application SHALL maintain referential integrity for all relationships"
  ears_type: ubiquitous
  priority: must

- id: "REQ-DATA-003"
  text: "The service SHALL log all data modifications with timestamp and user ID"
  ears_type: ubiquitous
  priority: must
```

## State-Driven Pattern Examples

### System State Domain

```yaml
- id: "REQ-STATE-001"
  text: "WHILE in maintenance mode, the system SHALL display a maintenance banner to all users"
  ears_type: state-driven
  priority: must

- id: "REQ-STATE-002"
  text: "WHILE the system is starting up, the load balancer SHALL return 503 Service Unavailable"
  ears_type: state-driven
  priority: must

- id: "REQ-STATE-003"
  text: "WHILE in read-only mode, the system SHALL reject all write operations with appropriate error messages"
  ears_type: state-driven
  priority: must
```

### Connection State Domain

```yaml
- id: "REQ-CONN-001"
  text: "WHILE the WebSocket connection is active, the system SHALL send heartbeat messages every 30 seconds"
  ears_type: state-driven
  priority: must

- id: "REQ-CONN-002"
  text: "WHILE disconnected from the primary database, the system SHALL route queries to the replica"
  ears_type: state-driven
  priority: should

- id: "REQ-CONN-003"
  text: "WHILE the API rate limit is exceeded, the system SHALL queue incoming requests"
  ears_type: state-driven
  priority: should
```

### User State Domain

```yaml
- id: "REQ-USER-001"
  text: "WHILE the user is authenticated, the system SHALL display the user dashboard"
  ears_type: state-driven
  priority: must

- id: "REQ-USER-002"
  text: "WHILE the user session is active, the system SHALL refresh the access token before expiration"
  ears_type: state-driven
  priority: must

- id: "REQ-USER-003"
  text: "WHILE the user is in admin mode, the system SHALL show administrative controls"
  ears_type: state-driven
  priority: must
```

## Event-Driven Pattern Examples

### User Interaction Domain

```yaml
- id: "REQ-UI-001"
  text: "WHEN a user submits the registration form, the system SHALL validate all required fields"
  ears_type: event-driven
  priority: must

- id: "REQ-UI-002"
  text: "WHEN a user clicks the logout button, the system SHALL invalidate the session and redirect to login"
  ears_type: event-driven
  priority: must

- id: "REQ-UI-003"
  text: "WHEN a user uploads a file, the system SHALL scan for malware before storage"
  ears_type: event-driven
  priority: must
```

### System Events Domain

```yaml
- id: "REQ-SYS-001"
  text: "WHEN the application starts, the system SHALL verify database connectivity"
  ears_type: event-driven
  priority: must

- id: "REQ-SYS-002"
  text: "WHEN a configuration change is detected, the system SHALL reload affected components"
  ears_type: event-driven
  priority: should

- id: "REQ-SYS-003"
  text: "WHEN memory usage exceeds 80%, the system SHALL trigger garbage collection"
  ears_type: event-driven
  priority: should
```

### Data Events Domain

```yaml
- id: "REQ-EVT-001"
  text: "WHEN a new order is created, the system SHALL publish an OrderCreated event"
  ears_type: event-driven
  priority: must

- id: "REQ-EVT-002"
  text: "WHEN payment is confirmed, the system SHALL update the order status to Paid"
  ears_type: event-driven
  priority: must

- id: "REQ-EVT-003"
  text: "WHEN an entity is modified, the system SHALL update the LastModified timestamp"
  ears_type: event-driven
  priority: must
```

## Unwanted Behavior Pattern Examples

### Authentication Failures

```yaml
- id: "REQ-AUTH-001"
  text: "IF authentication fails three times, THEN the system SHALL lock the account for 15 minutes"
  ears_type: unwanted
  priority: must

- id: "REQ-AUTH-002"
  text: "IF the access token is expired, THEN the system SHALL return 401 Unauthorized"
  ears_type: unwanted
  priority: must

- id: "REQ-AUTH-003"
  text: "IF the user provides invalid credentials, THEN the system SHALL log the failed attempt"
  ears_type: unwanted
  priority: must
```

### Infrastructure Failures

```yaml
- id: "REQ-INFRA-001"
  text: "IF the database connection fails, THEN the system SHALL retry with exponential backoff"
  ears_type: unwanted
  priority: must

- id: "REQ-INFRA-002"
  text: "IF the external service is unavailable, THEN the system SHALL return cached data if available"
  ears_type: unwanted
  priority: should

- id: "REQ-INFRA-003"
  text: "IF disk space falls below 10%, THEN the system SHALL trigger an alert and pause non-critical operations"
  ears_type: unwanted
  priority: must
```

### Validation Failures

```yaml
- id: "REQ-VAL-001"
  text: "IF input validation fails, THEN the system SHALL return detailed error messages for each invalid field"
  ears_type: unwanted
  priority: must

- id: "REQ-VAL-002"
  text: "IF the uploaded file exceeds the size limit, THEN the system SHALL reject with a 413 Payload Too Large"
  ears_type: unwanted
  priority: must

- id: "REQ-VAL-003"
  text: "IF the request payload is malformed, THEN the system SHALL return 400 Bad Request with parse error details"
  ears_type: unwanted
  priority: must
```

## Optional Feature Pattern Examples

### UI Customization Domain

```yaml
- id: "REQ-OPT-001"
  text: "WHERE dark mode is enabled, the system SHALL render all UI components with the dark theme"
  ears_type: optional
  priority: should

- id: "REQ-OPT-002"
  text: "WHERE high contrast mode is configured, the system SHALL increase color contrast ratios to WCAG AAA"
  ears_type: optional
  priority: could

- id: "REQ-OPT-003"
  text: "WHERE compact view is selected, the system SHALL reduce padding and font sizes"
  ears_type: optional
  priority: could
```

### Security Features Domain

```yaml
- id: "REQ-SEC-OPT-001"
  text: "WHERE two-factor authentication is enabled, the system SHALL require OTP after password verification"
  ears_type: optional
  priority: should

- id: "REQ-SEC-OPT-002"
  text: "WHERE audit logging is configured, the system SHALL log all data access with user context"
  ears_type: optional
  priority: should

- id: "REQ-SEC-OPT-003"
  text: "WHERE IP whitelisting is enabled, the system SHALL reject requests from non-whitelisted IPs"
  ears_type: optional
  priority: should
```

### Performance Features Domain

```yaml
- id: "REQ-PERF-OPT-001"
  text: "WHERE caching is enabled, the system SHALL cache API responses for the configured TTL"
  ears_type: optional
  priority: should

- id: "REQ-PERF-OPT-002"
  text: "WHERE lazy loading is configured, the system SHALL defer loading of non-critical resources"
  ears_type: optional
  priority: could

- id: "REQ-PERF-OPT-003"
  text: "WHERE compression is enabled, the system SHALL gzip responses larger than 1KB"
  ears_type: optional
  priority: should
```

## Complex Pattern Examples

### State + Event Combinations

```yaml
- id: "REQ-CMPLX-001"
  text: "WHILE the system is in degraded mode, WHEN a critical request arrives, the system SHALL prioritize processing"
  ears_type: complex
  priority: must

- id: "REQ-CMPLX-002"
  text: "WHILE connected to the message broker, WHEN a message is received, the system SHALL acknowledge within 5 seconds"
  ears_type: complex
  priority: must

- id: "REQ-CMPLX-003"
  text: "WHILE in batch processing mode, WHEN an item fails, the system SHALL log the failure and continue with remaining items"
  ears_type: complex
  priority: should
```

### State + Unwanted Combinations

```yaml
- id: "REQ-CMPLX-004"
  text: "WHILE in production mode, IF an unhandled exception occurs, THEN the system SHALL notify the operations team"
  ears_type: complex
  priority: must

- id: "REQ-CMPLX-005"
  text: "WHILE processing payments, IF the payment gateway times out, THEN the system SHALL mark the transaction as pending"
  ears_type: complex
  priority: must

- id: "REQ-CMPLX-006"
  text: "WHILE the user is authenticated, IF the session is inactive for 30 minutes, THEN the system SHALL require re-authentication"
  ears_type: complex
  priority: must
```

### Optional + Event Combinations

```yaml
- id: "REQ-CMPLX-007"
  text: "WHERE webhooks are configured, WHEN an order status changes, the system SHALL POST to registered webhook URLs"
  ears_type: complex
  priority: should

- id: "REQ-CMPLX-008"
  text: "WHERE email notifications are enabled, WHEN a password reset is requested, the system SHALL send a reset email"
  ears_type: complex
  priority: should

- id: "REQ-CMPLX-009"
  text: "WHERE real-time updates are enabled, WHEN data changes, the system SHALL push updates via WebSocket"
  ears_type: complex
  priority: should
```

### Optional + Unwanted Combinations

```yaml
- id: "REQ-CMPLX-010"
  text: "WHERE strict validation is enabled, IF any field is invalid, THEN the system SHALL reject the entire request"
  ears_type: complex
  priority: should

- id: "REQ-CMPLX-011"
  text: "WHERE debug mode is enabled, IF an error occurs, THEN the system SHALL include stack trace in the response"
  ears_type: complex
  priority: could

- id: "REQ-CMPLX-012"
  text: "WHERE failover is configured, IF the primary service fails, THEN the system SHALL route to the backup service"
  ears_type: complex
  priority: should
```

## Complete Specification Example

A complete feature specification using multiple EARS patterns:

```yaml
id: "SPEC-AUTH-001"
title: "User Authentication Feature"
type: feature

context:
  problem: |
    Users cannot securely access their accounts without
    a robust authentication mechanism.
  motivation: |
    Secure authentication protects user data and prevents
    unauthorized access to the system.

requirements:
  - id: "REQ-001"
    text: "The system SHALL authenticate users using email and password"
    priority: must
    ears_type: ubiquitous
    acceptance_criteria:
      - id: "AC-001"
        given: "a registered user"
        when: "the user provides valid credentials"
        then: "the system grants access"

  - id: "REQ-002"
    text: "WHEN a user provides valid credentials, the system SHALL issue a JWT token"
    priority: must
    ears_type: event-driven
    acceptance_criteria:
      - id: "AC-002"
        given: "valid user credentials"
        when: "authentication succeeds"
        then: "the system returns a JWT token"

  - id: "REQ-003"
    text: "WHILE the user is authenticated, the system SHALL validate the JWT on each request"
    priority: must
    ears_type: state-driven
    acceptance_criteria:
      - id: "AC-003"
        given: "a user with a valid JWT"
        when: "the user makes an API request"
        then: "the system validates the token before processing"

  - id: "REQ-004"
    text: "IF authentication fails three times, THEN the system SHALL lock the account for 15 minutes"
    priority: must
    ears_type: unwanted
    acceptance_criteria:
      - id: "AC-004"
        given: "a user who has failed authentication twice"
        when: "the user fails a third time"
        then: "the account is locked for 15 minutes"

  - id: "REQ-005"
    text: "WHERE two-factor authentication is enabled, the system SHALL require OTP after password"
    priority: should
    ears_type: optional
    acceptance_criteria:
      - id: "AC-005"
        given: "a user with 2FA enabled"
        when: "the user provides valid password"
        then: "the system prompts for OTP"

metadata:
  status: approved
  created: "2025-12-24"
  provider: ears
  bounded_context: "Orchestration"
```
