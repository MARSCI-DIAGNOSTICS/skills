# INVEST Criteria Reference

Detailed guidance on applying INVEST criteria to requirements.

## Overview

INVEST is an acronym that defines six quality criteria for well-formed requirements and user stories. Each criterion ensures requirements are suitable for agile development.

## Independent

### Definition

A requirement should be self-contained and implementable without depending on other requirements being completed first.

### Why It Matters

- Enables flexible prioritization
- Allows parallel development
- Reduces scheduling complexity
- Supports incremental delivery

### Assessment Questions

- Can this be implemented without waiting for other requirements?
- Can this be deployed independently?
- Does this have hidden dependencies?

### Examples

**Poor (Dependent):**

```text
FR-2: The system shall display order history.
(Depends on FR-1: Order creation being complete)
```

**Better (Independent):**

```text
FR-2: The system shall display order history.
- Can show "No orders yet" if none exist
- Does not require order creation to function
```

### Fixing Dependency Issues

| Situation | Solution |
| --- | --- |
| Hard dependency | Combine into single requirement |
| Soft dependency | Document but allow parallel work |
| Technical dependency | Extract to infrastructure story |
| Data dependency | Create stub/mock data approach |

---

## Negotiable

### Definition

Requirements should describe what is needed, not how to implement it, leaving room for discussion about the best approach.

### Why It Matters

- Leverages team expertise
- Allows creative solutions
- Adapts to constraints discovered during implementation
- Reduces rework from over-specification

### Assessment Questions

- Does this prescribe implementation details?
- Is there room to discuss alternatives?
- Would a developer feel constrained by this?

### Examples

**Poor (Over-specified):**

```text
FR-3: The system shall use Redis to cache user sessions
with a 30-minute TTL using JSON serialization.
```

**Better (Negotiable):**

```text
FR-3: The system shall cache user sessions to reduce
database load and maintain session state across requests.

Constraints:
- Session timeout: 30 minutes of inactivity
- Performance: < 10ms session retrieval

Implementation notes available for discussion.
```

### Balancing Negotiability

| Too Vague | Just Right | Over-specified |
| --- | --- | --- |
| "Fast login" | "Login < 2 seconds" | "Login using OAuth2 with PKCE via Azure AD B2C" |
| "Store data" | "Persist user preferences" | "Store in PostgreSQL JSON column" |

---

## Valuable

### Definition

Each requirement should deliver value to users or stakeholders, not just technical improvements.

### Why It Matters

- Ensures meaningful progress
- Justifies development effort
- Enables proper prioritization
- Connects work to business goals

### Assessment Questions

- Who benefits from this?
- What problem does this solve?
- Would a user notice if this was missing?

### Examples

**Poor (Technical-only):**

```text
FR-4: The system shall refactor the payment module
to use the strategy pattern.
```

**Better (User-valuable):**

```text
FR-4: The system shall support multiple payment methods
(credit card, PayPal, bank transfer) at checkout.

Value: Increases conversion by accommodating user preferences.
```

### Reframing Technical Requirements

| Technical Focus | User-Valuable Reframe |
| --- | --- |
| "Migrate to new database" | "Ensure data is always available during maintenance" |
| "Add logging" | "Provide detailed error information for support" |
| "Upgrade framework" | "Enable new accessibility features for users" |
| "Add caching" | "Ensure pages load within 2 seconds" |

---

## Estimable

### Definition

A requirement should have enough detail that the team can estimate the effort required to implement it.

### Why It Matters

- Enables sprint planning
- Supports capacity management
- Identifies unknowns early
- Allows realistic commitments

### Assessment Questions

- Can the team estimate this in story points or hours?
- Are there significant unknowns?
- Is the scope clear enough to bound effort?

### Examples

**Poor (Unestimable):**

```text
FR-5: The system shall integrate with external partners.
```

**Better (Estimable):**

