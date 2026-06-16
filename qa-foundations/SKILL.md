---
name: qa-foundations
description: Use this skill whenever the user mentions QA, bug hunting, testing, quality assurance, exploratory testing, bug reports, severity classification, or wants to find bugs in a web application. Also use when the user says "test my app", "find bugs", "explore for issues", or asks about bug severity, test methodology, or report format. This is the foundational knowledge base for all qa-hunter testing work. When in doubt about whether QA testing principles apply, they do — load this skill.
---

# QA Foundations

This skill provides the core QA knowledge base that underpins all bug hunting and quality assurance work. It covers four pillars:

1. **Oracle Layers** -- Five reliability-ranked detection methods for identifying bugs without access to source code
2. **Severity Classification** -- A structured S0-S4 scale for communicating bug impact consistently
3. **Confidence Levels** -- A framework for expressing certainty about each finding to reduce noise
4. **Testing Principles** -- The rules of engagement for black-box exploratory testing

Apply these foundations to any web application -- SaaS products, marketing sites, admin portals, mobile web apps, and any browser-based interface.

---

## Oracle Layers (Quick Reference)

Oracles are the decision rules you use to determine whether observed behavior is a bug. Each oracle has a different reliability level -- higher reliability means fewer false positives.

| Oracle | Reliability | Description | What to Look For |
|--------|------------|-------------|------------------|
| **Crash** | 100% | The application breaks in an unambiguous, undeniable way | HTTP 500 errors, uncaught JS exceptions in console, blank/white pages, infinite loading spinners, complete app crashes |
| **Convention** | ~95% | The application violates widely accepted UX and interaction patterns | Missing feedback after actions, no validation on required fields, dead links, broken navigation, missing loading states, form submission without confirmation |
| **Permission** | ~90% | The application exposes data or actions it should not | Unauthorized resource access, data leaking between roles, missing auth redirects, direct URL access to restricted pages, IDOR-like patterns |
| **Visual** | ~80% | The interface renders incorrectly or inconsistently | Broken layouts, text truncation/overflow, element overlap, images not loading, responsive breakage, z-index issues, misaligned elements |
| **Semantic** | ~60-70% | The data or workflow feels wrong but requires domain knowledge to confirm | Incorrect calculations, labels that contradict content, illogical workflow sequences, data that seems stale or wrong. Always flag for human review. |

> Full details with detection methods, examples, and false positive risks: see `references/oracle-layers.md`

---

## Severity Scale (Quick Reference)

Every bug gets a severity rating from S0 (most severe) to S4 (least severe). Severity communicates the impact on end users and business operations.

| Severity | Label | Description | Example |
|----------|-------|-------------|---------|
| **S0** | Blocker | Complete loss of critical functionality. No workaround exists. The application is unusable for its core purpose. | Login page returns 500 for all users. Payment processing crashes. Data loss on save. |
| **S1** | Critical | Major feature is broken or produces wrong results. Workaround may exist but is unacceptable for production. | Search returns no results when results exist. User profile shows another user's data. Form loses all input on validation error. |
| **S2** | Major | Important feature partially broken. Workaround exists but degrades experience significantly. | Pagination skips page 2. Export generates empty CSV. Filter applies but count badge shows wrong number. |
| **S3** | Minor | Small defect that does not block functionality. Users can complete their task without significant friction. | Typo in button label. Tooltip displays behind modal. Date picker defaults to wrong month. Success toast disappears too quickly. |
| **S4** | Trivial | Cosmetic issue or extremely minor inconsistency. No functional impact whatsoever. | 1px misalignment between elements. Slightly different shades of gray. Extra whitespace at bottom of page. Console warning (not error). |

> Full severity classification with decision factors and priority matrix: see `references/severity-scale.md`

---

## Confidence Levels (Quick Reference)

Every finding must include a confidence level that indicates how certain you are that the observed behavior is actually a bug.

| Confidence | When to Use | Required Action |
|------------|-------------|-----------------|
| **HIGH** | Observable, reproducible evidence from Crash or Convention oracles. Console errors, HTTP failures, or clearly violated interaction patterns. You can reproduce it reliably. | Report as confirmed bug. Include reproduction steps and evidence. |
| **MEDIUM** | Likely a bug based on Permission or Visual oracles, but could depend on context you lack (design intent, feature flags, A/B tests). Reproducible but ambiguous. | Report as probable bug. Note the ambiguity. Flag specific questions for the development team. |
| **LOW** | Suspicion based on Semantic oracle or edge-case behavior. May be intentional. Cannot fully reproduce or requires domain knowledge to confirm. | Report as potential issue. Explicitly recommend human review. Never present as confirmed. |

> Full confidence framework with oracle mapping and priority matrix: see `references/severity-scale.md`

---

## Testing Principles

These five principles govern all QA Hunter testing work. They are non-negotiable.

### 1. Black-Box Only
You test the application as an end user would. You have no access to source code, databases, or internal documentation unless explicitly provided. Your observations come from what the browser shows you: the rendered page, the browser console, and network requests.

### 2. Report Only — Never Fix
Your job is to find and document bugs, not to fix them. Never modify application code, suggest code patches, or attempt to correct issues directly. Produce a structured report and hand it to the development team.

### 3. Evidence-Based
Every bug report must include concrete evidence from at least one of these sources:
- **Console**: JavaScript errors, warnings, or uncaught exceptions visible in the browser dev tools
- **Network**: Failed HTTP requests (4xx/5xx), abnormally slow responses, or unexpected response payloads
- **Visual**: Observable rendering problems, layout breakage, or interaction failures

A "feeling" is not evidence. If you cannot point to specific, observable evidence, downgrade your confidence to LOW and flag for human review.

### 4. Scope-Guided
Test only what you are asked to test. If given specific flows, test those flows. If given a broad scope ("test the whole app"), prioritize high-traffic user journeys first: authentication, core CRUD operations, navigation, and search. Document what you tested and what you did not test.

### 5. Reproduce Before Reporting
Attempt to reproduce every issue at least once before including it in a report. If an issue occurs once but cannot be reproduced, note it as "intermittent" with LOW confidence. Flaky findings erode trust in the entire report.

---

## Reference Files

For detailed, audit-ready content on each pillar, consult:

| File | Contents |
|------|----------|
| `references/oracle-layers.md` | Full oracle layer documentation with detection methods, examples, and false positive analysis for each of the five oracles |
| `references/severity-scale.md` | Complete severity and confidence classification with decision factors, priority matrix, and scoring guidance |
| `references/report-template.md` | Structured bug report template with field definitions and formatting standards |
