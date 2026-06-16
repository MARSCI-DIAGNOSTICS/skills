---
name: generate-cases
description: Generate systematic test cases using formal techniques (equivalence partitioning, boundary value analysis, decision tables). Use for comprehensive test coverage design.
allowed-tools: Read, Write, Glob, Grep, Skill, Task
argument-hint: <requirement-or-feature>
---

# Generate Test Cases Command

Generate comprehensive test cases for a requirement or feature using formal test design techniques.

## Process

### Step 1: Parse Input

The requirement/feature can be:

- A requirement ID (REQ-001) - look up in docs
- A feature description - analyze directly
- A file path - read the specification

### Step 2: Load Skills

Invoke the `test-strategy:test-case-design` skill for technique guidance.

### Step 3: Analyze Test Space

Identify:

- **Inputs**: All parameters and their valid/invalid ranges
- **States**: Any state-dependent behavior
- **Conditions**: Business rules with multiple conditions
- **Outputs**: Expected results for each scenario

### Step 4: Delegate to Agent

Spawn the `test-case-generator` agent:

```text
Generate systematic test cases for the following:

[Requirement/Feature Description]

Apply these techniques:
1. Equivalence Partitioning - identify valid/invalid classes
2. Boundary Value Analysis - test at edges
3. Decision Tables - if multiple conditions exist
4. State Transition - if state-dependent behavior

Output:
1. Test case specifications in markdown
2. .NET xUnit code if applicable
```

### Step 5: Organize Output

Structure test cases by category:

```markdown
## Test Cases: [Feature Name]

### Positive Tests (Happy Path)
| TC-ID | Description | Input | Expected |
|-------|-------------|-------|----------|
| TC-001 | Valid minimum | 18 | Accept |
| TC-002 | Valid standard | 40 | Accept |

### Negative Tests (Validation)
| TC-ID | Description | Input | Expected |
|-------|-------------|-------|----------|
| TC-003 | Below minimum | 17 | Reject |
| TC-004 | Null input | null | Error |

### Boundary Tests
| TC-ID | Description | Input | Expected |
|-------|-------------|-------|----------|
| TC-005 | At minimum | 18 | Accept |
| TC-006 | At maximum | 65 | Accept |

### Edge Cases
| TC-ID | Description | Input | Expected |
|-------|-------------|-------|----------|
| TC-007 | Zero value | 0 | Reject |
| TC-008 | Negative | -1 | Reject |
```

### Step 6: Generate Code (Optional)

If .NET project detected, generate xUnit tests:

```csharp
public class [Feature]Tests
{
    // Boundary value tests
    [Theory]
    [InlineData(17, false)]
    [InlineData(18, true)]
    [InlineData(65, true)]
    [InlineData(66, false)]
    public void Validate_BoundaryValues_ReturnsExpected(int input, bool expected)
    {
        var result = _validator.Validate(input);
        Assert.Equal(expected, result);
    }
}
```

### Step 7: Report

```markdown
## Test Cases Generated

**Feature**: [Name]
**Techniques Applied**: [List]
**Total Test Cases**: [Count]

| Category | Count |
|----------|-------|
| Positive | X |
| Negative | Y |
| Boundary | Z |
| Edge Cases | W |

**Files Created**:
- [path/to/test-cases.md]
- [path/to/Tests.cs] (if applicable)

**Coverage Notes**:
- All input partitions covered
- Boundary values tested
- [Any gaps or assumptions]
```

## Examples

**From description:**

```bash
/test-strategy:generate-cases "Age validation: accept ages 18-65"
```

**From requirement:**

```bash
/test-strategy:generate-cases REQ-015
```

**From file:**

```bash
/test-strategy:generate-cases docs/requirements/user-registration.md
```