```text
FR-5: The system shall integrate with Stripe for payment processing.

Scope:
- Implement checkout flow with Stripe Elements
- Handle successful payment webhook
- Handle failed payment webhook
- Display payment status to user

Constraints:
- Use Stripe API v2023-10-16
- Support credit/debit cards only (Phase 1)
```

### Making Requirements Estimable

| Unclear Aspect | Resolution Approach |
| --- | --- |
| Unknown technology | Spike story first |
| Vague scope | Add explicit boundaries |
| Missing acceptance criteria | Define testable conditions |
| Unbounded integration | Limit to specific endpoints |

---

## Small

### Definition

A requirement should be small enough to complete within a single iteration (sprint).

### Why It Matters

- Enables frequent delivery
- Reduces risk
- Provides early feedback
- Maintains momentum

### Assessment Questions

- Can this be done in one sprint?
- Is the estimate more than half the sprint capacity?
- Can this be demonstrated independently?

### Size Guidelines

| Size | Guidance |
| --- | --- |
| XS (1-2 hours) | Ideal for quick wins |
| S (half day) | Good size for most work |
| M (1-2 days) | Acceptable upper bound |
| L (3-5 days) | Consider splitting |
| XL (> 5 days) | Must split |

### Splitting Strategies

**By Workflow Steps:**

```text
Original: User registration
Split:
- User enters email and password
- System sends verification email
- User verifies email
- User completes profile
```

**By User Type:**

```text
Original: Dashboard for all users
Split:
- Admin dashboard
- Manager dashboard
- Regular user dashboard
```

**By CRUD Operations:**

```text
Original: Manage products
Split:
- Create product
- Read product details
- Update product
- Delete product
```

**By Data Variations:**

```text
Original: Generate reports
Split:
- Generate daily report
- Generate weekly report
- Generate monthly report
```

---

## Testable

### Definition

A requirement must have clear, measurable acceptance criteria that can verify successful implementation.

### Why It Matters

- Defines "done"
- Enables QA
- Prevents scope creep
- Provides confidence

### Assessment Questions

- How will we know this is complete?
- Can we write automated tests for this?
- Is success objectively measurable?

### Examples

**Poor (Untestable):**

```text
FR-6: The system shall provide a good user experience.
```

**Better (Testable):**

```text
FR-6: The checkout process shall be completable in 3 steps or fewer.

Acceptance Criteria:
- [ ] AC-6.1: Given a cart with items, when user initiates checkout,
      then shipping, payment, and confirmation are the only steps
- [ ] AC-6.2: Given any checkout step, when user completes the step,
      then progress indicator shows current position
- [ ] AC-6.3: Given checkout completion, when order is placed,
      then confirmation is displayed within 2 seconds
```

### Testability Patterns

| Vague Quality | Testable Version |
| --- | --- |
| "Fast" | "Responds in < 200ms (p95)" |
| "Secure" | "Passes OWASP Top 10 checks" |
| "Reliable" | "99.9% uptime over 30 days" |
| "Scalable" | "Handles 1000 concurrent users" |
| "Accessible" | "Meets WCAG 2.1 AA" |

---

## INVEST Scoring Worksheet

### Template

| Criterion | Score (0-2) | Notes |
| --- | --- | --- |
| Independent | | |
| Negotiable | | |
| Valuable | | |
| Estimable | | |
| Small | | |
| Testable | | |
| **Total** | **/12** | |

### Scoring Guide

**0 - Does Not Meet:**

- Clear violation of criterion
- Significant rework needed

**1 - Partially Meets:**

- Minor issues present
- Improvement possible but workable

**2 - Fully Meets:**

- Criterion clearly satisfied
- No improvements needed

### Action Thresholds

| Score | Action |
| --- | --- |
| 10-12 | Ready for implementation |
| 7-9 | Address minor issues, then proceed |
| 4-6 | Significant refinement needed |
| 0-3 | Return to product owner for rewrite |
