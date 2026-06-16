---
name: userstory-author
description: "Author Agile-style user stories with linked acceptance criteria."
argument-hint: "<feature description or --interactive>"
allowed-tools: Read, Glob, Grep, Write, Edit, Skill, Task
---

# User Story Authoring

Create Agile-style user stories with acceptance criteria.

## User Story Format

```markdown
## US-XXX: [Short Title]

**As a** [type of user/persona],
**I want** [goal/desire],
**So that** [benefit/value].

### Acceptance Criteria

- [ ] AC-1: Given [context], when [action], then [outcome]
- [ ] AC-2: Given [context], when [action], then [outcome]

### Notes

- [Additional context]
- [Dependencies]
```

## Workflow

1. **Gather Context**
   - If argument provided, analyze description
   - If `--interactive`, guide through story creation

2. **Identify User**
   - Spawn `spec-author userstory` agent
   - Define the persona:
     - Who is the user?
     - What is their goal?
     - What pain point do they have?

3. **Define the Want**
   - Focus on goal, not solution
   - "I want to find products" not "I want a search box"

4. **Articulate Value**
   - Connect to business value
   - Save time, increase revenue, reduce risk

5. **Write Acceptance Criteria**
   - Use Given/When/Then format
   - Cover happy path and edge cases

6. **Validate with INVEST**
   - Independent, Negotiable, Valuable
   - Estimable, Small, Testable
   - Score must be ≥ 7

7. **Output**
   - Display formatted story
   - Suggest splitting if too large

## INVEST Criteria

| Criterion | Question | Score |
| --- | --- | --- |
| Independent | Can be delivered alone? | 0-2 |
| Negotiable | Describes what, not how? | 0-2 |
| Valuable | Delivers user/business value? | 0-2 |
| Estimable | Team can estimate effort? | 0-2 |
| Small | Fits in one sprint? | 0-2 |
| Testable | Has clear pass/fail criteria? | 0-2 |

**Threshold:** Score 7+ to proceed, otherwise split or refine.

## Arguments

- `$ARGUMENTS` - Feature description
- `--interactive` - Step-by-step guided authoring
- `--persona` - Specify user persona
- `--append` - Append to specification file

## Examples

```bash
# From description
/spec-driven-development:userstory-author "Search for products by keyword"

# Interactive mode
/spec-driven-development:userstory-author --interactive

# With specific persona
/spec-driven-development:userstory-author "View order history" --persona "returning customer"

# Append to spec
/spec-driven-development:userstory-author "Reset password" --append .specs/auth/spec.md
```

## Story Splitting Patterns

If INVEST score is low, the agent suggests splitting:

### Split by User Type

**Before:** "As a user, I want to see a dashboard"

**After:**

- "As an admin, I want to see system metrics dashboard"
- "As a sales rep, I want to see my pipeline dashboard"

### Split by Workflow Steps

**Before:** "As a user, I want to complete checkout"

**After:**

- "As a user, I want to review my cart"
- "As a user, I want to enter shipping info"
- "As a user, I want to confirm my order"

### Split by Operations (CRUD)

**Before:** "As a user, I want to manage my profile"

**After:**

- "As a user, I want to view my profile"
- "As a user, I want to update my profile"
- "As a user, I want to delete my account"

## Output Example

```markdown
## US-001: Search Products by Keyword

**As a** shopper,
**I want** to search for products using keywords,
**So that** I can quickly find items I'm interested in purchasing.

### Acceptance Criteria

- [ ] AC-1: Given I am on the product listing page, when I enter "laptop"
  in the search box and press enter, then I see products containing
  "laptop" in title or description

- [ ] AC-2: Given I have searched for "laptop", when results are displayed,
  then I see the result count and results are sorted by relevance

- [ ] AC-3: Given I search for a term with no matches, when results are
  displayed, then I see "No products found" message with suggestions

### INVEST Score: 10/12

| I | N | V | E | S | T |
| - | - | - | - | - | - |
| 2 | 2 | 2 | 2 | 1 | 1 |

**Notes:**
- S/T slightly reduced due to search relevance complexity
- Consider spike for search ranking algorithm

### Dependencies

- Product catalog must be indexed
- Search infrastructure required

### Priority

Must (core shopping functionality)
```

## Related Commands

- `/spec-driven-development:gherkin-author` - Create Gherkin scenarios
- `/spec-driven-development:ears-author` - Create EARS requirements
- `/spec-driven-development:specify` - Generate full specification
