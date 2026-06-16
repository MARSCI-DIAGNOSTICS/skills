# QA Bug Report Template — Format Reference

> This document defines the structured format for all QA Hunter bug reports. Every report must follow this template to ensure consistency, completeness, and actionability. Copy the structure below and fill in the fields for each testing session.

---

## Template

```markdown
# QA Bug Report

## Application: [app name/URL]
## Scope: [what was tested — specific flows, pages, or "full exploratory"]
## Date: [YYYY-MM-DD]
## Tester: QA Hunter (Claude Code plugin)

---

### Summary

- **Bugs found:** [total count]
- **By severity:** S0: [n] | S1: [n] | S2: [n] | S3: [n] | S4: [n]
- **By confidence:** HIGH: [n] | MEDIUM: [n] | LOW: [n]
- **Flows tested:** [comma-separated list of flows/features tested]
- **Credentials used:** [role names only — e.g., "admin, regular user". Never include actual passwords or tokens]

---

### Bugs

#### [BUG-001] [Short descriptive title] — S[X] / [CONFIDENCE]

| Field | Value |
|-------|-------|
| Severity | S[X] — [Blocker/Critical/Major/Minor/Trivial] |
| Confidence | [HIGH/MEDIUM/LOW] |
| Oracle | [Crash/Convention/Permission/Visual/Semantic] |
| URL | [full page URL where the bug occurs] |
| Role | [user role used during testing — e.g., "admin", "regular user", "logged out"] |

**Steps to Reproduce:**
1. [Navigate to specific URL or page]
2. [Perform specific action — be precise about what to click, type, or select]
3. [Describe the trigger — the final action that causes the bug to manifest]

**Expected:** [What should happen according to convention, logic, or explicit requirements]

**Actual:** [What actually happens — describe the observable behavior precisely]

**Evidence:**
- Console: [exact error message, or "No console errors"]
- Network: [failed request details — method, URL, status code — or "No network errors"]
- Visual: [description of what is visually wrong, or "No visual anomalies"]

---

#### [BUG-002] [Short descriptive title] — S[X] / [CONFIDENCE]

(repeat the same structure for each bug)

---

### Tested Flows

| # | Flow | Status | Bugs Found |
|---|------|--------|------------|
| 1 | [flow name — e.g., "User login"] | [PASS/FAIL] | [BUG-001, BUG-003 or "—"] |
| 2 | [flow name — e.g., "Create new project"] | [PASS/FAIL] | [BUG-002 or "—"] |
| 3 | [flow name — e.g., "Search and filter"] | [PASS] | — |

### Not Tested

- [Areas explicitly out of scope — e.g., "Admin panel (no admin credentials provided)"]
- [Features not reachable — e.g., "Payment flow (requires live Stripe keys)"]
- [Technical limitations — e.g., "Email verification (cannot receive emails in testing)"]
```

---

## Field Definitions

### Header Fields

| Field | Description | Rules |
|-------|-------------|-------|
| **Application** | The name or URL of the application being tested | Use the root URL or application name. Be specific enough that the report can be matched to the right project. |
| **Scope** | What was tested in this session | List specific flows if assigned, or "full exploratory" if given free rein. This sets expectations for what the report covers. |
| **Date** | When the testing was performed | Use ISO 8601 format: YYYY-MM-DD. |
| **Tester** | Who performed the testing | Always "QA Hunter (Claude Code plugin)" for automated reports. |

### Summary Fields

| Field | Description | Rules |
|-------|-------------|-------|
| **Bugs found** | Total count of unique bugs | Count each distinct issue once, even if it manifests on multiple pages. |
| **By severity** | Breakdown by S0-S4 | Must sum to total bugs found. |
| **By confidence** | Breakdown by HIGH/MEDIUM/LOW | Must sum to total bugs found. |
| **Flows tested** | List of user flows or features tested | Match the "Tested Flows" table entries. |
| **Credentials used** | Role names used during testing | Never include actual usernames, passwords, tokens, or API keys. Only role labels. |

