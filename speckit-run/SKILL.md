---
name: speckit-run
description: "Execute the complete GitHub Spec Kit 5-phase workflow from constitution to implementation."
argument-hint: "<feature request or --resume>"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Skill, Task
---

# Run Spec Kit Workflow

Execute the complete GitHub Spec Kit 5-phase specification-driven development workflow.

## The 5 Phases

```text
┌─────────────────────────────────────────────────────────────┐
│                    SPEC KIT WORKFLOW                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Phase 0: CONSTITUTION                                     │
│   Define project principles and constraints                 │
│        ↓ [Constitution exists and is valid]                 │
│                                                             │
│   Phase 1: SPECIFY                                          │
│   Generate canonical specification from feature request     │
│        ↓ [Spec validates, INVEST score ≥ 7]                 │
│                                                             │
│   Phase 2: PLAN                                             │
│   Create implementation design and approach                 │
│        ↓ [Design covers all requirements]                   │
│                                                             │
│   Phase 3: TASKS                                            │
│   Break down into implementable task list                   │
│        ↓ [Tasks map to requirements]                        │
│                                                             │
│   Phase 4: IMPLEMENT                                        │
│   Execute tasks with continuous validation                  │
│        ↓ [All ACs pass]                                     │
│                                                             │
│   ✓ COMPLETE                                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Workflow

1. **Initialize**
   - Spawn `speckit-runner` agent (Opus)
   - Check for existing constitution
   - Determine starting phase

2. **Phase 0: Constitution**
   - Check for `.constitution.md`
   - If missing, create with project principles
   - Validate constitution structure

3. **Phase 1: Specify**
   - Invoke `spec-processor generate` agent
   - Generate canonical specification
   - Validate with `spec-reviewer validate`
   - Gate: INVEST score ≥ 7

4. **Phase 2: Plan**
   - Analyze codebase
   - Generate implementation design
   - Map design to requirements
   - Gate: All requirements covered

5. **Phase 3: Tasks**
   - Break into vertical slices
   - Generate task breakdown
   - Map tasks to requirements
   - Gate: All requirements have tasks

6. **Phase 4: Implement**
   - Execute tasks in order
   - Validate acceptance criteria
   - Run tests
   - Gate: All ACs pass

7. **Complete**
   - Generate completion report
   - Update specification status
   - Archive workflow artifacts

## Arguments

- `$ARGUMENTS` - Feature request description
- `--resume` - Resume from last checkpoint
- `--phase` - Start from specific phase (0-4)
- `--skip-constitution` - Skip Phase 0 if constitution exists

## Examples

```bash
# Full workflow from feature request
/spec-driven-development:speckit-run "User authentication with email and OAuth"

# Resume interrupted workflow
/spec-driven-development:speckit-run --resume

# Start from Phase 2 (existing spec)
/spec-driven-development:speckit-run --phase 2 .specs/auth/spec.md

# Skip constitution check
/spec-driven-development:speckit-run "New feature" --skip-constitution
```

## Progress Tracking

The runner maintains checkpoints:

```markdown
## Spec Kit Workflow: user-auth

**Started:** 2024-01-15T09:00:00Z
**Status:** Phase 2 - Plan

### Progress

| Phase | Status | Started | Completed |
| --- | --- | --- | --- |
| 0. Constitution | ✓ Complete | 09:00 | 09:02 |
| 1. Specify | ✓ Complete | 09:02 | 09:15 |
| 2. Plan | 🔄 In Progress | 09:15 | - |
| 3. Tasks | ⏳ Pending | - | - |
| 4. Implement | ⏳ Pending | - | - |

### Artifacts

- Constitution: .constitution.md ✓
- Specification: .specs/user-auth/spec.md ✓
- Design: .specs/user-auth/design.md (in progress)
- Tasks: pending
```

## Validation Gates

Each phase has quality gates:

| Phase | Gate Criteria |
| --- | --- |
| Constitution | File exists, required sections present |
| Specify | Schema valid, EARS format, INVEST ≥ 7 |
| Plan | All requirements addressed, components defined |
| Tasks | All requirements have tasks, < 1 day each |
| Implement | All ACs pass, tests pass |

## Rollback Support

If a phase fails:

```markdown
## Rollback Required

**Phase:** 2 (Plan)
**Reason:** Design does not cover FR-3

### Options

1. [Retry] Re-run Phase 2 with updated context
2. [Rollback] Return to Phase 1 and update spec
3. [Skip] Mark FR-3 as out-of-scope and continue
```

## Completion Report

```markdown
# Spec Kit Workflow Complete

**Feature:** User Authentication
**Duration:** 09:00 - 11:30 (2h 30m)
**Status:** ✓ SUCCESS

## Phase Summary

| Phase | Duration | Artifacts | Issues |
| --- | --- | --- | --- |
| Constitution | 2m | .constitution.md | 0 |
| Specify | 13m | spec.md | 0 |
| Plan | 18m | design.md | 1 (resolved) |
| Tasks | 12m | tasks.md | 0 |
| Implement | 85m | 12 files | 2 (resolved) |

## Requirements Delivered

| ID | Title | Status | ACs |
| --- | --- | --- | --- |
| FR-1 | Email Login | ✓ | 4/4 |
| FR-2 | OAuth Login | ✓ | 3/3 |
| FR-3 | Session Management | ✓ | 5/5 |
```

## Related Commands

- `/spec-driven-development:specify` - Phase 1 only
- `/spec-driven-development:plan` - Phase 2 only
- `/spec-driven-development:tasks` - Phase 3 only
- `/spec-driven-development:implement` - Phase 4 only
- `/spec-driven-development:constitution` - Phase 0 only
