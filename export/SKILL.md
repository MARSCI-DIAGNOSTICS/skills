---
name: export
description: Export elicited requirements to specification formats. Supports canonical, EARS, Gherkin, and other formats.
argument-hint: "[--domain <domain-name>] [--to <format>] [--filter <filter-options>]"
allowed-tools: Read, Glob, Grep, Write, Skill
---

# Export Command

Export elicited requirements to specification formats for downstream processing.

## Usage

```bash
/requirements-elicitation:export
/requirements-elicitation:export --domain "authentication" --to canonical
/requirements-elicitation:export --to ears --filter "priority:must"
/requirements-elicitation:export --to gherkin --domain "checkout"
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| --domain | No | Domain to export (default: current/all) |
| --to | No | Export format: `canonical`, `ears`, `gherkin`, `markdown`, `yaml`, `json` (default: `canonical`) |
| --filter | No | Filter requirements: `priority:must`, `category:functional`, `confidence:high` |

## Supported Formats

### Canonical

Transforms to canonical specification format:

```yaml
# Output: .specs/{feature}/spec.md
---
id: SPEC-{feature}
title: "{Feature Name}"
version: 1.0.0
status: draft
---

# {Feature Name}

## Overview
{Generated from synthesis summary}

## Requirements

### Functional Requirements

#### REQ-F-001: {Title}
**Priority:** MUST
**Source:** Interview with Product Manager

The system shall {requirement text}.

**Acceptance Criteria:**
- Given {context}, When {action}, Then {outcome}
```

### EARS (Easy Approach to Requirements Syntax)

Transforms to EARS patterns:

```yaml
# Output: .requirements/{domain}/exports/EARS-{timestamp}.md

## Ubiquitous Requirements
- The system shall {capability}.

## Event-Driven Requirements
- When {trigger}, the system shall {response}.

## State-Driven Requirements
- While {state}, the system shall {behavior}.

## Unwanted Behavior Requirements
- If {condition}, then the system shall {response}.

## Optional Feature Requirements
- Where {feature enabled}, the system shall {behavior}.
```

### Gherkin (BDD)

Transforms to Gherkin feature files:

```gherkin
# Output: .requirements/{domain}/exports/{feature}.feature

Feature: {Feature Name}
  As a {role}
  I want {capability}
  So that {benefit}

  Scenario: {Scenario from acceptance criteria}
    Given {precondition}
    When {action}
    Then {expected result}
```

### Markdown

Human-readable documentation format:

```markdown
# {Domain} Requirements

## Executive Summary
{Generated overview}

## Functional Requirements
| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| REQ-F-001 | {text} | Must | Interview |

## Non-Functional Requirements
...
```

### YAML/JSON

Machine-readable formats for integration:

```yaml
# Output: .requirements/{domain}/exports/requirements.yaml
domain: "{domain}"
exported: "{ISO-8601}"
format_version: "1.0"

requirements:
  - id: REQ-F-001
    text: "{requirement}"
    category: functional
    priority: must
    source: interview
    confidence: high
```

## Workflow

### Step 1: Load Synthesized Requirements

Read from `.requirements/{domain}/synthesis/` folder.

### Step 2: Apply Filters

If --filter specified:

- Filter by priority (must, should, could)
- Filter by category (functional, non_functional, constraint)
- Filter by confidence (high, medium, low)
- Filter by source (interview, document, simulation, research)

### Step 3: Transform Format

Apply format-specific transformations:

```yaml
transformations:
  canonical:
    - Map priorities to MoSCoW
    - Generate acceptance criteria from requirements
    - Create spec.md structure

  ears:
    - Classify requirements by EARS pattern
    - Rewrite in EARS syntax
    - Group by pattern type

  gherkin:
    - Extract scenarios from acceptance criteria
    - Generate Given/When/Then structures
    - Create feature files
```

### Step 4: Quality Check

Verify export quality:

- All requirements included
- Format compliance
- Traceability preserved

### Step 5: Save Output

Save to appropriate location with clear filename.

## Examples

### Export to Canonical Format

```bash
/requirements-elicitation:export --domain "authentication" --to canonical
```

Output:

```text
Exporting: authentication
Format: canonical

