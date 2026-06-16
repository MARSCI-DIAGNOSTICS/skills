---
name: refine
description: "Refine specification with AI-assisted improvements."
argument-hint: "<path to specification file>"
allowed-tools: Read, Glob, Grep, Write, Edit, Skill, Task
---

# Refine Specification

Apply AI-assisted refinement to improve specification quality.

## Workflow

1. **Load Specification**
   - Read the specification file
   - Parse all requirements and acceptance criteria

2. **Analyze Quality**
   - Spawn `spec-processor refine` agent
   - Evaluate against INVEST criteria
   - Score clarity and completeness
   - Identify improvement opportunities

3. **Generate Suggestions**
   - Clarity enhancements
   - Missing acceptance criteria
   - Ambiguity resolution
   - Requirement splitting recommendations
   - Priority adjustments

4. **Present Improvements**
   - Show suggestions grouped by category
   - Indicate impact level (high/medium/low)
   - Provide before/after comparisons

5. **Apply Changes**
   - Interactive: Confirm each change
   - Batch: Apply all approved changes
   - Update specification file

## Arguments

- `$ARGUMENTS` - Path to specification file
- `--auto` - Apply all improvements without confirmation
- `--focus` - Focus area: clarity, completeness, testability, or all

## Examples

```bash
# Interactive refinement
/spec-driven-development:refine .specs/user-auth/spec.md

# Auto-apply all improvements
/spec-driven-development:refine .specs/user-auth/spec.md --auto

# Focus on clarity
/spec-driven-development:refine .specs/user-auth/spec.md --focus clarity
```

## Refinement Categories

### Clarity Enhancements

- Remove ambiguous words (some, few, many, etc.)
- Add specific values and thresholds
- Clarify actor and system boundaries

### Completeness Improvements

- Add missing acceptance criteria
- Add edge case scenarios
- Add error handling requirements

### Testability Improvements

- Make outcomes observable
- Add verification methods
- Specify expected values

### Structure Improvements

- Split large requirements
- Consolidate duplicates
- Improve requirement ordering

## Refinement Report

```markdown
# Refinement Report: user-auth

## Summary
- **Improvements Found:** 8
- **High Impact:** 3
- **Medium Impact:** 4
- **Low Impact:** 1

## Improvements

### HIGH: FR-2 - Ambiguous Threshold
**Before:**
> The system SHALL respond quickly to login requests.

**After:**
> The system SHALL respond to login requests within 500ms (p95).

**Rationale:** "quickly" is ambiguous; specific SLA is testable.

---

### MEDIUM: FR-1 - Missing Error Case
**Added AC:**
> Given the email format is invalid, when submitted, then display "Invalid email format" error.

**Rationale:** Original ACs only covered happy path.
```

## Related Commands

- `/spec-driven-development:validate` - Validate specification
- `/spec-driven-development:audit` - Full quality audit
- `/spec-driven-development:specify` - Generate new specification
