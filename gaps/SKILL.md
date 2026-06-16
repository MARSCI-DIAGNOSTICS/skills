---
name: gaps
description: Analyze current requirements for completeness and identify missing areas. Uses domain checklists, NFR categories, and INVEST criteria.
argument-hint: "[--domain <domain-name>] [--severity <min-severity>] [--category <category>]"
allowed-tools: Read, Glob, Grep, Write, Skill
---

# Gaps Command

Analyze requirements for completeness and identify missing areas.

## Usage

```bash
/requirements-elicitation:gaps
/requirements-elicitation:gaps --domain "checkout"
/requirements-elicitation:gaps --severity major
/requirements-elicitation:gaps --category security
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| --domain | No | Domain to analyze (default: current/all) |
| --severity | No | Minimum severity to report: `critical`, `major`, `minor` (default: `minor`) |
| --category | No | Focus on specific category: `security`, `performance`, `usability`, etc. |

## What It Analyzes

### Requirement Coverage

- Functional requirements by category
- Non-functional requirements
- Constraints and assumptions
- Domain-specific areas

### NFR Completeness

- Performance targets
- Security requirements
- Usability/accessibility
- Reliability/availability
- Scalability

### INVEST Criteria

- Independent
- Negotiable
- Valuable
- Estimable
- Small
- Testable

## Workflow

### Step 1: Load Requirements

Gather all requirements from:

- `.requirements/{domain}/interviews/`
- `.requirements/{domain}/documents/`
- `.requirements/{domain}/simulations/`
- `.requirements/{domain}/research/`

### Step 2: Load Gap Analysis Skill

Invoke the `requirements-elicitation:gap-analysis` skill to load checklists and criteria.

### Step 3: Run Analysis

Spawn `gap-detector` agent to:

- Check category coverage
- Evaluate NFR completeness
- Assess INVEST compliance
- Identify gaps

### Step 4: Generate Report

Save gap analysis to:

```text
.requirements/{domain}/analysis/GAP-{timestamp}.yaml
```

### Step 5: Display Summary

Show key findings and recommendations.

## Examples

### Basic Gap Analysis

```bash
/requirements-elicitation:gaps
```

Output:

```text
Gap Analysis: All Domains
Analyzing 45 requirements from 3 sources...

Coverage Summary:
  Functional:     ████████░░ 80%
  Non-Functional: ████░░░░░░ 40%
  Constraints:    ██████░░░░ 60%

Critical Gaps (2):
  1. [SECURITY] No authentication requirements
     → Interview technical stakeholder
  2. [SECURITY] No authorization model
     → Interview technical stakeholder

Major Gaps (4):
  1. [PERFORMANCE] No response time targets
     → Define SLAs with business
  2. [RELIABILITY] No uptime requirements
     → Interview operations stakeholder
  3. [USABILITY] No accessibility requirements
     → Research WCAG guidelines
  4. [ERROR] No error handling specified
     → Simulation with all personas

INVEST Issues (3):
  - REQ-012: Not testable (no acceptance criteria)
  - REQ-023: Too large (needs breakdown)
  - REQ-031: Not independent (depends on REQ-030)

Verdict: NOT READY for specification
         Resolve 2 critical gaps first

Saved to: .requirements/all/analysis/GAP-20251225-160000.yaml
```

### Domain-Specific Analysis

```bash
/requirements-elicitation:gaps --domain "authentication" --severity critical
```

Output:

```text
Gap Analysis: authentication
Showing critical gaps only

Critical Gaps (0):
  None found!

Your authentication requirements cover:
  ✓ Login methods (password, SSO)
  ✓ MFA requirements
  ✓ Session management
  ✓ Password policies
  ✓ Account recovery

Coverage Summary:
  Functional:     ██████████ 100%
  Non-Functional: ████████░░ 80%

Ready for specification: YES

Suggestion: Address 2 major gaps for higher quality:
  - Performance: Login response time not specified
  - Monitoring: Audit logging requirements vague
```

### Category-Focused Analysis

```bash
/requirements-elicitation:gaps --category performance
```

Output:

```text
Gap Analysis: Performance Category

Performance Requirements Found: 3
  - REQ-008: "Page load under 3 seconds"
  - REQ-015: "API response under 200ms"
  - REQ-022: "Support 1000 concurrent users"

Performance Gaps:
  Major:
    1. No peak load handling requirements
       → Simulate operations stakeholder
    2. No database query performance targets
       → Interview technical stakeholder
    3. No caching strategy requirements
       → Research best practices

  Minor:
    1. No CDN requirements for static assets
    2. No browser performance requirements

Recommendation:
  Run: /requirements-elicitation:simulate "performance" --personas technical,operations
```

## Output Format

### Saved YAML Structure

```yaml
gap_analysis:
  session_id: "GAP-{timestamp}"
  domain: "{domain}"
  timestamp: "{ISO-8601}"
  filters:
    severity: "{min-severity}"
    category: "{focused category or all}"

  input_summary:
    total_requirements: 45
    from_interviews: 20
    from_documents: 15
    from_simulations: 8
    from_research: 2

  coverage:
    functional: 80%
    non_functional: 40%
    constraints: 60%
    assumptions: 30%

  gaps:
    critical:
      - id: GAP-001
        category: security
        description: "No authentication requirements"
        recommendation:
          technique: interview
          persona: technical
          questions: [...]

    major:
      - id: GAP-002
        category: performance
        description: "No response time targets"
        recommendation:
          technique: interview
          persona: business
          questions: [...]

    minor:
      - id: GAP-003
        category: accessibility
        description: "Only basic WCAG coverage"
        recommendation:
          technique: research
          topic: "WCAG 2.1 AA guidelines"

  invest_issues:
    - requirement: REQ-012
      issue: "Not testable"
      suggestion: "Add acceptance criteria"

  verdict:
    ready_for_specification: false
    blockers: [GAP-001, GAP-002]
    recommendations:
      - "Conduct security interview"
      - "Define performance SLAs"
```

## Integration

### Follow-Up Commands

```bash
# Fill gaps via interview
/requirements-elicitation:interview "Technical Lead" --context "security gaps"

# Fill gaps via simulation
/requirements-elicitation:simulate "security" --personas technical,compliance

# Research to fill gaps
/requirements-elicitation:research "WCAG 2.1 accessibility requirements"

# After filling gaps, re-analyze
/requirements-elicitation:gaps

# When ready, export to specification
/requirements-elicitation:export --to canonical
```

## Quality Gate

Gap analysis serves as a quality gate before specification:

```text
Ready for Specification: YES
├── No critical gaps
├── No major gaps (or accepted)
├── All INVEST criteria passing
└── Coverage > 70% in all categories

Ready for Specification: NO
├── Critical gaps exist → Must resolve
├── Major gaps exist → Should resolve
├── INVEST failures → Should fix
└── Coverage < 50% → Need more elicitation
```
