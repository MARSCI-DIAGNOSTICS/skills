---
name: gherkin-convert
description: "Convert specifications to/from Gherkin/BDD format."
argument-hint: "<source file> [--to gherkin|canonical|ears|feature]"
allowed-tools: Read, Glob, Grep, Write, Edit, Skill, Task
---

# Gherkin Format Conversion

Convert specifications between Gherkin/BDD format and other formats.

## Supported Conversions

| From | To | Description |
| --- | --- | --- |
| EARS | Gherkin | EARS requirements to scenarios |
| Gherkin | EARS | Scenarios to EARS requirements |
| Canonical | Gherkin | Full spec to feature file |
| Gherkin | Canonical | Feature file to canonical spec |
| Inline AC | Feature | Inline criteria to .feature |
| Feature | Inline AC | .feature to inline criteria |

## Workflow

1. **Load Source**
   - Read source file
   - Detect current format

2. **Parse Content**
   - Extract requirements/scenarios
   - Identify structure

3. **Convert**
   - Spawn `spec-converter gherkin` agent
   - Transform to target format
   - Apply best practices

4. **Validate**
   - Check Gherkin syntax
   - Verify completeness

5. **Output**
   - Write .feature file or specification

## Arguments

- `$1` - Source file path
- `--to` - Target format: gherkin, feature, canonical, ears, inline
- `--output` - Output file path (optional)

## Examples

```bash
# Canonical spec to feature file
/spec-driven-development:gherkin-convert .specs/auth/spec.md --to feature

# Feature file to canonical
/spec-driven-development:gherkin-convert tests/login.feature --to canonical

# EARS to Gherkin
/spec-driven-development:gherkin-convert ears-requirements.md --to gherkin

# Inline to feature file
/spec-driven-development:gherkin-convert spec.md --to feature --output tests/spec.feature
```

## Conversion Examples

### EARS → Gherkin

**Input (EARS):**

```markdown
## FR-1: User Login

WHEN the user submits valid credentials,
the system SHALL authenticate the user
AND redirect to the dashboard.

### Acceptance Criteria
- AC-1.1: Valid credentials grant access
- AC-1.2: Invalid password shows error
```

**Output (Gherkin):**

```gherkin
Feature: User Login
  As a user
  I want to log in with my credentials
  So that I can access the dashboard

  # FR-1: User Login
  Scenario: Successful login with valid credentials
    Given a registered user exists
    When the user submits valid credentials
    Then the user is authenticated
    And the user is redirected to the dashboard

  Scenario: Failed login with invalid password
    Given a registered user exists
    When the user submits an invalid password
    Then an error message is displayed
    And the user remains on the login page
```

### Canonical → Feature File

**Input (Canonical):**

```markdown
# Specification: Shopping Cart

## FR-1: Add to Cart

WHEN the user clicks "Add to Cart",
the system SHALL add the item to the user's cart.

### Acceptance Criteria
- [ ] AC-1.1: Given product page, when clicking add, then item in cart
- [ ] AC-1.2: Given item in cart, when adding again, then quantity increases
```

**Output (Feature):**

```gherkin
# Specification: Shopping Cart
# Generated from: .specs/cart/spec.md

Feature: Shopping Cart
  As a shopper
  I want to add items to my cart
  So that I can purchase them

  @FR-1
  Scenario: Add item to cart from product page
    Given I am viewing a product page
    When I click "Add to Cart"
    Then the item is added to my cart

  @FR-1
  Scenario: Increase quantity when adding existing item
    Given I have an item in my cart
    When I add the same item again
    Then the item quantity increases by 1
```

## Pattern Mapping

| EARS Pattern | Gherkin Mapping |
| --- | --- |
| WHEN...SHALL | Scenario with When/Then |
| WHILE...SHALL | Given (continuous state) |
| IF...THEN...SHALL | Error/edge case scenario |
| WHERE...SHALL | @tag for feature toggle |
| Ubiquitous | Background or invariant check |

## Related Commands

- `/spec-driven-development:gherkin-author` - Create Gherkin scenarios
- `/spec-driven-development:ears-convert` - EARS conversions
- `/spec-driven-development:convert` - General format conversion
