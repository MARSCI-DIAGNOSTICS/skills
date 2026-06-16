# Refinement Patterns Reference

Techniques for improving requirement quality through iterative refinement.

## Overview

Requirement refinement is the process of improving requirements from initial drafts to implementation-ready specifications. This reference provides patterns and techniques for common refinement scenarios.

## Refinement Workflow

### Standard Process

```text
┌─────────────────────────────────────────────────────────────┐
│                    REFINEMENT CYCLE                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   1. Initial Draft                                           │
│        ↓                                                     │
│   2. INVEST Assessment ──────→ Score < 7? ──→ Apply Fixes   │
│        ↓                              ↑           │          │
│   3. Acceptance Criteria              └───────────┘          │
│        ↓                                                     │
│   4. Stakeholder Review                                      │
│        ↓                                                     │
│   5. Final Validation                                        │
│        ↓                                                     │
│   6. Ready for Implementation                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Iteration Limits

| Phase | Max Iterations | Escalation |
| --- | --- | --- |
| Draft refinement | 3 | Involve product owner |
| Technical clarification | 2 | Involve architect |
| Stakeholder alignment | 2 | Executive sponsor |

---

## Clarity Refinement Patterns

### Pattern: Remove Ambiguity

**When to Use:** Requirement contains vague or subjective terms.

**Before:**

```text
The system should quickly display relevant search results.
```

**Apply Pattern:**

1. Identify ambiguous terms: "quickly", "relevant"
2. Define measurable criteria
3. Specify context and constraints

**After:**

```text
WHEN the user submits a search query,
the system SHALL display the first 10 results within 500ms.

Results are relevant when they contain:
- All query terms (AND logic)
- OR phrase matches in title (higher ranking)
```

### Pattern: Explicit Actors

**When to Use:** Unclear who performs actions or is affected.

**Before:**

```text
The report shall be generated monthly.
```

**Apply Pattern:**

1. Identify who triggers the action
2. Identify who receives the output
3. Add actor context

**After:**

```text
WHEN the scheduler triggers at midnight on the first of each month,
the system SHALL generate the monthly sales report
AND send it to all users with the "Manager" role.
```

### Pattern: Boundary Definition

**When to Use:** Scope is unbounded or unclear.

**Before:**

```text
The system shall support multiple file formats.
```

**Apply Pattern:**

1. Enumerate supported items
2. Explicitly state exclusions
3. Add version constraints

**After:**

```text
The system SHALL support the following file formats:
- PDF (version 1.7 and earlier)
- DOCX (Office 2007 and later)
- TXT (UTF-8 encoding)

The system SHALL NOT support:
- Password-protected files (deferred to Phase 2)
- Files larger than 50MB
```

---

## Splitting Patterns

### Pattern: Split by User Type

**When to Use:** Requirement serves multiple user types with different needs.

**Before:**

```text
FR-10: The system shall display a dashboard with key metrics.
Estimate: XL (too large)
```

**Apply Pattern:**

1. Identify distinct user types
2. Extract type-specific needs
3. Create focused requirements

**After:**

```text
FR-10a: The system shall display an executive dashboard
        showing revenue, costs, and margin trends.
        Estimate: M

FR-10b: The system shall display an operations dashboard
        showing order volume, fulfillment rate, and inventory.
        Estimate: M

FR-10c: The system shall display a customer service dashboard
        showing ticket volume, resolution time, and satisfaction.
        Estimate: M
```

### Pattern: Split by Workflow Step

**When to Use:** Requirement describes an end-to-end process.

**Before:**

```text
FR-15: The system shall enable users to complete purchases.
Estimate: XL (too large)
```

**Apply Pattern:**

1. Map the complete workflow
2. Identify natural breakpoints
3. Create step-focused requirements

**After:**

```text
FR-15a: The system shall display a shopping cart summary.
        Estimate: S

FR-15b: The system shall collect shipping information.
        Estimate: S

FR-15c: The system shall process payment via Stripe.
        Estimate: M

FR-15d: The system shall display order confirmation.
        Estimate: S
```

### Pattern: Split by Data Variation

**When to Use:** Requirement handles multiple data types or formats.

**Before:**

```text
FR-20: The system shall import data from external sources.
Estimate: XL (too large)
```

**Apply Pattern:**

1. List data variations
2. Assess complexity per variation
3. Create variation-focused requirements

**After:**

```text
FR-20a: The system shall import customer data from CSV files.
        Estimate: M

FR-20b: The system shall import order data via REST API.
        Estimate: M

FR-20c: The system shall import inventory data via SFTP.
        Estimate: L
```

### Pattern: Split by Happy Path / Error Handling

**When to Use:** Requirement mixes success and failure scenarios.

**Before:**

```text
FR-25: The system shall process credit card payments.
Estimate: XL (too large)
```

**Apply Pattern:**

1. Separate success scenarios
2. Enumerate error conditions
3. Create focused requirements

**After:**

```text
FR-25a: The system shall process successful credit card payments.
        - Authorize and capture in single transaction
        - Display confirmation with transaction ID
        Estimate: M

FR-25b: The system shall handle declined payments.
        - Display user-friendly error message
        - Allow retry with different card
        Estimate: S

