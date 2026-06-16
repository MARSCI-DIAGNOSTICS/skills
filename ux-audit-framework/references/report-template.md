# UX Audit Report Template

Use this template as the starting structure for every UX audit report. Fill in each section with findings from the audit. Delete any instructional text (in italics or brackets) before delivering the final report.

---

## 1. Executive Summary

**Product**: [Product name and URL]
**Audit Date**: [Date]
**Auditor**: [Name/team]
**Scope**: [Which flows, pages, or features were audited]

### Overall UX Health Score

| Metric | Value |
|--------|-------|
| **UX Health Score** | **[XX] / 50 ([XX]%)** |
| **Critical Issues (Severity 4)** | [count] |
| **Major Issues (Severity 3)** | [count] |
| **Minor Issues (Severity 2)** | [count] |
| **Cosmetic Issues (Severity 0-1)** | [count] |
| **Total Issues Found** | [count] |

### Top 3 Findings

1. **[Finding title]** — [One-sentence summary]. Severity: [0-4]. Location: [where].
2. **[Finding title]** — [One-sentence summary]. Severity: [0-4]. Location: [where].
3. **[Finding title]** — [One-sentence summary]. Severity: [0-4]. Location: [where].

### Summary Assessment

*[2-3 paragraph overview of the product's UX health. Highlight the strongest areas, the weakest areas, and the overall trajectory. Frame the assessment in terms of user impact and business risk. End with a clear recommendation for next steps.]*

---

## 2. Methodology

### Frameworks Applied

- [ ] Nielsen's 10 Usability Heuristics
- [ ] WCAG 2.2 Level AA Accessibility Guidelines
- [ ] Core Web Vitals (LCP, FID/INP, CLS)
- [ ] 10-Dimension UX Scoring Rubric
- [ ] [Other domain-specific checklist, if applicable]

### Scope Definition

- **Product type**: [SaaS dashboard / Landing page / Admin portal / Mobile app / Other]
- **User flows evaluated**: [List each flow audited, e.g., "Sign-up flow," "Dashboard overview," "Settings page," "Checkout flow"]
- **Devices tested**: [e.g., "Chrome 120 on macOS 14, Safari on iOS 17 (iPhone 15), Chrome on Android 14 (Pixel 8)"]
- **User roles evaluated**: [e.g., "Admin, Standard user, Viewer"]
- **Tools used**: [e.g., "Lighthouse, axe DevTools, WAVE, Chrome DevTools, VoiceOver, manual keyboard testing"]

### Severity Rating System

| Rating | Label | Description |
|--------|-------|-------------|
| 0 | Not a problem | Heuristic violation, no real user impact |
| 1 | Cosmetic | Minor visual issue, does not affect task completion |
| 2 | Minor | Users slowed down but can complete tasks |
| 3 | Major | Users frequently fail or experience significant frustration |
| 4 | Catastrophic | Users cannot complete critical tasks; data loss or security risk |

---

## 3. Scores by Category

### 10-Dimension UX Health Score

| # | Dimension | Score (/5) | Severity Indicator |
|---|-----------|-----------|-------------------|
| 1 | Navigation | [1-5] | [Green/Yellow/Red] |
| 2 | Clarity | [1-5] | [Green/Yellow/Red] |
| 3 | Feedback | [1-5] | [Green/Yellow/Red] |
| 4 | Error Handling | [1-5] | [Green/Yellow/Red] |
| 5 | Consistency | [1-5] | [Green/Yellow/Red] |
| 6 | Accessibility | [1-5] | [Green/Yellow/Red] |
| 7 | Performance | [1-5] | [Green/Yellow/Red] |
| 8 | Mobile | [1-5] | [Green/Yellow/Red] |
| 9 | Visual Design | [1-5] | [Green/Yellow/Red] |
| 10 | Content | [1-5] | [Green/Yellow/Red] |
| | **Total** | **[XX] / 50** | |

*Severity indicator key: Green = 4-5 (strong), Yellow = 3 (adequate), Red = 1-2 (needs attention)*

### Score Commentary

*[For each dimension that scores 3 or below, provide 1-2 sentences explaining why it received that score and what the primary issues are. For dimensions that score 4-5, briefly note what is working well.]*

**Navigation** ([score]/5): *[Commentary]*

**Clarity** ([score]/5): *[Commentary]*

**Feedback** ([score]/5): *[Commentary]*

**Error Handling** ([score]/5): *[Commentary]*

**Consistency** ([score]/5): *[Commentary]*

**Accessibility** ([score]/5): *[Commentary]*

**Performance** ([score]/5): *[Commentary]*

**Mobile** ([score]/5): *[Commentary]*

**Visual Design** ([score]/5): *[Commentary]*

**Content** ([score]/5): *[Commentary]*

---

## 4. Issues by Severity

### Critical Issues (Severity 4)

*These issues prevent users from completing critical tasks or pose data loss/security risks. Fix immediately.*

---

#### Issue C1: [Issue Title]

| Field | Detail |
|-------|--------|
| **Severity** | 4 — Catastrophic |
| **Location** | [Page/screen/component where the issue occurs] |
| **Heuristic Violated** | [e.g., "H3: User control and freedom" or "WCAG 2.1.1: Keyboard"] |
| **Frequency** | [Common / Occasional / Rare] |
| **User Impact** | [Who is affected and how] |

**Description**: *[Detailed description of the problem. What happens, when it happens, and why it is problematic for users.]*

**Recommendation**: *[Specific, actionable recommendation for fixing the issue. Include implementation guidance where possible.]*

**Expected Impact**: *[What improvement users will experience after the fix. Quantify if possible.]*

---

#### Issue C2: [Issue Title]

| Field | Detail |
|-------|--------|
| **Severity** | 4 — Catastrophic |
| **Location** | [Page/screen/component] |
| **Heuristic Violated** | [Heuristic or guideline reference] |
| **Frequency** | [Common / Occasional / Rare] |
| **User Impact** | [Who is affected and how] |

**Description**: *[Detailed description]*

**Recommendation**: *[Specific recommendation]*

**Expected Impact**: *[Expected improvement]*

---

*[Repeat the issue block for each critical issue found. Delete unused blocks.]*

---

### Major Issues (Severity 3)

*These issues cause significant user frustration or frequent task failure. Fix before the next release.*

---

#### Issue M1: [Issue Title]

| Field | Detail |
|-------|--------|
| **Severity** | 3 — Major |
| **Location** | [Page/screen/component] |
| **Heuristic Violated** | [Heuristic or guideline reference] |
| **Frequency** | [Common / Occasional / Rare] |
| **User Impact** | [Who is affected and how] |

**Description**: *[Detailed description]*

**Recommendation**: *[Specific recommendation]*

**Expected Impact**: *[Expected improvement]*

---

#### Issue M2: [Issue Title]

| Field | Detail |
|-------|--------|
| **Severity** | 3 — Major |
| **Location** | [Page/screen/component] |
| **Heuristic Violated** | [Heuristic or guideline reference] |
| **Frequency** | [Common / Occasional / Rare] |
| **User Impact** | [Who is affected and how] |

**Description**: *[Detailed description]*

**Recommendation**: *[Specific recommendation]*

**Expected Impact**: *[Expected improvement]*

---

*[Repeat for each major issue. Delete unused blocks.]*

---

### Minor Issues (Severity 2)

*These issues slow users down but do not prevent task completion. Schedule for upcoming sprints.*

---

#### Issue N1: [Issue Title]

| Field | Detail |
|-------|--------|
| **Severity** | 2 — Minor |
| **Location** | [Page/screen/component] |
| **Heuristic Violated** | [Heuristic or guideline reference] |
| **Frequency** | [Common / Occasional / Rare] |
| **User Impact** | [Who is affected and how] |

**Description**: *[Detailed description]*

**Recommendation**: *[Specific recommendation]*

**Expected Impact**: *[Expected improvement]*

---

*[Repeat for each minor issue. Delete unused blocks.]*

---

### Cosmetic Issues (Severity 0-1)

*These issues are visual inconsistencies or polish items. Fix when time allows.*

---

#### Issue L1: [Issue Title]

| Field | Detail |
|-------|--------|
| **Severity** | [0 or 1] — [Not a problem / Cosmetic] |
| **Location** | [Page/screen/component] |
| **Heuristic Violated** | [Heuristic or guideline reference] |
| **Description** | *[Brief description]* |
| **Recommendation** | *[Brief recommendation]* |

---

*[Repeat for each cosmetic issue. Use the shorter format for low-severity items. Delete unused blocks.]*

---

## 5. Nielsen's 10 Heuristics Evaluation

| # | Heuristic | Score (/5) | Comment |
|---|-----------|-----------|---------|
| 1 | Visibility of system status | [1-5] | *[Brief assessment: loading indicators, progress bars, save confirmations, system status badges]* |
| 2 | Match between system and real world | [1-5] | *[Brief assessment: language familiarity, real-world metaphors, user-tested labels]* |
| 3 | User control and freedom | [1-5] | *[Brief assessment: undo/redo, cancel buttons, back navigation, escape to close]* |
| 4 | Consistency and standards | [1-5] | *[Brief assessment: button styles, terminology, icon usage, interaction patterns]* |
| 5 | Error prevention | [1-5] | *[Brief assessment: confirmation dialogs, input constraints, smart defaults, disabled invalid options]* |
| 6 | Recognition rather than recall | [1-5] | *[Brief assessment: visible labels, recently used items, contextual help, autocomplete]* |
| 7 | Flexibility and efficiency of use | [1-5] | *[Brief assessment: keyboard shortcuts, saved preferences, customizable views, command palette]* |
| 8 | Aesthetic and minimalist design | [1-5] | *[Brief assessment: information density, decorative elements, progressive disclosure, focused content]* |
| 9 | Help users recognize, diagnose, and recover from errors | [1-5] | *[Brief assessment: error message quality, field identification, recovery guidance]* |
| 10 | Help and documentation | [1-5] | *[Brief assessment: help center, tooltips, contextual docs, shortcut reference]* |
| | **Average** | **[X.X] / 5** | |

---

## 6. Prioritized Recommendations

### Recommendations Table

| # | Recommendation | Related Issues | Impact | Effort | Priority | Quadrant |
|---|---------------|---------------|--------|--------|----------|----------|
| R1 | [Specific recommendation] | C1, M2 | High | Low | P0 | Quick Win |
| R2 | [Specific recommendation] | C2 | High | High | P1 | Major Project |
| R3 | [Specific recommendation] | M1, M3 | High | Low | P1 | Quick Win |
| R4 | [Specific recommendation] | M4 | Medium | Medium | P2 | — |
| R5 | [Specific recommendation] | N1, N2 | Medium | Low | P2 | Fill-in |
| R6 | [Specific recommendation] | N3 | Low | Low | P3 | Fill-in |
| R7 | [Specific recommendation] | L1, L2 | Low | High | P4 | Avoid |

*[Add or remove rows as needed. Order by priority (P0 first, P4 last). Map each recommendation to the Impact-Effort quadrant.]*

### RICE Scores (for top recommendations)

*[Optional: Include RICE scoring for the top 5-10 recommendations when quantitative prioritization is needed.]*

| # | Recommendation | Reach | Impact | Confidence | Effort | RICE Score |
|---|---------------|-------|--------|------------|--------|------------|
| R1 | [Recommendation] | [users/mo] | [0.25-3] | [50-100%] | [person-months] | [score] |
| R2 | [Recommendation] | [users/mo] | [0.25-3] | [50-100%] | [person-months] | [score] |
| R3 | [Recommendation] | [users/mo] | [0.25-3] | [50-100%] | [person-months] | [score] |

---

## 7. Action Plan

### Immediate (Fix within 1 week)

*P0 issues and quick wins that address critical problems.*

- [ ] [Recommendation R1]: [Brief description of what to do and expected outcome]
- [ ] [Recommendation R3]: [Brief description of what to do and expected outcome]
- [ ] [Additional immediate items as needed]

**Expected outcome**: *[Summary of how the product improves after completing immediate fixes, e.g., "All critical task-blocking issues resolved. Users can complete sign-up and checkout flows without failure."]*

### Short-term (Fix within 1 month)

*P1 and P2 issues that significantly improve the user experience.*

- [ ] [Recommendation R2]: [Brief description of what to do and expected outcome]
- [ ] [Recommendation R4]: [Brief description of what to do and expected outcome]
- [ ] [Recommendation R5]: [Brief description of what to do and expected outcome]
- [ ] [Additional short-term items as needed]

**Expected outcome**: *[Summary of how the product improves after completing short-term fixes, e.g., "Major friction points resolved. UX Health Score expected to improve from XX/50 to XX/50."]*

### Medium-term (Fix within 1 quarter)

*P3 items, major projects, and systematic improvements.*

- [ ] [Recommendation R6]: [Brief description of what to do and expected outcome]
- [ ] [Recommendation R7]: [Brief description of what to do and expected outcome]
- [ ] [Additional medium-term items as needed]
- [ ] Conduct follow-up usability testing to validate fixes and identify new issues
- [ ] Re-audit after major changes to measure improvement

**Expected outcome**: *[Summary of the target state after completing medium-term work, e.g., "Full WCAG 2.2 AA compliance achieved. Design system consistency across all pages. UX Health Score target: XX/50."]*

---

## 8. Appendix

### A. Core Web Vitals Results

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Largest Contentful Paint (LCP) | [X.Xs] | < 2.5s | [Pass/Fail] |
| First Input Delay (FID) | [Xms] | < 100ms | [Pass/Fail] |
| Interaction to Next Paint (INP) | [Xms] | < 200ms | [Pass/Fail] |
| Cumulative Layout Shift (CLS) | [X.XX] | < 0.1 | [Pass/Fail] |
| Time to First Byte (TTFB) | [Xms] | < 800ms | [Pass/Fail] |

### B. Accessibility Summary

| Category | Items Checked | Items Passed | Items Failed | Pass Rate |
|----------|--------------|-------------|-------------|-----------|
| Perceivable | [X] | [X] | [X] | [X%] |
| Operable | [X] | [X] | [X] | [X%] |
| Understandable | [X] | [X] | [X] | [X%] |
| Robust | [X] | [X] | [X] | [X%] |
| **Total** | **[X]** | **[X]** | **[X]** | **[X%]** |

### C. Screenshots and Evidence

*[Include annotated screenshots for each finding. Organize by issue ID (C1, M1, N1, etc.). Annotations should highlight the specific problem area and reference the issue description.]*

### D. Tools and Versions

| Tool | Version | Purpose |
|------|---------|---------|
| [e.g., Google Lighthouse] | [version] | Performance and accessibility audit |
| [e.g., axe DevTools] | [version] | Automated accessibility testing |
| [e.g., WAVE] | [version] | Visual accessibility evaluation |
| [e.g., Chrome DevTools] | [version] | Manual inspection and network analysis |
| [e.g., VoiceOver] | [version] | Screen reader testing |

---

*Report generated using the UX Audit Framework. Refer to the audit-checklist.md for the complete evaluation criteria and severity-scoring.md for the scoring methodology.*
