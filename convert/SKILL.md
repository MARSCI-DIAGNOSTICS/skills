---
name: convert
description: "Convert specification between formats (EARS, Gherkin, Kiro, canonical)."
argument-hint: "<source path> --to <format>"
allowed-tools: Read, Glob, Grep, Write, Edit, Skill, Task
---

# Convert Specification Format

Convert specifications between different formats while preserving semantic meaning.

## Supported Formats

| Format | Description | Extension |
| --- | --- | --- |
| `canonical` | Canonical specification format | `.md` |
| `ears` | EARS-only requirements list | `.md` |
| `gherkin` | Gherkin feature file | `.feature` |
| `kiro` | AWS Kiro structure | `requirements.md`, `design.md`, `tasks.md` |
| `userstory` | Agile user stories | `.md` |

## Workflow

1. **Detect Source Format**
   - Read source file
   - Analyze structure to determine format
   - Parse content

2. **Select Converter**
   - Based on source and target formats:
     - EARS ↔ Canonical: `spec-converter ears` agent
     - Gherkin ↔ Canonical: `spec-converter gherkin` agent
     - Kiro ↔ Canonical: `spec-converter kiro` agent

3. **Execute Conversion**
   - Invoke appropriate converter agent
   - Preserve semantic meaning
   - Map identifiers appropriately

4. **Validate Output**
   - Check target format compliance
   - Verify no content lost
   - Report conversion summary

5. **Save Result**
   - Write to specified output path
   - Or derive path from source

## Arguments

- `$1` - Source file path
- `--to` - Target format (canonical, ears, gherkin, kiro, userstory)
- `--output` - Output file path (optional)

## Examples

```bash
# Convert EARS to Gherkin
/spec-driven-development:convert requirements.md --to gherkin

# Convert Gherkin to canonical
/spec-driven-development:convert auth.feature --to canonical

# Convert to Kiro format
/spec-driven-development:convert .specs/auth/spec.md --to kiro

# Specify output path
/spec-driven-development:convert spec.md --to gherkin --output tests/auth.feature
```

## Conversion Matrix

| From → To | Canonical | EARS | Gherkin | Kiro |
| --- | --- | --- | --- | --- |
| Canonical | - | ✓ | ✓ | ✓ |
| EARS | ✓ | - | ✓ | ✓ |
| Gherkin | ✓ | ✓ | - | ✓ |
| Kiro | ✓ | ✓ | ✓ | - |

## Conversion Notes

### EARS ↔ Gherkin

- EARS "WHEN...SHALL" maps to Gherkin "When...Then"
- State-Driven EARS maps to Given preconditions
- Unwanted EARS maps to negative scenarios

### Canonical ↔ Kiro

- Kiro uses EARS syntax natively
- requirements.md ↔ Functional Requirements
- design.md ↔ Design section
- tasks.md ↔ Implementation tasks

## Related Commands

- `/spec-driven-development:ears-convert` - EARS-specific conversion
- `/spec-driven-development:gherkin-convert` - Gherkin-specific conversion
- `/spec-driven-development:kiro-sync` - Kiro synchronization
