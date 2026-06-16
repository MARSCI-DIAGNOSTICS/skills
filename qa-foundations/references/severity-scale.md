# Severity & Confidence Classification — Complete Reference

> Every bug found during QA testing must be classified along two dimensions: **Severity** (how bad is the impact?) and **Confidence** (how sure are you it is a real bug?). Together, these produce a priority score that helps development teams triage effectively.

---

## Severity Scale

Severity measures the impact of a bug on end users and business operations. It is determined by what the bug does, not by how it was found.

### Severity Table

| Severity | Label | Description | Example | Required Action |
|----------|-------|-------------|---------|-----------------|
| **S0** | Blocker | Complete loss of critical functionality. The application is unusable for its core purpose. No workaround exists. Data loss or security breach may be involved. | Login returns 500 for all users. Payment processing crashes mid-transaction. Saved data is silently lost. Complete auth bypass allowing unauthenticated access. | Immediate fix required. This is a production emergency. All other work stops until resolved. |
| **S1** | Critical | A major feature is broken or produces incorrect results. A workaround may exist but is unacceptable for production use. Users are significantly blocked. | Search returns empty results when items exist. User profile displays another user's data. Form loses all input on validation error. File upload silently fails. | Fix within 24 hours. Feature is not shippable in this state. |
| **S2** | Major | An important feature is partially broken. Users can complete their task but with significant friction, incorrect information, or degraded experience. | Pagination skips page 2 (jumping from 1 to 3). Export generates a CSV with missing columns. Filter applies correctly but the count badge shows the wrong number. Table sort works but loses current page position. | Fix within the current sprint. The feature works but is unreliable or misleading. |
| **S3** | Minor | A small defect that does not block functionality. Users can complete their task without significant friction. The bug is noticeable but not disruptive. | Typo in a button label ("Cancle" instead of "Cancel"). Tooltip text is cut off. Date picker defaults to January 2020 instead of current month. Success toast disappears after 1 second (too fast to read). Hover state missing on secondary buttons. | Fix when convenient. Add to backlog and address in a future sprint. |
| **S4** | Trivial | A cosmetic issue or extremely minor inconsistency. No functional impact. Most users would never notice. | 1px misalignment between two buttons. Slightly different shades of gray (#666 vs #6A6A6A) on same-level elements. Extra whitespace at the bottom of a long page. Console warning (not error) about a deprecated API usage. Favicon missing on one page. | Fix if time permits. Lowest priority in the backlog. |

---

## Three Factors That Determine Severity

When deciding between adjacent severity levels (e.g., S1 vs S2, S2 vs S3), evaluate these three factors:

### 1. Frequency

How many users does this affect?

| Frequency | Description | Severity Impact |
|-----------|-------------|-----------------|
| **All users** | Every user encounters this bug in normal usage | Increase severity by one level |
| **Most users** | The bug affects a common workflow or popular feature | Keep severity as assessed |
| **Some users** | The bug affects a specific role, browser, or use case | Keep severity as assessed |
| **Edge case** | The bug requires unusual input or rare conditions to trigger | Decrease severity by one level |

### 2. Impact

How hard is it for the user to overcome?

| Impact | Description | Severity Impact |
|--------|-------------|-----------------|
| **Blocking** | User cannot complete their task at all | S0 or S1 |
| **Major friction** | User can complete the task but with significant difficulty, confusion, or lost work | S1 or S2 |
| **Minor friction** | User notices the issue but completes the task with minimal extra effort | S2 or S3 |
| **Cosmetic only** | User may not even notice; no workflow impact | S3 or S4 |

### 3. Persistence

Does the bug occur once or repeatedly?

| Persistence | Description | Severity Impact |
|-------------|-------------|-----------------|
| **Persistent** | The bug occurs every time the action is performed | Keep severity as assessed |
| **Frequent** | The bug occurs most of the time (>50% of attempts) | Keep severity as assessed |
| **Intermittent** | The bug occurs sometimes but not always | Decrease severity by one level, add note about intermittent nature |
| **One-time** | The bug occurred once and could not be reproduced | Report with LOW confidence regardless of severity |

### Decision Examples

| Scenario | Frequency | Impact | Persistence | Final Severity |
|----------|-----------|--------|-------------|----------------|
| Login 500 error for all users | All users | Blocking | Persistent | **S0** — every user is blocked permanently |
| Search returns wrong results for queries with special characters | Some users | Major friction | Persistent | **S2** — limited audience but reliably broken |
| Modal sometimes fails to close on first click | Most users | Minor friction | Intermittent | **S3** — noticeable but non-blocking, inconsistent |
| Header logo is 2px lower on Safari than Chrome | Edge case | Cosmetic only | Persistent | **S4** — trivial, browser-specific rendering |

---

## Confidence Levels

Confidence measures how certain you are that the observed behavior is actually a bug, not an intentional design decision, test environment artifact, or misunderstanding of the application.

### Confidence Table

| Confidence | When to Use | Oracle Types | Required Action |
|------------|-------------|--------------|-----------------|
| **HIGH** | You have clear, reproducible evidence. Console errors, HTTP failures, or unambiguous convention violations. You can reproduce the issue reliably on demand. The evidence speaks for itself. | Crash (always HIGH), Convention (usually HIGH) | Report as confirmed bug. Include full reproduction steps and evidence. No hedging language needed. |
| **MEDIUM** | The issue is likely a bug but depends on context you may not have. It could be affected by design intent, feature flags, A/B tests, or environment-specific conditions. You can reproduce it but the interpretation is ambiguous. | Permission (usually MEDIUM), Visual (usually MEDIUM), Convention (sometimes MEDIUM) | Report as probable bug. Note the ambiguity explicitly. Include a question for the team about intent. Example: "This appears to be a bug, but could be intentional if [scenario]." |
| **LOW** | You suspect something is wrong but cannot fully confirm it. The issue may require domain knowledge, business context, or access to specifications. You may not be able to reproduce it reliably, or the behavior could be intentional. | Semantic (always LOW unless domain knowledge confirms), any oracle for intermittent issues | Report as potential issue. Use hedging language: "This may be a bug." Recommend human review. Never present LOW confidence findings as confirmed bugs. |

### Oracle-to-Confidence Mapping

| Oracle | Default Confidence | Upgrade Condition | Downgrade Condition |
|--------|--------------------|-------------------|---------------------|
| Crash | HIGH | — (already max) | Never downgrade crash findings |
| Convention | HIGH | — | Downgrade to MEDIUM if the convention violation could be an intentional design choice |
| Permission | MEDIUM | Upgrade to HIGH if you have explicit documentation of the expected permission model | Downgrade to LOW if you are unsure about the intended role structure |
| Visual | MEDIUM | Upgrade to HIGH if the visual issue blocks functionality (e.g., modal behind overlay) | Downgrade to LOW if the issue could be a design choice (e.g., intentional truncation) |
| Semantic | LOW | Upgrade to MEDIUM if you have domain documentation or the math is objectively wrong | — (already min for uncertain findings) |

---

## Severity x Confidence Priority Matrix

Combine severity and confidence to produce a priority score (P0-P4) that determines triage order.

|  | **HIGH Confidence** | **MEDIUM Confidence** | **LOW Confidence** |
|--|--------------------|-----------------------|--------------------|
| **S0 — Blocker** | **P0** — Drop everything | **P1** — Verify and fix urgently | **P2** — Verify immediately |
| **S1 — Critical** | **P1** — Fix urgently | **P1** — Verify and fix soon | **P2** — Verify soon |
| **S2 — Major** | **P2** — Fix this sprint | **P2** — Verify and schedule | **P3** — Review when possible |
| **S3 — Minor** | **P3** — Add to backlog | **P3** — Add to backlog | **P4** — Note for future |
| **S4 — Trivial** | **P4** — Fix if time permits | **P4** — Note for future | **P4** — Note for future |

### Priority Definitions

| Priority | Label | Response Time | Description |
|----------|-------|---------------|-------------|
| **P0** | Emergency | Immediate | Production is broken. All hands on deck. Fix and deploy now. |
| **P1** | Urgent | Within 24 hours | Major functionality is compromised. Must be resolved before next release. |
| **P2** | High | Within current sprint | Significant issue that needs attention but is not an emergency. Schedule for this sprint. |
| **P3** | Medium | Next sprint | Real issue but low urgency. Add to backlog and address in the next planning cycle. |
| **P4** | Low | When convenient | Nice to fix but no urgency. Address during cleanup or polish phases. |

---

## Classification Checklist

When classifying a bug, follow this sequence:

1. **Identify the oracle**: Which oracle detected this issue? (Crash, Convention, Permission, Visual, Semantic)
2. **Assign confidence**: Based on the oracle type and your evidence quality, assign HIGH, MEDIUM, or LOW.
3. **Assess severity**: Evaluate the three factors (Frequency, Impact, Persistence) to determine S0-S4.
4. **Calculate priority**: Cross-reference severity and confidence in the priority matrix to get P0-P4.
5. **Document everything**: Include the oracle, severity, confidence, priority, evidence, and reproduction steps in the bug report.

Never skip confidence. A report full of HIGH severity bugs at LOW confidence is less useful than a report of MEDIUM severity bugs at HIGH confidence. Accurate confidence calibration builds trust in the QA process.
