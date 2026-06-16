---
name: gherkin-author
description: "Interactive Gherkin scenario authoring. Guides through Given/When/Then construction with BDD best practices."
argument-hint: "[feature description or --interactive]"
allowed-tools: Read, Glob, Grep, Write, Edit, Skill, Task
---

# Gherkin Scenario Authoring

Interactive assistant for creating Gherkin/BDD scenarios with best practices.

## Gherkin Keywords

| Keyword | Purpose | Example |
| --- | --- | --- |
| Feature | Describes the feature | Feature: User Login |
| Scenario | Single test case | Scenario: Successful login |
| Given | Precondition/context | Given a registered user |
| When | Action/trigger | When they enter credentials |
| Then | Expected outcome | Then they are logged in |
| And | Continue previous | And a session is created |
| But | Negative continuation | But no email is sent |
| Background | Shared setup | Background: Given logged in |
| Scenario Outline | Parameterized | Examples table |

## Workflow

1. **Gather Context**
   - If argument provided, analyze feature description
   - If `--interactive`, guide through scenario creation

2. **Feature Identification**
   - Spawn `spec-author gherkin` agent
   - Identify the feature being tested
   - Determine user persona (As a...)

3. **Scenario Construction**
   - Define preconditions (Given)
   - Specify action (When) - single action only
   - Describe outcomes (Then)
   - Add supporting steps (And/But)

4. **Best Practices Check**
   - Declarative over imperative
   - Single When per scenario
   - Observable outcomes
   - Independent scenarios

5. **Output**
   - Generate .feature file or inline criteria
   - Optionally include Reqnroll/.NET hints

## Arguments

- `$ARGUMENTS` - Feature description
- `--interactive` - Step-by-step guided authoring
- `--output` - Output .feature file path
- `--format` - Output format: feature (default), inline

## Examples

```bash
# From description
/spec-driven-development:gherkin-author "User can add items to shopping cart"

# Interactive mode
/spec-driven-development:gherkin-author --interactive

# Output to file
/spec-driven-development:gherkin-author "Login feature" --output tests/login.feature

# Inline acceptance criteria format
/spec-driven-development:gherkin-author "Password reset" --format inline
```

## Scenario Quality Checklist

```text
SCENARIO QUALITY CHECK

[✓] Name describes behavior (not implementation)
[✓] Given establishes necessary context only
[✓] When has exactly ONE action
[✓] Then has observable, verifiable outcomes
[✓] Uses business language, not technical jargon
[✓] Independent of other scenarios
[✓] Focused on one behavior
[✓] Can be automated
```

## Anti-Patterns to Avoid

| Anti-Pattern | Example | Better |
| --- | --- | --- |
| UI-coupled | "When I click the blue button" | "When I submit the form" |
| Imperative | "When I type 'john' in field" | "When I enter credentials" |
| Too many Ands | Given X And Y And Z... | Use Background |
| Testing code | "Then database has record" | "Then user is registered" |
| Vague Then | "Then it works" | "Then I see confirmation" |

## Output Format

### Feature File (.feature)

```gherkin
Feature: Shopping Cart
  As a shopper
  I want to add items to my cart
  So that I can purchase them later

  Background:
    Given I am logged in as a customer
    And the product catalog is available

  Scenario: Add single item to empty cart
    Given my cart is empty
    When I add "Widget" to my cart
    Then my cart contains 1 item
    And the cart total reflects the item price

  Scenario: Add item already in cart
    Given my cart contains 1 "Widget"
    When I add another "Widget"
    Then my cart contains 2 "Widget"
    And the cart total is updated
```

### Inline Acceptance Criteria

```markdown
### Acceptance Criteria

- [ ] AC-1: Given empty cart, when adding item, then cart contains 1 item
- [ ] AC-2: Given item in cart, when adding same item, then quantity increases
- [ ] AC-3: Given item in cart, when removing item, then cart is empty
```

## Related Commands

- `/spec-driven-development:gherkin-convert` - Convert between formats
- `/spec-driven-development:ears-author` - Create EARS requirements
- `/spec-driven-development:specify` - Generate full specification
