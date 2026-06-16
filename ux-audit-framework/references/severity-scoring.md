# Severity Rating and Prioritization Systems

This reference provides the complete scoring and prioritization frameworks used during **Phase 3 (Score)** and **Phase 5 (Prioritize)** of the UX audit process. It covers Nielsen's severity scale, the three-factor severity model, four prioritization frameworks, and the full 10-dimension UX scoring rubric.

---

## 1. Nielsen's Severity Rating Scale (0-4)

**Source**: Jakob Nielsen, Nielsen Norman Group (1994, updated)

This is the standard severity classification for usability findings. Every issue discovered during an audit receives a rating from 0 to 4.

### Scale Definition

| Rating | Label | Description | Required Action | Timeline |
|--------|-------|-------------|-----------------|----------|
| **0** | Not a usability problem | A heuristic violation is present but does not affect real users in practice | Document for reference only | No fix needed |
| **1** | Cosmetic problem | A minor visual inconsistency or polish issue that does not affect task completion or user comprehension | Fix if time and resources allow | Low priority backlog |
| **2** | Minor usability problem | Users are slowed down or mildly confused but can still complete their tasks without assistance | Schedule for an upcoming sprint | Next 2-4 weeks |
| **3** | Major usability problem | Users frequently fail, get stuck, or experience significant frustration; some users may abandon the task | Fix before the next release | Next 1-2 weeks |
| **4** | Usability catastrophe | Users cannot complete critical tasks; risk of data loss, security compromise, or complete task failure; the product should not ship with this issue | Fix immediately; consider hotfix | Within 1-3 days |

### Examples by Severity Level

**Severity 0 — Not a problem**
- A button uses 14px font instead of the design system's 15px specification
- A tooltip arrow is 2px off-center
- A transition animation uses ease-in instead of ease-in-out

**Severity 1 — Cosmetic**
- Inconsistent border radius between similar cards (4px vs. 8px)
- Slightly different shades of the brand color on different pages
- Icon style mismatch (one outlined icon among filled icons)
- Uneven spacing between footer links

**Severity 2 — Minor**
- Users must scroll to find the save button on a commonly used form
- Search results are relevant but lack highlighting of matched terms
- A filter panel does not remember selections when navigating back from a detail view
- Date format is ambiguous (01/02/2025 — is it January 2 or February 1?)

**Severity 3 — Major**
- Form validation only triggers on submit, causing users to re-enter multiple fields
- No confirmation dialog before deleting records
- Navigation labels use internal jargon that users do not understand
- Mobile users cannot access a feature that is available on desktop
- Error messages display raw technical text ("Error 422: Unprocessable Entity")

**Severity 4 — Catastrophic**
- Form loses all entered data on a validation error or page refresh
- Users cannot complete the sign-up or checkout flow due to a broken step
- No keyboard accessibility — keyboard-only users are locked out entirely
- Sensitive data (passwords, API keys) displayed in plain text
- Critical action (delete account, transfer funds) executes without any confirmation

---

## 2. Three-Factor Severity Model

When a finding's severity is ambiguous, evaluate these three factors independently, then combine them to determine the final rating.

### Factor Definitions

| Factor | Question | Scale |
|--------|----------|-------|
| **Frequency** | How often does this problem occur? | Rare (affects edge cases) / Occasional (some users, some flows) / Common (most users encounter it) |
| **Impact** | How difficult is it for users to overcome the problem? | Easy (minor inconvenience, user adapts quickly) / Difficult (user struggles, may need help) / Impossible (user cannot complete the task) |
| **Persistence** | Does the problem recur each time the user encounters this situation? | One-time (only affects first encounter, user learns to work around it) / Recurring (happens every time the user encounters this context) |

### Combining the Three Factors

Use this decision table to map factor combinations to severity ratings:

| Frequency | Impact | Persistence | Severity |
|-----------|--------|-------------|----------|
| Rare | Easy | One-time | 0 — Not a problem |
| Rare | Easy | Recurring | 1 — Cosmetic |
| Rare | Difficult | One-time | 1 — Cosmetic |
| Rare | Difficult | Recurring | 2 — Minor |
| Rare | Impossible | Any | 3 — Major |
| Occasional | Easy | One-time | 1 — Cosmetic |
| Occasional | Easy | Recurring | 2 — Minor |
| Occasional | Difficult | One-time | 2 — Minor |
| Occasional | Difficult | Recurring | 3 — Major |
| Occasional | Impossible | Any | 3 — Major |
| Common | Easy | One-time | 1 — Cosmetic |
| Common | Easy | Recurring | 2 — Minor |
| Common | Difficult | One-time | 2 — Minor |
| Common | Difficult | Recurring | 3 — Major |
| Common | Impossible | Any | 4 — Catastrophic |

**Special rule**: Any issue involving data loss, security risk, or complete inability to use a core feature defaults to severity 4 regardless of frequency.

---

## 3. Severity x Frequency Prioritization Matrix

After scoring severity, map findings to priority codes using this matrix. Priority codes determine the fix timeline.

|  | Low Frequency | Medium Frequency | High Frequency |
|--|---------------|------------------|----------------|
| **High Severity (3-4)** | **P2** — Schedule soon (next 2 sprints) | **P1** — Fix next sprint | **P0** — Fix immediately (hotfix) |
| **Medium Severity (2)** | **P3** — Add to backlog | **P2** — Schedule soon (next 2 sprints) | **P1** — Fix next sprint |
| **Low Severity (0-1)** | **P4** — Nice to have (polish backlog) | **P3** — Add to backlog | **P2** — Schedule soon (next 2 sprints) |

### Priority Code Definitions

| Priority | Label | Timeline | Description |
|----------|-------|----------|-------------|
| **P0** | Critical | Fix within 1-3 days | Blocking issue affecting many users on critical flows. Warrants a hotfix outside normal release cycle. |
| **P1** | High | Fix next sprint | Significant usability issue that should be addressed in the next development sprint. |
| **P2** | Medium | Fix within 2 sprints | Important issue that should be scheduled soon but does not require immediate action. |
| **P3** | Low | Backlog | Issue that should be fixed but can wait for a convenient development window. |
| **P4** | Minimal | Polish backlog | Cosmetic or low-impact issue. Fix when time permits or bundle with related work. |

---

## 4. RICE Scoring Framework

RICE provides a quantitative method for prioritizing UX fixes when multiple issues compete for limited development resources. It is especially useful for comparing issues of similar severity.

### Formula

**RICE Score = (Reach x Impact x Confidence) / Effort**

### Factor Definitions

| Factor | Definition | How to Estimate |
|--------|-----------|-----------------|
| **Reach** | How many users are affected per time period (e.g., per month) | Use analytics data: page views, feature usage counts, or percentage of total users |
| **Impact** | How much does fixing this issue improve the experience for each affected user? | 3 = Massive improvement / 2 = High improvement / 1 = Medium improvement / 0.5 = Low improvement / 0.25 = Minimal improvement |
| **Confidence** | How confident are you in your Reach and Impact estimates? | 100% = High confidence (data-backed) / 80% = Medium confidence (strong heuristic evidence) / 50% = Low confidence (gut feel, limited data) |
| **Effort** | How many person-months (or person-weeks) will this take to fix? | Estimate including design, development, QA, and deployment. Use 0.5 for quick fixes, 1-2 for moderate work, 3+ for major projects |

### Worked Example

**Issue**: Form validation only triggers on submit (severity 3, major).

| Factor | Value | Rationale |
|--------|-------|-----------|
| Reach | 5,000 users/month | All users who submit the registration form |
| Impact | 2 (High) | Prevents repeated errors and frustration during a critical flow |
| Confidence | 80% | Strong heuristic evidence; confirmed by 3 support tickets/week |
| Effort | 0.5 person-months | Straightforward front-end validation implementation |

**RICE Score** = (5,000 x 2 x 0.8) / 0.5 = **16,000**

**Issue**: Icon style inconsistency on the settings page (severity 1, cosmetic).