FR-25c: The system shall handle payment gateway timeouts.
        - Retry once after 5 seconds
        - Display timeout message if retry fails
        Estimate: S
```

---

## Value Refinement Patterns

### Pattern: Connect to Business Goal

**When to Use:** Requirement lacks clear business justification.

**Before:**

```text
FR-30: The system shall implement caching for API responses.
```

**Apply Pattern:**

1. Identify the user benefit
2. Connect to business metric
3. Reframe around value

**After:**

```text
FR-30: The system SHALL return API responses within 100ms
       to ensure responsive user experience.

Business Value:
- Reduces user wait time by 80%
- Supports 10x increase in concurrent users
- Reduces infrastructure costs by 40%

Implementation Note: Caching recommended but not mandated.
```

### Pattern: User Story Wrapper

**When to Use:** Technical requirement needs user context.

**Before:**

```text
FR-35: The system shall compress images on upload.
```

**Apply Pattern:**

1. Identify the end user
2. Define the desired outcome
3. Wrap in user story format

**After:**

```text
FR-35: As a content creator,
       I want uploaded images to load quickly,
       so that my audience has a smooth viewing experience.

The system SHALL compress uploaded images to:
- Maximum 500KB for display images
- Maximum 100KB for thumbnails
- Maintain minimum 80% quality score
```

---

## Testability Refinement Patterns

### Pattern: Add Acceptance Criteria

**When to Use:** Requirement lacks testable conditions.

**Before:**

```text
FR-40: The system shall validate user input.
```

**Apply Pattern:**

1. Identify validation scenarios
2. Define pass/fail conditions
3. Add Given/When/Then criteria

**After:**

```text
FR-40: The system SHALL validate user input before submission.

Acceptance Criteria:

AC-40.1: Given an empty required field,
         When the user attempts to submit,
         Then the field is highlighted with error message.

AC-40.2: Given an invalid email format,
         When the user leaves the field,
         Then validation error appears immediately.

AC-40.3: Given all fields are valid,
         When the user submits,
         Then form processes without validation errors.
```

### Pattern: Quantify Quality Attributes

**When to Use:** Requirement uses subjective quality terms.

**Before:**

```text
NFR-5: The system shall be highly available.
```

**Apply Pattern:**

1. Define the quality attribute precisely
2. Set measurable thresholds
3. Specify measurement method

**After:**

```text
NFR-5: The system SHALL maintain 99.9% uptime monthly.

Measurement:
- Uptime = (Total minutes - Downtime minutes) / Total minutes
- Downtime includes: unplanned outages, degraded performance (>5s response)
- Excludes: scheduled maintenance (max 4 hours/month, announced 48h ahead)

Acceptance Criteria:
AC-NFR5.1: Given the production system,
           When monitored over 30 days,
           Then uptime percentage >= 99.9%.
```

---

## Dependency Resolution Patterns

### Pattern: Extract Shared Dependency

**When to Use:** Multiple requirements depend on common infrastructure.

**Before:**

```text
FR-50: User registration (depends on email service)
FR-51: Password reset (depends on email service)
FR-52: Order confirmation (depends on email service)
```

**Apply Pattern:**

1. Identify common dependency
2. Extract as separate requirement
3. Document relationships

**After:**

```text
FR-49: The system SHALL provide email sending capability.
       - Support HTML and plain text
       - Handle retry on temporary failure
       - Log all sent emails

FR-50: User registration (uses FR-49)
FR-51: Password reset (uses FR-49)
FR-52: Order confirmation (uses FR-49)

Note: FR-49 becomes a sprint 0 / infrastructure story.
```

### Pattern: Define Interface Contract

**When to Use:** Requirement depends on another team's work.

**Before:**

```text
FR-55: The system shall display inventory from warehouse system.
```

**Apply Pattern:**

1. Define the interface contract
2. Create mock/stub capability
3. Decouple from external dependency

**After:**

```text
FR-55: The system SHALL display inventory levels.

Interface Contract (agreed with Warehouse team):
- Endpoint: GET /api/v1/inventory/{sku}
- Response: { "sku": string, "quantity": number, "updated": ISO8601 }
- SLA: 200ms p95, 99.5% availability

Development Approach:
- Implement against interface contract
- Use mock service until integration ready
- Integration testing in staging environment
```

---

## Refinement Session Template

### Agenda (60 minutes)

| Time | Activity |
| --- | --- |
| 0-5 min | Review requirements for session |
| 5-15 min | INVEST assessment (score each) |
| 15-40 min | Apply refinement patterns |
| 40-50 min | Add/refine acceptance criteria |
| 50-60 min | Confirm ready for sprint |

### Participants

| Role | Responsibility |
| --- | --- |
| Product Owner | Value clarification, prioritization |
| Tech Lead | Technical feasibility, estimation |
| QA Lead | Testability, acceptance criteria |
| Developers | Estimation, dependency identification |

### Exit Criteria

- [ ] All requirements score 7+ on INVEST
- [ ] Each requirement has 2-5 acceptance criteria
- [ ] Dependencies documented
- [ ] Estimates provided
- [ ] Ready for sprint planning
