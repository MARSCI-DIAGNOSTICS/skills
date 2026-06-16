---
name: ux-audit-framework
description: Use this skill whenever the user asks for a UX audit, UI review, usability evaluation, heuristic evaluation, UX scoring, interface audit, accessibility audit, UX report, or wants to evaluate any existing interface against best practices. Also use when the user says "check the UX", "review this UI", "is this accessible", "score this page", or asks for feedback on an implemented interface. If someone has built something and wants to know if the UX is good, this skill provides the evaluation framework.
---

# UX Audit Framework

This skill provides a structured methodology for evaluating user interfaces against established usability heuristics, accessibility standards, and UX best practices. It equips the practitioner with severity rating scales, a multi-dimensional scoring rubric, prioritization frameworks, and a complete report template to deliver actionable, evidence-based audit findings.

## Audit Methodology Overview

A UX audit is a systematic evaluation of a digital product's user experience. Unlike usability testing (which observes real users), a heuristic audit is conducted by an evaluator who measures the interface against codified principles — primarily Nielsen's 10 Usability Heuristics, WCAG 2.2 accessibility guidelines, and domain-specific best practices for the product category (SaaS dashboard, landing page, admin portal, etc.).

The output of a UX audit is a prioritized list of findings, each rated by severity, accompanied by specific recommendations and an overall UX health score. This skill covers the full lifecycle: scoping the audit, conducting the analysis, scoring findings, generating the report, and prioritizing fixes.

## Severity Scale Quick Reference (Nielsen 0-4)

Use this scale to classify every issue discovered during the audit:

| Rating | Label | Description | Required Action |
|--------|-------|-------------|-----------------|
| **0** | Not a problem | Heuristic violation detected but no real user impact | Document only |
| **1** | Cosmetic | Minor visual inconsistency; does not affect task completion | Fix if time allows |
| **2** | Minor | Users are slowed down but can still complete tasks | Schedule for next sprint |
| **3** | Major | Users frequently fail or get stuck; significant frustration | Fix before next release |
| **4** | Catastrophic | Users cannot complete critical tasks; data loss risk; security issue | Fix immediately |

Three factors determine severity:

1. **Frequency** — How often does the problem occur? (Every time, occasionally, rarely)
2. **Impact** — How difficult is it for users to overcome? (Impossible, difficult, easy)
3. **Persistence** — Is it a one-time problem or does it recur every time the user encounters the situation?

Refer to `references/severity-scoring.md` for the full severity and prioritization framework, including the Severity x Frequency matrix, RICE scoring, Impact-Effort matrix, and MoSCoW method.

## 10-Dimension UX Scoring Rubric (/100)

Score each dimension from 1 (Poor) to 10 (Excellent). The sum produces a Global UX Score out of 100.

| # | Dimension | 1-3 (Poor) | 4-6 (Adequate) | 7-10 (Excellent) |
|---|-----------|------------|----------------|------------------|
| 1 | **Navigation** | Users cannot find core features | Users find features with some searching | Users find everything instantly |
| 2 | **Clarity** | Users do not understand what to do | Users figure it out with effort | Intent is immediately clear |
| 3 | **Feedback** | No response to user actions | Basic loading/success states | Rich, contextual feedback for every action |
| 4 | **Error Handling** | Errors cause data loss or dead ends | Errors caught with generic messages | Errors prevented; specific recovery guidance |
| 5 | **Consistency** | Every page feels like a different app | Most patterns are consistent | Complete pattern consistency |
| 6 | **Accessibility** | Keyboard unusable, no alt text | Partial WCAG compliance | Full WCAG 2.2 AA compliance |
| 7 | **Performance** | LCP > 5s, significant CLS | LCP 2.5-4s, some layout shift | LCP < 2.5s, CLS < 0.1, FID < 100ms |
| 8 | **Mobile** | Broken on mobile | Functional but awkward on mobile | Native-quality mobile experience |
| 9 | **Visual Design** | Cluttered, no hierarchy | Clean with some hierarchy issues | Clear hierarchy, purposeful whitespace, polished |
| 10 | **Content** | Jargon-heavy, unclear | Mostly clear, some jargon | Scannable, user-centered, helpful |

**Interpreting the score:**

- **Below 60/100** — Critical attention needed. The product has fundamental usability problems that likely cause user drop-off, support tickets, and low satisfaction.
- **60-80/100** — Solid foundation with room for improvement. Core flows work but friction points exist that reduce efficiency and satisfaction.
- **Above 80/100** — Strong UX. The product demonstrates mature design thinking. Focus shifts to polish, edge cases, and competitive differentiation.

## Audit Process Steps

Follow these five phases to conduct a thorough, repeatable UX audit.

### Phase 1: Scope

Define the boundaries of the audit before beginning any evaluation.

- Identify the product type (SaaS dashboard, landing page, admin portal, marketing site, mobile app).
- Determine which user flows to evaluate. Prioritize critical paths: sign-up, onboarding, core value action, settings, and error/edge cases.
- Establish the device and browser matrix. At minimum, test the latest Chrome on desktop and Safari on iOS.
- Confirm which heuristics and standards apply: Nielsen's 10 heuristics, WCAG 2.2 Level AA, and any domain-specific checklists.
- Agree on deliverables: report format, scoring method, and timeline.

### Phase 2: Analyze

Walk through each user flow methodically, screen by screen.

