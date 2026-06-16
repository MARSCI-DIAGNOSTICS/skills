---
name: ears-convert
description: "Convert specifications to/from EARS format."
argument-hint: "<source file> [--to ears|canonical|prose|gherkin]"
allowed-tools: Read, Glob, Grep, Write, Edit, Skill, Task
---

# EARS Format Conversion

Convert specifications between EARS format and other formats.

## Supported Conversions

| From | To | Description |
| --- | --- | --- |
| Prose | EARS | Natural language to structured EARS |
| EARS | Prose | EARS to readable natural language |
| EARS | Gherkin | EARS to Given/When/Then scenarios |
| Gherkin | EARS | Gherkin scenarios to EARS requirements |
| EARS | Canonical | EARS list to canonical specification |
| Canonical | EARS | Extract EARS requirements from spec |

## Workflow

1. **Load Source**
   - Read source file
   - Detect current format

2. **Analyze Content**
   - Parse requirements or scenarios
   - Identify patterns and structure

3. **Convert**
   - Spawn `spec-converter ears` agent
   - Transform to target format
   - Preserve semantic meaning

4. **Validate**
   - Check target format compliance
   - Verify content preservation

5. **Output**
   - Write to file or display

## Arguments

- `$1` - Source file path
- `--to` - Target format: ears, canonical, prose, gherkin
- `--output` - Output file path (optional)

## Examples

```bash
# Prose to EARS
/spec-driven-development:ears-convert requirements.txt --to ears

# EARS to Gherkin
/spec-driven-development:ears-convert ears-requirements.md --to gherkin

# EARS to readable prose
/spec-driven-development:ears-convert spec.md --to prose

# Specify output
/spec-driven-development:ears-convert input.md --to ears --output output.md
```

## Conversion Examples

### Prose → EARS

**Input (Prose):**

```text
Users should be able to log in using their email and password.
The system needs to validate credentials before granting access.
```

**Output (EARS):**

```markdown
## FR-1: User Authentication

WHEN the user submits login credentials,
the system SHALL validate the email and password
AND grant access if credentials are valid.
```

### EARS → Gherkin

**Input (EARS):**

```markdown
WHEN the user submits valid credentials,
the system SHALL create a session token.
```

**Output (Gherkin):**

```gherkin
Scenario: Successful login creates session
  Given a user with valid credentials
  When the user submits the login form
  Then a session token is created
  And the user is redirected to dashboard
```

### EARS → Prose

**Input (EARS):**

```markdown
WHILE the user is authenticated,
the system SHALL display the user's name in the header.
```

**Output (Prose):**

```text
When a user is logged in, the system shows their name in the page header.
This ensures users can confirm they're using the correct account.
```

## Pattern Preservation

The converter preserves EARS pattern semantics:

| EARS Pattern | Preserved As |
| --- | --- |
| WHEN...SHALL | Gherkin When...Then |
| WHILE...SHALL | Gherkin Given (state)...Then |
| IF...THEN...SHALL | Gherkin error scenario |
| WHERE...SHALL | Gherkin @tag scenario |

## Related Commands

- `/spec-driven-development:ears-author` - Create EARS requirements
- `/spec-driven-development:gherkin-convert` - Gherkin conversions
- `/spec-driven-development:convert` - General format conversion