| Factor | Value | Rationale |
|--------|-------|-----------|
| Reach | 800 users/month | Users who visit the settings page |
| Impact | 0.25 (Minimal) | Does not affect task completion |
| Confidence | 100% | Clearly visible, no ambiguity |
| Effort | 0.25 person-months | Simple asset replacement |

**RICE Score** = (800 x 0.25 x 1.0) / 0.25 = **800**

The form validation issue (16,000) should be prioritized significantly above the icon inconsistency (800).

---

## 5. Impact-Effort Matrix (2x2)

This is a rapid visual prioritization tool for sorting recommendations into four quadrants during stakeholder presentations or sprint planning.

### The Four Quadrants

```
                    HIGH IMPACT
                        |
     Major Projects     |     Quick Wins
     (Plan carefully)   |     (Do first)
                        |
  HIGH EFFORT ----------+---------- LOW EFFORT
                        |
     Avoid              |     Fill-ins
     (Deprioritize)     |     (Do if spare time)
                        |
                    LOW IMPACT
```

### Quadrant Descriptions

- [ ] **Quick Wins (High Impact, Low Effort)** — Implement these first. They deliver the most value for the least investment. Examples: fixing broken form validation, adding missing alt text, improving error messages, adding a loading indicator.

- [ ] **Major Projects (High Impact, High Effort)** — These require careful planning, dedicated sprints, and potentially cross-team coordination. Examples: redesigning the navigation architecture, implementing comprehensive keyboard accessibility, rebuilding the onboarding flow, achieving full WCAG 2.2 AA compliance.

- [ ] **Fill-ins (Low Impact, Low Effort)** — Handle these during slack time, bug-fix sprints, or when working on adjacent code. Examples: fixing minor spacing inconsistencies, aligning icon styles, adjusting animation timing, tweaking microcopy.

- [ ] **Avoid (Low Impact, High Effort)** — Deprioritize or eliminate these from the roadmap. The effort does not justify the impact. Examples: rebuilding a rarely-used settings page for marginal visual improvement, implementing a complex animation system for decorative purposes.

### How to Use in the Audit Report

1. Plot each recommendation on the matrix based on estimated impact (how much it improves user experience and business metrics) and effort (design + development + QA time).
2. Label each recommendation with its quadrant assignment in the prioritized recommendations table.
3. Present Quick Wins as the recommended starting point in the action plan.

---

## 6. MoSCoW Prioritization Method

MoSCoW categorization translates audit findings into stakeholder-friendly language by grouping recommendations into four categories based on necessity.

### Category Definitions

- [ ] **Must Have** — Non-negotiable fixes. Critical usability failures that prevent task completion, accessibility violations that create legal risk, broken flows, data loss scenarios, and security issues. These correspond to severity 3-4 findings and P0-P1 priorities.

- [ ] **Should Have** — Significant UX improvements with clear return on investment. These issues cause measurable friction, increase support load, or reduce conversion rates. They are important but the product can technically function without fixing them. Correspond to severity 2-3 findings and P1-P2 priorities.

- [ ] **Could Have** — Desirable enhancements that improve polish, consistency, and delight. These make the product feel more refined but do not significantly impact core usability or business metrics. Correspond to severity 1-2 findings and P3 priorities.

- [ ] **Won't Have (this iteration)** — Acknowledged issues that are explicitly deferred to a future iteration. This category prevents scope creep and sets clear expectations. Items here may be severity 0-1 findings, aspirational improvements, or major projects that require prerequisite work.

### Mapping Severity to MoSCoW

| Severity | Typical MoSCoW Category |
|----------|------------------------|
| 4 — Catastrophic | Must Have (always) |
| 3 — Major | Must Have or Should Have |
| 2 — Minor | Should Have or Could Have |
| 1 — Cosmetic | Could Have or Won't Have |
| 0 — Not a problem | Won't Have |

---

## 7. Ten-Dimension UX Scoring Rubric (Full Detail)

This rubric provides the structured evaluation criteria for the 10-dimension UX Health Score. Each dimension is scored 1 through 5. The sum of all 10 dimensions produces a total out of 50.

### Scoring Instructions