- Evaluate every screen against the audit checklist in `references/audit-checklist.md`. This checklist covers 10 categories: Navigation, Visual Design, Content/Messaging, Forms/Input, Performance, Accessibility, Mobile/Responsive, Error Handling, Loading/Feedback, and Conversion.
- For each issue found, document: the screen or component where it occurs, which heuristic or guideline it violates, a description of the problem, and a screenshot or reference.
- Apply Nielsen's 10 Usability Heuristics to each flow. Score each heuristic 1-5 and note specific violations.
- Check Core Web Vitals (LCP, FID/INP, CLS) using Lighthouse, PageSpeed Insights, or Chrome DevTools.
- Test keyboard navigation end-to-end. Verify focus order, visible focus indicators, and the absence of keyboard traps.
- Test with a screen reader (VoiceOver on macOS, NVDA on Windows) for critical flows.

### Phase 3: Score

Apply structured scoring to every finding.

- Assign a severity rating (0-4) to each issue using the three-factor model (frequency, impact, persistence).
- Score each of the 10 dimensions on the 1-10 rubric to produce the Global UX Score (/100).
- Score each of Nielsen's 10 heuristics individually (1-5) for a heuristic compliance profile.
- Categorize findings by severity tier: Critical (severity 4), Major (severity 3), Minor (severity 1-2), Cosmetic (severity 0-1).
- Use the Severity x Frequency matrix to assign priority codes (P0 through P4).

### Phase 4: Report

Assemble findings into a structured, actionable report.

- Use the report template in `references/report-template.md` as the starting structure.
- Write an executive summary with the overall score, count of critical issues, and the top three findings.
- Present the 10-dimension score table with color-coded severity indicators.
- List all issues grouped by severity tier (Critical first, then Major, then Minor). For each issue, include: title, description, location, heuristic violated, severity rating, and specific recommendation.
- Include the Nielsen Heuristics evaluation table with per-heuristic scores and comments.
- Build the prioritized recommendations table using impact, effort, and priority columns.

### Phase 5: Prioritize

Translate findings into an actionable plan.

- Apply the Impact-Effort matrix to sort recommendations into four quadrants: Quick Wins (high impact, low effort — do first), Major Projects (high impact, high effort — plan carefully), Fill-ins (low impact, low effort — do if spare time), and Avoid (low impact, high effort — deprioritize).
- For complex prioritization, use RICE scoring: Score = (Reach x Impact x Confidence) / Effort.
- Apply MoSCoW categorization: Must have (critical failures, accessibility violations, broken flows), Should have (significant improvements with clear ROI), Could have (polish enhancements), Won't have (deferred to future iterations).
- Create a three-tier action plan: Immediate (fix within 1 week — P0 and quick wins), Short-term (fix within 1 month — P1 and P2 items), Medium-term (fix within 1 quarter — P3 items and major projects).

## Reference Materials

This skill includes three reference documents for detailed application:

- **`references/audit-checklist.md`** — Comprehensive checklist organized into 10 categories (Navigation, Visual Design, Content/Messaging, Forms/Input, Performance, Accessibility, Mobile/Responsive, Error Handling, Loading/Feedback, Conversion). Use this as the primary evaluation instrument during Phase 2.

- **`references/severity-scoring.md`** — Complete scoring systems including Nielsen's severity scale, the three-factor severity model, the Severity x Frequency prioritization matrix, RICE formula, Impact-Effort 2x2 matrix, MoSCoW method, and the full 10-dimension scoring rubric with detailed descriptions for scores of 1, 3, and 5.

- **`references/report-template.md`** — Ready-to-fill audit report template with sections for Executive Summary, Methodology, Scores by Category, Issues by Severity, Nielsen Heuristics Evaluation, Prioritized Recommendations, and Action Plan.

## Common UX Anti-Patterns to Watch For

During the audit, watch for these frequently encountered anti-patterns:

- **Navigation**: Icon-only navigation without labels, mega-menus that close unexpectedly, breadcrumbs that do not reflect the actual hierarchy, inconsistent back button behavior.
- **Forms**: Placeholder text used as labels (disappears on input), form resets on validation error, validation only on submit rather than inline, ambiguous required-field marking.
- **Content**: Walls of text without headings, "click here" link text, content that shifts as the page loads (CLS), auto-playing media with sound.
- **Interaction**: Confirm/deny dialogs with unclear labels ("OK"/"Cancel" for destructive actions), disabled back button, pagination that resets position, hover-only interactions with no mobile equivalent, toast notifications that disappear in under 4 seconds.
- **Dark Patterns**: Confirmshaming, hidden costs at checkout, forced continuity after trial, roach motel (easy sign-up, hard cancellation), fake urgency timers, misdirection, trick questions with double negatives, privacy zuckering.

Flag any dark pattern as a severity 4 (Catastrophic) finding. Dark patterns erode trust and may violate regulations (FTC guidelines, EU Digital Services Act).

## When to Recommend a Full Usability Test

A heuristic audit identifies likely problems based on principles. Recommend supplementing with usability testing when:

- The product serves a specialized domain where expert evaluation may miss domain-specific user mental models.
- Findings are ambiguous — a pattern could be problematic or acceptable depending on user expectations.
- Stakeholders need quantitative evidence (task completion rates, time-on-task, System Usability Scale scores) to justify investment.
- The product is pre-launch and no user data exists yet.

A combined approach — heuristic audit for breadth, usability testing for depth — produces the most reliable results.
