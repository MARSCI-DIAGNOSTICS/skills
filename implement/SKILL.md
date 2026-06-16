---
name: implement
description: "Guide implementation of specification tasks. Phase 4 of Spec Kit workflow."
argument-hint: "<path to specification file or task ID>"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Skill, Task
---

# Guide Implementation

Guide the implementation of tasks from a specification, validating acceptance criteria as you go.

## Workflow

1. **Load Artifacts**
   - Read specification, design, and tasks
   - Identify current task to implement
   - Load relevant acceptance criteria

2. **Present Implementation Checklist**
   - Show current task details
   - Display acceptance criteria
   - List files to create/modify

3. **Guide Implementation**
   - Provide step-by-step guidance
   - Create/modify files as needed
   - Run tests after each change

4. **Validate Acceptance Criteria**
   - Check each criterion is met
   - Run verification commands
   - Mark criteria as passed/failed

5. **Update Task Status**
   - Mark task as complete
   - Update tasks.md
   - Show progress summary
   - Suggest next task

## Arguments

- `$ARGUMENTS` - Path to specification file OR specific task ID (e.g., "TASK-1")

## Examples

```bash
# Start implementing from specification
/spec-driven-development:implement .specs/user-auth/spec.md

# Implement specific task
/spec-driven-development:implement TASK-3

# Continue with next task
/spec-driven-development:implement --next
```

## Implementation Session

During implementation, the command provides:

### Task Context

```text
╔══════════════════════════════════════╗
║  TASK-3: Create login endpoint       ║
╠══════════════════════════════════════╣
║  Requirement: FR-1                   ║
║  Depends On: TASK-1 ✓, TASK-2 ✓      ║
╚══════════════════════════════════════╝
```

### Acceptance Criteria Tracker

```text
Acceptance Criteria:
[✓] AC-1.1: Given valid credentials, login succeeds
[ ] AC-1.2: Given invalid password, returns 401
[ ] AC-1.3: Given locked account, returns 403
```

### Progress Summary

```text
Feature Progress: 3/8 tasks complete (37%)
Current Task: TASK-3 (2/3 criteria met)
```

## Related Commands

- `/spec-driven-development:specify` - Generate specification (Phase 1)
- `/spec-driven-development:plan` - Generate design (Phase 2)
- `/spec-driven-development:tasks` - Generate task breakdown (Phase 3)
- `/spec-driven-development:validate` - Validate specification