- Evaluate each dimension independently based on the descriptions below.
- A score of **1** indicates severe deficiency. A score of **3** indicates acceptable but improvable performance. A score of **5** indicates best-in-class implementation.
- Scores of **2** and **4** represent intermediate levels (between poor/adequate and adequate/excellent respectively). Use them when the interface partially meets the criteria for the next level.
- Document specific evidence for each score to justify the rating.

---

### Dimension 1: Navigation

*How easily can users find features and move through the product?*

| Score | Description |
|-------|-------------|
| **1 — Poor** | Users cannot locate core features. Navigation is hidden, mislabeled, or inconsistent. No breadcrumbs or wayfinding aids. Users rely on browser back button or direct URLs. More than 9 top-level items or deeply nested menus with no hierarchy aid. |
| **2** | Navigation exists but is confusing. Some labels are unclear. Active state may be missing. Users can eventually find things but waste significant time. |
| **3 — Adequate** | Users can find features with some effort. Navigation is present and mostly consistent. Some wayfinding gaps exist (missing breadcrumbs for deep pages, occasional label ambiguity). 7-9 top-level items. |
| **4** | Navigation is clear and consistent. Minor issues remain (one or two missing breadcrumbs, a slightly unclear label). Users rarely get lost. |
| **5 — Excellent** | Users find everything instantly. Navigation is intuitive, consistently placed, clearly labeled, and appropriate for the information architecture. Breadcrumbs, search, keyboard navigation, and mobile adaptation all function correctly. Under 7 top-level items. |

---

### Dimension 2: Clarity

*How quickly can users understand what to do on any given screen?*

| Score | Description |
|-------|-------------|
| **1 — Poor** | Users do not understand the purpose of pages or how to accomplish tasks. Language is full of jargon. No visual hierarchy guides attention. Users frequently ask "what does this mean?" or "what am I supposed to do?" |
| **2** | Page purpose is guessable but not obvious. Some jargon remains. Visual hierarchy is weak — multiple elements compete for attention without clear priority. |
| **3 — Adequate** | Users figure out what to do with moderate effort. Language is mostly clear. Visual hierarchy exists but could be stronger. Primary actions are present but not immediately prominent. |
| **4** | Intent is clear on most screens. Language is user-centered. Visual hierarchy effectively guides attention. Minor clarity issues on secondary screens. |
| **5 — Excellent** | Intent is immediately clear on every screen. Headlines, labels, and microcopy are concise and user-centered. Visual hierarchy is strong — users' eyes go directly to the primary action. Zero jargon. |

---

### Dimension 3: Feedback

*How well does the system communicate what is happening in response to user actions?*

| Score | Description |
|-------|-------------|
| **1 — Poor** | No visible response to user actions. Users click buttons with no indication of success, failure, or processing. No loading states. Users cannot tell if the system received their input. |
| **2** | Minimal feedback — some actions produce a response but many do not. Loading states are inconsistent. Users are sometimes left wondering if their action worked. |
| **3 — Adequate** | Basic loading and success states are present for primary flows. Some secondary actions lack feedback. Generic messages ("Success") without specifics. |
| **4** | Most actions produce clear, timely feedback. Loading states, success confirmations, and error messages are present. Minor gaps in feedback for edge cases or secondary flows. |
| **5 — Excellent** | Rich, contextual feedback for every action. Loading indicators appear within 100ms. Success messages are specific ("Project 'Alpha' saved"). Progress bars for long operations. Background task status is visible. Optimistic UI where appropriate. |

---

### Dimension 4: Error Handling

*How well does the system prevent errors and help users recover from them?*

| Score | Description |
|-------|-------------|
| **1 — Poor** | Errors cause data loss or dead ends. No validation before submission. Error messages are technical ("Error 500"), unhelpful, or absent. No undo for destructive actions. Users cannot recover without starting over. |
| **2** | Some error handling exists but is inconsistent. Error messages appear but are vague. Some destructive actions lack confirmation. Data is occasionally lost on errors. |
| **3 — Adequate** | Errors are caught with generic messages ("Something went wrong"). Confirmation exists for most destructive actions. Inline validation is present on some forms. Recovery is possible but not guided. |
| **4** | Error messages are mostly specific and helpful. Input constraints prevent many common errors. Undo is available for most reversible actions. Minor gaps in error prevention on secondary flows. |
| **5 — Excellent** | Errors are proactively prevented through input constraints, smart defaults, and inline validation. When errors occur, messages are plain-language, specific, and suggest corrective action. Undo and soft-delete protect against mistakes. Destructive actions require graduated confirmation. |