Loading synthesis: SYN-20251225-160000.yaml
Requirements found: 32

Transforming to canonical format...
  Functional requirements: 20
  Non-functional requirements: 8
  Constraints: 3
  Assumptions: 1

Quality check:
  ✓ All requirements mapped
  ✓ Priorities converted to MoSCoW
  ✓ Acceptance criteria generated for 18/20 functional requirements
  ⚠ 2 requirements need manual acceptance criteria

Saved to: .specs/authentication/spec.md

Next step: Review and refine specifications as needed
```

### Export to EARS Format

```bash
/requirements-elicitation:export --domain "checkout" --to ears
```

Output:

```text
Exporting: checkout
Format: EARS

Loading synthesis: SYN-20251225-163000.yaml
Requirements found: 28

Classifying by EARS pattern...
  Ubiquitous: 8
  Event-driven: 12
  State-driven: 4
  Unwanted behavior: 3
  Optional feature: 1

Saved to: .requirements/checkout/exports/EARS-20251225-170000.md

Sample transformations:
  Original: "Users must be able to add items to cart"
  EARS: "The system shall allow users to add items to the shopping cart."

  Original: "Show error when payment fails"
  EARS: "If payment processing fails, then the system shall display an error message to the user."
```

### Export to Gherkin

```bash
/requirements-elicitation:export --domain "user-registration" --to gherkin
```

Output:

```text
Exporting: user-registration
Format: Gherkin

Loading synthesis: SYN-20251225-164500.yaml
Requirements found: 15

Generating feature files...
  user_registration.feature: 8 scenarios
  email_verification.feature: 4 scenarios
  profile_setup.feature: 3 scenarios

Saved to: .requirements/user-registration/exports/features/

Sample scenario:
  Feature: User Registration
    Scenario: Successful registration with valid email
      Given I am on the registration page
      When I enter a valid email "user@example.com"
      And I enter a password meeting complexity requirements
      And I click the Register button
      Then I should see a verification email sent message
      And a verification email should be sent to "user@example.com"
```

### Filtered Export

```bash
/requirements-elicitation:export --domain "inventory" --to yaml --filter "priority:must,confidence:high"
```

Output:

```text
Exporting: inventory
Format: YAML
Filters: priority=must, confidence=high

Loading synthesis: SYN-20251225-165000.yaml
Total requirements: 42
After filtering: 18

Saved to: .requirements/inventory/exports/requirements-must-high.yaml

Filtered summary:
  Functional: 12
  Non-functional: 4
  Constraints: 2
```

## Output Locations

```yaml
output_locations:
  canonical: ".specs/{domain}/spec.md"
  ears: ".requirements/{domain}/exports/EARS-{timestamp}.md"
  gherkin: ".requirements/{domain}/exports/features/*.feature"
  markdown: ".requirements/{domain}/exports/requirements-{timestamp}.md"
  yaml: ".requirements/{domain}/exports/requirements-{timestamp}.yaml"
  json: ".requirements/{domain}/exports/requirements-{timestamp}.json"
```

## Quality Gates

Before export completes, verify:

```yaml
quality_gates:
  traceability:
    check: "All requirements have source attribution"
    action_if_fail: "Warn user, proceed anyway"

  completeness:
    check: "No critical gaps in synthesis"
    action_if_fail: "Warn user, suggest gap-filling first"

  conflicts:
    check: "No unresolved conflicts"
    action_if_fail: "Warn user, export with conflict markers"

  acceptance_criteria:
    check: "Functional requirements have acceptance criteria"
    action_if_fail: "Generate basic criteria, flag for review"
```

## Error Handling

```yaml
error_handling:
  no_synthesis:
    message: "No synthesized requirements found for domain"
    action: "Run /discover first to elicit requirements"

  empty_after_filter:
    message: "No requirements match filter criteria"
    action: "Suggest broader filter or show available options"

  format_unsupported:
    message: "Export format not recognized"
    action: "List supported formats"
```
