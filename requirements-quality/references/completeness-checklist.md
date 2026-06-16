# Completeness Checklist Reference

Comprehensive validation checklists for requirements and specifications.

## Overview

Completeness validation ensures that requirements and specifications contain all necessary information for successful implementation. This reference provides checklists at multiple levels: individual requirements, feature specifications, and full project specifications.

---

## Individual Requirement Checklist

### Required Elements

| Element | Description | Check |
| --- | --- | --- |
| **ID** | Unique identifier (FR-xxx, NFR-xxx) | [ ] |
| **Title** | Brief, descriptive title | [ ] |
| **Type** | Functional or Non-Functional | [ ] |
| **Description** | Full requirement text (EARS format preferred) | [ ] |
| **Priority** | MoSCoW level (Must/Should/Could/Won't) | [ ] |
| **Acceptance Criteria** | At least 2 testable conditions | [ ] |

### Optional Elements (Include if Applicable)

| Element | When Required | Check |
| --- | --- | --- |
| **Dependencies** | If depends on other requirements | [ ] |
| **Assumptions** | If requirement assumes context | [ ] |
| **Constraints** | If technical/business limits exist | [ ] |
| **Business Rules** | If logic rules apply | [ ] |
| **Data Requirements** | If specific data structures needed | [ ] |
| **Security Considerations** | If sensitive data/operations | [ ] |
| **Performance Criteria** | If timing/load requirements | [ ] |

### Quality Validation

| Criterion | Question | Check |
| --- | --- | --- |
| **Clarity** | Is the requirement unambiguous? | [ ] |
| **Completeness** | Is all necessary information present? | [ ] |
| **Consistency** | Does it align with other requirements? | [ ] |
| **Testability** | Can we verify implementation? | [ ] |
| **Feasibility** | Is it technically achievable? | [ ] |
| **Traceability** | Is it linked to business need? | [ ] |

---

## Feature Specification Checklist

### Context Section

| Element | Description | Check |
| --- | --- | --- |
| **Problem Statement** | Clear articulation of the problem | [ ] |
| **Motivation** | Why this is important/valuable | [ ] |
| **Scope** | What's in and out of scope | [ ] |
| **Stakeholders** | Who is affected | [ ] |
| **Success Metrics** | How we measure success | [ ] |

### Functional Requirements Section

| Element | Description | Check |
| --- | --- | --- |
| **All Identified** | No missing functionality | [ ] |
| **Unique IDs** | Each has unique identifier | [ ] |
| **EARS Format** | Using EARS patterns | [ ] |
| **Prioritized** | MoSCoW assigned | [ ] |
| **Acceptance Criteria** | Each has testable conditions | [ ] |
| **Dependencies Mapped** | Relationships documented | [ ] |

### Non-Functional Requirements Section

| Category | Question | Check |
| --- | --- | --- |
| **Performance** | Are timing/throughput requirements defined? | [ ] |
| **Scalability** | Are growth expectations documented? | [ ] |
| **Availability** | Are uptime requirements specified? | [ ] |
| **Security** | Are security requirements included? | [ ] |
| **Accessibility** | Are accessibility standards specified? | [ ] |
| **Usability** | Are usability criteria defined? | [ ] |
| **Maintainability** | Are maintenance needs considered? | [ ] |
| **Compatibility** | Are integration points defined? | [ ] |

### Edge Cases and Error Handling

| Scenario Type | Question | Check |
| --- | --- | --- |
| **Empty States** | What happens with no data? | [ ] |
| **Boundary Values** | Min/max limits defined? | [ ] |
| **Invalid Input** | Error handling specified? | [ ] |
| **Timeout Scenarios** | Timeout behavior defined? | [ ] |
| **Concurrent Access** | Race conditions addressed? | [ ] |
| **Permission Denied** | Authorization failures handled? | [ ] |
| **System Failures** | Graceful degradation defined? | [ ] |

---

## Project Specification Checklist

### Vision and Scope

| Element | Check |
| --- | --- |
| Vision statement | [ ] |
| Business objectives | [ ] |
| Target users/personas | [ ] |
| Success criteria | [ ] |
| Project constraints | [ ] |
| Assumptions | [ ] |
| Dependencies on external systems | [ ] |

### Requirements Coverage

| Area | Check |
| --- | --- |
| All user stories addressed | [ ] |
| All use cases covered | [ ] |
| All business rules captured | [ ] |
| All interfaces defined | [ ] |
| All data entities identified | [ ] |
| All workflows documented | [ ] |
| All reports/outputs specified | [ ] |

### Technical Requirements

| Category | Check |
| --- | --- |
| Architecture constraints | [ ] |
| Technology stack requirements | [ ] |
| Integration requirements | [ ] |
| Data migration requirements | [ ] |
| Environment requirements | [ ] |
| Deployment requirements | [ ] |
| Monitoring requirements | [ ] |

### Quality Attributes

| Attribute | Defined? | Measurable? |
| --- | --- | --- |
| Performance | [ ] | [ ] |
| Security | [ ] | [ ] |
| Availability | [ ] | [ ] |
| Scalability | [ ] | [ ] |
| Maintainability | [ ] | [ ] |
| Accessibility | [ ] | [ ] |
| Usability | [ ] | [ ] |
| Compatibility | [ ] | [ ] |

### Compliance and Standards

| Area | Check |
| --- | --- |
| Regulatory requirements | [ ] |
| Industry standards | [ ] |
| Internal policies | [ ] |
| Accessibility standards (WCAG) | [ ] |
| Security standards (OWASP) | [ ] |
| Data protection (GDPR/CCPA) | [ ] |

---

## Acceptance Criteria Completeness

### Individual AC Checklist

| Element | Check |
| --- | --- |
| Uses Given/When/Then format | [ ] |
| Given establishes preconditions | [ ] |
| When describes single action | [ ] |
| Then specifies observable outcome | [ ] |
| Is independently testable | [ ] |
| Has clear pass/fail | [ ] |

### Coverage Checklist

| Scenario Type | Check |
| --- | --- |
| Happy path covered | [ ] |
| Alternative paths covered | [ ] |
| Error conditions covered | [ ] |
| Edge cases covered | [ ] |
| Boundary conditions covered | [ ] |
| Security scenarios covered | [ ] |

### Quality Checklist

| Criterion | Check |
| --- | --- |
| No duplicate scenarios | [ ] |
| No contradictory criteria | [ ] |
| Sufficient but not excessive | [ ] |
| Automatable | [ ] |
| Independent of other ACs | [ ] |

---

## Specification Review Checklist

### Before Review

| Preparation | Check |
| --- | --- |
| Spell check completed | [ ] |
| Consistent terminology | [ ] |
| All acronyms defined | [ ] |
| Cross-references valid | [ ] |
| Diagrams legible | [ ] |
| Version/date current | [ ] |

### During Review

| Verification | Check |
| --- | --- |
| All sections present | [ ] |
| No TBD/TBC items remaining | [ ] |
| All questions resolved | [ ] |
| Stakeholder sign-off obtained | [ ] |
| Technical feasibility confirmed | [ ] |
| Estimates provided | [ ] |

### After Review

| Finalization | Check |
| --- | --- |
| Review comments addressed | [ ] |
| Changes tracked | [ ] |
| Baseline established | [ ] |
| Distribution list notified | [ ] |
| Linked to project management tool | [ ] |

---

## Common Gaps by Domain

### Web Applications

| Often Missing | Check |
| --- | --- |
| Browser compatibility matrix | [ ] |
| Mobile/responsive requirements | [ ] |
| Offline behavior | [ ] |
| Session management | [ ] |
| Cookie/tracking consent | [ ] |
| SEO requirements | [ ] |

### APIs

| Often Missing | Check |
| --- | --- |
| Rate limiting | [ ] |
| Pagination | [ ] |
| Versioning strategy | [ ] |
| Authentication/authorization | [ ] |
| Error response format | [ ] |
| Retry behavior | [ ] |

### Data-Intensive Systems

| Often Missing | Check |
| --- | --- |
| Data retention policies | [ ] |
| Archival requirements | [ ] |
| Data quality rules | [ ] |
| Audit trail requirements | [ ] |
| Backup/recovery | [ ] |
| Data sovereignty | [ ] |

### Enterprise Applications

| Often Missing | Check |
| --- | --- |
| Multi-tenancy | [ ] |
| Role-based access | [ ] |
| Audit logging | [ ] |
| Integration patterns | [ ] |
| Migration from legacy | [ ] |
| Training requirements | [ ] |

---

## Completeness Score

### Scoring Guide

Calculate completeness percentage:

```text
Score = (Checked Items / Total Items) × 100
```

### Thresholds

| Score | Status | Action |
| --- | --- | --- |
| 95-100% | Ready | Proceed to implementation |
| 85-94% | Nearly Ready | Address gaps, then proceed |
| 70-84% | Needs Work | Significant refinement needed |
| < 70% | Incomplete | Return for major rework |

### Critical Gaps (Automatic Block)

These gaps block progress regardless of overall score:

- [ ] Missing acceptance criteria
- [ ] Undefined priority
- [ ] No security consideration for sensitive features
- [ ] Missing performance requirements for user-facing features
- [ ] Unresolved dependencies
- [ ] Conflicting requirements