---

### Dimension 5: Consistency

*How uniform are patterns, terminology, and behavior across the product?*

| Score | Description |
|-------|-------------|
| **1 — Poor** | Every page feels like a different application. Buttons, forms, navigation, and terminology vary randomly. No discernible design system or pattern library in use. Users must relearn the interface on each screen. |
| **2** | Some patterns repeat but inconsistencies are frequent. Similar actions sometimes use different controls or labels. Color usage is inconsistent. |
| **3 — Adequate** | Most patterns are consistent. A design system appears to be in use but with gaps. Occasional inconsistencies in terminology, spacing, or interaction patterns. Users generally know what to expect. |
| **4** | Strong consistency across the product. Design system is well-applied. Minor inconsistencies exist in edge cases or recently added features. |
| **5 — Excellent** | Complete pattern consistency. Every button, form, modal, table, and interaction follows the same design system. Terminology is uniform. Users who learn one area of the product can predict behavior in all other areas. |

---

### Dimension 6: Accessibility

*How usable is the product for people with disabilities and users of assistive technology?*

| Score | Description |
|-------|-------------|
| **1 — Poor** | Keyboard navigation is non-functional. No alt text on images. Color contrast fails WCAG minimums. Screen reader users cannot use the product. Focus indicators are invisible. |
| **2** | Some accessibility basics are present but significant gaps remain. Partial alt text coverage. Some keyboard functionality. Contrast passes on some elements but fails on others. |
| **3 — Adequate** | Partial WCAG 2.2 Level AA compliance. Most images have alt text. Keyboard navigation works for primary flows. Color contrast mostly passes. Focus indicators are present but may be low contrast. Some ARIA usage. |
| **4** | Strong accessibility. Most WCAG 2.2 Level AA criteria are met. Keyboard navigation is comprehensive. Screen reader experience is functional. Touch targets meet size requirements. Minor gaps remain. |
| **5 — Excellent** | Full WCAG 2.2 Level AA compliance. Keyboard navigation is complete and logical. Screen reader experience is polished with proper announcements, landmark regions, and ARIA labels. Focus indicators are high-contrast. Touch targets exceed minimum size. Skip navigation is present. All media has captions/transcripts. |

---

### Dimension 7: Performance

*How fast does the product load and respond to interactions?*

| Score | Description |
|-------|-------------|
| **1 — Poor** | LCP exceeds 5 seconds. Significant layout shift (CLS > 0.25). Interactions feel sluggish (FID/INP > 500ms). No loading states — users stare at blank screens. Page weight is excessive. |
| **2** | LCP is 4-5 seconds. Some layout shift occurs. Loading states are present but inconsistent. Some interactions feel slow. |
| **3 — Adequate** | LCP is 2.5-4 seconds. CLS is 0.1-0.25 (some layout shift). FID/INP is 100-300ms. Basic skeleton/loading states exist. Room for optimization. |
| **4** | LCP is under 2.5 seconds. CLS is under 0.1. Most interactions are responsive. Loading states are well-implemented. Minor performance issues on specific pages. |
| **5 — Excellent** | LCP under 2.5 seconds consistently. CLS under 0.1. FID/INP under 100ms/200ms. Skeleton screens, optimistic updates, lazy loading, and image optimization are all implemented. The product feels instant. |

---

### Dimension 8: Mobile Experience

*How well does the product work on mobile devices?*