### Bug Fields

| Field | Description | Rules |
|-------|-------------|-------|
| **Bug ID** | Sequential identifier | Format: BUG-001, BUG-002, etc. Number sequentially in order of discovery. |
| **Title** | Short descriptive summary | Under 80 characters. Include the what and where: "Login form accepts empty password", "Dashboard chart shows wrong date range". |
| **Severity** | S0-S4 with label | Include both the code and the label. Justify based on frequency, impact, and persistence (see severity-scale.md). |
| **Confidence** | HIGH/MEDIUM/LOW | Based on the oracle type and evidence quality. See confidence framework in severity-scale.md. |
| **Oracle** | Which oracle detected the issue | One of: Crash, Convention, Permission, Visual, Semantic. See oracle-layers.md for definitions. |
| **URL** | Page URL where the bug occurs | Full URL including path. If the bug occurs on multiple pages, list the primary one and note others in the description. |
| **Role** | User role used when the bug was found | Must match one of the roles listed in "Credentials used". |
| **Steps to Reproduce** | Ordered list of actions to trigger the bug | Start from a known state (e.g., "Navigate to /dashboard"). Each step should be a single action. A developer should be able to follow these steps exactly and see the same bug. |
| **Expected** | What should happen | Based on convention, explicit requirements, or common sense. Be specific: "A success toast should appear and the user should be redirected to /dashboard" not "It should work". |
| **Actual** | What actually happens | Describe the observable behavior. Be precise and factual: "The page remains on /login with no error message displayed" not "It doesn't work". |
| **Evidence — Console** | Console errors or messages | Copy the exact error text. If no console errors, write "No console errors". |
| **Evidence — Network** | Network request failures | Include method, URL path, and status code: "POST /api/login → 500 Internal Server Error". If no failures, write "No network errors". |
| **Evidence — Visual** | Visual observation | Describe what you see: "The button text reads 'Cancle' instead of 'Cancel'". If no visual issues, write "No visual anomalies". |

### Tested Flows Table

| Column | Description | Rules |
|--------|-------------|-------|
| **#** | Sequential number | Number flows in order tested. |
| **Flow** | Name of the user flow | Use clear, verb-based names: "User login", "Create project", "Search and filter results". |
| **Status** | PASS or FAIL | FAIL if any bug was found in this flow. PASS if the flow completed without issues. |
| **Bugs Found** | Bug IDs linked to this flow | Comma-separated BUG-xxx references, or "—" if PASS. |

### Not Tested Section

List everything that was not covered, organized by reason:

- **Out of scope**: Features the tester was told not to test
- **Not reachable**: Features that require credentials, keys, or infrastructure not available during testing
- **Technical limitations**: Features that cannot be tested in the current environment (email, SMS, payment processing)

This section is critical for setting expectations. A report that does not list what was not tested implies everything was tested, which is almost never true.

---

## Writing Guidelines

1. **Be precise, not verbose.** "The submit button does not respond to clicks" is better than "When I tried to click the submit button on the form, it seemed like nothing happened and I could not determine whether my action had any effect."

2. **Use neutral language.** Report what you observe, not what you feel. "The modal appears behind the overlay" not "The modal UX is terrible."

3. **One bug per entry.** If a single page has three issues, create three bug entries. Do not combine unrelated issues.

4. **Order bugs by severity.** List S0 bugs first, then S1, S2, S3, S4. Within the same severity, order by confidence (HIGH first).

5. **Include negative evidence.** If the console shows no errors for a visual bug, write "Console: No console errors." This confirms you checked, rather than leaving it ambiguous.

6. **Never include secrets.** No passwords, API keys, tokens, session IDs, or other credentials in the report. Use role labels ("admin", "user") and redact any sensitive data visible in evidence.