| Score | Description |
|-------|-------------|
| **1 — Poor** | Product is broken on mobile. Horizontal scrolling, unreadable text (< 14px), overlapping elements, unreachable buttons, or completely non-functional features. Desktop layout forced onto mobile viewport. |
| **2** | Product is technically usable on mobile but with significant issues. Some elements are too small. Some features are hard to reach. Layout breaks at certain widths. |
| **3 — Adequate** | Product is functional on mobile but feels awkward. Touch targets are mostly adequate. Layout adapts but with some issues (unnecessary scrolling, cramped sections). Some desktop-only interactions lack mobile equivalents. |
| **4** | Mobile experience is good. Layout adapts well. Touch targets are appropriate. Most interactions work smoothly. Minor issues with specific components or edge cases on small screens. |
| **5 — Excellent** | Native-quality mobile experience. Fluid responsive design across all breakpoints. Touch targets exceed minimums. Thumb-zone optimization for key actions. Mobile-appropriate navigation (bottom nav, gestures). All features fully accessible on mobile. |

---

### Dimension 9: Visual Design

*How well does the visual design support usability and communicate hierarchy?*

| Score | Description |
|-------|-------------|
| **1 — Poor** | Cluttered layout with no clear hierarchy. Every element competes for attention. Excessive color usage. Inconsistent spacing. No design system apparent. The interface feels chaotic and unprofessional. |
| **2** | Some design structure exists but is weak. Spacing is inconsistent. Color usage is not fully purposeful. Hierarchy is unclear in some areas. |
| **3 — Adequate** | Clean design with some hierarchy issues. Whitespace is used but not optimally. Color palette exists but has minor inconsistencies. The interface is professional but not polished. |
| **4** | Well-designed interface with clear hierarchy. Purposeful use of whitespace, color, and typography. Minor refinements needed for full polish. |
| **5 — Excellent** | Clear visual hierarchy on every screen. Purposeful whitespace creates breathing room and groups content. Color is used systematically and meaningfully. Typography scale is well-defined. The interface feels polished, modern, and intentionally designed. Every visual element serves a purpose. |

---

### Dimension 10: Content

*How effective is the written content at guiding users and communicating clearly?*

| Score | Description |
|-------|-------------|
| **1 — Poor** | Content is jargon-heavy, unclear, and unhelpful. Error messages are technical or absent. Labels are confusing. Users cannot understand what things mean or what to do. No empty states or help text. |
| **2** | Content is partially clear but significant jargon or ambiguity remains. Some helpful microcopy exists but coverage is inconsistent. |
| **3 — Adequate** | Content is mostly clear with occasional jargon. Labels and headings are generally understandable. Error messages exist but are generic. Empty states are present but basic. |
| **4** | Content is user-centered and clear. Most microcopy is helpful and specific. Error messages guide users. Minor content gaps on secondary screens. |
| **5 — Excellent** | All content is scannable, user-centered, and helpful. Headings allow users to understand page purpose instantly. Error messages are specific and suggest corrective actions. Empty states are encouraging and actionable. Microcopy is consistent, concise, and jargon-free throughout. Help text is contextual. |

---

## Score Interpretation

### UX Health Score Calculation

**Total = Sum of all 10 dimensions (each scored 1-5)**

| Score Range | Percentage | Interpretation |
|-------------|-----------|----------------|
| 10-20 | 20-40% | **Critical** — Fundamental usability problems across multiple dimensions. The product likely suffers from high abandonment, frequent support requests, and low user satisfaction. Immediate, broad intervention required. |
| 21-29 | 42-58% | **Needs significant work** — Multiple dimensions are below adequate. Users can accomplish some tasks but experience substantial friction. Prioritize must-have fixes and quick wins. |
| 30-35 | 60-70% | **Adequate foundation** — Core functionality works but rough edges reduce efficiency and satisfaction. Target the lowest-scoring dimensions for maximum improvement. |
| 36-40 | 72-80% | **Good** — Solid UX with identifiable areas for improvement. Users can accomplish tasks effectively. Focus on raising the weakest dimensions and refining the overall polish. |
| 41-45 | 82-90% | **Strong** — Well-designed product with minor gaps. Most best practices are followed. Focus on edge cases, advanced accessibility, and competitive differentiation. |
| 46-50 | 92-100% | **Excellent** — Best-in-class UX. Continuous iteration and user research will maintain this level. Look for innovation opportunities and emerging standards. |
